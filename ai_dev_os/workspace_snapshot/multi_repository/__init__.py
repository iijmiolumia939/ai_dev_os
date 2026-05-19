from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.workspace_snapshot._workspace_utils import (
    discover_repositories,
    has_any_marker,
    read_text_if_exists,
)


@dataclass(frozen=True)
class MultiRepositoryFrame:
    repository_relationships: tuple[str, ...]
    ai_dev_os_consumer_repos: tuple[str, ...]
    isolated_repos: tuple[str, ...]
    stale_repos: tuple[str, ...]
    migration_state: dict[str, str]
    adapter_compatibility_state: dict[str, str]
    governance_compatibility: dict[str, str]
    repository_dependency_graph_summary: tuple[str, ...]
    bounded: bool
    read_only: bool


class MultiRepositoryPolicy:
    def map(
        self, workspace: str | Path = ".", *, max_repositories: int = 8
    ) -> MultiRepositoryFrame:
        repositories = discover_repositories(workspace, max_repositories=max_repositories)
        consumers: list[str] = []
        isolated: list[str] = []
        stale: list[str] = []
        relationships: list[str] = []
        migration: dict[str, str] = {}
        adapter_state: dict[str, str] = {}
        governance_state: dict[str, str] = {}

        for repository in repositories:
            metadata = self._bounded_metadata(repository.path)
            is_consumer = has_any_marker(metadata, ("ai-dev-os", "ai_dev_os"))
            has_governance = has_any_marker(metadata, ("governance", "runtime_audit"))
            has_adapter = has_any_marker(metadata, ("adapter", "provider", "integration"))
            if repository.name == "ai_dev_os":
                migration[repository.name] = "platform"
                governance_state[repository.name] = "source"
                adapter_state[repository.name] = "source"
                relationships.append("ai_dev_os: platform")
            elif is_consumer:
                consumers.append(repository.name)
                migration[repository.name] = "consumer-linked"
                governance_state[repository.name] = (
                    "compatible" if has_governance else "consumer-light"
                )
                adapter_state[repository.name] = "adapter-aware" if has_adapter else "not-declared"
                relationships.append(f"ai_dev_os -> {repository.name}: consumer")
            else:
                isolated.append(repository.name)
                migration[repository.name] = "isolated"
                governance_state[repository.name] = "isolated"
                adapter_state[repository.name] = "isolated"
                relationships.append(f"{repository.name}: isolated")
            if has_any_marker(metadata, ("legacy", "deprecated", "stale")):
                stale.append(repository.name)

        graph = (
            f"nodes={len(repositories)}",
            f"consumer_edges={len(consumers)}",
            f"isolated={len(isolated)}",
            f"stale={len(stale)}",
        )
        return MultiRepositoryFrame(
            repository_relationships=tuple(relationships),
            ai_dev_os_consumer_repos=tuple(consumers),
            isolated_repos=tuple(isolated),
            stale_repos=tuple(stale),
            migration_state=migration,
            adapter_compatibility_state=adapter_state,
            governance_compatibility=governance_state,
            repository_dependency_graph_summary=graph,
            bounded=len(repositories) <= max_repositories,
            read_only=True,
        )

    def _bounded_metadata(self, repository: Path) -> str:
        files = ("pyproject.toml", "README.md", "AGENTS.md", ".github/copilot-instructions.md")
        return "\n".join(read_text_if_exists(repository / file_name) for file_name in files)
