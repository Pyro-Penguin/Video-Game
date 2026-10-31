# First Playable — Validation and Playtest

**Status:** hand-validation notes and acceptance checklist. No Unity execution has been recorded.

## Fixture layout

| Node | Position | Role |
|---|---|---|
| 0 | (0, 0, 0) | Floor spawn |
| 1 | (2, 0, 0) | Pre-bridge |
| 2 | (4, 0, 0) | Post-bridge |
| 3 | (6, 0, 0) | Quest-locked room |
| 4 | (0, 0, 0) | Ladder base; co-located with floor node 0 |
| 5 | (0, 2, 0) | Ladder top |

Edges:
- 0↔1: unconditional walk.
- 1↔2: bridge; linker gate 1 must be between 85° and 95°.
- 2↔3: locked door; Boolean gate 2 must be open.
- 4↔5: ladder climb.

## Scene wiring

| Component | Field | Value |
|---|---|---|
| NavigationHost | `_navigationJson` | `navigation.json` |
| NavigationHost | `_gateJson` | `gates.json` |
| NavigationHost | `_boolConditionEntries` | `[{ "GateId": 2, "ConditionKey": "quest_gate_01" }]` |
| NavigationHost | `_conditionProviderBehaviours` | One FakeQuestProvider; Key = `quest_gate_01`; IsOpen = false initially |
| NavigationHost | `_dualNodeRegistry` | A DualNodeRegistry in the scene |
| DualNodeRegistry | `_entries` | `[{ "NodeA": 0, "NodeB": 4 }]` |
| LinkerBridge | `_navigationHost` | The same NavigationHost |
| LinkerBridge | `_linkerGateId` | 1 |
| LinkerBridge | `_axis` | Y, or the actual bridge rotation axis |
| LinkerBridge | transform | Attach to bridge pivot |
| PathWalker | — | Attach to player; wire through the controller |

The two nodes at (0,0,0) intentionally represent different contexts: node 0 is the floor and node 4 is the ladder base. Node 5 is intentionally a dead end except for the ladder-down edge.

## Manual builder walkthrough

The supplied hand-validation reports these checks as passing against the previously reviewed NavigationGraphBuilder contract:

| Check | Fixture value | Reported result |
|---|---|---|
| Nodes array | Non-null, length 6 | Pass |
| Edges array | Non-null, length 4 | Pass |
| Node entries | All six non-null | Pass |
| Node Facing | Values 1 or 4, expected range [0,5] | Pass |
| Node Animation | Values 0 or 1, expected range [0,4] | Pass |
| Edge endpoints | All indices in [0,6) | Pass |
| Edge Animation | Values 0, 1, or 3, expected range [0,3] | Pass |
| Referenced gate IDs | 1 and 2 exist | Pass |
| Duplicate gate IDs | None | Pass |
| Linker angle bounds | 85 and 95; finite and in [0,360) | Pass |
| Boolean condition | Gate 2 registered to quest_gate_01 | Pass when scene provider is wired |

**Verification caveat:** this is a recorded manual walkthrough, not a reproduced build. The builder source and its tests are not present in this repository, so the result must be re-run against the actual domain implementation before the fixture is considered validated.

Expected directed edge halves:
- Four unconditional halves: 0→1, 1→0, 4→5, 5→4.
- Two linker-gated halves: 1→2, 2→1.
- Two Boolean-gated halves: 2→3, 3→2.

Initial state: node 0 can reach node 1; the bridge and quest door are closed. The ladder edge 4↔5 is active.

## Playtest checklist

Record pass/fail and observed behavior for every item.

### Baseline traversal

- [ ] Spawn at node 0. Walk to node 1; path is found, player moves, and arrival is reported.
- [ ] From node 1, tap node 2 while the bridge is closed. TryFindPath returns false; player does not move; no exception.
- [ ] From node 1, tap the ladder base with Walk intent. Resolver should select floor node 0; route 1→0 is available. Confirm the spatial selector and resolver do not accidentally choose node 4.

### Linker gate

