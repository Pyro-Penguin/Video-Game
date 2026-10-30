#!/usr/bin/env python3
"""Pre-registered all-vs-all damage sensitivity experiment.

All stat profiles and thresholds are synthetic review fixtures, not approved rules.
Exact Fraction arithmetic is used for candidate damage; gameplay KO gates use
integer-floored damage. The Pokémon Gen IX core is a reference harness only.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

ATTACKERS = {
    "balanced": (300, 275),
    "offensive": (400, 250),
    "defensive": (250, 350),
    "high_pressure": (400, 200),
    "low_pressure": (200, 350),
}
DEFENDERS = ATTACKERS
VITALITIES = (250, 350, 500)
LEVELS = (1, 5, 10, 25, 50, 75, 100)
POWERS = (40, 80, 100, 120, 160)
PERTURBATIONS = (-20, -10, -5, 5, 10, 20)
REFERENCE_LEVEL = 100
REFERENCE_ATTACK = 300
REFERENCE_DEFENSE = 275
REFERENCE_POWER = 100
REFERENCE_VITALITY = 350
REFERENCE_DAMAGE = Fraction(50)
B_OFFSETS = (0, 25, 50, 100, 200, 400, 71, 143)


def floor_fraction(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_fraction(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def pokemon_gen9_base(level: int, power: int, attack: int, defense: int) -> int:
    """Gen IX deterministic base-damage core; fixed 100% random factor.

    Implements floor(((2L/5 + 2) * BP * A / D) / 50) + 2 as exact
    integer arithmetic. STAB, type, critical, weather, items, abilities,
    screens and all other modifiers are intentionally excluded.
    """
    if level < 1 or power < 1 or attack < 1 or defense < 1:
        raise ValueError("level, power, attack and defense must be positive")
    level_term = Fraction(2 * level, 5) + 2
    numerator = level_term * power * attack
    return floor_fraction(numerator / (50 * defense)) + 2


def raw_a(power: int, attack: int, defense: int) -> Fraction:
    return Fraction(REFERENCE_DAMAGE) * Fraction(power, REFERENCE_POWER) * Fraction(attack * REFERENCE_DEFENSE, defense * REFERENCE_ATTACK)


def raw_b(power: int, attack: int, defense: int, offset: int) -> Fraction:
    anchor_ratio = Fraction(REFERENCE_ATTACK + offset, REFERENCE_DEFENSE + offset)
    return REFERENCE_DAMAGE * Fraction(power, REFERENCE_POWER) * Fraction(attack + offset, defense + offset) / anchor_ratio


def raw_d(power: int, attack: int, defense: int) -> Fraction:
    anchor_share = Fraction(REFERENCE_ATTACK, REFERENCE_ATTACK + REFERENCE_DEFENSE)
    return REFERENCE_DAMAGE * Fraction(power, REFERENCE_POWER) * Fraction(attack, attack + defense) / anchor_share


def raw_c_direct(power: int, attack: int, defense: int, level: int) -> Fraction:
    def core(lvl: int) -> Fraction:
        return (Fraction(2 * lvl, 5) + 2) * power * attack / (50 * defense) + 2
    anchor = core(REFERENCE_LEVEL)
    return REFERENCE_DAMAGE * core(level) / anchor


def candidate_damage(name: str, power: int, attack: int, defense: int, level: int, offset: int = 100) -> Fraction:
    if name == "A_direct_ratio":
        return raw_a(power, attack, defense)
    if name == "B_offset_ratio":
        return raw_b(power, attack, defense, offset)
    if name == "C_direct_level":
        return raw_c_direct(power, attack, defense, level)
    if name == "D_bounded_share":
        return raw_d(power, attack, defense)
    raise ValueError(f"unknown candidate: {name}")


def damage_pair(raw: Fraction) -> tuple[Fraction, int]:
    return raw, max(1, floor_fraction(raw))


def make_matchups() -> list[dict]:
    rows = []
    for attacker, (attack, _) in ATTACKERS.items():
        for defender, (_, defense) in DEFENDERS.items():
            for vitality in VITALITIES:
                for name in ("A_direct_ratio", "B_offset_ratio", "C_direct_level", "D_bounded_share"):
                    offsets = B_OFFSETS if name == "B_offset_ratio" else (100,)
                    for offset in offsets:
                        raw = candidate_damage(name, REFERENCE_POWER, attack, defense, REFERENCE_LEVEL, offset)
                        floored = max(1, floor_fraction(raw))
                        rows.append({
                            "attacker": attacker, "defender": defender,
                            "attack": attack, "defense": defense, "vitality": vitality,
                            "level": REFERENCE_LEVEL, "power": REFERENCE_POWER,
                            "candidate": name, "offset_c": offset if name == "B_offset_ratio" else None,
                            "raw_damage": {"numerator": raw.numerator, "denominator": raw.denominator, "decimal": round(float(raw), 6)},
                            "raw_ttk": ceil_fraction(Fraction(vitality, 1) / raw),
                            "floored_damage": floored,
                            "floored_ttk": ceil_fraction(Fraction(vitality, floored)),
                        })
    return rows


def combined_perturbations() -> list[dict]:
    rows = []
    groups = {
        "attack_defense": ("attack", "defense"),
        "attack_vitality": ("attack", "vitality"),
        "defense_vitality": ("defense", "vitality"),
        "attack_defense_vitality": ("attack", "defense", "vitality"),
    }
    for profile, (attack, defense) in ATTACKERS.items():
        for name in ("A_direct_ratio", "B_offset_ratio", "C_direct_level", "D_bounded_share"):
            offsets = B_OFFSETS if name == "B_offset_ratio" else (100,)
            for offset in offsets:
                base = candidate_damage(name, 100, attack, defense, 100, offset)
                for group, dimensions in groups.items():
                    for pct in (0,) + PERTURBATIONS:
                        values = {"attack": attack, "defense": defense, "vitality": REFERENCE_VITALITY}
                        for dimension in dimensions:
                            values[dimension] = max(1, (values[dimension] * (100 + pct)) // 100)
                        changed = candidate_damage(name, 100, values["attack"], values["defense"], 100, offset)
                        floored = max(1, floor_fraction(changed))
                        rows.append({
                            "profile": profile, "candidate": name,
                            "offset_c": offset if name == "B_offset_ratio" else None,
                            "group": group, "requested_percent": pct,
                            **values,
                            "raw_damage": round(float(changed), 6),
                            "raw_damage_delta_percent": round(float((changed / base - 1) * 100), 6),
                            "floored_damage": floored,
                            "floored_ttk": ceil_fraction(Fraction(values["vitality"], floored)),
                        })
    return rows


def rank_flip_audit(matchups: list[dict]) -> dict:
    flips = []
    for attacker in ATTACKERS:
        for defender in DEFENDERS:
            for vitality in VITALITIES:
                subset = [r for r in matchups if r["attacker"] == attacker and r["defender"] == defender and r["vitality"] == vitality and r["candidate"] != "B_offset_ratio"]
                raw_order = sorted(((r["candidate"], r["raw_ttk"]) for r in subset), key=lambda x: (x[1], x[0]))
                floor_order = sorted(((r["candidate"], r["floored_ttk"]) for r in subset), key=lambda x: (x[1], x[0]))
                raw_rank = {name: i for i, (name, _) in enumerate(raw_order)}
                floor_rank = {name: i for i, (name, _) in enumerate(floor_order)}
                changed = [name for name in raw_rank if raw_rank[name] != floor_rank[name]]
                flips.append({"attacker": attacker, "defender": defender, "vitality": vitality, "raw_order": raw_order, "floored_order": floor_order, "rank_changed_candidates": changed})
    return {"matchup_count": len(flips), "matchups_with_rank_changes": sum(bool(x["rank_changed_candidates"]) for x in flips), "details": flips}


def offset_rank_audit(matchups: list[dict]) -> dict:
    rows = []
    for attacker in ATTACKERS:
        for defender in DEFENDERS:
            for vitality in VITALITIES:
                subset = [r for r in matchups if r["attacker"] == attacker and r["defender"] == defender and r["vitality"] == vitality and r["candidate"] == "B_offset_ratio"]
                ordered = sorted(subset, key=lambda r: r["offset_c"])
                rows.append({
                    "attacker": attacker, "defender": defender, "vitality": vitality,
                    "raw_ttk_by_c": [{"c": r["offset_c"], "ttk": r["raw_ttk"]} for r in ordered],
                    "floored_ttk_by_c": [{"c": r["offset_c"], "ttk": r["floored_ttk"]} for r in ordered],
                    "floored_ttk_spread": max(r["floored_ttk"] for r in ordered) - min(r["floored_ttk"] for r in ordered),
                })
    return {"matchup_count": len(rows), "details": rows}


def level_sweep() -> list[dict]:
    rows = []
    for profile, (attack, defense) in ATTACKERS.items():
        for level in LEVELS:
            derived_only = candidate_damage("A_direct_ratio", 100, attack, defense, level)
            direct = candidate_damage("C_direct_level", 100, attack, defense, level)
            pokemon = pokemon_gen9_base(level, 100, attack, defense)
            rows.append({
                "profile": profile, "level": level,
                "derived_only_damage": round(float(derived_only), 6),
                "direct_level_damage": round(float(direct), 6),
                "pokemon_reference_damage": pokemon,
                "derived_only_floor": max(1, floor_fraction(derived_only)),
                "direct_level_floor": max(1, floor_fraction(direct)),
            })
    return rows


def calibration_and_gates() -> dict:
    equal = Fraction(REFERENCE_DAMAGE)
    ratio = candidate_damage("A_direct_ratio", 100, 600, 275, 100) / equal
    gates = {}
    for c in B_OFFSETS:
        neutral = candidate_damage("B_offset_ratio", 100, 300, 275, 100, c)
        specialized = candidate_damage("B_offset_ratio", 100, 600, 275, 100, c)
        equal_stat = candidate_damage("B_offset_ratio", 100, 300, 300, 100, c)
        ratio_2to1 = specialized / equal_stat
        gates[str(c)] = {
            "neutral_floored_ttk": ceil_fraction(Fraction(350, max(1, floor_fraction(neutral)))),
            "two_to_one_damage_ratio": round(float(ratio_2to1), 6),
            "full_vitality_one_hit_ko": floor_fraction(neutral) >= 350,
            "specialization_gate_pass": Fraction(14, 10) <= ratio_2to1 <= Fraction(18, 10),
            "neutral_ttk_gate_pass": 4 <= ceil_fraction(Fraction(350, max(1, floor_fraction(neutral)))) <= 6,
            "one_hit_gate_pass": floor_fraction(neutral) < 350,
        }
    return {
        "neutral_reference": {"level": 100, "attack": 300, "defense": 275, "power": 100, "vitality": 350, "target_floored_ttk": [4, 6]},
        "specialization_target": [1.4, 1.8],
        "candidate_b_offset_gate_results": gates,
        "candidate_b_offset_values": list(B_OFFSETS),
        "candidate_b_scale_relative_offsets": {"0.25x_mean_reference_stat": 71, "0.50x_mean_reference_stat": 143},
        "candidate_a_clean_2to1_ratio": round(float(ratio), 6),
    }


def run_experiment() -> dict:
    matchups = make_matchups()
    combined = combined_perturbations()
    return {
        "experiment": "all_vs_all_combined_stat_damage_sensitivity_v2",
        "status": "synthetic investigation; no game rule selected",
        "pre_registration": {
            "competitive_level": 100, "historical_calibration_anchor": 50,
            "story_levels": list(LEVELS), "attacker_profiles": list(ATTACKERS),
            "defender_profiles": list(DEFENDERS), "matchup_pairs": 25,
            "vitalities": list(VITALITIES), "powers": list(POWERS),
            "combined_groups": ["attack_defense", "attack_vitality", "defense_vitality", "attack_defense_vitality"],
            "perturbations_percent": list(PERTURBATIONS),
            "b_offsets": list(B_OFFSETS),
            "pokemon_reference_role": "Generation IX deterministic base-damage reference harness only; not a selectable candidate",
            "flooring_policy": "integer-floored per-hit damage governs every acceptance gate; raw values diagnostic only",
        },
        "method": {
            "arithmetic": "Exact rational arithmetic for candidate equations; floor applied explicitly for gameplay damage.",
            "calibration": "A, B and D calibrated to 50 damage at Level 100, P100, A300, D275. Each B offset is separately calibrated to this same anchor. C direct-level path is calibrated to 50 at the same Level-100 anchor.",
            "limitations": ["Synthetic profiles and ranges only.", "No type, STAB, criticals, weather, equipment, abilities, status, screens, shields, RNG, multi-hit, simultaneous resolution, or damage application.", "Generation IX harness includes only deterministic base damage with fixed 100% random factor; no external modifiers.", "The level-derived-only path holds derived stats constant across levels; this isolates direct level dependence and does not model actual stat progression."],
        },
        "sample_counts": {"all_vs_all_rows": len(matchups), "combined_perturbation_rows": len(combined), "level_rows": len(level_sweep())},
        "gates": calibration_and_gates(),
        "all_vs_all": matchups,
        "raw_vs_floored_rank_audit": rank_flip_audit(matchups),
        "candidate_b_offset_rank_audit": offset_rank_audit(matchups),
        "combined_perturbations": combined,
        "level_sweep": level_sweep(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("report-v2.json"))
    args = parser.parse_args()
    report = run_experiment()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {report['sample_counts']} to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
