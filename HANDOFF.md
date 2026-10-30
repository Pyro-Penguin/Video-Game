# Developer Handoff

## Project
A mobile Unity RPG for iOS and Android. Current priority is a deterministic local battle prototype, not full campaign production.

## Source of Truth
Read in this order:
1. [Project Index](PROJECT_INDEX.md)
2. [Project Status](PROJECT_STATUS.md)
3. [Battle Prototype Specification](docs/battle/BATTLE_PROTOTYPE_SPEC.md)
4. [Decision Log](docs/DECISION_LOG.md)
5. [Open Questions](docs/OPEN_QUESTIONS.md)
6. [Implementation Plan](docs/IMPLEMENTATION_PLAN.md)

## Prototype Target
Each side currently targets one commander, two active monsters, and one reserve; simultaneous turns; normalized stats; elemental types; and automatic reserve handling. The preview rule says bring five monsters and select three, but its relationship to the commander and reserve is unresolved.

## Engineering Guardrails
- Keep authoritative battle rules in pure C# where practical.
- Unity MonoBehaviours should adapt input and presentation, not own game rules.
- Prefer composition and explicit ownership.
- Communicate across boundaries through commands, events, and narrow interfaces.
- Keep balance-sensitive data outside resolver logic.
- Avoid per-frame allocations and LINQ in hot paths.
- Test match logic without loading a Unity scene.

## Do Not Assume
- Exact Unity version.
- That a complete Unity project is already present in this repository.
- That unresolved battle rules have been approved.
- That any source archive may be modified.

## Immediate Next Work
1. Confirm the Unity project baseline and inspect any supplied source archives.
2. Resolve roster accounting, commander defeat, reserve entry, and simultaneous action ordering.
3. Implement a pure C# battle simulation with unit tests only after the blocking rules are settled.
