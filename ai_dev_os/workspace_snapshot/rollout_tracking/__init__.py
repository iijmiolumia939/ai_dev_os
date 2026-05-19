from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.workspace_snapshot._workspace_utils import discover_repositories
from ai_dev_os.workspace_snapshot.multi_repository import (
    MultiRepositoryFrame,
    MultiRepositoryPolicy,
)


@dataclass(frozen=True)
class RolloutTrackingFrame:
    ai_dev_os_version: str
    rollout_stage: str
    consumer_adoption_status: dict[str, str]
    migration_completeness: float
    adapter_certification_state: dict[str, str]
    runtime_audit_coverage: float
    session_lifecycle_coverage: float
    rollout_risk_summary: tuple[str, ...]
    read_only: bool


class RolloutTrackingPolicy:
    def track(self, workspace: str | Path = ".") -> RolloutTrackingFrame:
        multi = MultiRepositoryPolicy().map(workspace)
        repositories = discover_repositories(workspace)
        version = self._version_for_workspace(workspace, repositories)
        adoption = {repo: "adopted" for repo in multi.ai_dev_os_consumer_repos} | {
            repo: "isolated" for repo in multi.isolated_repos
        }
        total = max(1, len(repositories) - 1)
        completeness = round(len(multi.ai_dev_os_consumer_repos) / total, 4)
        adapter_certification = {
            repo: self._adapter_certification(state)
            for repo, state in multi.adapter_compatibility_state.items()
        }
        runtime_audit_coverage = self._coverage(multi, marker="governance")
        session_lifecycle_coverage = self._coverage(multi, marker="compatible")
        risks = self._risks(multi, completeness)
        stage = "platform" if version != "unknown" else "workspace"
        if multi.ai_dev_os_consumer_repos:
            stage = "consumer-rollout"
        return RolloutTrackingFrame(
            ai_dev_os_version=version,
            rollout_stage=stage,
            consumer_adoption_status=adoption,
            migration_completeness=completeness,
            adapter_certification_state=adapter_certification,
            runtime_audit_coverage=runtime_audit_coverage,
            session_lifecycle_coverage=session_lifecycle_coverage,
            rollout_risk_summary=risks,
            read_only=True,
        )

    def _version_for_workspace(self, workspace: str | Path, repositories) -> str:
        candidates = [Path(workspace).resolve() / "pyproject.toml"]
        candidates.extend(
            repo.path / "pyproject.toml" for repo in repositories if repo.name == "ai_dev_os"
        )
        for path in candidates:
            if path.exists():
                data = tomllib.loads(path.read_text(encoding="utf-8"))
                return str(data.get("project", {}).get("version", "unknown"))
        return "unknown"

    def _adapter_certification(self, state: str) -> str:
        if state in {"source", "adapter-aware"}:
            return "certification-ready"
        if state == "isolated":
            return "not-applicable"
        return "not-declared"

    def _coverage(self, multi: MultiRepositoryFrame, *, marker: str) -> float:
        states = tuple(multi.governance_compatibility.values())
        if not states:
            return 0.0
        covered = sum(1 for state in states if marker in state or state == "source")
        return round(covered / len(states), 4)

    def _risks(self, multi: MultiRepositoryFrame, completeness: float) -> tuple[str, ...]:
        risks = []
        if multi.stale_repos:
            risks.append("stale repositories require bounded rollover notes")
        if multi.isolated_repos:
            risks.append("isolated repositories excluded from AI_DEV_OS continuity")
        if completeness < 1.0:
            risks.append("consumer rollout incomplete")
        return tuple(risks or ("no rollout risk detected",))
