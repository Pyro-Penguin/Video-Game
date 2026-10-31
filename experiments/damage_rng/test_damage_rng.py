import unittest
from fractions import Fraction

from damage_rng import (
    MODELS,
    SELECTED_MODEL,
    SELECTED_MODEL_NAME,
    sample_roll,
    build_report,
    calculate_damage,
    exact_ko_probability,
    simulate_hits_to_ko,
)


class ExactProbabilityTests(unittest.TestCase):
    EXPECTED = {
        "fixed_100": (Fraction(1), Fraction(1), Fraction(1)),
        "fixed_95": (Fraction(0), Fraction(1), Fraction(1)),
        "uniform_95_105": (Fraction(6, 11), Fraction(1), Fraction(1)),
        "uniform_90_110": (Fraction(11, 21), Fraction(16, 21), Fraction(1)),
        "uniform_85_105_raw": (Fraction(6, 21), Fraction(11, 21), Fraction(1)),
        "uniform_85_105_normalized": (Fraction(11, 21), Fraction(15, 21), Fraction(1)),
    }

    def test_d029_selected_model_is_raw_uniform_integer_85_to_105(self):
        self.assertEqual(SELECTED_MODEL_NAME, "uniform_85_105_raw")
        self.assertEqual(SELECTED_MODEL.rolls(), tuple(range(85, 106)))
        self.assertEqual(SELECTED_MODEL.normalization, Fraction(1))
        self.assertEqual(SELECTED_MODEL.theoretical_mean(), Fraction(19, 20))

    def test_d028_anchor_60_is_100_percent_roll_not_expected_damage(self):
        outcomes = [calculate_damage(60, roll) for roll in SELECTED_MODEL.rolls()]
        self.assertEqual((min(outcomes), max(outcomes)), (51, 63))
        self.assertEqual(Fraction(sum(outcomes), len(outcomes)), Fraction(57))

    def test_per_hit_sampler_draws_only_allowed_integer_values(self):
        import random
        rng = random.Random(20261031)
        draws = [sample_roll(SELECTED_MODEL, rng) for _ in range(500)]
        self.assertTrue(all(85 <= roll <= 105 for roll in draws))
        self.assertGreater(len(set(draws)), 1)

    def test_sequential_integer_floors_match_combined_denominator_floor(self):
        for level in (1, 5, 10, 25, 50, 75, 100):
            term=(2*level)//5+2
            for power in (1,40,100,160):
                for attack in (1,50,100,300,1000):
                    for defense in (1,50,100,275,350,1000):
                        numerator=term*power*attack
                        self.assertEqual((numerator//defense)//50,numerator//(50*defense))

    def test_required_exact_probabilities(self):
        for model in MODELS:
            actual = tuple(exact_ko_probability(model, hp) for hp in (100, 95, 85))
            self.assertEqual(actual, self.EXPECTED[model.name], model.name)

    def test_damage_floor_is_applied_after_modifiers(self):
        self.assertEqual(calculate_damage(101, 95, stab=Fraction(3, 2)), 143)

    def test_nonimmune_damage_minimum_one(self):
        self.assertEqual(calculate_damage(1, 1), 1)

    def test_immunity_always_zero(self):
        self.assertEqual(calculate_damage(100, 100, immune=True), 0)
        self.assertEqual(calculate_damage(100, 100, effectiveness=Fraction(0)), 0)

    def test_seeded_simulation_reproducible(self):
        model = MODELS[2]
        a = simulate_hits_to_ko(model, 200, trials=1000, seed=7)
        b = simulate_hits_to_ko(model, 200, trials=1000, seed=7)
        self.assertEqual(a, b)

    def test_report_has_required_sections(self):
        report = build_report(trials=100, seed=1)
        self.assertEqual(len(report["models"]), 6)
        self.assertIn("limitations", report)
        self.assertIn("modifier_configuration", report)
        self.assertEqual(report["selected_model"], SELECTED_MODEL_NAME)
        self.assertEqual(report["selected_sampling_contract"]["probability_per_roll"], "1/21")
        self.assertEqual(report["anchor_60_reference"]["integer_damage_range"], [51, 63])


if __name__ == "__main__":
    unittest.main()
