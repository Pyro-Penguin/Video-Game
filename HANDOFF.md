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
- docs/battle/BATTLE_ENGINE_GAP_ANALYSIS.md
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
- Immediate knockout application and end-of-turn reserve deployment. D-019 is implemented through an injected pure ReserveSelector: when eligible reserves do not outnumber vacancies, all deploy automatically; when multiple reserves compete for fewer vacancies, the caller must supply exactly the required unique eligible reserve IDs. Missing, duplicate, ineligible, unnecessary, and unknown-side selections are rejected. D-020 is implemented through derived immutable BattleFacts and an injected pure VictoryPolicy. ConfiguredVictoryPolicy supports commander defeat, monster team wipe, or both enabled (either condition independently eliminates a side); the default fixture enables commander defeat only. Tournament timeout/draw variants remain future policy configurations. A pre-existing dual-commander-defeat state is classified as a draw, but sequential single-target actions cannot generate mutual KO while defeated actors lose queued actions.

The fixture matches confirmed D-003 competitive counts: five registered monsters are represented as three selected monsters (two active, one reserve), with one commander separate, per side. Damage is fixed test data, not the damage formula. Automatic replacement, commander defeat, and unit-ID tie-breaking are explicit test assumptions. The harness does not implement five-to-three team preview, final target rules, types, RNG, status, switching, or Unity.

Decision D-017 authorizes this bounded harness in parallel with the damage-equation review. It does not approve any of its fixture rules. D-014 remains in force: damage-equation design resolution is still the formal first project priority.

### Damage experiment status
- Analytical review corrections are committed and CI-verified: shared raw A–D candidate functions/calibration live in experiments/common/damage_candidates.py; the sensitivity and equation experiments retain separate explicit anchors and now sweep the same Candidate B offsets. experiments/stat_range_sensitivity/config.json owns the reference anchor, Defense band, specialization bounds, and provenance. Import-time validation rejects duplicate Defense coordinates.
- The specialization gate uses an explicit Defense band independent of matchup-profile labels. Isolated floored-TTK shifts are emitted separately from the combined-versus-additive interaction metric; see RESULTS.md. The Generation IX reference expresses sequential floors explicitly, with a regression test confirming equivalence to the former integer expression.
- D-025 resolves the c=400 raw-versus-floored discrepancy. The follow-up source audit at commit 9100eec found a second defect: DEFENDERS = ATTACKERS duplicated Defense 350 and omitted 300. The corrected defender sweep is independently defined as 200/250/275/300/350. c=400 still fails the floored full-band gate: 1.351× at Defense 200 through 1.474× at Defense 350; at Defense 300 the floored ratio is 1.439× (raw 1.429×).
- The corrected distinct-band source, regression test, and documentation passed all eight CI jobs in [run 41169279570](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169279570), commit 2396475901967cb7a39653ba96d0da79a5727e22.
- fixtures/creatures.json contains five explicitly non-canonical Pokémon scaffolds (Weavile, Snorlax, Machamp, Gengar, Skarmory), base stats used directly, three 40/80/120 moves each, and neutral type effectiveness. The required warning is stored in the JSON _comment field. It also defines three deterministic pipeline scenarios.
- experiments/battle_sim/cli_runner.py exercises the existing pure-Python harness and injected DamageModel seam. Candidate B c=100 is only a replaceable pipeline adapter, not an equation or offset selection. The CLI uses immutable battle snapshots and command-in / state-and-events-out interfaces; no Unity/C# runtime work was added.
- Playtest A passed: 32 battle-simulation/CLI tests; three full battles completed; each battle exercised reserve deployment and all turn-phase markers; CI ran the same fixture twice and byte-compared both JSON and readable traces. The trace is published as [pokemon-scaffold-pipeline-trace](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169363724/artifacts/13030750326).
- Exact code commit 33b352cac82520f2c6bfc0a3b151ae1b815b9e90 passed all eight CI jobs in [run 41169602974](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169602974), including the per-battle reserve-deployment assertion, corrected Defense sweep, all Python damage RNG versions, damage equation tests, documentation, and battle/CLI tests.
- Playtest A is pipeline validation only. It establishes no creature balance, 4–6-hit feel, matchup quality, or formula choice. Playtest B remains reserved for original game creatures/moves; the Light/Shadow draft remains unverified and is not a substitute.

### New research and battle-engine assessment
- docs/inspiration/MECHANIC_INTEGRATION_REVIEW.md consolidates the supplied Unciv, OpenRCT2, A Dark Room, Monument Valley, customization, Disco Elysium, Fable, and Shenmue reports. It extracts shared architecture principles and defers village, NPC, puzzle, dialogue, and customization implementation until the battle core is stable. Supplied research claims and license details are explicitly marked unaudited.
- docs/battle/BATTLE_ENGINE_GAP_ANALYSIS.md identifies the current harness boundary and the highest-risk gaps: damage/effective-stat contract, attack-only action model, unresolved mutual-KO semantics, D-021 effectiveness comparison semantics, and incomplete state/terminal invariants. It proposes domain ownership and a staged roadmap without adding rules.
- These are analysis documents only. No Decision Log entry was added, no game mechanic was promoted, and no Python battle code or Unity/C# runtime was changed.

