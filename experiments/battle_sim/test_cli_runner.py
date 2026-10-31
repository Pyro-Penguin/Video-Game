import unittest
from fractions import Fraction
from battle_sim import COMMANDER, MoveDefinition, UnitState
from cli_runner import CandidateBDamageModel, DEFAULT_FIXTURE, format_trace, load_fixture, run_pipeline


class PipelineFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_fixture(DEFAULT_FIXTURE)

    def test_fixture_has_five_explicit_scaffolding_archetypes(self):
        self.assertIn("Not representative of final roster", self.fixture["_comment"])
        self.assertEqual({c["id"] for c in self.fixture["creatures"]}, {"weavile", "snorlax", "machamp", "gengar", "skarmory"})
        self.assertEqual({c["archetype"] for c in self.fixture["creatures"]}, {"fast_frail", "slow_tanky", "balanced", "special_attacker", "physical_wall"})

    def test_base_stats_are_used_directly(self):
        weavile = next(c for c in self.fixture["creatures"] if c["id"] == "weavile")
        self.assertEqual((weavile["stats"]["hp"], weavile["stats"]["attack"], weavile["stats"]["speed"]), (70, 120, 125))

    def test_each_creature_has_three_moves_at_40_80_120_power(self):
        for creature in self.fixture["creatures"]:
            self.assertEqual(sorted(move["power"] for move in creature["moves"]), [40, 80, 120])

    def test_damage_adapter_uses_physical_and_special_stat_pairs_and_floors(self):
        actor = UnitState("A", "A", COMMANDER, 100, 100, 80, 0)
        target = UnitState("B", "B", COMMANDER, 100, 100, 80, 0)
        stats = {"A": {"attack": 120, "defense": 65, "special_attack": 45, "special_defense": 85},
                 "B": {"attack": 100, "defense": 100, "special_attack": 100, "special_defense": 100}}
        model = CandidateBDamageModel(stats, {"physical": "physical", "special": "special"}, 100)
        physical = model.calculate_damage(actor, target, MoveDefinition("physical", 80))
        special = model.calculate_damage(actor, target, MoveDefinition("special", 80))
        raw = Fraction(60 * 80, 100) * Fraction(220, 200) / Fraction(400, 375)
        self.assertEqual(physical, max(1, raw.numerator // raw.denominator))
        self.assertGreater(physical, special)

    def test_three_battles_complete_and_emit_all_phase_markers(self):
        payload = run_pipeline()
        self.assertEqual(len(payload["battles"]), 3)
        self.assertIn("not balance evidence", payload["status"])
        for battle in payload["battles"]:
            self.assertTrue(battle["final_state"]["is_finished"])
            self.assertEqual(len(battle["teams"]["A"]), 3)
            self.assertEqual(len(battle["teams"]["B"]), 3)
            for turn in battle["turns"]:
                phases = [(e["event_type"], e["detail"]) for e in turn["events"] if e["event_type"] in ("PhaseStarted", "PhaseCompleted")]
                self.assertEqual(phases, [
                    ("PhaseStarted", "action_resolution"), ("PhaseCompleted", "action_resolution"),
                    ("PhaseStarted", "end_of_turn_replacement"), ("PhaseCompleted", "end_of_turn_replacement"),
                    ("PhaseStarted", "victory_check"), ("PhaseCompleted", "victory_check"),
                ])

    def test_replay_and_readable_trace_are_deterministic(self):
        first, second = run_pipeline(), run_pipeline()
        self.assertEqual(first, second)
        self.assertEqual(format_trace(first), format_trace(second))
        self.assertIn("PLAYTEST A", format_trace(first))
        self.assertIn("NOT A BALANCE PLAYTEST", format_trace(first))


if __name__ == "__main__":
    unittest.main()
