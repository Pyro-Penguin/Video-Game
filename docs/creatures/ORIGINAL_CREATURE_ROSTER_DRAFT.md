# Original Creature Roster — Provisional Draft 0.1

**Status:** Provisional design input. Not human-approved species data, not a selected roster, and not balance evidence.

## Purpose

Provide five original creature concepts and stat/move inputs so the existing pure-Python battle harness can be exercised without relying on Pokémon species data. This is a first-pass test roster, not a claim that these creatures are balanced or representative of the final game.

The machine-readable fixture is [original_creatures_draft.json](../../fixtures/original_creatures_draft.json). It deliberately preserves the existing Playtest A fixture and CLI contract.

## Draft stat spreads

All values are direct provisional game-stat inputs. HP is the harness's current field name for Vitality. The synthetic D-022 envelope is used only as a screening range: Vitality 250–500, Attack 200–400, Defense 200–350. It is not a final creature-stat standard.

| Creature | Intended role | Vitality | Attack | Defense | Special Attack | Special Defense | Speed |
|---|---|---:|---:|---:|---:|---:|---:|
| Thornback | Physical bulwark | 460 | 320 | 340 | 220 | 300 | 220 |
| Zephyrkin | Fast physical striker | 280 | 380 | 220 | 280 | 230 | 390 |
| Emberlynx | Fast special attacker | 300 | 220 | 230 | 390 | 300 | 340 |
| Tideforged | Special-defense anchor | 430 | 250 | 330 | 290 | 350 | 210 |
| Gloamantis | Mixed disruptor | 350 | 330 | 260 | 340 | 270 | 310 |

## Creature concepts

### Thornback — physical bulwark
A patient frontline guardian built around physical durability. Its low speed and low special attack are intentional weaknesses. It tests whether a slow defensive role can survive focus fire and still contribute.

### Zephyrkin — fast physical striker
A high-tempo skirmisher with the roster's strongest speed and physical attack. Its low Vitality and defenses test the cost of offensive specialization.

### Emberlynx — fast special attacker
A special burst attacker with enough speed to threaten fragile targets. Low physical durability tests whether a special attacker can be pressured meaningfully.

### Tideforged — special-defense anchor
A durable special-defense role with mixed offense and low speed. It tests whether defensive specialization remains useful against special pressure.

### Gloamantis — mixed disruptor
A flexible mixed attacker with moderate bulk and speed. It tests role compression without matching either specialist's peak stat.

## Move inputs

Each creature has three placeholder attacks at Power 40, 80, and 120, using the existing CLI fixture schema. Physical and special categories select the current stat pairs. Names are flavor labels only.

No move currently has accuracy, target pattern, priority, status, cooldown, resource cost, secondary effect, multi-hit behavior, or unique mechanics. Those should not be inferred from the names.

## Type and identity boundary

The JSON includes candidate affinity labels (Plant, Air, Fire, Water, Shadow) only as identity prompts. They do **not** define the seven battle types, village assignments, type matchups, STAB, resistance, weakness, or immunity. The pipeline deliberately applies neutral effectiveness to every interaction.

## Commander test input

The commander is assigned 380 Vitality and 300 in each other stat as a neutral pipeline placeholder. This is not a finalized player-character stat line or a competitive normalization decision.

## What this fixture can test

- Whether five original concepts can be represented by the current CLI schema.
- Whether the existing turn resolver can run three mixed-role scenarios.
- Whether Candidate B c=100 and c=143 can be exercised through the same injected damage seam.
- Whether reserve deployment and deterministic trace generation still function with original-game stat inputs.

## What it cannot establish

- Creature balance, role viability, matchup fairness, or the desired 4–6-hit pacing.
- The final damage equation or offset.
- Type-chart balance, STAB, immunities, or village/type design.
- Move usefulness or action diversity; all moves are direct-damage placeholders.
- Competitive roster legality, preview rules, or progression fairness.

## Review and acceptance gate

Before treating this as Playtest B balance evidence, review each creature's role, stats, and move category. Changes should be recorded as a new fixture revision with a clear rationale. Human acceptance is required before the roster or any resulting balance conclusion is promoted into the decision log.

## Data ownership and flow

- The JSON fixture owns the provisional creature and commander inputs.
- The CLI loads and validates the fixture read-only.
- The battle harness owns no persistent match state; it receives commands and returns immutable state/events.
- Candidate B is a replaceable experiment adapter, not a selected formula.
- Type effectiveness is fixed to neutral in this fixture.
