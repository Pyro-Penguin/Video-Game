using System;
using Project.Domain.Navigation;
using UnityEngine;

public sealed class PathWalker : MonoBehaviour
{
    [SerializeField, Min(16)] private int _initialCapacity = 64;
    [SerializeField, Min(0.01f)] private float _walkSpeed = 2f;
    [SerializeField, Min(0.01f)] private float _climbSpeed = 1f;
    [SerializeField, Min(0.01f)] private float _rotateSpeed = 1f;

    private int[] _activePath;
    private int _activePathLength;
    private NavigationGraph _graph;
    private NodeId _currentStart;
    private int _currentEdgeSlot;
    private float _t;

    public event Action Arrived;

    public bool IsWalking => _graph != null && _activePathLength > 0 && _currentEdgeSlot < _activePathLength;
    public int ActivePathLength => _activePathLength;
    public ReadOnlySpan<int> ActivePath => _activePath.AsSpan(0, _activePathLength);

    private void Awake()
    {
        if (_initialCapacity < 1)
            throw new InvalidOperationException(
                "[PathWalker] _initialCapacity must be >= 1; the Inspector [Min] attribute is not a runtime guarantee.");
        _activePath = new int[_initialCapacity];
    }

    /// <summary>
    /// Starts walking. Caller must not pass an empty path; the controller handles the
    /// "already at destination" case before calling SetPath. Passing empty is a no-op
    /// that leaves IsWalking false and never fires Arrived.
    /// </summary>
    public void SetPath(NavigationGraph graph, ReadOnlySpan<int> edgePath, NodeId from)
    {
        if (graph == null) throw new ArgumentNullException(nameof(graph));
        if (edgePath.Length > _activePath.Length) Grow(edgePath.Length);
        edgePath.CopyTo(_activePath);
        _activePathLength = edgePath.Length;
        _graph = graph;
        _currentStart = from;
        _currentEdgeSlot = 0;
        _t = 0f;
    }

    public void ClearPath()
    {
        _activePathLength = 0;
        _graph = null;
        _currentEdgeSlot = 0;
        _t = 0f;
    }

    private void Update()
    {
        if (!IsWalking) return;

        int edgeIdx = _activePath[_currentEdgeSlot];
        var edge = _graph.GetEdge(edgeIdx);
        var from = edge.From.Value == _currentStart.Value ? edge.From : edge.To;
        var to   = edge.From.Value == _currentStart.Value ? edge.To   : edge.From;

        float speed = edge.Animation switch
        {
            EdgeAnimationHint.ClimbLadder => _climbSpeed,
            EdgeAnimationHint.RotateWalk  => _rotateSpeed,
            _ => _walkSpeed
        };

        float len = Distance(_graph.GetNode(from).Position, _graph.GetNode(to).Position);
        _t += (speed * Time.deltaTime) / Mathf.Max(len, 0.001f);

        if (_t >= 1f)
        {
            // Snap before advancing state or notifying listeners. Arrived subscribers
            // must observe the transform at the final destination node.
            transform.position = ToUnity(_graph.GetNode(to).Position);
            _currentStart = to;
            _currentEdgeSlot++;
            _t = 0f;
            if (_currentEdgeSlot >= _activePathLength)
            {
                var callback = Arrived;
                _graph = null;
                callback?.Invoke();
                return;
            }

            edgeIdx = _activePath[_currentEdgeSlot];
            edge = _graph.GetEdge(edgeIdx);
            from = edge.From.Value == _currentStart.Value ? edge.From : edge.To;
            to   = edge.From.Value == _currentStart.Value ? edge.To   : edge.From;
        }

        var pA = _graph.GetNode(from).Position;
        var pB = _graph.GetNode(to).Position;
        transform.position = Lerp(ToUnity(pA), ToUnity(pB), _t);

        var delta = ToUnity(pB) - ToUnity(pA);
        if (delta.sqrMagnitude > 1e-6f)
            transform.rotation = Quaternion.LookRotation(delta.normalized, Vector3.up);
    }

    private void Grow(int min)
    {
        int next = _activePath.Length;
        while (next < min) next *= 2;
        Array.Resize(ref _activePath, next);
    }

    private static float Distance(Float3 a, Float3 b)
    {
        float dx = b.X - a.X, dy = b.Y - a.Y, dz = b.Z - a.Z;
        return Mathf.Sqrt(dx * dx + dy * dy + dz * dz);
    }

    private static Vector3 ToUnity(Float3 v) => new Vector3(v.X, v.Y, v.Z);

    private static Vector3 Lerp(Vector3 a, Vector3 b, float t) => a + (b - a) * t;
}
