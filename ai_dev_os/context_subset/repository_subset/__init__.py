from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.repository_intelligence.runtime_discovery import RuntimeDiscoveryFrame
from ai_dev_os.repository_intelligence.sprint_metadata import SprintMetadataFrame
from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotFrame
from ai_dev_os.workspace_snapshot.multi_repository import MultiRepositoryFrame
from ai_dev_os.workspace_snapshot.workspace_state import WorkspaceStateFrame


@dataclass(frozen=True)
class RepositorySubsetFrame:
    active_repositories: tuple[str, ...]
    excluded_repositories: tuple[str, ...]
    stale_repositories: tuple[str, ...]
    architecture_sensitive_repositories: tuple[str, ...]
    rollout_related_repositories: tuple[str, ...]
    continuity_priority: tuple[str, ...]
    summary_only: bool
    full_workspace_continuation_blocked: bool


class RepositorySubsetPolicy:
    def select(
        self,
        *,
        workspace_state: WorkspaceStateFrame,
        multi_repository: MultiRepositoryFrame,
        sprint_metadata: SprintMetadataFrame,
        architecture_hotspots: ArchitectureHotspotFrame,
        runtime_discovery: RuntimeDiscoveryFrame,
        max_repositories: int = 3,
    ) -> RepositorySubsetFrame:
        active_candidates = list(workspace_state.modified_repositories)
        active_candidates.extend(multi_repository.ai_dev_os_consumer_repos)
        active_candidates.extend(
            repo for repo in workspace_state.active_repositories if repo == "ai_dev_os"
        )
        if not active_candidates:
            active_candidates.extend(workspace_state.active_repositories[:1])

        stale = tuple(
            repo
            for repo in multi_repository.stale_repos
            if repo in workspace_state.active_repositories
        )
        active = tuple(
            repo
            for repo in dict.fromkeys(active_candidates)
            if repo not in stale and repo not in multi_repository.isolated_repos
        )[:max_repositories]
        excluded = tuple(
            repo for repo in workspace_state.active_repositories if repo not in active
        )
        architecture_sensitive = self._architecture_sensitive(
            workspace_state,
            architecture_hotspots,
        )
        rollout_related = tuple(
            repo
            for repo in workspace_state.active_repositories
            if repo == "ai_dev_os" or repo in multi_repository.ai_dev_os_consumer_repos
        )
        priority = self._priority(
            active,
            sprint_metadata.affected_runtimes,
            runtime_discovery.runtime_packages,
        )
        return RepositorySubsetFrame(
            active_repositories=active,
            excluded_repositories=excluded,
            stale_repositories=stale,
            architecture_sensitive_repositories=architecture_sensitive,
            rollout_related_repositories=rollout_related,
            continuity_priority=priority,
            summary_only=True,
            full_workspace_continuation_blocked=len(active)
            < len(workspace_state.active_repositories),
        )

    def _architecture_sensitive(
        self,
        workspace_state: WorkspaceStateFrame,
        architecture_hotspots: ArchitectureHotspotFrame,
    ) -> tuple[str, ...]:
        if architecture_hotspots.risk_severity in {"high", "critical"}:
            return workspace_state.modified_repositories or workspace_state.active_repositories[:1]
        if (
            architecture_hotspots.governance_leakage_risk
            or architecture_hotspots.provider_lock_in_risk
        ):
            return workspace_state.modified_repositories
        return ()

    def _priority(
        self,
        active_repositories: tuple[str, ...],
        affected_runtimes: tuple[str, ...],
        runtime_packages: tuple[str, ...],
    ) -> tuple[str, ...]:
        runtime_hits = tuple(
            runtime
            for runtime in affected_runtimes
            if any(runtime in package for package in runtime_packages)
        )
        repo_hits = tuple(f"repo:{repo}" for repo in active_repositories)
        return repo_hits + tuple(f"runtime:{runtime}" for runtime in runtime_hits)
