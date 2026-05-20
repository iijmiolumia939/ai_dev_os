from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_graph.dependency_graph import RuntimeDependencyGraphFrame
from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryFrame

_CLUSTERS = (
    "governance",
    "retrieval",
    "persistence",
    "orchestration",
    "provider",
    "vscode",
    "cognition",
    "adapters",
)


@dataclass(frozen=True)
class RuntimeClusterFrame:
    cluster_sizes: dict[str, int]
    oversized_clusters: tuple[str, ...]
    cross_cluster_pressure: str
    merge_candidates: tuple[str, ...]
    isolation_candidates: tuple[str, ...]
    bounded_clusters: bool
    summary_only: bool


class RuntimeClusterPolicy:
    def cluster(
        self,
        discovery: RuntimeDiscoveryFrame,
        graph: RuntimeDependencyGraphFrame,
        *,
        max_cluster_size: int = 5,
    ) -> RuntimeClusterFrame:
        sizes = {cluster: discovery.category_counts.get(cluster, 0) for cluster in _CLUSTERS}
        oversized = tuple(cluster for cluster, size in sizes.items() if size > max_cluster_size)
        sparse = tuple(cluster for cluster, size in sizes.items() if size == 1)
        isolated = tuple(
            cluster
            for cluster, size in sizes.items()
            if size > 0 and cluster in graph.isolated_runtime_groups
        )
        cross_ratio = len(graph.cross_boundary_edges) / max(1, graph.edge_count)
        pressure = "high" if cross_ratio > 0.75 else "medium" if cross_ratio > 0.45 else "low"
        return RuntimeClusterFrame(
            cluster_sizes=sizes,
            oversized_clusters=oversized,
            cross_cluster_pressure=pressure,
            merge_candidates=sparse[:4],
            isolation_candidates=isolated[:4],
            bounded_clusters=all(size <= max_cluster_size + 3 for size in sizes.values()),
            summary_only=True,
        )
