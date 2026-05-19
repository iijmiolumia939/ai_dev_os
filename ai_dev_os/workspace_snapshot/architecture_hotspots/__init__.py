from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.workspace_snapshot.workspace_state import WorkspaceStateFrame, WorkspaceStatePolicy


@dataclass(frozen=True)
class ArchitectureHotspotFrame:
    broad_runtime_modifications: bool
    cross_boundary_modifications: bool
    giant_runtime_growth: bool
    governance_leakage_risk: bool
    renderer_authority_risk: bool
    provider_lock_in_risk: bool
    adapter_contamination_risk: bool
    experimental_runtime_spread: bool
    risk_severity: str
    review_recommendation: str
    isolation_recommendation: str
    hotspot_summary: tuple[str, ...]
    read_only: bool


class ArchitectureHotspotPolicy:
    def detect(
        self, workspace: str | Path = ".", *, state: WorkspaceStateFrame | None = None
    ) -> ArchitectureHotspotFrame:
        snapshot = state or WorkspaceStatePolicy().snapshot(workspace)
        runtime_total = sum(snapshot.dirty_runtime_counts.values())
        governance_total = sum(snapshot.dirty_governance_counts.values())
        adapter_total = sum(snapshot.dirty_adapter_counts.values())
        artifact_total = sum(snapshot.untracked_artifact_counts.values())
        modified_count = len(snapshot.modified_repositories)

        broad_runtime = runtime_total >= 5 or modified_count >= 3
        cross_boundary = modified_count >= 2 and runtime_total > 0
        giant_growth = artifact_total >= 5 or runtime_total >= 12
        governance_leakage = runtime_total > 0 and governance_total > 0
        renderer_authority = (
            any(
                "unity" in repo.lower() or "aituber" in repo.lower()
                for repo in snapshot.modified_repositories
            )
            and runtime_total > 0
        )
        provider_lock_in = adapter_total >= 2
        adapter_contamination = adapter_total > 0 and governance_total > 0
        experimental_spread = any(
            "experimental" in repo.lower() for repo in snapshot.modified_repositories
        )
        severity = self._severity(
            broad_runtime,
            cross_boundary,
            giant_growth,
            governance_leakage,
            renderer_authority,
            provider_lock_in,
            adapter_contamination,
            experimental_spread,
        )
        review = (
            "architecture_review_required"
            if severity in {"high", "critical"}
            else "bounded_review"
        )
        isolation = "isolate_architecture_session" if severity == "critical" else "same_session_ok"
        summary = (
            f"runtime_dirty={runtime_total}",
            f"governance_dirty={governance_total}",
            f"adapter_dirty={adapter_total}",
            f"modified_repositories={modified_count}",
            f"severity={severity}",
        )
        return ArchitectureHotspotFrame(
            broad_runtime_modifications=broad_runtime,
            cross_boundary_modifications=cross_boundary,
            giant_runtime_growth=giant_growth,
            governance_leakage_risk=governance_leakage,
            renderer_authority_risk=renderer_authority,
            provider_lock_in_risk=provider_lock_in,
            adapter_contamination_risk=adapter_contamination,
            experimental_runtime_spread=experimental_spread,
            risk_severity=severity,
            review_recommendation=review,
            isolation_recommendation=isolation,
            hotspot_summary=summary,
            read_only=True,
        )

    def _severity(self, *flags: bool) -> str:
        score = sum(1 for flag in flags if flag)
        if score >= 5:
            return "critical"
        if score >= 3:
            return "high"
        if score >= 1:
            return "medium"
        return "low"
