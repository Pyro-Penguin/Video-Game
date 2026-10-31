"""CLI pipeline-validation runner for the explicitly non-canonical Pokémon fixture."""
from __future__ import annotations
import argparse
import json
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple
from battle_sim import ACTIVE, COMMANDER, MONSTER, RESERVE, ActionCommand, BattleResolver, BattleState, MoveDefinition, UnitState

DEFAULT_FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "creatures.json"
STAT_KEYS = ("hp", "attack", "defense", "special_attack", "special_defense", "speed")
VALID_CATEGORIES = {"physical", "special"}


class FixtureError(ValueError):
    """Malformed or incomplete pipeline fixture."""


def load_fixture(path: Path = DEFAULT_FIXTURE) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected_comment = ("Scaffolding fixture. Not representative of final roster. Base stats used "
                        "directly as game stats. Neutral type effectiveness. Replace with real "
                        "creatures before design playtest.")
    if payload.get("_comment") != expected_comment:
        raise FixtureError("fixture warning comment is missing or changed")
    if payload.get("schema_version") != 1 or payload.get("fixture_kind") != "pipeline_validation_only":
        raise FixtureError("unsupported fixture schema or purpose")
    if payload.get("type_effectiveness") != "neutral; the type chart is intentionally excluded from this fixture":
        raise FixtureError("fixture must use neutral type effectiveness")
    creatures = payload.get("creatures")
    if not isinstance(creatures, list) or len(creatures) != 5:
        raise FixtureError("fixture must define exactly five creatures")
    creature_ids = set()
    for creature in creatures:
        creature_id = creature.get("id")
        if not creature_id or creature_id in creature_ids:
            raise FixtureError("creature IDs must be non-empty and unique")
        creature_ids.add(creature_id)
        stats = creature.get("stats", {})
        if set(stats) != set(STAT_KEYS) or any(type(stats[key]) is not int or stats[key] <= 0 for key in STAT_KEYS):
            raise FixtureError(f"invalid direct-base-stat block for {creature_id}")
        moves = creature.get("moves")
        if not isinstance(moves, list) or len(moves) != 3 or sorted(move.get("power") for move in moves) != [40, 80, 120]:
            raise FixtureError(f"{creature_id} must define three moves at 40/80/120 power")
        if any(move.get("category") not in VALID_CATEGORIES for move in moves):
            raise FixtureError(f"invalid move category for {creature_id}")
    commander = payload.get("commander", {})
    commander_stats = commander.get("stats", {})
    if set(commander_stats) != set(STAT_KEYS) or any(type(commander_stats[key]) is not int or commander_stats[key] <= 0 for key in STAT_KEYS):
        raise FixtureError("commander fixture stats are incomplete")
    commander_moves = commander.get("moves", [])
    if len(commander_moves) != 3 or sorted(move.get("power") for move in commander_moves) != [40, 80, 120]:
        raise FixtureError("commander fixture must define three moves at 40/80/120 power")
    if any(move.get("category") not in VALID_CATEGORIES for move in commander_moves):
        raise FixtureError("invalid commander move category")
    scenarios = payload.get("pipeline_battles", [])
    if len(scenarios) != 3:
        raise FixtureError("fixture must define exactly three pipeline battles")
    for scenario in scenarios:
        for side in ("side_a", "side_b"):
            team = scenario.get(side)
            if not isinstance(team, list) or len(team) != 3 or any(species not in creature_ids for species in team):
                raise FixtureError(f"scenario {scenario.get('name')} must provide three known creatures for {side}")
    return payload


