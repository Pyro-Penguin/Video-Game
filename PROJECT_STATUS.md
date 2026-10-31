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
- Prior local test run recorded: 6 tests passed.
- GitHub Actions workflow executed successfully on Python 3.10, 3.11, 3.12, and 3.13; automated tests and JSON report smoke test passed in all four jobs.
- Collaboration protocol and Stage 1 governance changes committed and read back from GitHub; human review/acceptance is pending.
- Stage 2 documentation validator, malformed-document tests, and CI integration committed. GitHub Actions run 41085210865 passed the documentation job, all four Python-version experiment jobs, and the damage RNG report smoke tests.
- Damage Equation Decision Brief added; it compares candidate equation families without selecting a formula or changing game rules.
- Synthetic damage-equation comparison experiment and six automated tests added. GitHub Actions run 41086133510 passed the equation tests and report-generation smoke test, the documentation checks, and the existing four-version damage RNG matrix.
- Team-proposal stat-range sensitivity experiment added under `experiments/stat_range_sensitivity/`; five synthetic paired Attack/Defense profiles, four equation candidates, four levels, five move powers, three Vitality points, KO thresholds, and one-stat sensitivity are covered. Initial CI run [41089058406](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41089058406) passed all seven jobs. Flooring-enhanced CI run [41090778744](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41090778744) also passed all seven jobs and published the updated JSON artifact: 1,200 damage/KO rows, 120 sensitivity rows, 80 level rows; integer flooring changes KO count in 247/1,200 rows.
- Human-readable [Stat-Range Sensitivity Results](experiments/stat_range_sensitivity/RESULTS.md), numeric screening gates, and sequenced review questions added. Flooring audit of the CI JSON found the 247 changed rows distributed A=40, B=48, C=91, D=68; 60 rows change by more than one hit, all in Candidate C. Aggregate mean-TTK order is unchanged (B, D, A, C), but individual pairwise ordering changes in some scenario coordinates. Future pass/fail checks must use floored results.
- Expanded all-vs-all / combined-stat damage experiment added. Historical CI run [41094836607](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41094836607) passed all seven jobs; its artifact contained 825 matchup rows, 2,695 single/combined-stat rows, 35 level rows, and 4,125 raw/floored pairwise comparisons. The shared Level-100 calibration is 60 damage at the named Vitality-350 reference. A subsequent code review found that the specialization gate was evaluated at only one Defense coordinate; that result is superseded. The gate is now corrected to sweep all five pre-registered defender profiles, gate on both worst-case ratio bounds, and regression-test Candidate B c=400 failing at Defense 200 (4/3). Source, tests, README, and RESULTS were updated. Corrected code/test commit `e2201bc831b38a6d2ee175c934461aad7299ff05` passed all seven CI jobs in [run 41160522573](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41160522573), including the stat-range unit tests and JSON report smoke test. The subsequent c=400 audit found that the implementation swept the registered Defense band but compared raw ratios, while D-022 requires floored damage ratios. D-025 records c=400 failing at a floored worst case of 1.351× (Defense 200). The gate, regression test, results table, and review were corrected. Code/test commit 7bc26a67e2d5bb64ac89678198ee78cd582079ca passed all eight CI jobs in [run 41167917475](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41167917475). No formula or offset selected.
- Handoff verification freshness rule recorded as D-015; protocol and decision log now agree.
- Battle-rule decisions D-019 through D-021 now record the user's revised exact-Speed-tie hierarchy, end-of-turn reserve policy (automatic with one legal reserve; player choice with multiple), and encounter-specific victory policies. The D-021 exact-Speed-tie comparator is implemented with exact Fraction effectiveness comparison, integer HP-percentage comparison, and fixture-only unit-ID fallback; the corrected commit passed all eight CI jobs in [run 41165107246](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165107246). D-019 multi-reserve selection is implemented through an injected pure selector and caller-supplied selection IDs, with validation and regression tests; the implementation commit passed CI in [run 41165240887](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165240887). D-020 now derives immutable battle facts and injects a pure victory policy; commander-defeat, monster-team-wipe, and combined OR-condition configurations are tested. D-020 passed CI in [run 41165443061](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165443061). Explicit `PhaseStarted`/`PhaseCompleted` markers for action resolution, end-of-turn replacement, and victory check are now implemented and regression-tested; this latest phase-marker commit is awaiting CI. Multi-target commands now support explicit target lists, per-target revalidation, skipping defeated targets while continuing to later targets, and duplicate-target validation. Regression tests cover these cases. Additional D-020 policy tests now cover mixed-condition mutual elimination and disabled terminal flags; latest code and documentation commits are awaiting CI.
- A bounded pure-Python battle simulation harness was added under `experiments/battle_sim/`. It implements immutable battle snapshots, complete command validation, simultaneous command locking, priority/Speed ordering, deterministic fixture tie-breaking, invalidated-action handling, knockout application, end-of-turn reserve deployment, and commander-defeat outcomes. A pre-existing dual-commander-defeat state is classified as a draw, but the sequential single-target fixture cannot generate mutual KO while defeated actors lose queued actions. Fifteen tests cover the current fixture contract, including a test that swaps the damage strategy without changing turn resolution and a two-turn scripted trace covering invalidation and reserve deployment. All values and unresolved semantics are explicitly marked as test assumptions; no final damage formula, type chart, RNG model, tie-break, roster interpretation, or encounter rule is selected. The current 15-test harness, injectable DamageModel seam, two-turn scenario trace, confirmed roster-document reconciliation, documentation validation, and all existing experiment suites passed all eight CI jobs in [run 41162480306](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41162480306). This verifies the exact tested commit before the status-only follow-up.
- Pokémon final-stage baseline data audit added under `docs/creatures/POKEMON_BASELINE_DATA_AUDIT.md`. The Gen I–IX CSV yields 546 identified final-stage entries (mean BST 509.2) and 456 after excluding sublegendary/legendary/mythical entries (mean BST 491.2); simplified Level-100 comparisons show the proposed synthetic bands are elevated relative to ordinary final-stage medians. This is research evidence only; no stat band or transformation rule selected.

