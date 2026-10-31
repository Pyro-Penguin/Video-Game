# Open Questions

Questions are grouped in the canonical project-wide priority order defined only by [PROJECT_STATUS.md](../PROJECT_STATUS.md). These headings organize unresolved work; they do not establish a separate priority hierarchy. A decision can be Confirmed while implementation details remain unresolved.

## Priority 1 — Damage Equation Design
1. What is the exact deterministic base damage equation, including level treatment and constants?
2. Which move categories exist, and which attacker/defender stats do they use?
3. How are effective Attack and Defense constructed from base stats, stages, class/nature, status, abilities, and equipment?
4. Are screens included in effective Defense or applied as separate damage modifiers?
5. What is the exact order of power changes, STAB, type effectiveness, critical hits, weather/field, status, screens, abilities, equipment, relationship effects, and RNG?
6. Which modifiers are additive versus multiplicative?
7. Where exactly does integer truncation occur?
8. What is the minimum non-immune damage, and how is immunity handled?
9. Which RNG distribution is selected, and is it rolled per action, target, or hit? Keep this separate from the deterministic equation.
10. How are multi-hit damage, recoil, drain, shields, and interruption handled?

See [Damage Model](battle/DAMAGE_MODEL.md) and [Damage RNG Experiment](../experiments/damage_rng/README.md). This is the first design priority; it does not authorize selecting a final RNG model.

## Priority 2 — Battle Structure and Resolution
1. How is type effectiveness compared for exact-Speed ties when actions are non-damaging, multi-target, or target different units? What is the tie result when effectiveness is equal or undefined?
4. What is the final fallback if every user-defined criterion is equal?
5. Can a queued action be interrupted after it begins resolving, and what action types can be redirected?
6. What are the exact rules for simultaneous player defeat?
7. Which encounter rules make player-character defeat mandatory versus optional?
8. Which story encounter compositions differ from the confirmed competitive structure (one commander, two active monsters, one reserve)?

## Priority 3 — Replacement and Victory
1. What are the exact replacement phases and sequencing rules?
2. Does victory checking after replacement behave correctly when both sides have knockouts or no reserve?
3. What happens when both player characters are defeated in the same resolution window?
4. Which encounter-specific rules alter player-defeat requirements?

## Priority 4 — Stats and Progression
1. How does the 70-point allocation and 30-point cap work in story mode?
2. Are points freely allocated, earned, resettable, or tied to equipment/class?
3. What does competitive normalization preserve or remove?
4. How do relationship buffs/debuffs map to OCEAN-derived relationship dimensions, and what is their cap?
5. Are relationship effects applied to the player, companions, monsters, or only bonded units?

## Priority 5 — Types and Competitive Rules
1. Which affinities are actual battle types?
2. Which seven types/villages form the initial structure?
3. What are all type multipliers and immunities?
4. What are the exact Species Clause, Item Clause, and Open Team List rules?
5. What are timer precedence, pause behavior, and timeout outcomes?

## Priority 6 — Balance Input Audit
1. Which Light/Shadow stat drafts are current, and which are obsolete?
2. What provenance and normalization are required before those drafts can be used as balance inputs?

## Priority 7 — Story and Feature Scope
1. What is the protagonist's role in the AI-related coup?
2. What agency do the Light and Shadow mythical creatures have?
3. Is the Portal Gauntlet the primary capture mechanic?
4. Is the old man the first companion, the respec guide, or both?
5. Is the mother-as-leader succession story part of the main plot?
6. Which exploration features are core versus optional: shrinking, rideable monsters, Dimengeon-like encounter storage, and Nemesis-style rivals?

## Project Integration (Deferred)
1. What Unity editor version will be used?
2. Where is the actual Unity project root, and does it contain Assets/, Packages/, and ProjectSettings/?
3. Which existing archive, if any, is the canonical starting point?
4. Are there scripts or assets that must be preserved?

## Deferred Until the Battle Core Is Stable
- Full campaign/world structure and village-specific progression.
- Online matchmaking, server authority, and anti-cheat implementation.
- Save format and long-term progression persistence.
- Final art pipeline and production asset creation.
- Localization, analytics, monetization, and live operations.
