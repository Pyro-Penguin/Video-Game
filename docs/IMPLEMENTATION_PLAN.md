# Implementation Plan

**Authority:** This plan organizes milestones. `PROJECT_STATUS.md` remains the sole canonical project-wide priority list; `docs/DECISION_LOG.md` remains authoritative for accepted/provisional/unresolved game decisions. This plan does not approve mechanics or authorize engine work by itself.

## Goal

Reach a coherent, deterministic local battle prototype before broad world/content production. The current repository is an engine-independent design and Python research workspace. No Unity project or production C# runtime exists.

## Gate 0 — Repository and research baseline

- [x] Establish the project index, status, handoff, decision log, open questions, and collaboration protocol.
- [x] Establish Python experiment packages and GitHub Actions validation.
- [x] Add a portable `AGENTS.md` entry point that reflects the repository as it actually exists.
- [x] Preserve the Pokémon-based Playtest A fixture as pipeline-only scaffolding.
- [x] Draft five original creatures as provisional Playtest B inputs.

**Exit criteria:** project state and validation boundaries are documented; Python experiments and docs pass CI. This gate is complete, but the original creature draft still requires human review.

## Gate 1 — Priority 1: Damage-model decision and original input review

- [ ] Review the five original creature concepts, roles, direct stat spreads, and placeholder move categories in [ORIGINAL_CREATURE_ROSTER_DRAFT.md](creatures/ORIGINAL_CREATURE_ROSTER_DRAFT.md).
- [ ] Revise/accept the provisional input data before drawing balance conclusions.
- [ ] Compare Candidate B c=100 and c=143 using the same original-creature fixture and existing full-band integer-floored gates.
- [x] Add a reproducible neutral Power-80 single-attacker screen across all 25 creature pairings at c=100 and c=143. This is a diagnostic only, not match TTK.
- [ ] After human review, run bounded manual battles and broader matchup/pacing analysis; clearly separate formula diagnostics from player-facing feel.
- [ ] Specify effective-stat ownership, physical/special stat pairs, modifier order, floor points, minimum damage, immunity, and RNG boundaries.
- [ ] Record a recommendation and limitations. Do not auto-select a formula or offset.

**Exit criteria:** a human-reviewed original input set, reproducible comparison outputs, and an explicit damage contract sufficient for the next rules-design step. D-022–D-025 remain provisional/limited as recorded; no final formula or offset is selected by this plan.

## Gate 2 — Priority 2: Minimum coherent battle rules

- [ ] Resolve D-021 effectiveness comparison scope, including non-damaging, multi-target, and cross-target cases; ensure the ordering contract is transitive.
- [ ] Specify the minimum action vocabulary and legal target patterns for the first playable match.
- [ ] Resolve queued-action invalidation and whether/how an action can be interrupted or redirected.
- [ ] Define simultaneous damage and mutual-knockout semantics.
- [ ] Specify end-of-turn effects, replacement, and victory-check ordering for relevant edge cases.
- [ ] Preserve the confirmed five-registered / three-selected / two-active-plus-one-reserve arithmetic in D-003.

**Exit criteria:** two independent implementations can resolve the same accepted test turn and complete match to the same result.

## Gate 3 — Pure battle-domain vertical slice

- [ ] Implement accepted battle state, definitions, validation, and deterministic turn resolution in engine-independent code.
- [ ] Keep damage, reserve selection, and encounter victory behavior behind explicit pure interfaces/policies.
- [ ] Add tests for legal/illegal commands, target revalidation, KO timing, reserve deployment, victory, draws, and deterministic replay.
- [ ] Add the minimum player/commander action set; do not import a large action catalog before the rules require it.
- [ ] Validate a complete local match through a deterministic CLI before adding presentation.

**Exit criteria:** a complete match runs without Unity objects, scene lifecycle, rendering, or frame updates; accepted rules are covered by regression tests.

## Gate 4 — Unity project baseline and presentation

**Requires explicit engine-project authorization.** The repository currently contains only bounded navigation candidates; it is not a Unity project.

- [ ] Confirm Unity editor version and iOS/Android target baselines.
- [ ] Locate or create the actual Unity project root and establish a reproducible baseline commit.
- [ ] Import the accepted pure battle domain without introducing Unity dependencies into domain logic.
- [ ] Build a thin battle presentation layer that submits commands and renders returned state/events.
- [ ] Implement touch-friendly controls, safe-area layout, feedback, and two-side local control.
- [ ] Compile and run the navigation candidate only after the complete reviewed domain source and a real Unity test scene are available.

**Exit criteria:** two local sides can complete an accepted match through the mobile-oriented Unity UI, with tests and editor version recorded.

## Gate 5 — Initial content and production readiness

- [ ] Add the approved minimum content set: two commanders, two main weapons, and six distinct monsters with movesets.
- [ ] Store balance-sensitive definitions in data assets and validate them against the same domain rules.
- [ ] Establish save/load, content validation, scene transitions, and mobile performance baselines only as required by the playable loop.
- [ ] Run a complete end-to-end playtest before broad world, quest, cinematic, or multiplayer production.

**Exit criteria:** the core battle loop is playable end-to-end, content changes do not require editing resolution code, and the human accepts the milestone.

## Parallel-work policy

- Navigation remains a bounded parallel prototype and does not reorder the canonical priority list.
- Art-reference curation may proceed independently; production asset creation should follow approved art-direction constraints.
- Parallelize independent research and test work. Keep one integration owner for shared source, fixtures, decisions, and CI.
- Every work package needs an observable deliverable, exact scope, dependencies, acceptance checks, and stop conditions.

## Constraints

- Do not promote fixture assumptions or experiment outcomes into game rules without explicit human acceptance.
- Do not expand the battle action model or broad world systems ahead of the canonical priority gates.
- Keep pure game rules independent of Unity APIs.
- Do not claim Unity compilation or Play Mode verification until those checks are actually run.
- Keep `PROJECT_STATUS.md` as the only canonical project-wide priority order.
