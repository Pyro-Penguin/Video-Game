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

ROOT = Path(__file__).resolve().parent
BASELINE_DAMAGE = Fraction(50)
BASELINE_POWER = 100
BASELINE_ATTACK = 100
BASELINE_DEFENSE = 100
BASELINE_LEVEL = 50
OFFSET_C = 100

SYNTHETIC_SCALES = {
    "compact": (25, 250),
    "expanded": (100, 1000),
}
LEVELS = (1, 25, 50, 100)
POWERS = (40, 80, 100, 120, 160)
RATIOS = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1), Fraction(4, 3), Fraction(2), Fraction(4))


def _candidate_a(power: int, attack: int, defense: int, level: int) -> Fraction:
    del level
    return Fraction(1, 2) * power * Fraction(attack, defense)


def _candidate_b(power: int, attack: int, defense: int, level: int) -> Fraction:
    del level
    return Fraction(1, 2) * power * Fraction(attack + OFFSET_C, defense + OFFSET_C)


def _candidate_c(power: int, attack: int, defense: int, level: int) -> Fraction:
    raw = (Fraction(2 * level, 5) + 2) * power * attack / (50 * defense) + 2
    calibration = Fraction(25, 23)  # Makes the defined baseline equal 50.
    return calibration * raw


def _candidate_d(power: int, attack: int, defense: int, level: int) -> Fraction:
    del level
    return power * Fraction(attack, attack + defense)


CANDIDATES: dict[str, Callable[[int, int, int, int], Fraction]] = {
    "A_direct_ratio": _candidate_a,
    "B_offset_ratio_c100": _candidate_b,
    "C_level_scaled": _candidate_c,
    "D_bounded_offense_share": _candidate_d,
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
                    for name, equation in CANDIDATES.items():
                        damage = equation(power, attack, defense, level)
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
                            "damage": _number(damage),
                        })

    baseline = {
        name: _number(equation(
            BASELINE_POWER,
            BASELINE_ATTACK,
            BASELINE_DEFENSE,
            BASELINE_LEVEL,
        ))
        for name, equation in CANDIDATES.items()
    }

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
            "offset_c": OFFSET_C,
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
