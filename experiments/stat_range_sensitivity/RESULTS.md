# Expanded Damage Sensitivity — Results

**Evidence:** The updated experiment and battle harness passed all eight CI jobs in [run 41165870453](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165870453), testing commit `dc0e128897b332de48f5f935406fcb3f966df782`. Artifact `expanded-damage-sensitivity-report` was downloaded and inspected (SHA-256 `d281347a283af9d55cf466e7e50bec55f1eb8a011758cfc1153f8685ece06cf9`).

**Design status:** Synthetic evidence only. No formula, stat band, level policy, or TTK rule has been selected. Current human preferences remain provisional in the Damage Equation Decision Brief; they are not Decision Log entries.

**Residual-method update:** The implementation now computes multiplicative interaction in log space using exact rational ratios before logarithm evaluation. The figures below were regenerated from the updated CI artifact.

## Scope and calibration

| Measure | Result |
|---|---:|
| Attacker × defender pairs | 25 |
| All-vs-all rows | 825 |
| Single + combined perturbation rows | 2,695 |
| Level sweep rows | 35 |
| Raw/floored pairwise candidate comparisons | 4,125 |
| Candidate B matchup-pair comparisons per offset | 2,775 |

Five profiles remain synthetic coordinates: Balanced 300/275; Offensive 400/250; Defensive 250/350; High-pressure 400/200; Low-pressure 200/350. Competitive comparison is Level 100; Level 50 remains the historical anchor. Vitality values are 250/350/500; Power 100.

The initial expanded run's 50-damage anchor produced 7 hits against Vitality 350, outside the provisional 4–6 target from the outset. The comparison was therefore recalibrated to a shared **60-damage Level-100 anchor** at Power 100, Attack 300, Defense 275. This produces 6 floored hits (350/60 = 5.83 raw hits-to-KO). The anchor is recorded as Provisional Decision D-016: a comparison calibration, not a selected gameplay damage value; revisit it if the neutral reference stats, Vitality, ordinary move power, competitive normalization, or 4–6 target changes. Each B offset is independently calibrated to the same anchor. Candidate C uses one global calibration constant based on the same reference profile. The original Level-50/50-damage experiment remains historical evidence.

## Candidate screening

Corrected gate: 2:1 specialization is evaluated for each of the five pre-registered defender profiles. For each profile Defense D, the specialized coordinate is Attack 2D / Defense D and the equal-stat coordinate is Attack D / Defense D, at Power 100 / Level 100. Both the minimum and maximum ratio across the profile band must remain within 1.4×–1.8×. This replaces the earlier single-point Defense=300 check. All TTK values use integer-floored damage.

| Candidate | Neutral floored TTK | Full-band floored 2:1 ratio (min–max) | Combined numeric gates |
|---|---:|---:|---|
| A — direct ratio | 6 | 2.000×–2.000× | Fail: too volatile |
| B — c=0 | 6 | 2.000×–2.000× | Fail |
| B — c=25 | 6 | 1.891×–1.945× | Fail |
| B — c=50 | 6 | 1.818×–1.891× | Fail |
| B — c=71 | 6 | 1.764×–1.855× | Fail: exceeds upper bound |
| B — c=100 | 6 | 1.661×–1.786× | **Pass** |
| B — c=143 | 6 | 1.589×–1.714× | **Pass** |
| B — c=200 | 6 | 1.491×–1.632× | **Pass** |
| B — c=400 | 6 | 1.351×–1.474× | **Fail: below lower bound** |
| C — direct level | 6 | 1.964×–1.964× | Fail: too volatile |
| D — bounded share | 6 | 1.333×–1.333× | Fail: too compressed |

The ratio range is calculated from integer-floored specialized and equal-stat damage at every pre-registered Defense coordinate (200, 250, 275, 300, 350). The five coordinates are explicitly distinct in code and covered by a regression test. Both extrema must satisfy the 1.40×–1.80× gate. All candidates pass neutral TTK and no-full-HP-one-hit checks at the named reference. This is screening evidence, not a selection.

### c=400 reconciliation audit — commit 4dd9fd3

The original RESULTS.md value of 1.429× was not the minimum across the registered Defense band. It numerically corresponds to the single-point raw ratio at Defense 300. The audit found a second defect: the source at commit 4dd9fd3 aliased DEFENDERS to ATTACKERS, so its five named profiles contained only four distinct Defense values (200, 250, 275, 350, 350); Defense 300 was missing. It also calculated specialization from raw Fraction damage rather than floored per-hit damage, contrary to D-022. The defender sweep is now independent and explicitly covers 200, 250, 275, 300, and 350.

