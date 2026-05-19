from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.context_subset.topic_isolation import TopicIsolationFrame
from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotFrame

FOCUS_ORDER = (
    "implementation",
    "architecture",
    "rollout",
    "governance",
    "renderer",
    "provider",
    "debugging",
)


@dataclass(frozen=True)
class SessionFocusFrame:
    primary_focus: str
    secondary_focus: tuple[str, ...]
    excluded_focus: tuple[str, ...]
    escalation_required: bool
    focus_drift_risk: str
    recommended_session_type: str


class SessionFocusPolicy:
    def focus(
        self,
        *,
        requested_focus: str = "implementation",
        topic_isolation: TopicIsolationFrame,
        architecture_hotspots: ArchitectureHotspotFrame,
    ) -> SessionFocusFrame:
        primary = requested_focus if requested_focus in FOCUS_ORDER else "implementation"
        if topic_isolation.architecture_session_required:
            primary = "architecture"
        secondary = tuple(
            topic.replace("_redesign", "").replace("_strategy", "").replace("_migration", "")
            for topic in topic_isolation.active_topics
            if topic != primary
        )[:2]
        excluded = tuple(
            focus for focus in FOCUS_ORDER if focus != primary and focus not in secondary
        )
        escalation = architecture_hotspots.risk_severity in {"high", "critical"}
        drift = self._drift(topic_isolation, architecture_hotspots)
        recommended = "isolated-architecture" if escalation else f"bounded-{primary}"
        return SessionFocusFrame(
            primary_focus=primary,
            secondary_focus=secondary,
            excluded_focus=excluded,
            escalation_required=escalation,
            focus_drift_risk=drift,
            recommended_session_type=recommended,
        )

    def _drift(
        self,
        topic_isolation: TopicIsolationFrame,
        architecture_hotspots: ArchitectureHotspotFrame,
    ) -> str:
        if architecture_hotspots.risk_severity == "critical":
            return "critical"
        if topic_isolation.fork_session_required or architecture_hotspots.risk_severity == "high":
            return "high"
        if topic_isolation.isolated_topics:
            return "medium"
        return "low"
