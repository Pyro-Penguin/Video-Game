# Project Status

## Project
Original creature-collecting RPG with tactical PvP ambitions. Long-term target platform is mobile (iOS/Android). No Unity project or engine implementation exists yet.

## Current Stage
**Design consolidation, collaboration governance, and standalone mechanics experimentation.** The repository remains intentionally engine-independent.

## Verified Progress
- Documentation foundation created and indexed.
- Supplied game, story, world, creature, class, exploration, and art/audio concepts organized into topic documents.
- Battle-format contradictions preserved explicitly.
- Battle format decision framework added, including a provisional local-prototype candidate clearly marked as not approved.
- Stat system research plan added; no stat formula has been selected.
- Standalone Python damage RNG experiment and automated tests committed.
- Navigation first-playable prototype artifacts committed under `prototypes/navigation/`: corrected six-node/four-edge fixture JSON, linker/Boolean gate JSON, scene-wiring and manual playtest checklist, supplied PathWalker Unity candidate, and scene-reload Unity test candidate. This is a scoped prototype exception authorized by the user; it does not create a Unity project, change the canonical priority order, or establish a production C# runtime.
- Prior local test run recorded: 6 tests passed.
- GitHub Actions workflow executed successfully on Python 3.10, 3.11, 3.12, and 3.13; automated tests and JSON report smoke test passed in all four jobs.
- Collaboration protocol and Stage 1 governance changes committed and read back from GitHub; human review/acceptance is pending.
- Stage 2 documentation validator, malformed-document tests, and CI integration committed. GitHub Actions run 41085210865 passed the documentation job, all four Python-version experiment jobs, and the damage RNG report smoke tests.
- Damage Equation Decision Brief added; it compares candidate equation families without selecting a formula or changing game rules.
- Synthetic damage-equation comparison experiment and six automated tests added. GitHub Actions run 41086133510 passed the equation tests and report-generation smoke test, the documentation checks, and the existing four-version damage RNG matrix.
- Team-proposal stat-range sensitivity experiment added under `experiments/stat_range_sensitivity/`; five synthetic paired Attack/Defense profiles, four equation candidates, four levels, five move powers, three Vitality points, KO thresholds, and one-stat sensitivity are covered. Initial CI run [41089058406](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41089058406) passed all seven jobs. Flooring-enhanced CI run [41090778744](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41090778744) also passed all seven jobs and published the updated JSON artifact: 1,200 damage/KO rows, 120 sensitivity rows, 80 level rows; integer flooring changes KO count in 247/1,200 rows.
- Human-readable [Stat-Range Sensitivity Results](experiments/stat_range_sensitivity/RESULTS.md), numeric screening gates, and sequenced review questions added. Flooring audit of the CI JSON found the 247 changed rows distributed A=40, B=48, C=91, D=68; 60 rows change by more than one hit, all in Candidate C. Aggregate mean-TTK order is unchanged (B, D, A, C), but individual pairwise ordering changes in some scenario coordinates. Future pass/fail checks must use floored results.
- Expanded all-vs-all / combined-stat damage experiment added. Historical CI run [41094836607](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41094836607) passed all seven jobs; its artifact contained 825 matchup rows, 2,695 single/combined-stat rows, 35 level rows, and 4,125 raw/floored pairwise comparisons. The shared Level-100 calibration is 60 damage at the named Vitality-350 reference. A subsequent code review found that the specialization gate was evaluated at only one Defense coordinate; that result is superseded. The gate is now corrected to sweep all five pre-registered defender profiles, gate on both worst-case ratio bounds, and regression-test Candidate B c=400 failing at Defense 200 (4/3). Source, tests, README, and RESULTS were updated. Corrected code/test commit `e2201bc831b38a6d2ee175c934461aad7299ff05` passed all seven CI jobs in [run 41160522573](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41160522573), including the stat-range unit tests and JSON report smoke test. The c=400 audit also caught `DEFENDERS = ATTACKERS`, which duplicated Defense 350 and omitted Defense 300. The independent sweep now tests five distinct values: 200/250/275/300/350. c=400 still fails the floored gate at 1.351× worst case (Defense 200). The correction passed all eight CI jobs in [run 41169279570](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169279570).
- Handoff verification freshness rule recorded as D-015; protocol and decision log now agree.
- Battle-rule decisions D-019 through D-021 now record the user's revised exact-Speed-tie hierarchy, end-of-turn reserve policy (automatic with one legal reserve; player choice with multiple), and encounter-specific victory policies. The D-021 exact-Speed-tie comparator is implemented with exact Fraction effectiveness comparison, integer HP-percentage comparison, and fixture-only unit-ID fallback; the corrected commit passed all eight CI jobs in [run 41165107246](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165107246). D-019 multi-reserve selection is implemented through an injected pure selector and caller-supplied selection IDs, with validation and regression tests; the implementation commit passed CI in [run 41165240887](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165240887). D-020 now derives immutable battle facts and injects a pure victory policy; commander-defeat, monster-team-wipe, and combined OR-condition configurations are tested. D-020 passed CI in [run 41165443061](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165443061). Explicit `PhaseStarted`/`PhaseCompleted` markers for action resolution, end-of-turn replacement, and victory check are now implemented and regression-tested; this latest phase-marker commit is awaiting CI. Multi-target commands now support explicit target lists, per-target revalidation, skipping defeated targets while continuing to later targets, and duplicate-target validation. Regression tests cover these cases. Additional D-020 policy tests now cover mixed-condition mutual elimination and disabled terminal flags; latest code and documentation commits are awaiting CI.
- A bounded pure-Python battle simulation harness was added under `experiments/battle_sim/`. It implements immutable battle snapshots, complete command validation, simultaneous command locking, priority/Speed ordering, deterministic fixture tie-breaking, invalidated-action handling, knockout application, end-of-turn reserve deployment, and commander-defeat outcomes. A pre-existing dual-commander-defeat state is classified as a draw, but the sequential single-target fixture cannot generate mutual KO while defeated actors lose queued actions. Fifteen tests cover the current fixture contract, including a test that swaps the damage strategy without changing turn resolution and a two-turn scripted trace covering invalidation and reserve deployment. All values and unresolved semantics are explicitly marked as test assumptions; no final damage formula, type chart, RNG model, tie-break, roster interpretation, or encounter rule is selected. The current 15-test harness, injectable DamageModel seam, two-turn scenario trace, confirmed roster-document reconciliation, documentation validation, and all existing experiment suites passed all eight CI jobs in [run 41162480306](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41162480306). This verifies the exact tested commit before the status-only follow-up.
- Playtest A pipeline fixture and CLI runner added: `fixtures/creatures.json` contains five clearly labeled Pokémon scaffolds with direct base stats, 40/80/120-power moves, neutral effectiveness, and three 3v3 scenarios. `experiments/battle_sim/cli_runner.py` uses the existing `BattleResolver` and injected `DamageModel` seam; Candidate B c=100 is a replaceable test adapter only. Three battles completed with reserve deployment, full phase traces, and deterministic replay; 32 tests passed. Exact code commit `33b352cac82520f2c6bfc0a3b151ae1b815b9e90` passed all eight CI jobs in [run 41169602974](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169602974). The trace artifact is available [here](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41169363724/artifacts/13030750326). Playtest A is pipeline-only; Playtest B remains blocked on original creature design data. No formula, offset, or type chart is selected.
- Pokémon final-stage baseline data audit added under `docs/creatures/POKEMON_BASELINE_DATA_AUDIT.md`. The Gen I–IX CSV yields 546 identified final-stage entries (mean BST 509.2) and 456 after excluding sublegendary/legendary/mythical entries (mean BST 491.2); simplified Level-100 comparisons show the proposed synthetic bands are elevated relative to ordinary final-stage medians. This is research evidence only; no stat band or transformation rule selected.

