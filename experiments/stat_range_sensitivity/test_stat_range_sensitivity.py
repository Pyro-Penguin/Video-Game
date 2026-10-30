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
    run_experiment,
)


class ExpandedDamageExperimentTests(unittest.TestCase):
    def test_all_candidates_share_level_100_reference_anchor(self):
        for name in ("A_direct_ratio", "B_offset_ratio", "C_direct_level", "D_bounded_share"):
            offsets = B_OFFSETS if name == "B_offset_ratio" else (100,)
            for c in offsets:
                self.assertEqual(candidate_damage(name, 100, 300, 275, 100, c), Fraction(50))

    def test_generation_nine_reference_core_known_fixtures(self):
        self.assertEqual(pokemon_gen9_base(100, 100, 100, 100), 86)
        self.assertEqual(pokemon_gen9_base(50, 100, 100, 100), 46)
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
            "attack_defense", "attack_vitality",
            "defense_vitality", "attack_defense_vitality",
        })
        self.assertIn(-20, {r["requested_percent"] for r in rows})
        self.assertIn(20, {r["requested_percent"] for r in rows})

    def test_every_b_offset_is_independently_calibrated(self):
        for c in B_OFFSETS:
            self.assertEqual(candidate_damage("B_offset_ratio", 100, 300, 275, 100, c), Fraction(50))

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
