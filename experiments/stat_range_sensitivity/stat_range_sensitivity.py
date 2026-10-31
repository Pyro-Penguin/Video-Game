#!/usr/bin/env python3
"""Pre-registered all-vs-all damage sensitivity experiment.

All stat profiles and thresholds are synthetic review fixtures, not approved rules.
Exact Fraction arithmetic is used for candidate damage; gameplay KO gates use
integer-floored damage. The Pokémon Gen IX core is a reference harness only.
"""
from __future__ import annotations

import argparse
import json
from math import log
from itertools import combinations
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
REFERENCE_DAMAGE = Fraction(60)
B_OFFSETS = (0, 25, 50, 100, 200, 400, 71, 143)
SPECIALIZATION_MIN = Fraction(14, 10)
SPECIALIZATION_MAX = Fraction(18, 10)
SPECIALIZATION_PROFILES = tuple((name, defense) for name, (_, defense) in DEFENDERS.items())


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
    level_term = (2 * level) // 5 + 2
    numerator = level_term * power * attack
    return numerator // (50 * defense) + 2


def raw_a(power: int, attack: int, defense: int) -> Fraction:
    return Fraction(REFERENCE_DAMAGE) * Fraction(power, REFERENCE_POWER) * Fraction(attack * REFERENCE_DEFENSE, defense * REFERENCE_ATTACK)


def raw_b(power: int, attack: int, defense: int, offset: int) -> Fraction:
    anchor_ratio = Fraction(REFERENCE_ATTACK + offset, REFERENCE_DEFENSE + offset)
    return REFERENCE_DAMAGE * Fraction(power, REFERENCE_POWER) * Fraction(attack + offset, defense + offset) / anchor_ratio


def raw_d(power: int, attack: int, defense: int) -> Fraction:
    anchor_share = Fraction(REFERENCE_ATTACK, REFERENCE_ATTACK + REFERENCE_DEFENSE)
    return REFERENCE_DAMAGE * Fraction(power, REFERENCE_POWER) * Fraction(attack, attack + defense) / anchor_share


def raw_c_direct(power: int, attack: int, defense: int, level: int) -> Fraction:
    def core(lvl: int, atk: int, deff: int) -> Fraction:
        return (Fraction(2 * lvl, 5) + 2) * power * atk / (50 * deff) + 2
    anchor = core(REFERENCE_LEVEL, REFERENCE_ATTACK, REFERENCE_DEFENSE)
    return REFERENCE_DAMAGE * core(level, attack, defense) / anchor



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
        "single_attack": ("attack",),
        "single_defense": ("defense",),
        "single_vitality": ("vitality",),
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
    lookup = {
        (r["profile"], r["candidate"], r["offset_c"], r["group"], r["requested_percent"]): r
        for r in rows
    }
    for row in rows:
        if row["group"].startswith("single_") or row["requested_percent"] == 0:
            row["interaction_log_residual"] = 0.0
            row["interaction_ttk_residual_hits"] = 0
            continue
        dimensions = {
            "attack_defense": ("single_attack", "single_defense"),
            "attack_vitality": ("single_attack", "single_vitality"),
            "defense_vitality": ("single_defense", "single_vitality"),
            "attack_defense_vitality": ("single_attack", "single_defense", "single_vitality"),
        }[row["group"]]
        controls = [
            lookup[(row["profile"], row["candidate"], row["offset_c"], group, row["requested_percent"])]
            for group in dimensions
        ]
        baseline_ttk = lookup[(row["profile"], row["candidate"], row["offset_c"], row["group"], 0)]["floored_ttk"]
        base_row = lookup[(row["profile"], row["candidate"], row["offset_c"], row["group"], 0)]
        offset = row["offset_c"] or 100
        baseline_raw = candidate_damage(
            row["candidate"], 100, base_row["attack"], base_row["defense"], 100, offset
        )
        combined_raw = candidate_damage(
            row["candidate"], 100, row["attack"], row["defense"], 100, offset
        )
        isolated_log_effects = 0.0
        for group, control in zip(dimensions, controls):
            control_base = lookup[
                (row["profile"], row["candidate"], row["offset_c"], group, 0)
            ]
            isolated_raw = candidate_damage(
                row["candidate"], 100, control["attack"], control["defense"], 100, offset
            )
            isolated_baseline = candidate_damage(
                row["candidate"], 100, control_base["attack"],
                control_base["defense"], 100, offset
            )
            isolated_log_effects += log(float(isolated_raw / isolated_baseline))
        row["interaction_log_residual"] = round(
            log(float(combined_raw / baseline_raw)) - isolated_log_effects, 9
        )
        row["interaction_ttk_residual_hits"] = (
            row["floored_ttk"] - baseline_ttk
            - sum(x["floored_ttk"] - baseline_ttk for x in controls)
        )
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


