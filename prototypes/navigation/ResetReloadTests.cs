using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

public sealed class ResetReloadTests
{
    private const string SceneName = "FirstPlayable";

    [UnityTest]
    public IEnumerator Reload_RestoresInitialNavigationState()
    {
        yield return SceneManager.LoadSceneAsync(SceneName, LoadSceneMode.Single);
        yield return null;

        var host = Object.FindFirstObjectByType<NavigationHost>();
        Assert.IsNotNull(host);
        Assert.IsNotNull(host.Runtime);

        host.Runtime.SetLinkerAngle(1, 90f);
        host.Runtime.RebuildState();
        var gate2 = Object.FindFirstObjectByType<FakeQuestProvider>();
        gate2.SetOpen(true);
        host.Runtime.RebuildState();

        var pf = host.Runtime.Pathfinder;
        var path = new int[8];
        Assert.IsTrue(pf.TryFindPath(host.Runtime.State, new NodeId(1), new NodeId(3), path, out _));

        yield return SceneManager.LoadSceneAsync(SceneName, LoadSceneMode.Single);
        yield return null;

        var newHost = Object.FindFirstObjectByType<NavigationHost>();
        Assert.IsNotNull(newHost);
        Assert.IsNotNull(newHost.Runtime);
        Assert.AreNotSame(host.Runtime, newHost.Runtime, "Runtime must be reconstructed on reload.");

        var newPath = new int[8];
        Assert.IsFalse(newHost.Runtime.Pathfinder.TryFindPath(
            newHost.Runtime.State, new NodeId(1), new NodeId(3), newPath, out _),
            "Reloaded runtime must start with bridge closed and quest locked.");

        Assert.IsTrue(newHost.Runtime.Pathfinder.TryFindPath(
            newHost.Runtime.State, new NodeId(0), new NodeId(1), newPath, out _));
    }
}
