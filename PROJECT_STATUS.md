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
- Human-readable [Stat-Range Sensitivity Results](experiments/stat_range_sensitivity/RESULTS.md), screening criteria, and grouped review questions added. No formula, normalization level, stat band, or TTK rule has been selected.

## Current Experiments
- [Damage RNG Experiment](experiments/damage_rng/README.md) compares six RNG models. It does not select a final game rule.
- [Damage Equation Comparison](experiments/damage_equation/README.md) compares four base-equation families on synthetic inputs.
- [Stat-Range Sensitivity](experiments/stat_range_sensitivity/README.md) translates the team's proposed endgame bands into synthetic damage, KO-pacing, and sensitivity tests.

## Canonical Project Priorities
This is the single authoritative project-wide priority list. [Open Questions](docs/OPEN_QUESTIONS.md) groups unresolved questions in this order; it does not establish a separate priority hierarchy.

1. **Damage equation design resolution.** Define the deterministic damage pipeline, stat inputs, modifier order, immunity, and rounding boundaries. Treat RNG distribution/placement as a separate decision. This is the immediate prerequisite before expanding turn queues or state loops; it does not authorize selecting a final RNG model.
2. **Battle structure and resolution.** Resolve side composition, roster/selection/active/reserve counts, player role, turn phases, action economy, targeting, priority/speed/ties, invalidated actions, and knockout timing.
3. **Replacement and victory.** Define replacement timing and victory conditions, including simultaneous defeat and encounter-specific player defeat.
4. **Stats and progression.** Define stat ownership, Level 100 normalization, allocation, and relationship-effect boundaries.
5. **Types and competitive rules.** Reconcile the type inventory and seven-village structure; then define competitive clauses and timer policy.
6. **Audit existing balance inputs.** Audit Light/Shadow stat drafts before using them as balance inputs.
7. **Story and feature scope.** Revisit broader campaign/world systems after the battle foundations are coherent.

The damage-equation-first ordering is a project sequencing decision, not a claim that all damage details are already specified. It is recorded in [Decision D-014](docs/DECISION_LOG.md).

## Not Yet Implemented
- Unity project, scenes, prefabs, or C# game systems.
- Battle simulation or damage engine for the game.
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
