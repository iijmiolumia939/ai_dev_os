from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.bounded_retention import GovernanceBoundedRetentionPrimitive
from ai_dev_os.observation_review import RuntimeReadinessFrame

MAX_REVIEW_HISTORY_RETENTION = 4
SUPPORTED_OPERATOR_REVIEW_STATUSES = (
    "NORMAL",
    "ATTENTION",
    "REVIEW_REQUIRED",
    "CRITICAL",
)
SUPPORTED_OPERATOR_REVIEW_PRIORITIES = (
    "LOW",
    "MEDIUM",
    "HIGH",
    "URGENT",
)
MAX_OPERATOR_REASONS = 8


@dataclass(frozen=True)
class OperatorReviewFrame:
    operator_review_active: bool
    status: str
    priority: str
    requires_attention: bool
    reasons: tuple[str, ...]
    retained_review_history: tuple[str, ...]
    evicted_review_history: tuple[str, ...]
    retention_limit: int
    readiness_score: int
    risk_level: str
    escalation_action: str
    blocker_count: int
    warning_count: int
    continuation_stability: str
    deterministic: bool
    bounded: bool
    local_only: bool
    no_provider_calls: bool
    no_autonomous_execution: bool


class OperatorReviewRuntime:
    _PRIORITY_BY_STATUS = {
        "NORMAL": "LOW",
        "ATTENTION": "MEDIUM",
        "REVIEW_REQUIRED": "HIGH",
        "CRITICAL": "URGENT",
    }

    def evaluate(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        review_history: tuple[str, ...] = (),
    ) -> OperatorReviewFrame:
        status = self._status_for(observation_review=observation_review)
        priority = self._PRIORITY_BY_STATUS[status]
        reasons = self._reasons_for(observation_review=observation_review, status=status)
        requires_attention = status != "NORMAL"
        history_entry = (
            f"status={status};priority={priority};attention={str(requires_attention).lower()}"
        )
        bounded_history = GovernanceBoundedRetentionPrimitive().apply(
            review_history + (history_entry,),
            retention_limit=MAX_REVIEW_HISTORY_RETENTION,
        )
        return OperatorReviewFrame(
            operator_review_active=True,
            status=status,
            priority=priority,
            requires_attention=requires_attention,
            reasons=reasons,
            retained_review_history=bounded_history.retained_items,
            evicted_review_history=bounded_history.evicted_items,
            retention_limit=MAX_REVIEW_HISTORY_RETENTION,
            readiness_score=observation_review.readiness_score,
            risk_level=observation_review.risk_level,
            escalation_action=observation_review.action,
            blocker_count=observation_review.blocker_count,
            warning_count=len(observation_review.operational_warnings),
            continuation_stability=observation_review.continuation.continuation_stability,
            deterministic=True,
            bounded=bounded_history.bounded_growth_maintained
            and len(reasons) <= MAX_OPERATOR_REASONS,
            local_only=True,
            no_provider_calls=True,
            no_autonomous_execution=True,
        )

    def _status_for(self, *, observation_review: RuntimeReadinessFrame) -> str:
        if (
            observation_review.action == "OPERATOR_ATTENTION"
            or observation_review.risk_level == "CRITICAL"
        ):
            return "CRITICAL"
        if (
            observation_review.action in {"THROTTLE", "PAUSE_REVIEW"}
            or observation_review.risk_level == "HIGH"
            or observation_review.blocker_count > 0
            or observation_review.continuation.continuation_stability == "UNSTABLE"
        ):
            return "REVIEW_REQUIRED"
        if (
            observation_review.action == "MONITOR"
            or observation_review.risk_level == "MODERATE"
            or observation_review.readiness_score < 80
            or len(observation_review.operational_warnings) > 0
            or observation_review.continuation.continuation_stability == "GUARDED"
        ):
            return "ATTENTION"
        return "NORMAL"

    def _reasons_for(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        status: str,
    ) -> tuple[str, ...]:
        reasons: list[str] = []
        ordered_reasons = (
            (
                "ESCALATION_ACTION_OPERATOR_ATTENTION",
                observation_review.action == "OPERATOR_ATTENTION",
            ),
            ("RISK_LEVEL_CRITICAL", observation_review.risk_level == "CRITICAL"),
            ("ESCALATION_ACTION_PAUSE_REVIEW", observation_review.action == "PAUSE_REVIEW"),
            ("ESCALATION_ACTION_THROTTLE", observation_review.action == "THROTTLE"),
            ("RISK_LEVEL_HIGH", observation_review.risk_level == "HIGH"),
            ("BLOCKERS_PRESENT", observation_review.blocker_count > 0),
            (
                "CONTINUATION_UNSTABLE",
                observation_review.continuation.continuation_stability == "UNSTABLE",
            ),
            ("ESCALATION_ACTION_MONITOR", observation_review.action == "MONITOR"),
            ("RISK_LEVEL_MODERATE", observation_review.risk_level == "MODERATE"),
            ("READINESS_BELOW_ATTENTION_THRESHOLD", observation_review.readiness_score < 80),
            ("WARNINGS_PRESENT", len(observation_review.operational_warnings) > 0),
            (
                "CONTINUATION_GUARDED",
                observation_review.continuation.continuation_stability == "GUARDED",
            ),
        )
        for reason, active in ordered_reasons:
            if active:
                reasons.append(reason)
        if not reasons and status == "NORMAL":
            reasons.append("NORMAL_OPERATIONAL_WINDOW")
        return tuple(reasons[:MAX_OPERATOR_REASONS])


__all__ = [
    "MAX_OPERATOR_REASONS",
    "MAX_REVIEW_HISTORY_RETENTION",
    "OperatorReviewFrame",
    "OperatorReviewRuntime",
    "SUPPORTED_OPERATOR_REVIEW_PRIORITIES",
    "SUPPORTED_OPERATOR_REVIEW_STATUSES",
]
