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


### Current provisional damage decisions (2026-10-31)

D-022 records the 4–6-hit neutral pacing gate, 1.40×–1.80× 2:1 specialization envelope (evaluated across the full tested Defense band), ordinary-power no-full-health-OHKO screen, monotonicity, floored pass/fail behavior, and the synthetic working envelope Attack 200–400 / Defense 200–350 / Vitality 250–500. D-023 records derived-stat/Vitality-only level treatment and Level-100 competitive normalization. D-024 records c=143 as the exact sampled Candidate B starting point for narrowing, not a locked gameplay constant, with c=100 retained as the stronger-specialization comparison. All three are **Provisional**; no final equation or offset is selected.

Remaining Priority 1 work is deliberately narrow:
1. **Resolved by D-025:** Candidate B c=400 fails the provisional specialization gate. The original report's 1.429× value was not the full-band minimum, and the gate now uses floored damage ratios across the registered Defense profiles.
2. Narrow the next comparison to c=100 and c=143. Retain c=200 only if a softer-specialization comparison is still needed to distinguish the desired feel; no broad sweep.
3. A five-creature original-game CLI fixture is now drafted in `fixtures/original_creatures_draft.json` and documented in `docs/creatures/ORIGINAL_CREATURE_ROSTER_DRAFT.md`. It is provisional and not yet human-approved or balance evidence. Review the five roles, direct stat spreads, and 40/80/120 placeholder moves before treating it as Playtest B input. The Light/Shadow stat draft remains unverified and internally inconsistent, so it is not a substitute. Use the existing pure battle harness and injected DamageModel seam; this is not Unity/C# runtime work.
4. Run a bounded set of manual battles and all-pairs creature matchup checks. Treat the 4–6-hit gate as a provisional hypothesis until playtest; synthetic ranges do not prove real roster representativeness.

The 4,125 pairwise relation count is dimensionally reproducible as 75 matchup/Vitality coordinates × 55 candidate/offset pairs. The separate 2,775 figure is C(75,2) comparisons for one offset comparison. Log-space interaction residuals remain a mathematical diagnostic, not a formula-quality score.

## Priority 2 — Battle Structure and Resolution
1. D-021's current effectiveness field is caller-supplied and only models a single action/target ratio. Its semantics remain unresolved for non-damaging actions, multi-target actions (single value vs per-target vs aggregate), and actions targeting different units (whether cross-target comparison is meaningful). Decide whether effectiveness applies only to single-target damaging actions or define another explicit comparison contract. Do not change the comparator until decided.
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
