# Implementation Plan

## Goal
Reach a small, deterministic, locally playable 3v3 battle prototype before building broad world content.

## Gate 0 — Project Baseline
- [ ] Confirm Unity editor version and target iOS/Android versions.
- [ ] Locate the actual Unity project root and inspect its existing structure.
- [ ] Confirm whether existing archives contain source worth importing; do not modify originals.
- [ ] Establish a clean baseline commit and verify the project opens in the editor.

**Exit criteria:** project opens without errors; baseline is reproducible; editor version is recorded.

## Gate 1 — Battle Rules
- [ ] Resolve commander defeat / match end.
- [ ] Resolve the apparent mismatch between "bring 5, select 3" and "2 active + 1 reserve".
- [ ] Specify reserve deployment and replacement timing.
- [ ] Specify legal actions, targeting, ties, simultaneous resolution, and fainting order.
- [ ] Specify stat normalization, damage formula, and elemental chart.
- [ ] Define a deterministic example turn with expected results.

**Exit criteria:** a rules document is complete enough that two independent implementations would produce the same outcome.

## Gate 2 — Pure Battle Simulation
- [ ] Implement engine-independent battle state and immutable battle definitions.
- [ ] Implement validation for team setup and actions.
- [ ] Implement deterministic turn resolver with explicit ordering.
- [ ] Add unit tests for legal/illegal actions, damage, switching, knockouts, reserve handling, and victory.
- [ ] Add seeded randomness only where the rules explicitly require it.

**Exit criteria:** tests exercise a full match without requiring Unity scenes, GameObjects, or frame updates.

## Gate 3 — Unity Presentation
- [ ] Add a thin battle scene controller that translates player input into battle commands.
- [ ] Render battle state from simulation snapshots/events.
- [ ] Add touch-friendly action selection and safe-area-aware layout.
- [ ] Add basic feedback for actions, damage, status, and victory.

**Exit criteria:** two local sides can complete a match through the UI.

## Gate 4 — Initial Content
- [ ] Add 2 commanders, 2 main weapons, and 6 distinct monsters with movesets.
- [ ] Store balance-sensitive definitions as data assets.
- [ ] Validate all content through the same rules used by the simulation.

**Exit criteria:** content can be changed without editing core resolution code.

## Constraints
- Do not begin broad world, quest, or cinematic production before Gate 2 is stable.
- Do not invent missing design decisions in code; represent unresolved rules explicitly.
- Keep pure rules code independent of Unity APIs.
