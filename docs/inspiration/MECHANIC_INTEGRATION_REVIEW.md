# Mechanic Integration Review

**Status:** Reference analysis only. Nothing here is an approved gameplay rule or implementation commitment.

## Purpose and evidence boundary

This document consolidates the supplied mechanic reports into reusable design and architecture patterns. The reports were supplied as research summaries; their implementation details, repository claims, dates, and license interpretations have not been independently source-audited. Treat them as leads, not authoritative technical documentation. Do not copy source code or assets without a separate provenance and license review.

## Cross-reference synthesis

| Reference | Transferable pattern | Best-fit project use | Priority / boundary |
|---|---|---|---|
| Unciv | Data-driven rules/uniques, leader traits, short policy trees, settlement yields, derived diplomacy | Lightweight seven-village layer; leader, clan, building, and policy modifiers | High later; not a full 4X |
| OpenRCT2 | Goal-oriented agents, role-specific behavior, bounded pathfinding, scheduled AI budgets, transient thoughts | Ambient NPCs, specialists, roaming creatures | Deferred until battle core; not every resident needs a full agent |
| A Dark Room | Aggregate population/jobs/yields, slow production ticks, resource chains, soft unlocks | Background population and village growth | High later; anonymous residents remain aggregate |
| Monument Valley | Configuration-dependent navigation graph, discrete puzzle states, environmental teaching, guaranteed solvability | Portal Gauntlet, shrines, companion-operated mechanisms | Strong fit for short authored puzzle spaces; defer full-world geometry |
| Customization research | Layered asset composition, typed numeric build data, artist-authored morph extremes, modular creature parts | Player appearance, equipment, dyes, creature variants/fusion | Data schema and art-pipeline decisions before content production |
| Disco Elysium | Build-dependent internal voices, micro-reactivity, meaningful failure, ideology as a costly stateful build | Dialogue/character identity, thought-like traits, narrative checks | High creative value; substantial writing cost |
| Fable | Script hosts, stat-driven morphing, local reputation tags, per-character memory, simulation/host separation | PCRS, local reputation, quest/entity scripting, customization | Useful architecture reference; verify claims and licensing |
| Shenmue | Central world clock, authored schedules, routine state machines, occupancy limits, shared animation sets | Time-of-day, NPC routines, shops, weather, ambience | Later world-simulation layer; avoid real-time simulation for every NPC |

## Architectural patterns to adopt

### 1. Authoritative simulation with thin hosts

Use pure domain state and deterministic rules for battle, relationships, village economy, schedules, and puzzle connectivity. Unity (when deliberately introduced) owns rendering, animation, input, audio, navigation presentation, and platform integration—not rule authority.

- Domain systems own their state and expose narrow commands and queries.
- Presentation consumes immutable snapshots and domain events.
- Avoid direct cross-system object references; prefer interfaces or explicit event/data channels.
- Keep persistent state separate from transient presentation state.
- Inject deterministic randomness wherever reproducible simulation matters.

### 2. Data-driven definitions with a small, typed effect vocabulary

Adopt the pattern of Unciv's Uniques, not its syntax. Define a constrained effect vocabulary with typed parameters, validation, explicit stacking rules, and deterministic evaluation order.

Potential consumers include battle moves, abilities, equipment, status and arena effects; creature species and evolution; clan passives, leader traits, village buildings and policies; and dialogue checks, reputation tags, and quest conditions.

Do not create an unrestricted string/eval scripting language. Unknown effect IDs, invalid parameter ranges, incompatible targets, and unsupported stacking should fail validation at content-load time. Effects should be pure data interpreted by a small set of domain handlers.

### 3. Different simulation fidelity for different populations

Use three tiers rather than one universal NPC system:

1. **Major characters:** persistent identity, authored schedule, witnessed-event memory, PCRS dimensions, and explicit narrative state.
2. **Recurring minor characters/specialists:** role, schedule, location, lightweight needs/mood, a small memory/tag set, and limited decision logic.
3. **Ambient population:** aggregate counts and job assignments; no individual pathfinding or full relationship simulation.

This prevents the recurring-character plan from becoming a requirement to run hundreds of full AI brains. Update by scheduled ticks and meaningful events, not every frame.

