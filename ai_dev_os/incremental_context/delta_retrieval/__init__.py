from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.incremental_context.context_delta import ContextDeltaFrame
from ai_dev_os.retrieval_budget import RetrievalBudgetRuntime
from ai_dev_os.retrieval_budget.retrieval_radius import RuntimeDependency


@dataclass(frozen=True)
class DeltaRetrievalFrame:
    delta_only_retrieval: bool
    bounded_incremental_retrieval_radius: int
    unchanged_dependency_suppression: bool
    compact_changed_neighborhood: tuple[str, ...]
    suppressed_unchanged_dependencies: tuple[str, ...]
    repo_wide_replay_forbidden: bool
    retrieval_budget_active: bool
    summary_only: bool
    local_only: bool
    deterministic: bool


class DeltaRetrievalPolicy:
    def retrieve(
        self,
        *,
        delta: ContextDeltaFrame,
        all_runtimes: tuple[str, ...],
        dependencies: tuple[RuntimeDependency, ...],
        continuity_size: int,
        max_dependency_distance: int = 1,
    ) -> DeltaRetrievalFrame:
        changed_runtimes = tuple(
            summary.removeprefix("runtime:") for summary in delta.changed_runtime_summaries
        )
        budget = RetrievalBudgetRuntime().evaluate(
            affected_runtimes=changed_runtimes,
            all_runtimes=all_runtimes,
            dependencies=dependencies,
            continuity_size=continuity_size,
            contract_surfaces=delta.changed_contract_summaries,
            architecture_isolation=True,
            max_dependency_distance=max_dependency_distance,
        )
        neighborhood = budget.scope.bounded_retrieval_neighborhood
        suppressed = tuple(
            f"{item.source}->{item.target}"
            for item in dependencies
            if item.source not in neighborhood and item.target not in neighborhood
        )
        return DeltaRetrievalFrame(
            delta_only_retrieval=True,
            bounded_incremental_retrieval_radius=max_dependency_distance,
            unchanged_dependency_suppression=True,
            compact_changed_neighborhood=neighborhood,
            suppressed_unchanged_dependencies=tuple(sorted(suppressed)),
            repo_wide_replay_forbidden=budget.repo_wide_retrieval_forbidden,
            retrieval_budget_active=budget.retrieval_budget_active,
            summary_only=budget.summary_only,
            local_only=budget.local_only,
            deterministic=budget.deterministic,
        )
