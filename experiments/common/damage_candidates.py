"""Shared exact-rational candidate damage functions for offline experiments."""
from __future__ import annotations
from fractions import Fraction
from typing import Callable
Candidate = Callable[[int, int, int, int, int], Fraction]
B_OFFSETS = (0, 25, 50, 100, 200, 400, 71, 143)
def candidate_a(power: int, attack: int, defense: int, level: int, offset: int = 100) -> Fraction:
    del level, offset
    return Fraction(power * attack, defense)
def candidate_b(power: int, attack: int, defense: int, level: int, offset: int = 100) -> Fraction:
    del level
    if offset < 0: raise ValueError("Candidate B offset must be non-negative")
    return Fraction(power * (attack + offset), defense + offset)
def candidate_c(power: int, attack: int, defense: int, level: int, offset: int = 100) -> Fraction:
    del offset
    return (Fraction(2 * level, 5) + 2) * power * attack / (50 * defense) + 2
def candidate_d(power: int, attack: int, defense: int, level: int, offset: int = 100) -> Fraction:
    del level, offset
    return Fraction(power * attack, attack + defense)
CANDIDATES: dict[str, Candidate] = {
    "A_direct_ratio": candidate_a, "B_offset_ratio": candidate_b,
    "C_level_scaled": candidate_c, "D_bounded_offense_share": candidate_d,
}
def calibrate(anchor_damage: int | Fraction, anchor_power: int, anchor_attack: int,
              anchor_defense: int, anchor_level: int, candidate: Candidate,
              *, offset: int = 100) -> Fraction:
    raw = candidate(anchor_power, anchor_attack, anchor_defense, anchor_level, offset)
    if raw <= 0: raise ValueError("Candidate anchor output must be positive")
    return Fraction(anchor_damage) / raw
def calibrated_damage(candidate: Candidate, power: int, attack: int, defense: int,
                      level: int, *, anchor_damage: int | Fraction, anchor_power: int,
                      anchor_attack: int, anchor_defense: int, anchor_level: int,
                      offset: int = 100) -> Fraction:
    scale = calibrate(anchor_damage, anchor_power, anchor_attack, anchor_defense,
                      anchor_level, candidate, offset=offset)
    return scale * candidate(power, attack, defense, level, offset)
