# Damage Model

**Status:** Formula fragments captured; no complete game damage formula approved.

## Inputs Mentioned
- **Power:** Move base power, potentially modified by abilities during defined power-calculation steps.
- **A:** Effective Attack or Special Attack of the attacker, including applicable stat stages and move-specific rules.
- **D:** Effective Defense or Special Defense of the target, including screens, stat stages, and move mechanics.

## Modifier Chain
A draft note describes final damage as base damage multiplied by a sequential modifier chain, with integer truncation after each step. The exact order, modifier list, and rounding convention are not supplied.

## Separation from RNG Experiment
The standalone RNG experiment has a narrower requirement: apply its RNG multiplier and configurable modifiers, then floor once at the end. It must not silently implement the draft sequential-truncation chain.

These may describe different layers: an isolated experiment versus a future full game formula. The final game rule remains unresolved.

## Open Formula Questions
- Exact base damage equation and constants.
- Order of power, attack/defense, STAB, type effectiveness, random factor, critical hits, and other modifiers.
- Whether truncation occurs after each modifier or only at specified checkpoints.
- Minimum damage and immunity handling.
- Integer or fractional intermediate representation.
- Physical/special split and exceptions.
- Ability, weather, terrain, status, screen, and equipment interactions.

See [Damage RNG Experiment](../../experiments/damage_rng/README.md). Its output is evidence about RNG distributions only.