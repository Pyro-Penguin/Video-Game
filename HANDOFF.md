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
**Stage 1 governance changes:** committed and read back from GitHub (Verified); human review/acceptance remains pending. **Stage 2 validator:** committed, read back, and tested successfully in GitHub Actions run [41085210865](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41085210865).

**Stat-range experiment:** the initial implementation and JSON report passed all seven jobs in [CI run 41089058406](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41089058406). The artifact `stat-range-sensitivity-report` was published and retrieved. A follow-up adds per-hit integer flooring and a test; its CI run is currently pending. The human-readable initial summary is [RESULTS.md](experiments/stat_range_sensitivity/RESULTS.md). Do not mark the flooring extension Tested until its own CI run passes.

## Active Review Package
Team proposal is represented only as synthetic test ranges:
- Attack / Special Attack: 200–400.
- Defense / Special Defense: 200–350.
- Vitality / HP: 250–500.
- Speed: 100–400 (not included in damage experiment).
- Levels: 1, 25, 50, 100.
- Move powers: 40, 80, 100, 120, 160.
- Vitality points: 250, 350, 500.
- Five paired test profiles: Balanced 300/275; Offensive 400/250; Defensive 250/350; High-pressure 400/200; Low-pressure 200/350.

The initial comparison is calibrated at Level 50. Team feedback is split on Level 50 vs Level 100 normalization and direct vs derived-stat-only story level scaling; both remain unresolved. The team broadly supports 3–6 neutral hits, moderate specialization, and treating the bands as test envelopes only. These are review preferences, not accepted decisions.

## Highest-Priority Next Work
1. Confirm the integer-floor extension CI run is green; inspect the updated artifact and update RESULTS.md so its evidence points to the same green commit.
2. Extend the experiment with (a) an all-vs-all attacker/defender archetype matrix and (b) combined-stat perturbations. Current profiles pair Attack and Defense and do not test every attacker against every defender.
3. Use the screening criteria in [Damage Equation Decision Brief](docs/battle/DAMAGE_EQUATION_DECISION_BRIEF.md): calibration parity, named neutral TTK reference, no accidental ordinary-power one-hit KO, agreed 2:1 specialization envelope, sensitivity/monotonicity, integer behavior, and reproducibility.
4. Collect binding preferences only after the extended report and human-readable summary are validated. Keep responses as proposals until the human explicitly accepts them; do not add Decision Log entries without that acceptance.
5. Keep the battle-structure track alive in parallel. Damage-equation work must not silently replace the unresolved active/reserve, commander, simultaneous-selection, and turn-resolution decisions.

No formula, normalization level, stat range, level-scaling policy, TTK rule, or RNG model has been selected.

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
