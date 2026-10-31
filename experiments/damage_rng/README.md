# Damage RNG Experiment

A standalone Python 3.10+ exact-arithmetic experiment comparing six RNG models. **D-029 selects `uniform_85_105_raw`: one integer is drawn uniformly from 85 through 105 inclusive for each damaging hit, independently of every other hit, with no normalization.**

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

Use `--stab 1 --effectiveness 1` for the baseline comparison. Modifiers are experiment inputs only; the complete production modifier order remains unresolved.

## Selected sampling contract (D-029)
- Distribution: discrete uniform integer `{85, 86, ..., 105}`; 21 equally likely outcomes, each with probability `1/21` (about 4.76%).
- Cadence: draw once per damaging hit; repeated hits are independent and identically distributed.
- Normalization: none. The multiplier is `roll / 100`; its arithmetic mean is 0.95. Do not re-center to 1.0.
- Arithmetic in this isolated experiment: exact rational multiplication, then one final integer floor. Production ordering of RNG relative to STAB, type, critical, equipment, and other modifiers is not decided here.
- Nonimmune damage is at least 1. Immunity returns 0.
- Repeated-hit simulations sample a fresh roll for every hit. Exact single-hit probabilities are enumerated; simulation summaries are seed-dependent.

## Anchor and pacing separation
D-028's 60-damage point means damage at the 100% roll at Level 100 / Power 100 / Attack 300 / Defense 275 / Vitality 350. Under the selected raw model, pre-floor expected damage is 57 and integer damage outcomes are 51–63. It is neither expected damage nor maximum damage. Comparisons with older fixed-100% reports must identify the old anchor meaning.

Do not evaluate D-026 pacing at anchor 60: it is retained for experiment parity only and produces a 6–7 hit reference at Vitality 350. D-026's 2–3-hit neutral pacing and representative-core wallbreaker benchmark require a separate gameplay calibration anchor, original creature spreads, and representative moves. That gameplay anchor and the base formula remain unselected. The anchor-60 sweep is a relative candidate comparison, not a pacing gate.

## Model Definitions
1. Fixed 100% (deterministic comparator).
2. Fixed 95% (deterministic comparator).
3. Uniform integer 95–105% (comparison model).
4. Uniform integer 90–110% (comparison model).
5. **Selected:** uniform integer 85–105%, raw and unnormalized.
6. Uniform integer 85–105%, divided by 0.95 (counterfactual only; not selected).

## Limitations
This experiment isolates RNG behavior. It does not implement the full battle damage formula, defense, move power, stat stages, abilities, status, shields, multi-hit move rules, or turn economy. Passing tests establish implementation consistency, not balance, battle duration, or final formula quality. The selected RNG sampling contract does not authorize a production resolver before modifier ordering and the floor checkpoint are specified.
