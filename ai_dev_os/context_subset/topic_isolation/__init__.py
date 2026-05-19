from __future__ import annotations

from dataclasses import dataclass

TOPIC_MARKERS = {
    "architecture_redesign": ("architecture", "redesign", "boundary", "hotspot"),
    "provider_migration": ("provider", "adapter", "migration", "sdk"),
    "renderer_authority": ("renderer", "unity", "live2d", "authority"),
    "governance_redesign": ("governance", "policy", "budget", "audit"),
    "rollout_strategy": ("rollout", "adoption", "consumer", "migration"),
    "experimental_runtime_spread": ("experimental", "prototype", "spread"),
    "ci_debt_review": ("ci", "lint", "format", "failure", "debt"),
}


@dataclass(frozen=True)
class TopicIsolationFrame:
    isolated_topics: tuple[str, ...]
    active_topics: tuple[str, ...]
    deferred_topics: tuple[str, ...]
    fork_session_required: bool
    architecture_session_required: bool
    summary_only: bool


class TopicIsolationPolicy:
    def isolate(
        self,
        topics: tuple[str, ...],
        *,
        session_type: str = "implementation",
        architecture_severity: str = "low",
    ) -> TopicIsolationFrame:
        detected = tuple(
            dict.fromkeys(self._topic_for(text) for text in topics if self._topic_for(text))
        )
        active_allowed = self._allowed_topics(session_type)
        isolated = tuple(topic for topic in detected if topic not in active_allowed)
        active = tuple(topic for topic in detected if topic in active_allowed)
        deferred = tuple(topic for topic in isolated if topic != "ci_debt_review")
        architecture_required = architecture_severity in {"high", "critical"} or any(
            topic in isolated for topic in ("architecture_redesign", "governance_redesign")
        )
        fork_required = architecture_required or len(isolated) >= 2
        return TopicIsolationFrame(
            isolated_topics=isolated,
            active_topics=active or ("implementation",),
            deferred_topics=deferred,
            fork_session_required=fork_required,
            architecture_session_required=architecture_required,
            summary_only=True,
        )

    def _topic_for(self, text: str) -> str:
        normalized = text.lower()
        for topic, markers in TOPIC_MARKERS.items():
            if any(marker in normalized for marker in markers):
                return topic
        return ""

    def _allowed_topics(self, session_type: str) -> tuple[str, ...]:
        if session_type == "architecture":
            return ("architecture_redesign", "governance_redesign")
        if session_type == "rollout":
            return ("rollout_strategy", "ci_debt_review")
        if session_type == "provider":
            return ("provider_migration", "ci_debt_review")
        if session_type == "renderer":
            return ("renderer_authority", "ci_debt_review")
        if session_type == "governance":
            return ("governance_redesign", "ci_debt_review")
        if session_type == "debugging":
            return ("ci_debt_review",)
        return ("ci_debt_review",)
