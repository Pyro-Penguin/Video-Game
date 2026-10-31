# AGENTS.md

## Repository reality
This repository is the shared design, documentation, and mechanics-research workspace for an original creature-collecting RPG. It currently contains Python experiments, JSON test fixtures, and uncompiled navigation C# candidates. It is **not** a Unity project and does not contain a production game runtime. Do not invent engine versions, project paths, assemblies, scenes, or build commands.

## Required startup
1. Read `COLLABORATION_PROTOCOL.md`.
2. Read `PROJECT_INDEX.md`, `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/DECISION_LOG.md`, and `docs/OPEN_QUESTIONS.md`.
3. Read only the task-specific specifications, source, fixtures, and tests needed for the assigned work.

## Authority and decision fidelity
- Follow `COLLABORATION_PROTOCOL.md` for document authority, status labels, verification, and handoff.
- Use only **Confirmed**, **Provisional**, **Unresolved**, and **Superseded** for decision status.
- AI proposals, fixtures, experiments, and passing tests do not approve game rules. Human acceptance is explicit.
- `PROJECT_STATUS.md` owns the canonical project-wide priority order. Do not silently reorder it.
- Preserve original archives and user-provided source material; do not replace them with reconstructed approximations.

## Work boundaries
- `experiments/` contains offline analytical tools, not shipped game code. Preserve reproducibility, explicit assumptions, deterministic seeds, and tests.
- `fixtures/` contains test inputs. A fixture is not canonical creature content or an approved balance dataset unless explicitly accepted.
- `prototypes/navigation/` contains bounded Unity-side candidates. They are uncompiled and depend on domain/scene source not present here; never claim Unity verification without an actual Unity build/test.
- Do not create a Unity project, production C# runtime, online services, or broad content systems without explicit authorization and a coherent design gate.
- Keep changes small, modular, and within the assigned work package. Do not add provider-specific agent infrastructure merely because a template suggests it.

## Validation commands
Run the relevant package tests after changing code. The complete current repository validation sequence is:

```bash
(cd experiments/common && python3 -m unittest -v)
(cd experiments/damage_rng && python3 -m unittest -v)
(cd experiments/damage_equation && python3 -m unittest -v)
(cd experiments/stat_range_sensitivity && python3 -m unittest -v)
(cd experiments/battle_sim && python3 -m unittest -v)
(cd tools && python3 -m unittest -v test_validate_docs.py && python3 validate_docs.py)
```

The GitHub Actions workflow additionally runs the damage RNG tests on Python 3.10–3.13 and publishes deterministic experiment artifacts. If a command fails, report the exact failure; do not claim verification.

## Reporting
For each repository change, report the files changed, commit, read-back verification, tests actually run, and remaining limitations. Distinguish **Proposed**, **Committed**, **Verified**, **Tested**, and **Accepted** work states. Never claim a commit, test, Unity build, or human approval that did not occur.
