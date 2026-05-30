from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.bounded_retention import GovernanceBoundedRetentionPrimitive
from ai_dev_os.governance_health.governance_dashboard import (
    GovernanceDashboardFrame,
    GovernanceDashboardPolicy,
)
from ai_dev_os.governance_health.health_score import GovernanceHealthFrame, GovernanceHealthPolicy
from ai_dev_os.governance_health.pressure_aggregation import (
    GovernancePressureFrame,
    GovernancePressurePolicy,
)
from ai_dev_os.governance_health.risk_aggregation import GovernanceRiskFrame, GovernanceRiskPolicy
from ai_dev_os.governance_health.stability_assessment import (
    GovernanceStabilityFrame,
    GovernanceStabilityPolicy,
)
from ai_dev_os.governance_trace import GovernanceTraceFrame
from ai_dev_os.merge_readiness import MergeReadinessFrame
from ai_dev_os.observation_review import RuntimeReadinessFrame
from ai_dev_os.operator_review import OperatorReviewFrame
from ai_dev_os.repository_readiness import RepositoryReadinessFrame
from ai_dev_os.validation_evidence import ValidationEvidenceFrame

MAX_HEALTH_HISTORY_RETENTION = 4
MAX_HEALTH_REASONS = 8
SUPPORTED_GOVERNANCE_HEALTH_STATUSES = (
    "HEALTHY",
    "DEGRADED",
    "UNHEALTHY",
)


@dataclass(frozen=True)
class GovernanceHealthRuntimeFrame:
    governance_health_active: bool
    status: str
    summary: str
    reasons: tuple[str, ...]
    retained_health_history: tuple[str, ...]
    evicted_health_history: tuple[str, ...]
    retention_limit: int
    readiness_score: int
    risk_level: str
    operator_status: str
    merge_status: str
    validation_status: str
    repository_status: str
    governance_trace_status: str
    governance_trace_root_cause: str
    deterministic: bool
    bounded: bool
    read_only: bool
    local_only: bool
    no_provider_calls: bool
    no_filesystem_access: bool
    no_process_execution: bool
    no_git_operations: bool
    no_autonomous_execution: bool


