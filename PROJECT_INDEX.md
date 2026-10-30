# Project Index

## Purpose
Canonical navigation for the Video Game project repository.

## Start Here
- [Project Status](PROJECT_STATUS.md) — current stage, prototype scope, and engineering constraints.
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) — ordered work toward the first playable local battle.
- [Battle Prototype Specification](docs/battle/BATTLE_PROTOTYPE_SPEC.md) — current battle-mode scope and explicitly unresolved rules.
- [Decision Log](docs/DECISION_LOG.md) — decisions, provisional choices, and rationale.
- [Open Questions](docs/OPEN_QUESTIONS.md) — decisions required before implementation can be considered stable.
- [AI / Developer Handoff](HANDOFF.md) — concise context for continuing work.

## Documentation Rules
1. Treat this repository as the project source of truth.
2. Label decisions as **confirmed**, **provisional**, or **unresolved**.
3. Do not silently convert brainstorms into confirmed requirements.
4. Update the relevant specification and decision log when a rule changes.
5. Preserve original archives as immutable reference material.
6. Keep implementation status evidence-based: distinguish designed, implemented, and tested.

## Planned Areas
- `docs/battle/` — battle rules, state model, turn resolution, and balance.
- `docs/architecture/` — ownership, lifetimes, boundaries, and communication contracts.
- `Assets/` and `Packages/` — Unity project content, once the actual Unity project and editor version are confirmed.
