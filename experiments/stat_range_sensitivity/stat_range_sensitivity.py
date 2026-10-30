#!/usr/bin/env python3
"""Sensitivity sweep for proposed endgame stat bands and damage candidates.

All inputs are synthetic review fixtures. This script does not select game rules.
Uses exact rational arithmetic; JSON decimals are presentation-only.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

BASELINE_DAMAGE = Fraction(50)
BASELINE_POWER = 100
BASELINE_ATTACK = 100
BASELINE_DEFENSE = 100
BASELINE_LEVEL = 50
OFFSET_C = 100

# Proposal-derived test bands, not approved game stats.
ATTACK_VALUES = (200, 250, 300, 350, 400)
DEFENSE_VALUES = (200, 250, 275, 300, 350)
VITALITY_VALUES = (250, 350, 500)
MOVE_POWERS = (40, 80, 100, 120, 160)
LEVELS = (1, 25, 50, 100)
SENSITIVITY_PCTS = (5, 10, 20)

# Curated archetypes span the proposed band without assuming a final stat formula.
ARCHETYPES = {
    "balanced": (300, 275),
    "offensive": (400, 250),
    "defensive": (250, 350),
    "high_pressure": (400, 200),
    "low_pressure": (200, 350),
}


def candidate_a(power: int, attack: int, defense: int, level: int) -> Fraction:
    del level
    return Fraction(1, 2) * power * Fraction(attack, defense)


def candidate_b(power: int, attack: int, defense: int, level: int) -> Fraction:
    del level
    return Fraction(1, 2) * power * Fraction(attack + OFFSET_C, defense + OFFSET_C)


def candidate_c(power: int, attack: int, defense: int, level: int) -> Fraction:
    raw = (Fraction(2 * level, 5) + 2) * power * attack / (50 * defense) + 2
    return Fraction(25, 23) * raw


def candidate_d(power: int, attack: int, defense: int, level: int) -> Fraction:
    del level
    return power * Fraction(attack, attack + defense)


CANDIDATES = {
    "A_direct_ratio": candidate_a,
    "B_offset_ratio_c100": candidate_b,
    "C_level_scaled": candidate_c,
    "D_bounded_offense_share": candidate_d,
}


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def as_number(value: Fraction) -> dict[str, int | float]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": round(float(value), 6),
    }


def run_experiment() -> dict:
    rows = []
    for archetype, (attack, defense) in ARCHETYPES.items():
        for level in LEVELS:
            for power in MOVE_POWERS:
                for candidate_name, equation in CANDIDATES.items():
                    damage = equation(power, attack, defense, level)
                    for vitality in VITALITY_VALUES:
                        hits = ceil_fraction(Fraction(vitality, 1) / damage)
                        rows.append({
                            "archetype": archetype,
                            "attack": attack,
                            "defense": defense,
                            "level": level,
                            "move_power": power,
                            "candidate": candidate_name,
                            "vitality": vitality,
                            "raw_damage": as_number(damage),
                            "hits_to_knockout": hits,
                        })

    sensitivity = []
    for archetype, (attack, defense) in ARCHETYPES.items():
        for candidate_name, equation in CANDIDATES.items():
            baseline = equation(100, attack, defense, 100)
            for pct in SENSITIVITY_PCTS:
                delta = Fraction(pct, 100)
                for dimension, changed_attack, changed_defense in (
                    ("attack_up", Fraction(attack) * (1 + delta), Fraction(defense)),
                    ("defense_up", Fraction(attack), Fraction(defense) * (1 + delta)),
                ):
                    changed = equation(
                        100,
                        int(changed_attack),
                        int(changed_defense),
                        100,
                    )
                    sensitivity.append({
                        "archetype": archetype,
                        "candidate": candidate_name,
                        "change": dimension,
                        "requested_percent": pct,
                        "baseline_damage": as_number(baseline),
                        "changed_damage": as_number(changed),
                        "actual_damage_change_percent": round(
                            float((changed / baseline - 1) * 100), 6
                        ),
                        "note": "Stats are integer-truncated after applying the requested percentage.",
                    })

    level_effect = []
    for archetype, (attack, defense) in ARCHETYPES.items():
        for candidate_name, equation in CANDIDATES.items():
            for level in LEVELS:
                damage = equation(100, attack, defense, level)
                level_effect.append({
                    "archetype": archetype,
                    "candidate": candidate_name,
                    "level": level,
                    "damage": as_number(damage),
                })

    return {
        "experiment": "proposed_endgame_stat_range_sensitivity",
        "status": "synthetic investigation; no game rule selected",
        "source_proposal": {
            "attack_and_special_attack": [200, 400],
            "defense_and_special_defense": [200, 350],
            "vitality": [250, 500],
            "speed": [100, 400],
            "interpretation": "Team-supplied proposal converted into test bands only; not project-approved stats.",
        },
        "method": {
            "arithmetic": "Exact fractions for damage and KO thresholds; JSON decimals are presentation-only.",
            "candidate_calibration": "Inherited from the existing damage-equation experiment: 50 damage at P=100, A=100, D=100, L=50.",
            "offset_c": OFFSET_C,
            "levels": list(LEVELS),
            "move_powers": list(MOVE_POWERS),
            "vitality_test_points": list(VITALITY_VALUES),
            "archetypes": {name: {"attack": pair[0], "defense": pair[1]} for name, pair in ARCHETYPES.items()},
            "sensitivity_percentages": list(SENSITIVITY_PCTS),
            "sensitivity_note": "Requested percentage changes are applied to one stat at a time and truncated to integer stats.",
            "limitations": [
                "All stat bands, archetypes, move powers, and Vitality points are synthetic review fixtures.",
                "No actual creature data, stat-allocation conversion, equipment, stages, type, modifiers, RNG, flooring, shields, or damage application are modeled.",
                "Hits-to-knockout uses exact raw damage with no integer damage flooring; it is a comparative pacing indicator, not a battle prediction.",
                "Speed is not modeled because this experiment concerns damage and survivability only.",
                "Candidate C directly uses level; candidates A, B, and D do not.",
                "Candidate constants are inherited comparison controls, not balance recommendations.",
            ],
        },
        "sample_count": len(rows),
        "sensitivity_sample_count": len(sensitivity),
        "level_sample_count": len(level_effect),
        "results": rows,
        "sensitivity": sensitivity,
        "level_effect": level_effect,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("report.json"))
    args = parser.parse_args()
    report = run_experiment()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {report['sample_count']} damage/KO rows, "
        f"{report['sensitivity_sample_count']} sensitivity rows, and "
        f"{report['level_sample_count']} level rows to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
