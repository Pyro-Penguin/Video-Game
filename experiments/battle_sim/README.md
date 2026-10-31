# Battle Simulation Harness

**Status:** Engine-independent executable prototype. Synthetic fixtures only; no gameplay rules are selected by this package.

## Purpose

Exercise the battle-domain contract before Unity exists and before the final damage equation, type chart, or RNG model is selected. This is a pure-Python rules harness, not a production runtime or balance simulator.

## Ownership and data flow

- BattleState is the authoritative immutable snapshot returned by each turn.
- UnitState, MoveDefinition, and BattleRules are immutable input data.
- Callers own the current snapshot and submit a complete tuple of ActionCommand values.
- BattleResolver owns no persistent match state. It validates commands, resolves one turn, and returns a new BattleState plus an ordered event tuple. Damage is injected through the pure DamageModel protocol; FixedDamageFixture is only the current test implementation.
- Presentation, replay storage, UI, networking, and persistence are outside the package. They may consume snapshots/events later; they must not mutate battle state.
- Communication is command-in / state-and-events-out. No global service locator, callbacks, or bidirectional references.

## Prototype assumptions (not accepted game rules)

| Concern | Harness behavior | Why it is temporary |
|---|---|---|
| Composition | One commander, two active monsters, one reserve per side | Matches a useful test fixture; roster/preview accounting remains unresolved |
| Action economy | Every active unit submits exactly one command | Current broad direction; detailed player action set unresolved |
| Selection | All commands validate against the same turn-start state | Exercises simultaneous selection |
| Resolution | Priority descending, then Speed descending | Broad direction; exact ties unresolved |
| Exact tie | Unit ID ascending | Deterministic fixture fallback only; not a competitive fairness rule |
| Targeting | One opposing active unit | Simplifies core sequencing; no ally/area/self targeting |
| Damage | Positive integer supplied by an injected DamageModel; current FixedDamageFixture reads MoveDefinition fixture damage | Placeholder fixture value, not the damage formula |
| Invalidated actor/target | Queued action is skipped; no retarget | Matches current D-006 direction for defeated actors/targets |
| Replacement | Automatically deploy reserve at end of turn, roster order | Provisional behavior under test |
| Victory | Commander defeat; mutual commander defeat is a draw | Uses D-007 broad commander-survival principle; exact encounter conditions remain open |
| RNG, types, statuses | Omitted | Not needed to validate command sequencing |

The test fixture contains a commander plus three selected monsters per side (two active, one reserve). It does not implement the unresolved five-to-three team preview process.

## Turn pipeline

1. Validate the state, move definitions, and complete command set.
2. Lock all commands against the same start-of-turn snapshot.
3. Order commands by priority, Speed, then the explicit fixture tie-break.
4. Resolve actions sequentially. A defeated actor cannot act; an unavailable target is not retargeted.
5. Apply knockouts immediately to the working state.
6. Deploy reserves into vacancies at end of turn.
7. Check commander-defeat victory; a state in which both commanders are already defeated is classified as a draw. The sequential single-target action loop cannot itself create a mutual knockout because a defeated actor loses its queued action.
8. Return a new immutable state and ordered events.

## Run tests

From this directory:

    python -m unittest -v

No third-party dependencies are required. The package is compatible with Python 3.10+.

## Test coverage

- Fixture composition and validation.
- Immutable input-state behavior.
- Priority/Speed ordering.
- Defeated actor loses its queued action.
- Defeated target is not automatically retargeted.
- Reserve deployment occurs only after all locked actions resolve.
- Single commander knockout ends the match with the surviving side winning.
- A pre-existing dual-commander-defeat terminal state is classified as a draw; simultaneous damage generation remains unresolved.
- Monster knockouts alone do not end the match.
- Invalid command set rejection.
- Finished match cannot resolve another turn.

## Deliberately not implemented

Final damage math (the interface seam exists, but no production implementation), type effectiveness, RNG, status, shields, switching, protection, interruption/redirection, move targeting patterns, turn clocks, preview, online authority, Unity integration, and content progression.

Passing tests means the encoded fixture behaves consistently; it does not mean the fixture has been accepted as the game rules.
