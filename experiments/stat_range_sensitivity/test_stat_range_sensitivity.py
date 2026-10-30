import unittest
from fractions import Fraction

from stat_range_sensitivity import (
    ARCHETYPES,
    CANDIDATES,
    MOVE_POWERS,
    VITALITY_VALUES,
    ceil_fraction,
    run_experiment,
)


class StatRangeSensitivityTests(unittest.TestCase):
    def test_candidate_calibration_matches_existing_experiment_anchor(self):
        for equation in CANDIDATES.values():
            self.assertEqual(equation(100, 100, 100, 50), Fraction(50))

    def test_all_archetypes_stay_inside_proposed_attack_and_defense_bands(self):
        for attack, defense in ARCHETYPES.values():
            self.assertGreaterEqual(attack, 200)
            self.assertLessEqual(attack, 400)
            self.assertGreaterEqual(defense, 200)
            self.assertLessEqual(defense, 350)

    def test_ko_ceiling_is_exact(self):
        self.assertEqual(ceil_fraction(Fraction(251, 100)), 3)
        self.assertEqual(ceil_fraction(Fraction(250, 100)), 3)
        self.assertEqual(ceil_fraction(Fraction(249, 100)), 3)

    def test_report_has_complete_damage_ko_matrix(self):
        report = run_experiment()
        expected = len(ARCHETYPES) * 4 * len(MOVE_POWERS) * len(CANDIDATES) * len(VITALITY_VALUES)
        self.assertEqual(report["sample_count"], expected)
        self.assertEqual(report["sample_count"], len(report["results"]))
        self.assertEqual(report["status"], "synthetic investigation; no game rule selected")

    def test_only_level_scaled_candidate_changes_with_level(self):
        for name, equation in CANDIDATES.items():
            low = equation(100, 300, 275, 1)
            high = equation(100, 300, 275, 100)
            if name == "C_level_scaled":
                self.assertGreater(high, low)
            else:
                self.assertEqual(high, low)

    def test_sensitivity_report_contains_attack_and_defense_changes(self):
        report = run_experiment()
        changes = {row["change"] for row in report["sensitivity"]}
        self.assertEqual(changes, {"attack_up", "defense_up"})
        self.assertEqual(report["sensitivity_sample_count"], len(report["sensitivity"]))

    def test_all_damage_rows_have_positive_damage_and_ko_count(self):
        report = run_experiment()
        for row in report["results"]:
            self.assertGreater(row["raw_damage"]["numerator"], 0)
            self.assertGreaterEqual(row["hits_to_knockout"], 1)

    def test_integer_floor_damage_and_ko_are_reported(self):
        report = run_experiment()
        for row in report["results"]:
            self.assertGreaterEqual(row["integer_floor_damage"], 1)
            self.assertGreaterEqual(row["hits_to_knockout_integer_floor"], 1)
            self.assertGreaterEqual(
                row["hits_to_knockout_integer_floor"],
                row["hits_to_knockout"],
            )


if __name__ == "__main__":
    unittest.main()