class GovernanceHealthRuntime:
    _SUMMARY_BY_STATUS = {
        "HEALTHY": "GOVERNANCE_HEALTHY",
        "DEGRADED": "GOVERNANCE_DEGRADED",
        "UNHEALTHY": "GOVERNANCE_UNHEALTHY",
    }

    def evaluate(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
        repository_readiness: RepositoryReadinessFrame,
        governance_trace: GovernanceTraceFrame,
        health_history: tuple[str, ...] = (),
    ) -> GovernanceHealthRuntimeFrame:
        status = self._status_for(
            merge_readiness=merge_readiness,
            validation_evidence=validation_evidence,
            repository_readiness=repository_readiness,
            governance_trace=governance_trace,
        )
        summary = self._SUMMARY_BY_STATUS[status]
        reasons = self._reasons_for(
            observation_review=observation_review,
            operator_review=operator_review,
            merge_readiness=merge_readiness,
            validation_evidence=validation_evidence,
            repository_readiness=repository_readiness,
            governance_trace=governance_trace,
        )
        history_entry = (
            f"status={status};summary={summary};"
            f"repository_status={repository_readiness.status};"
            f"validation_status={validation_evidence.status};"
            f"merge_status={merge_readiness.status};"
            f"trace_status={governance_trace.status};"
            f"operator_status={operator_review.status};"
            f"risk_level={observation_review.risk_level};"
            f"readiness_score={observation_review.readiness_score};"
            f"root_cause={governance_trace.root_cause};"
            f"reasons={'|'.join(reasons)}"
        )
        bounded_history = GovernanceBoundedRetentionPrimitive().apply(
            health_history + (history_entry,),
            retention_limit=MAX_HEALTH_HISTORY_RETENTION,
        )
        return GovernanceHealthRuntimeFrame(
            governance_health_active=True,
            status=status,
            summary=summary,
            reasons=reasons,
            retained_health_history=bounded_history.retained_items,
            evicted_health_history=bounded_history.evicted_items,
            retention_limit=MAX_HEALTH_HISTORY_RETENTION,
            readiness_score=observation_review.readiness_score,
            risk_level=observation_review.risk_level,
            operator_status=operator_review.status,
            merge_status=merge_readiness.status,
            validation_status=validation_evidence.status,
            repository_status=repository_readiness.status,
            governance_trace_status=governance_trace.status,
            governance_trace_root_cause=governance_trace.root_cause,
            deterministic=True,
            bounded=bounded_history.bounded_growth_maintained
            and len(reasons) <= MAX_HEALTH_REASONS,
            read_only=True,
            local_only=True,
            no_provider_calls=True,
            no_filesystem_access=True,
            no_process_execution=True,
            no_git_operations=True,
            no_autonomous_execution=True,
        )

    def _status_for(
        self,
        *,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
        repository_readiness: RepositoryReadinessFrame,
        governance_trace: GovernanceTraceFrame,
    ) -> str:
        if any(
            (
                repository_readiness.status == "NOT_READY",
                validation_evidence.status == "FAILED",
                merge_readiness.status == "NOT_READY",
                governance_trace.status == "TRACE_INCOMPLETE",
            )
        ):
            return "UNHEALTHY"
        if all(
            (
                repository_readiness.status == "READY",
                validation_evidence.status == "PASSED",
                merge_readiness.status == "READY",
                governance_trace.status == "TRACE_AVAILABLE",
            )
        ):
            return "HEALTHY"
        if any(
            (
                repository_readiness.status == "READY_WITH_WARNINGS",
                validation_evidence.status == "PASSED_WITH_WARNINGS",
                merge_readiness.status == "READY_WITH_WARNINGS",
            )
        ):
            return "DEGRADED"
        return "DEGRADED"

    def _reasons_for(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
        repository_readiness: RepositoryReadinessFrame,
        governance_trace: GovernanceTraceFrame,
    ) -> tuple[str, ...]:
        ordered_reasons = (
            ("REPOSITORY_NOT_READY", repository_readiness.status == "NOT_READY"),
            ("VALIDATION_FAILED", validation_evidence.status == "FAILED"),
            ("MERGE_NOT_READY", merge_readiness.status == "NOT_READY"),
            ("TRACE_INCOMPLETE", governance_trace.status == "TRACE_INCOMPLETE"),
            (
                "REPOSITORY_READY_WITH_WARNINGS",
                repository_readiness.status == "READY_WITH_WARNINGS",
            ),
            (
                "VALIDATION_PASSED_WITH_WARNINGS",
                validation_evidence.status == "PASSED_WITH_WARNINGS",
            ),
            ("MERGE_READY_WITH_WARNINGS", merge_readiness.status == "READY_WITH_WARNINGS"),
            ("READINESS_BELOW_READY_THRESHOLD", observation_review.readiness_score < 80),
            (f"OPERATOR_STATUS_{operator_review.status}", operator_review.status != "NORMAL"),
            (
                f"RISK_LEVEL_{observation_review.risk_level}",
                observation_review.risk_level != "LOW",
            ),
            (
                f"ROOT_CAUSE_{self._normalize_reason_token(governance_trace.root_cause)}",
                True,
            ),
        )
        reasons = tuple(reason for reason, active in ordered_reasons if active)
        return reasons[:MAX_HEALTH_REASONS]

    def _normalize_reason_token(self, value: str) -> str:
        normalized = "".join(
            character if character.isalnum() else "_"
            for character in value.upper()
        ).strip("_")
        return normalized or "UNSPECIFIED"


__all__ = [
    "GovernanceDashboardFrame",
    "GovernanceDashboardPolicy",
    "GovernanceHealthFrame",
    "GovernanceHealthPolicy",
    "GovernanceHealthRuntime",
    "GovernanceHealthRuntimeFrame",
    "GovernancePressureFrame",
    "GovernancePressurePolicy",
    "GovernanceRiskFrame",
    "GovernanceRiskPolicy",
    "GovernanceStabilityFrame",
    "GovernanceStabilityPolicy",
    "MAX_HEALTH_HISTORY_RETENTION",
    "MAX_HEALTH_REASONS",
    "SUPPORTED_GOVERNANCE_HEALTH_STATUSES",
]
