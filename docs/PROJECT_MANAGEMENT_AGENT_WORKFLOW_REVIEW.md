# Project Management Review: Free-Agent Development Model

**Status:** Engineering/process recommendation. Not a provider contract, budget commitment, or approved game-design decision.

## Executive recommendation

Adopt the proposal's central operating principle: repository state is durable project memory, deterministic automation should replace repeated model bookkeeping, and each agent task should receive a compact, complete work package.

Do **not** copy the proposed scaffold wholesale. Several examples assume a Unity/C# application that does not exist in this repository, some provider quota statements are not verified for the current date/account, and the supplied Copilot hook example does not match the current documented hook schema.

The project already has a useful governance foundation in `COLLABORATION_PROTOCOL.md`, `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/DECISION_LOG.md`, and `docs/OPEN_QUESTIONS.md`. New agent infrastructure should reinforce those files, not create a competing management system.

## Project-management implications

When agents are low-cost or available at no additional cash cost, the limiting resource shifts toward:

1. Human decisions and review bandwidth.
2. Integration and verification.
3. Context assembly and task handoff.
4. Provider-specific request/credit quotas, which vary and change.
5. CI compute, artifact storage, and repository maintenance.

The response is not maximum parallelism. It is a controlled flow of small, independently verifiable work packages.

### Required work-package contract

Every non-trivial agent assignment should include:

- **Outcome:** one observable deliverable.
- **Owner:** one accountable agent or human; other agents may contribute, but there is one integration owner.
- **Scope:** exact files/subsystems allowed to change.
- **Authority:** relevant confirmed/provisional decisions and documents.
- **Dependencies:** what must exist first.
- **Acceptance:** commands, tests, output checks, or human review that prove completion.
- **Stop conditions:** unresolved design decisions, scope expansion, failing tests, or missing source.
- **Handoff:** commit, verification state, test results, limitations, and next action.

Do not split coupled changes across agents merely to increase parallelism. Parallelize independent research, documentation, or isolated test work; serialize changes to shared source files and decisions.

## Review of the supplied practices

| Practice | Assessment | Recommendation |
|---|---|---|
| Request/credit budgeting | Correct principle; provider quotas change and are account-specific | Record the active provider and meter only when verified. Never hard-code an assumed monthly request cap as project truth. |
| Avoid multi-agent debate | Directionally efficient, too absolute | Avoid repetitive debate loops. Reserve independent review for high-risk milestones: damage math, resolver semantics, schemas, CI/security, and engine ports. |
| Dense context packet | Strong | Build one complete task packet from the index, status, handoff, decision log, and relevant source. Do not spend turns rediscovering known context. |
| Deterministic scripts and CI | Strongest recommendation | Move repeatable validation into tests and CI. Keep human review for design correctness and acceptance. |
| Reviewer agent per PR | Sensible to batch | Use CI on every change; use targeted independent review for high-risk changes and periodic accumulated-diff reviews. |
| Minimal procedural instructions | Strong | Keep a short portable root file; load domain-specific details only for matching paths. |
| Repository as memory | Strong | Continue using the existing protocol/status/handoff/decision structure as the authoritative record. |

## Review of the proposed repository architecture

### Adopt now

- A root `AGENTS.md` as a portable entry point.
- Path-scoped instructions only where a real code area exists.
- Existing GitHub Actions as the deterministic last gate.
- Task-specific prompts only after a workflow repeats often enough to justify one.
- A clear distinction between fixture data, provisional proposals, confirmed decisions, and tested code.

A repository-specific `AGENTS.md` has been added. It points agents to the existing collaboration protocol and states the actual repository boundaries and validation commands. It does not assume `src/`, `Assets/`, Unity 6, a .NET solution, or production C# code.

### Defer

- **Generated `.github/copilot-instructions.md`:** GitHub Copilot currently documents support for `AGENTS.md` and path-specific instructions. Do not generate a duplicate copy unless a specific client/version demonstrably needs an adapter. If an adapter is later required, keep it minimal and verify it in that client.
- **Nested `AGENTS.md` files:** add only when a subproject has distinct ownership, commands, or constraints. No `src/` or Unity subtree exists yet.
- **Skills and prompts:** create only for recurring procedures. The current test commands are explicit and already automated; a skill layer is not yet necessary.
- **Hooks:** defer until a supported client and exact event schema are confirmed. Hooks are tool-specific, not a universal repository standard.
- **Instruction-budget script:** defer until multiple instruction files exist and measured drift justifies a budget gate. Character-count divided by four is only a rough estimate, not a tokenizer.
- **Provider budget YAML:** keep personal/account quota values out of canonical project decisions. A dated local note is enough if the active plan requires tracking.