## Current Experiments
- [Damage RNG Experiment](experiments/damage_rng/README.md) compares six RNG models. It does not select a final game rule.
- [Damage Equation Comparison](experiments/damage_equation/README.md) compares four base-equation families on synthetic inputs.
- [Stat-Range Sensitivity](experiments/stat_range_sensitivity/README.md) translates the team's proposed endgame bands into synthetic damage, KO-pacing, and sensitivity tests.
- [Battle Simulation Harness](experiments/battle_sim/README.md) tests deterministic turn sequencing with synthetic fixed-damage fixtures; it is not a production engine or approved ruleset.

## Canonical Project Priorities
This is the single authoritative project-wide priority list. [Open Questions](docs/OPEN_QUESTIONS.md) groups unresolved questions in this order; it does not establish a separate priority hierarchy.

1. **Damage equation design resolution.** Provisional gates and level treatment are recorded in D-022/D-023; D-024 prefers narrowing Candidate B around c=143 with c=100 retained. D-025 resolves the c=400 audit: it fails the floored full-band specialization gate. The narrow comparison is c=100 and c=143, with c=200 only if a softer point is still informative. The next evidence dependency is 3–5 actual creature stat spreads and 2–3 moves each, followed by a text-only CLI playtest using the existing pure-Python harness. No Unity/C# runtime work is authorized.
2. **Battle structure and resolution.** Competitive roster accounting is confirmed in D-003: five registered monsters, select three, two active plus one reserve, with commander separate. Resolve turn phases, action economy, legal actions/targeting, priority/Speed/ties, invalidated actions, and knockout timing. The Python harness is a rules-discovery fixture, not final implementation.
3. **Replacement and victory.** Define reserve replacement choice/timing, no-reserve behavior, and victory conditions, including simultaneous defeat and encounter-specific player defeat.
4. **Stats and progression.** Define stat ownership, Level 100 normalization, allocation, and relationship-effect boundaries.
5. **Types and competitive rules.** Reconcile the type inventory and seven-village structure; then define competitive clauses and timer policy.
6. **Audit existing balance inputs.** Audit Light/Shadow stat drafts before using them as balance inputs.
7. **Story and feature scope.** Revisit broader campaign/world systems after the battle foundations are coherent.

The combined-stat experiment's interaction residual has been corrected from additive percentage subtraction to a log-space multiplicative residual, retaining exact Fraction ratios until logarithm evaluation. Regenerated artifact in [run 41165870453](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41165870453) reports 120/1,320 nonzero log residuals (max 0.012399 natural-log units) and 724/1,320 nonzero floored-TTK residuals (max 2 hits). The pairwise rank audit now uses `itertools.combinations` and derives comparison counts from actual subset sizes; its 4,125 comparisons and 439 tie/order changes match the report. The damage-equation-first ordering is a project sequencing decision, not a claim that all damage details are already specified. It is recorded in [Decision D-014](docs/DECISION_LOG.md).


## 2026-10-31 Damage Design Review Update

The human review has accepted a provisional working envelope (Attack 200–400, Defense 200–350, Vitality 250–500) for formula-family comparison and provisional gates of 4–6 floored neutral hits, 1.40×–1.80× 2:1 specialization across the Defense band, no ordinary-power full-health OHKO absent an explicit mechanic, and monotonicity. Level is provisionally excluded from the base damage equation and affects derived stats/Vitality only; competitive normalization is Level 100. Candidate B c≈143 is the provisional preferred narrowing point, with c=100 retained as the stronger-specialization comparison. See D-022–D-024 in the Decision Log.

No final equation or offset is selected. D-025 reconciles c=400: the published 1.429× value was not the worst-case band result, and the corrected floored ratio at Defense 200 is 1.351×, below the provisional 1.40× minimum. The corrected code and tests passed exact-commit CI run 41167917475. The next dependency is actual creature stat/move data; the repository has no validated five-creature roster, and the Light/Shadow stat draft remains unverified and inconsistent. The CLI slice must wait for those real inputs. These are provisional design gates, not final balance conclusions.

## Not Yet Implemented
- Unity project, scenes, prefabs, or C# game systems.
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
