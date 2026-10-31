import unittest
from fractions import Fraction

from damage_equation import (
    BASELINE_ATTACK,
    BASELINE_DEFENSE,
    BASELINE_LEVEL,
    BASELINE_POWER,
    CANDIDATES,
    candidate_damage,
    run_experiment,
)


class DamageEquationExperimentTests(unittest.TestCase):
    def test_all_candidates_share_the_calibrated_anchor(self):
        for equation in CANDIDATES.values():
            self.assertEqual(
                equation(BASELINE_POWER, BASELINE_ATTACK, BASELINE_DEFENSE, BASELINE_LEVEL),
                Fraction(50),
            )

    def test_candidate_b_offset_sweep_uses_shared_anchor_calibration(self):
        report = run_experiment()
        rows = [r for r in report["results"]
                if r["scale"] == "compact" and r["target_attack_defense_ratio"] == "1/1"
                and r["level"] == 50 and r["power"] == 100 and r["candidate"] == "B_offset_ratio"]
        self.assertEqual({r["offset_c"] for r in rows}, {0, 25, 50, 71, 100, 143, 200, 400})
        for offset in (0, 25, 50, 71, 100, 143, 200, 400):
            self.assertEqual(candidate_damage("B_offset_ratio",100,100,100,50,offset),Fraction(50))

    def test_power_is_monotonic_for_all_candidates(self):
        for equation in CANDIDATES.values():
            low = equation(80, 120, 100, 50)
            high = equation(120, 120, 100, 50)
            self.assertGreater(high, low)

    def test_attack_is_monotonic_for_all_candidates(self):
        for equation in CANDIDATES.values():
            low = equation(100, 80, 100, 50)
            high = equation(100, 120, 100, 50)
            self.assertGreater(high, low)

    def test_defense_is_monotonic_for_all_candidates(self):
        for equation in CANDIDATES.values():
            low = equation(100, 100, 80, 50)
            high = equation(100, 100, 120, 50)
            self.assertLess(high, low)

    def test_report_labels_synthetic_assumptions(self):
        report = run_experiment()
        self.assertEqual(report["status"], "synthetic investigation; no game rule selected")
        self.assertEqual(report["sample_count"], len(report["results"]))
        self.assertIn("Synthetic ranges are not approved game stat ranges.", report["method"]["limitations"])

    def test_level_only_changes_candidate_c_directly(self):
        for name, equation in CANDIDATES.items():
            low = equation(100, 120, 100, 25)
            high = equation(100, 120, 100, 100)
            if name == "C_level_scaled":
                self.assertGreater(high, low)
            else:
                self.assertEqual(high, low)


if __name__ == "__main__":
    unittest.main()