### Navigation first-playable prototype — artifacts committed, Unity verification pending

A bounded navigation prototype package is now committed under `prototypes/navigation/`:
- `data/navigation.json` and `data/gates.json`: corrected hand-authored six-node/four-edge fixture and linker/Boolean gates.
- `FIRST_PLAYABLE_CHECKLIST.md`: scene wiring, recorded builder walkthrough, traversal/gate/dual-node/reset checklist, and concrete failure criteria.
- `PathWalker.cs`: supplied Unity movement candidate.
- `ResetReloadTests.cs`: supplied scene-reload Unity test candidate.
- `README.md`: scope, ownership/lifetime/communication boundaries, and verification limits.

This is a user-authorized, bounded parallel prototype, not a change to the canonical priority order. No Unity project or navigation domain source was added. The JSON walkthrough has not been reproduced against builder source in this repository. The C# files have not been compiled or run. Code review found a final-edge issue in PathWalker: it clears the graph and raises Arrived before assigning the exact final destination position. Fix that before using the walker in a scene. The dual-node context-switch behavior remains deliberately unresolved; the resolver can select a co-located alternate node for which no graph edge exists.

**Navigation next action:** only after the actual domain source and a Unity test scene/project are available and authorized, compile the candidate, correct the final-edge snap, then execute the checklist. The reset test also requires a real FirstPlayable scene, NavigationHost, NodeId/domain API, and FakeQuestProvider.SetOpen(bool). Do not claim Unity verification until those checks are run.

## Highest-Priority Next Work
1. Keep Playtest A's JSON fixture and CLI runner stable as an engineering scaffold. Replace the fixture's creature section only when original game creature data is approved; preserve the schema and runner contract.
2. Complete Priority 1 damage-model narrowing under D-022–D-025: compare c=100 and c=143 using the existing full-band floored gates; retain c=200 only if it adds useful information. Do not broaden the sweep or select a formula from synthetic evidence alone.
3. Prepare Playtest B inputs from 3–5 original game creatures and 2–3 representative moves each. The current creature-design inventory contains no validated roster; the Light/Shadow draft is not a valid substitute. The user must supply or approve original creature stats/moves before balance conclusions can be drawn.
4. Run bounded manual battles and all-pairs creature matchup checks through the existing runner once valid inputs exist. Record neutral pacing, matchup outliers, and observed decisions.
5. After Priority 1, resolve the D-021 comparator contract (non-damaging, multi-target, cross-target semantics and final fallback), then decide simultaneous-resolution/mutual-KO semantics before expanding the action model.
6. Do not begin village economy, NPC simulation, puzzle engine, Unity project creation, or C# runtime work until the battle-core priority and explicit authorization allow it.

## Verification Boundary
The latest verified code commit remains 33b352cac82520f2c6bfc0a3b151ae1b815b9e90; it passed all eight CI jobs in run [41169602974](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169602974). The battle-simulation job ran 32 tests and executed three complete CLI battles twice; JSON and readable outputs were byte-identical, and each battle asserted reserve deployment. The pipeline trace artifact is available at [pokemon-scaffold-pipeline-trace](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169363724/artifacts/13030750326). Documentation commits after that code commit do not change the verified code state. Refresh verification claims after the current documentation commit's CI completes; follow D-015. Historical harness CI runs and earlier implementation evidence remain recorded in the project status and decision log.

## Do Not Assume
- The fixture composition is the final interpretation of five registered monsters / three selected monsters.
- Unit-ID ordering is an approved competitive Speed tie-break; it is fixture-only. D-021 is the confirmed user hierarchy.
- D-019 multi-reserve selection is implemented as caller-supplied pure input, not UI behavior; voluntary switching remains separate.
- Commander defeat is not the universal victory condition; D-020 derives battle facts and injects a policy. The current configured implementation treats enabled terminal conditions as OR conditions; this is an explicit policy configuration, not a universal rule.
- Fixed fixture damage is the selected damage equation.
- A production C# runtime or Unity project exists.
- The supplied inspiration reports establish approved game mechanics or verified source-code facts.

## Guardrails
- Repository is shared project memory; conversations are temporary.
- Preserve decision statuses: Confirmed, Provisional, Unresolved, Superseded.
- Test fixtures are not game rules. Do not add Decision Log entries for unaccepted mechanics.
- No Unity/C# implementation, online authority, matchmaking, or production content work is implied by this Python harness.
- Keep the battle domain independent of presentation, persistence, networking, and engine APIs.
