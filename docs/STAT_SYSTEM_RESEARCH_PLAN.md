# Stat System Research Plan

**Status:** Research plan. No stat formula or point budget is approved.

## Objective
Design one stat architecture that supports both collectible monsters and the player character, while keeping progression meaningful in story mode and competitive battles fair.

## Stat Set in Current Notes
- HP
- Attack
- Defense
- Special Attack
- Special Defense
- Speed

This six-stat set is a working assumption inherited from creature-battler conventions, not a finalized rule.

## Candidate Build Inputs
The notes mention:
- Species/base stats.
- Nature-like tradeoffs.
- IV-like individual variation.
- Level.
- Equipment.
- Class-specific effects for the player.
- Transformations / Mega-like forms.
- Level 100 competitive normalization.

These inputs should not be conflated. Each needs an explicit owner and a defined place in the calculation pipeline.

## Proposed Separation of Data
1. **Species/character template:** Baseline identity and base-stat budget.
2. **Individual build:** Nature/personality and any individual variation.
3. **Progression state:** Story level and earned development.
4. **Equipment:** Explicit item modifiers and restrictions.
5. **Battle ruleset:** Competitive normalization and permitted transformations.
6. **Derived battle stats:** Final immutable snapshot used by the battle simulation.

## Questions That Must Be Answered
- Are player and monster stats calculated by the same formula?
- Is the stated player BST benchmark intended as parity with top Mega creatures, or only thematic guidance?
- Are IV-like values random, selectable, or removed in PvP?
- Does the proposed 70-point allocation with 30 maximum per stat still apply? It appears in earlier design discussions but is not included in the current raw notes, so it must be re-confirmed before adoption.
- Are classes equivalent to natures (stat tradeoff plus access rules), or separate layers?
- Does Level 100 normalization preserve nature, equipment, and build differences?
- How are HP and non-HP stats scaled?
- Can competitive rules normalize equipment and transformations?
- What happens when story progression grants a stat bonus that is illegal in PvP?

## Recommended Investigation Order
1. Freeze the six stat definitions and naming.
2. Define raw template data separately from derived battle stats.
3. Compare at least three normalization models using synthetic test creatures.
4. Measure role preservation, stat-budget fairness, and breakpoints.
5. Test edge cases: zero/low stats, extreme specialization, transformation, and equipment.
6. Only then select a formula.

## Do Not Do Yet
- Do not derive final Level 100 values from the supplied Light/Shadow tables.
- Do not treat the Mega-stat comparison as a numeric cap.
- Do not mix equipment into base stats without documenting the calculation order.
- Do not implement stat generation in Unity before the formula is testable in a standalone harness.

## Suggested Next Experiment
A Python stat-normalization comparison with synthetic species templates, build allocation, and level scaling. Keep it separate from the damage RNG experiment and report role preservation and budget constraints.