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
- Priority then effective Speed ordering. The confirmed exact-Speed-tie hierarchy (D-021) is implemented: greater type effectiveness → greater % HP remaining → greater current HP → greater maximum HP stat. Ability tie advantage, Champion relationship, and hardware/tap input-registration priority are excluded. The current unit-ID fallback remains fixture-only.
- Skipping an action if its actor or target is defeated before resolution.
- Immediate knockout application and end-of-turn reserve deployment. D-019 is implemented through an injected pure `ReserveSelector`: when eligible reserves do not outnumber vacancies, all deploy automatically; when multiple reserves compete for fewer vacancies, the caller must supply exactly the required unique eligible reserve IDs. Missing, duplicate, ineligible, unnecessary, and unknown-side selections are rejected. D-020 is implemented through derived immutable `BattleFacts` and an injected pure `VictoryPolicy`. `ConfiguredVictoryPolicy` supports commander defeat, monster team wipe, or both enabled (either condition independently eliminates a side); the default fixture enables commander defeat only. Tournament timeout/draw variants remain future policy configurations. A pre-existing dual-commander-defeat state is classified as a draw, but sequential single-target actions cannot generate mutual KO while defeated actors lose queued actions.

The fixture matches confirmed D-003 competitive counts: five registered monsters are represented as three selected monsters (two active, one reserve), with one commander separate, per side. Damage is fixed test data, not the damage formula. Automatic replacement, commander defeat, and unit-ID tie-breaking are explicit test assumptions. The harness does not implement five-to-three team preview, final target rules, types, RNG, status, switching, or Unity.

Decision D-017 authorizes this bounded harness in parallel with the damage-equation review. It does not approve any of its fixture rules. D-014 remains in force: damage-equation design resolution is still the formal first project priority.

### Damage experiment status
- D-025 resolves the c=400 discrepancy. At commit 4dd9fd3, the gate swept all five registered Defense profiles but used raw damage ratios; the published 1.429× value was not the band minimum. The corrected gate floors specialized and equal-stat damage before division.
- Candidate B c=400 fails D-022: floored specialization ratios range from 1.351× at Defense 200 to 1.474× at Defense 350. c=100, 143, and 200 pass the provisional specialization gate. No offset is selected.
- The corrected source, regression tests, report, D-025 record, and review documentation are in commit 1cc745f36dc093dde4380a04e7e89395253e28c3, with test-precision correction in commit 7bc26a67e2d5bb64ac89678198ee78cd582079ca.
- Exact code commit 7bc26a67e2d5bb64ac89678198ee78cd582079ca passed all eight CI jobs in run [41167917475](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41167917475), including the floored specialization regression and report smoke test.
- Pokémon Generation IX remains an audit-only reference harness, not a selectable candidate. No damage formula, stat range, RNG model, or final numeric acceptance gate has been approved.
- No validated five-creature stat/move fixture exists. The Light/Shadow stat draft is unverified and internally inconsistent; do not use it as canonical creature data.

## Highest-Priority Next Work
1. Author 3–5 actual creature stat spreads and 2–3 representative moves each. This is the current content dependency; do not fabricate a roster or substitute the unverified Light/Shadow draft.
2. Encode those approved creature/move inputs in a JSON fixture with explicit provenance and assumptions.
3. Build the text-only CLI battle runner on the existing pure-Python harness and injected DamageModel seam. Keep it bounded; no Unity/C# runtime work.
4. Run 10 manual CLI battles, record observations, and check all-pairs creature matchups for degenerate TTK outcomes.
5. Use playtest evidence to confirm or revise D-022 gates and then decide whether c=100, the c=143 starting point, or an optional c=200 best matches the intended specialization feel. Treat c=143 as a sampled starting point, not a locked constant. No final formula selection before that evidence.
6. Keep commander-defeat and team-wipe as separate outcome flags under D-020. Do not expand runtime scope.

## Verification Boundary
The latest verified damage-gate code/test commit is 7bc26a67e2d5bb64ac89678198ee78cd582079ca; it passed all eight CI jobs in run 41167917475, including stat-range sensitivity tests, generated report validation, documentation validation, battle simulation, damage equation, and the four-version damage RNG matrix. This is the exact code commit verified before this handoff refresh. The first harness CI pass found and corrected terminal-test fixture omissions and an impossible mutual-KO expectation under sequential action invalidation. The prior 15-test harness baseline passed all eight CI jobs in [run 41162480306](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41162480306), testing commit `3d6448c39e1d68043dfd6af2825ad04ab7d091cc`. The D-021 implementation initially exposed one stale expected-order assertion; corrected commit `addc55ee0004c5eb4c4c2d10af41410b3f14ce20` passed all eight CI jobs in [run 41165107246](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165107246). D-019 reserve-selection code passed CI on commit `b21a5284430171be2bd1d240a6ce0b1e4e5ce699` in [run 41165240887](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165240887). D-020 code/tests passed all eight jobs in [run 41165443061](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165443061). The c=400 gate/report audit and its floored-ratio regression are verified in run 41167917475. The current handoff/status refresh follows that verified code commit under D-015.

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
