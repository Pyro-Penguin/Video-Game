# Battle Overview

**Status:** Core direction clarified by the user; several rules remain provisional or encounter-specific.

## Shared Battle Principles

- Turn-based tactical combat.
- Player character participates directly in battle.
- Every active entity receives one action per turn.
- All actions are selected before resolution.
- Turn order is determined by priority tiers, then Speed, with tie-break rules still being designed.
- Actions can be interrupted or redirected by specific moves, abilities, items, or powers.
- A target defeated before its queued action is resolved is removed from the battlefield and does not act.
- A defeated monster is removed from battle.
- A replacement enters at the end of the turn if an eligible reserve remains.
- Losing monsters alone does not cause a side to lose; the player character must also be defeated, subject to encounter-specific victory rules.
- The final character to be defeated is the winner under the current broad direction; exact simultaneous-defeat handling remains open.

## Single-Player Encounter Formats

Single-player battles are not restricted to one fixed field size. Candidate formats supplied by the user:

1. Player character + 2 monsters vs. opponent + 2 monsters, with one reserve monster per side.
2. Player character + 1 monster vs. opponent + 1 monster.
3. Player character + 1 monster vs. 2 monsters.
4. Player character + 1 monster + companion character + 1 monster vs. a corresponding opponent group.
5. Optional encounter compression: skip individual random monster encounters and fight multiple monsters at once. Maximum simultaneous monster count and scaling/encounter rules remain unresolved.

The battle engine should support configurable encounter compositions rather than hard-code the competitive field size into all story battles.

## Competitive Online Format

**User-specified format:**
- Bring 5 monsters to team preview.
- Select 3 monsters.
- Each side fields the player character + 2 monsters.
- One selected monster is held as reserve.
- Each side therefore has 1 player character, 2 active monsters, and 1 reserve monster during the match.
- The player character is separate from the three selected monsters.

This is the defined competitive target format. Remaining details include preview procedure, legal team validation, and match-ending rules.

## Turn Resolution Direction

- One action per active entity per turn.
- All actions are selected before resolution.
- Actions resolve by priority tier and then Speed.
- A unit defeated before its queued action resolves does not execute that action.
- Interruptions and redirections exist only where a specific move, ability, item, or power permits them.
- Replacements enter at end of turn.

### Proposed tie-break candidates — not finalized

The user listed:
1. Speed.
2. Ability that wins Speed ties.
3. Type effectiveness between the tied entities.
4. Higher percentage of Vitality remaining.
5. Higher current Vitality.
6. Higher maximum Vitality stat.
7. Higher relationship score with Champion.
8. Hardware/tap input priority.

This list needs refinement:
- Ability-based tie-breaks need explicit scope and stacking rules.
- Type effectiveness needs a defined comparison target; it should not create a universal ordering when tied entities target different units.
- Relationship is single-player only and must not affect competitive tie resolution.
- Client-reported tap timestamps are not trustworthy in competitive play; network latency and device differences make them unsuitable as an authoritative fairness rule. A server-authoritative tie policy must be chosen; deterministic seeded resolution is one candidate.
- If all approved tie-breakers remain equal, define a final fallback.

## Defeat and Victory

- Monster knockouts alone do not cause defeat if the player character remains alive.
- Player-character defeat conditions vary by encounter and may be defined by tournament, gym, or other battle rules.
- User's current broad principle: the last character to be defeated wins.
- Victory is currently checked after end-of-turn replacement. This is a provisional ordering choice and must be tested against simultaneous knockouts and replacement availability.

## Timer Proposal — Unconfirmed

- Team preview: 64 seconds.
- Move time limit: 45 seconds per turn.
- Player time: 7 minutes per player.
- Total game timer: 20 minutes.

Clock precedence, pause behavior, and timeout outcomes remain undefined.

## Competitive Team Clauses — Proposed

- **Species Clause:** No two monsters on a team share the same monster ID.
- **Item Clause:** No two monsters on a team hold the same item.
- **Open Team Lists:** Opponents can see selected roster details before the match.

The exact disclosure policy and clause semantics remain unresolved.

## Stat Direction

Current stat names (subject to renaming):
- Vitality (HP)
- Attack
- Defense
- Special Attack
- Special Defense
- Speed
- Relationship with User/Champion — single-player only; intended to provide small buffs/debuffs based on the OCEAN relationship implementation.

Players and monsters use the same core stat formula. The 70-point allocation with a 30-point per-stat cap remains a candidate, but its single-player progression implementation is unresolved.

## Level Normalization — Proposed

Competitive normalization and single-player progression must be treated separately. Competitive monsters are intended to normalize to the chosen battle level, but the formula and preserved build inputs are not yet specified.

## Remaining High-Priority Decisions

1. Player-character defeat and encounter-specific victory rules.
2. Exact tie-break hierarchy and online-safe final fallback.
3. Maximum monsters in compressed random encounters.
4. Exact damage equation, modifier order, rounding, and RNG placement.
5. How the 70-point allocation interacts with single-player progression.
6. Type inventory and complete effectiveness chart.
7. Timer and competitive clause semantics.
