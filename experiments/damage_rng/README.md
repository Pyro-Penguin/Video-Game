# Damage RNG Experiment

A standalone Python 3.10+ experiment comparing six damage randomization models. It uses only the Python standard library and does not choose a final game RNG rule.

## Requirements
- macOS
- Python 3.10 or newer (`python3 --version`)
- No third-party packages

## Run
From the repository root:

```bash
cd experiments/damage_rng
python3 damage_rng.py
python3 -m unittest -v
```

The first command writes `report.json` beside the script. Defaults are 100,000 trials per model per target and seed `20261030`.

Optional experimental modifiers use exact rational inputs:

```bash
python3 damage_rng.py --stab 3/2 --effectiveness 2 --trials 250000 --seed 42
```

Use `--stab 1 --effectiveness 1` for the required baseline single-hit comparison. Modifiers are experimental configuration only, not approved game rules.

## Method
- Exact enumeration computes single-hit knockout probabilities from every possible roll.
- Repeated-hit simulations independently sample a model's roll values against 200 HP and 300 HP.
- RNG, STAB, and type effectiveness are multiplied as exact fractions; damage is floored once at the end.
- Nonimmune damage is at least 1. Immunity always returns 0.
- Percentiles use the nearest-rank method.

## Model Definitions
1. Fixed 100%.
2. Fixed 95%.
3. Uniform integer 95–105%, inclusive.
4. Uniform integer 90–110%, inclusive.
5. Uniform integer 85–105%, inclusive, without normalization.
6. Uniform integer 85–105%, inclusive, divided by 0.95.

## Limitations
The experiment isolates damage RNG. It does not model the full battle damage formula, defense, move power, stat stages, abilities, status, shields, multi-hit moves, or turn economy. Repeated-hit simulations assume constant pre-RNG damage and independent rolls. Results are evidence about these models, not proof of balance, battle duration, or a final design choice.