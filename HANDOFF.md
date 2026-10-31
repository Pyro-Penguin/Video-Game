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
- D-025 resolves the c=400 raw-versus-floored discrepancy. The follow-up source audit at commit 9100eec found a second defect: `DEFENDERS = ATTACKERS` duplicated Defense 350 and omitted 300. The corrected defender sweep is independently defined as 200/250/275/300/350. c=400 still fails the floored full-band gate: 1.351× at Defense 200 through 1.474× at Defense 350; at Defense 300 the floored ratio is 1.439× (raw 1.429×).
- The corrected distinct-band source, regression test, and documentation passed all eight CI jobs in [run 41169279570](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169279570), commit `2396475901967cb7a39653ba96d0da79a5727e22`.
- `fixtures/creatures.json` now contains the five explicitly non-canonical Pokémon scaffolds (Weavile, Snorlax, Machamp, Gengar, Skarmory), base stats used directly, three 40/80/120 moves each, and neutral type effectiveness. The required warning is stored in the JSON `_comment` field. It also defines three deterministic pipeline scenarios.
- `experiments/battle_sim/cli_runner.py` exercises the existing pure-Python harness and injected `DamageModel` seam. Candidate B c=100 is only a replaceable pipeline adapter, not an equation or offset selection. The CLI uses immutable battle snapshots and command-in / state-and-events-out interfaces; no Unity/C# runtime work was added.
- Playtest A passed: 32 battle-simulation/CLI tests; three full battles completed; all turn-phase markers were present; CI ran the same fixture twice and byte-compared both JSON and readable traces. The trace is published as [pokemon-scaffold-pipeline-trace](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169363724/artifacts/13030750326).
- Exact code commit `14492fa6fb447997d93e736a3e4c25aa80ac49dd` passed all eight CI jobs in [run 41169363724](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169363724), including the corrected Defense sweep, all Python damage RNG versions, damage equation tests, documentation, and battle/CLI tests.
- Playtest A is pipeline validation only. It establishes no creature balance, 4–6-hit feel, matchup quality, or formula choice. Playtest B remains reserved for original game creatures/moves; the Light/Shadow draft remains unverified and is not a substitute.

## Highest-Priority Next Work
1. Keep Playtest A's JSON fixture and CLI runner stable as an engineering scaffold. Replace the fixture's creature section only when original game creature data is approved; preserve the schema and runner contract.
2. Run Playtest B with 3–5 actual game creatures and 2–3 representative moves each. Use the same runner/harness and replace the fixture data, not the engine code.
3. Record neutral pacing, matchup outliers, and observed decisions from Playtest B. Compare c=100 and c=143; include c=200 only if a softer-specialization point remains informative.
4. Use Playtest B evidence to confirm or revise D-022 gates and then decide whether Candidate B is viable. No final formula or offset is selected.
5. Keep commander-defeat and team-wipe as separate outcome flags under D-020. Do not expand runtime scope or begin Unity/C# implementation.

## Verification Boundary
The latest verified code commit is `14492fa6fb447997d93e736a3e4c25aa80ac49dd`; it passed all eight CI jobs in run [41169363724](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169363724). The battle-simulation job ran 32 tests and executed three complete CLI battles twice; JSON and readable outputs were byte-identical. The pipeline trace artifact is available at [pokemon-scaffold-pipeline-trace](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169363724/artifacts/13030750326). This exact-commit verification satisfies D-015 before this handoff refresh. The first harness CI pass found and corrected terminal-test fixture omissions and an impossible mutual-KO expectation under sequential action invalidation. The prior 15-test harness baseline passed all eight CI jobs in [run 41162480306](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41162480306), testing commit `3d6448c39e1d68043dfd6af2825ad04ab7d091cc`. The D-021 implementation initially exposed one stale expected-order assertion; corrected commit `addc55ee0004c5eb4c4c2d10af41410b3f14ce20` passed all eight CI jobs in [run 41165107246](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165107246). D-019 reserve-selection code passed CI on commit `b21a5284430171be2bd1d240a6ce0b1e4e5ce699` in [run 41165240887](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165240887). D-020 code/tests passed all eight jobs in [run 41165443061](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165443061). The c=400 gate/report audit and its floored-ratio regression are verified in run 41167917475. The current handoff/status refresh follows that verified code commit under D-015.

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
