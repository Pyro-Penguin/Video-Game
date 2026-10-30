# Open Questions

Questions are grouped by what they block. None of the items below should be treated as decided.

## Priority 1 — Battle Format (Blocks a Coherent Battle Prototype)
1. Does "3v3" count the player character, or three monsters in addition to the player?
2. Does each side bring five monsters and select three, with the player separate?
3. How many monsters are active simultaneously?
4. Is there one reserve, or can all selected monsters rotate?
5. Is the player a field combatant, a commander outside the field, or both?
6. Does player-character defeat immediately end the match?
7. Can the player be targeted directly? Are there protection, interception, or guard rules?
8. What actions does the player take, and how many actions does each active monster take?
9. Are all actions selected before simultaneous resolution?
10. What happens if a selected target is defeated before an action resolves?
11. How are speed, priority, ties, and dependent actions resolved?
12. When and how does a reserve enter play?

See [Battle Format Decision Framework](battle/BATTLE_FORMAT_DECISION.md).

## Priority 2 — Battle Clock and Competitive Rules
1. Does the 45-second move timer run inside the 7-minute player clock or independently?
2. Does the player clock pause during animations, opponent selection, and forced replacement?
3. What happens when a player clock expires?
4. What happens when the 20-minute match clock expires?
5. Are the 64-second preview and all three clocks mandatory in the first prototype?
6. Does Species Clause use stable species IDs across forms?
7. Does Item Clause apply to held item identity, item category, or consumable charges?
8. What exactly is visible in Open Team Lists, and when is it revealed?

## Priority 3 — Stats and Damage
1. What are the six core stats and their exact definitions?
2. Do player and monster stats use the same calculation pipeline?
3. What is the role of base stats, individual variation, nature/class, level, equipment, and transformations?
4. Is the previously discussed 70-point allocation with a 30-point per-stat cap still intended?
5. What does Level 100 auto-normalization preserve or remove?
6. What is the complete base damage equation?
7. Where does RNG apply, and at which exact points does integer truncation occur?
8. What are the finalized STAB and type-effectiveness values?
9. How are immunity, minimum damage, critical hits, screens, weather, terrain, and status handled?

See [Stat System Research Plan](STAT_SYSTEM_RESEARCH_PLAN.md), [Damage Model](battle/DAMAGE_MODEL.md), and [Damage RNG Experiment](../experiments/damage_rng/README.md).

## Priority 4 — Types, Villages, and Progression
1. Which of the 12 named affinities are actual battle types?
2. Are Light, Shadow, and Prismatic part of the same chart or special affinities?
3. Which seven types/villages form the initial structure?
4. What are the complete type multipliers, including resistances and immunities?
5. Does each village have exactly three clans?
6. How does origin identity coexist with later type/move flexibility?
7. Are weather-like clan abilities global, local, or user-side effects?

## Priority 5 — Story and Feature Scope
1. What is the protagonist's role in the AI-related coup?
2. What agency do the Light and Shadow mythical creatures have?
3. Is the Portal Gauntlet the primary capture mechanic?
4. Is the old man the first companion, the respec guide, or both?
5. Is the mother-as-leader succession story part of the main plot?
6. Which exploration features are core versus optional: shrinking, rideable monsters, Dimengeon-like encounter storage, and Nemesis-style rivals?

## Project Integration (Deferred)
1. What Unity editor version will be used?
2. Where is the actual Unity project folder, and does it contain `Assets/`, `Packages/`, and `ProjectSettings/`?
3. Which existing archive, if any, is the canonical starting point?
4. Are there scripts or assets that must be preserved?

## Deferred Until the Battle Core Is Stable
- Full campaign/world structure and village-specific progression.
- Online multiplayer, matchmaking, and server authority.
- Save format and long-term progression persistence.
- Final art pipeline and production asset creation.
- Localization, analytics, monetization, and live operations.
