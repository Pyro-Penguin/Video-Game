# Six-Combatant Mobile Rendering Spike — Test Specification

**Status:** Proposed experiment. No renderer, proportions, outline, device floor, or frame-rate target is approved.

## Question

Can one coherent, painterly stylized 3D rendering approach keep the hero and two creatures per side readable and performant on an older mid-range Android phone, without a separate creator/gameplay asset pipeline?

This is a rendering/content spike, not a production character system. Do not build the creator, bake service, asset validator, full elemental VFX suite, or a generalized creature framework for this test.

## Scope

### Required scene
- One hero and two distinct creatures for each side (six visible combatants).
- One representative painterly environment with foreground, midground, and background detail.
- The intended tactical battle camera, framing, and mobile aspect ratio.
- Representative idle, locomotion, attack, hit reaction, and defeat/recall animation states.
- A small amount of representative VFX; include an effect overlap case.
- Targeting selection and status indicators sufficient to test UI/readability.

### Explicitly out of scope
- PBR/SSS character creator.
- Runtime or offline PBR-to-gameplay bake.
- Full-screen edge detection.
- Final elemental type chart/VFX library.
- Production creature roster or final animation library.
- Networked multiplayer, AI opponents, or battle-rule implementation changes.

## Visual variants

Use the same camera, lighting, poses, environment, and output resolution for comparisons.

1. **Sleek heroic:** smaller head, longer limbs, athletic massing, elegant pose language.
2. **Stylized heroic:** modestly enlarged hands/feet and facial cues, but no toy-like chibi proportions.
3. **Creature-specific:** distinct anatomy/body plans; do not force creatures into one humanoid ratio.

The variants must be visibly different proportion studies, not minor slider changes. Test hero and creatures independently. Use grayscale captures to check silhouette separation before relying on color.

### Rendering A/Bs
- Primary shared stylized material/shader with no outline.
- Same scene with a subtle per-character outline, only as an optional comparison.
- Painterly environment with the same character setup.
- One neutral lighting setup plus warm and cool variants.

Do not add cel-shading bands, pixel-art skies, hard-surface emissive tech, or multiple stylistic systems to the baseline. The purpose is to test the coherence of the central style.

## Capture matrix

Capture stills and short motion clips for:
- All six characters idle.
- All six moving simultaneously.
- Two or more overlapping silhouettes.
- Target selection on each side.
- Attack VFX while multiple characters remain visible.
- Hit reactions and low-health/defeat states.
- Bright and dark environment values.
- Phone-native screenshot size and a zoomed-out battle-camera view.

## Performance measurement protocol

Record the exact device model, SoC/GPU, RAM, OS version, graphics API, screen resolution, render scale, quality settings, and build configuration.

After a warm-up period, capture:
- Average, 95th-percentile, and worst sustained frame time.
- CPU and GPU frame time separately where available.
- Draw calls/batches and material count.
- Triangles/vertices and number of skinned renderers.
- Texture memory and render-target memory.
- Transparent overdraw/fill-rate observations.
- Animation and VFX cost with six combatants active.
- Thermal behavior over a sustained session (at least 10 minutes).

Run the same scene with six animated characters, then with animation/VFX selectively disabled to isolate cost. Keep all capture settings identical across variants.

## Pass/fail method

Do not invent universal numerical thresholds before selecting the device floor and target frame rate.

The first run establishes a baseline. After inspecting the bottlenecks, set:
- Minimum supported device tier.
- Target frame rate and allowed frame-time variance.
- CPU/GPU frame-time budgets.
- Memory budget.
- Maximum simultaneous skinned characters and VFX density.
- Maximum texture/material budgets.

A visual variant fails if character facing/action/identity cannot be distinguished at battle distance, if silhouettes collapse under overlap, or if outlines/lighting make the scene noisier rather than clearer. A performance variant fails if it exceeds the subsequently approved budgets on the minimum target device.

## Deliverables

1. Side-by-side proportion board with six combatants and phone-size crops.
2. Short motion captures for all required action states.
3. Device and build configuration record.
4. Raw profiler captures and a summary table.
5. Bottleneck diagnosis and recommendation: retain, simplify, or reject each tested feature.
6. Explicit unresolved decisions; no unmeasured performance claims.

## Architecture constraints

- Character/creature identity and proportions remain data-driven.
- Shared gameplay/creator asset pipeline remains the default hypothesis.
- No new global manager or static service locator.
- Rendering and animation adapters own engine objects; pure identity/configuration data stays engine-independent.
- The spike must be disposable or evolvable into production without entangling battle-domain logic.

## Exit gate

The spike is complete when the creative director can choose a proportion direction from phone-scale evidence and the team has a measured baseline for six simultaneous combatants on the selected minimum device. Until then, do not freeze shader complexity, outlines, atlas sizes, device performance targets, or asset budgets.
