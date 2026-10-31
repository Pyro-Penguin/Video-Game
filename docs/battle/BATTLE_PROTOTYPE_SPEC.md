# Battle Prototype Specification

**Status:** Draft — scope captured; several match rules remain unresolved.

## Prototype Objective
A local, PvP-style tactical battle in which one person controls both sides. The prototype is intended to validate battle rules and engine correctness, not online networking or the full RPG.

## Current Scope
| Area | Current target | Status |
|---|---|---|
| Battle format | 1 commander + 2 active monsters per side; 1 selected monster reserve | Confirmed prototype target |
| Commander | 1 commander per side | Confirmed prototype target |
| Active monsters | 2 per side | Confirmed prototype target |
| Reserve | 1 of the 3 selected monsters is held in reserve; the other 2 are active | Confirmed competitive target |
| Team preview | Register 5 monsters; select 3 monsters; commander is separate | Confirmed competitive target |
| Turn resolution | Simultaneous | Confirmed prototype target |
| Stats | Normalized | Confirmed direction; formula unresolved |
| Elements | Elemental types included | Confirmed direction; chart unresolved |
| Reserve behavior | Automatic | Provisional; trigger and timing unresolved |
| Victory | Test both sides | Unresolved exact condition |
| Content target | 2 commanders, 2 main weapons, 6 monsters with movesets | Initial content target |

## Roster Accounting — Resolved
The confirmed competitive target is five registered monsters at preview, three selected monsters, two active monsters plus one reserve, and one commander/player combatant separate from those three monsters. This is recorded in D-003 and the Battle Overview. The phrase 3v3 is shorthand only; implementation must use the explicit counts above. Story encounters may use different compositions.

## Rules That Must Be Specified
1. **Commander defeat:** Does commander knockout immediately end the match? Can the commander be protected, revived, or replaced?
2. **Reserve deployment:** What event triggers reserve entry? Is entry automatic, immediate, or at the next turn boundary? Can a player choose its position?
3. **Turn commands:** Which actions can each unit take? Can a commander and both active monsters all act in one turn?
4. **Simultaneity:** Are actions selected from the start-of-turn state and then resolved in a deterministic priority order? What happens if a target is removed before a later action resolves?
5. **Targeting:** Define legal targets, retargeting, invalidated actions, and friendly targeting.
6. **Knockouts:** Define when fainting is checked and when replacement occurs.
7. **Timing:** Define status, cooldown, duration, and end-of-turn processing order.
8. **Damage:** Define base formula, stat inputs, rounding, minimum damage, modifiers, and critical/random variance (if any).
9. **Elements:** Define the type list and complete matchup matrix, including neutral interactions.
10. **Victory/draw:** Define simultaneous commander knockouts, simultaneous last-unit knockouts, timeouts, and no-legal-action states.

## Simulation Contract (implemented as a Python fixture harness)

The command-in / state-and-events-out contract is implemented in [the battle simulation harness](../../experiments/battle_sim/README.md):
- A battle starts from a validated immutable state and explicit fixture definitions.
- Player input is expressed as commands; commands do not directly mutate battle state.
- The resolver validates the complete command set against the same turn-start snapshot.
- The resolver produces a new immutable state and ordered event log.
- Presentation is not part of the package and cannot mutate battle state.

A deterministic two-turn scenario runner and JSON trace are also included to review invalidated actions and reserve deployment across turn boundaries. This is an engine-independent rules-discovery harness, not the production C# implementation. The DamageModel is an injected pure interface; FixedDamageFixture currently supplies fixed synthetic values. Fixed damage, exact-tie fallback, automatic replacement, and commander-defeat outcomes are fixture assumptions. A pre-existing state with both commanders defeated is classified as a draw; the sequential single-target action loop cannot generate mutual KO while defeated actors lose their queued actions. The harness uses the confirmed five-to-three preview result as a fixed fixture roster (three selected monsters); it does not implement the preview UI or team legality validation.

## Non-Goals for This Prototype
- Online multiplayer, matchmaking, ranking, and server authority.
- Full seven-village campaign, quests, exploration, and cinematics.
- Large-scale monster roster or long-term progression.
- Production art and final animation.
