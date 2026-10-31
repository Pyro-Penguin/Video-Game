import unittest
from dataclasses import replace

from demo_scenario import run_demo_scenario

from battle_sim import (
    ACTIVE, DEFEATED, RESERVE, ActionCommand, BattleResolver,
    BattleValidationError, ConfiguredVictoryPolicy, MoveDefinition,
    build_battle_facts, make_test_battle, make_test_moves,
    _finish_if_commander_defeated,
)


def commands_for(state, targets):
    return tuple(
        ActionCommand(unit.unit_id, "strike", targets[unit.unit_id])
        for unit in state.units if unit.status == ACTIVE
    )


class DoubleDamageFixture:
    def calculate_damage(self, actor, target, move):
        return move.fixture_damage * 2


class BattleSimulationTests(unittest.TestCase):
    def setUp(self):
        self.state = make_test_battle()
        self.moves = make_test_moves()
        self.resolver = BattleResolver()

    def test_fixture_has_commander_two_active_monsters_and_one_reserve(self):
        for side in ("A", "B"):
            side_units = [u for u in self.state.units if u.side_id == side]
            self.assertEqual(sum(u.kind == "commander" for u in side_units), 1)
            self.assertEqual(sum(u.kind == "monster" and u.status == ACTIVE for u in side_units), 2)
            self.assertEqual(sum(u.kind == "monster" and u.status == RESERVE for u in side_units), 1)

    def test_resolver_does_not_mutate_input_state(self):
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        result = self.resolver.resolve_turn(self.state, commands_for(self.state, targets), self.moves)
        self.assertEqual(self.state.turn_number, 1)
        self.assertEqual(next(u for u in self.state.units if u.unit_id == "B-C").vitality, 120)
        self.assertEqual(result.state.turn_number, 2)

    def test_damage_model_is_injected_without_changing_turn_resolution(self):
        resolver = BattleResolver(damage_model=DoubleDamageFixture())
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        result = resolver.resolve_turn(
            self.state, commands_for(self.state, targets), self.moves
        )
        self.assertEqual(
            next(u for u in result.state.units if u.unit_id == "B-C").vitality,
            40,
        )
        self.assertEqual(
            next(u for u in result.state.units if u.unit_id == "A-C").vitality,
            40,
        )

    def test_exact_speed_tie_uses_fixture_unit_id_fallback(self):
        tied_state = replace(
            self.state,
            units=tuple(
                replace(unit, speed=50) if unit.status == ACTIVE else unit
                for unit in self.state.units
            ),
        )
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        result = self.resolver.resolve_turn(
            tied_state, commands_for(tied_state, targets), self.moves
        )
        actors = [
            event.actor_id for event in result.events
            if event.event_type == "DamageApplied"
        ]
        self.assertEqual(actors, ["A-C", "B-C", "A-M1", "A-M2", "B-M1", "B-M2"])

    def test_exact_speed_tie_prefers_greater_supplied_type_effectiveness(self):
        tied_state = replace(
            self.state,
            units=tuple(replace(u, speed=50) if u.status == ACTIVE else u for u in self.state.units),
        )
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        commands = [
            replace(command, type_effectiveness=(2, 1)) if command.actor_id == "B-C"
            else replace(command, type_effectiveness=(1, 1))
            for command in commands_for(tied_state, targets)
        ]
        result = self.resolver.resolve_turn(tied_state, commands, self.moves)
        first_damage = next(e for e in result.events if e.event_type == "DamageApplied")
        self.assertEqual(first_damage.actor_id, "B-C")

    def test_exact_speed_tie_uses_hp_percentage_before_raw_hp(self):
        units = tuple(
            replace(u, speed=50, vitality=50) if u.unit_id == "A-C"
            else replace(u, speed=50) if u.unit_id == "B-C"
            else replace(u, speed=1) if u.status == ACTIVE else u
            for u in self.state.units
        )
        tied_state = replace(self.state, units=units)
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        result = self.resolver.resolve_turn(tied_state, commands_for(tied_state, targets), self.moves)
        first_damage = next(e for e in result.events if e.event_type == "DamageApplied")
        self.assertEqual(first_damage.actor_id, "B-C")

    def test_priority_then_speed_orders_actions(self):
        moves = dict(self.moves)
        moves["quick_strike"] = MoveDefinition("quick_strike", 25, 1)
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        commands = [
            replace(command, move_id="quick_strike") if command.actor_id == "B-M2" else command
            for command in commands_for(self.state, targets)
        ]
        result = self.resolver.resolve_turn(self.state, commands, moves)
        damage_events = [e for e in result.events if e.event_type == "DamageApplied"]
        self.assertEqual(damage_events[0].actor_id, "B-M2")
        self.assertEqual(damage_events[1].actor_id, "A-C")

    def test_defeated_actor_loses_its_queued_action(self):
        units = tuple(
            replace(u, vitality=20) if u.unit_id == "B-M1" else u
            for u in self.state.units
        )
        state = replace(self.state, units=units)
        targets = {"A-C": "B-M1", "A-M1": "B-M2", "A-M2": "B-C",
                   "B-C": "A-C", "B-M1": "A-C", "B-M2": "A-M1"}
        commands = [
            replace(command, move_id="finisher") if command.actor_id == "A-C" else command
            for command in commands_for(state, targets)
        ]
        result = self.resolver.resolve_turn(state, commands, self.moves)
        skipped = [e for e in result.events if e.event_type == "ActionSkipped"]
        self.assertTrue(any(
            e.actor_id == "B-M1" and e.detail == "actor_defeated_before_resolution"
            for e in skipped
        ))
        self.assertFalse(any(
            e.actor_id == "B-M1" and e.event_type == "DamageApplied"
            for e in result.events
        ))

    def test_target_defeated_before_action_is_not_retargeted(self):
        units = tuple(
            replace(u, vitality=20) if u.unit_id == "B-M1" else u
            for u in self.state.units
        )
        state = replace(self.state, units=units)
        targets = {"A-C": "B-M1", "A-M1": "B-M1", "A-M2": "B-C",
                   "B-C": "A-C", "B-M1": "A-C", "B-M2": "A-M1"}
        commands = [
            replace(command, move_id="finisher") if command.actor_id == "A-C" else command
            for command in commands_for(state, targets)
        ]
        result = self.resolver.resolve_turn(state, commands, self.moves)
        self.assertTrue(any(
            e.actor_id == "A-M1" and e.detail == "target_not_active_at_resolution"
            for e in result.events if e.event_type == "ActionSkipped"
        ))

    def test_reserve_deploys_only_after_all_locked_actions_resolve(self):
        units = tuple(
            replace(u, vitality=20) if u.unit_id == "B-M1" else u
            for u in self.state.units
        )
        state = replace(self.state, units=units)
        targets = {"A-C": "B-M1", "A-M1": "B-M2", "A-M2": "B-C",
                   "B-C": "A-C", "B-M1": "A-C", "B-M2": "A-M1"}
        commands = [
            replace(command, move_id="finisher") if command.actor_id == "A-C" else command
            for command in commands_for(state, targets)
        ]
        result = self.resolver.resolve_turn(state, commands, self.moves)
        reserve = next(u for u in result.state.units if u.unit_id == "B-R1")
        self.assertEqual(reserve.status, ACTIVE)
        self.assertEqual(next(u for u in result.state.units if u.unit_id == "B-M1").status, DEFEATED)
        self.assertTrue(any(e.event_type == "ReserveDeployed" for e in result.events))

    def test_multiple_reserves_require_and_honor_explicit_selection(self):
        extra_reserve = replace(
            next(u for u in self.state.units if u.unit_id == "B-R1"),
            unit_id="B-R2",
            roster_order=4,
        )
        units = tuple(
            replace(u, vitality=20) if u.unit_id == "B-M1" else u
            for u in self.state.units
        ) + (extra_reserve,)
        state = replace(self.state, units=units)
        targets = {"A-C": "B-M1", "A-M1": "B-M2", "A-M2": "B-C",
                   "B-C": "A-C", "B-M1": "A-C", "B-M2": "A-M1"}
        commands = [
            replace(command, move_id="finisher") if command.actor_id == "A-C" else command
            for command in commands_for(state, targets)
        ]
        result = self.resolver.resolve_turn(
            state, commands, self.moves, reserve_selections={"B": ("B-R2",)}
        )
        final_units = {u.unit_id: u for u in result.state.units}
        self.assertEqual(final_units["B-R2"].status, ACTIVE)
        self.assertEqual(final_units["B-R1"].status, RESERVE)
        deployed = [e.target_id for e in result.events if e.event_type == "ReserveDeployed"]
        self.assertEqual(deployed, ["B-R2"])

    def test_multiple_reserves_without_selection_are_rejected(self):
        extra_reserve = replace(
            next(u for u in self.state.units if u.unit_id == "B-R1"),
            unit_id="B-R2",
            roster_order=4,
        )
        units = tuple(
            replace(u, vitality=20) if u.unit_id == "B-M1" else u
            for u in self.state.units
        ) + (extra_reserve,)
        state = replace(self.state, units=units)
        targets = {"A-C": "B-M1", "A-M1": "B-M2", "A-M2": "B-C",
                   "B-C": "A-C", "B-M1": "A-C", "B-M2": "A-M1"}
        commands = [
            replace(command, move_id="finisher") if command.actor_id == "A-C" else command
            for command in commands_for(state, targets)
        ]
        with self.assertRaises(BattleValidationError):
            self.resolver.resolve_turn(state, commands, self.moves)

    def test_commander_knockout_ends_battle_with_other_side_winning(self):
        moves = {"strike": MoveDefinition("strike", 40, 0),
                 "finisher": MoveDefinition("finisher", 120, 0)}
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        commands = [
            replace(command, move_id="finisher") if command.actor_id == "A-C" else command
            for command in commands_for(self.state, targets)
        ]
        result = self.resolver.resolve_turn(self.state, commands, moves)
        self.assertTrue(result.state.is_finished)
        self.assertFalse(result.state.is_draw)
        self.assertEqual(result.state.winner_side_id, "A")
        self.assertTrue(any(
            event.actor_id == "A-C" and event.event_type == "DamageApplied"
            and event.target_id == "B-C"
            for event in result.events
        ))

    def test_team_wipe_policy_uses_reserves_as_remaining_monsters(self):
        units = tuple(
            replace(u, vitality=0, status=DEFEATED)
            if u.side_id == "B" and u.kind == "monster" else u
            for u in self.state.units
        )
        state = replace(self.state, units=units)
        facts = build_battle_facts(state)
        side_b = next(side for side in facts.sides if side.side_id == "B")
        self.assertEqual(side_b.active_monster_count, 0)
        self.assertEqual(side_b.reserve_monster_count, 0)
        self.assertFalse(side_b.commander_defeated)

        outcome = ConfiguredVictoryPolicy(
            commander_defeat=False, monster_team_wipe=True
        ).evaluate(facts)
        self.assertTrue(outcome.is_finished)
        self.assertEqual(outcome.winner_side_id, "A")
        self.assertFalse(outcome.is_draw)

    def test_both_victory_flags_mean_either_condition_can_end_encounter(self):
        units = tuple(
            replace(u, vitality=0, status=DEFEATED)
            if u.unit_id == "B-C" else u
            for u in self.state.units
        )
        facts = build_battle_facts(replace(self.state, units=units))
        outcome = ConfiguredVictoryPolicy(
            commander_defeat=True, monster_team_wipe=True
        ).evaluate(facts)
        self.assertTrue(outcome.is_finished)
        self.assertEqual(outcome.winner_side_id, "A")
        self.assertIn("commander_defeated", outcome.reason)

    def test_preexisting_dual_commander_defeat_state_classifies_as_draw(self):
        units = tuple(
            replace(u, vitality=0, status=DEFEATED)
            if u.kind == "commander" else u
            for u in self.state.units
        )
        terminal_state, events = _finish_if_commander_defeated(
            replace(self.state, units=units)
        )
        self.assertTrue(terminal_state.is_finished)
        self.assertTrue(terminal_state.is_draw)
        self.assertIsNone(terminal_state.winner_side_id)
        self.assertEqual(events[0].detail, "draw:A:commander_defeated; B:commander_defeated")

    def test_monster_knockouts_alone_do_not_end_battle(self):
        units = tuple(
            replace(u, vitality=1) if u.kind == "monster" and u.status == ACTIVE else u
            for u in self.state.units
        )
        state = replace(self.state, units=units)
        moves = {"finisher": MoveDefinition("finisher", 1, 0)}
        targets = {"A-C": "B-M1", "A-M1": "B-M2", "A-M2": "B-M1",
                   "B-C": "A-M1", "B-M1": "A-M2", "B-M2": "A-M1"}
        commands = [
            replace(command, move_id="finisher")
            for command in commands_for(state, targets)
        ]
        result = self.resolver.resolve_turn(state, commands, moves)
        self.assertFalse(result.state.is_finished)
        self.assertEqual(
            sum(u.side_id == "A" and u.kind == "monster" and u.status == ACTIVE for u in result.state.units),
            2,
        )
        self.assertEqual(
            sum(u.side_id == "B" and u.kind == "monster" and u.status == ACTIVE for u in result.state.units),
            2,
        )

    def test_invalid_command_set_is_rejected_before_resolution(self):
        commands = commands_for(
            self.state,
            {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
             "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"},
        )
        with self.assertRaises(BattleValidationError):
            self.resolver.resolve_turn(self.state, commands[:-1], self.moves)

    def test_two_turn_scenario_trace_records_reserve_and_invalidated_action(self):
        trace = run_demo_scenario()
        self.assertEqual([turn["turn"] for turn in trace["turns"]], [1, 2])
        self.assertEqual(trace["final_state"]["turn_number"], 3)
        first_events = trace["turns"][0]["events"]
        self.assertTrue(any(event["event_type"] == "ReserveDeployed" for event in first_events))
        self.assertTrue(any(
            event["event_type"] == "ActionSkipped"
            and event["detail"] == "actor_defeated_before_resolution"
            for event in first_events
        ))
        self.assertEqual(trace["status"], "synthetic deterministic fixture; not an approved game ruleset")

    def test_demo_scenario_is_replay_deterministic(self):
        self.assertEqual(run_demo_scenario(), run_demo_scenario())

    def test_finished_battle_rejects_more_turns(self):
        moves = {"strike": MoveDefinition("strike", 40, 0), "finisher": MoveDefinition("finisher", 120, 0)}
        targets = {"A-C": "B-C", "A-M1": "B-M1", "A-M2": "B-M2",
                   "B-C": "A-C", "B-M1": "A-M1", "B-M2": "A-M2"}
        commands = [
            replace(command, move_id="finisher")
            if command.actor_id in ("A-C", "B-C") else command
            for command in commands_for(self.state, targets)
        ]
        finished = self.resolver.resolve_turn(self.state, commands, moves).state
        with self.assertRaises(BattleValidationError):
            self.resolver.resolve_turn(finished, (), moves)


if __name__ == "__main__":
    unittest.main()
