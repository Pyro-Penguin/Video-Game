# Damage Equation Comparison Experiment

A standard-library Python experiment comparing four parameterized base-damage equation families across synthetic stat scales. It is an investigation tool, not an approved game rule or balance model.

## Run

From the repository root:

```bash
cd experiments/damage_equation
python3 damage_equation.py
python3 -m unittest -v
```

The script writes `report.json` in this directory. Use `--output /path/to/report.json` to choose another destination.

## Candidate families

- A: direct multiplicative attack/defense ratio.
- B: offset ratio with sampled synthetic offsets c=0, 25, 50, 71, 100, 143, 200, and 400. Each offset is independently calibrated to the experiment's own baseline.
- C: level-scaled cartridge-style structure.
- D: bounded offense-share ratio.

Each candidate is calibrated to the same baseline (50 damage at Level 50, Power 100, Attack 100, Defense 100) so the sweep compares curve behavior rather than arbitrary starting scale. Raw candidate functions and the exact calibration helper are shared with the stat-range sensitivity experiment in experiments/common/damage_candidates.py; each experiment passes its own anchor explicitly. The calibration constants and offsets are experiment controls, not recommendations.

## Synthetic inputs

Two stat ranges are swept: 25–250 and 100–1000. The script tests levels 1, 25, 50, and 100; move powers 40, 80, 100, 120, and 160; and target attack/defense ratios from 1/4 through 4.

These values are deliberately synthetic. They are not inferred from creature stat drafts and must not be treated as the game's intended stat or move-power ranges.

## Scope and limitations

- Uses exact rational arithmetic; decimal values in JSON are display-only.
- Compares base-equation behavior only.
- Does not include stat stages, equipment, abilities, type, critical hits, status, weather, RNG, flooring, shields, or Vitality application.
- Candidates A, B, and D do not directly use level; Candidate C does. This is an intentional comparison of level-treatment choices.
- Passing tests confirms the experiment's implementation properties, not the suitability or balance of any equation.

No candidate is selected by this experiment. Review the report and choose the next design decision explicitly.
