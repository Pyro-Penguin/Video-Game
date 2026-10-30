# Project Status

## Project
Original creature-collecting RPG with tactical PvP ambitions. The long-term target platform is mobile (iOS/Android), but no Unity project or engine implementation exists yet.

## Current Stage
**Design consolidation and standalone mechanics experimentation.** The repository is intentionally engine-independent at this stage.

## Verified Progress
- Repository documentation foundation created.
- High-level game premise, design pillars, world/story concepts, type/village inventory, creature concepts, and inspiration references documented.
- Battle-format conflicts and unresolved timer/roster rules recorded rather than silently reconciled.
- Standalone Python damage RNG experiment implemented.
- Exact single-hit KO checks match the required probabilities.
- Automated test suite executed locally: 6 tests passed.
- Seeded JSON experiment report generated and committed.

## Current Experiment
See [Damage RNG Experiment](experiments/damage_rng/README.md). It compares six RNG models and does not select a final game rule.

## Current Design Priorities
1. Resolve the battle party/field format, especially player character versus monster counts.
2. Define commander/player defeat and reserve deployment.
3. Clarify timer interaction and competitive clauses.
4. Define the full damage formula separately from the isolated RNG experiment.
5. Reconcile the type inventory and seven-village structure.
6. Audit Light/Shadow stat drafts before using them as balance inputs.

## Not Yet Implemented
- Unity project, scenes, prefabs, or C# game systems.
- Battle simulation or damage engine for the game.
- Creature capture, progression, world traversal, puzzle, or story systems.
- Online PvP, matchmaking, or server authority.

## Engineering Direction
When engine work begins:
- Keep game rules and state in pure, testable C# where practical.
- Keep Unity scene components thin and presentation-focused.
- Prefer composition, explicit ownership, and event/interface-based communication.
- Use data-driven configuration for balance-sensitive content.
- Avoid allocations and expensive work in per-frame gameplay paths.

## Repository Notes
- Do not assume an installed Unity version or existing Unity project folder.
- Treat original project archives as immutable source material.
- Experimental outputs are evidence, not approved balance rules.