def pairwise_rank_flip_audit(matchups: list[dict]) -> dict:
    details = []
    for attacker in ATTACKERS:
        for defender in DEFENDERS:
            for vitality in VITALITIES:
                subset = [r for r in matchups if r["attacker"] == attacker and r["defender"] == defender and r["vitality"] == vitality]
                for i, left in enumerate(subset):
                    for right in subset[i + 1:]:
                        raw_relation = (left["raw_ttk"] > right["raw_ttk"]) - (left["raw_ttk"] < right["raw_ttk"])
                        floor_relation = (left["floored_ttk"] > right["floored_ttk"]) - (left["floored_ttk"] < right["floored_ttk"])
                        if raw_relation != floor_relation:
                            details.append({
                                "attacker": attacker, "defender": defender, "vitality": vitality,
                                "left_candidate": left["candidate"], "left_c": left["offset_c"],
                                "right_candidate": right["candidate"], "right_c": right["offset_c"],
                                "raw_relation": raw_relation, "floored_relation": floor_relation,
                            })
    return {"pairwise_comparisons": sum(len(rows) * (len(rows) - 1) // 2 for rows in [[r for r in matchups if r["attacker"] == attacker and r["defender"] == defender and r["vitality"] == vitality] for attacker in ATTACKERS for defender in DEFENDERS for vitality in VITALITIES]), "rank_flips_or_tie_changes": len(details), "details": details}


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


def offset_cross_matchup_rank_stability(matchups: list[dict]) -> dict:
    """Compare each B-offset ordering against c=100 across all matchup coordinates."""
    def coordinate(row: dict) -> tuple[str, str, int]:
        return row["attacker"], row["defender"], row["vitality"]

    base_rows = [
        row for row in matchups
        if row["candidate"] == "B_offset_ratio" and row["offset_c"] == 100
    ]
    baseline = {coordinate(row): row for row in base_rows}
    comparisons = []
    for c in B_OFFSETS:
        if c == 100:
            continue
        current = {
            coordinate(row): row for row in matchups
            if row["candidate"] == "B_offset_ratio" and row["offset_c"] == c
        }
        if set(current) != set(baseline):
            missing = sorted(set(baseline) - set(current))
            unexpected = sorted(set(current) - set(baseline))
            raise ValueError(
                f"offset c={c} matchup key mismatch: missing={missing}, unexpected={unexpected}"
            )

        changed_raw = 0
        changed_floored = 0
        total = 0
        for left_key, right_key in combinations(baseline.keys(), 2):
            b_left, b_right = baseline[left_key], baseline[right_key]
            c_left, c_right = current[left_key], current[right_key]
            base_raw = (b_left["raw_ttk"] > b_right["raw_ttk"]) - (b_left["raw_ttk"] < b_right["raw_ttk"])
            now_raw = (c_left["raw_ttk"] > c_right["raw_ttk"]) - (c_left["raw_ttk"] < c_right["raw_ttk"])
            base_floor = (b_left["floored_ttk"] > b_right["floored_ttk"]) - (b_left["floored_ttk"] < b_right["floored_ttk"])
            now_floor = (c_left["floored_ttk"] > c_right["floored_ttk"]) - (c_left["floored_ttk"] < c_right["floored_ttk"])
            changed_raw += base_raw != now_raw
            changed_floored += base_floor != now_floor
            total += 1
        comparisons.append({
            "c": c, "matchup_pair_comparisons": total,
            "raw_order_changes_vs_c100": changed_raw,
            "floored_order_changes_vs_c100": changed_floored,
            "raw_fraction_changed": round(changed_raw / total, 6),
            "floored_fraction_changed": round(changed_floored / total, 6),
        })
    return {
        "baseline_c": 100,
        "matchup_coordinates": len(baseline),
        "pair_comparisons_per_offset": len(baseline) * (len(baseline) - 1) // 2,
        "offsets": comparisons,
    }

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
                "derived_only_ttk_vit350": ceil_fraction(Fraction(350, max(1, floor_fraction(derived_only)))),
                "direct_level_ttk_vit350": ceil_fraction(Fraction(350, max(1, floor_fraction(direct)))),
                "pokemon_reference_ttk_vit350": ceil_fraction(Fraction(350, max(1, pokemon))),
            })
    return rows


