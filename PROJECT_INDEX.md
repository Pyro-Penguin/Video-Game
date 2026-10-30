# Project Index

## Purpose
Canonical navigation for the Video Game project repository.

## Mandatory Start Here
1. [Collaboration Protocol](COLLABORATION_PROTOCOL.md) — startup sequence, authority, decision fidelity, verification, and handoff rules.
2. [Project Status](PROJECT_STATUS.md) — current stage, verified progress, and canonical project priorities.
3. [Developer Handoff](HANDOFF.md) — current work state and next action.
4. [Decision Log](docs/DECISION_LOG.md) — durable decisions and their status.
5. [Open Questions](docs/OPEN_QUESTIONS.md) — unresolved questions grouped by canonical project priority.

After these, use the task-specific references below.

## Design and Systems
- [Game Overview](docs/GAME_OVERVIEW.md) — premise, player fantasy, and current scope.
- [Design Pillars](docs/DESIGN_PILLARS.md) — provisional design principles.
- [Battle Overview](docs/battle/BATTLE_OVERVIEW.md) — battle format, timers, clauses, and conflicts.
- [Battle Format Decision Framework](docs/battle/BATTLE_FORMAT_DECISION.md) — separate roster, active field, player, and reserve decisions.
- [Battle Rules Decision Checklist](docs/battle/BATTLE_RULES_DECISION_CHECKLIST.md) — actionable blocking, important, and deferred rules decisions.
- [Damage Model](docs/battle/DAMAGE_MODEL.md) — formula fragments and unresolved mechanics.
- [Damage Equation Decision Brief](docs/battle/DAMAGE_EQUATION_DECISION_BRIEF.md)
- [Damage Equation Design Review](docs/battle/DAMAGE_EQUATION_DESIGN_REVIEW.md) — candidate equation families, mathematical checks, and experiment plan; no rule selected.
- [Damage RNG Experiment](experiments/damage_rng/README.md) — executable Python experiment and tests.
- [Damage Equation Comparison Experiment](experiments/damage_equation/README.md) — synthetic comparison of four equation families; no game rule selected.
- [Proposed Endgame Stat-Range Sensitivity Experiment](experiments/stat_range_sensitivity/README.md) — tests the team's proposed endgame stat bands against damage, KO pacing, and stat sensitivity; synthetic only.
- [Stat-Range Sensitivity Results](experiments/stat_range_sensitivity/RESULTS.md) — human-readable summary of the expanded all-vs-all, combined-stat, offset-sweep, level-treatment, and integer-floor results.
- [Stat System Research Plan](docs/STAT_SYSTEM_RESEARCH_PLAN.md) — stat ownership, normalization questions, and next experiment.
- [World and Story](docs/world/WORLD_AND_STORY.md) — narrative and setting concepts.
- [Types and Villages](docs/world/TYPES_AND_VILLAGES.md) — candidate type inventory.
- [Clans and Abilities](docs/world/CLANS_AND_ABILITIES.md) — current partial clan concepts.
- [Creature Design](docs/creatures/CREATURE_DESIGN.md) — creature and progression ideas.
- [Player Character and Classes](docs/player/PLAYER_CHARACTER_AND_CLASSES.md) — player combat role and class concepts.
- [Exploration and Capture](docs/world/EXPLORATION_AND_CAPTURE.md) — Portal Gauntlet, traversal, puzzles, and capture ideas.
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) — milestones and exit criteria.

## Documentation Rules
1. Treat this repository as the shared, durable project memory; conversations are temporary workspaces.
2. Follow [COLLABORATION_PROTOCOL.md](COLLABORATION_PROTOCOL.md) for authority, status labels, verification, and update rules.
3. Use only **Confirmed**, **Provisional**, **Unresolved**, or **Superseded** for decision status.
4. Do not silently convert brainstorming or experimental results into confirmed requirements.
5. Keep implementation status evidence-based: distinguish committed, verified, tested, and human-accepted work.
6. Keep experimental code/results separate from approved game rules.
7. Preserve original archives as immutable reference material.

## Repository Areas
- `docs/battle/` — battle rules and mechanics.
- `docs/world/` — story, villages, types, clans, and abilities.
- `docs/creatures/` — creature concepts and stat records.
- `docs/inspiration/` — visual, audio, and gameplay references.
- `experiments/` — isolated executable mechanics investigations.
- `tools/` — standard-library documentation validator and its tests.
- `.github/workflows/` — automated validation for Python experiments and project documentation.
- A Unity `Assets/`, `Packages/`, and `ProjectSettings/` structure will be added only after an engine project is deliberately created.
