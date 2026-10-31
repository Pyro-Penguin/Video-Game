# Painterly Folklore — Unified Runtime Art Direction

**Status:** Provisional architecture proposal incorporating the creative director's latest direction. This is not a production build rule or a final art bible.

## Direction

The target is **sleek, cool, stylized painterly 3D**. Avoid exaggerated chibi proportions, toy-like bodies, oversized heads, and thick cartoon outlines. Characters should feel agile, elegant, and grounded in a distinctive fantasy world. Their readability comes primarily from silhouette, pose, proportion, value grouping, animation, and restrained color—not from cartoon exaggeration.

Painterly Folklore remains the leading visual identity, but real-time painterly 3D on mobile is unproven. Prove that central rendering approach before adding techniques borrowed from unrelated styles. Cohesion is a higher priority than collecting visual tricks.

## Core architecture decision

**Use one shared stylized character-rendering pipeline for both customization and gameplay. Do not build a high-fidelity PBR creator plus a second gameplay bake pipeline by default.**

The creator and gameplay should use the same character assets, material model, shader family, and appearance data. The creator may present the character with a dedicated turntable, controlled studio lighting, a higher-quality render scale, and restrained post-processing. These are presentation settings—not a second asset pipeline.

This avoids maintaining two versions of every hair piece, face feature, armor piece, and material, and avoids a converter whose job is to make two representations match.

A bake may be reconsidered only if profiling later demonstrates a concrete need and a measured prototype shows a net benefit that justifies its content and maintenance cost. It is not part of the baseline architecture.

## Product-first visual test: six combatants

The game's defining visual load is not a lone avatar. It is a hero plus two creatures per side: **six characters visible in a mobile battle scene**. The creature roster and its growth over time determine the real content and runtime budget.

The first art prototype must include:
- One hero and two distinct creatures on each side.
- Six distinct silhouettes, with different body plans and readable roles.
- At least two contrasting elemental identities represented through shape language, palette accents, and restrained VFX—not color alone.
- Idle, locomotion, attack, hit reaction, and defeat/recall poses sufficient to test silhouette and animation readability.
- A painterly environment with foreground/background detail, so separation is tested against the intended visual density.
- The actual battle camera, framing, target phone aspect ratio, and realistic character screen-space height.

The scene must remain legible when all six characters act or overlap. Test status indicators and targeting selection without relying on tiny text.

## Proportions and silhouette

Do not use 1:3 chibi as the default. It conflicts with the desired sleek aesthetic. Do not infer a final proportion from 2D/2.5D side-scrolling references; translate only high-level principles such as graceful shape flow, atmospheric composition, and restrained detail.

Create three genuinely distinct proportion boards:
1. **Sleek heroic:** smaller head, longer limbs, narrow/athletic massing, clear equipment silhouette.
2. **Stylized heroic:** moderately enlarged hands/feet and facial features for mobile readability, without toy-like proportions.
3. **Creature-led stylization:** varied species-specific body plans; no universal human proportion ratio imposed on creatures.

Evaluate hero and creatures independently. A creature may need a large head, broad shell, long neck, or unusual limb arrangement to communicate its identity. Do not force every creature into the hero's proportion system.

Pass criteria at battle-camera scale:
- Facing and action are identifiable at a glance.
- Silhouette remains distinct in grayscale.
- Creature identity is not dependent on fine texture or color alone.
- Equipment and elemental cues remain readable without obscuring anatomy.
- The hero is visually important but does not overwhelm the creatures.

## Rendering hypothesis

First test a single coherent stylized 3D material/shader family that supports:
- Hand-authored base color and value grouping.
- Controlled roughness/specular response; avoid photorealistic PBR as the visual target.
- Soft painterly lighting transitions and atmospheric depth.
- Stable material response across the world, hero, and creatures.
- Optional vertex color or baked environment contribution where it supports the look and reduces cost.

Do not assume vertex lighting alone guarantees performance. Measure GPU time, CPU time, draw calls, material count, texture memory, overdraw, transparency, skinning, animation, and thermal behavior. Do not claim 60 FPS or battery benefits without device measurements.

The initial prototype should use one primary lighting model and avoid layering a separate cel-shaded look on top. A subtle per-character outline may be tested as an isolated A/B option only if the unoutlined character fails readability. Full-screen edge detection is not the starting point.

The Gauntlet and ancient technology may eventually use a restrained emissive accent, but do not add a hard-surface visual language until the base world/character combination feels cohesive. If tested, emissive state must remain readable in daylight, overcast, dusk, and low display brightness.

## Character and creature content architecture

### Persistent definition

A versioned, engine-independent definition owns:
- Stable character/creature ID.
- Species/body-plan or hero body preset.
- Proportion and silhouette preset.
- Face, hair, markings, and palette selections where applicable.
- Equipment and cosmetic IDs.
- Animation-set and material-profile IDs.
- Elemental identity and gameplay stats as separate data domains.