def calibration_and_gates() -> dict:
    all_gates = {}
    candidates = {
        "A_direct_ratio": (100,),
        "B_offset_ratio": B_OFFSETS,
        "C_direct_level": (100,),
        "D_bounded_share": (100,),
    }
    for name, offsets in candidates.items():
        all_gates[name] = {}
        for c in offsets:
            neutral = candidate_damage(name, 100, 300, 275, 100, c)
            profile_ratios = {
                profile: candidate_damage(name, 100, 2 * defense, defense, 100, c)
                / candidate_damage(name, 100, defense, defense, 100, c)
                for profile, defense in SPECIALIZATION_PROFILES
            }
            worst_case_ratio = min(profile_ratios.values())
            best_case_ratio = max(profile_ratios.values())
            ttk = ceil_fraction(Fraction(350, max(1, floor_fraction(neutral))))
            specialization_pass = (
                worst_case_ratio >= SPECIALIZATION_MIN
                and best_case_ratio <= SPECIALIZATION_MAX
            )
            all_gates[name][str(c)] = {
                "neutral_floored_ttk": ttk,
                "two_to_one_damage_ratio": round(float(profile_ratios["balanced"]), 6),
                "specialization_ratio_by_profile": {
                    profile: round(float(ratio), 6)
                    for profile, ratio in profile_ratios.items()
                },
                "specialization_worst_case_ratio": round(float(worst_case_ratio), 6),
                "specialization_best_case_ratio": round(float(best_case_ratio), 6),
                "full_vitality_one_hit_ko": floor_fraction(neutral) >= 350,
                "specialization_gate_pass": specialization_pass,
                "neutral_ttk_gate_pass": 4 <= ttk <= 6,
                "one_hit_gate_pass": floor_fraction(neutral) < 350,
                "combined_numeric_gates_pass": 4 <= ttk <= 6 and specialization_pass and floor_fraction(neutral) < 350,
            }
    return {
        "neutral_reference": {"level": 100, "attack": 300, "defense": 275, "power": 100, "vitality": 350, "target_floored_ttk": [4, 6]},
        "specialization_target": [float(SPECIALIZATION_MIN), float(SPECIALIZATION_MAX)],
        "specialization_defense_profiles": {profile: defense for profile, defense in SPECIALIZATION_PROFILES},
        "specialization_gate_policy": "Every pre-registered defender profile must remain inside the target ratio band; both worst-case minimum and maximum are gated.",
        "candidate_gate_results": all_gates,
        "candidate_b_offset_values": list(B_OFFSETS),
        "candidate_b_scale_relative_offsets": {"0.25x_mean_reference_stat": 71, "0.50x_mean_reference_stat": 143},
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
            "calibration": "A, B and D calibrated to 60 damage at Level 100, P100, A300, D275. Each B offset is separately calibrated to this same anchor. C direct-level path is calibrated to 60 at the same Level-100 anchor.",
            "limitations": ["Synthetic profiles and ranges only.", "No type, STAB, criticals, weather, equipment, abilities, status, screens, shields, RNG, multi-hit, simultaneous resolution, or damage application.", "Generation IX harness includes only deterministic base damage with fixed 100% random factor; no external modifiers.", "The level-derived-only path holds derived stats constant across levels; this isolates direct level dependence and does not model actual stat progression.", "The damage interaction residual is computed in log space: log(combined damage ratio) minus the sum of isolated log ratios. Zero indicates multiplicatively independent effects; nonzero values measure interaction. The TTK residual remains a discrete, flooring-sensitive diagnostic."],
        },
        "sample_counts": {"all_vs_all_rows": len(matchups), "combined_perturbation_rows": len(combined), "level_rows": len(level_sweep())},
        "gates": calibration_and_gates(),
        "all_vs_all": matchups,
        "raw_vs_floored_rank_audit": rank_flip_audit(matchups),
        "pairwise_rank_flip_audit": pairwise_rank_flip_audit(matchups),
        "candidate_b_offset_rank_audit": offset_rank_audit(matchups),
        "candidate_b_cross_matchup_rank_stability": offset_cross_matchup_rank_stability(matchups),
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
