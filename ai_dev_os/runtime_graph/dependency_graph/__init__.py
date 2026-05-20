from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryFrame, RuntimeRecord


@dataclass(frozen=True)
class RuntimeDependencyEdge:
    source_runtime: str
    target_runtime: str
    dependency_kind: str
    cross_boundary: bool
    governance_critical: bool
    optional_dependency: bool


@dataclass(frozen=True)
class RuntimeDependencyGraphFrame:
    runtime_nodes: tuple[str, ...]
    bounded_dependency_edges: tuple[RuntimeDependencyEdge, ...]
    cross_boundary_edges: tuple[RuntimeDependencyEdge, ...]
    governance_critical_edges: tuple[RuntimeDependencyEdge, ...]
    optional_dependency_edges: tuple[RuntimeDependencyEdge, ...]
    isolated_runtime_groups: tuple[str, ...]
    node_count: int
    edge_count: int
    isolated_clusters: tuple[str, ...]
    architecture_pressure: str
    dependency_density: float
    max_edge_limit: int
    bounded_graph_size: bool
    full_repository_graph_used: bool


class RuntimeDependencyGraphPolicy:
    def build(
        self,
        discovery: RuntimeDiscoveryFrame,
        *,
        max_edges: int = 32,
    ) -> RuntimeDependencyGraphFrame:
        if max_edges <= 0:
            raise ValueError("max_edges must be positive")
        edges = tuple(self._bounded_edges(discovery.runtimes, max_edges=max_edges))
        node_names = discovery.runtime_names
        cross_boundary = tuple(edge for edge in edges if edge.cross_boundary)
        governance_critical = tuple(edge for edge in edges if edge.governance_critical)
        optional = tuple(edge for edge in edges if edge.optional_dependency)
        connected = {edge.source_runtime for edge in edges} | {
            edge.target_runtime for edge in edges
        }
        isolated = tuple(name for name in node_names if name not in connected)
        density = round(len(edges) / max(1, len(node_names)), 4)
        pressure = "high" if density >= 2.0 else "medium" if density >= 1.0 else "low"
        return RuntimeDependencyGraphFrame(
            runtime_nodes=node_names,
            bounded_dependency_edges=edges,
            cross_boundary_edges=cross_boundary,
            governance_critical_edges=governance_critical,
            optional_dependency_edges=optional,
            isolated_runtime_groups=isolated,
            node_count=len(node_names),
            edge_count=len(edges),
            isolated_clusters=isolated,
            architecture_pressure=pressure,
            dependency_density=density,
            max_edge_limit=max_edges,
            bounded_graph_size=len(edges) <= max_edges,
            full_repository_graph_used=False,
        )

    def _bounded_edges(
        self,
        records: tuple[RuntimeRecord, ...],
        *,
        max_edges: int,
    ) -> list[RuntimeDependencyEdge]:
        by_category: dict[str, RuntimeRecord] = {}
        for record in records:
            by_category.setdefault(record.runtime_category, record)
        rules = (
            ("orchestration", "governance", "control", True),
            ("orchestration", "persistence", "state", True),
            ("orchestration", "retrieval", "context", True),
            ("governance", "persistence", "retention", True),
            ("governance", "provider", "budget", True),
            ("retrieval", "persistence", "memory", False),
            ("cognition", "retrieval", "summary", False),
            ("cognition", "governance", "pressure", True),
            ("vscode", "orchestration", "handoff", False),
            ("vscode", "governance", "dashboard", True),
            ("adapters", "provider", "optional", False),
        )
        edges: list[RuntimeDependencyEdge] = []
        for source_category, target_category, kind, critical in rules:
            if len(edges) >= max_edges:
                break
            source = by_category.get(source_category)
            target = by_category.get(target_category)
            if source is None or target is None:
                continue
            edges.append(
                RuntimeDependencyEdge(
                    source_runtime=source.runtime_name,
                    target_runtime=target.runtime_name,
                    dependency_kind=kind,
                    cross_boundary=source.runtime_category != target.runtime_category,
                    governance_critical=critical,
                    optional_dependency=kind == "optional",
                )
            )
        return edges
