# Battle Simulation Harness

**Status:** Engine-independent executable prototype. Synthetic fixtures only; no gameplay rules are selected by this package.

## Purpose

Exercise the battle-domain contract before Unity exists and before the final damage equation, type chart, or RNG model is selected. This is a pure-Python rules harness, not a production runtime or balance simulator.

## Ownership and data flow

- BattleState is the authoritative immutable snapshot returned by each turn.
- UnitState, MoveDefinition, and BattleRules are immutable input data.
- Callers own the current snapshot and submit a complete tuple of ActionCommand values.
- BattleResolver owns no persistent match state. It validates commands, resolves one turn, and returns a new BattleState plus an ordered event tuple. It receives pure `DamageModel`, `ReserveSelector`, and `VictoryPolicy` strategies; the caller owns all per-turn choices. Damage is injected through the pure DamageModel protocol; FixedDamageFixture is only the current test implementation.
- Presentation, replay storage, UI, networking, and persistence are outside the package. They may consume snapshots/events later; they must not mutate battle state.
- Communication is command-in / state-and-events-out. No global service locator, callbacks, or bidirectional references.

## Prototype assumptions (not accepted game rules)

| Concern | Harness behavior | Why it is temporary |
|---|---|---|
| Composition | One commander, two active monsters, one reserve per side | Matches a useful test fixture; roster/preview accounting remains unresolved |
| Action economy | Every active unit submits exactly one command | Current broad direction; detailed player action set unresolved |
| Selection | All commands validate against the same turn-start state | Exercises simultaneous selection |
| Resolution | Priority descending, then Speed descending | Broad direction; exact ties unresolved |
| Exact tie | Greater type effectiveness → greater % HP remaining → greater current HP → greater maximum HP stat | D-021 is implemented as an ordering comparator. Callers may supply an exact positive effectiveness ratio per action; when either value is undefined or values are equal, comparison advances to the next criterion. HP percentage uses exact cross-multiplication. Unit ID ascending is fixture-only. Multi-target action semantics remain unsupported. |
| Targeting | One or more explicitly listed opposing active units; each target is revalidated at resolution, and a defeated target is skipped while later targets continue | Multi-target execution is a harness capability only; targeting patterns, per-target modifiers, redirection, and D-021 effectiveness semantics remain unresolved |
| Damage | Positive integer supplied by an injected DamageModel; current FixedDamageFixture reads MoveDefinition fixture damage | Placeholder fixture value, not the damage formula |
| Invalidated actor/target | Queued action is skipped; no retarget | Matches current D-006 direction for defeated actors/targets |
| Replacement | At end of turn, auto-deploy all eligible reserves when there are no more reserves than vacancies; if reserves outnumber vacancies, caller must provide an explicit selection for each vacancy | Implements D-019 through an injected pure `ReserveSelector`; selection input is caller-owned. Voluntary switching remains separate |
| Victory | Injected pure `VictoryPolicy` evaluates derived `BattleFacts`; `ConfiguredVictoryPolicy` supports commander-defeat and monster-team-wipe flags | Default fixture enables commander defeat only. With both flags enabled, either condition independently eliminates a side. Other timeout/tournament/draw policies remain future strategies |
| RNG, types, statuses | Omitted | Not needed to validate command sequencing |

The test fixture contains a commander plus three selected monsters per side (two active, one reserve). It does not implement the unresolved five-to-three team preview process.

## Turn pipeline

1. Validate the state, move definitions, complete command set, and caller-supplied reserve choices.
2. Lock all commands against the same start-of-turn snapshot.
3. Emit `PhaseStarted(action_resolution)`; order commands by priority, effective Speed, then D-021 criteria. Effectiveness is compared only when both commands provide a defined ratio; equal/undefined values advance to HP percentage, current HP, and maximum HP. Unit ID is the final fixture-only fallback.
4. Resolve actions sequentially. A defeated actor cannot act; an unavailable target is not retargeted.
5. Apply knockouts immediately to the working state.
6. Emit `PhaseCompleted(action_resolution)` and `PhaseStarted(end_of_turn_replacement)`. Resolve reserve choices at end of turn. Automatically deploy when there is no meaningful choice; require explicit caller selection when multiple eligible reserves compete for fewer vacancies. Then emit `PhaseCompleted(end_of_turn_replacement)`.
7. Emit `PhaseStarted(victory_check)`, derive immutable `BattleFacts` (commander status and active/reserve monster counts) and pass them to the injected `VictoryPolicy`. The default fixture policy ends on commander defeat; team-wipe and combined-condition configurations are available. A state in which both sides meet an enabled terminal condition is a draw. The sequential single-target action loop cannot itself create mutual damage knockout because a defeated actor loses its queued action.
8. Emit `PhaseCompleted(victory_check)` and return a new immutable state and ordered events. A non-terminal turn ends with `TurnCompleted`.

## Deterministic scenario trace

Run `python demo_scenario.py --output battle-scenario-trace.json` to generate a two-turn JSON trace. Turn one demonstrates a queued action invalidated by a knockout and end-of-turn reserve deployment; turn two demonstrates the replacement acting in the next turn. CI publishes the trace as the `battle-simulation-scenario-trace` artifact.

## Run tests

From this directory:

    python -m unittest -v

No third-party dependencies are required. The package is compatible with Python 3.10+.

## Test coverage

- Fixture composition and validation.
- Injectable damage-model substitution without changing turn sequencing.
- Two-turn trace generation, invalidated-action event, and reserve deployment.
- Ordered action-resolution, end-of-turn-replacement, and victory-check phase markers.
- Immutable input-state behavior.
- Priority/Speed ordering and the explicit fixture-only exact-tie fallback.
- Repeatable identical two-turn trace for deterministic replay.
- Defeated actor loses its queued action.
- A defeated single target is not retargeted; for a multi-target command, that target is skipped and remaining listed targets continue resolving.
- Multi-target commands reject duplicate, inactive, unknown, or allied targets at command lock.
- Single legal reserve auto-deploys after all locked actions resolve.
- Multiple legal reserves require an explicit valid selection; selected reserve deploys and unselected reserves remain in reserve.
- Missing, duplicate, ineligible, unnecessary, and unknown-side reserve selections are rejected.
- Single commander knockout ends the match with the surviving side winning.
- A pre-existing dual-commander-defeat terminal state is classified as a draw under the default policy; simultaneous damage generation remains unresolved.
- Derived battle facts and configurable commander/team-wipe victory policy, including combined-condition behavior.
- Monster knockouts alone do not end the match.
- Invalid command set rejection.
- Finished match cannot resolve another turn.

## Deliberately not implemented

Final damage math (the interface seam exists, but no production implementation), type effectiveness, RNG, status, shields, switching, protection, interruption/redirection, move targeting patterns beyond explicit target lists, per-target multi-hit/modifier semantics, turn clocks, preview, online authority, Unity integration, and content progression.

Passing tests means the encoded fixture behaves consistently; it does not mean the fixture has been accepted as the game rules.
