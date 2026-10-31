---
name: Python experiment rules
description: Rules for offline mechanics experiments, fixture runners, and repository validation scripts.
applyTo: "experiments/**/*.py,tools/**/*.py"
---

# Python experiment rules

- Code in these paths is offline research/validation tooling, not shipped game runtime.
- Keep experiment assumptions explicit and separate from accepted game rules.
- Prefer standard-library dependencies; justify any new dependency before adding it.
- Preserve deterministic outputs. Any stochastic experiment must expose and record its seed.
- Use exact rational arithmetic where flooring, ratios, or candidate ordering can affect conclusions.
- Every behavioral correction needs a focused regression test.
- Keep CLI inputs/outputs schema-stable; update fixtures, tests, and documentation together when a schema intentionally changes.
- Do not add engine, Unity, network, UI, or persistence dependencies to these experiments.
- Never describe a passing synthetic fixture as proof of game balance or player-facing feel.
