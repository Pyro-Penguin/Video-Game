# Developer Handoff

## Project
Original creature-collecting RPG with tactical PvP ambitions. Long-term target is mobile (iOS/Android). No Unity project exists yet; current work is engine-independent design consolidation and mechanics experimentation.

## Source of Truth
Read:
1. [Project Index](PROJECT_INDEX.md)
2. [Project Status](PROJECT_STATUS.md)
3. [Game Overview](docs/GAME_OVERVIEW.md)
4. [Design Pillars](docs/DESIGN_PILLARS.md)
5. [Battle Overview](docs/battle/BATTLE_OVERVIEW.md)
6. [Damage Model](docs/battle/DAMAGE_MODEL.md)
7. [Damage RNG Experiment](experiments/damage_rng/README.md)
8. [Decision Log](docs/DECISION_LOG.md)
9. [Open Questions](docs/OPEN_QUESTIONS.md)

## Completed
- Structured the supplied fragmented concepts into referenceable design documents.
- Recorded contradictions and unknowns rather than inventing resolutions.
- Implemented the standalone Python damage RNG experiment with six models.
- Verified the six required exact KO probability rows.
- Ran the automated suite locally: 6 tests passed.
- Generated a seeded JSON report (100,000 trials per model per target; seed 20261030).

## Important Battle Ambiguity
The notes variously describe 2v2, player + three monsters, bring five/select three, 3v3, and commander + two active monsters + one reserve. Do not assume these mean the same thing. Define party size, active field size, and reserve count independently.

## Engineering Guardrails
When engine implementation begins:
- Keep authoritative rules in pure C# where practical.
- Unity components adapt input and presentation; they do not own core rules.
- Prefer composition and explicit ownership.
- Communicate across boundaries through commands, events, and narrow interfaces.
- Keep balance-sensitive data outside resolver logic.
- Avoid per-frame allocations and LINQ in hot paths.
- Test match logic without loading a Unity scene.

## Do Not Assume
- Exact Unity version or even that Unity has been installed.
- That a complete Unity project is already present.
- That unresolved battle rules have been approved.
- That any source archive may be modified.
- That the RNG experiment selects a final damage model.

## Immediate Next Work
1. Continue capturing fragmented notes into topic documents without converting ideas into decisions.
2. Resolve battle party/field composition and commander defeat.
3. Specify full damage formula and type chart independently from the RNG experiment.
4. Decide whether the next experiment should investigate stat normalization, type-chart balance, or simultaneous turn resolution.
