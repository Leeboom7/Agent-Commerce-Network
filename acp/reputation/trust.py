"""
ACP Reputation System — Transitive Trust.

Computes indirect trust scores between agents who have never
transacted directly, using the trust graph of the network.

Formula: Trust(A→C) = Σ(Trust(A→B) × Trust(B→C)) / Σ(Trust(A→B))
where B iterates over all intermediate agents.
"""

from __future__ import annotations

from collections import defaultdict


class TrustGraph:
    """
    A directed graph of direct trust scores between agents.

    Enables queries like: "Agent A has never worked with Agent C.
    Agent A trusts Agent B (score 0.9), and Agent B trusts Agent C
    (score 0.8). What's the estimated trust A→C?"
    """

    def __init__(self) -> None:
        # agent_id → {other_agent_id: direct_trust_score}
        self._graph: dict[str, dict[str, float]] = defaultdict(dict)

    # ── Direct Trust ──────────────────────────────────────

    def set_trust(self, from_agent: str, to_agent: str, score: float) -> None:
        """
        Set direct trust score from one agent to another.
        Score should be in [0, 1].
        """
        self._graph[from_agent][to_agent] = max(0.0, min(1.0, score))

    def get_direct_trust(self, from_agent: str, to_agent: str) -> float | None:
        """Get direct trust score, or None if no direct experience."""
        return self._graph.get(from_agent, {}).get(to_agent)

    def update_trust(
        self, from_agent: str, to_agent: str, delta: float
    ) -> None:
        """Update trust score by a delta (positive or negative)."""
        current = self.get_direct_trust(from_agent, to_agent) or 0.5
        new_score = max(0.0, min(1.0, current + delta))
        self.set_trust(from_agent, to_agent, new_score)

    # ── Transitive Trust ──────────────────────────────────

    def compute_transitive_trust(
        self, from_agent: str, to_agent: str, max_depth: int = 3
    ) -> float | None:
        """
        Compute transitive trust from A to C through the trust graph.

        Uses weighted average of all paths:
          T(A→C) = Σ_w(path) × trust_along_path / Σ_w(path)

        where w(path) is higher for shorter paths with fewer hops.
        """
        if from_agent == to_agent:
            return 1.0

        # Check direct trust first
        direct = self.get_direct_trust(from_agent, to_agent)
        if direct is not None:
            return direct

        # BFS-like traversal for paths up to max_depth
        paths = self._find_paths(from_agent, to_agent, max_depth)
        if not paths:
            return None

        # Weighted average of trust along each path
        weighted_sum = 0.0
        total_weight = 0.0

        for path in paths:
            # Trust along path = product of trust scores
            path_trust = 1.0
            for i in range(len(path) - 1):
                edge_trust = self.get_direct_trust(path[i], path[i + 1])
                if edge_trust is None:
                    path_trust = 0.0
                    break
                path_trust *= edge_trust

            # Shorter paths have higher weight
            weight = 1.0 / len(path)

            weighted_sum += path_trust * weight
            total_weight += weight

        if total_weight == 0:
            return None

        return round(weighted_sum / total_weight, 3)

    def get_trust_network(
        self, agent_id: str, depth: int = 1
    ) -> dict[str, dict[str, float]]:
        """
        Get the trust subgraph centered on an agent, up to given depth.
        """
        result: dict[str, dict[str, float]] = {}
        visited: set[str] = {agent_id}

        current_layer = {agent_id}
        for _ in range(depth):
            next_layer: set[str] = set()
            for node in current_layer:
                neighbors = self._graph.get(node, {})
                result[node] = dict(neighbors)
                next_layer.update(neighbors.keys())
            current_layer = next_layer - visited
            visited.update(current_layer)

        return result

    # ── Graph Analysis ────────────────────────────────────

    def get_most_trusted(self, agent_id: str, limit: int = 10) -> list[tuple[str, float]]:
        """Get agents most trusted by a given agent."""
        trust_scores = self._graph.get(agent_id, {})
        sorted_scores = sorted(trust_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:limit]

    def get_trusting(self, agent_id: str) -> list[tuple[str, float]]:
        """Get agents that trust the given agent."""
        result = []
        for from_agent, trusts in self._graph.items():
            if agent_id in trusts:
                result.append((from_agent, trusts[agent_id]))
        return sorted(result, key=lambda x: x[1], reverse=True)

    # ── Helpers ───────────────────────────────────────────

    def _find_paths(
        self, start: str, end: str, max_depth: int
    ) -> list[list[str]]:
        """Find all simple paths from start to end up to max_depth."""
        paths: list[list[str]] = []
        self._dfs(start, end, [start], set(), max_depth, paths)
        # Sort by path length (shorter first)
        paths.sort(key=len)
        return paths

    def _dfs(
        self, current: str, target: str, path: list[str],
        visited: set[str], remaining_depth: int, results: list[list[str]],
    ) -> None:
        if remaining_depth <= 0:
            return
        if current == target and len(path) > 1:
            results.append(list(path))
            return

        visited.add(current)
        for neighbor in self._graph.get(current, {}):
            if neighbor not in visited or neighbor == target:
                self._dfs(
                    neighbor, target, path + [neighbor],
                    visited.copy(), remaining_depth - 1, results,
                )

    @property
    def agent_count(self) -> int:
        return len(self._graph)

    @property
    def edge_count(self) -> int:
        return sum(len(trusts) for trusts in self._graph.values())