## Current Experiments
- [Damage RNG Experiment](experiments/damage_rng/README.md) compares six RNG models. It does not select a final game rule.
- [Damage Equation Comparison](experiments/damage_equation/README.md) compares four base-equation families on synthetic inputs.
- [Stat-Range Sensitivity](experiments/stat_range_sensitivity/README.md) translates the team's proposed endgame bands into synthetic damage, KO-pacing, and sensitivity tests.
- [Battle Simulation Harness](experiments/battle_sim/README.md) tests deterministic turn sequencing and includes a CLI pipeline runner using a clearly labeled Pokémon scaffolding fixture. It is not a production engine or balance test.

## Canonical Project Priorities
This is the single authoritative project-wide priority list. [Open Questions](docs/OPEN_QUESTIONS.md) groups unresolved questions in this order; it does not establish a separate priority hierarchy.

1. **Damage equation design resolution.** Provisional gates and level treatment are recorded in D-022/D-023; D-024 prefers narrowing Candidate B from c=143 as a sampled starting point, with c=100 retained. D-025 resolves c=400 as failing the floored full-band gate. The corrected independent Defense sweep is 200/250/275/300/350. Playtest A pipeline validation is complete on the Pokémon scaffolding fixture; Playtest B uses original game creatures/moves to assess pacing and matchups, then compare c=100 and c=143 (c=200 only if informative). No formula or offset is selected; no Unity/C# runtime work is authorized.
2. **Battle structure and resolution.** Competitive roster accounting is confirmed in D-003: five registered monsters, select three, two active plus one reserve, with commander separate. Resolve turn phases, action economy, legal actions/targeting, priority/Speed/ties, invalidated actions, and knockout timing. The Python harness is a rules-discovery fixture, not final implementation.
3. **Replacement and victory.** Define reserve replacement choice/timing, no-reserve behavior, and victory conditions, including simultaneous defeat and encounter-specific player defeat.
4. **Stats and progression.** Define stat ownership, Level 100 normalization, allocation, and relationship-effect boundaries.
5. **Types and competitive rules.** Reconcile the type inventory and seven-village structure; then define competitive clauses and timer policy.
6. **Audit existing balance inputs.** Audit Light/Shadow stat drafts before using them as balance inputs.
7. **Story and feature scope.** Revisit broader campaign/world systems after the battle foundations are coherent.

