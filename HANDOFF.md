# Developer Handoff

## Project
Original creature-collecting RPG with tactical PvP ambitions. Long-term target is mobile (iOS/Android). No Unity project or production C# runtime exists. Current work is engine-independent design and pure-Python mechanics validation.

## Mandatory Startup
Read COLLABORATION_PROTOCOL.md, then PROJECT_INDEX.md, PROJECT_STATUS.md, this handoff, docs/DECISION_LOG.md, and docs/OPEN_QUESTIONS.md before task-specific work.

## Authoritative Battle Context
- docs/battle/BATTLE_OVERVIEW.md
- docs/battle/BATTLE_PROTOTYPE_SPEC.md
- docs/battle/BATTLE_RULES_DECISION_CHECKLIST.md
- docs/battle/BATTLE_FORMAT_DECISION.md
- docs/battle/DAMAGE_MODEL.md
- docs/battle/DAMAGE_EQUATION_DESIGN_REVIEW.md
- docs/battle/DAMAGE_EQUATION_DECISION_BRIEF.md
- experiments/battle_sim/README.md

## Current Work State

### Battle simulation harness — first vertical slice committed
The pure-Python harness under experiments/battle_sim/ now exercises:
- Immutable battle-state snapshots and command-in / state-and-events-out ownership.
- Validation that every active unit submits exactly one legal command.
- Simultaneous command locking against the turn-start state.
- Priority then Speed ordering, with a deterministic unit-ID tie fallback used only as a fixture.
- Skipping an action if its actor or target is defeated before resolution.
- Immediate knockout application, end-of-turn automatic reserve deployment, and commander-defeat / mutual-defeat draw handling.

The fixture is one commander, two active monsters, and one reserve per side. Damage is fixed test data, not the damage formula. Automatic replacement, commander defeat, and unit-ID tie-breaking are explicit test assumptions. The harness does not implement five-to-three team preview, final target rules, types, RNG, status, switching, or Unity.

Decision D-017 authorizes this bounded harness in parallel with the damage-equation review. It does not approve any of its fixture rules. D-014 remains in force: damage-equation design resolution is still the formal first project priority.

### Damage experiment status
- The profile-wide specialization gate correction is committed and passed all seven CI jobs in run 41160522573.
- Candidate B c=400 correctly fails the 1.4x minimum at Defense 200 (4/3). c=100, 143, and 200 pass the corrected provisional gate; no offset is selected.
- Pokémon Generation IX remains an audit-only reference harness, not a selectable candidate.
- No damage formula, stat range, RNG model, or final numeric acceptance gate has been approved.

## Immediate Next Actions
1. Verify CI for the current battle-harness commits, including all battle simulation tests and documentation validation. Read back the exact files and inspect failures before proceeding.
2. Fix any implementation/test issues found by CI. Add regression tests for state invariants or event-order edge cases if needed.
3. Add a small multi-turn scenario fixture and a deterministic trace artifact so the complete state progression can be reviewed, not just isolated turns.
4. Reconcile unresolved battle decisions with worked examples: commander defeat, simultaneous commander knockout, no reserve remaining, multiple knockouts, and target invalidation. Keep recommendations separate from accepted rules.
5. Continue the damage-equation review and shared experiment-configuration work as a parallel track. Do not block state-machine correctness on final formula selection, but keep damage behind a replaceable pure interface.
6. Only after the rules contract is stable, port the agreed pure-domain contract to C# with differential test vectors. Do not create a Unity project until its baseline/version is explicitly established.

## Verification Boundary
The latest verified corrected-damage code/test commit e2201bc831b38a6d2ee175c934461aad7299ff05 passed all seven CI jobs in run 41160522573. The later documentation refresh passed all seven jobs in run 41160615690. The newly added battle harness and its current documentation have not yet been tested by CI; verify the workflow run for the exact latest commit before describing them as Tested.

## Guardrails
- Repository is shared project memory; conversations are temporary.
- Preserve decision statuses: Confirmed, Provisional, Unresolved, Superseded.
- Test fixtures are not game rules. Do not add Decision Log entries for unaccepted mechanics.
- No Unity/C# implementation, online authority, matchmaking, or production content work is implied by this Python harness.
- Keep the battle domain independent of presentation, persistence, networking, and engine APIs.
