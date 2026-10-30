# Damage Equation Design Review

**Purpose:** Make the current damage-equation decision answerable in one review. This package presents measured evidence and numeric criteria without selecting a formula or silently converting provisional preferences into game rules.

**Status:** Ready for human design review. The expanded experiment is held; no third experiment is authorized by default.

## 1. Stable comparison question

The current comparison uses a Level-100 neutral reference of Attack 300 / Defense 275, Power 100, Vitality 350, calibrated to 60 damage. The shared 60 anchor produces 6 floored hits at the reference. The earlier 50 anchor produced 7 hits and contradicted the provisional 4–6-hit target; D-016 records 60 as a Provisional comparison anchor. It is not a selected gameplay damage value.

Five profiles and Vitality values remain synthetic test coordinates, not accepted stat bands or creature archetypes.

## 2. Numeric gates presented for acceptance or revision

| Criterion | Current numeric value / rule | Evidence and review status |
|---|---|---|
| Calibration parity | All candidates and each B offset use the same 60-damage anchor at Level 100, P100, A300, D275 | Achieved in the comparison; accept or revise the reference |
| Neutral pacing | **4–6 floored hits** at Vitality 350 | All candidates pass at the anchor |
| Ordinary-power full-health one-hit KO | **0 allowed** at the neutral reference, absent an explicit mechanic | All candidates pass |
| 2:1 specialization envelope | **1.40×–1.80×** floored damage ratio for A600/D300 versus A300/D300 | B c=100/143/200/400 pass; other candidates fail high/low |
| Monotonicity | **0 violations**: Attack up cannot lower damage; Defense up cannot raise damage; Vitality up cannot lower TTK | Retain as a hard test invariant; confirm coverage before acceptance |
| Strict pairwise reversal under flooring | **0 strict reversals** | Pass: 0/4,125. Separately, 122 raw ties became strict floored relations and 317 strict raw relations became ties |
| Pairwise tie changes | Report count and direction; no numeric cap currently pre-registered | 439 total relation changes; decide whether tie creation/removal needs a bound |
| Combined-stat raw interaction residual | **No numeric tolerance was pre-registered** | 1,320 residuals; 660 nonzero; maximum absolute residual 5 percentage points |
| Combined-stat floored-TTK interaction residual | **No numeric tolerance was pre-registered** | 1,320 residuals; 721 nonzero; maximum absolute residual 2 hits |
| Matchup TTK variance | **No ±1-hit acceptance bound was numerically pre-registered** | Do not claim a ±1-hit pass. Set a bound or leave this descriptive |
| Candidate B offset interval | Tested eligible points c={100,143,200,400}; sampled bounds **[100,400]** | Candidate interval only, not a selected value or proof every intermediate c passes |

The review must explicitly decide whether to add numeric limits for interaction residuals and matchup variance. Do not backfill tolerances after seeing the results and describe them as pre-registered.

## 3. Candidate B is a design tradeoff curve

All four values meet the current neutral TTK, no-one-hit, and 2:1 specialization gates. Their design implications differ:

| Offset c | 2:1 damage ratio | Floored matchup-order changes vs c=100 | Design interpretation |
|---:|---:|---:|---|
| 100 | 1.750× | 0% baseline | Strongest specialization advantage in this eligible set |
| 143 | 1.677× | 1.62% | Moderately softer specialization; closest tested ordering to c=100 |
| 200 | 1.600× | 5.30% | More compressed specialization advantage |
| 400 | 1.429× | 17.19% | Softest specialization advantage; near the lower gate boundary |

The team should choose the intended feel along this curve: how much should focused Attack investment outperform an equal-stat build? c=143 is not the default merely because its ordering is stable. c=400 is not preferable merely because it compresses extremes. The design answer selects the point; the experiment describes the tradeoffs.

## 4. Flooring interpretation

The 4,125 comparisons contain:
- 122 cases where two raw TTK values were tied but flooring made them strictly ordered.
- 317 cases where raw TTK was strictly ordered but flooring made them tied.
- 0 cases where a strict ordering became the opposite strict ordering.

Flooring changed 439 pairwise relations, but caused no strict preference reversal. Tie creation/removal remains meaningful and should not be collapsed into “no pairwise changes.”

## 5. Level treatment

The level sweep holds derived stats constant to isolate the direct level term. The Level-1 direct-level TTK of 88 is not a story-mode prediction: real low-level combatants would have proportionally lower derived stats. The table measures sensitivity to the level term's strength, not the combined result of a progression curve. Review the preferred path:
- Level affects damage through derived stats / Vitality only; or
- Level also contributes a separate direct damage term.

The second path cannot be selected from this table without progression-derived stat curves.

## 6. Stat-scale and progression adequacy gate

Before any further experiment, answer both questions:

1. Do the current synthetic Attack/Defense/Vitality ranges represent the intended competitive design space?
2. Do the intended progression-derived stats represent story progression well enough to judge the level path?

If both answers are **yes**, no third damage experiment is needed before narrowing the formula/offset choice against accepted gates.

If either answer is **no**, specify the exact gap (which stat range, progression band, level interval, or interaction is missing). Any third experiment must be scoped only to that gap. No general-purpose wider sensitivity pass is authorized by this review.

## 7. Speed-system dependency — historical 150 cap

Initial planning used **150 as the maximum base Speed stat**. Treat this as a historical design input to validate, not an accepted cap. The battle model orders actions by priority tier and then Speed, so the Speed scale must be reviewed alongside stat allocation and progression before the speed rule is locked.

The review should ask whether a 150 ceiling creates useful tier density across realistic builds, whether small Speed investments cross too many decisive breakpoints, and how priority effects interact with Speed. Do not extrapolate speed-tier balance from the damage experiment: it contains no Speed distributions or action-order simulation. Keep Speed analysis as a parallel design dependency for the later battle-structure review; it does not reopen or extend the damage experiment by itself.

## 8. Decisions required from the review

1. Accept or revise the Level-100 reference (A300/D275, P100, Vitality350) and 60 calibration anchor.
2. Accept or revise the neutral 4–6 floored-hit target.
3. Accept or revise the no-full-health-one-hit rule.
4. Accept or revise the 1.40×–1.80× specialization envelope.
5. Accept or revise zero strict pairwise reversals as the flooring gate; decide whether tie changes need a numeric bound.
6. Set or decline numeric tolerances for combined-stat residuals and matchup TTK variance.
7. Choose the desired specialization feel on the c=100/143/200/400 curve, or request a narrowly defined additional offset sample.
8. Choose derived-stat-only versus direct-level contribution, with progression evidence considered.
9. Confirm whether current stat ranges and progression-derived stats represent the intended design space.
10. Carry the historical 150 maximum base Speed into a separate speed-tier review; do not silently approve it as a cap.

## 9. Hold point

No formula, Candidate B offset, stat band, level path, Speed cap, or new numeric residual tolerance is selected by this document. The experiment remains held. A third damage experiment requires a documented “no” on the stat-scale or progression-adequacy question and a narrowly scoped gap statement.