class CandidateBDamageModel:
    """Replaceable Candidate B adapter for pipeline exercise; not a formula selection."""
    def __init__(self, unit_stats: Mapping[str, Mapping[str, int]], move_categories: Mapping[str, str], offset_c: int = 100):
        if offset_c < 0:
            raise ValueError("offset_c must be non-negative")
        self._unit_stats = unit_stats
        self._move_categories = move_categories
        self._offset_c = offset_c

    def calculate_damage(self, actor: UnitState, target: UnitState, move: MoveDefinition) -> int:
        try:
            attacker, defender = self._unit_stats[actor.unit_id], self._unit_stats[target.unit_id]
            category = self._move_categories[move.move_id]
        except KeyError as error:
            raise FixtureError(f"missing damage input: {error}") from error
        if category == "physical":
            attack, defense = attacker["attack"], defender["defense"]
        elif category == "special":
            attack, defense = attacker["special_attack"], defender["special_defense"]
        else:
            raise FixtureError(f"unsupported move category: {category}")
        c = self._offset_c
        raw = Fraction(60 * move.fixture_damage, 100) * Fraction(attack + c, defense + c) / Fraction(300 + c, 275 + c)
        return max(1, raw.numerator // raw.denominator)


def _build_battle(fixture: Mapping[str, Any], scenario: Mapping[str, Any], offset_c: int):
    creatures = {creature["id"]: creature for creature in fixture["creatures"]}
    units, unit_stats, actor_moves, moves, move_categories = [], {}, {}, {}, {}
    commander = fixture["commander"]
    commander_move_ids = []
    for move in commander["moves"]:
        move_id = f"commander:{move['id']}"
        commander_move_ids.append(move_id)
        moves[move_id] = MoveDefinition(move_id, move["power"], 0)
        move_categories[move_id] = move["category"]
    for side_id, team_key in (("A", "side_a"), ("B", "side_b")):
        commander_id, stats = f"{side_id}-C", commander["stats"]
        units.append(UnitState(commander_id, side_id, COMMANDER, stats["hp"], stats["hp"], stats["speed"], 0, ACTIVE))
        unit_stats[commander_id], actor_moves[commander_id] = stats, tuple(commander_move_ids)
        for roster_index, creature_id in enumerate(scenario[team_key], start=1):
            creature, unit_id = creatures[creature_id], f"{side_id}-M{roster_index}-{creature_id}"
            stats = creature["stats"]
            status = ACTIVE if roster_index <= 2 else RESERVE
            units.append(UnitState(unit_id, side_id, MONSTER, stats["hp"], stats["hp"], stats["speed"], roster_index, status))
            unit_stats[unit_id] = stats
            move_ids = []
            for move in creature["moves"]:
                move_id = f"{creature_id}:{move['id']}"
                move_ids.append(move_id)
                moves[move_id] = MoveDefinition(move_id, move["power"], 0)
                move_categories[move_id] = move["category"]
            actor_moves[unit_id] = tuple(move_ids)
    state = BattleState(tuple(sorted(units, key=lambda u: (u.side_id, u.roster_order, u.unit_id))))
    return state, moves, CandidateBDamageModel(unit_stats, move_categories, offset_c), actor_moves


def _commands_for_turn(state: BattleState, actor_moves: Mapping[str, Tuple[str, ...]]) -> Tuple[ActionCommand, ...]:
    commands = []
    for actor in sorted((u for u in state.units if u.status == ACTIVE), key=lambda u: (u.side_id, u.roster_order, u.unit_id)):
        enemy_side = "B" if actor.side_id == "A" else "A"
        enemy_commander = next(u for u in state.units if u.side_id == enemy_side and u.kind == COMMANDER)
        if actor.kind == COMMANDER:
            target = enemy_commander
        else:
            targets = [u for u in state.units if u.side_id == enemy_side and u.kind == MONSTER and u.status == ACTIVE]
            target = min(targets, key=lambda u: (Fraction(u.vitality, u.max_vitality), u.vitality, u.unit_id)) if targets else enemy_commander
        choices = actor_moves[actor.unit_id]
        move_id = choices[(state.turn_number - 1) % len(choices)]
        commands.append(ActionCommand(actor.unit_id, move_id, target.unit_id))
    return tuple(commands)


def run_pipeline(fixture_path: Path = DEFAULT_FIXTURE, offset_c: int = 100, battle_count: int = 3, max_turns: int = 30) -> Dict[str, Any]:
    fixture = load_fixture(fixture_path)
    if not 1 <= battle_count <= len(fixture["pipeline_battles"]):
        raise ValueError("battle_count must be between 1 and 3")
    if max_turns < 1:
        raise ValueError("max_turns must be positive")
    battles = []
    for index, scenario in enumerate(fixture["pipeline_battles"][:battle_count], start=1):
        state, moves, model, actor_moves = _build_battle(fixture, scenario, offset_c)
        resolver, turns = BattleResolver(damage_model=model), []
        for _ in range(max_turns):
            commands = _commands_for_turn(state, actor_moves)
            result = resolver.resolve_turn(state, commands, moves)
            state = result.state
            turns.append({"turn": state.turn_number - 1, "commands": [asdict(c) for c in commands],
                          "events": [asdict(e) for e in result.events], "state_after": asdict(state)})
            if state.is_finished:
                break
        if not state.is_finished:
            raise RuntimeError(f"battle {scenario['name']} exceeded {max_turns} turns")
        battles.append({"battle": index, "name": scenario["name"],
                        "teams": {"A": list(scenario["side_a"]), "B": list(scenario["side_b"])},
                        "turns": turns, "final_state": asdict(state)})
    return {
        "schema_version": 1,
        "fixture_name": fixture.get("display_name", "PLAYTEST A"),
        "status": "Pipeline validation only; not balance evidence or an approved game ruleset",
        "fixture_comment": fixture["_comment"],
        "damage_model": {"adapter": "Candidate B formula behind the existing DamageModel seam",
                         "offset_c": offset_c, "purpose": "pipeline exercise only; not a formula or offset selection",
                         "type_effectiveness": "neutral", "floor": "integer per-hit, minimum 1"},
        "battles": battles,
    }


def format_trace(payload: Mapping[str, Any]) -> str:
    lines = [f"PIPELINE VALIDATION — {payload.get('fixture_name', 'PLAYTEST A')} (NOT A BALANCE PLAYTEST)",
             f"Damage adapter: Candidate B scaffold, c={payload['damage_model']['offset_c']}; neutral effectiveness"]
    for battle in payload["battles"]:
        lines.extend(["", f"Battle {battle['battle']}: {battle['name']} | A={','.join(battle['teams']['A'])} vs B={','.join(battle['teams']['B'])}"])
        for turn in battle["turns"]:
            lines.append(f"  Turn {turn['turn']}")
            for command in turn["commands"]:
                lines.append(f"    {command['actor_id']} uses {command['move_id']} -> {command['target_id']}")
            for event in turn["events"]:
                if event["event_type"] == "DamageApplied":
                    lines.append(f"    damage: {event['actor_id']} -> {event['target_id']} {event['detail']} = {event['amount']}")
                elif event["event_type"] == "ReserveDeployed":
                    lines.append(f"    reserve: {event['target_id']} deployed")
                elif event["event_type"] == "ActionSkipped":
                    lines.append(f"    skipped: {event['actor_id']} -> {event['target_id']} ({event['detail']})")
                elif event["event_type"] == "BattleFinished":
                    lines.append(f"    outcome: {event['detail']}")
        final = battle["final_state"]
        outcome = "draw" if final["is_draw"] else f"winner={final['winner_side_id']}"
        lines.append(f"  Completed in {len(battle['turns'])} turns; {outcome}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--offset", type=int, default=100, help="temporary Candidate B test offset; not a design selection")
    parser.add_argument("--battles", type=int, default=3)
    parser.add_argument("--max-turns", type=int, default=30)
    parser.add_argument("--output", type=Path, help="optional JSON trace output path")
    args = parser.parse_args()
    payload = run_pipeline(args.fixture, args.offset, args.battles, args.max_turns)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(format_trace(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
