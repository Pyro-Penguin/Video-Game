# Battle Format Decision Framework

**Status:** Historical decision framework. The competitive roster/field composition is now Confirmed in D-003; this document preserves the reasoning and tracks remaining encounter-format questions.

## Why This Decision Comes First
The current notes mix roster size, active field size, player participation, and reserve count. These are separate variables. A prototype cannot be specified until each is explicit.

## Terminology
- **Player character / commander:** The human-controlled avatar as a combat unit, if present on the field.
- **Monster roster:** All monsters registered for the match.
- **Selected monsters:** Monsters chosen from the roster at team preview.
- **Active field:** Units currently able to take actions.
- **Reserve:** Selected units not currently active.
- **Side:** One player's complete combat group.

## Candidate Interpretations

| Candidate | Per-side composition | Strength | Main risk |
|---|---|---|---|
| A. Player + 2 monsters | 3 active units, no reserve unless separately defined | Clear 3-unit field; player is integral | Could be mistaken for three monsters |
| B. Player + 3 monsters | 4 total party units; field size unresolved | Matches the broad party note | Does not define simultaneous active count |
| C. Commander + 2 active monsters + 1 reserve | 1 player/commander, 2 active monsters, 1 reserve | Gives player strategic identity and supports switching | Is this called 2v2 or 3v3? |
| D. Three monsters only | 3 selected monsters; player absent or noncombat | Familiar creature-battler structure | Conflicts with player-as-combatant pillar |

## Separate Decisions Required
1. **Roster size:** How many monsters are registered before preview?
2. **Selection size:** How many monsters are locked for the match?
3. **Active monster count:** How many monsters can act simultaneously?
4. **Player role:** Is the player a field unit, a commander outside the field, or both?
5. **Reserve:** How many selected monsters wait off-field?
6. **Replacement:** Is replacement automatic, chosen, or triggered by a knockout?
7. **Defeat:** Does player-character defeat immediately end the match?
8. **Targeting:** Can attacks target the player, monsters, or either?
9. **Action economy:** Does the player receive one action, multiple actions, or issue commands to companions?
10. **Terminology:** Does the format name count all active units or monsters only?

## Confirmed Competitive Target (D-003)

The current competitive target is:
- Register five monsters for team preview.
- Select three monsters.
- Field the commander/player character separately from the monster selection.
- Field two of the three selected monsters at once.
- Hold the third selected monster as reserve.

Therefore, the per-side match composition is one commander, two active monsters, and one reserve monster. The commander is not counted among the three selected monsters. The shorthand "3v3" must not obscure these exact counts.

This is a confirmed competitive target. It does not force every story encounter to use the same composition; the engine must accept configurable encounter compositions.

## Team Preview and Timer Notes
The notes specify bringing five monsters and selecting three, with a 64-second preview. That can coexist with the prototype above only if the player is separate from the three selected monsters and the selected roster contains two active monsters plus one reserve. It does not naturally coexist with a three-monster active field plus player.

Timer proposals:
- Preview: 64 seconds.
- Move selection: 45 seconds per turn.
- Player clock: 7 minutes per player.
- Match clock: 20 minutes.

Define clock precedence before implementation. A practical rules spec must state whether move time also consumes player clock, when clocks pause, and the outcome on timeout.

## Prototype Exit Criteria
Do not begin a battle-engine implementation until a one-page rules sheet specifies:
- Exact per-side roster and field diagram.
- Player participation and defeat condition.
- Reserve and replacement behavior.
- Action count and targeting rules.
- Turn phases and simultaneous resolution ordering.
- Timeout and match-clock outcomes.

## Related Documents
- [Battle Overview](BATTLE_OVERVIEW.md)
- [Open Questions](../OPEN_QUESTIONS.md)
- [Damage Model](DAMAGE_MODEL.md)
