"""Deterministic two-turn scenario trace for the battle simulation harness."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

from battle_sim import (
    ActionCommand,
    BattleResolver,
    make_test_battle,
    make_test_moves,
)


def _commands(state, target_by_actor, move_by_actor=None):
    move_by_actor = move_by_actor or {}
    active = [unit for unit in state.units if unit.status == "active"]
    if set(target_by_actor) != {unit.unit_id for unit in active}:
        raise ValueError("scenario must provide exactly one target for every active unit")
    return tuple(
        ActionCommand(
            actor_id=unit.unit_id,
            move_id=move_by_actor.get(unit.unit_id, "strike"),
            target_id=target_by_actor[unit.unit_id],
        )
        for unit in active
    )


def run_demo_scenario() -> Dict[str, Any]:
    """Run two fully scripted turns; all damage and choices are fixture data."""
    resolver = BattleResolver()
    moves = make_test_moves()
    state = make_test_battle()
    turns: List[Dict[str, Any]] = []

    turn_one_targets = {
        "A-C": "B-M1",
        "A-M1": "B-M2",
        "A-M2": "B-C",
        "B-C": "A-C",
        "B-M1": "A-M1",
        "B-M2": "A-M2",
    }
    turn_one = resolver.resolve_turn(
        state,
        _commands(state, turn_one_targets, {"A-C": "finisher"}),
        moves,
    )
    state = turn_one.state
    turns.append({
        "turn": 1,
        "commands": [asdict(c) for c in _commands(
            make_test_battle(), turn_one_targets, {"A-C": "finisher"}
        )],
        "events": [asdict(event) for event in turn_one.events],
        "state_after": asdict(state),
    })

    turn_two_targets = {
        "A-C": "B-C",
        "A-M1": "B-M2",
        "A-M2": "B-R1",
        "B-C": "A-C",
        "B-M2": "A-M2",
        "B-R1": "A-M1",
    }
    turn_two = resolver.resolve_turn(
        state,
        _commands(state, turn_two_targets),
        moves,
    )
    state = turn_two.state
    turns.append({
        "turn": 2,
        "commands": [asdict(c) for c in _commands(state, turn_two_targets)],
        "events": [asdict(event) for event in turn_two.events],
        "state_after": asdict(state),
    })

    return {
        "schema_version": 1,
        "status": "synthetic deterministic fixture; not an approved game ruleset",
        "assumptions": {
            "composition": "one commander, two active monsters, one reserve per side",
            "damage": "fixed move fixture values",
            "turn_order": "priority descending, Speed descending, unit ID ascending",
            "replacement": "automatic at end of turn, roster order",
            "targeting": "single opposing active unit; no retarget",
        },
        "turns": turns,
        "final_state": asdict(state),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = run_demo_scenario()
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
