from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.retrieval_budget import RetrievalBudgetRuntime, RuntimeDependency
from ai_dev_os.runtime_graph.architecture_pressure import (
    ArchitecturePressureFrame,
    ArchitecturePressurePolicy,
)
from ai_dev_os.runtime_graph.contract_surface import (
    RuntimeContractSurfaceFrame,
    RuntimeContractSurfacePolicy,
)
from ai_dev_os.runtime_graph.dependency_graph import (
    RuntimeDependencyGraphFrame,
    RuntimeDependencyGraphPolicy,
)
from ai_dev_os.runtime_graph.runtime_clustering import RuntimeClusterFrame, RuntimeClusterPolicy
from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryFrame, RuntimeDiscoveryPolicy


@dataclass(frozen=True)
class RuntimeGraphFrame:
    discovery: RuntimeDiscoveryFrame
    dependency_graph: RuntimeDependencyGraphFrame
    contract_surface: RuntimeContractSurfaceFrame
    runtime_clusters: RuntimeClusterFrame
    architecture_pressure: ArchitecturePressureFrame
    runtime_graph_active: bool
    summary_only_dependency_cognition: bool
    hidden_telemetry_used: bool
    retrieval_budget_active: bool
    retrieval_budget_summary_only: bool
    repo_wide_retrieval_forbidden: bool


class RuntimeGraphPolicy:
    def evaluate(self, repo_path: str | Path = ".", *, max_edges: int = 32) -> RuntimeGraphFrame:
        discovery = RuntimeDiscoveryPolicy().discover(repo_path)
        graph = RuntimeDependencyGraphPolicy().build(discovery, max_edges=max_edges)
        contract = RuntimeContractSurfacePolicy().summarize(discovery)
        clusters = RuntimeClusterPolicy().cluster(discovery, graph)
        pressure = ArchitecturePressurePolicy().evaluate(discovery, graph, contract, clusters)
        runtimes = tuple(discovery.runtime_names)
        affected = runtimes[:2] or runtimes
        retrieval_budget = RetrievalBudgetRuntime().evaluate(
            affected_runtimes=affected,
            all_runtimes=runtimes,
            dependencies=tuple(
                RuntimeDependency(
                    source=edge.source_runtime,
                    target=edge.target_runtime,
                    contract=edge.dependency_kind,
                )
                for edge in graph.bounded_dependency_edges[:max_edges]
            ),
            continuity_size=min(2_400, contract.contract_surface_size * 20),
            contract_surfaces=contract.exported_contracts,
            architecture_isolation=pressure.simplification_recommended,
        )
        return RuntimeGraphFrame(
            discovery=discovery,
            dependency_graph=graph,
            contract_surface=contract,
            runtime_clusters=clusters,
            architecture_pressure=pressure,
            runtime_graph_active=bool(discovery.runtimes) and graph.bounded_graph_size,
            summary_only_dependency_cognition=True,
            hidden_telemetry_used=False,
            retrieval_budget_active=retrieval_budget.retrieval_budget_active,
            retrieval_budget_summary_only=retrieval_budget.summary_only,
            repo_wide_retrieval_forbidden=retrieval_budget.repo_wide_retrieval_forbidden,
        )
