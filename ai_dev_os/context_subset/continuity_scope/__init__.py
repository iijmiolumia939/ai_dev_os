from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.context_subset.repository_subset import RepositorySubsetFrame
from ai_dev_os.context_subset.topic_isolation import TopicIsolationFrame


@dataclass(frozen=True)
class ContinuityScopeFrame:
    included_context: tuple[str, ...]
    excluded_context: tuple[str, ...]
    continuity_depth: str
    continuity_budget: int
    summary_only_required: bool


class ContinuityScopePolicy:
    def scope(
        self,
        *,
        repository_subset: RepositorySubsetFrame,
        topic_isolation: TopicIsolationFrame,
        active_tests: tuple[str, ...] = (),
        deployment_required: bool = False,
        rollout_required: bool = False,
        max_budget: int = 2_400,
    ) -> ContinuityScopeFrame:
        included = ["active_sprint_continuity"]
        if repository_subset.active_repositories:
            included.append("repository_subset")
        if repository_subset.continuity_priority:
            included.append("required_runtime_continuity")
        if active_tests:
            included.append("test_continuity")
        if topic_isolation.architecture_session_required:
            included.append("architecture_continuity_summary")
        if deployment_required:
            included.append("deployment_continuity")
        if rollout_required or repository_subset.rollout_related_repositories:
            included.append("rollout_continuity")

        excluded = ["full_workspace_continuation", "giant_continuity_summary"]
        excluded.extend(f"stale_repo:{repo}" for repo in repository_subset.stale_repositories)
        excluded.extend(f"deferred_topic:{topic}" for topic in topic_isolation.deferred_topics)
        if repository_subset.excluded_repositories:
            excluded.append("inactive_repository_details")
        depth = self._depth(len(included), topic_isolation.fork_session_required)
        budget = min(max_budget, 400 + len(included) * 180)
        return ContinuityScopeFrame(
            included_context=tuple(dict.fromkeys(included)),
            excluded_context=tuple(dict.fromkeys(excluded)),
            continuity_depth=depth,
            continuity_budget=budget,
            summary_only_required=True,
        )

    def _depth(self, included_count: int, fork_required: bool) -> str:
        if fork_required:
            return "isolated-summary"
        if included_count >= 5:
            return "bounded"
        return "minimal"
