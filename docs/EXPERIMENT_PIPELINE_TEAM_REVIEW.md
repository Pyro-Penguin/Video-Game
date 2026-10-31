# Team Review: Analytical Experiment Pipeline

**Status:** Initial team findings have been re-audited against current main and corrective work is being applied. This document is an audit checklist, not an approved game-rule specification.

## Scope boundary

The repository is a design/documentation workspace plus three standard-library Python experiment packages. It is not a Unity project. There is no C# engine, MonoBehaviour lifecycle, mobile runtime, gameplay hot path, or touch-latency surface to audit.

The current code is offline analytical tooling:
- exact-arithmetic damage-model comparison;
- RNG-model enumeration and seeded simulation;
- a sensitivity harness with pre-registered gates.

For the current repository, review analytical correctness, gate validity, reproducibility, and maintainability. Runtime architecture and mobile performance become applicable only when a runtime is deliberately introduced. Python `Fraction` is an experiment oracle, not a runtime implementation candidate; any future C# port needs an explicit fixed-point/integer arithmetic contract.

## Reviewed data flow

### `experiments/damage_rng/damage_rng.py`

- `RNGModel` defines six roll models: fixed 100, fixed 95, uniform 95–105, 90–110, 85–105 raw, and 85–105 normalized.
- `calculate_damage` applies roll, normalization, STAB, and effectiveness using exact `Fraction` arithmetic, floors once, and clamps damage to at least 1.
- `exact_damage_outcomes` enumerates rolls for single-hit KO probability.
- `simulate_hits_to_ko` samples repeated hits with a seed.
- `build_report` serializes models, KO probabilities, and simulation summaries to JSON.

### `experiments/damage_equation/damage_equation.py`

- Four candidate equation families A–D, calibrated to 50 damage at P=100/A=100/D=100/L=50.
- Sweeps synthetic stat scales, levels, powers, and attack/defense ratios; writes JSON.

### `experiments/stat_range_sensitivity/stat_range_sensitivity.py`

- Five attacker/defender profiles, three Vitalities, four candidates (Candidate B swept over eight offsets).
- `make_matchups` builds a 25-pair × 3-vitality × candidate matrix at reference power/level.
- `combined_perturbations` computes single, pair, and triple stat perturbations and interaction residuals.
- `calibration_and_gates` applies neutral TTK, 2:1 specialization, one-hit KO, and monotonicity gates.
- `rank_flip_audit` and `pairwise_rank_flip_audit` compare raw versus floored candidate ordering.
- `offset_cross_matchup_rank_stability` compares each Candidate B offset with c=100 across 75 coordinates.

## Findings ranked by impact

### P0 — Specialization gate samples only one Defense coordinate

**Root cause:** `calibration_and_gates` computes the 2:1 specialization ratio at Attack 600 / Defense 300 versus Attack 300 / Defense 300. It does not sweep the intended Defense band.

**Known counterexamples supplied by the team:** Candidate B c=400 produces:
- Defense 200 / Attack 400: 800/600 = 1.333×;
- Defense 250 / Attack 500: 900/650 = 1.385×;
- Defense 300 / Attack 600: 1000/700 = 1.428×.

Thus the single-point check reports a pass at Defense 300 while the proposed 1.4× minimum is violated at Defense 200 and 250.

**Impact if unaddressed:** A candidate that fails the design intent across a meaningful portion of the Defense band can be advanced.

**Required correction:** Sweep Defense values (proposed: 200, 250, 300, 350), calculate best- and worst-case ratios, and gate on the worst case. The team proposes the full band 1.4×–1.8×, with a regression test proving c=400 fails at Defense 200 and 250. The band and thresholds remain experiment criteria, not approved game rules.

**Verification target:** independently recompute all four Defense coordinates and test a known-bad candidate. This is the sole listed change expected to alter which candidates survive the current specialization gate.

### P1 — POWERS is defined but not swept by the sensitivity harness

The team reports `POWERS = (40, 80, 100, 120, 160)`, while `make_matchups`, `combined_perturbations`, and `level_sweep` use only reference power 100.

**Correction:** either implement the intended power sweep in all relevant tables or remove the unused constant and explicitly document that move-power sensitivity is outside this experiment. Do not imply coverage that the report does not contain. A second reviewer suggested demoting this from P0 to P1 because it is a coverage/documentation mismatch, not the sole known design-conclusion-changing defect.

### P1 — Interaction residual is not a single-stat TTK shift

The current `interaction_ttk_residual_hits` is:

`combined floored TTK - baseline TTK - sum(single-control floored TTK - baseline TTK)`

This is a combined-versus-additive interaction residual, not the TTK shift caused by one isolated stat perturbation. Multiplicative formulas can produce a nonzero interaction residual even when individual perturbations do not change TTK.

**Correction:** rename the field to `interaction_ttk_delta_vs_additive`. Add a separate single-stat TTK-shift table grouped by perturbation size. Team-reported rates of isolated rows exceeding one hit are 0/330 at ±5%, approximately 0.9% at ±10%, and 22.7% at ±20%. Treat these as reported figures pending recomputation; no ±1-hit acceptance threshold should be implied unless explicitly pre-registered.

### P1 — Candidate C calibration is duplicated and opaque

The team reports that `damage_equation.py` hardcodes `Fraction(25, 23)` to force Candidate C to 50 baseline damage, while the sensitivity experiment derives Candidate C by ratio against the reference anchor.

**Correction:** derive the calibration from the baseline expression and share candidate functions between experiments. First verify whether both current paths produce identical baseline and sweep values; if they do, this is latent drift risk, and if not, it is an active inconsistency.

### P1 — Rank-stability audit rebuilds slices and assumes complete coordinate coverage

