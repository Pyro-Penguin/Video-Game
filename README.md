# Video Game

Original creature-collecting RPG with tactical PvP ambitions. This repository is the shared design, documentation, and mechanics-validation workspace for a mobile iOS/Android game. It does **not** yet contain a Unity project or production engine runtime.

## Start Here
- [Project Index](PROJECT_INDEX.md)
- [Project Status](PROJECT_STATUS.md)
- [Developer Handoff](HANDOFF.md)
- [Game Overview](docs/GAME_OVERVIEW.md)
- [Design Pillars](docs/DESIGN_PILLARS.md)
- [Battle Overview](docs/battle/BATTLE_OVERVIEW.md)
- [Decision Log](docs/DECISION_LOG.md)
- [Open Questions](docs/OPEN_QUESTIONS.md)

## Executable Experiments

All experiments are engine-independent Python tools. Their fixtures and results support investigation; they do not automatically become approved game rules.

- [Damage RNG](experiments/damage_rng/README.md) — compare six random-damage models with seeded simulation and exact single-hit KO enumeration.
- [Damage Equation Comparison](experiments/damage_equation/README.md) — compare four synthetic base-equation families.
- [Stat-Range Sensitivity](experiments/stat_range_sensitivity/README.md) — examine synthetic stat profiles, integer-floored damage, KO pacing, and sensitivity.
- [Battle Simulation Harness](experiments/battle_sim/README.md) — deterministic turn-resolution and CLI pipeline fixture with injectable damage-model seam; not a production battle engine or balance test.

Run the relevant experiment's documented unittest command from its directory. The repository's GitHub Actions workflow validates these experiments and project documentation.

## Bounded Prototype Artifacts

[Navigation First Playable](prototypes/navigation/README.md) contains a hand-authored graph/gate fixture, Unity-side candidate scripts, and an acceptance checklist. The scripts are not compiled or playtested; the navigation domain source and Unity project are not present.

## Project Principle

Ideas, experiments, provisional decisions, and confirmed rules remain distinct. Experimental results do not become game rules without explicit human acceptance.
