# Project Index

## Purpose
Canonical navigation for the Video Game project repository.

## Start Here
- [Project Status](PROJECT_STATUS.md) — current stage and verified progress.
- [Game Overview](docs/GAME_OVERVIEW.md) — premise, player fantasy, and current scope.
- [Design Pillars](docs/DESIGN_PILLARS.md) — provisional design principles.
- [Battle Overview](docs/battle/BATTLE_OVERVIEW.md) — battle format, timers, clauses, and conflicts.
- [Battle Format Decision Framework](docs/battle/BATTLE_FORMAT_DECISION.md) — separate roster, active field, player, and reserve decisions.
- [Damage Model](docs/battle/DAMAGE_MODEL.md) — formula fragments and unresolved mechanics.
- [Damage RNG Experiment](experiments/damage_rng/README.md) — executable Python experiment and tests.
- [Stat System Research Plan](docs/STAT_SYSTEM_RESEARCH_PLAN.md) — stat ownership, normalization questions, and next experiment.
- [World and Story](docs/world/WORLD_AND_STORY.md) — narrative and setting concepts.
- [Types and Villages](docs/world/TYPES_AND_VILLAGES.md) — candidate type inventory.
- [Clans and Abilities](docs/world/CLANS_AND_ABILITIES.md) — current partial clan concepts.
- [Creature Design](docs/creatures/CREATURE_DESIGN.md) — creature and progression ideas.
- [Player Character and Classes](docs/player/PLAYER_CHARACTER_AND_CLASSES.md) — player combat role and class concepts.
- [Exploration and Capture](docs/world/EXPLORATION_AND_CAPTURE.md) — Portal Gauntlet, traversal, puzzles, and capture ideas.
- [Decision Log](docs/DECISION_LOG.md) — confirmed, provisional, and unresolved decisions.
- [Open Questions](docs/OPEN_QUESTIONS.md) — design and technical blockers.
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) — milestones and exit criteria.
- [Developer Handoff](HANDOFF.md) — concise context for continuing work.

## Documentation Rules
1. Treat this repository as the project source of truth.
2. Label decisions as **confirmed**, **provisional**, or **unresolved**.
3. Do not silently convert brainstorms into confirmed requirements.
4. Update the relevant specification and decision log when a rule changes.
5. Preserve original archives as immutable reference material.
6. Keep implementation status evidence-based: distinguish designed, implemented, and tested.
7. Keep experimental code/results separate from approved game rules.

## Repository Areas
- `docs/battle/` — battle rules and mechanics.
- `docs/world/` — story, villages, types, clans, and abilities.
- `docs/creatures/` — creature concepts and stat records.
- `docs/inspiration/` — visual, audio, and gameplay references.
- `experiments/` — isolated executable mechanics investigations.
- `.github/workflows/` — automated validation for Python experiments.
- A Unity `Assets/`, `Packages/`, and `ProjectSettings/` structure will be added only after an engine project is deliberately created.
