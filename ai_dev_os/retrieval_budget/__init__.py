from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.retrieval_budget.retrieval_budget_policy import (
    RetrievalBudgetPolicy,
    RetrievalBudgetPolicyFrame,
)
from ai_dev_os.retrieval_budget.retrieval_compaction import (
    RetrievalCompactionFrame,
    RetrievalCompactionPolicy,
)
from ai_dev_os.retrieval_budget.retrieval_pressure import (
    RetrievalPressureFrame,
    RetrievalPressurePolicy,
)
from ai_dev_os.retrieval_budget.retrieval_radius import (
    RetrievalRadiusFrame,
    RetrievalRadiusPolicy,
    RuntimeDependency,
)
from ai_dev_os.retrieval_budget.retrieval_scope import RetrievalScopeFrame, RetrievalScopePolicy


@dataclass(frozen=True)
class RetrievalBudgetFrame:
    scope: RetrievalScopeFrame
    radius: RetrievalRadiusFrame
    budget: RetrievalBudgetPolicyFrame
    compaction: RetrievalCompactionFrame
    pressure: RetrievalPressureFrame
    retrieval_budget_active: bool
    estimated_avoided_hidden_input_tokens: int
    estimated_avoided_repo_wide_reasoning: int
    local_only: bool
    deterministic: bool
    summary_only: bool
    repo_wide_retrieval_forbidden: bool


class RetrievalBudgetRuntime:
    def evaluate(
        self,
        *,
        affected_runtimes: tuple[str, ...],
        all_runtimes: tuple[str, ...],
        dependencies: tuple[RuntimeDependency, ...],
        continuity_size: int,
        contract_surfaces: tuple[str, ...],
        architecture_isolation: bool = False,
        max_dependency_distance: int = 2,
    ) -> RetrievalBudgetFrame:
        radius = RetrievalRadiusPolicy().evaluate(
            affected_runtimes,
            dependencies,
            max_dependency_distance=max_dependency_distance,
            isolated_runtimes=affected_runtimes if architecture_isolation else (),
        )
        scope = RetrievalScopePolicy().scope(
            affected_runtimes=affected_runtimes,
            all_runtimes=all_runtimes,
            radius=radius,
            architecture_isolation=architecture_isolation,
        )
        budget = RetrievalBudgetPolicy().evaluate(
            runtime_count=len(scope.bounded_retrieval_neighborhood),
            contract_count=len(radius.bounded_contract_adjacency),
            continuity_size=continuity_size,
        )
        compaction = RetrievalCompactionPolicy().compact(
            runtime_summaries=tuple(
                f"runtime:{runtime}" for runtime in scope.bounded_retrieval_neighborhood
            ),
            contract_surfaces=contract_surfaces or radius.bounded_contract_adjacency,
            runtime_metadata=tuple(
                f"{runtime} summary-only retrieval metadata"
                for runtime in scope.bounded_retrieval_neighborhood
            ),
        )
        pressure = RetrievalPressurePolicy().evaluate(
            selected_runtime_count=len(scope.bounded_retrieval_neighborhood),
            all_runtime_count=len(all_runtimes),
            continuity_size=continuity_size,
            max_runtime_count=budget.max_runtime_count,
            max_continuity_size=budget.max_continuity_size,
            architecture_isolation=architecture_isolation,
        )
        repo_wide_burn = (
            max(0, len(all_runtimes) - len(scope.bounded_retrieval_neighborhood)) * 320
        )
        return RetrievalBudgetFrame(
            scope=scope,
            radius=radius,
            budget=budget,
            compaction=compaction,
            pressure=pressure,
            retrieval_budget_active=scope.repo_wide_retrieval_forbidden
            and radius.dependency_depth_cap_applied
            and compaction.summary_only,
            estimated_avoided_hidden_input_tokens=pressure.estimated_hidden_input_token_burn,
            estimated_avoided_repo_wide_reasoning=repo_wide_burn,
            local_only=scope.local_only,
            deterministic=radius.deterministic and budget.deterministic and pressure.deterministic,
            summary_only=scope.summary_only and compaction.summary_only,
            repo_wide_retrieval_forbidden=scope.repo_wide_retrieval_forbidden,
        )


__all__ = [
    "RetrievalBudgetFrame",
    "RetrievalBudgetPolicy",
    "RetrievalBudgetPolicyFrame",
    "RetrievalBudgetRuntime",
    "RetrievalCompactionFrame",
    "RetrievalCompactionPolicy",
    "RetrievalPressureFrame",
    "RetrievalPressurePolicy",
    "RetrievalRadiusFrame",
    "RetrievalRadiusPolicy",
    "RetrievalScopeFrame",
    "RetrievalScopePolicy",
    "RuntimeDependency",
]
