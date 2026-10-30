# Developer Handoff

## Project
Original creature-collecting RPG with tactical PvP ambitions. Long-term target platform is mobile (iOS/Android). No Unity project exists yet; current work is engine-independent design consolidation and mechanics experimentation.

## Mandatory Startup
Read [COLLABORATION_PROTOCOL.md](COLLABORATION_PROTOCOL.md) first, then follow its startup sequence. The repository is the shared project memory; conversations are temporary workspaces.

## Source of Truth
- [Project Index](PROJECT_INDEX.md)
- [Project Status](PROJECT_STATUS.md) — canonical project-wide priorities.
- [Decision Log](docs/DECISION_LOG.md) — authoritative durable decisions.
- [Open Questions](docs/OPEN_QUESTIONS.md) — unresolved questions grouped by canonical priority.
- [Game Overview](docs/GAME_OVERVIEW.md)
- [Battle Overview](docs/battle/BATTLE_OVERVIEW.md)
- [Battle Format Decision Framework](docs/battle/BATTLE_FORMAT_DECISION.md)
- [Stat System Research Plan](docs/STAT_SYSTEM_RESEARCH_PLAN.md)
- [Damage Model](docs/battle/DAMAGE_MODEL.md)
- [Damage Equation Decision Brief](docs/battle/DAMAGE_EQUATION_DECISION_BRIEF.md)
- [Damage Equation Comparison Experiment](experiments/damage_equation/README.md)
- [Proposed Endgame Stat-Range Sensitivity Experiment](experiments/stat_range_sensitivity/README.md)
- [Stat-Range Sensitivity Results](experiments/stat_range_sensitivity/RESULTS.md)
- [Damage RNG Experiment](experiments/damage_rng/README.md)

## Completed
- Structured fragmented concepts into referenceable documents.
- Preserved contradictions and unknowns rather than inventing resolutions.
- Implemented the standalone Python damage RNG experiment with six models.
- Recorded the prior local test result: 6 tests passed.
- Added a GitHub Actions workflow to run the experiment tests on Python 3.10–3.13 and smoke-test JSON report generation. CI verified: all four Python-version jobs passed, including unit tests and JSON report generation.
- Added battle-format decision framework and stat-system research plan.
- Added collaboration protocol and reconciled the canonical priority order; see D-014.

## Current Work State

**Expanded damage experiment:** CI run [41094836607](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41094836607) passed all seven jobs. Its artifact was downloaded and inspected: 825 all-vs-all rows, 2,695 single/combined-stat rows, 35 level rows, and 4,125 raw/floored pairwise candidate comparisons. [RESULTS.md](experiments/stat_range_sensitivity/RESULTS.md) was updated from this artifact. Subsequent documentation, status, and index updates passed all seven jobs in [41095218936](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41095218936).

**Review-package verification:** CI run [41097941386](https://github.com/Pyro-Penguin/Video-Game/actions/runs/41097941386) tested commit `1ca7ddca3d8460058220ad2b5ffa8c5309c0923a` and passed all seven jobs, including documentation validation, damage equation, stat-range sensitivity, and the four-version damage RNG matrix. This handoff refresh is documentation-only and triggers a follow-up CI run; check that run before marking this exact handoff commit Tested.

## Expanded experiment findings

- The Level-100 comparison uses a shared 60-damage calibration at Power 100 / Attack 300 / Defense 275. The first 50-damage anchor yielded 7 hits against Vitality 350 and conflicted with the provisional 4–6 target; D-016 records the corrected 60 anchor as Provisional, with explicit revisit conditions.
- Candidate B offsets c=100, 143, 200, and 400 pass the current provisional neutral TTK, 2:1 specialization, and no-full-HP-one-hit numeric gates. No offset is selected.
- c=143 preserves c=100's floored matchup ordering most closely among tested alternatives (1.62% of matchup-pair orderings change); c=400 compresses more but changes ordering more (17.19%).
- Flooring changed 439/4,125 pairwise relations: 122 raw ties became strict floored relations, 317 strict raw relations became ties, and zero strict order reversals occurred.
- Direct level scaling causes severe low-level TTK when endgame derived stats are held constant. The Level-1 result is not a story prediction; it isolates sensitivity to the direct level term.
- Combined-stat interaction residuals: 1,320 evaluated; 660 raw-damage residuals nonzero (max 5 percentage points); 721 floored-TTK residuals nonzero (max 2 hits). The ±1-hit concept was specified to use floored TTK but was not established as a numeric acceptance gate; if adopted as an isolated-stat screen, combined residuals require a separate tolerance. The 5 pp raw / 2-hit floored maxima are threshold-sensitive, not unrelated effects.
- Flooring changed 439 pairwise relations: 122 ties split into strict orderings, 317 strict orderings merged into ties, zero strict reversals; flooring more often collapses distinctions in this sample.
- The Generation IX deterministic base-damage implementation is a reference harness only, not a fifth candidate; it uses the integer level term (including at Level 1) and excludes external modifiers.
- Provisional preferences and gates live in the Damage Equation Decision Brief. They are not game rules or Decision Log entries.

## Highest-Priority Next Work
1. Conduct the one-sitting design review using [Damage Equation Design Review](docs/battle/DAMAGE_EQUATION_DESIGN_REVIEW.md). Resolve the scope of the proposed ±1 isolated-stat screen versus the separate combined-stat residual tolerance; select or reject an offset and level path; use the explicit exit criteria.
2. Hold the expanded experiment. Run a third pass only if the team says current stat ranges or progression-derived stats are inadequate, and scope it to the specific missing range or progression gap. No broad sensitivity pass by default.
3. Carry the historical **150 maximum base Speed** into the pre-registered speed-tier review. It is not an accepted cap. State the assumed allocation model (provisional 70 total / 30 per stat), accept/revise the proposed cluster definition (>2 distinct builds within ±5% of a decisive threshold), and keep priority-mechanic design separate from Speed analysis.
4. After damage-equation resolution, continue battle structure/resolution. This experiment does not decide active/reserve, commander, simultaneous-selection, or turn-resolution rules.
5. Do not create further game-rule Decision Log entries until the human explicitly accepts the decisions.

No final damage formula, stat range, story-level scaling policy, TTK rule, or RNG model has been selected.

## Engineering Guardrails
- Keep authoritative rules in pure, testable C# where practical once engine implementation is authorized.
- Unity components adapt input and presentation; they do not own core rules.
- Prefer composition and explicit ownership.
- Communicate across boundaries through commands, events, and narrow interfaces.
- Keep balance-sensitive data outside resolver logic.
- Avoid per-frame allocations and LINQ in hot paths.
- Test match logic without loading a Unity scene.

## Do Not Assume
- Exact Unity version or that Unity has been installed.
- That a complete Unity project exists.
- That unresolved battle rules have been approved.
- That any source archive may be modified.
- That the RNG experiment selects a final damage model.
