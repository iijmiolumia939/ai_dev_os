from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeDependency:
    source: str
    target: str
    distance: int = 1
    contract: str = ""


@dataclass(frozen=True)
class RetrievalRadiusFrame:
    max_dependency_distance: int
    compact_runtime_neighborhood: tuple[str, ...]
    bounded_contract_adjacency: tuple[str, ...]
    isolated_runtime_boundaries: tuple[str, ...]
    dependency_depth_cap_applied: bool
    summary_only: bool
    deterministic: bool


class RetrievalRadiusPolicy:
    def evaluate(
        self,
        affected_runtimes: tuple[str, ...],
        dependencies: tuple[RuntimeDependency, ...],
        *,
        max_dependency_distance: int = 2,
        isolated_runtimes: tuple[str, ...] = (),
    ) -> RetrievalRadiusFrame:
        affected = set(affected_runtimes)
        isolated = set(isolated_runtimes)
        neighborhood = set(affected_runtimes)
        contracts: set[str] = set()
        boundaries: set[str] = set()

        for dependency in dependencies:
            touches_affected = dependency.source in affected or dependency.target in affected
            within_radius = dependency.distance <= max_dependency_distance
            touches_isolated = dependency.source in isolated or dependency.target in isolated
            if touches_isolated and not touches_affected:
                boundaries.add(f"{dependency.source}->{dependency.target}")
                continue
            if touches_affected and within_radius:
                neighborhood.update((dependency.source, dependency.target))
                if dependency.contract:
                    contracts.add(dependency.contract)
            elif touches_affected:
                boundaries.add(f"{dependency.source}->{dependency.target}")

        return RetrievalRadiusFrame(
            max_dependency_distance=max_dependency_distance,
            compact_runtime_neighborhood=tuple(sorted(neighborhood)),
            bounded_contract_adjacency=tuple(sorted(contracts)),
            isolated_runtime_boundaries=tuple(sorted(boundaries)),
            dependency_depth_cap_applied=True,
            summary_only=True,
            deterministic=True,
        )
