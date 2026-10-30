# Damage Equation Decision Brief

**Status:** Investigation brief only. No equation, constants, modifier order, or RNG model is approved.

## Objective

Select a deterministic base-damage model that is understandable, tunable, testable, and compatible with story progression and competitive normalization. Keep the deterministic equation separate from random variation and from applying damage to battle state.

This brief expands the Priority 1 investigation in [PROJECT_STATUS.md](../../PROJECT_STATUS.md) and the open items in [Damage Model](DAMAGE_MODEL.md). It does not change any Decision Log entry.

## Current constraints from the project

- Shared core stats are intended for player characters and monsters: Vitality, Attack, Defense, Special Attack, Special Defense, and Speed.
- Physical and special attacks are expected to select corresponding offensive and defensive stats, but exact categories and exceptions remain open.
- Competitive battles are intended to normalize combatants to Level 100; the story mode still needs meaningful level progression.
- Equipment, class/nature tradeoffs, stat stages, abilities, status, type effectiveness, and single-player relationship effects may influence damage.
- Relationship effects are single-player only and must not leak into the competitive calculation.
- The six-stat set and stat normalization formula are still working assumptions, not finalized rules.
- The RNG experiment floors once after multiplying its simplified modifiers. That is not evidence for the full damage pipeline's rounding policy.

## Separate the decisions

Do not solve all damage questions with one formula decision. Resolve them in this order:

1. **Stat contract:** define what the offensive and defensive inputs represent (base stats, derived battle stats, stages, and any permitted modifiers).
2. **Base equation:** define level treatment, move power, attack/defense relationship, scaling constants, and additive offsets.
3. **Modifier ownership:** assign each effect to exactly one stage: effective stats, move power, post-base modifier, random variation, or damage application.
4. **Modifier order:** define the ordered deterministic pipeline.
5. **Integer behavior:** define precision, flooring checkpoints, clamps, immunity, and minimum damage.
6. **RNG contract:** separately choose distribution, sampling scope, seed/replay behavior, and placement.
7. **Application contract:** define shields, actual Vitality loss, recoil/drain basis, and simultaneous damage recording.

A formula cannot be calibrated responsibly until the scale of P, A, and D is known. The formula may be selected in parameterized form before all stat values are finalized, but constants must not be tuned against invented stat ranges.

## Candidate base-equation families

These are comparison candidates, not recommendations already accepted as game rules.

### Candidate A — Direct multiplicative ratio

\[
B = K \cdot P \cdot \frac{A}{D}
\]

- **Advantages:** compact, intuitive, easy to inspect; doubling power doubles raw damage; doubling attack doubles damage; doubling defense halves damage.
- **Risks:** highly sensitive to extreme A/D ratios; low defense can produce runaway damage; requires a defined scale constant K and a nonzero defensive floor.
- **Questions:** Is the ratio too volatile for story progression? Should effective stats be clamped or softened?

### Candidate B — Offset ratio

\[
B = K \cdot P \cdot \frac{A+c}{D+c}
\]

- **Advantages:** retains a ratio-based model while reducing sensitivity at low stat values; c provides a tunable softening parameter.
- **Risks:** c is another balance constant; behavior depends on the stat scale; can make small stat differences feel muted.
- **Questions:** Should c be global, level-scaled, or derived from the stat budget? What is the intended ratio at equal stats?

### Candidate C — Level-scaled cartridge-style structure

\[
B = \left(\frac{\left(\frac{2L}{5}+2\right)PA}{50D}\right)+2
\]

- **Advantages:** explicit level contribution; recognizable baseline for a creature-battler; easy to compare against familiar genre behavior.
- **Risks:** the level term may double-count progression if A and D already scale strongly with level; constants and rounding conventions are not automatically appropriate for this game's stat ranges.
- **Questions:** Should level directly affect damage if derived stats already encode level? Does competitive Level 100 normalization make the level term redundant online?

### Candidate D — Bounded offense share

\[
B = K \cdot P \cdot \frac{A}{A+D}
\]

