# Developer Handoff

## Project
Original creature-collecting RPG with tactical PvP ambitions. Long-term target platform is mobile (iOS/Android). No Unity project exists yet; current work is engine-independent design consolidation and mechanics experimentation.

## Mandatory Startup
Read [COLLABORATION_PROTOCOL.md](COLLABORATION_PROTOCOL.md) first, then follow its startup sequence. The repository is the shared project memory; conversations are temporary workspaces.

## Source of Truth
- [Project Index](PROJECT_INDEX.md)
- [Project Status](PROJECT_STATUS.md) — canonical project-wide priorities.
- [Decision Log](docs/DECISION_LOG.md) — authoritative durable decisions.
- [Open Questions](docs/OPEN_QUESTIONS.md) — unresolved questions grouped by canonical priority.
- [Game Overview](docs/GAME_OVERVIEW.md)
- [Battle Overview](docs/battle/BATTLE_OVERVIEW.md)
- [Battle Format Decision Framework](docs/battle/BATTLE_FORMAT_DECISION.md)
- [Stat System Research Plan](docs/STAT_SYSTEM_RESEARCH_PLAN.md)
- [Damage Model](docs/battle/DAMAGE_MODEL.md)
- [Damage Equation Decision Brief](docs/battle/DAMAGE_EQUATION_DECISION_BRIEF.md)
- [Damage Equation Comparison Experiment](experiments/damage_equation/README.md)
- [Proposed Endgame Stat-Range Sensitivity Experiment](experiments/stat_range_sensitivity/README.md)
- [Stat-Range Sensitivity Results](experiments/stat_range_sensitivity/RESULTS.md)
- [Damage RNG Experiment](experiments/damage_rng/README.md)

## Completed
- Structured fragmented concepts into referenceable documents.
- Preserved contradictions and unknowns rather than inventing resolutions.
- Implemented the standalone Python damage RNG experiment with six models.
- Recorded the prior local test result: 6 tests passed.
- Added a GitHub Actions workflow to run the experiment tests on Python 3.10–3.13 and smoke-test JSON report generation. CI verified: all four Python-version jobs passed, including unit tests and JSON report generation.
- Added battle-format decision framework and stat-system research plan.
- Added collaboration protocol and reconciled the canonical priority order; see D-014.

## Current Work State

**Expanded damage experiment:** CI run [41094836607](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41094836607) passed all seven jobs. Its artifact was downloaded and inspected: 825 all-vs-all rows, 2,695 single/combined-stat rows, 35 level rows, and 4,125 raw/floored pairwise candidate comparisons. [RESULTS.md](experiments/stat_range_sensitivity/RESULTS.md) was updated from this artifact. Subsequent documentation, status, and index updates passed all seven jobs in [41095218936](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41095218936).

**Verification before this handoff edit:** CI run 41095218936 tested commit `254fc50719c11d82e137ff38a68a278547b9266a` and passed all seven jobs. This handoff edit triggers a new run; check that run before describing this handoff as Tested.

## Expanded experiment findings

- The Level-100 comparison uses a shared 60-damage calibration at Power 100 / Attack 300 / Defense 275. The first 50-damage anchor yielded 7 hits against Vitality 350 and conflicted with the provisional 4–6 target.
- Candidate B offsets c=100, 143, 200, and 400 pass the current provisional neutral TTK, 2:1 specialization, and no-full-HP-one-hit numeric gates. No offset is selected.
- c=143 preserves c=100's floored matchup ordering most closely among tested alternatives (1.62% of matchup-pair orderings change); c=400 compresses more but changes ordering more (17.19%).
- Flooring changed 439/4,125 pairwise candidate relations, all by creating/removing ties; there were zero strict order reversals in this Level-100 matrix.
- Direct level scaling causes severe low-level TTK when endgame derived stats are held constant. This isolates direct level dependence; it is not a story stat-growth model.
- The Generation IX deterministic base-damage implementation is a reference harness only, not a fifth candidate; external modifiers are excluded.
- Provisional preferences and gates live in the Damage Equation Decision Brief. They are not game rules or Decision Log entries.

## Highest-Priority Next Work
1. Review the expanded results against the provisional gates; accept or revise the neutral reference, 4–6 floored TTK target, 1.4×–1.8× specialization envelope, and candidate-screening rules.
2. If gates are accepted, decide whether a second sensitivity pass across a wider stat scale / progression-derived stats is needed before narrowing B offsets or pruning A–D. Do not select c=143 or any formula from this synthetic grid alone.
3. Keep battle structure/resolution alive as the next project priority after damage-equation resolution. This experiment does not decide active/reserve, commander, simultaneous-selection, or turn-resolution rules.
4. Do not create game-rule Decision Log entries until the human explicitly accepts the decisions.

No final damage formula, stat range, story-level scaling policy, TTK rule, or RNG model has been selected.

## Engineering Guardrails
- Keep authoritative rules in pure, testable C# where practical once engine implementation is authorized.
- Unity components adapt input and presentation; they do not own core rules.
- Prefer composition and explicit ownership.
- Communicate across boundaries through commands, events, and narrow interfaces.
- Keep balance-sensitive data outside resolver logic.
- Avoid per-frame allocations and LINQ in hot paths.
- Test match logic without loading a Unity scene.

## Do Not Assume
- Exact Unity version or that Unity has been installed.
- That a complete Unity project exists.
- That unresolved battle rules have been approved.
- That any source archive may be modified.
- That the RNG experiment selects a final damage model.
