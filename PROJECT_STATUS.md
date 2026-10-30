# Project Status

## Project
Mobile Unity RPG for iOS and Android.

## Current Stage
Prototype planning and repository foundation. The immediate engineering objective is a coherent, testable local 3v3 battle prototype before expanding world content.

## Current Prototype Target
- Local PvP-style battle with both sides controlled by the user.
- Each side: 1 commander, 2 active monsters, and 1 reserve.
- Team preview: bring 5 monsters and select 3 for battle.
- Simultaneous turn resolution.
- Normalized battle stats and elemental types.
- Initial content target: 2 commanders, 2 main weapons, and 6 distinct monsters with movesets.

## Unresolved Design Decisions
- Commander defeat and match-ending rules.
- Final reserve deployment behavior.
- Detailed turn-resolution and targeting rules.
- Final damage and elemental effectiveness formulas.

## Engineering Constraints
- Keep game rules and state in pure, testable C# where practical.
- Keep Unity scene components thin and presentation-focused.
- Prefer composition, explicit ownership, and event/interface-based communication.
- Use data-driven configuration for balance-sensitive content.
- Avoid allocations and expensive work in per-frame gameplay paths.

## Repository Notes
- Confirm the Unity editor version and actual project folder before committing engine-specific implementation.
- Treat original project archives as immutable source material.
- Update this document when prototype scope or implementation status changes.
