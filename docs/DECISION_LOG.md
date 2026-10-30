# Decision Log

Use exactly four decision statuses: **Confirmed**, **Provisional**, **Unresolved**, and **Superseded**. Confirmed records may still have unresolved details; state their scope and limits explicitly. Proposals are not decisions until the human accepts them.

## Decision Register

| ID | Topic | Status | Date | Decision and scope | Rationale / authority | Dependencies | Supersession |
|---|---|---|---|---|---|---|---|
| D-001 | Initial prototype focus | Confirmed | Not recorded | Validate coherent battle rules and a local battle before broad content production. Does not authorize engine-project creation. | Prior explicit project direction; historical rationale not recorded. | Coherent battle rules. | None |
| D-002 | Local control | Confirmed | Not recorded | One user controls both sides for the initial prototype. | Prior explicit project direction. | Local battle prototype. | None |
| D-003 | Competitive battle structure | Confirmed | Not recorded | Online target: bring five monsters, select three; field player character plus two active monsters, with one selected monster as reserve. Timing and edge cases remain open. | Prior explicit project direction. | Battle resolution and player role. | None |
| D-004 | Turn model | Confirmed | Not recorded | One action per active entity; all actions selected before resolution; priority tiers then Speed determine order. Tie-break, interruption, redirection, and invalidation details remain open. | Prior explicit project direction. | Battle structure and action definitions. | None |
| D-005 | Single-player formats | Confirmed | Not recorded | Support multiple encounter compositions, including player plus one/two monsters and companion-character formats. Maximum encounter size and exact availability remain open. | Prior explicit project direction. | Encounter composition and companion control. | None |
| D-006 | Knockout and replacement | Confirmed | Not recorded | Defeated monsters leave battle; queued action is lost if actor or target is defeated before resolution; replacements enter at end of turn if reserve remains. Exceptions and sequencing details remain open. | Prior explicit project direction. | Turn phases and victory timing. | None |
| D-007 | Monster defeat and victory | Confirmed | Not recorded | Losing monsters alone does not cause defeat; player character must also be defeated, with encounter-specific rules. Victory timing and simultaneous defeat remain open. | Prior explicit project direction. | Encounter rules and replacement timing. | None |
| D-008 | Battle stats | Confirmed | Not recorded | Players and monsters share core stats: Vitality, Attack, Defense, Special Attack, Special Defense, Speed. Exact formulas and normalization remain open. | Prior explicit project direction. | Damage equation and normalization. | None |
| D-009 | Relationship stat | Confirmed | Not recorded | Relationship effects are single-player only; OCEAN-derived dimensions may influence combat. Exact mapping and magnitude remain open; no competitive effect. | Prior explicit project direction. | Relationship design and damage modifiers. | None |
| D-010 | Stat allocation | Provisional | Not recorded | 70-point allocation and 30-point per-stat cap remain under consideration; story progression integration is unresolved. | Working proposal, not finalized balance. | Stat formula and normalization. | None |
| D-011 | Elemental system | Confirmed | Not recorded | Elemental types are included; type inventory, chart, multipliers, and immunities remain open. | Prior explicit project direction. | Type/village design and damage equation. | None |
| D-012 | Victory check timing | Provisional | Not recorded | Check victory after end-of-turn replacement as a working candidate; test edge cases before confirming. | Provisional sequencing proposal. | Knockout and replacement rules. | None |
| D-013 | Engine baseline | Unresolved | Not recorded | Unity on macOS is intended, but editor version and project root are unverified. No Unity project exists in the repository. | Current repository state. | Explicit engine setup decision. | None |
| D-014 | Canonical project priority order | Confirmed | 2026-10-30 | PROJECT_STATUS.md is the single canonical project-wide priority list. Damage-equation design resolution is Priority 1 and precedes expansion of turn queues/state loops; battle structure/resolution follows. OPEN_QUESTIONS.md groups questions in that order and does not set a competing hierarchy. This does not approve a final formula or RNG model. | Explicit human direction on 2026-10-30 resolving the conflict between the two documents. | Damage model, stat definitions, battle resolution. | None |

| D-015 | Handoff verification freshness | Confirmed | 2026-10-30 | Before committing a handoff, re-check the latest relevant CI run and confirm that it tested the exact current commit. Refresh handoff verification claims, run IDs, and artifact counts; do not carry forward stale or unverified claims. This governs reporting process only and does not alter game rules. | Process correction from review of the damage experiment handoff, intended to prevent stale verification state from being mistaken for current evidence. | Work-verification states; HANDOFF.md. | None |

## Metadata and Change Policy

- Every new decision must have a unique ID, status, ISO date, scoped record, rationale/source, dependencies where applicable, and supersession links where applicable.
- Do not invent historical dates or rationales. “Not recorded” means the repository did not establish them.
- Add a new row when a decision changes; preserve the prior record and mark it **Superseded**, linking the replacement ID.
- Keep decision status separate from work-verification state.
- Update relevant specifications and Open Questions when a decision changes.
- Follow [COLLABORATION_PROTOCOL.md](../COLLABORATION_PROTOCOL.md) for authority and process.
