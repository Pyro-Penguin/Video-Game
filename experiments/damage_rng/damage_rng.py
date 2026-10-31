#!/usr/bin/env python3
"""Standalone, exact-arithmetic damage RNG experiment (Python 3.10+)."""
from __future__ import annotations

import argparse
import json
import random
import statistics
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class RNGModel:
    name: str
    kind: str
    values: tuple[int, ...] = ()
    fixed_percent: int | None = None
    normalization: Fraction = Fraction(1, 1)
    description: str = ""

    def rolls(self) -> tuple[int, ...]:
        return (self.fixed_percent,) if self.fixed_percent is not None else self.values

    def multiplier(self, roll: int) -> Fraction:
        return Fraction(roll, 100) / self.normalization

    def theoretical_mean(self) -> Fraction:
        return sum((self.multiplier(x) for x in self.rolls()), Fraction()) / len(self.rolls())


MODELS = (
    RNGModel("fixed_100", "fixed", fixed_percent=100, description="Fixed 100% damage."),
    RNGModel("fixed_95", "fixed", fixed_percent=95, description="Fixed 95% damage."),
    RNGModel("uniform_95_105", "uniform_integer", tuple(range(95, 106)), description="Uniform integer percentage roll from 95 through 105 inclusive."),
    RNGModel("uniform_90_110", "uniform_integer", tuple(range(90, 111)), description="Uniform integer percentage roll from 90 through 110 inclusive."),
    RNGModel("uniform_85_105_raw", "uniform_integer", tuple(range(85, 106)), description="Uniform integer percentage roll from 85 through 105 inclusive; no normalization."),
    RNGModel("uniform_85_105_normalized", "uniform_integer", tuple(range(85, 106)), normalization=Fraction(95, 100), description="Uniform integer percentage roll from 85 through 105 inclusive, divided by 0.95."),
)

SELECTED_MODEL_NAME = "uniform_85_105_raw"
SELECTED_MODEL = next(model for model in MODELS if model.name == SELECTED_MODEL_NAME)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def calculate_damage(
    pre_rng_damage: int,
    roll_percent: int,
    *,
    stab: Fraction = Fraction(1),
    effectiveness: Fraction = Fraction(1, 1),
    immune: bool = False,
    normalization: Fraction = Fraction(1, 1),
) -> int:
    """Apply RNG and configurable modifiers, then floor exactly once."""
    if immune or effectiveness == 0:
        return 0
    if pre_rng_damage < 0 or stab < 0 or effectiveness < 0 or normalization <= 0:
        raise ValueError("Damage and modifiers must be non-negative; normalization must be positive")
    result = Fraction(pre_rng_damage) * Fraction(roll_percent, 100) / normalization * stab * effectiveness
    return max(1, floor_fraction(result))


def exact_damage_outcomes(
    model: RNGModel,
    pre_rng_damage: int = 100,
    stab: Fraction = Fraction(1),
    effectiveness: Fraction = Fraction(1),
) -> dict[int, int]:
    outcomes: dict[int, int] = {}
    for roll in model.rolls():
        damage = calculate_damage(
            pre_rng_damage, roll, stab=stab, effectiveness=effectiveness,
            normalization=model.normalization,
        )
        outcomes[damage] = outcomes.get(damage, 0) + 1
    return dict(sorted(outcomes.items()))


def exact_ko_probability(
    model: RNGModel,
    hp: int,
    pre_rng_damage: int = 100,
    stab: Fraction = Fraction(1),
    effectiveness: Fraction = Fraction(1),
) -> Fraction:
    outcomes = exact_damage_outcomes(model, pre_rng_damage, stab, effectiveness)
    successful = sum(count for damage, count in outcomes.items() if damage >= hp)
    return Fraction(successful, sum(outcomes.values()))


def sample_roll(model: RNGModel, rng: random.Random) -> int:
    """Draw one roll; callers invoke this once per damaging hit."""
    rolls = model.rolls()
    return rolls[rng.randrange(len(rolls))]


def percentile(sorted_values: list[int], p: Fraction) -> int:
    """Nearest-rank percentile: rank = ceil(p*n), one-indexed."""
    if not sorted_values:
        raise ValueError("Cannot calculate percentile of empty data")
    rank = (p.numerator * len(sorted_values) + p.denominator - 1) // p.denominator
    return sorted_values[max(0, rank - 1)]


