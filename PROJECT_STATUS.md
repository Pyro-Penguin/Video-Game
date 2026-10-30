# Project Status

## Project
Original creature-collecting RPG with tactical PvP ambitions. Long-term target platform is mobile (iOS/Android). No Unity project or engine implementation exists yet.

## Current Stage
**Design consolidation and standalone mechanics experimentation.** The repository remains intentionally engine-independent.

## Verified Progress
- Documentation foundation created and indexed.
- Supplied game, story, world, creature, class, exploration, and art/audio concepts organized into topic documents.
- Battle-format contradictions preserved explicitly.
- Battle format decision framework added, including a provisional local-prototype candidate clearly marked as not approved.
- Stat system research plan added; no stat formula has been selected.
- Standalone Python damage RNG experiment and automated tests committed.
- Prior local test run recorded: 6 tests passed.
- Seeded JSON report committed.
- GitHub Actions workflow executed successfully on Python 3.10, 3.11, 3.12, and 3.13; automated tests and JSON report smoke test passed in all four jobs.

## Current Experiment
[Damage RNG Experiment](experiments/damage_rng/README.md) compares six RNG models. It does not select a final game rule.

## Current Design Priorities
1. Resolve side composition: what 3v3 counts, registered/selected roster, player role, active field, and reserve.
2. Define turn phases, action economy, targeting, priority/speed/ties, invalidated actions, and knockout timing.
3. Define replacement and victory conditions, including simultaneous defeat cases.
4. Define stat ownership and Level 100 normalization.
5. Define the full damage formula, modifier order, and rounding separately from RNG.
6. Reconcile the type inventory and seven-village structure.
7. Audit Light/Shadow stat drafts before using them as balance inputs.
8. Define competitive clauses and timer policy after core turn resolution is coherent.

See [Battle Rules Decision Checklist](docs/battle/BATTLE_RULES_DECISION_CHECKLIST.md) for the decision-by-decision register.

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
