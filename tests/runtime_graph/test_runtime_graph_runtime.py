from __future__ import annotations

import inspect

from ai_dev_os.runtime_graph import RuntimeGraphPolicy
from ai_dev_os.runtime_graph.architecture_pressure import ArchitecturePressurePolicy
from ai_dev_os.runtime_graph.contract_surface import RuntimeContractSurfacePolicy
from ai_dev_os.runtime_graph.dependency_graph import RuntimeDependencyGraphPolicy
from ai_dev_os.runtime_graph.runtime_clustering import RuntimeClusterPolicy
from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryPolicy


def test_runtime_discovery_validation() -> None:
    frame = RuntimeDiscoveryPolicy().discover(".")

    assert frame.deterministic_discovery is True
    assert frame.summary_only is True
    assert frame.full_source_indexing_used is False
    assert frame.ast_replay_used is False
    assert frame.dynamic_tracing_used is False
    assert "governance" in frame.runtime_categories
    assert "retrieval" in frame.runtime_categories
    assert "persistence" in frame.runtime_categories


def test_bounded_graph_validation_and_max_edge_enforcement() -> None:
    discovery = RuntimeDiscoveryPolicy().discover(".")
    graph = RuntimeDependencyGraphPolicy().build(discovery, max_edges=5)

    assert graph.bounded_graph_size is True
    assert graph.edge_count <= 5
    assert graph.node_count == discovery.runtime_count
    assert graph.dependency_density > 0
    assert graph.full_repository_graph_used is False
    assert graph.cross_boundary_edges
    assert graph.governance_critical_edges


def test_cluster_and_architecture_pressure_validation() -> None:
    discovery = RuntimeDiscoveryPolicy().discover(".")
    graph = RuntimeDependencyGraphPolicy().build(discovery, max_edges=24)
    contract = RuntimeContractSurfacePolicy().summarize(discovery)
    clusters = RuntimeClusterPolicy().cluster(discovery, graph)
    pressure = ArchitecturePressurePolicy().evaluate(discovery, graph, contract, clusters)

    assert clusters.summary_only is True
    assert set(clusters.cluster_sizes) >= {"governance", "retrieval", "persistence"}
    assert pressure.dominant_architecture_pressure
    assert pressure.architecture_stability in {"stable", "watch", "unstable"}
    assert pressure.bounded_architecture_maintained is True


def test_runtime_graph_aggregate_frame_is_local_only() -> None:
    frame = RuntimeGraphPolicy().evaluate(".", max_edges=24)

    assert frame.runtime_graph_active is True
    assert frame.summary_only_dependency_cognition is True
    assert frame.hidden_telemetry_used is False
    assert frame.dependency_graph.edge_count <= frame.dependency_graph.max_edge_limit


def test_no_hidden_telemetry_ast_replay_or_dynamic_tracing() -> None:
    import ai_dev_os.runtime_graph as root
    import ai_dev_os.runtime_graph.contract_surface as contract
    import ai_dev_os.runtime_graph.dependency_graph as graph
    import ai_dev_os.runtime_graph.runtime_discovery as discovery

    source = "\n".join(
        inspect.getsource(module).lower() for module in (root, discovery, graph, contract)
    )

    forbidden = (
        "requests",
        "http",
        "subprocess",
        "ast.",
        "trace",
        "telemetry.upload",
        "full_repository_graph_used=true",
    )
    assert all(item not in source for item in forbidden)


def test_runtime_audit_reports_runtime_graph_section() -> None:
    from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

    report = run_runtime_enforcement_audit()

    assert report.runtime_graph.runtime_graph_active is True
    assert report.runtime_graph.runtime_discovery_active is True
    assert report.runtime_graph.dependency_graph_active is True
    assert report.runtime_graph.contract_surface_active is True
    assert report.runtime_graph.runtime_clustering_active is True
    assert report.runtime_graph.architecture_pressure_active is True
    assert report.runtime_graph.estimated_avoided_architecture_cognition_tokens > 0
    assert report.runtime_graph.estimated_avoided_runtime_explosion_drift > 0
    assert report.runtime_graph.hidden_telemetry_used is False
