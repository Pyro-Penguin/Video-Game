# Battle Rules Decision Checklist

**Status:** Open decision register. Recommendations are not approved rules. A bounded pure-Python simulation harness now exists under `experiments/battle_sim/`; its assumptions are fixtures, not approved rules.
**Purpose:** Resolve the minimum coherent ruleset for a standalone local battle simulator. This is not a Unity implementation plan.

## How to use this checklist
- **Blocking:** A deterministic resolver cannot be specified without this answer.
- **Important:** Temporary test values are possible, but no balance claim is valid until resolved.
- **Deferred:** Does not block the first battle-resolution harness.
- When an answer is accepted, update this checklist, the relevant specification, and `DECISION_LOG.md` together.

## Gate A — Side composition and team selection

The competitive target's roster accounting is confirmed by D-003: register five monsters, select three monsters, field two active monsters, hold one selected monster in reserve, and field the commander separately. Do not count the commander as one of the three selected monsters. Story encounter compositions remain configurable.

| ID | Decision | Current direction / remaining question | Status |
|---|---|---|---|
| A1 | Meaning of "3v3" | Use explicit counts: 1 commander + 2 active monsters; 1 additional selected monster in reserve. "3v3" is shorthand and must not drive array sizes. | Confirmed |
| A2 | Registered roster | Five monsters enter team preview. | Confirmed |
| A3 | Selected roster | Select three monsters; commander is separate. | Confirmed |
| A4 | Active field | Commander plus two active monsters per side. | Confirmed |
| A5 | Player role | Commander/player character is a field combatant. | Confirmed |
| A6 | Reserve | One of the three selected monsters is reserve. | Confirmed |
| A7 | Replacement | Automatic replacement is a provisional prototype behavior; trigger, exact timing, and handling of multiple vacancies remain unresolved. | Provisional |
| A8 | Defeat | Broad direction: monster knockouts alone do not defeat a side; commander/player defeat is required, subject to encounter-specific rules. Exact simultaneous and no-reserve outcomes remain unresolved. | Confirmed |
| A9 | Preview | Choose three monsters from the five registered monsters; the three comprise two active and one reserve. | Confirmed |

**Remaining deliverable:** define the replacement choice/entry timing and exact match-end behavior. The five-to-three roster arithmetic is no longer a blocker.

## Gate B — Turn and action semantics

| ID | Decision | Questions to answer | Recommended test default | Priority |
|---|---|---|---|---|
| B1 | Turn phases | Exact order from command selection through end-of-turn effects? | Start effects → lock commands → resolve → apply outcomes → end effects → replacement → victory check | Blocking |
| B2 | Action economy | How many actions per active unit? Does player act independently? | One action per active unit per turn | Blocking |
| B3 | Player action | Weapon attack, ability, guard, command, or mix? | One explicit player action from a small test action set | Blocking |
| B4 | Targeting | Which unit categories can be targeted? Single-target, self, ally, area? | Explicit target IDs; no implicit targeting | Blocking |
| B5 | Simultaneity | Are choices simultaneous but execution ordered, or truly simultaneous? | Lock choices together; resolve in priority/speed order | Blocking |
| B6 | Priority and speed | How are priority brackets, speed, and ties handled? | Priority, then speed, then deterministic tie-break | Blocking |
| B7 | Invalidated action | What if target faints or becomes invalid before action executes? | Action fails; no automatic retarget unless rule says so | Blocking |
| B8 | Knockout timing | Can a unit at 0 HP still execute a queued action? | No later action after reaching 0 HP | Blocking |
| B9 | Switching | Is voluntary switching allowed, and does it consume an action? | Omit voluntary switching in first harness | Important |
| B10 | Protection | Can player protect allies? What is repeat-use drawback? | Defer until a concrete action is specified | Deferred |
| B11 | Randomness | Which rules consume RNG? How are seeds/replays handled? | Deterministic by default; seeded RNG only for explicit random rules | Important |

**Deliverables:** phase diagram and worked examples for speed ordering, mutual knockout, and a target defeated before its queued action.

## Gate C — Stats and damage

