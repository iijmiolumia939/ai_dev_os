from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.context_subset.continuity_scope import ContinuityScopeFrame
from ai_dev_os.context_subset.repository_subset import RepositorySubsetFrame
from ai_dev_os.context_subset.session_focus import SessionFocusFrame
from ai_dev_os.context_subset.topic_isolation import TopicIsolationFrame
from ai_dev_os.repository_intelligence.validation_collector import ValidationCollectorFrame
from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotFrame


@dataclass(frozen=True)
class SessionModeRouterFrame:
    recommended_mode: str
    fallback_mode: str
    escalation_required: bool
    compact_mode: bool
    isolation_required: bool
    recommended_prompt_type: str


class SessionModeRouterPolicy:
    def route(
        self,
        *,
        session_focus: SessionFocusFrame,
        topic_isolation: TopicIsolationFrame,
        continuity_scope: ContinuityScopeFrame,
        repository_subset: RepositorySubsetFrame,
        architecture_hotspots: ArchitectureHotspotFrame,
        validation: ValidationCollectorFrame,
    ) -> SessionModeRouterFrame:
        recommended = self._recommended_mode(session_focus, topic_isolation, architecture_hotspots)
        if validation.remote_ci_summary not in {"success", "not_checked", "unknown"}:
            recommended = "debugging"
        fallback = "bounded_implementation"
        isolation = recommended == "isolated_architecture" or topic_isolation.fork_session_required
        compact = continuity_scope.summary_only_required or repository_subset.summary_only
        prompt_type = self._prompt_type(recommended)
        return SessionModeRouterFrame(
            recommended_mode=recommended,
            fallback_mode=fallback,
            escalation_required=session_focus.escalation_required,
            compact_mode=compact,
            isolation_required=isolation,
            recommended_prompt_type=prompt_type,
        )

    def _recommended_mode(
        self,
        session_focus: SessionFocusFrame,
        topic_isolation: TopicIsolationFrame,
        architecture_hotspots: ArchitectureHotspotFrame,
    ) -> str:
        if (
            topic_isolation.architecture_session_required
            or architecture_hotspots.risk_severity == "critical"
        ):
            return "isolated_architecture"
        if session_focus.primary_focus == "rollout":
            return "rollout_review"
        if session_focus.primary_focus == "governance":
            return "governance_review"
        if session_focus.primary_focus == "debugging":
            return "debugging"
        if session_focus.primary_focus == "provider":
            return "provider_analysis"
        if session_focus.primary_focus == "renderer":
            return "renderer_review"
        return "bounded_implementation"

    def _prompt_type(self, mode: str) -> str:
        if mode == "isolated_architecture":
            return "architecture_isolation"
        if mode in {"rollout_review", "governance_review"}:
            return "remote_verification"
        if mode == "debugging":
            return "patch_only"
        return "patch_only"
