# Battle Engine Gap Analysis and Roadmap

**Status:** Engineering assessment and proposed sequence. This document does not approve new battle rules, select a damage formula, or authorize a Unity/C# runtime.

## Current verified foundation

The current implementation is the pure-Python harness in [experiments/battle_sim](../../experiments/battle_sim/README.md), not a production battle engine.

It already provides:
- Immutable battle/unit snapshots and command-in / state-and-events-out resolution.
- Full active-unit command-set validation against the same turn-start snapshot.
- Priority then Speed ordering.
- The D-021 exact-Speed-tie hierarchy, with unit-ID ordering explicitly fixture-only.
- Per-target revalidation, immediate knockout state changes, and invalidated-action handling.
- End-of-turn reserve deployment through a pure selector (D-019).
- Derived battle facts and an injected encounter-specific victory policy (D-020).
- A pure injected DamageModel seam.
- Deterministic trace generation and replay tests.

Preserve these domain boundaries while the damage model and unresolved rules are finalized.

## Highest-risk gaps

### 1. Damage and effective-stat contract — current project Priority 1

The resolver currently asks an injected DamageModel for a positive integer. The CLI adapter stores combat stats outside BattleState and uses Candidate B as replaceable scaffolding. This is correct for testing the seam but not a complete domain contract.

Before selecting a final implementation, define effective-stat inputs and ownership; physical/special move categories and stat pairs; ordered modifier stages and additive/multiplicative semantics; type, critical, weather/field, status, shield, equipment, and relationship responsibilities; integer truncation points, minimum damage, immunity, multi-hit, recoil, drain, and RNG call boundaries.

D-022–D-025 remain authoritative. Candidate B c=143 is only a provisional narrowing starting point; c=100 is retained for comparison. No final formula, offset, or RNG model is selected. Playtest B remains blocked on original creature inputs.

### 2. Action model is currently attack-only

ActionCommand contains a move ID and target IDs. MoveDefinition contains fixture damage and priority. There is no domain representation yet for switching, guarding, protecting, item use, setup/status moves, healing, redirection, or commander-specific actions.

Do not add every action type as a bespoke resolver branch. First define a small typed action envelope and effect vocabulary. Distinguish actor intent/command, action definition and legal target pattern, resolution-time effect(s), costs/cooldowns/failure conditions, and emitted events. The final supported action list must come from prototype rules, not be imported wholesale from another game.

### 3. Simultaneity and mutual knockout are not fully specified

Commands are locked simultaneously, then resolved sequentially by priority/Speed. A unit defeated before its queued action loses that action. Consequently, the current loop cannot produce mutual damage knockouts from two queued single-target attacks when the first knockout removes the second actor.

D-020 allows encounter-specific draw/terminal policies, but the current test's pre-existing dual-defeat state is not proof that the resolver can produce a simultaneous mutual KO. Before changing code, decide whether the game means:
- Sequential resolution with defeated actors losing queued actions; or
- A simultaneous damage window in which eligible effects are calculated from a phase snapshot and applied together; or
- A hybrid in which some action classes resolve sequentially and specific effects are simultaneous.

This is a battle-rule decision, not an implementation detail.

### 4. Exact-Speed-tie comparison has unresolved action semantics

D-021 is implemented for supplied effectiveness ratios, but its meaning is not settled for non-damaging actions, multi-target actions, or actions targeting different units. The current single effectiveness value is attached to the whole command, not each target. The Open Questions document already records this. Do not silently redefine the comparator.

**Additional implementation risk found in source review:** `_compare_action_commands` compares effectiveness only when both commands provide a value; if either value is `None`, it falls through to HP percentage. Pairwise omission can make the comparator non-transitive, which violates the ordering contract required by `sorted(..., key=cmp_to_key(...))`. Example with equal priority and Speed: A has effectiveness 1 and 75% HP; B has undefined effectiveness and 50% HP; C has effectiveness 2 and 25% HP. Pairwise comparison yields A before B, B before C, but C before A. The resulting sort order can depend on input ordering or sorting implementation details.

