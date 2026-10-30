# Damage Model

**Status:** Incomplete specification. The user's supplied fragments define inputs and a modifier-chain concept, but not a complete executable equation. No final damage formula is approved.

## 1. What Has Been Specified

- **Power (P):** Move base power, potentially modified by abilities during defined power-calculation steps.
- **A:** Effective Attack or Special Attack of the attacker, including applicable stat stages and move-specific physical penalties.
- **D:** Effective Defense or Special Defense of the target, including applicable stat stages, screens, and move mechanics.
- **Modifier chain:** Base damage is multiplied by sequential modifiers, with integer truncation/flooring after each step in the draft description.

The standalone RNG experiment intentionally uses a different, narrower contract: configurable multipliers are applied and the result is floored once at the end. That experiment must not be mistaken for the full game damage rule.

## 2. Missing Parts of the Equation

The current fragments are not enough to calculate one move's damage unambiguously.

### A. Base damage equation
We need the mathematical relationship between attacker level (or normalized level), move power, effective offensive stat A, effective defensive stat D, and any global scaling/additive constants. The notes provide P, A, and D, but not the equation connecting them. We must decide whether level is an explicit factor, how it scales, and whether additive constants exist. Competitive Level 100 normalization does not remove the need for a level rule in single-player.

### B. Move category and stat selection
For every damaging move, define:
- Physical, special, or another category.
- Which attacker stat it uses.
- Which defender stat it checks.
- Whether any move overrides the normal pairing.
- Whether player characters follow the same mapping as monsters.

The six current stat names are provisional: Vitality (HP), Attack, Defense, Special Attack, Special Defense, and Speed.

### C. Effective Attack and Defense
A and D need exact construction rules.

For A: base/current Attack or Special Attack; positive and negative stat stages; nature/class modifiers; status penalties; move-specific penalties or conversions; ability/item effects.

For D: base/current Defense or Special Defense; positive and negative stat stages; screens and defensive field effects; status, ability, item, and move effects; damage-category-specific exceptions.

**Potential overlap:** the draft says D includes screens, but screens could instead be independent damage modifiers. They must not be applied both inside D and again in the modifier chain.

### D. Power calculation
Specify whether each move has fixed or dynamic base power; whether ability/item power changes happen before the base equation; whether multiple power modifiers add or multiply; what happens for zero/variable power; and whether charge, target count, or missing Vitality changes power.

### E. Final modifier chain
The full list and order are missing. Candidate categories to evaluate:
1. Critical-hit modifier.
2. Same-type attack bonus (STAB) or equivalent.
3. Type effectiveness.
4. Weather/field/terrain effects.
5. Status conditions and move-specific penalties.
6. Screens and defensive effects, if not already included in D.
7. Abilities.
8. Held items and equipment.
9. Relationship-based modifiers in single-player only.
10. Random damage variation.

This is a checklist, not an assertion that every category must exist. For every modifier, specify whether it affects P, A, D, or final damage, and whether it is additive or multiplicative.

### F. Type effectiveness and immunity
The type chart is not finalized. Define exact multipliers; whether dual types multiply effectiveness values; whether immunity is zero effectiveness or a separate rule; whether abilities/items can bypass immunity; and whether effectiveness is calculated once per target or per damage hit.

### G. Rounding and integer behavior
The draft says to truncate/floor after sequential modifiers, but does not define:
- Whether intermediate values are integers or fixed-precision fractions.
- Whether modifiers use rational multipliers, decimals, or integer percentages.
- Whether flooring occurs after every modifier or only at named checkpoints.
- Whether values are clamped.
- Whether a non-immune hit has minimum damage of one.
- Whether multi-hit moves round each hit separately or after summing.

Repeated flooring can produce a different result from multiplying all modifiers and flooring once.

### H. Randomness
The RNG experiment compared six candidate models, but none has been selected. Specify the distribution and bounds; whether the roll is per action, target, or hit; whether area targets share a roll; where the roll occurs relative to modifiers and rounding; and how seeded/replayable randomness works in local tests and authoritative online play.

### I. Damage application and battle effects
The equation calculates damage, but battle resolution must also define:
- Whether damage is capped at remaining Vitality.
- Whether shields/barriers absorb damage before Vitality.
- Whether damage triggers reactions, interruption, redirection, or contact effects.
- Whether recoil/drain uses calculated damage or actual Vitality lost.
- Whether damage-over-time uses the same formula or a separate rule.
- How simultaneous damage and knockouts are recorded.

These are adjacent resolution rules, not necessarily part of the base equation.

## 3. Recommended Calculation Separation

Keep the implementation conceptually split into pure stages:

1. **Move definition:** category, base power, type, target pattern, and move tags.
2. **Stat selection:** choose attack and defense stats.
3. **Effective stat calculation:** apply stages and relevant effects exactly once.
4. **Power calculation:** apply defined power-changing effects.
5. **Base damage:** evaluate the selected base equation.
6. **Modifier pipeline:** apply approved modifiers in documented order.
7. **Random variation:** apply the selected RNG rule at its specified point.
8. **Rounding and clamping:** apply exact integer behavior.
9. **Damage application:** subtract actual damage from shields/Vitality and emit resulting battle events.

This is a proposed decomposition, not a chosen formula. It prevents screens, abilities, equipment, or status from being counted twice.

## 4. Relationship Stat Boundary

Relationship with the Champion is intended for single-player only. Keep it out of the shared competitive stat formula.

The existing OCEAN relationship design is event-driven: personality traits influence how characters appraise events and update persistent relationship dimensions such as Trust, Respect, Affection, and Rivalry. Derived reactions such as fear, resentment, jealousy, or contempt should not automatically become combat stats.

The missing combat design is a separate mapping:
- Which relationship dimension can affect combat?
- Does it affect damage, defense, accuracy, action priority, recovery, or a narrow special trigger?
- What are the maximum/minimum combat modifiers?
- Can negative relationship ever cause a debuff?
- Is the effect deterministic and visible?
- Does it apply to the player character, companion characters, monsters, or only bonded monsters?

Do not apply raw OCEAN scores directly to damage. Convert relationship into a bounded, explicit single-player battle modifier through a separate rules layer.

## 5. Suggested First Decisions

1. Choose the base damage equation, including level treatment and constants.
2. Define physical/special move stat pairing and construction of A and D.
3. Decide whether screens are part of D or final modifiers.
4. Establish the modifier list and exact order.
5. Define type effectiveness and immunity.
6. Define rounding and minimum-damage behavior.
7. Choose an RNG model and exact placement.
8. Add critical hits, statuses, weather, abilities, items, and single-player relationship effects only after the core is testable.

## 6. Minimum Worked Examples

Before treating the formula as implementable, calculate and test:
- Neutral physical hit.
- Neutral special hit.
- Same-type hit.
- Super-effective and resisted hits.
- Immunity.
- Attack and Defense stage changes.
- Screen interaction.
- Minimum damage and a one-hit knockout boundary.
- A case where sequential flooring differs from flooring only once.
- A single-player relationship modifier example, kept separate from competitive calculations.

## 7. Related Experiments

See [Damage RNG Experiment](../../experiments/damage_rng/README.md). It provides evidence about candidate random distributions and repeated-hit outcomes under a simplified fixed-damage model. It does not select the base equation, modifier order, or final game rules.
