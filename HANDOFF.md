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

**Stat-range experiment:** the initial implementation passed all seven jobs in [CI run 41089058406](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41089058406). The flooring-enhanced implementation and report passed all seven jobs in [CI run 41090778744](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41090778744). Its artifact was downloaded and inspected: 1,200 damage/KO rows, 120 sensitivity rows, 80 level rows; per-hit integer flooring changes KO count in 247/1,200 rows. See the human-readable [RESULTS.md](experiments/stat_range_sensitivity/RESULTS.md).

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

The initial candidate calibration anchor remains Level 50. The current human review has expressed these **Provisional preferences**: competitive normalization Level 100; neutral reference = Balanced 300 Attack / 275 Defense, Vitality 350, Power 100; neutral target = 4–6 hits; and Pokémon-style damage calculation as the specialization-response reference rather than an arbitrary 1.5×–1.7× cap. These are working directions, not accepted game rules. Story-level treatment remains open; default test bias is level → derived stats → damage, with direct level scaling retained as a comparison. Five profiles remain test coordinates only.

Flooring audit of the CI JSON is now documented in RESULTS.md: the 247 changed rows distribute A=40, B=48, C=91, D=68; 60 rows change by more than one hit, all in Candidate C. Aggregate mean-TTK ranking remains B, D, A, C, but individual pairwise ordering changes in some scenario coordinates. Floored outcomes must govern future pass/fail checks.

## Highest-Priority Next Work
1. Extend the experiment with the all-vs-all attacker/defender matrix and combined-stat perturbations; include matched Level-100 calibration, raw and floored outputs, and a Pokémon-style cartridge reference calculation.
2. Re-evaluate the provisional Balanced/Vitality-350/Power-100 neutral reference and 4–6 TTK target, plus the measured 2:1 specialization response, against that expanded matrix. Any ±1-hit tolerance must apply to floored results.
3. Parameterize Candidate B's offset rather than treating c=100 as scale-independent. Do not prune candidates until the expanded results are reviewed against pre-stated gates.
4. Keep the battle-structure track alive in parallel. Damage-equation work must not silently replace unresolved active/reserve, commander, simultaneous-selection, and turn-resolution decisions.
5. Do not add Decision Log entries until the human explicitly accepts the resulting decisions.

No final formula, stat range, story-level scaling policy, TTK rule, or RNG model has been selected. Level 100 and Pokémon-style calculation are provisional human preferences only.

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