Appearance data must not own gameplay stats, battle state, or engine-specific shader objects. Creature species identity, elemental typing, and combat role must not be encoded only in textures or color.

### Runtime representation

- Reuse the same approved mesh, rig, material family, and appearance data in creator and gameplay.
- Creator presentation owns its turntable camera, studio lighting, preview framing, and temporary UI state.
- Gameplay character views own spawned mesh/rig/material instances and animation state for the life of the spawned actor.
- A pure customization validator checks stable IDs and compatible combinations before the view is updated.
- UI and character views communicate through data and narrow interfaces/events; avoid bidirectional scene-object references.

No atlas bake, high-poly/PBR twin asset, or runtime conversion service is required for the baseline.

## Roster-scale content budget

The asset budget must scale with the planned number of creatures, not with the number in the first prototype. Before production content expansion, define:
- Target creature count per village/element and total launch roster.
- Number of shared base rigs/body plans versus unique rigs.
- Animation set per rig archetype and required unique creature animations.
- Material slots and texture resolution tiers.
- Reuse policy for accessories, markings, VFX, and locomotion.
- Maximum simultaneous animated characters and VFX density in battle.
- Low/mid/high device tiers and memory/frame-time budgets.

Prefer a small set of high-quality reusable rig archetypes where anatomy permits, with bespoke rigs only when the silhouette or motion language genuinely requires them. Avoid a one-rig-fits-all rule that erases creature identity.

## AI-assisted content pipeline

The intended content pipeline is AI-assisted and budget-conscious; do not assume outsourced artist capacity unless the project explicitly adopts that model.

1. **Data generator:** produces schema-validated, versioned JSON for creature/character identity, body plan, proportions, palettes, rig profile, animation needs, and stats. It does not output shaders or textures.
2. **Prompt writer:** turns approved design data into original visual briefs and prompts. Describe properties such as sleek silhouette, elegant proportions, painterly brush texture, atmospheric value grouping, restrained material response, and readable elemental motifs. Do not request imitation of a named living artist or reproduce a reference composition.
3. **Asset validator:** checks measurable metadata and project conventions. It should report texture dimensions/formats, channel usage, material/shader identifiers, normal-map use, material-slot counts, rig/animation references, and folder/profile violations. Do not pretend metadata validation can judge artistic quality.

Separate creator presentation settings from gameplay runtime restrictions only where the same shared assets genuinely need different quality settings. Do not create duplicate creator/gameplay asset classes merely to satisfy a validator.

## Prototype plan: prove the core style first

Build one representative scene before making a production pipeline decision.

### Scene contents
- Six combatants: hero + two creatures per side.
- One painterly 3D environment.
- One shared stylized shader/material family.
- Actual battle camera and mobile aspect ratio.
- Representative animation and modest battle VFX.
- No creator/gameplay bake.
- No mandatory outline; test it as a separate optional variant.

### Capture variants
- Three proportion/silhouette options, including the sleek option as the leading candidate.
- Same camera, pose, lighting, and environment for fair comparisons.
- Neutral lighting and one warm/cool lighting comparison.
- With and without a subtle per-character outline only if needed.
- Phone-size screenshots and short motion captures.

### Measurements
On an older mid-range Android target, record:
- Device model, SoC/GPU, OS, resolution, and graphics API.
- Average, 95th percentile, and worst sustained frame time after warm-up.
- CPU and GPU frame time separately where tooling permits.
- Draw calls/batches, material count, triangles/vertices, skinned mesh count.
- Texture and render-target memory.
- Transparent overdraw/fill-rate observations.
- VFX and animation cost with all six characters active.
- Thermal behavior after a sustained run, not only a short cold start.

Do not invent universal pass thresholds before the device floor and target frame rate are chosen. First collect a baseline and identify the dominant bottleneck; then set explicit acceptance budgets.

## Ownership and communication

- **Character/Creature Definition:** pure versioned data; persistent save/content lifetime.
- **Customization validator:** pure logic; invoked when choices change or a character is loaded.
- **Creator presentation adapter:** owns preview camera, lighting, and UI-only state; creator session lifetime.
- **Gameplay character view:** owns spawned render/animation objects; actor lifetime.
- **Asset validator:** build/content pipeline; no runtime ownership.
- **Communication:** data transfer and narrow interfaces/events. The definition is authoritative; presentation never writes gameplay state back into it.

## Decisions intentionally deferred

- Exact head/body proportions and species-specific rig taxonomy.
- Unity render pipeline, shader implementation, and graphics API.
- Texture dimensions, compression formats, material-slot caps, and normal-map policy.
- Outline implementation and whether outlines are needed at all.
- Emissive Gauntlet/ancient-tech treatment.
- Device floor, frame-rate target, and numeric performance budgets.
- Total launch creature count and animation counts.
- Any bake/atlas conversion; reconsider only with measured evidence.

The next decision should come from the six-combatant mobile prototype, not from further style taxonomy. Keep this art work parallel to, and subordinate to, the battle-rules milestone.
