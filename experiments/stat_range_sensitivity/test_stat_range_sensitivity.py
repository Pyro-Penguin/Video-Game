import unittest
from fractions import Fraction

from stat_range_sensitivity import (
    ATTACKERS,
    B_OFFSETS,
    candidate_damage,
    combined_perturbations,
    make_matchups,
    pokemon_gen9_base,
    rank_flip_audit,
    offset_cross_matchup_rank_stability,
    calibration_and_gates,
    run_experiment,
)


class ExpandedDamageExperimentTests(unittest.TestCase):
    def test_all_candidates_share_level_100_reference_anchor(self):
        for name in ("A_direct_ratio", "B_offset_ratio", "C_direct_level", "D_bounded_share"):
            offsets = B_OFFSETS if name == "B_offset_ratio" else (100,)
            for c in offsets:
                self.assertEqual(candidate_damage(name, 100, 300, 275, 100, c), Fraction(60))

    def test_specialization_gate_sweeps_all_pre_registered_defenses(self):
        gates = calibration_and_gates()["candidate_gate_results"]["B_offset_ratio"]
        c100 = gates["100"]
        self.assertEqual(set(c100["specialization_ratio_by_profile"]), set(ATTACKERS))
        self.assertAlmostEqual(c100["specialization_ratio_by_profile"]["balanced"], 650 / 375, places=5)
        self.assertAlmostEqual(c100["specialization_worst_case_ratio"], 500 / 300, places=5)
        self.assertAlmostEqual(c100["specialization_best_case_ratio"], 800 / 450, places=5)
        self.assertTrue(c100["specialization_gate_pass"])

    def test_known_candidate_b_c400_failure_at_defense_200_is_not_hidden(self):
        gates = calibration_and_gates()["candidate_gate_results"]["B_offset_ratio"]
        self.assertAlmostEqual(
            gates["400"]["specialization_ratio_by_profile"]["high_pressure"],
            4 / 3,
            places=5,
        )
        self.assertFalse(gates["400"]["specialization_gate_pass"])
        self.assertFalse(gates["400"]["combined_numeric_gates_pass"])

    def test_cross_matchup_audit_rejects_missing_coordinate(self):
        rows = make_matchups()
        rows.remove(next(
            row for row in rows
            if row["candidate"] == "B_offset_ratio" and row["offset_c"] == 143
        ))
        with self.assertRaisesRegex(ValueError, "matchup key mismatch"):
            offset_cross_matchup_rank_stability(rows)

    def test_generation_nine_reference_core_known_fixtures(self):
        self.assertEqual(pokemon_gen9_base(100, 100, 100, 100), 86)
        self.assertEqual(pokemon_gen9_base(50, 100, 100, 100), 46)
        self.assertEqual(pokemon_gen9_base(1, 100, 100, 100), 6)
        self.assertEqual(pokemon_gen9_base(100, 100, 200, 100), 170)

    def test_reference_rejects_nonpositive_inputs(self):
        with self.assertRaises(ValueError):
            pokemon_gen9_base(100, 100, 100, 0)

    def test_all_vs_all_contains_every_ordered_pair_and_vitality(self):
        rows = make_matchups()
        self.assertEqual(len(rows), 25 * 3 * (3 + len(B_OFFSETS)))
        pairs = {(r["attacker"], r["defender"]) for r in rows}
        self.assertEqual(len(pairs), 25)
        self.assertEqual({r["vitality"] for r in rows}, {250, 350, 500})

    def test_combined_perturbations_cover_all_four_groups(self):
        rows = combined_perturbations()
        self.assertEqual({r["group"] for r in rows}, {
            "single_attack", "single_defense", "single_vitality",
            "attack_defense", "attack_vitality",
            "defense_vitality", "attack_defense_vitality",
        })
        self.assertIn(-20, {r["requested_percent"] for r in rows})
        self.assertIn(20, {r["requested_percent"] for r in rows})

    def test_log_space_interaction_residual_is_zero_for_factorized_candidate_a(self):
        rows = combined_perturbations()
        factorized = [
            row for row in rows
            if row["candidate"] == "A_direct_ratio"
            and row["group"] in (
                "attack_defense", "attack_vitality",
                "defense_vitality", "attack_defense_vitality",
            )
            and row["requested_percent"] != 0
        ]
        self.assertTrue(factorized)
        for row in factorized:
            self.assertAlmostEqual(row["interaction_log_residual"], 0.0, places=7)

    def test_every_b_offset_is_independently_calibrated(self):
        for c in B_OFFSETS:
            self.assertEqual(candidate_damage("B_offset_ratio", 100, 300, 275, 100, c), Fraction(60))

    def test_candidate_c_retains_attack_defense_sensitivity_after_global_calibration(self):
        base = candidate_damage("C_direct_level", 100, 300, 300, 100)
        stronger = candidate_damage("C_direct_level", 100, 600, 300, 100)
        self.assertGreater(stronger, base)

    def test_level_derived_only_and_direct_level_paths_are_distinct(self):
        low = candidate_damage("A_direct_ratio", 100, 300, 275, 1)
        high = candidate_damage("A_direct_ratio", 100, 300, 275, 100)
        self.assertEqual(low, high)
        direct_low = candidate_damage("C_direct_level", 100, 300, 275, 1)
        direct_high = candidate_damage("C_direct_level", 100, 300, 275, 100)
        self.assertLess(direct_low, direct_high)

    def test_rank_audit_reports_all_25_pairs_at_three_vitalities(self):
        report = run_experiment()
        self.assertEqual(report["raw_vs_floored_rank_audit"]["matchup_count"], 75)
        self.assertEqual(report["candidate_b_cross_matchup_rank_stability"]["pair_comparisons_per_offset"], 2775)
        self.assertEqual(len(report["raw_vs_floored_rank_audit"]["details"]), 75)

    def test_report_counts_match_generated_rows(self):
        report = run_experiment()
        self.assertEqual(report["sample_counts"]["all_vs_all_rows"], len(report["all_vs_all"]))
        self.assertEqual(report["sample_counts"]["combined_perturbation_rows"], len(report["combined_perturbations"]))
        self.assertEqual(report["sample_counts"]["level_rows"], len(report["level_sweep"]))
        self.assertEqual(report["status"], "synthetic investigation; no game rule selected")

    def test_attackers_are_the_five_pre_registered_profiles(self):
        self.assertEqual(len(ATTACKERS), 5)


if __name__ == "__main__":
    unittest.main()