- **Advantages:** the stat relationship is bounded between zero and one for positive inputs; avoids unbounded damage from a large A/D ratio.
- **Risks:** does not preserve the intuitive "double attack, double damage" behavior; adding the same amount to both stats changes the ratio; requires a larger scale constant K.
- **Questions:** Does this compress stat investment too much? Can it create enough damage separation between specialized and defensive builds?

## Required mathematical properties

Every candidate must be evaluated against the same property suite before selection:

| Property | Required behavior / question |
|---|---|
| Positive domain | Define behavior for A <= 0, D <= 0, P <= 0, and invalid level values. |
| Monotonic power | Increasing P must never reduce damage. |
| Monotonic offense | Increasing A must not reduce damage. |
| Monotonic defense | Increasing D must not increase damage. |
| Equal-stat anchor | Define damage at A = D for representative move powers and levels. |
| Scale behavior | Determine whether multiplying A and D by the same factor preserves damage. |
| Level behavior | Determine whether level affects damage directly, through derived stats, or both. |
| Boundedness | Identify maximum plausible damage and whether low D creates pathological spikes. |
| Integer stability | Identify where flooring changes outcomes and whether small stat changes cause abrupt breakpoints. |
| Competitive consistency | Confirm Level 100 normalization does not unintentionally erase build choices. |
| Story progression | Confirm level growth feels meaningful without making low-level encounters or high-level encounters trivial. |
| Determinism | Same inputs and same random seed must produce replayable results after RNG is specified. |

## Modifier ownership table to complete

Before implementation, each effect must have one owner and one application point.

| Effect | Candidate owner | Unresolved question |
|---|---|---|
| Move base power | Move definition / power stage | Can power be dynamic? |
| Attack / Special Attack | Effective-stat stage | Which stages, status, class/nature, equipment, and abilities apply? |
| Defense / Special Defense | Effective-stat stage | Are screens included here or applied later? Never both. |
| Critical hit | Post-base modifier | Does it bypass stages, screens, or other defenses? |
| STAB equivalent | Post-base modifier | Does it stack multiplicatively with type effectiveness? |
| Type effectiveness | Post-base modifier | How do dual types and immunity work? |
| Weather / field | Power or post-base modifier | Which effects change move power versus final damage? |
| Status | Effective-stat or post-base stage | Which statuses alter offense, power, or final damage? |
| Ability / item / equipment | Explicit named stage | Avoid applying the same effect in multiple stages. |
| Relationship | Single-player-only modifier stage | Which relationship values can affect damage, and what are their bounds? |
| RNG | Randomization stage | Distribution, roll scope, seed, and exact position remain undecided. |
| Screens | Effective defense or post-base modifier | Choose exactly one ownership point. |

## Minimum comparison experiment

Build a separate standard-library Python experiment only after the team confirms representative input ranges. It should:

1. Implement each candidate equation as a pure function.
2. Use exact rational arithmetic for intermediate calculations where practical.
3. Keep base damage, deterministic modifiers, RNG, and final application as separate functions.
4. Generate a fixed matrix of levels, move powers, offensive stats, and defensive stats.
5. Assert monotonicity, domain safety, equal-stat anchors, and scale behavior.
6. Report damage curves and one-hit/two-hit KO breakpoints against representative Vitality values.
7. Include tests for every rounding checkpoint and boundary.
8. Record all input assumptions and seeds in the generated report.

Do not use guessed stat ranges as if they were project data. If ranges are needed before the stat system is settled, label them synthetic and run sensitivity analysis across multiple scales.

## Decisions required before an equation can be selected

- Confirm whether level directly appears in the equation.
- Confirm the stat scale or provide a parameterized normalization contract.
- Confirm move-power scale and representative move-power bands.
- Confirm the intended sensitivity of damage to A/D ratios.
- Confirm whether a minimum-damage rule exists outside immunity.
- Confirm the treatment of zero/invalid inputs.
- Confirm the deterministic modifier and rounding boundaries.

## Recommended next action

Create a synthetic-input comparison experiment only after choosing a representative stat scale or explicitly defining a multi-scale sensitivity sweep. Use its output to compare the four equation families; do not automatically select the highest-performing or most familiar formula. Bring the measured tradeoffs to the human for the actual design decision.
