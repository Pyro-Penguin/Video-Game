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
- Injectable pure DamageModel interface; fixed damage remains a test-only implementation.
- Validation that every active unit submits exactly one legal command.
- Simultaneous command locking against the turn-start state.
- Priority then effective Speed ordering. The confirmed exact-Speed-tie hierarchy (D-021) is greater type effectiveness → greater % HP remaining → greater current HP → greater maximum HP stat. Ability tie advantage, Champion relationship, and hardware/tap input-registration priority are excluded. The current unit-ID fallback remains fixture-only; the hierarchy is recorded but is not yet implemented in the harness.
- Skipping an action if its actor or target is defeated before resolution.
- Immediate knockout application and end-of-turn reserve deployment. D-019 is implemented through an injected pure `ReserveSelector`: when eligible reserves do not outnumber vacancies, all deploy automatically; when multiple reserves compete for fewer vacancies, the caller must supply exactly the required unique eligible reserve IDs. Missing, duplicate, ineligible, unnecessary, and unknown-side selections are rejected. D-020 is implemented through derived immutable `BattleFacts` and an injected pure `VictoryPolicy`. `ConfiguredVictoryPolicy` supports commander defeat, monster team wipe, or both enabled (either condition independently eliminates a side); the default fixture enables commander defeat only. Tournament timeout/draw variants remain future policy configurations. A pre-existing dual-commander-defeat state is classified as a draw, but sequential single-target actions cannot generate mutual KO while defeated actors lose queued actions.

The fixture matches confirmed D-003 competitive counts: five registered monsters are represented as three selected monsters (two active, one reserve), with one commander separate, per side. Damage is fixed test data, not the damage formula. Automatic replacement, commander defeat, and unit-ID tie-breaking are explicit test assumptions. The harness does not implement five-to-three team preview, final target rules, types, RNG, status, switching, or Unity.

Decision D-017 authorizes this bounded harness in parallel with the damage-equation review. It does not approve any of its fixture rules. D-014 remains in force: damage-equation design resolution is still the formal first project priority.

### Damage experiment status
- The profile-wide specialization gate correction is committed and passed all seven CI jobs in run 41160522573.
- Candidate B c=400 correctly fails the 1.4x minimum at Defense 200 (4/3). c=100, 143, and 200 pass the corrected provisional gate; no offset is selected.
- Pokémon Generation IX remains an audit-only reference harness, not a selectable candidate.
- No damage formula, stat range, RNG model, or final numeric acceptance gate has been approved.

## Highest-Priority Next Work
1. Verify CI for the current battle-harness commits, including all battle simulation tests and documentation validation. Read back the exact files and inspect failures before proceeding.
2. Fix any implementation/test issues found by CI. Add regression tests for state invariants or event-order edge cases if needed.
3. Review the two-turn scenario trace artifact; expand into a longer scripted match only after the phase and outcome assumptions are reviewed.
4. Implement the remaining recorded rules without collapsing them into fixture assumptions: multi-reserve player choice versus single-reserve auto-deploy (D-019), encounter-configurable victory policy (D-020), then explicit target categories and multi-target invalidation. D-021's comparator is now implemented; validate its unresolved action/target edge cases before expanding targeting. Add end-of-turn phase markers before status/residual effects. Keep commander action/target rules open. True simultaneous damage remains unnecessary; sequential effects followed by a batched victory check remain the intended architecture.
5. Continue the damage-equation review and shared experiment-configuration work as a parallel track. Do not block state-machine correctness on final formula selection, but keep damage behind a replaceable pure interface.
6. Only after the rules contract is stable, port the agreed pure-domain contract to C# with differential test vectors. Do not create a Unity project until its baseline/version is explicitly established.

## Verification Boundary
The latest verified corrected-damage code/test commit e2201bc831b38a6d2ee175c934461aad7299ff05 passed all seven CI jobs in run 41160522573. The later documentation refresh passed all seven jobs in run 41160615690. The first harness CI pass found and corrected terminal-test fixture omissions and an impossible mutual-KO expectation under sequential action invalidation. The prior 15-test harness baseline passed all eight CI jobs in [run 41162480306](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41162480306), testing commit `3d6448c39e1d68043dfd6af2825ad04ab7d091cc`. The D-021 implementation initially exposed one stale expected-order assertion; corrected commit `addc55ee0004c5eb4c4c2d10af41410b3f14ce20` passed all eight CI jobs in [run 41165107246](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165107246). D-019 reserve-selection code passed CI on commit `b21a5284430171be2bd1d240a6ce0b1e4e5ce699` in [run 41165240887](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165240887). D-020 code/tests passed all eight jobs in [run 41165443061](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165443061). Phase-marker code/tests and their documentation are newer and awaiting CI.

## Do Not Assume
- The fixture composition is the final interpretation of five registered monsters / three selected monsters.
- Unit-ID ordering is an approved competitive Speed tie-break; it is fixture-only. D-021 is the confirmed user hierarchy.
- D-019 multi-reserve selection is implemented as caller-supplied pure input, not UI behavior; voluntary switching remains separate.
- Commander defeat is not the universal victory condition; D-020 derives battle facts and injects a policy. The current configured implementation treats enabled terminal conditions as OR conditions; this is an explicit policy configuration, not a universal rule.
- Fixed fixture damage is the selected damage equation.
- A production C# runtime or Unity project exists.

## Guardrails
- Repository is shared project memory; conversations are temporary.
- Preserve decision statuses: Confirmed, Provisional, Unresolved, Superseded.
- Test fixtures are not game rules. Do not add Decision Log entries for unaccepted mechanics.
- No Unity/C# implementation, online authority, matchmaking, or production content work is implied by this Python harness.
- Keep the battle domain independent of presentation, persistence, networking, and engine APIs.
