import unittest
from fractions import Fraction
from damage_candidates import B_OFFSETS, CANDIDATES, calibrate
class SharedDamageCandidateTests(unittest.TestCase):
    def test_every_candidate_and_offset_reproduces_anchor(self):
        anchor=(100,300,275,100)
        for name,fn in CANDIDATES.items():
            for offset in (B_OFFSETS if name=="B_offset_ratio" else (100,)):
                with self.subTest(candidate=name,offset=offset):
                    scale=calibrate(Fraction(60),*anchor,fn,offset=offset)
                    self.assertEqual(scale*fn(*anchor,offset),Fraction(60))
    def test_calibration_rejects_nonpositive_anchor(self):
        def invalid(power,attack,defense,level,offset): return Fraction(0)
        with self.assertRaisesRegex(ValueError,"must be positive"):
            calibrate(60,100,300,275,100,invalid)
if __name__=="__main__": unittest.main()
