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

This is a user-authorized, bounded parallel prototype, not a change to the canonical priority order. No Unity project or navigation domain source was added. The JSON walkthrough has not been reproduced against builder source in this repository. The C# files have not been compiled or run. PathWalker's final-arrival ordering fix is now committed: each completed edge snaps transform.position to its destination before state advancement; final completion snapshots Arrived, clears the graph, then invokes the callback. Empty paths are a true no-op: they preserve any active traversal, do not start a new walk, and do not fire Arrived. The controller handles already-at-destination before calling SetPath. The dual-node context-switch behavior remains deliberately unresolved; the resolver can select a co-located alternate node for which no graph edge exists.

**Navigation next action:** obtain the actual domain source and a Unity test scene/project, compile the candidate, and add/run a Play Mode regression test that observes transform.position inside Arrived. The test must be demonstrated to fail against the pre-fix implementation and pass against the corrected one, then execute the remaining checklist. The reset test also requires a real FirstPlayable scene, NavigationHost, NodeId/domain API, and FakeQuestProvider.SetOpen(bool). Do not claim Unity verification until those checks are run.



### Original creature roster draft and agent workflow

- Five original creature concepts and direct stat/move inputs are in `docs/creatures/ORIGINAL_CREATURE_ROSTER_DRAFT.md` and `fixtures/original_creatures_draft.json`. Roles: physical bulwark, fast physical striker, fast special attacker, special-defense anchor, mixed disruptor.
- The draft uses the current CLI fixture schema and placeholder 40/80/120 moves. Candidate affinity names do not define types or matchups. The commander stats are also a pipeline placeholder.
- The CLI now accepts a display name for each fixture. The original draft was smoke-tested through all three scenarios at Candidate B c=100 and c=143. `experiments/battle_sim/draft_roster_screen.py` computes 25 neutral Power-80 single-attacker matchups at both offsets using the same damage adapter: mean repeated-hit-to-KO is 7.68 at c=100 and 7.76 at c=143 (range 5–12). This is not match TTK or a balance verdict; Tideforged averages 8.8 hits and deserves review for passivity. Exact code/test commit `83f817d5a88fdd22c273ce11a10fb93217e01b78` passed all eight CI jobs in [run 41218717224](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41218717224).
- Root `AGENTS.md`, Python path-scoped instructions, `docs/PROJECT_MANAGEMENT_AGENT_WORKFLOW_REVIEW.md`, and the revised milestone plan are committed. No provider quotas, generated vendor adapter, tool-specific hooks, skills, or Unity path instructions were added.

## Highest-Priority Next Work
1. Keep Playtest A's JSON fixture and CLI runner stable as an engineering scaffold. Replace the fixture's creature section only when original game creature data is approved; preserve the schema and runner contract.
2. Complete Priority 1 damage-model narrowing under D-022–D-025: after reviewing the original-creature draft, compare c=100 and c=143 using the same fixture and existing full-band floored gates; retain c=200 only if it adds useful information. Do not broaden the sweep or select a formula from synthetic evidence alone.
3. Review or revise the five provisional original creatures in `docs/creatures/ORIGINAL_CREATURE_ROSTER_DRAFT.md` and `fixtures/original_creatures_draft.json`. The fixture is schema/pipeline-tested at c=100 and c=143, but is not human-approved or balance evidence. Obtain explicit acceptance before using its matchup outputs to support balance conclusions.
4. After human review of the draft, run bounded manual battles and extend the neutral 25-pair screen into a documented matchup review. The existing Power-80 screen is only a single-attacker repeated-hit diagnostic; record matchup outliers and observed decisions without treating it as match pacing.
5. After Priority 1, resolve the D-021 comparator contract (non-damaging, multi-target, cross-target semantics and final fallback), then decide simultaneous-resolution/mutual-KO semantics before expanding the action model.
6. Do not begin village economy, NPC simulation, puzzle engine, Unity project creation, or C# runtime work until the battle-core priority and explicit authorization allow it.

## Verification Boundary
Latest repository HEAD is `3b6d70d7a5e2ca91c0158d95e3719e95dccc0e97`. Its exact-HEAD GitHub Actions run [41224842044](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41224842044) passed all eight jobs: battle simulation, damage equation, stat-range sensitivity, documentation, and damage RNG on Python 3.10–3.13. This validates the existing CI checks and documentation links. It does not execute the new local `scripts/validate.sh`; that script's Bash syntax was checked, but its full sequence still needs to be run from a complete checkout. No Unity compile or Play Mode verification has been performed.

## Parallel Art Direction Work
A provisional visual direction is documented in [Proposed Art Direction: Painterly Folklore with Diorama Skies](docs/inspiration/ART_DIRECTION_PROPOSAL.md). It explores a painterly gameplay world, a controlled pixel/dither sky treatment, atmospheric-perspective composition, and a brief high-saturation travel transition based on the user's description of Environment reference image 8. This is a proposal only: no palette, shader, rendering stack, or final art direction is accepted.

**Next art task:** create a single comparison board with painterly, pixel-grid, and dithered sky variants of the same original route composition, then review it at mobile scale. Keep it independent of battle-rule implementation. The exact image 8 asset has not been visually inspected in this review; the proposal records the user's description and the repository filename mapping.
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


### PathWalker arrival fix — source committed, verification pending

Commit `fdbae4a7f8e3e2982ff45f97e97e4bb7a96efc1f` applies the minimal snap fix. The walker now sets transform.position to the completed edge's destination before updating its cursor; final completion captures the Arrived delegate, clears the graph reference, and invokes the captured delegate. The XML contract documents that zero-length paths are a no-op and must be handled by the controller as already-at-destination.

Required falsification test: subscribe to Arrived, capture the transform inside the callback, and assert it equals the final node position. Show that the test fails against the pre-fix source and passes against the corrected source. The supplied test sketch still needs a graph fixture implemented against the real domain API. No Unity compile or Play Mode execution has been performed.

**Domain source remains absent.** The manifest in the user-provided handoff lists approved domain, Unity integration, and test files, but their complete source contents are not available in this repository. Do not recreate them from names or review summaries and label them approved source. Add them only from the complete reviewed source artifact.
