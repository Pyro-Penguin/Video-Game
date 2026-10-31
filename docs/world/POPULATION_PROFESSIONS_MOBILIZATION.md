# Population, Professions & Mobilization

**Status:** Unresolved design investigation. This document records a concept for later review; it does not authorize implementation or establish confirmed game rules.

## Purpose

Create a world in which people have persistent lives and useful civilian roles, while also being capable of participating in tournaments, organized war, and unexpected encounters. A person's combat capability should coexist with—not replace—their profession, relationships, commitments, and place in the village.

**Design principle:** When someone leaves their job to fight, the world should notice their absence. When they return, their life should continue.

## Core model: three independent dimensions

Do not collapse profession, combat capability, and current availability into one class or unit type.

1. **Profession / contribution** — what the person normally does for the community: farming, smithing, hunting, research, trade, healing, guarding, transport, leadership, and so on.
2. **Combat capability** — what the person can do in a fight, shaped by training, experience, physical attributes, abilities, equipment, and willingness. Most adults may have some basic defensive capability; dedicated fighters and trained professions have meaningful advantages.
3. **Availability / readiness** — whether the person can participate in a specific event now, considering location, schedule, work commitments, fatigue, injury, equipment, fear, loyalty, and other circumstances.

These dimensions interact but remain separately represented. A blacksmith can be a capable armored fighter; a hunter can be a scout or archer; a farmer may defend their home but be poorly prepared for a campaign. Profession should influence likely skills and equipment without hard-locking a person's identity.

## Event contexts

### Tournaments

- Participation is scheduled, registered, and visible to the community.
- Participants temporarily leave normal duties; the village may experience reduced service or production.
- Results can affect reputation, rivalries, relationships, and future opportunities.
- NPCs can be contenders, support staff, spectators, or people who decline to participate.

### Organized war and mobilization

- Mobilization draws people from professions and households into a shared effort.
- Recruitment may be voluntary, socially expected, legally required, coerced, or refused depending on the society and circumstances.
- The village experiences opportunity costs: reduced production, fewer services, weaker local security, transport constraints, and family disruption.
- Casualties, injuries, absences, desertion, and return home have persistent consequences.
- Do not assume all villagers respond identically or that every conflict creates a universal draft.

### Random engagements

- Participation depends on who is present, equipped, trained, committed, and willing at the moment.
- Possible responses include fighting, defending, fleeing, hiding, warning others, protecting dependents, or arriving too late.
- A person should not automatically become a battle unit merely because an encounter exists nearby.

## Simulation layers and fidelity

Use different simulation fidelity according to narrative importance and proximity to the player.

1. **Named / major characters:** persistent identity, profession, schedule, relationships, beliefs, combat profile, commitments, and consequential history.
2. **Minor named / local characters:** lighter individual state, with only the details needed for local events and continuity.
3. **Ambient population:** aggregate counts and availability by profession, location, and broad readiness; do not run a full schedule and combat simulation for every background resident.

The village layer tracks community-level production, services, security, and disruption. It reacts to people leaving, returning, being injured, dying, migrating, or changing roles. Avoid turning this into worker-by-worker city-builder micromanagement.

World events (tournaments, raids, wars, monster attacks, emergencies) request participants from the population simulation. The population layer determines who can respond and at what cost; the battle layer resolves the encounter; outcomes are reconciled back into persistent character and village state.

## Ownership and data flow (conceptual; no runtime exists)

The repository is currently a design/documentation workspace plus standard-library Python analytical experiments. It contains no Unity project, C# engine, MonoBehaviour lifecycle, mobile runtime, or gameplay hot path. The following is a future architecture sketch only, not a current code review or implementation plan.

- **Persistent character data:** owns identity, profession, training, relationships, beliefs, and durable injuries/history. Lifetime: character/world save.
- **World / population simulation:** owns schedules, job assignment, local availability, mobilization, and village-level aggregate effects. Lifetime: world session/save.
- **Encounter / battle simulation:** owns temporary encounter participants and combat state. Lifetime: one encounter.
- **Reconciliation boundary:** battle results are returned to the world through explicit outcome data or domain events; the world updates durable character and village state. Avoid persistent character objects holding bidirectional references into a battle scene.

The exact communication mechanism (events, commands, or narrow interfaces), update cadence, persistence schema, and simulation fidelity remain unresolved until a runtime architecture is deliberately authorized.

## Shared character model across game modes

The same conceptual character definition should support three related but distinct populations:

- **Broad world population:** includes ordinary, untrained, and non-combatant people; profession and social contribution matter.
- **Final-stage story / encounter roster:** focuses on notable creatures and combatants used for authored encounters and progression.
- **Normalized competitive roster:** uses standardized competitive rules so a character's civilian economic value, village wealth, or campaign progression does not create an unfair battle advantage.

These are not one identical balance cohort. Define explicit translation/normalization rules between them rather than forcing all world inhabitants into competitive stat distributions.

## Design constraints

- No universal requirement that every person fight.
- No assumption that profession determines combat class.
- No job micromanagement or five separate player-facing meters; derive availability and readiness from underlying state where possible.
- The village should register meaningful absences and returns without simulating every background person at full fidelity.
- Training, equipment, fatigue, injury, age, fear, loyalty, relationships, and circumstances can affect participation, but avoid arbitrary hidden dice that make NPC behavior feel incoherent.
- Competitive normalization must prevent economic or narrative progression from becoming a competitive power advantage.
- The system should support the experience pillars of Discovery, Connection, Mastery, Expression, and Transformation without becoming a management game for its own sake.

## Open questions for later review

1. What population scale and simulation fidelity are needed for the first playable slice?
2. Which professions are represented individually, and which are aggregated?
3. What minimum combat capability does an ordinary adult have, and how is it expressed without making everyone a trained soldier?
4. How do voluntary service, civic obligation, conscription, refusal, and desertion vary by village and political context?
5. Which absences should visibly affect services, production, security, or relationships?
6. How do age, injury, fatigue, fear, and equipment affect availability without creating excessive simulation complexity?
7. How are tournament registration, war mobilization, and spontaneous encounters scheduled and reconciled?
8. What is the exact conversion boundary between world characters, authored combatants, and normalized competitive participants?
9. How do consequences persist when a character is injured, killed, missing, captured, or returns home?
10. What is the smallest prototype that demonstrates the principle without requiring a full population simulator?

## Suggested review sequence

1. Agree on the player-facing fantasy and consequences before choosing simulation technology.
2. Define one small village with a small named cast plus aggregated ambient population.
3. Walk the same people through a normal workday, a tournament, a local emergency, and a mobilization event.
4. Record what changes in their availability, village services, relationships, and post-event state.
5. Only then define data schemas, event boundaries, and a prototype scope.

## Inspiration note: 0 A.D.

The 0 A.D. citizen-soldier concept is useful as inspiration for the opportunity cost of mobilization: the same population contributes to civilian production and military action. Borrow the design principle, not necessarily its RTS control model, ECS architecture, formations, or real-time micro-management. This RPG needs persistent lives, schedules, relationships, and authored narrative consequences rather than an RTS worker-selection loop.
