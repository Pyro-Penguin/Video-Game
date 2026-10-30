# Collaboration Protocol

## Purpose and operating model

This repository is the shared, durable memory of the Video Game project. Individual AI conversations are temporary workspaces: useful analysis must be transferred into the repository when it changes project knowledge, decisions, specifications, experiments, or the next work handoff.

The project is currently an engine-independent design and mechanics-experiment workspace. No Unity project or engine implementation exists. Do not create an engine project, promote a design proposal to a rule, or expand implementation scope without the required human direction.

## Mandatory session startup

Read in this order:

1. [Collaboration Protocol](COLLABORATION_PROTOCOL.md) — operating rules and authority.
2. [Project Index](PROJECT_INDEX.md) — repository map.
3. [Project Status](PROJECT_STATUS.md) — current stage, verified progress, and canonical priorities.
4. [Developer Handoff](HANDOFF.md) — current work state and next action.
5. [Decision Log](docs/DECISION_LOG.md) — accepted and unresolved durable decisions.
6. [Open Questions](docs/OPEN_QUESTIONS.md) — unresolved questions grouped by project priority.
7. Only then read the task-specific specifications, experiments, source material, or code needed for the task.

Do not reread the entire repository by default. Follow links from the index and handoff, then inspect the smallest relevant set of files. If required context is missing, retrieve it rather than guessing.

## Document authority

When sources conflict, apply this hierarchy:

1. **Explicit current human direction.** It supersedes an older document or AI interpretation. Record durable changes in the repository.
2. **Collaboration Protocol.** Governs process, terminology, and collaboration.
3. **Decision Log.** Authoritative record of accepted, provisional, unresolved, and superseded decisions.
4. **Project Status.** Authoritative current stage, verified progress, and single canonical project-wide priority order.
5. **Relevant specification.** Defines detailed system requirements within the boundaries of the Decision Log.
6. **Open Questions.** Organizes unresolved questions against the canonical priority order; it does not independently set project-wide priorities.
7. **Handoff, experiments, reports, informal notes, and conversation history.** Useful context, but cannot silently override the sources above.

A specification cannot silently override the Decision Log. Project Status cannot silently rewrite a design decision. Open Questions cannot establish a competing priority order. If two authoritative sources appear inconsistent, surface the conflict, state the impact, and resolve it through an explicit human decision or a clearly scoped reconciliation entry. Do not conceal ambiguity by editing one side without recording why.

## Decision fidelity and status labels

Use exactly these four decision-status labels:

- **Confirmed** — the stated decision is accepted. Any remaining limits or open details must be stated explicitly in its record.
- **Provisional** — an accepted working direction that remains subject to validation or revision.
- **Unresolved** — no decision has been made.
- **Superseded** — replaced by a later decision; link the replacement ID.

Do not use variants such as “Confirmed direction,” “Tentative,” or “In progress” as decision statuses. Work progress is tracked separately below.

Brainstorming, recommendations, simulations, test results, and AI-generated proposals are not confirmed game rules unless the human explicitly accepts them. Preserve uncertainty. Distinguish what is decided from what remains open.

### Decision log metadata

Every new decision entry must include:

- Unique ID.
- Topic.
- Status (one of the four labels).
- Decision date (ISO 8601, YYYY-MM-DD).
- Decision / current record, including explicit scope and limitations.
- Rationale / source of authority.
- Dependencies or affected decisions, where applicable.
- Supersedes / superseded by references, where applicable.

Existing entries should be migrated to this structure as they are touched; do not fabricate historical dates or rationales. Use “Historical date not recorded” or “Not recorded in source” where the repository does not establish the information.

### Append-only history

- Add a new decision row when an accepted decision changes; do not erase the previous decision or its rationale.
- Mark the old row **Superseded** and link the replacement ID.
- Keep IDs unique and never reuse them.
- Update the relevant specification and Open Questions when a decision changes.
- A correction to wording that does not change the decision may edit the existing row, but preserve the decision's scope and provenance.

## Work verification is separate from decision status

Track work using these states; they are not decision labels:

1. **Proposed** — described but not yet written to the repository.
2. **Committed** — changes have been written to the repository.
3. **Verified** — the committed content has been read back or inspected in its destination.
4. **Tested** — relevant automated or manual checks have been run and their results recorded.
5. **Accepted** — the human has reviewed and approved the result.