| ID | Decision | What is unresolved | Recommended test default | Priority |
|---|---|---|---|---|
| C1 | Stat vocabulary | Are HP/Atk/Def/SpA/SpD/Spe final? | Use six as provisional schema only | Important |
| C2 | Stat ownership | Species, individual, progression, equipment, class/nature, transformation layers? | Keep source layers separate; derive immutable battle-stat snapshot | Blocking |
| C3 | Normalization | What does Level 100 auto-leveling preserve/remove? | Use fixed synthetic stats for resolver tests; do not claim balance | Blocking for balance |
| C4 | Allocation | Is 70-point budget / 30 cap still intended? | Confirm or retire; do not assume | Important |
| C5 | Base damage | Exact equation and constants? | Isolate damage behind a pure function until specified | Blocking for damage tests |
| C6 | Modifier order | Power, A/D, STAB, type, critical, RNG, weather, status, screens, equipment? | Explicit ordered pipeline; do not copy another game's formula by assumption | Blocking |
| C7 | Rounding | Floor at every modifier or at named checkpoints? | Specify exact intermediate precision and rounding points | Blocking |
| C8 | RNG model | Which distribution? | None selected; existing experiment is evidence only | Important |
| C9 | STAB/type multipliers | Are 1.5x, 2x, and proposed effectiveness values final? | Keep configurable and provisional | Blocking for balance |
| C10 | Immunity/minimum | Can immunity be bypassed? Minimum damage for nonimmune hits? | Explicitly define; experiment behavior is not game policy | Blocking |
| C11 | Other mechanics | Crits, status, weather, terrain, screens, abilities, items, multi-hit? | Defer unless needed for a core test | Deferred |

**Deliverable:** canonical damage spec plus hand-calculated examples matching automated tests. The RNG experiment alone does not satisfy this.

## Gate D — Types and competitive constraints

| ID | Decision | What is unresolved | Priority |
|---|---|---|---|
| D1 | Type inventory | Which of Fire, Plant, Water, Dragon, Metal, Celestial, Earth, Electricity, Air, Light, Shadow, Prismatic, and "Strong" are actual types? | Important |
| D2 | Seven villages | Which seven are starting village types? | Important |
| D3 | Type chart | Complete attack/defense matrix, reciprocal values, and immunities? | Blocking for balance |
| D4 | Species Clause | Stable species ID or form ID? | Deferred |
| D5 | Item Clause | Exact item identity, category, or charges? | Deferred |
| D6 | Open Team Lists | Which fields are revealed, and when? | Deferred |
| D7 | Transformations | What changes, when, and under what limits? | Deferred |

## Gate E — Timers and match outcomes

| ID | Decision | What is unresolved | Priority |
|---|---|---|---|
| E1 | Preview clock | Is 64 seconds retained? | Deferred |
| E2 | Move clock | Does 45 seconds consume the 7-minute player clock? | Deferred |
| E3 | Player clock | What pauses it; what happens at zero? | Deferred |
| E4 | Match clock | What happens at 20 minutes? | Deferred |
| E5 | Disconnect/inactivity | Future online-play outcomes? | Deferred |

The first local simulator can omit real-time clocks. Timer policy is not needed to validate deterministic turn resolution.

## Gate F — Deferred beyond the battle core
- Full village/clan progression and balance.
- Campaign, quests, cinematics, and full story structure.
- Capture, storage, party management, and long-term progression.
- Online multiplayer, matchmaking, server authority, and anti-cheat.
- Complete move, ability, and equipment catalogs.
- Art, animation, audio, and mobile UI.
- Unity setup: no engine work until an actual project baseline is supplied and verified.

## Minimum rules packet before implementing a resolver
1. Per-side composition and preview diagram.
2. Unit lifecycle: active, reserve, defeated, and eligible-to-act states.
3. Legal actions, action economy, and targeting.
4. Turn phases, priority/speed/tie order, and invalid-target behavior.
5. Knockout, replacement, and victory rules.
6. Fixed synthetic stats and deterministic test damage, clearly labeled as test fixtures.
7. At least three worked turns with expected state after each phase.

**Architecture boundary:** a pure Python harness can test turn sequencing with synthetic stats and deterministic actions before the final stat formula, type chart, or RNG model exists. It must not present fixture values as approved game balance.
