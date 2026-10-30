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
**Stage 1 governance changes:** committed and read back from GitHub (Verified); human review/acceptance remains pending. **Stage 2 validator:** committed, read back, and tested successfully in GitHub Actions run [41085210865](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41085210865). The documentation validator, malformed-document tests, four Python-version experiment jobs, and RNG report smoke tests passed.

## Highest-Priority Next Work
1. Review and accept or amend the collaboration protocol and Stage 1/Stage 2 governance changes.
2. Review the synthetic comparison report from [Damage Equation Comparison Experiment](experiments/damage_equation/README.md) after its CI run completes. Evaluate sensitivity across both synthetic scales, especially direct ratio versus offset ratio and direct-level versus derived-stat level treatment.
3. Use the measured tradeoffs to narrow the design choices, then request human approval for any actual damage equation, stat scale, or RNG decision. Do not select a formula or RNG model automatically.
3. Only after the damage-equation work is sufficiently specified, return to battle structure and turn-resolution decisions.

Do not begin Unity implementation or select a final RNG model without explicit approval.

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