### Reject as written

The proposed `AGENTS.md` refers to `src/Core/`, `src/Domain/`, `src/Presentation/`, `Assets/`, `App.slnx`, and `tests/App.Domain.Tests/`. None exists. It also states that the Python harness is the oracle for future C# damage code; that cross-runtime authority and parity contract have not been approved.

The proposed out-of-scope list includes `legacy/` and `Assets/ThirdParty/`, which are not present. It forbids changes to `.github/workflows/**` while simultaneously proposing new workflows there. Do not import those assumptions.

The sample hook JSON is incomplete for the current Copilot hook reference: current command-hook examples include a top-level `version`, event keys such as `preToolUse`, and an item `type` plus an execution field such as `bash` or `exec`. The exact payload differs between native and VS Code-compatible event formats. The supplied guard script also fails open on malformed/missing input and does not robustly canonicalize traversal paths or symlinks. It must not be treated as a security boundary without schema-specific tests.

## Current project-specific workflow

The current project is still in design consolidation and Python mechanics research.

| Workstream | Current state | Gate to advance |
|---|---|---|
| Damage equation | Provisional Candidate B narrowing at c=100 and c=143; no formula selected | Original creature inputs, controlled comparisons, explicit design acceptance |
| Original creature roster | Five provisional concepts now drafted | Human review of roles, stats, move categories, and identity |
| Battle resolver | Pure-Python attack-focused harness | Resolve outstanding semantics before broad action expansion |
| Navigation | Bounded Unity-side candidates only | Obtain complete domain source and Unity project; compile and run Play Mode tests |
| Unity baseline | Not present | Explicit project-creation authorization and editor/platform confirmation |
| Art direction | Reference folders and Environment image uploads exist | Curate references with source/attribution and convert into approved visual constraints |

The five-creature draft is a pipeline-ready input proposal, not a balance conclusion. Its type labels are identity prompts only; the type chart remains unresolved. The existing Pokémon fixture remains intact as Playtest A engineering scaffolding. A reproducible neutral Power-80 single-attacker screen covers all 25 pairs at c=100 and c=143; mean repeated-hit-to-KO is 7.68 and 7.76 respectively, with a 5–12 range. This narrow result does not resolve offset selection or match pacing.

## Recommended milestone gates

### M0 — Repository and agent operating baseline (complete)
**Done when:** current project status, handoff, decision authority, CI commands, and agent entry instructions agree. No duplicate project-management source of truth.

### M1 — Original-creature input review and damage-model narrowing
**Done when:** the human accepts or revises the provisional five-creature data; c=100 and c=143 are compared using the same fixture and full floored gates; output limitations are documented. No formula is auto-selected.

### M2 — Battle-rule closure
**Done when:** the remaining Priority 1 damage contract is explicit and the Priority 2 comparator/action/mutual-KO questions needed for the minimum prototype are resolved.

### M3 — Pure battle-domain vertical slice
**Done when:** deterministic tests cover the accepted rules and a complete local match without engine objects. Keep rules, state, damage, and policies engine-independent.

### M4 — Unity baseline and presentation
**Done when:** the user authorizes the engine project, the exact editor/platform baseline is recorded, the pure domain is integrated, and two local sides can finish a match through touch UI.

### M5 — Initial content and polish
**Done when:** the approved minimum content set is data-driven, tested through the same rules, and playable end-to-end. Broad world production follows only after the core loop is stable.

## Operating cadence

- **Every work package:** one owner, one deliverable, explicit scope, acceptance checks, stop conditions.
- **Every code change:** deterministic tests and CI; report exact commit and verification state.
- **Every milestone:** one accumulated-diff review and explicit human acceptance.
- **Every handoff:** update `HANDOFF.md`; update `PROJECT_STATUS.md` only when stage/priority/evidence changes; update `DECISION_LOG.md` only for human-accepted decisions; update `OPEN_QUESTIONS.md` when unresolved work changes.
- **Every provider/tool change:** verify current plan limits and actual instruction/hook behavior before editing project policy.

## Success metric

Optimize for **verified, human-accepted milestone outcomes per unit of human attention**, not agent count, generated lines, number of commits, or raw request volume.
