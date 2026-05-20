from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_graph.contract_surface import RuntimeContractSurfaceFrame
from ai_dev_os.runtime_graph.dependency_graph import RuntimeDependencyGraphFrame
from ai_dev_os.runtime_graph.runtime_clustering import RuntimeClusterFrame
from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryFrame


@dataclass(frozen=True)
class ArchitecturePressureFrame:
    runtime_count_pressure: str
    dependency_density_pressure: str
    contract_surface_pressure: str
    cross_boundary_pressure: str
    orchestration_pressure: str
    persistence_complexity_pressure: str
    dominant_architecture_pressure: str
    architecture_stability: str
    bounded_architecture_maintained: bool
    simplification_recommended: bool


class ArchitecturePressurePolicy:
    def evaluate(
        self,
        discovery: RuntimeDiscoveryFrame,
        graph: RuntimeDependencyGraphFrame,
        contract: RuntimeContractSurfaceFrame,
        clusters: RuntimeClusterFrame,
    ) -> ArchitecturePressureFrame:
        runtime_count = _pressure(discovery.runtime_count, medium=12, high=20)
        dependency_density = graph.architecture_pressure
        contract_surface = contract.runtime_api_pressure
        cross_boundary = clusters.cross_cluster_pressure
        orchestration_size = discovery.category_counts.get("orchestration", 0)
        persistence_size = discovery.category_counts.get("persistence", 0)
        orchestration = _pressure(orchestration_size, medium=3, high=5)
        persistence = _pressure(persistence_size, medium=3, high=5)
        pressures = {
            "runtime_count": runtime_count,
            "dependency_density": dependency_density,
            "contract_surface": contract_surface,
            "cross_boundary": cross_boundary,
            "orchestration": orchestration,
            "persistence_complexity": persistence,
        }
        dominant = max(pressures, key=lambda key: _score(pressures[key]))
        bounded = (
            graph.bounded_graph_size
            and discovery.summary_only
            and not contract.full_signature_replay_used
            and not contract.raw_ast_export_used
        )
        recommended = any(value == "high" for value in pressures.values())
        stability = "stable" if bounded and not recommended else "watch" if bounded else "unstable"
        return ArchitecturePressureFrame(
            runtime_count_pressure=runtime_count,
            dependency_density_pressure=dependency_density,
            contract_surface_pressure=contract_surface,
            cross_boundary_pressure=cross_boundary,
            orchestration_pressure=orchestration,
            persistence_complexity_pressure=persistence,
            dominant_architecture_pressure=dominant,
            architecture_stability=stability,
            bounded_architecture_maintained=bounded,
            simplification_recommended=recommended or contract.simplification_recommended,
        )


def _pressure(value: int, *, medium: int, high: int) -> str:
    if value >= high:
        return "high"
    if value >= medium:
        return "medium"
    return "low"


def _score(pressure: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}.get(pressure, 0)