The team reports that `offset_cross_matchup_rank_stability` repeatedly constructs `list(baseline)[i + 1:]` inside nested loops and assumes every offset has every baseline key.

**Correction:** materialize baseline keys once, validate key-set parity before comparison, and use `itertools.combinations`. Apply the same approach to `pairwise_rank_flip_audit`. Raise a clear data-integrity error if coordinate coverage differs rather than leaking a `KeyError`.

### P2 — Candidate B offset scope differs between experiments

The team reports `damage_equation.py` uses `OFFSET_C=100`, while the sensitivity experiment tests `B_OFFSETS = (0, 25, 50, 100, 200, 400, 71, 143)`.

**Correction:** either parameterize both over the same set or explicitly document their different scopes. Otherwise readers comparing reports see different Candidate B results without an explanation.

### P2 — Tests do not test known design failures

The current tests reportedly verify calibration and that c=100 passes, but do not assert known-bad candidates fail.

**Required regression coverage:**
- Candidate B c=400 fails the 1.4× floor at Defense 200 and 250.
- Candidate C at 2:1 fails the proposed 1.4×–1.8× band (team cites a Generation IX reference ratio of 1.977×; verify harness comparability before using this as a regression).
- The renamed interaction metric is zero for a purely additive model and nonzero for a multiplicative model.

Tests should validate discrimination and intended semantics, not only repeat calibration assertions.

## Maintainability and reporting

- Move shared experiment parameters (reference damage, B offsets, Defense band, powers, levels) into one JSON/TOML configuration consumed by code and tests.
- Generate prose counts and summaries from machine-readable reports where practical; avoid manual duplication and stale counts.
- Add Python ignores such as `__pycache__/` and `*.pyc` to `.gitignore`.
- Decide whether committed `report.json` files are intentionally versioned review fixtures. Otherwise publish generated reports as CI artifacts rather than tracked outputs.
- The team reports a stale six-test count in `PROJECT_STATUS.md` versus 28 tests. Verify the actual current suite before changing the status count.
- Record exact experiment configuration and source revision alongside every report so results can be reproduced.

## Performance and future port

These are offline tools; GC pressure and frame time are not current concerns. Avoidable costs include repeated O(n²) list slicing and unnecessary full materialization of row lists.

For a future runtime, do not port Python `Fraction` directly into gameplay. Define a deterministic fixed-point/integer representation (the team suggests a denominator such as 1024 as one candidate), rounding order, overflow bounds, and test vectors. Precomputation may be appropriate for bounded matchup tables. This is future design guidance only.

## Prioritized action list

1. Fix the specialization gate to sweep Defense and add the c=400 regression. **Only listed item that can change current candidate survival.**
2. Resolve the unused `POWERS` dimension: sweep it or remove it and state the limitation.
3. Rename/re-scope the interaction residual and add isolated single-stat TTK shifts.
4. Deduplicate Candidate C and derive calibration from its baseline expression.
5. Replace repeated slices with `itertools.combinations` and validate key parity.
6. Unify or document Candidate B offset scope.
7. Centralize experiment parameters and reduce manually copied report numbers.
8. Add Python `.gitignore` entries and decide report artifact policy.

## Reviewer agreement and qualifications

A second team review endorsed the analytical diagnosis and prioritization, with these refinements:
- Keep the unused `POWERS` finding at P1 unless documentation explicitly claims a complete multidimensional sweep.
- Verify whether Candidate C's two current calibration paths are numerically identical before describing the issue as active.
- State the observable offset-report consequence explicitly: side-by-side reports show different Candidate B scopes without explanation.
- Add a concise verification subsection listing the Defense values and ratios recomputed.
- The analytical core is considered disciplined (exact arithmetic, seeded simulations, explicit limitations, separation of experiment from game rules); the gate layer needs to become genuinely discriminative.

## Verification status

This file records the team's supplied review. The repository source, test suite, report artifacts, and CI results must be inspected before any finding is marked independently verified or any code change is made. No damage formula, stat range, RNG model, or game rule is selected by this review.


## Follow-up audit against main at 178a7d3

- P0 Defense band: The supplied report was stale relative to current main. DEFENDERS already contained five distinct values (200, 250, 275, 300, 350), including 300. The correction strengthens this with an explicit DEFENSE_BAND loaded from config, import-time uniqueness validation, and specialization coordinates generated independently of named matchup profiles.
- Shared candidate functions: Both experiments use the same four mathematical families but had separate implementations and calibration anchors. This is a latent drift defect. The fix centralizes raw A-D functions and calibration in experiments/common/damage_candidates.py; each experiment supplies its own explicit anchor. Candidate B offsets are swept in both experiments.
- TTK residual: interaction_ttk_residual_hits was a combined-versus-additive interaction, not an isolated single-stat shift. It is renamed interaction_ttk_delta_vs_additive; isolated shifts are emitted in a separate table.
- Generation IX floor placement: The proposed sequential expression is mathematically equivalent to the existing combined denominator floor for positive integers: floor(floor(n / D) / 50) = floor(n / (50D)). The implementation is made explicit and regression-tested; no numerical correction is expected.
- Log residual semantics: The supplied test description had its meaning reversed. A multiplicatively separable function produces zero log interaction residual; a non-separable function generally produces a nonzero residual. Tests discriminate those behaviors.
- Configuration and project hygiene: Reference anchors, Defense band, specialization bounds, and Candidate B offsets are moved into configuration; root pyproject.toml and Python .gitignore are added.
- Remaining separate review item: POWERS is still a declared report dimension but is not swept by the sensitivity harness. The README/report describe Power 100 as the ordinary reference, so this remains a coverage limitation, not a claimed power sensitivity sweep; resolve separately before claiming power sensitivity coverage.

No damage formula, RNG model, stat range, or game rule is selected by these engineering corrections.