Recomputing the same Candidate B c=400 inputs with the D-022 floored-ratio definition across the corrected five-point band gives Defense 200: 77/57 = 1.351×; Defense 250: 80/57 = 1.404×; Defense 275: 81/57 = 1.421×; Defense 300: 82/57 = 1.439×; Defense 350: 84/57 = 1.474×. The worst case remains 1.351×, so c=400 fails the 1.40× minimum. The earlier raw values 1.333× at Defense 200 and 1.385× at Defense 250 are also mathematically correct, but raw values are diagnostic rather than the gate.

The gate now floors specialized and equal-stat damage before taking their ratio. Regression coverage asserts the Defense-200 c=400 result and verifies that flooring changes the ratio from 4/3 to 77/57. This is a narrow gate/report correction, not a new experiment.

## All-vs-all TTK at Vitality 350

Candidate B at c=100; rows are attackers, columns are defenders.

| Attacker ↓ / Defender → | Balanced | Offensive | Defensive | High-pressure | Low-pressure |
|---|---:|---:|---:|---:|---:|
| Balanced | 6 | 6 | 7 | 5 | 7 |
| Offensive | 5 | 5 | 6 | 4 | 6 |
| Defensive | 7 | 7 | 9 | 6 | 9 |
| High-pressure | 5 | 5 | 6 | 4 | 6 |
| Low-pressure | 8 | 8 | 10 | 7 | 10 |

Mean and range across the 25 pairings:

| Candidate | Mean floored hits | Range |
|---|---:|---:|
| A | 6.76 | 4–12 |
| B c=100 | 6.56 | 4–10 |
| B c=143 | 6.40 | 4–9 |
| B c=200 | 6.44 | 5–9 |
| B c=400 | 6.36 | 5–8 |
| C | 6.76 | 4–11 |
| D | 6.56 | 5–9 |

The mean is descriptive, not a gate. Defensive-tail outcomes are visible in the matrix and should not be hidden by aggregate averages.

## Flooring and ranking

Across 4,125 candidate-pair comparisons (25 ordered matchups × three Vitality values × 55 candidate/offset pairs), flooring changed the pairwise relation in **439 comparisons**: **122 raw ties became strict floored orderings**, while **317 raw strict orderings became floored ties**. There were **zero strict order reversals**: no pair that was strictly ordered one way before flooring became strictly ordered the opposite way after flooring. Flooring changed pairwise distinctions, but did not invert a strict preference. The 317 tie creations exceed the 122 tie splits: in this sample flooring more often merges distinctions than creates them, so it conservatively under-reports ordering differences. The simpler A/C/D audit reports two of 75 matchup/Vitality coordinates with a changed rank. The full pairwise audit includes every B offset and exposes ties.

Flooring remains mandatory. This result is specific to the Level-100 expanded matrix and does not invalidate the earlier mixed-level paired-profile flooring finding.

## Candidate B offset stability

Each c is compared with c=100 by ordering 75 matchup coordinates (25 pairs × three Vitality values), with 2,775 matchup-pair comparisons per offset.

| c | Raw ordering changes | Floored ordering changes |
|---:|---:|---:|
| 0 | 11.32% | 11.68% |
| 25 | 9.95% | 9.59% |
| 50 | 8.86% | 7.57% |
| 71 | 3.96% | 4.18% |
| 143 | 5.01% | **1.62%** |
| 200 | 8.25% | 5.30% |
| 400 | 18.31% | 17.19% |

c=143 is the most stable alternative to c=100 in floored matchup ordering. c=400 creates stronger compression but changes ordering more. Across individual matchup coordinates, the floored TTK spread across B offsets reaches 6 hits. The offset is a consequential parameter, not a cosmetic constant.

## Combined-stat interactions

The earlier screening language's ±1-hit concept must be scoped carefully. The experiment specification required any ±1-hit tolerance to use floored TTK, but did not establish ±1 as a numeric acceptance gate. The expanded combined-stat residuals reach 2 hits. A blanket ±1 rule across combined perturbations would therefore be exceeded; whether ±1 is adopted for isolated-stat screening, and what separate tolerance governs combined interactions, are design-review decisions.

