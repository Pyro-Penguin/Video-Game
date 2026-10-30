# Battle Overview

**Status:** Multiple concepts captured; exact battle format unresolved.

## Stable Direction
- Turn-based tactical combat.
- The player character participates directly alongside monster companions.
- Team selection is from a larger roster.
- Elemental interactions and character/monster build choices matter.
- A local prototype should validate rules before online PvP.

## Competing Format Notes

| Draft | Description | Status |
|---|---|---|
| Early shorthand | 2v2 turn-based battle, described as a Final Fantasy / Pokémon blend | Historical; ambiguous whether units or sides |
| Party concept | User character + 3 selected monsters from a pool of 5 | Broad party concept |
| PvP format | Bring 5 monsters to preview, select 3; described as 3v3 | Does 3v3 count player or monsters only? |
| Local prototype | 1 commander + 2 active monsters + 1 reserve per side | Prior target; not reconciled |

Do not assume these are equivalent. Decide total party size, active field size, and reserve size separately.

## Timer Proposal — Unconfirmed
- Team preview: 64 seconds.
- Move time limit: 45 seconds per turn.
- Player time: 7 minutes per player.
- Total game timer: 20 minutes.

Clarify whether move time also consumes player time, whether player time pauses during animations, and what happens on expiration.

## Team Clauses — Proposed
- **Species Clause:** No two monsters on a team share the same monster ID.
- **Item Clause:** No two monsters on a team hold the same item.
- **Open Team Lists:** Opponents can see selected roster details before the match.

The supplied tournament reference lists species, ability, held item, Tera Type or equivalent gimmick, and moveset. This is inspiration, not an adopted ruleset. Define the project's own disclosure policy.

## Level Normalization — Proposed
All monsters dynamically adjust to Level 100 during battle. This does not yet define how base stats, natures, IV-like values, effort allocation, equipment, or progression bonuses translate into normalized stats.

## Required Decisions
1. Does the player count as one of the three field units?
2. Does select three mean three monsters plus player, or three total combatants?
3. How many units are active simultaneously?
4. Is there a reserve?
5. Does player/commander defeat end the match?
6. How do preview, move, player, and match clocks interact?
7. Are all three clauses intended for competitive play?
8. What is the exact Level 100 normalization formula?