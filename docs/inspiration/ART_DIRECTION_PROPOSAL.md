# Proposed Art Direction: Painterly Folklore with Diorama Skies

**Status:** Proposed visual direction for review. Not yet human-accepted, production-approved, or a technical rendering specification.

## Executive assessment

The proposal has a coherent visual hypothesis: a tactile, painterly world as the primary visual language, with a deliberately separate pixel-art sky as a stylized atmospheric layer, and occasional high-energy travel vistas as short-lived transitions. Bob Ross landscape painting is a useful reference for readable environmental composition and atmospheric depth.

I recommend advancing this as a **prototype direction**, not declaring it a finished or market-ready art direction. The strongest idea is the hierarchy between readable gameplay space and expressive sky/transition layers. The weakest parts of the original review are its certainty about audience response, its fixed numerical value ranges, and its overly strict claim that pixel and painterly elements must never overlap.

## Proposed visual hierarchy

### 1. Gameplay world: painterly folklore

The explorable world should carry the dominant visual identity:
- Stylized, hand-authored forms with intentional shape language rather than photorealistic material detail.
- Broad, readable value masses and controlled texture density.
- Soft atmospheric depth, selective edge detail, and restrained highlights.
- Strong silhouettes for the player, companions, interactables, traversal routes, and combat-relevant objects.
- Whimsical, calm environmental storytelling, with weather and time-of-day changing the mood without destroying navigation readability.

Use the broad qualities being studied in the supplied painterly references; do not reproduce a named artist's signature style, specific compositions, or recognizable artwork.

### 2. Sky: pixel-art / dithered diorama layer

Treat the pixel sky as a distinct visual treatment, not as an arbitrary low-resolution asset pasted behind a high-resolution scene.

Prototype these constraints:
- Define a logical pixel grid and render the sky to a controlled low-resolution target with point filtering.
- Test integer-scale presentation at representative mobile aspect ratios and resolutions. If exact integer scaling cannot fill the display, prefer deliberate letterboxing, a stable logical viewport, or a carefully designed pixel-grid shader over arbitrary per-axis stretching.
- Keep dithering deterministic and temporally stable. Animated camera motion, TAA, dynamic resolution, and sub-pixel movement can cause shimmer; test those interactions explicitly.
- Use a shared color-script palette, but do not restrict the entire sky to only five literal colors. The proposed Amber, Indigo, Cyan, Emerald, and Rose are hue families or palette anchors; each needs value steps, neutrals, and controlled lighting variants.
- Preserve a clear depth relationship between sky, distant silhouettes, midground, and foreground. Pixel clouds may overlap other layers only when the compositing and occlusion are intentional and visually coherent; a categorical ban on crossing planes is unnecessarily restrictive.

The pixel sky is a **visual experiment**, not yet a committed technical requirement. Compare it against a painterly sky using the same scene composition before choosing.

### 3. Travel transition: brief scale and color contrast

The user identifies Environment reference image 8 as a high-saturation green alien landscape and proposes using it as a 2–5 second travel transition rather than a normal gameplay environment. The repository's Environment image list places image 8 at [IMG_1082.jpeg](../inspiration/art-direction-references/Environment/IMG_1082.jpeg). The image's description and intended role here are taken from the user's supplied review; the image has not been independently visually inspected in this review.

That limited use is promising because it separates the transition's purpose from the gameplay world's sustained readability. However:
- Treat 2–5 seconds as a test range, not a fixed requirement. The transition should not add avoidable waiting or conceal loading latency.
- Use camera motion, parallax, a cloud pass, or a dissolve only when it improves the sense of travel. Motion should remain comfortable on mobile and respect reduced-motion/accessibility settings.
- A shared color grade can connect the vista to the game's palette, but do not force every shadow to one literal hex value. Test color grading against scene lighting, skin/creature readability, and display variation.
- Use saturation as a controlled accent. A full-screen high-chroma burst can fatigue or reduce readability; compare several intensity levels.
- Keep the transition skippable or short enough not to interrupt repeated travel.

The reference should inform contrast, scale, and atmosphere—not be copied as a level, composition, or final environment asset.

## Composition: atmospheric depth and readable traversal

Bob Ross landscape paintings are useful studies for:
- Foreground framing that gives a scene scale.
- Midground forms that guide the eye through the playable space.
- Distant forms that establish depth and a focal destination.
- Atmospheric perspective: distant forms generally lose contrast and detail, with hue/value shifts depending on lighting and weather.
- A deliberate balance between negative space, silhouette, and focal detail.

Do not turn the suggested 0–25%, 40–60%, and 70–100% value bands into hard rules. They are rough teaching shorthand, not a calibrated luminance specification. The player, route, interactables, and hazards must remain readable in every lighting condition. Pure-black foreground silhouettes can obscure important gameplay information, especially on small screens.

Use original compositions and world layouts. Study the principles of framing and depth rather than recreating recognizable painting arrangements.

## Palette hypothesis

The proposed five anchors are:
- Amber
- Midnight Indigo (the supplied proposal uses #2A2354 as one possible shadow anchor)
- Cyan
- Emerald
- Rose

This is not yet a complete production palette. Define:
- Light, mid, and dark value steps for each hue family.
- Warm/cool neutrals and material-specific colors.
- Accessibility-safe contrast pairs for UI, silhouettes, and interactables.
- Weather/time-of-day variants.
- Rules for how the pixel sky and painterly world share color without flattening material identity.

The exact hex value #2A2354 is a candidate color, not a confirmed universal shadow color. Validate it against multiple biomes, skin/creature colors, dusk/night scenes, and color-vision simulations.

## Risks and falsification tests

| Risk | Test |
|---|---|
| Pixel sky feels pasted on | Compare painterly-only, pixel-only, and hybrid versions of the same composition. |
| Pixel grid shimmers on phones | Capture camera pans at multiple device resolutions, aspect ratios, and frame rates. |
| Dithering creates visual noise | Test at gameplay camera distance and thumbnail scale; reduce pattern contrast if it competes with the route. |
| Foreground silhouettes hide navigation | Run a small-screen readability test with the player, route, exits, and interactables visible. |
| Transition is visually tiring or interrupts play | Compare saturation and motion variants; measure perceived comfort and skip behavior in a short user test. |
| Five-color palette becomes restrictive | Build a representative environment, character, creature, and UI color sheet before freezing palette rules. |
| Reference dependence weakens originality | Produce original shape, architecture, and composition studies from the extracted principles only. |

## First prototype package

Do not build a full environment or shader system yet. Create one small comparison board:
1. One original outdoor route composition with foreground, midground, and distant focal point.
2. Three sky treatments: painterly, pixel-grid, and pixel-grid with restrained ordered dithering.
3. Two lighting conditions: warm late afternoon and cool overcast.
4. One travel transition study based on the *role* of Environment image 8, using original shapes and composition.
5. A mobile readability crop at a narrow phone aspect ratio and a wider phone aspect ratio.

Evaluate at actual phone scale, not only on a desktop canvas. The prototype should answer whether the hybrid language is cohesive, readable, and worth the additional rendering complexity.

## Decision boundary

This document proposes a direction and a falsification plan. It does not:
- Approve the five-color palette or #2A2354 as canonical.
- Require pixel art in all skies or all travel transitions.
- Approve a specific shader, render pipeline, resolution, or post-processing stack.
- Approve copying reference images, Bob Ross compositions, or any artist's distinctive style.
- Reorder the canonical battle-system priorities or authorize a Unity project.

Human review is required before this proposal becomes an accepted art-direction specification.