The 2,695 rows include single-stat controls plus Attack×Defense, Attack×Vitality, Defense×Vitality, and Attack×Defense×Vitality combinations. Each participating stat receives −20%, −10%, −5%, +5%, +10%, or +20%, with integer stat values floored. The report calculates a log-space raw-damage interaction residual and a floored-TTK residual against corresponding single-stat controls. The log residual is `log(combined damage ratio) − sum(log(isolated damage ratios))`; zero means the effects combine multiplicatively without interaction. The ratios are calculated from exact `Fraction` values before the logarithm is evaluated. TTK residuals remain discrete and threshold-sensitive.

Across the combined-stat portion, **1,320 interaction residuals** were evaluated (5 profiles × 11 candidate/offset variants × 4 combined groups × 6 nonzero perturbations). **120/1,320 log-space damage residuals were nonzero**; the largest absolute residual was **0.012399 natural-log units**. **724/1,320 floored-TTK residuals were nonzero**; the largest absolute residual was **2 hits**. By interaction: Attack×Defense had 60 nonzero log residuals (max 0.012399) / 201 nonzero TTK residuals (max 2 hits); Attack×Vitality had 0 log residuals / 156 nonzero TTK residuals (max 1 hit); Defense×Vitality had 0 log residuals / 157 nonzero TTK residuals (max 1 hit); Attack×Defense×Vitality had 60 nonzero log residuals (max 0.012399) / 210 nonzero TTK residuals (max 2 hits). The log-space damage residual alongside a floored-TTK maximum (2 hits) remains threshold-sensitive: integer flooring can amplify modest response differences when they cross KO breakpoints, rather than representing two unrelated effects. These are descriptive findings, not a pass/fail result: the pre-registration required reporting but did **not** define a numeric residual tolerance. The design review must set or explicitly decline such a tolerance before using it as a gate.

## Level treatment and Pokémon reference harness

The Generation IX deterministic base-damage implementation is a **reference harness**, not a fifth candidate. It uses the core level/power/Attack/Defense structure with exact integer floors and a fixed 100% random factor. STAB, type, criticals, weather, items, abilities, screens, and other modifiers are excluded.

At Balanced 300/275, Power 100, Vitality 350:

| Level | Derived-stat-only path | Direct-level C | Pokémon reference |
|---:|---:|---:|---:|
| 1 | 6 hits | 88 hits | 59 hits |
| 5 | 6 | 59 | 35 |
| 10 | 6 | 39 | 24 |
| 25 | 6 | 20 | 13 |
| 50 | 6 | 11 | 7 |
| 75 | 6 | 8 | 5 |
| 100 | 6 | 6 | 4 |

**These figures isolate the level term by holding derived stats constant; in a real progression, low-level combatants would have proportionally lower stats, so the Level-1 direct-level figure is not a story-mode prediction.** Candidate C's low-level TTK demonstrates that direct-level scaling is sensitive to the strength of its level term and must be evaluated together with progression-derived stats. The Pokémon harness is not calibrated to this game's 60-damage anchor and is a mechanical reference only.

## Interpretation

1. Candidate B's currently eligible tested interval is c=100–400 at sampled points 100, 143, 200, and 400. These form a tradeoff curve, not a ranking: c=100 gives the strongest specialization response (1.750×); c=143 gives 1.677× and 1.62% floored ordering change versus c=100; c=200 gives 1.600× and 5.30%; c=400 gives the softest response (1.429×) and 17.19%. The team must choose the intended specialization feel; c=143's ordering stability is a screening metric, not a design preference.
2. A and C exceed the 2:1 specialization envelope; D falls below it.
3. Direct level scaling creates extreme low-level TTK when endgame derived stats are held constant. Actual story stat growth must be modeled before a progression decision.
4. Flooring changed ties, but did not strictly reverse pairwise ordering in this Level-100 matrix.
5. No formula is selected. Review and explicitly accept/revise the gates before any Decision Log entry.

## Limitations

No type/STAB, criticals, weather, status, abilities, items, equipment, stat stages, RNG variation, shields, multi-hit, simultaneous resolution, or final damage application. No actual creature/class data or stat-allocation model. Profiles are synthetic. The Pokémon harness is deliberately incomplete. The level-derived-only sweep holds battle stats constant. CI verifies implementation consistency, not game balance or human acceptance.
