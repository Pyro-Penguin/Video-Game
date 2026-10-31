"""Neutral 80-power creature matchup screen; diagnostic only, not battle TTK."""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict

from battle_sim import ACTIVE, MONSTER, MoveDefinition, UnitState
from cli_runner import DEFAULT_FIXTURE, CandidateBDamageModel, load_fixture


def analyze_fixture(fixture_path: Path, offset_c: int = 100) -> Dict[str, Any]:
    fixture = load_fixture(fixture_path)
    creatures = fixture["creatures"]
    pair_results = []
    by_attacker = []

    for attacker in creatures:
        move = next(move for move in attacker["moves"] if move["power"] == 80)
        attacker_id = attacker["id"]
        attacker_unit = UnitState(
            f"attacker:{attacker_id}", "A", MONSTER,
            attacker["stats"]["hp"], attacker["stats"]["hp"],
            attacker["stats"]["speed"], 1, ACTIVE,
        )
        attacker_summary = []

        for defender in creatures:
            defender_id = defender["id"]
            defender_unit = UnitState(
                f"defender:{defender_id}", "B", MONSTER,
                defender["stats"]["hp"], defender["stats"]["hp"],
                defender["stats"]["speed"], 1, ACTIVE,
            )
            move_id = f"{attacker_id}:{move['id']}"
            model = CandidateBDamageModel(
                {
                    attacker_unit.unit_id: attacker["stats"],
                    defender_unit.unit_id: defender["stats"],
                },
                {move_id: move["category"]},
                offset_c,
            )
            damage = model.calculate_damage(
                attacker_unit,
                defender_unit,
                MoveDefinition(move_id, move["power"], 0),
            )
            hits = (defender["stats"]["hp"] + damage - 1) // damage
            result = {
                "attacker_id": attacker_id,
                "defender_id": defender_id,
                "move_id": move["id"],
                "category": move["category"],
                "power": move["power"],
                "damage_per_hit": damage,
                "defender_vitality": defender["stats"]["hp"],
                "repeated_hits_to_ko": hits,
            }
            pair_results.append(result)
            attacker_summary.append(hits)

        total = sum(attacker_summary)
        by_attacker.append({
            "attacker_id": attacker_id,
            "move_id": move["id"],
            "category": move["category"],
            "pair_count": len(attacker_summary),
            "average_hits_numerator": total,
            "average_hits_denominator": len(attacker_summary),
            "minimum_hits": min(attacker_summary),
            "maximum_hits": max(attacker_summary),
        })

    all_hits = [row["repeated_hits_to_ko"] for row in pair_results]
    return {
        "schema_version": 1,
        "status": "Provisional neutral single-move screen only; not actual match TTK, balance evidence, or an approved ruleset.",
        "fixture_name": fixture.get("display_name", fixture_path.stem),
        "offset_c": offset_c,
        "method": (
            "Each creature uses its own Power-80 move against each opposing creature. "
            "Candidate B test adapter, integer floor per hit, neutral effectiveness, "
            "no STAB, RNG, statuses, shields, switching, or return damage. "
            "Repeated hits to KO is a single-attacker diagnostic, not turns-to-KO."
        ),
        "pair_count": len(pair_results),
        "overall": {
            "average_hits_numerator": sum(all_hits),
            "average_hits_denominator": len(all_hits),
            "minimum_hits": min(all_hits),
            "maximum_hits": max(all_hits),
        },
        "by_attacker": by_attacker,
        "matchups": pair_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--offset", type=int, default=100)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = analyze_fixture(args.fixture, args.offset)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