The combined-stat experiment's interaction residual has been corrected from additive percentage subtraction to a log-space multiplicative residual, retaining exact Fraction ratios until logarithm evaluation. Regenerated artifact in [run 41165870453](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165870453) reports 120/1,320 nonzero log residuals (max 0.012399 natural-log units) and 724/1,320 nonzero floored-TTK residuals (max 2 hits). The pairwise rank audit now uses `itertools.combinations` and derives comparison counts from actual subset sizes; its 4,125 comparisons and 439 tie/order changes match the report. The damage-equation-first ordering is a project sequencing decision, not a claim that all damage details are already specified. It is recorded in [Decision D-014](docs/DECISION_LOG.md).


## 2026-10-31 Damage Design Review Update

The human review has accepted a provisional working envelope (Attack 200–400, Defense 200–350, Vitality 250–500) for formula-family comparison and provisional gates of 4–6 floored neutral hits, 1.40×–1.80× 2:1 specialization across the Defense band, no ordinary-power full-health OHKO absent an explicit mechanic, and monotonicity. Level is provisionally excluded from the base damage equation and affects derived stats/Vitality only; competitive normalization is Level 100. Candidate B c≈143 is the provisional preferred narrowing point, with c=100 retained as the stronger-specialization comparison. See D-022–D-024 in the Decision Log.

No final equation or offset is selected. The follow-up audit corrected the duplicated Defense coordinate, and the independent sweep now covers 200/250/275/300/350. c=400 remains a provisional-gate failure at 1.351× worst case. Playtest A is complete: three deterministic CLI battles passed through the existing harness and DamageModel seam, with exact replay verification and a published trace artifact. This is pipeline evidence only. Playtest B still requires original game creature designs and is the only valid source for balance conclusions.

## Not Yet Implemented
- No Unity project, scenes, or prefabs exist. A navigation-specific PathWalker.cs and ResetReloadTests.cs candidate are now stored under `prototypes/navigation/`; neither has been compiled or executed in Unity, and they depend on domain/scene types not included in this repository.
- Production battle engine, final damage resolver, or Unity/C# runtime. The Python harness is a test instrument only.
- Creature capture, progression, world traversal, puzzle, or story systems.
- Online PvP, matchmaking, or server authority.

