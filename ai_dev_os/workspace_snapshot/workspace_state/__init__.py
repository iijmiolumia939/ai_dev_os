from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.repository_intelligence.git_collector import GitCollector
from ai_dev_os.workspace_snapshot._workspace_utils import discover_repositories


@dataclass(frozen=True)
class WorkspaceStateFrame:
    active_repositories: tuple[str, ...]
    current_sprint: str
    modified_repositories: tuple[str, ...]
    dirty_runtime_counts: dict[str, int]
    dirty_governance_counts: dict[str, int]
    dirty_adapter_counts: dict[str, int]
    untracked_artifact_counts: dict[str, int]
    architecture_review_pending: bool
    rollout_state: str
    continuity_state: str
    bounded_summary: tuple[str, ...]
    read_only: bool


class WorkspaceStatePolicy:
    def snapshot(
        self,
        workspace: str | Path = ".",
        *,
        current_sprint: str = "next",
        max_repositories: int = 8,
    ) -> WorkspaceStateFrame:
        repositories = discover_repositories(workspace, max_repositories=max_repositories)
        git = GitCollector()
        modified: list[str] = []
        runtime_counts: dict[str, int] = {}
        governance_counts: dict[str, int] = {}
        adapter_counts: dict[str, int] = {}
        artifact_counts: dict[str, int] = {}

        for repository in repositories:
            frame = git.collect(repository.path)
            changed_paths = frame.changed_runtime_paths + frame.changed_test_paths
            governance_paths = frame.changed_governance_paths
            adapter_paths = tuple(
                path
                for path in changed_paths
                if "adapter" in path or "provider" in path or "integrations" in path
            )
            artifact_paths = tuple(
                path
                for path in self._changed_paths(frame)
                if path.endswith((".log", ".tmp", ".json"))
                or path.startswith(("dist/", "build/", ".pytest_cache/", ".ruff_cache/"))
            )
            if changed_paths or governance_paths or frame.untracked_file_count:
                modified.append(repository.name)
            runtime_counts[repository.name] = len(changed_paths)
            governance_counts[repository.name] = len(governance_paths)
            adapter_counts[repository.name] = len(adapter_paths)
            artifact_counts[repository.name] = len(artifact_paths)

        architecture_pending = any(runtime_counts.values()) and any(governance_counts.values())
        rollout_state = (
            "active" if "ai_dev_os" in [repo.name for repo in repositories] else "external"
        )
        continuity_state = "bounded" if len(repositories) <= max_repositories else "truncated"
        summary = (
            f"repositories={len(repositories)}",
            f"modified={len(modified)}",
            f"dirty_runtime={sum(runtime_counts.values())}",
            f"dirty_governance={sum(governance_counts.values())}",
            f"dirty_adapters={sum(adapter_counts.values())}",
            f"untracked_artifacts={sum(artifact_counts.values())}",
        )
        return WorkspaceStateFrame(
            active_repositories=tuple(repo.name for repo in repositories),
            current_sprint=current_sprint,
            modified_repositories=tuple(modified),
            dirty_runtime_counts=runtime_counts,
            dirty_governance_counts=governance_counts,
            dirty_adapter_counts=adapter_counts,
            untracked_artifact_counts=artifact_counts,
            architecture_review_pending=architecture_pending,
            rollout_state=rollout_state,
            continuity_state=continuity_state,
            bounded_summary=summary,
            read_only=True,
        )

    def _changed_paths(self, frame) -> tuple[str, ...]:
        return (
            frame.changed_runtime_paths + frame.changed_test_paths + frame.changed_governance_paths
        )
