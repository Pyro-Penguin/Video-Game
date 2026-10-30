# Damage RNG Experiment — Design Record

**Status:** Experiment specification; no final RNG model selected.

The executable experiment lives in [experiments/damage_rng](../../experiments/damage_rng/README.md).

## Required Models
1. Fixed 100%.
2. Fixed 95%.
3. Uniform integer 95–105%, inclusive.
4. Uniform integer 90–110%, inclusive.
5. Uniform integer 85–105%, inclusive, no normalization.
6. Uniform integer 85–105%, inclusive, normalized by 0.95.

## Required Exact Single-Hit Checks
Pre-RNG damage is 100. Enumerate every possible outcome against remaining HP 100, 95, and 85.

| Model | HP 100 | HP 95 | HP 85 |
|---|---:|---:|---:|
| Fixed 100% | 100% | 100% | 100% |
| Fixed 95% | 0% | 100% | 100% |
| Uniform 95–105% | 54.55% | 100% | 100% |
| Uniform 90–110% | 52.38% | 76.19% | 100% |
| Raw uniform 85–105% | 28.57% | 52.38% | 100% |
| Normalized uniform 85–105% | 52.38% | 71.43% | 100% |

## Repeated-Hit Simulation
Seeded repeated-hit simulations against 200 HP and 300 HP report mean, median, 10th percentile, 90th percentile, minimum, and maximum hits to knockout.

## Calculation Contract
- Apply RNG before flooring once at the end.
- Nonimmune damage is at least 1.
- Immunity always returns 0.
- STAB and type effectiveness are configurable experimental inputs, not finalized rules.
- JSON report includes model definitions, theoretical mean multipliers, realized damage outcomes, exact KO probabilities, simulation settings, seed, and limitations.

## Interpretation Guardrail
These results compare mathematical RNG distributions. They are not proof of balance or battle duration and do not select a final game RNG model.