## Engineering Direction
When engine work begins:
- Keep game rules and state in pure, testable C# where practical.
- Keep Unity scene components thin and presentation-focused.
- Prefer composition, explicit ownership, and event/interface-based communication.
- Use data-driven configuration for balance-sensitive content.
- Avoid allocations and expensive work in per-frame gameplay paths.

## Repository Notes
- Follow [COLLABORATION_PROTOCOL.md](COLLABORATION_PROTOCOL.md) for startup, authority, decision fidelity, verification, and conditional updates.
- Do not assume an installed Unity version or existing Unity project folder.
- Treat original project archives as immutable source material.
- Experimental outputs are evidence, not approved balance rules.


## 2026-10-31 Analytical Experiment Review Closure

The supplied P0/P1/P2 analytical review was checked against current main rather than the older 9100eec snapshot. The Defense coordinate list was already corrected in a newer commit; this pass moved the gate band into explicit JSON configuration and added import-time uniqueness validation. Raw Candidate A–D functions and calibration are now centralized in experiments/common/damage_candidates.py; each experiment retains its own explicit calibration anchor, and both use the same Candidate B offset sample set. The sensitivity experiment now separates isolated single-stat floored-TTK shifts from combined-versus-additive interaction residuals. The interaction field was renamed accordingly.

The Generation IX reference now spells out sequential integer floors. The claimed discrepancy was mathematically equivalent for positive integer inputs, so this was a clarity/test improvement rather than a numerical correction. Log-residual tests now encode the correct contract: zero for multiplicatively separable effects, nonzero for a non-separable interaction. Reference values and gate coordinates are in experiments/stat_range_sensitivity/config.json; root pyproject.toml and .gitignore were added.

Commit c2251a5a661c3895135389dd3f2c090086922805 passed all eight CI jobs in [run 41171803352](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41171803352). The regenerated sensitivity report contains 825 matchup rows, 2,695 combined-stat rows, 990 isolated single-stat TTK-shift rows, and 35 level rows. Isolated shift summaries and interpretation are in experiments/stat_range_sensitivity/RESULTS.md.

No damage formula, offset, RNG model, stat band, or other game rule was selected by this maintenance pass. The remaining declared POWERS dimension is still not swept by the sensitivity harness; the report treats Power 100 as its reference move power, so no full power-sensitivity claim is made.


## 2026-10-31 Navigation Prototype Artifact Update

A bounded first-playable navigation package was added under `prototypes/navigation/`. It contains the corrected six-node/four-edge `navigation.json`, `gates.json`, scene-wiring and acceptance checklist, a supplied Unity PathWalker candidate, and a scene-level reset/reload Unity test candidate. The checklist preserves the co-located floor/ladder context-switch edge case as an unresolved playtest observation; no pseudo-edge or context-switch rule was introduced.

The JSON walkthrough is a recorded manual check against the previously reviewed NavigationGraphBuilder contract, not a reproduced build: the builder source is not present in this public repository. The C# files are uncompiled and untested. A follow-up source fix now snaps PathWalker to each completed edge's destination before state advancement and before Arrived callbacks. The empty-path no-op contract is documented: the controller handles already-at-destination before calling SetPath. A Play Mode regression test is still required, including confirmation that it fails against the pre-fix implementation. Node.Facing is present in the schema but unused by the supplied walker.

This scoped prototype update does not create a Unity project, promote a game rule, or reorder canonical project priorities. The project remains in its documented engine-independent stage; navigation is a bounded, explicitly authorized parallel prototype.


## 2026-10-31 PathWalker Arrival Fix

PathWalker.cs was updated in commit `fdbae4a7f8e3e2982ff45f97e97e4bb7a96efc1f`. On every completed edge, the transform is snapped to the destination node before the traversal cursor advances. On final completion, the Arrived delegate is copied locally, the graph reference is cleared, and the callback is invoked only after the transform is at the destination. The empty-path contract is documented: an empty SetPath is a no-op; the controller owns the already-at-destination case.

The README and first-playable checklist now reflect this correction and specify a Play Mode regression test that must observe the final transform from inside Arrived and be shown to fail against the pre-fix source. The code remains uncompiled and unverified in Unity. No navigation domain files were reconstructed or added in this update.


## 2026-10-31 Repository Audit and Art Reference Structure

