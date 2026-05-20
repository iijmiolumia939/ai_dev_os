from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GovernanceDashboardFrame:
    governance_health: str
    pressure_summary: str
    risk_summary: str
    active_warnings: tuple[str, ...]
    stale_session_state: str
    persistence_budget_state: str
    checkpoint_pressure: str
    architecture_isolation_state: str
    workspace_cleanliness: str
    rollout_stability: str
    summary_only: bool
    raw_runtime_replay_allowed: bool


class GovernanceDashboardPolicy:
    def build(
        self,
        *,
        health: Any,
        pressure: Any,
        risk: Any,
        stale_session_active: bool,
        persistence_budget_state: str,
        checkpoint_pressure: str,
        architecture_isolation_required: bool,
        workspace_dirty: bool,
        rollout_stability: str,
    ) -> GovernanceDashboardFrame:
        warnings = []
        if getattr(health, "governance_attention_required", False):
            warnings.append("governance attention required")
        if getattr(pressure, "bounded_operation_recommended", False):
            warnings.append("bounded operation recommended")
        if getattr(risk, "compact_recommended", False):
            warnings.append("compact governance context recommended")
        if stale_session_active:
            warnings.append("stale session state detected")
        if workspace_dirty:
            warnings.append("workspace cleanliness review needed")
        return GovernanceDashboardFrame(
            governance_health=getattr(health, "governance_health_state", "UNKNOWN"),
            pressure_summary=(
                f"aggregate={getattr(pressure, 'aggregate_pressure', 'unknown')}; "
                f"dominant={getattr(pressure, 'dominant_pressure', 'unknown')}"
            ),
            risk_summary=(
                f"aggregate={getattr(risk, 'aggregate_risk', 'unknown')}; "
                f"highest={getattr(risk, 'highest_risk', 'unknown')}"
            ),
            active_warnings=tuple(warnings),
            stale_session_state="active" if stale_session_active else "clear",
            persistence_budget_state=persistence_budget_state,
            checkpoint_pressure=checkpoint_pressure,
            architecture_isolation_state=(
                "recommended" if architecture_isolation_required else "not_required"
            ),
            workspace_cleanliness="dirty" if workspace_dirty else "clean",
            rollout_stability=rollout_stability,
            summary_only=True,
            raw_runtime_replay_allowed=False,
        )