def simulate_hits_to_ko(
    model: RNGModel,
    target_hp: int,
    *,
    trials: int,
    seed: int,
    pre_rng_damage: int = 100,
    stab: Fraction = Fraction(1),
    effectiveness: Fraction = Fraction(1),
) -> dict[str, int | float]:
    if trials < 1 or target_hp < 1:
        raise ValueError("trials and target_hp must be positive")
    rng = random.Random(seed)
    hit_counts: list[int] = []
    for _ in range(trials):
        remaining = target_hp
        hits = 0
        while remaining > 0:
            roll = sample_roll(model, rng)
            damage = calculate_damage(
                pre_rng_damage, roll, stab=stab, effectiveness=effectiveness,
                normalization=model.normalization,
            )
            remaining -= damage
            hits += 1
        hit_counts.append(hits)
    hit_counts.sort()
    return {
        "trials": trials,
        "mean_hits": statistics.fmean(hit_counts),
        "median_hits": statistics.median(hit_counts),
        "p10_hits": percentile(hit_counts, Fraction(10, 100)),
        "p90_hits": percentile(hit_counts, Fraction(90, 100)),
        "minimum_hits": hit_counts[0],
        "maximum_hits": hit_counts[-1],
    }


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def build_report(
    *,
    trials: int = 100_000,
    seed: int = 20261030,
    stab: Fraction = Fraction(1),
    effectiveness: Fraction = Fraction(1),
) -> dict:
    models_report = []
    for model in MODELS:
        outcomes = exact_damage_outcomes(model, stab=stab, effectiveness=effectiveness)
        denominator = len(model.rolls())
        realized = [
            {"damage": damage, "count": count, "probability": count / denominator}
            for damage, count in outcomes.items()
        ]
        ko = {}
        for hp in (100, 95, 85):
            probability = exact_ko_probability(model, hp, stab=stab, effectiveness=effectiveness)
            ko[str(hp)] = {
                "numerator": probability.numerator,
                "denominator": probability.denominator,
                "probability": float(probability),
                "percent": float(probability * 100),
            }
        models_report.append({
            "name": model.name,
            "kind": model.kind,
            "description": model.description,
            "roll_percentages": list(model.rolls()),
            "normalization_divisor": fraction_text(model.normalization),
            "theoretical_mean_multiplier": fraction_text(model.theoretical_mean()),
            "theoretical_mean_multiplier_decimal": float(model.theoretical_mean()),
            "realized_damage": realized,
            "single_hit_ko_probabilities": ko,
            "repeated_hit_simulations": {
                str(hp): simulate_hits_to_ko(
                    model, hp, trials=trials, seed=seed,
                    stab=stab, effectiveness=effectiveness,
                )
                for hp in (200, 300)
            },
        })
    return {
        "experiment": "damage_rng_model_comparison",
        "pre_rng_damage": 100,
        "selected_model": SELECTED_MODEL_NAME,
        "selected_sampling_contract": {
            "distribution": "uniform_integer",
            "roll_percentages": list(SELECTED_MODEL.rolls()),
            "probability_per_roll": "1/21",
            "sampling_cadence": "independent draw per damaging hit (i.i.d.)",
            "normalization_divisor": fraction_text(SELECTED_MODEL.normalization),
            "mean_multiplier": fraction_text(SELECTED_MODEL.theoretical_mean()),
            "flooring": "exact rational multiplication followed by one final integer floor in this isolated experiment",
            "production_modifier_order": "not selected by this experiment",
        },
        "anchor_60_reference": {
            "meaning": "damage at the 100% roll, not expected or maximum damage",
            "expected_damage_before_floor": "57",
            "integer_damage_range": [51, 63],
            "pacing_gate": "not evaluated at this experiment-parity anchor; D-026 requires a separate gameplay anchor",
        },
        "modifier_configuration": {
            "stab": fraction_text(stab),
            "type_effectiveness": fraction_text(effectiveness),
            "note": "Configurable experimental inputs only; these values are not finalized game rules.",
        },
        "simulation_settings": {
            "trials_per_model_per_target": trials,
            "seed": seed,
            "targets_hp": [200, 300],
            "percentile_method": "nearest-rank",
        },
        "models": models_report,
        "limitations": [
            "These calculations compare mathematical RNG models; they do not establish game balance.",
            "Repeated-hit results assume independent rolls and constant damage inputs on every hit.",
            "The experiment does not model defenses, stat stages, move power, abilities, status, shields, or turn economy.",
            "STAB and type effectiveness are configurable inputs, not finalized game rules.",
            "Simulation summaries are seed-dependent estimates; exact single-hit probabilities are enumerated.",
            "D-029 selects uniform integer 85–105 rolls, independently sampled per hit without normalization; this experiment does not finalize the production modifier order or damage formula.",
            "The 60-damage experiment-parity anchor is not a D-026 pacing gate; gameplay pacing requires a separately selected anchor and representative original creature/move inputs.",
        ],
    }


def parse_fraction(text: str) -> Fraction:
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise argparse.ArgumentTypeError(f"Invalid rational number: {text}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=20261030)
    parser.add_argument("--stab", type=parse_fraction, default=Fraction(1),
                        help="Experimental STAB multiplier, e.g. 3/2; default 1")
    parser.add_argument("--effectiveness", type=parse_fraction, default=Fraction(1),
                        help="Experimental type multiplier, e.g. 2 or 1/2; default 1")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("report.json"))
    args = parser.parse_args()
    report = build_report(
        trials=args.trials, seed=args.seed, stab=args.stab,
        effectiveness=args.effectiveness,
    )
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