Never claim a later state without evidence. A successful commit is not verification; read back the changed content. Verification is not testing. Passing tests do not prove design correctness. Human acceptance is not implied by AI confidence or CI success.

For repository changes, report the exact files changed, commit identifiers when available, read-back verification, tests actually run, and remaining work. If a write fails or cannot be verified, say so plainly.

## Anti-silo workflow and conditional documentation updates

Before proposing or implementing a change:

1. Inspect the current index, status, handoff, decision log, open questions, and relevant specification.
2. Search for existing work, experiments, prior decisions, and contradictory records.
3. Identify ownership, dependencies, and the smallest coherent change.
4. State assumptions and distinguish recommendations from decisions.
5. Make changes only within the user's authorization.

Update documents only when their authoritative content changes:

- **PROJECT_STATUS.md:** stage, verified progress, canonical priorities, or implementation status changes.
- **HANDOFF.md:** next-session starting point, active task, verification state, or blocking context changes.
- **DECISION_LOG.md:** a durable decision is accepted, revised, or superseded.
- **OPEN_QUESTIONS.md:** a question is added, resolved, split, or reprioritized within the canonical plan.
- **Specifications:** requirements, rules, constraints, or system details change.
- **PROJECT_INDEX.md:** navigation or repository structure changes.
- **Experiments/reports:** experiment method, code, or results change.

Do not edit every document after every task. Avoid duplicate descriptions of the same rule; link to the authoritative source. Keep handoffs concise and actionable.

## Canonical project priorities

[PROJECT_STATUS.md](PROJECT_STATUS.md) owns the single project-wide priority list. [OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md) groups the unresolved questions in that order and must not create a competing priority ranking.

Current priority order is maintained only in Project Status. The current first priority is the damage equation design resolution as a prerequisite to expanding battle-resolution queues/state loops. See decision D-014 for the recorded reconciliation.

## Architecture and engineering guardrails

When engine implementation is explicitly authorized:

- Target mobile iOS/Android; keep performance, touch latency, safe areas, battery, and memory in scope.
- Separate pure game rules, math, and state from engine-facing presentation/input classes wherever practical.
- State data ownership, lifetime, and communication method (events, interfaces, or data channels) before introducing a system.
- Prefer composition and narrow interfaces; avoid bidirectional component references and static service locators.
- Keep engine components thin. Use data-driven configuration for balance-sensitive rules.
- Avoid allocations, LINQ, and unnecessary string work in per-frame or turn-resolution hot paths; use pooling where appropriate.
- Test core rules without loading an engine scene.
- Do not assume a Unity version, project root, or existing Unity project.

## Human approval boundaries

Do not do any of the following without explicit human approval:

- Create or modify a Unity project or engine implementation.
- Promote a provisional or unresolved mechanic to a confirmed rule.
- Select a final damage/RNG model where the decision remains open.
- Expand the relationship/emotional system's dimensions.
- Expand the game into full 4X city micro-management.
- Treat AI-generated code as production-ready without inspection and relevant tests.
- Make irreversible or destructive repository changes.

## Session startup prompt

Use this at the beginning of a new AI session:

> Read COLLABORATION_PROTOCOL.md first, then follow its mandatory startup sequence. Inspect the current repository state and the task-specific files before proposing changes. Treat the repository as the shared project memory and this conversation as temporary. Do not invent decisions or promote experiments to rules. Report conflicts, assumptions, ownership, dependencies, and verification honestly. Take the highest-priority authorized next step and update only the documents whose authoritative content changes.

## Task completion and handoff template

At the end of substantial work, provide a concise report using this structure:

- **Outcome:** what changed or was learned.
- **Files changed:** exact repository paths, or none.
- **Decision impact:** decision IDs added/changed, or explicitly none.
- **Work state:** Proposed / Committed / Verified / Tested / Accepted, with evidence for each reached state.
- **Checks:** exact tests or inspections run and their results; state “not run” when applicable.
- **Open issues:** unresolved risks, conflicts, or missing inputs.
- **Next action:** one concrete next step, its dependencies, and what requires human approval.

Before committing a handoff, re-check the verification state against the latest relevant CI run and the exact commit it tested. Update stale run IDs, pending/completed wording, and artifact counts; never carry forward an unverified status statement.

Do not create a handoff merely to restate unchanged context. Update HANDOFF.md when the next-session starting point or active work has materially changed.
