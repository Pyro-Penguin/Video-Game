# Navigation Prototype — First Playable

**Status:** prototype specification and candidate Unity source; not compiled or playtested.

This folder records the first hand-authored navigation fixture and the Unity-side traversal adapter supplied for the navigation milestone. It does not create a Unity project, contain the frozen navigation domain implementation, or establish production readiness.

## Ownership and data flow

- **NavigationHost:** owns the level-scoped NavigationRuntime and rebuilds it from the JSON assets. The runtime is valid for the scene/level lifetime.
- **Navigation domain:** owns graph topology, gate state, pathfinding, and traversal rules. It remains engine-independent and is not duplicated here.
- **PathWalker:** owns its reusable path-index buffer and transient traversal cursor. It borrows the graph reference only while following a path; the host must outlive the walk.
- **Gate conditions:** NavigationHost composes condition providers through the narrow IConditionProvider interface. Providers own their condition state; the host/runtime is explicitly rebuilt when a condition changes.
- **LinkerBridge:** translates a Unity transform angle into a domain gate update. It references the host in one direction.
- **DualNodeRegistry / resolver:** maps co-located graph nodes to traversal contexts. The first-playable fixture intentionally tests this behavior.

Communication is through explicit method calls at the Unity integration boundary, the IConditionProvider interface for Boolean conditions, and the PathWalker.Arrived event for completion. No static service locator is introduced.

## Files

- `data/navigation.json` — six-node, four-edge hand-authored fixture.
- `data/gates.json` — linker and Boolean gate definitions.
- `FIRST_PLAYABLE_CHECKLIST.md` — claimed builder walkthrough, scene wiring, and manual acceptance checklist.
- `PathWalker.cs` — supplied Unity MonoBehaviour candidate; requires the frozen domain assembly and Unity compilation.
- `ResetReloadTests.cs` — supplied Unity Test Framework test candidate; requires a configured Unity test assembly, scene, NavigationHost, and FakeQuestProvider.

## Verification boundary

The JSON was manually checked against the previously reviewed NavigationGraphBuilder contract, but that builder source is not present in this public repository; the walkthrough is therefore not an independently reproduced build result. The C# files have **not** been compiled. The scene has **not** been created or playtested.

Code review note: the supplied PathWalker does not snap the transform to the final destination node before clearing the graph and raising Arrived. Correct that before using it in a scene, then compile and test it against the actual domain API. Do not treat this source snapshot as ready-to-ship code.

## Known design questions

1. Co-located dual nodes represent distinct traversal contexts, but the current graph has no edge between them. The resolver can select the alternate context while pathfinding correctly reports no route. The controller-level context-switch behavior is unresolved and intentionally not implemented here.
2. Node.Facing is present in the data schema but PathWalker faces along movement direction; Node.Facing is not consumed by this candidate.
3. Closing a gate during an already committed path does not cancel that path in this v1 fixture. The walker is expected to finish the committed path.
4. The ladder top is deliberately a dead end in this fixture; it exercises resolver selection and the ladder-down edge only.

## Scope

This is a bounded navigation prototype record. It does not alter the project's canonical priority order, approve a game rule, or authorize a full Unity project or production runtime.
