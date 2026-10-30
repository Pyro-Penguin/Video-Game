# Expanded Damage Sensitivity — Results

**Evidence:** Expanded code/report passed all seven CI jobs in [run 41094836607](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41094836607). Artifact `expanded-damage-sensitivity-report` was downloaded and inspected. Follow-up documentation passed all seven jobs in [run 41094929165](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41094929165).

**Design status:** Synthetic evidence only. No formula, stat band, level policy, or TTK rule has been selected. Current human preferences remain provisional in the Damage Equation Decision Brief; they are not Decision Log entries.

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

Clean 2:1 specialization compares Attack 600 / Defense 300 against equal Attack 300 / Defense 300 at Power 100, Level 100. All TTK values use integer-floored damage.

| Candidate | Neutral floored TTK | 2:1 damage ratio | Combined numeric gates |
|---|---:|---:|---|
| A — direct ratio | 6 | 2.000× | Fail: too volatile |
| B — c=0 | 6 | 2.000× | Fail |
| B — c=25 | 6 | 1.923× | Fail |
| B — c=50 | 6 | 1.857× | Fail |
| B — c=71 | 6 | 1.809× | Fail |
| B — c=100 | 6 | 1.750× | **Pass** |
| B — c=143 | 6 | 1.677× | **Pass** |
| B — c=200 | 6 | 1.600× | **Pass** |
| B — c=400 | 6 | 1.429× | **Pass** |
| C — direct level | 6 | 1.977× | Fail |
| D — bounded share | 6 | 1.333× | Fail: too compressed |

All candidates pass neutral TTK and no-full-HP-one-hit checks at the named reference. The four B offsets listed as passing also meet the specialization gate. This is screening evidence, not a selection.

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

The 2,695 rows include single-stat controls plus Attack×Defense, Attack×Vitality, Defense×Vitality, and Attack×Defense×Vitality combinations. Each participating stat receives −20%, −10%, −5%, +5%, +10%, or +20%, with integer stat values floored. The report calculates raw-damage and floored-TTK interaction residuals against the corresponding single-stat controls.

Across the combined-stat portion, **1,320 interaction residuals** were evaluated (5 profiles × 11 candidate/offset variants × 4 combined groups × 6 nonzero perturbations). **660/1,320 raw-damage residuals were nonzero**; the largest absolute residual was **5 percentage points**. **721/1,320 floored-TTK residuals were nonzero**; the largest absolute residual was **2 hits**. By interaction: Attack×Defense max 5 pp / 2 hits; Attack×Vitality 0 pp / 1 hit; Defense×Vitality 0 pp / 1 hit; Attack×Defense×Vitality 5 pp / 2 hits. The raw-damage maximum (5 pp) alongside a floored-TTK maximum (2 hits) is a threshold-sensitive pattern: integer flooring can amplify modest response differences when they cross KO breakpoints, rather than representing two unrelated effects. These are descriptive findings, not a pass/fail result: the pre-registration required reporting but did **not** define a numeric residual tolerance. The design review must set or explicitly decline such a tolerance before using it as a gate.

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