Do not patch this with an arbitrary numeric sentinel. First decide when effectiveness is meaningfully comparable under D-021; then implement a total, transitive ordering contract (or explicitly omit effectiveness for action classes/target relationships where it is not comparable) and add permutation/transitivity regression tests. This is a harness correctness issue, not a new game-rule decision.

### 5. Battle-state validation and terminal semantics need a formal contract

The current fixture validates unique IDs, two sides, one commander per side, vitality bounds, and active/reserve/defeated status. It does not yet define all invariants needed for production content, such as which entity types may occupy active slots; whether commander commands are mandatory and which commands are legal; how a finished state encodes winner/draw and whether terminal states can be re-evaluated; whether a unit can be removed, revived, or change side; and whether status/cooldown/field durations tick before or after replacement and victory evaluation.

Add invariants only after the corresponding rule is decided.

## Proposed domain boundary (when implementation is authorized)

- **BattleSetup / roster validation:** owns immutable encounter configuration and legal composition; created before the match.
- **BattleState:** owns authoritative per-match state; one immutable snapshot per completed phase/turn.
- **CommandValidator:** validates complete player intents against the correct snapshot.
- **TurnResolver:** coordinates phases; owns no persistent match state.
- **ActionResolver / effect handlers:** resolve typed action effects using injected pure policies.
- **DamageCalculator:** pure deterministic formula implementation; accepts effective combat inputs and returns a structured result, not presentation text.
- **BattleFacts + VictoryPolicy:** facts are derived from state; policy classifies encounter outcomes.
- **BattleEvent stream:** records domain facts (action selected/resolved, damage, status, knockout, switch, reserve deployed, phase boundary, battle end). UI animation is a separate consumer.
- **RandomSource:** injected, seeded, and scoped to explicit roll sites; no global RNG.
- **Content definitions:** validated data for moves, abilities, status effects, types, equipment, and encounter rules.

Ownership and lifetime:
- Encounter/content definitions are immutable shared data.
- BattleState is owned by the match/session coordinator and replaced atomically with each resolved result.
- TurnResolver and effect handlers are stateless per-call services.
- Random state is owned by the match/session and advanced only at documented roll sites.
- Presentation owns no battle state; it consumes snapshots/events.
- Communication is commands in, immutable state plus ordered events out; narrow pure interfaces inject policies/calculators.

## Recommended sequence

1. **Finish Priority 1 damage design.** Narrow c=100/c=143 under the existing gates; do not broaden the formula sweep. Acquire original creature inputs for Playtest B. Keep formula, RNG, and gameplay acceptance separate.
2. **Resolve the D-021 comparator contract.** Define effectiveness comparison for non-damaging, multi-target, and cross-target actions. Decide the final tie fallback.
3. **Resolve simultaneity semantics.** Explicitly decide whether mutual KO is possible and what snapshot each action reads. Add tests for the selected rule only after approval.
4. **Define the minimum action vocabulary.** Start with the actions required by the first local prototype; specify targeting, costs, failure, and interruption.
5. **Specify phase order.** Command validation/lock, priority resolution, effects/status, knockouts, replacement, victory, duration ticks, and turn transition need an explicit ordered contract.
6. **Expand test fixtures around invariants.** Include multi-target ordering, reserve choice, no reserve, commander defeat, team wipe, draws, status-duration boundaries, invalid commands, and deterministic replay. Keep synthetic assumptions visibly labeled.
7. **Only after rule stability and explicit authorization, port the domain contract to pure C#.** Keep Unity adapters thin; no engine project is implied by this document.

## Immediate next action

Do not add more action/effect systems yet. The next authorized engineering task is focused D-022–D-025 damage-model narrowing and source-backed Playtest B input preparation. Keep comparator and simultaneity questions visible as Priority 2 blockers. No new battle rule is accepted by this assessment.