- [ ] Rotate bridge to 85°. RebuildState fires once when the angle crosses the configured threshold (the supplied note says 84.5°).
- [ ] From node 1, tap node 2. Path is found and the player crosses the bridge.
- [ ] Rotate bridge back to 0°. A new path to node 2 is unavailable.
- [ ] Close the bridge while the player is mid-crossing. Record whether the committed path completes; v1 accepts completion of an already committed path.

### Boolean gate

- [ ] From node 2, tap node 3 while the quest condition is false. No path is found.
- [ ] Set FakeQuestProvider.IsOpen to true using a debug control, then call RebuildState. The provider-to-host change notification is not currently wired in this fixture.
- [ ] Tap node 3. Path is found and the player arrives.

### Dual-node resolver and context switching

- [ ] At spawn, tap the ladder position with Walk intent. Resolver returns node 0; movement is empty/no-op.
- [ ] At spawn, tap the same position with Climb intent. Resolver returns node 4. TryFindPath(0,4) is expected to fail because no 0↔4 edge exists.
- [ ] Record whether the controller has an explicit same-group context-switch behavior. It is not part of the current design. Do not silently add a pseudo-edge or teleport rule during this playtest.
- [ ] At ladder top (node 5), tap ladder base with Climb intent. Resolver returns node 4 and path 5→4 is found.
- [ ] At ladder top, tap floor position with Walk intent. Resolver should select node 0. Path 5→0 is expected to fail because 4↔0 does not exist. Record spatial selection and resolver outputs separately.

**Known edge case:** co-located nodes are distinct graph identities. The resolver can select the correct alternate context, but no graph edge connects the two identities. A controller-level context switch, pseudo-edge, or other explicit rule may be needed. This is deliberately recorded for playtest rather than preemptively fixed.

### Reset / reload

- [ ] Open the bridge, complete the quest, and reach node 3.
- [ ] Reload the FirstPlayable scene using scene-level reload only for v1.
- [ ] New NavigationHost and NavigationRuntime are created.
- [ ] Bridge transform returns to its authored initial angle; LinkerBridge reapplies the initial angle and rebuilds state.
- [ ] FakeQuestProvider returns to IsOpen = false.
- [ ] Player returns to node 0.
- [ ] Path 0→1 is available; path 1→3 is unavailable.
- [ ] Confirm no old NavigationRuntime references survive scene reload.

Soft reset is out of scope. The supplied reset test is a candidate and depends on a FakeQuestProvider.SetOpen(bool) debug method that must exist in the Unity test fixture.

## Additional implementation observations

- PathWalker faces along movement direction. Node.Facing is currently unused at runtime; this is a schema observation, not a demonstrated failure.
- PathWalker now snaps transform.position to each completed edge's destination before advancing state; on final completion it snapshots the Arrived delegate, clears the graph, then invokes the callback. The source-level correction is committed but has not been compiled or verified in Unity.
- Empty-path contract: SetPath with a zero-length span is a no-op (IsWalking false; Arrived does not fire). The controller must handle already-at-destination before calling SetPath.
- Add a Play Mode regression test that subscribes to Arrived and asserts the observed transform equals the final destination position. Confirm it fails on the pre-fix implementation and passes on the corrected implementation. The proposed test sketch still needs a concrete BuildLinearGraph fixture matching the actual domain API.
- Add a Play Mode regression test that starts a valid path, calls SetPath with an empty span, and confirms the original path continues unchanged. Empty input must return before mutating the active path or graph reference.
- The supplied PathWalker and ResetReloadTests have not been compiled against the actual Unity version/domain API.
- No first-playable scene, prefab, debug controls, or condition-provider implementation is included in this repository update.

## Concrete failure categories that justify reopening frozen navigation work

1. Pathfinder returns a valid path that PathWalker cannot follow due to discontinuity.
2. Dual-node resolver selects the wrong node for a reproducible input.
3. RebuildState causes a measured frame spike at actual edge count; profile before changing rebuild strategy.
4. Reset/reload creates stale or corrupted runtime state.
5. A configured edge is unreachable despite accepted JSON and builder validation.

Movement feel, camera framing, and speed are tuning issues unless they expose one of these correctness failures.