The seven requested art-direction category folders are now tracked under `docs/inspiration/art-direction-references/`: Character & NPC, Creature, Armor & Weapons, Environment, Lighting, VFX, and UI. Each currently contains a README with category guidance and reference-attribution fields. These are folder/index scaffolds, not populated image libraries or approved final art direction.

The audit found that the documentation validator treated percent-encoded relative Markdown destinations as literal filesystem paths. This incorrectly rejected valid links to category folders whose names contain spaces and an ampersand. `tools/validate_docs.py` now URL-decodes relative link destinations before checking them, and `tools/test_validate_docs.py` includes a regression test for the encoded Character & NPC path. The fix preserves proper URL-encoded Markdown links and does not weaken broken-link validation.

The validator change (commit `200670a0b840663449c657e1a4466e38d2f11b54`) and regression test (commit `636b986fb2386028ea6e636d5fe511ae27cbad78`) were read back from GitHub. The exact source/test commit `636b986fb2386028ea6e636d5fe511ae27cbad78` passed all eight GitHub Actions jobs in [run 41217122730](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41217122730): documentation validation, shared/stat-range sensitivity tests, damage-equation tests, battle-simulation and deterministic CLI replay, and damage RNG tests on Python 3.10–3.13.

This repository audit does not change the canonical project priority order. Playtest B remains blocked on approval of original creature stats and moves. The navigation C# candidates remain uncompiled and untested because the Unity project and frozen navigation domain source are absent.


## 2026-10-31 Original Creature Draft and Agent Workflow Baseline

A five-creature original-game roster draft is now stored in `fixtures/original_creatures_draft.json` and documented in `docs/creatures/ORIGINAL_CREATURE_ROSTER_DRAFT.md`: Thornback (physical bulwark), Zephyrkin (fast physical striker), Emberlynx (fast special attacker), Tideforged (special-defense anchor), and Gloamantis (mixed disruptor). The direct stat inputs sit inside the provisional D-022 synthetic Vitality/Attack/Defense screening envelope. Each has 40/80/120-power placeholder moves. Candidate affinity labels are identity prompts only; the type chart, STAB, resistances, immunities, and village assignments remain unresolved. This roster is provisional and requires human review; it is not balance evidence.

The CLI now labels traces using the fixture's display name rather than hardcoding Playtest A. Regression tests load the original roster fixture and run all three pipeline scenarios at Candidate B c=100 and c=143. The new `experiments/battle_sim/draft_roster_screen.py` calculates 25 neutral Power-80 single-attacker matchup rows at both offsets, reusing the existing Candidate B adapter rather than duplicating the equation. Initial mean repeated-hit-to-KO is 7.68 at c=100 and 7.76 at c=143 (range 5–12 for both); this is not match TTK, a balance verdict, or evidence to choose an offset. Tideforged has the slowest offensive screen average (8.8 hits), a role-fit signal that needs human review. Exact code/test commit `feba52e5c797d0d61ab9f87c34efabe4c0b9c8a7` passed all eight CI jobs in [run 41218300594](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41218300594), including the new original-roster pipeline smoke test and artifact publication. This verifies schema and pipeline execution only, not creature balance, TTK feel, formula selection, or type design.

A portable root `AGENTS.md` now points to the existing collaboration protocol and records the repository's actual boundaries and validation commands. A Python path-scoped instruction file lives at `.github/instructions/python.instructions.md`. The proposed provider-specific quota file, generated Copilot adapter, nested Unity instructions, skills, hooks, and instruction-budget script were not added: they are either account/client-specific, unsupported by the current repository structure, or premature. `docs/PROJECT_MANAGEMENT_AGENT_WORKFLOW_REVIEW.md` records the assessment, and `docs/IMPLEMENTATION_PLAN.md` has been reordered into current milestone gates. No game decision was added or promoted by these changes.

The latest repository HEAD at this status update, `53e1d1bbed37e0882d133799da532163d7cc87bf`, passed all eight GitHub Actions jobs in [run 41218562730](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41218562730). This exact-HEAD run includes the original creature fixture, its c=100/c=143 pipeline tests, documentation/index updates, root AGENTS.md, and Python path-scoped instructions.
