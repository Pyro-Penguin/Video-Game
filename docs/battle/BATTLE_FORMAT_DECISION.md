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

## Remaining Design Decisions

The competitive roster arithmetic is confirmed. The remaining battle-format questions concern behavior rather than counts:
1. Does commander defeat immediately end every competitive match, and what encounter-specific exceptions exist?
2. Which legal actions and target categories are available to commanders and monsters?
3. Does a replacement enter immediately, at end of turn, or at the next turn boundary?
4. Who chooses the reserve when multiple reserves are available in story encounters?
5. Which story encounters use different active-unit and reserve counts?
6. What exact tie-break and final fallback determine action order?

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
The five-to-three preview is consistent with the confirmed structure: the player/commander is separate; the three selected monsters comprise two active monsters and one reserve. The 64-second preview remains an unconfirmed timer proposal.

Timer proposals:
- Preview: 64 seconds.
- Move selection: 45 seconds per turn.
- Player clock: 7 minutes per player.
- Match clock: 20 minutes.

Define clock precedence before implementation. A practical rules spec must state whether move time also consumes player clock, when clocks pause, and the outcome on timeout.

## Production Resolver Exit Criteria
The test harness can evolve while decisions are resolved. Before treating the resolver as production behavior, specify:
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
