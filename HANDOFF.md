# Developer Handoff

## Project
Original creature-collecting RPG with tactical PvP ambitions. Long-term target is mobile (iOS/Android). No Unity project exists yet; current work is engine-independent design consolidation and mechanics experimentation.

## Source of Truth
1. [Project Index](PROJECT_INDEX.md)
2. [Project Status](PROJECT_STATUS.md)
3. [Game Overview](docs/GAME_OVERVIEW.md)
4. [Battle Overview](docs/battle/BATTLE_OVERVIEW.md)
5. [Battle Format Decision Framework](docs/battle/BATTLE_FORMAT_DECISION.md)
6. [Stat System Research Plan](docs/STAT_SYSTEM_RESEARCH_PLAN.md)
7. [Damage Model](docs/battle/DAMAGE_MODEL.md)
8. [Damage RNG Experiment](experiments/damage_rng/README.md)
9. [Decision Log](docs/DECISION_LOG.md)
10. [Open Questions](docs/OPEN_QUESTIONS.md)

## Completed
- Structured fragmented concepts into referenceable documents.
- Preserved contradictions and unknowns rather than inventing resolutions.
- Implemented the standalone Python damage RNG experiment with six models.
- Recorded the prior local test result: 6 tests passed.
- Added a GitHub Actions workflow to run the experiment tests on Python 3.10–3.13 and smoke-test JSON report generation. CI verified: all four Python-version jobs passed, including unit tests and JSON report generation.
- Added battle-format decision framework and stat-system research plan.

## Highest-Priority Design Decision
Separate roster size, selected monsters, active monsters, player participation, and reserve count. These are independent variables. Do not call a format "3v3" without defining what the three counts.

A useful local test candidate is player + two active monsters, with one reserve monster. This is a recommendation for a test fixture only, not a final design decision.

## Engineering Guardrails
- Keep authoritative rules in pure, testable C# where practical.
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

## Immediate Next Work
1. Get explicit agreement on the battle format variables.
2. Build a standalone stat-normalization experiment only after selecting the candidate input model.
3. Define the full damage formula and rounding checkpoints separately from the RNG model.
4. Evaluate the type chart and village structure after the type roster is fixed.
