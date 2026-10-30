# Decision Log

Record durable decisions here. Use **Confirmed**, **Provisional**, or **Unresolved**. A proposal is not a decision until explicitly accepted.

| ID | Topic | Status | Current record |
|---|---|---|---|
| D-001 | Initial prototype focus | Confirmed | Validate coherent battle rules and a local battle before broad content production. |
| D-002 | Local control | Confirmed | One user controls both sides for the initial prototype. |
| D-003 | Competitive battle structure | Confirmed direction | Online target: bring five monsters, select three; field player character + two active monsters, with one selected monster as reserve. |
| D-004 | Turn model | Confirmed direction | One action per active entity; all actions selected before resolution; priority tiers then Speed determine order. Exact tie-break and interruption rules remain open. |
| D-005 | Single-player formats | Confirmed direction | Support multiple encounter compositions, including player + 1/2 monsters and companion-character formats; max multi-encounter size remains open. |
| D-006 | Knockout and replacement | Confirmed direction | Defeated monsters leave battle; queued action is lost if actor/target is defeated before resolution; replacements enter at end of turn if reserve remains. |
| D-007 | Monster defeat and victory | Confirmed direction | Losing monsters alone does not cause defeat; player character must also be defeated, with encounter-specific player-defeat rules. Exact victory timing remains provisional. |
| D-008 | Battle stats | Confirmed direction | Shared core stat formula for players and monsters; current names include Vitality, Attack, Defense, Special Attack, Special Defense, Speed. |
| D-009 | Relationship stat | Confirmed direction | Single-player-only relationship value may provide small buffs/debuffs; exact mapping from OCEAN relationship dimensions to combat effects is unresolved. |
| D-010 | Stat allocation | Provisional | 70-point allocation and 30-point per-stat cap remain under consideration; single-player progression integration unresolved. |
| D-011 | Elemental system | Confirmed direction | Elemental types are included; type chart remains open. |
| D-012 | Victory check timing | Provisional | Check victory after end-of-turn replacement for now; test edge cases before confirming. |
| D-013 | Engine baseline | Unresolved | Unity on macOS; exact editor version and project root not yet verified. |

## Change Policy
- Add a new row when a decision is made; do not erase historical rationale.
- If a decision is superseded, mark it superseded and link the replacement ID.
- Update the relevant specification and decision log when a rule changes.
