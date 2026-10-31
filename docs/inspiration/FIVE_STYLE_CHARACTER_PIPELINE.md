# Painterly Folklore: Five-Style Integration and Character Pipeline

**Status:** Provisional architecture proposal. This document translates the supplied five-style synthesis into testable production constraints. It does not approve a renderer, shader, engine version, character ratio, texture budget, or final art direction.

## Executive decision

Use **Painterly Folklore** as the primary visual identity. Treat the five mobile styles as specialist techniques with bounded responsibilities rather than five competing global styles:

| Style family | Proposed role | Adoption status |
|---|---|---|
| Clean cel-shaded anime | Selective silhouette/edge readability and restrained gradient accents | Provisional; do not adopt its global hard cel bands or anime rendering language |
| High-readability stylized proportions | Character and creature silhouette readability at mobile camera distance | Provisional; test 1:3, 1:4, and an elongated-limb/smaller-head alternative |
| Dark-fantasy PBR | Character-creator presentation only | Provisional; constrain scope and profile performance |
| Neo-retro low-poly / vertex-lit | Runtime environment and character-lighting cost strategy | Provisional; validate on target devices; not a blanket ban on dynamic lighting |
| Stylized hard-surface / emissive tech | Gauntlet, ancient mechanisms, and selected UI-adjacent objects | Provisional; isolate emissive masks and preserve painterly material contrast |

The world remains painterly, atmospheric, and shape-led. The character pipeline may be more graphic for legibility, and the Gauntlet may be deliberately technological. These contrasts must feel authored as one world through shared palette, value hierarchy, material response, and shape language.

## Character pipeline: proposed stages

### 1. Authoritative character definition

**Owner:** Character data model and customization domain, not the renderer.

Persist semantic customization data: body preset, proportions preset, face/hair choices, palette choices, equipment identifiers, and any supported blend parameters. Keep gameplay stats and identity separate from appearance data. Use stable IDs and versioned data so a character can be re-created after content updates.

Do not store generated shader state, transient render targets, or platform-specific GPU resources as character identity.

### 2. Creator presentation

The creator may use a richer material and lighting setup than gameplay. PBR and a restrained skin response are candidates, not requirements. Prefer a controlled studio lighting rig and a representative range of skin/material presets over unrestricted real-time lights.

Do not assume high-poly meshes or true subsurface scattering are necessary to deliver a satisfying creator. A well-authored low/medium-poly base mesh, layered materials, and carefully designed lighting may achieve the required customization quality at lower cost.

Creator-only assets and shaders must live in an explicitly scoped creator content group. Opening the creator may load that group; leaving it should release creator-only render targets/material variants where practical. Character customization data survives; transient presentation resources do not.

### 3. Bake / gameplay representation

The bake is a conversion from semantic customization data to a gameplay representation. It is not automatically a conversion from a fully lit PBR image into a universal albedo map.

**Preferred first implementation hypothesis:** retain a simplified, animatable 3D mesh and rig; bake or compose appearance into a compact material atlas; preserve lighting response through a small runtime material model. This keeps camera rotation, equipment visibility, animation, and silhouette changes possible.

A 2D impostor may be useful for distant NPCs or preview thumbnails, but should not be the default player representation while the camera can orbit or the character must animate in combat.

Separate material information that must remain dynamic (e.g. emissive Gauntlet seams, selected metal response) from appearance that can be baked. Avoid baking one scene's directional lighting into base color unless the resulting flat look is intentional and tested under day/night changes.

The conversion should be deterministic from versioned customization data and content assets. Cache the resulting atlas by a stable content hash. Rebuild only when customization or source assets change, not every time the player enters the world. Define fallback behavior if a bake fails or the cache is invalid.

**Unresolved:** whether baking occurs in an editor/content pipeline, on first character creation, or on-device after customization. On-device baking must be profiled for latency, memory spikes, and thermal impact before adoption.

### 4. Gameplay silhouette and proportions

The 1:3 ratio is a useful candidate, not a locked requirement. It is strongly chibi; the accompanying elongated-limb/small-head description may point toward a less extreme proportion. Compare at least:
- 1:3 head-to-total-height ratio.
- 1:4 ratio.
- An elongated, smaller-head variant with enlarged hands/feet/equipment for readable pose language.

Evaluate at actual battle-camera scale on a narrow six-inch-class phone viewport. Test front, side, three-quarter, movement, attack, damage, and equipment silhouettes. The pass condition is not “cute”; it is that facing, role, equipment, action, and state remain readable without relying on tiny detail.

### 5. Edge treatment

Do not begin with full-screen edge detection. It can outline background texture, foliage, particles, and UI, adding noise and mobile post-processing cost.

Prototype a per-character outline first (inverted hull or material/vertex-based edge treatment). Make thickness stable in screen space where possible, but test perspective and animation artifacts. Use the outline selectively: important characters and interactables should separate from the background without becoming sticker-like.

