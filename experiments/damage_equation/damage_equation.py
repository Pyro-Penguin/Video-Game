#!/usr/bin/env python3
"""Compare candidate damage equations across explicitly synthetic stat scales.

This experiment is analytical only. It does not select or approve game rules.
All calculations use Fraction until values are serialized for the JSON report.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Callable
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from common.damage_candidates import B_OFFSETS, CANDIDATES as RAW_CANDIDATES, calibrated_damage
BASELINE_DAMAGE = Fraction(50)
BASELINE_POWER = 100
BASELINE_ATTACK = 100
BASELINE_DEFENSE = 100
BASELINE_LEVEL = 50

SYNTHETIC_SCALES = {
    "compact": (25, 250),
    "expanded": (100, 1000),
}
LEVELS = (1, 25, 50, 100)
POWERS = (40, 80, 100, 120, 160)
RATIOS = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1), Fraction(4, 3), Fraction(2), Fraction(4))


def candidate_damage(name: str, power: int, attack: int, defense: int, level: int, offset: int = 100) -> Fraction:
    try:
        candidate = RAW_CANDIDATES[name]
    except KeyError as exc:
        raise ValueError(f"unknown candidate: {name}") from exc
    return calibrated_damage(
        candidate, power, attack, defense, level,
        anchor_damage=BASELINE_DAMAGE, anchor_power=BASELINE_POWER,
        anchor_attack=BASELINE_ATTACK, anchor_defense=BASELINE_DEFENSE,
        anchor_level=BASELINE_LEVEL,
        offset=offset if name == "B_offset_ratio" else 100,
    )


def _wrapper(name: str) -> Callable[[int, int, int, int], Fraction]:
    return lambda power, attack, defense, level: candidate_damage(name, power, attack, defense, level)


CANDIDATES: dict[str, Callable[[int, int, int, int], Fraction]] = {
    "A_direct_ratio": _wrapper("A_direct_ratio"),
    "B_offset_ratio_c100": _wrapper("B_offset_ratio"),
    "C_level_scaled": _wrapper("C_level_scaled"),
    "D_bounded_offense_share": _wrapper("D_bounded_offense_share"),
}


def _number(value: Fraction) -> dict[str, int | float]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": round(float(value), 6),
    }


def run_experiment() -> dict:
    results: list[dict] = []

    for scale_name, (low, high) in SYNTHETIC_SCALES.items():
        anchor = (low + high) // 2
        for ratio in RATIOS:
            attack = anchor
            defense = max(1, int(Fraction(anchor, 1) / ratio))
            for level in LEVELS:
                for power in POWERS:
                    for name in RAW_CANDIDATES:
                        offsets = B_OFFSETS if name == "B_offset_ratio" else (100,)
                        for offset in offsets:
                            damage = candidate_damage(name, power, attack, defense, level, offset)
                            results.append({
                                "scale": scale_name,
                                "synthetic_range": [low, high],
                                "attack": attack,
                                "defense": defense,
                                "target_attack_defense_ratio": f"{ratio.numerator}/{ratio.denominator}",
                                "actual_attack_defense_ratio": f"{Fraction(attack, defense).numerator}/{Fraction(attack, defense).denominator}",
                                "level": level,
                                "power": power,
                                "candidate": name,
                                "offset_c": offset if name == "B_offset_ratio" else None,
                                "damage": _number(damage),
                            })

    baseline = {
        f"B_offset_ratio_c{offset}": _number(candidate_damage(
            "B_offset_ratio", BASELINE_POWER, BASELINE_ATTACK,
            BASELINE_DEFENSE, BASELINE_LEVEL, offset
        ))
        for offset in B_OFFSETS
    }
    baseline.update({
        name: _number(candidate_damage(name, BASELINE_POWER, BASELINE_ATTACK,
                                       BASELINE_DEFENSE, BASELINE_LEVEL))
        for name in ("A_direct_ratio", "C_level_scaled", "D_bounded_offense_share")
    })

    return {
        "experiment": "damage_equation_candidate_sweep",
        "status": "synthetic investigation; no game rule selected",
        "method": {
            "arithmetic": "exact rational arithmetic; decimal values are report-only",
            "calibration": "each candidate is calibrated to 50 damage at P=100, A=100, D=100, L=50",
            "synthetic_stat_scales": {
                name: {"minimum": bounds[0], "maximum": bounds[1]}
                for name, bounds in SYNTHETIC_SCALES.items()
            },
            "candidate_b_offsets": list(B_OFFSETS),
            "levels": list(LEVELS),
            "move_powers": list(POWERS),
            "attack_defense_ratios": [
                f"{ratio.numerator}/{ratio.denominator}" for ratio in RATIOS
            ],
            "limitations": [
                "Synthetic ranges are not approved game stat ranges.",
                "Candidates A, B, and D do not directly use level.",
                "Candidate C uses a direct level term; this isolates level-treatment differences.",
                "No modifiers, RNG, integer flooring, shields, or damage application are included.",
                "Candidate constants are baseline-calibrated for comparison, not balance recommendations.",
            ],
        },
        "baseline_anchor": {
            "inputs": {
                "level": BASELINE_LEVEL,
                "power": BASELINE_POWER,
                "attack": BASELINE_ATTACK,
                "defense": BASELINE_DEFENSE,
            },
            "damage_by_candidate": baseline,
        },
        "sample_count": len(results),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "report.json",
        help="JSON report destination (default: experiments/damage_equation/report.json)",
    )
    args = parser.parse_args()

    report = run_experiment()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {report['sample_count']} synthetic comparisons to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
