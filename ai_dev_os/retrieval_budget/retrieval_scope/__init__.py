from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.retrieval_budget.retrieval_radius import RetrievalRadiusFrame


@dataclass(frozen=True)
class RetrievalScopeFrame:
    bounded_retrieval_neighborhood: tuple[str, ...]
    affected_runtime_only_retrieval: bool
    dependency_depth_cap: int
    architecture_isolation_aware_retrieval: bool
    repo_wide_retrieval_forbidden: bool
    excluded_runtimes: tuple[str, ...]
    summary_only: bool
    local_only: bool
    no_ast_replay: bool
    no_dynamic_tracing: bool
    no_automatic_repo_wide_indexing: bool


class RetrievalScopePolicy:
    def scope(
        self,
        *,
        affected_runtimes: tuple[str, ...],
        all_runtimes: tuple[str, ...],
        radius: RetrievalRadiusFrame,
        architecture_isolation: bool = False,
    ) -> RetrievalScopeFrame:
        selected = tuple(
            runtime
            for runtime in radius.compact_runtime_neighborhood
            if runtime in set(affected_runtimes) | set(radius.compact_runtime_neighborhood)
        )
        excluded = tuple(sorted(set(all_runtimes) - set(selected)))
        return RetrievalScopeFrame(
            bounded_retrieval_neighborhood=selected,
            affected_runtime_only_retrieval=set(affected_runtimes).issubset(set(selected)),
            dependency_depth_cap=radius.max_dependency_distance,
            architecture_isolation_aware_retrieval=architecture_isolation
            or bool(radius.isolated_runtime_boundaries),
            repo_wide_retrieval_forbidden=True,
            excluded_runtimes=excluded,
            summary_only=True,
            local_only=True,
            no_ast_replay=True,
            no_dynamic_tracing=True,
            no_automatic_repo_wide_indexing=True,
        )