Gradient hair tips and edge accents may use palette anchors such as Midnight Indigo (#2A2354) and Amber (#E88B3A), but these are candidate colors, not universal material rules.

### 6. Gauntlet and ancient technology

Treat the Gauntlet as a high-contrast hard-surface object that can bridge puzzle interaction, traversal, and diegetic UI. Cyan emissive (#1ECBE1) is a candidate accent. Use emissive masks for controlled seams, glyphs, and state feedback; avoid making every surface glow.

The Gauntlet should remain visually distinct from the painterly world through geometry, value contrast, and restrained emissive response—not by importing an unrelated full-screen sci-fi UI language. Keep puzzle-critical state readable in grayscale and at low brightness.

## Runtime environment strategy

Vertex colors/lighting, hand-painted textures, baked ambient occlusion, and simplified material response are candidate runtime tools. They do not guarantee a frame rate by themselves.

The performance budget must account for:
- GPU fill rate and overdraw, especially foliage, particles, transparent effects, and outlines.
- Draw calls/material variants and texture memory/bandwidth.
- Mesh density, skinning cost, animation count, and CPU submission.
- Dynamic lights/shadows, post-processing, render resolution, and thermal throttling.
- Worst-case combat scenes and dense village scenes, not only an empty route.

Do not prohibit all dynamic shadows in advance. Prefer baked/static lighting for stable environment illumination; reserve dynamic lighting/shadows for cases where they materially improve gameplay or composition and pass device profiling.

**No 60 FPS claim is accepted yet.** Establish low/mid/high device targets, resolution policy, frame-time budgets, memory budgets, and thermal test duration before committing to a runtime lighting stack.

## AI-assisted content pipeline

Keep the three-agent division, but make every output deterministic and reviewable:

1. **Data generator:** emits schema-validated, versioned JSON for semantic character parameters and references stable content IDs. It does not emit shaders, texture files, or engine-specific code.
2. **Prompt writer:** converts approved data and visual briefs into artist prompts. Prompts should specify original high-level traits—painterly brush texture, atmospheric value grouping, stylized readable proportions, flat hand-painted surface treatment, controlled edge accents, and restrained emissive tech. Do not require direct imitation of named contemporary artists or reproduce reference compositions.
3. **Asset validator:** checks imported assets against a versioned profile by folder/asset role. It should validate measurable metadata, not infer quality from vague labels.

### Validator profiles

Use separate profiles so creator exceptions do not weaken gameplay restrictions:

- **Gameplay character/environment:** allowlisted runtime shaders/material features; texture dimension and format caps; explicit normal-map policy; bounded material slots; no creator-only shader dependencies; controlled emissive usage.
- **Creator-only:** explicitly allowlisted richer material features and creator-only dependencies; separate memory and load profile.
- **Gauntlet/tech:** allowlisted emissive mask/channel and material variants; enforce restrained texture and material budgets.

A first validator can inspect import metadata and a small asset manifest. It should fail closed on unknown shader/material identifiers in restricted folders. Avoid brittle rules based only on shader display names. A “4K texture forbidden” rule should be a configurable numeric maximum per profile, not a hardcoded global assumption.

## Architecture ownership and lifetime

- **CharacterDefinition (pure data):** owns persistent appearance choices and schema version; lifetime is save/profile lifetime.
- **Customization service (pure domain):** validates choices and emits a versioned customization description; lifetime is creator/session scope.
- **Creator renderer (engine adapter):** owns creator-only materials, lights, and preview render targets; lifetime is creator scene/session.
- **Bake service (engine adapter behind interface):** converts a validated description plus content version into a cached gameplay appearance asset; lifetime is cache/content-version scope.
- **Gameplay character view (engine adapter):** owns mesh, rig, runtime material instances, and animation bindings; lifetime is spawned character instance.
- **Asset validator (build/content pipeline):** owns no runtime state; validates imported assets before they enter a build.
- **Communication:** pure data and stable IDs flow from customization to bake; an interface returns a bake result/cache key; events notify presentation when an appearance asset is ready. Avoid direct bidirectional references between creator UI, character view, and bake implementation.

## Prototype and falsification plan

Do not implement the full pipeline yet. Use one representative player character and one representative creature/NPC.

1. **Silhouette board:** render 1:3, 1:4, and elongated variants at actual mobile gameplay scale; include front/side/three-quarter and action poses.
2. **Material board:** compare painterly hand-painted runtime material, vertex-color/low-poly treatment, and the creator-only PBR presentation using the same character.
3. **Bake proof:** prove that a small set of customization parameters deterministically produces a simplified 3D gameplay character with preserved animation and equipment. Measure bake time, atlas dimensions, memory, and cache hit behavior.
4. **Outline proof:** compare no outline, per-character outline, and a restrained screen-space treatment at phone scale; reject any option that outlines busy background detail or shimmers during camera motion.
5. **Gauntlet proof:** test emissive-mask states in daylight, overcast, dusk, and low-brightness display conditions.
6. **Device profiling:** profile worst-case character count, foliage, transparency, and combat VFX on a low/mid-tier target device before setting frame-rate claims.

### Acceptance gates

- Character facing, pose, equipment, and action remain readable at mobile battle distance.
- The gameplay character remains animatable and visually coherent under camera rotation.
- The bake is deterministic, cached, and does not introduce recurring scene-entry stalls.
- Creator-only rendering resources are not loaded into normal gameplay scenes.
- Runtime asset validation distinguishes creator assets from gameplay assets and reports actionable failures.
- Performance targets are demonstrated on actual target hardware; they are not inferred from shader category names.

## Decision boundary

This proposal does not approve:
- A 1:3 or 1:4 proportion as canonical.
- Runtime on-device baking or a specific atlas resolution.
- True SSS, high-poly creator meshes, or any specific PBR shader.
- Full-screen edge detection or a specific outline implementation.
- A blanket ban on dynamic shadows or a 60 FPS guarantee.
- A Unity render pipeline, shader language, device tier, or final texture budget.
- A final palette or the supplied hex colors as universal material constants.

The art comparison board and prototype results should decide which techniques earn adoption. Keep this work parallel to, and subordinate to, the canonical battle-system milestone.