### 4. World clock as a shared time source

A pure WorldClock should own canonical in-game date/time and emit discrete time-boundary events. NPC schedules, shop availability, weather, lighting, and village production subscribe independently. Define pause, fast-forward, offline progression, and catch-up behavior before implementation.

Do not make the clock a global service locator. Inject it or pass the current time snapshot into systems.

### 5. Puzzle connectivity as authored state, not continuous geometry inference

Represent puzzle spaces as nodes and edges. A discrete mechanism configuration selects which edges are enabled; ordinary BFS/A* then solves routes on the active graph. Recompute connectivity only after a discrete configuration change. Companion abilities and relationship gates may enable specific interactions, but the graph must remain inspectable and testable.

Mandatory puzzle paths need a guaranteed solution and safe recovery. Optional puzzles can carry higher difficulty and more valuable rewards. Art, camera, interaction affordances, and narrative context should be authored together, while the puzzle graph remains a testable domain model.

### 6. Typed customization and layered presentation

Keep numeric build/equipment fields enumerable and serializable. Use stable IDs for parts, equipment slots, dyes, morph controls, and creature components. Separate species base definition, individual variation/genes (only if breeding is approved), equipment and set effects, player appearance parameters, and presentation composition/material overrides.

Artist-authored extreme morph configurations with bounded interpolation are a promising mobile compromise, but need a representative rig and CPU/GPU profiling before commitment. Do not expose arbitrary bone transforms to players.

### 7. Relationships are event-driven, not merely a bar

PCRS remains the detailed personal relationship layer. Village-to-village stance should be derived from aggregate relationship/reputation state rather than maintained as a second independent matrix.

Local reputation tags are a useful cheap complement: witnessed actions create settlement-scoped tags; NPC preference data maps those tags to dialogue, service, and appraisal modifiers. Temporary mood/thoughts must remain distinct from persistent memory and durable relationship dimensions.

Regression, decay, cooldowns, and irreversible relationship states are design choices—not automatic features. They require explicit player-experience goals.

## Recommended scope boundaries

**Adopt as architecture principles now**
- Pure simulation / thin host boundary.
- Data-driven typed definitions and effect handlers.
- Event-driven persistent memory and relationship appraisal.
- Deterministic time and scheduled update budgets.
- Distinct fidelity tiers for major, minor, and ambient populations.
- Explicit graph-based puzzle connectivity.
- Typed, serializable customization schemas.

**Defer until battle core is stable**
- Village yields, jobs, policies, leader uniques, and production.
- NPC schedules, navigation, patrols, and ambient needs.
- Thought/ideology progression and dialogue micro-reactivity tooling.
- Character morph tooling, modular creature fusion, and dye pipeline.
- Portal Gauntlet puzzle graph prototype and mutable arenas.

**Avoid unless later evidence justifies**
- Full Civ-style tile micro-management, worker movement, and deep technology trees.
- Full individual simulation for ambient residents.
- Continuous pathfinding or geometry recomputation every frame.
- An unrestricted universal scripting/effect language.
- Frequent arena mutation as a battle mechanic.

## Source and licensing cautions

- The supplied OpenRCT2 report identifies GPL-3.0. Treat it as idea-level reference unless legal review approves a specific reuse strategy.
- The supplied Unciv and A Dark Room reports identify MPL-2.0; verify the exact repository, file headers, version, and obligations before any code reuse.
- Decompilation, reverse engineering, modding tools, and reconstructed source (including Fable and Shenmue references) require provenance and license review. Public availability is not permission to copy.
- Commercial-game descriptions are design hypotheses, not proof of implementation details. Verify technical claims against primary sources before using them to constrain architecture.

## Decision impact

No Decision Log entry is created. This is a synthesis of supplied research, not user approval of a specific mechanic. Existing battle decisions and canonical project priorities remain unchanged.

## Next use

When the battle core is stable, select one bounded village slice: one leader, a small number of major characters, aggregate ambient population, a few yields/jobs, one short doctrine branch, and one facility unlock. Reuse the same event stream for relationship appraisal and village effects. Do not build all seven villages at once.
