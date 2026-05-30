from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.bounded_retention import GovernanceBoundedRetentionPrimitive
from ai_dev_os.observation_review import RuntimeReadinessFrame
from ai_dev_os.operator_review import OperatorReviewFrame

MAX_MERGE_HISTORY_RETENTION = 4
MAX_MERGE_REASONS = 8
SUPPORTED_MERGE_READINESS_STATUSES = (
    "NOT_READY",
    "READY_WITH_WARNINGS",
    "READY",
)
SUPPORTED_MERGE_RECOMMENDATIONS = (
    "DO_NOT_MERGE",
    "REVIEW_BEFORE_MERGE",
    "MERGE_CANDIDATE",
)


@dataclass(frozen=True)
class MergeReadinessFrame:
    merge_readiness_active: bool
    status: str
    recommendation: str
    reasons: tuple[str, ...]
    retained_merge_history: tuple[str, ...]
    evicted_merge_history: tuple[str, ...]
    retention_limit: int
    readiness_score: int
    risk_level: str
    action: str
    blocker_count: int
    warning_count: int
    continuation_stability: str
    operator_status: str
    operator_priority: str
    requires_attention: bool
    deterministic: bool
    bounded: bool
    local_only: bool
    no_provider_calls: bool
    no_autonomous_execution: bool


class MergeReadinessRuntime:
    _RECOMMENDATION_BY_STATUS = {
        "NOT_READY": "DO_NOT_MERGE",
        "READY_WITH_WARNINGS": "REVIEW_BEFORE_MERGE",
        "READY": "MERGE_CANDIDATE",
    }

    def evaluate(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_history: tuple[str, ...] = (),
    ) -> MergeReadinessFrame:
        status = self._status_for(
            observation_review=observation_review,
            operator_review=operator_review,
        )
        recommendation = self._RECOMMENDATION_BY_STATUS[status]
        reasons = self._reasons_for(
            observation_review=observation_review,
            operator_review=operator_review,
            status=status,
        )
        history_entry = (
            f"status={status};recommendation={recommendation};"
            f"operator_status={operator_review.status}"
        )
        bounded_history = GovernanceBoundedRetentionPrimitive().apply(
            merge_history + (history_entry,),
            retention_limit=MAX_MERGE_HISTORY_RETENTION,
        )
        return MergeReadinessFrame(
            merge_readiness_active=True,
            status=status,
            recommendation=recommendation,
            reasons=reasons,
            retained_merge_history=bounded_history.retained_items,
            evicted_merge_history=bounded_history.evicted_items,
            retention_limit=MAX_MERGE_HISTORY_RETENTION,
            readiness_score=observation_review.readiness_score,
            risk_level=observation_review.risk_level,
            action=observation_review.action,
            blocker_count=observation_review.blocker_count,
            warning_count=len(observation_review.operational_warnings),
            continuation_stability=observation_review.continuation.continuation_stability,
            operator_status=operator_review.status,
            operator_priority=operator_review.priority,
            requires_attention=operator_review.requires_attention,
            deterministic=True,
            bounded=bounded_history.bounded_growth_maintained
            and len(reasons) <= MAX_MERGE_REASONS,
            local_only=True,
            no_provider_calls=True,
            no_autonomous_execution=True,
        )

    def _status_for(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
    ) -> str:
        if self._is_not_ready(
            observation_review=observation_review,
            operator_review=operator_review,
        ):
            return "NOT_READY"
        if self._is_ready(
            observation_review=observation_review,
            operator_review=operator_review,
        ):
            return "READY"
        return "READY_WITH_WARNINGS"

    def _is_ready(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
    ) -> bool:
        return all(
            (
                observation_review.risk_level == "LOW",
                observation_review.blocker_count == 0,
                operator_review.requires_attention is False,
                observation_review.readiness_score >= 80,
                observation_review.continuation.continuation_stability == "STABLE",
            )
        )

    def _is_not_ready(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
    ) -> bool:
        return any(
            (
                observation_review.blocker_count > 0,
                observation_review.action in {
                    "THROTTLE",
                    "PAUSE_REVIEW",
                    "OPERATOR_ATTENTION",
                },
                operator_review.status in {"REVIEW_REQUIRED", "CRITICAL"},
                observation_review.risk_level in {"HIGH", "CRITICAL"},
                observation_review.continuation.continuation_stability == "UNSTABLE",
            )
        )

    def _reasons_for(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        status: str,
    ) -> tuple[str, ...]:
        reasons: list[str] = []
        warning_count = len(observation_review.operational_warnings)
        if status == "NOT_READY":
            ordered_reasons = (
                ("BLOCKERS_PRESENT", observation_review.blocker_count > 0),
                ("ESCALATION_ACTION_THROTTLE", observation_review.action == "THROTTLE"),
                ("ESCALATION_ACTION_PAUSE_REVIEW", observation_review.action == "PAUSE_REVIEW"),
                (
                    "ESCALATION_ACTION_OPERATOR_ATTENTION",
                    observation_review.action == "OPERATOR_ATTENTION",
                ),
                (
                    "OPERATOR_STATUS_REVIEW_REQUIRED",
                    operator_review.status == "REVIEW_REQUIRED",
                ),
                ("OPERATOR_STATUS_CRITICAL", operator_review.status == "CRITICAL"),
                ("RISK_LEVEL_HIGH", observation_review.risk_level == "HIGH"),
                ("RISK_LEVEL_CRITICAL", observation_review.risk_level == "CRITICAL"),
                (
                    "CONTINUATION_UNSTABLE",
                    observation_review.continuation.continuation_stability == "UNSTABLE",
                ),
            )
        elif status == "READY":
            ordered_reasons = (
                ("LOW_RISK_CONFIRMED", observation_review.risk_level == "LOW"),
                ("NO_BLOCKERS_PRESENT", observation_review.blocker_count == 0),
                ("OPERATOR_REVIEW_NORMAL", operator_review.status == "NORMAL"),
                ("READINESS_SCORE_READY", observation_review.readiness_score >= 80),
                (
                    "CONTINUATION_STABLE",
                    observation_review.continuation.continuation_stability == "STABLE",
                ),
            )
        else:
            ordered_reasons = (
                ("RISK_LEVEL_MODERATE", observation_review.risk_level == "MODERATE"),
                ("READINESS_BELOW_READY_THRESHOLD", observation_review.readiness_score < 80),
                ("OPERATOR_STATUS_ATTENTION", operator_review.status == "ATTENTION"),
                ("WARNINGS_PRESENT", warning_count > 0),
            )
        for reason, active in ordered_reasons:
            if active:
                reasons.append(reason)
        if not reasons:
            reasons.append("MERGE_REVIEW_REQUIRED")
        return tuple(reasons[:MAX_MERGE_REASONS])


__all__ = [
    "MAX_MERGE_HISTORY_RETENTION",
    "MAX_MERGE_REASONS",
    "MergeReadinessFrame",
    "MergeReadinessRuntime",
    "SUPPORTED_MERGE_READINESS_STATUSES",
    "SUPPORTED_MERGE_RECOMMENDATIONS",
]
