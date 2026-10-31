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
| Combined-stat log-space damage interaction residual | **No numeric tolerance was pre-registered** | 1,320 residuals; 120 nonzero; maximum absolute residual 0.012399 natural-log units. Defined as log(combined ratio) minus summed isolated log ratios. |
| Combined-stat floored-TTK interaction residual | **No numeric tolerance was pre-registered** | 1,320 residuals; 724 nonzero; maximum absolute residual 2 hits |
| Isolated-stat TTK screen | **±1 hit is a proposed screen, not a confirmed pre-registered numeric gate** | The brief pre-registered floored TTK for any such tolerance, but did not fix ±1 as the accepted limit. Team must accept/revise the proposed ±1 isolated-stat screen |
| Combined-stat interaction TTK residual | **Separate tolerance required; no limit pre-registered** | Observed maximum residual is 2 hits, exceeding ±1 if someone were to apply that screen indiscriminately. Decide the combined-stat tolerance separately |
| Matchup TTK variance | **No numeric acceptance bound pre-registered** | Do not infer a ±1-hit matchup-variance pass. Set a bound or leave descriptive |
| Candidate B offset interval | Tested eligible points c={100,143,200,400}; sampled bounds **[100,400]** | Candidate interval only, not a selected value or proof every intermediate c passes |

The ±1-hit wording requires careful scope. The experiment brief required any ±1-hit tolerance to be assessed on floored TTK, but it did not pre-register ±1 as a numeric acceptance limit. For this review, ±1 hit is presented as a proposed isolated-stat screen only. Combined-stat interaction residuals are a separate question: the observed maximum is 2 hits, so applying ±1 to combined residuals would fail at least one observed case. The team must explicitly accept, revise, or reject the isolated ±1 screen and set or decline a separate combined-stat residual tolerance. No tolerance may be retroactively labelled pre-registered.

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

Flooring changed 439 pairwise relations, but caused no strict preference reversal. It merged 317 strict raw distinctions into ties while splitting 122 raw ties into strict orderings: flooring therefore more often collapses than creates distinctions in this sample, conservatively under-reporting ordering differences. Tie creation/removal remains meaningful and should not be collapsed into “no pairwise changes.”

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

## 7. Speed-system review pre-registration — historical 150 cap

Initial planning used **150 as the maximum base Speed stat**. Treat this as a historical design input to validate, not an accepted cap. The prior allocation proposal is **70 total points with a maximum of 30 in any one stat** (D-010, Provisional); it is not confirmed. Any Speed-tier analysis must state whether it assumes that 70/30 allocation model or a different explicitly named scenario. Do not analyze a 150 cap in isolation from the allocation budget and cap.

### Tier-density question and proposed cluster definition

Before running a Speed distribution analysis, define a decisive threshold as a Speed breakpoint at which a one-point stat/build difference changes the action order between two otherwise comparable builds, after applying the priority tier. Proposed cluster flag: **more than 2 distinct legal builds fall within ±5% of the same decisive Speed threshold**. This is a proposed operational definition for review, not an accepted balance gate. The team must accept or revise the count (>2), distance (±5%), and what qualifies as a distinct legal build before any distribution run. Report both build count and represented usage/build prevalence where available; raw build enumeration alone can overstate practical clustering.

### Keep priority mechanics separate

Priority tier is resolved before Speed under the current turn model. The Speed review may identify where priority changes the comparison set, but it must not decide priority move availability, priority magnitude, cancellation, or priority-vs-counterplay balance. Those are combat-architecture questions for Battle Structure and Resolution. Speed analysis should report ordinary same-priority ordering first, then provide clearly separated sensitivity cases for any already-defined priority rules. Do not invent priority rules to complete the Speed model.

### Required Speed review questions

1. Under the explicitly stated 150 base-Speed ceiling and provisional 70-total/30-per-stat allocation model, how dense are legal Speed tiers across representative builds?
2. How many decisive thresholds meet the proposed cluster definition (>2 distinct builds within ±5%)?
3. What is the opportunity cost of Speed investment versus Vitality and offense under the same allocation budget?
4. Do progression-derived Speed values create different clusters from competitive normalized builds?
5. Which conclusions remain valid if the provisional 70/30 allocation model changes?

No speed distribution, tier-density analysis, or action-order simulation is included in the damage experiment. The Speed review is a separate design task and does not reopen the damage experiment by itself.

## 8. Decisions required from the review

1. Accept or revise the Level-100 reference (A300/D275, P100, Vitality350) and 60 calibration anchor.
2. Accept or revise the neutral 4–6 floored-hit target.
3. Accept or revise the no-full-health-one-hit rule.
4. Accept or revise the 1.40×–1.80× specialization envelope.
5. Accept or revise zero strict pairwise reversals as the flooring gate; decide whether tie changes need a numeric bound.
6. Decide whether to adopt ±1 floored hit as an isolated-stat screen; separately set or decline a combined-stat interaction residual tolerance (observed maximum: 2 hits) and a matchup TTK variance bound.
7. Choose the desired specialization feel on the c=100/143/200/400 curve, or request a narrowly defined additional offset sample.
8. Choose derived-stat-only versus direct-level contribution, with progression evidence considered.
9. Confirm whether current stat ranges and progression-derived stats represent the intended design space.
10. Carry the historical 150 maximum base Speed into the separately pre-registered speed-tier review; explicitly confirm the assumed allocation model (provisional 70 total / 30 per stat) and accept or revise the proposed cluster definition before analysis.

## 9. Review exit criteria and hold point

The review must end in one of two states:

- **Decision reached:** The team accepts/revises the gates, accepts a level path, confirms the tested stat/progression space is adequate, and selects an offset from the stated tradeoff curve. The selected formula/parameter is recorded as **Confirmed** with scope and limitations. No third experiment runs unless the review identifies a specific uncovered gap.
- **Evidence gap identified:** The team rejects a gate or cannot choose an offset/level path on the available evidence. Record the exact disputed criterion or missing data. Any next experiment is scoped only to that rejection or gap; no general sensitivity pass is authorized. If the team accepts the gates but leaves the offset undecided without naming a concrete evidence gap, the review is not complete and must resolve the design preference rather than defaulting to another experiment.

No formula, Candidate B offset, stat band, level path, Speed cap, or new numeric residual tolerance is selected by this document. The experiment remains held. A third damage experiment requires a documented rejection or specific gap and a narrowly scoped plan.
