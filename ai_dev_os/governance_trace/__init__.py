from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.bounded_retention import GovernanceBoundedRetentionPrimitive
from ai_dev_os.merge_readiness import (
    SUPPORTED_MERGE_READINESS_STATUSES,
    MergeReadinessFrame,
)
from ai_dev_os.observation_review import (
    SUPPORTED_OBSERVATION_RISK_LEVELS,
    RuntimeReadinessFrame,
)
from ai_dev_os.operator_review import (
    SUPPORTED_OPERATOR_REVIEW_STATUSES,
    OperatorReviewFrame,
)
from ai_dev_os.repository_readiness import (
    SUPPORTED_REPOSITORY_READINESS_STATUSES,
    RepositoryReadinessFrame,
)
from ai_dev_os.validation_evidence import (
    SUPPORTED_VALIDATION_EVIDENCE_STATUSES,
    ValidationEvidenceFrame,
)

MAX_TRACE_HISTORY_RETENTION = 4
MAX_TRACE_CHAIN_LENGTH = 5
SUPPORTED_GOVERNANCE_TRACE_STATUSES = (
    "TRACE_AVAILABLE",
    "TRACE_INCOMPLETE",
)
SUPPORTED_CONTINUATION_STABILITY = ("STABLE", "GUARDED", "UNSTABLE")


@dataclass(frozen=True)
class GovernanceTraceFrame:
    governance_trace_active: bool
    status: str
    root_cause: str
    trace_chain: tuple[str, ...]
    retained_trace_history: tuple[str, ...]
    evicted_trace_history: tuple[str, ...]
    retention_limit: int
    repository_status: str
    repository_recommendation: str
    merge_status: str
    merge_recommendation: str
    operator_status: str
    operator_priority: str
    validation_status: str
    validation_passed: bool
    risk_level: str
    readiness_score: int
    continuation_stability: str
    deterministic: bool
    bounded: bool
    read_only: bool
    local_only: bool
    no_provider_calls: bool
    no_filesystem_access: bool
    no_process_execution: bool
    no_git_operations: bool
    no_autonomous_execution: bool


class GovernanceTraceRuntime:
    def evaluate(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
        repository_readiness: RepositoryReadinessFrame,
        trace_history: tuple[str, ...] = (),
    ) -> GovernanceTraceFrame:
        trace_chain = self._trace_chain(
            observation_review=observation_review,
            operator_review=operator_review,
            merge_readiness=merge_readiness,
            repository_readiness=repository_readiness,
        )
        trace_status = self._trace_status(
            observation_review=observation_review,
            operator_review=operator_review,
            merge_readiness=merge_readiness,
            validation_evidence=validation_evidence,
            repository_readiness=repository_readiness,
            trace_chain=trace_chain,
        )
        root_cause = self._root_cause(
            trace_status=trace_status,
            observation_review=observation_review,
            operator_review=operator_review,
            merge_readiness=merge_readiness,
            validation_evidence=validation_evidence,
            repository_readiness=repository_readiness,
        )
        history_entry = (
            f"status={trace_status};root_cause={root_cause};"
            f"repository_status={repository_readiness.status};"
            f"repository_recommendation={repository_readiness.recommendation};"
            f"merge_status={merge_readiness.status};"
            f"merge_recommendation={merge_readiness.recommendation};"
            f"operator_status={operator_review.status};"
            f"operator_priority={operator_review.priority};"
            f"validation_status={validation_evidence.status};"
            f"validation_passed={str(validation_evidence.validation_passed).lower()};"
            f"continuation_stability={observation_review.continuation.continuation_stability};"
            f"risk_level={observation_review.risk_level};"
            f"readiness_score={observation_review.readiness_score};"
            f"trace={'|'.join(trace_chain)}"
        )
        bounded_history = GovernanceBoundedRetentionPrimitive().apply(
            trace_history + (history_entry,),
            retention_limit=MAX_TRACE_HISTORY_RETENTION,
        )
        return GovernanceTraceFrame(
            governance_trace_active=True,
            status=trace_status,
            root_cause=root_cause,
            trace_chain=trace_chain,
            retained_trace_history=bounded_history.retained_items,
            evicted_trace_history=bounded_history.evicted_items,
            retention_limit=MAX_TRACE_HISTORY_RETENTION,
            repository_status=repository_readiness.status,
            repository_recommendation=repository_readiness.recommendation,
            merge_status=merge_readiness.status,
            merge_recommendation=merge_readiness.recommendation,
            operator_status=operator_review.status,
            operator_priority=operator_review.priority,
            validation_status=validation_evidence.status,
            validation_passed=validation_evidence.validation_passed,
            risk_level=observation_review.risk_level,
            readiness_score=observation_review.readiness_score,
            continuation_stability=observation_review.continuation.continuation_stability,
            deterministic=True,
            bounded=bounded_history.bounded_growth_maintained
            and len(trace_chain) <= MAX_TRACE_CHAIN_LENGTH,
            read_only=True,
            local_only=True,
            no_provider_calls=True,
            no_filesystem_access=True,
            no_process_execution=True,
            no_git_operations=True,
            no_autonomous_execution=True,
        )

    def _trace_status(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
        repository_readiness: RepositoryReadinessFrame,
        trace_chain: tuple[str, ...],
    ) -> str:
        if (
            repository_readiness.status in SUPPORTED_REPOSITORY_READINESS_STATUSES
            and merge_readiness.status in SUPPORTED_MERGE_READINESS_STATUSES
            and operator_review.status in SUPPORTED_OPERATOR_REVIEW_STATUSES
            and validation_evidence.status in SUPPORTED_VALIDATION_EVIDENCE_STATUSES
            and observation_review.risk_level in SUPPORTED_OBSERVATION_RISK_LEVELS
            and observation_review.continuation.continuation_stability
            in SUPPORTED_CONTINUATION_STABILITY
            and 0 <= observation_review.readiness_score <= 100
            and len(trace_chain) == MAX_TRACE_CHAIN_LENGTH
        ):
            return "TRACE_AVAILABLE"
        return "TRACE_INCOMPLETE"

    def _root_cause(
        self,
        *,
        trace_status: str,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
        repository_readiness: RepositoryReadinessFrame,
    ) -> str:
        if trace_status == "TRACE_INCOMPLETE":
            return self._incomplete_root_cause(
                observation_review=observation_review,
                operator_review=operator_review,
                merge_readiness=merge_readiness,
                validation_evidence=validation_evidence,
                repository_readiness=repository_readiness,
            )
        if repository_readiness.status == "READY":
            return "GOVERNANCE_HEALTHY"
        if repository_readiness.status == "READY_WITH_WARNINGS":
            return self._warning_root_cause(
                observation_review=observation_review,
                operator_review=operator_review,
                merge_readiness=merge_readiness,
                validation_evidence=validation_evidence,
            )
        return self._not_ready_root_cause(
            observation_review=observation_review,
            operator_review=operator_review,
            merge_readiness=merge_readiness,
            validation_evidence=validation_evidence,
        )

    def _incomplete_root_cause(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
        repository_readiness: RepositoryReadinessFrame,
    ) -> str:
        checks = (
            (
                "REPOSITORY_TRACE_INCOMPLETE",
                repository_readiness.status not in SUPPORTED_REPOSITORY_READINESS_STATUSES,
            ),
            (
                "MERGE_TRACE_INCOMPLETE",
                merge_readiness.status not in SUPPORTED_MERGE_READINESS_STATUSES,
            ),
            (
                "OPERATOR_TRACE_INCOMPLETE",
                operator_review.status not in SUPPORTED_OPERATOR_REVIEW_STATUSES,
            ),
            (
                "VALIDATION_TRACE_INCOMPLETE",
                validation_evidence.status not in SUPPORTED_VALIDATION_EVIDENCE_STATUSES,
            ),
            (
                "RISK_TRACE_INCOMPLETE",
                observation_review.risk_level not in SUPPORTED_OBSERVATION_RISK_LEVELS,
            ),
            (
                "CONTINUATION_TRACE_INCOMPLETE",
                observation_review.continuation.continuation_stability
                not in SUPPORTED_CONTINUATION_STABILITY,
            ),
            (
                "READINESS_TRACE_INCOMPLETE",
                not 0 <= observation_review.readiness_score <= 100,
            ),
        )
        for reason, active in checks:
            if active:
                return reason
        return "TRACE_CHAIN_INCOMPLETE"

    def _warning_root_cause(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
    ) -> str:
        ordered_reasons = (
            (
                "VALIDATION_STATUS_PASSED_WITH_WARNINGS",
                validation_evidence.status == "PASSED_WITH_WARNINGS",
            ),
            ("MERGE_READY_WITH_WARNINGS", merge_readiness.status == "READY_WITH_WARNINGS"),
            ("OPERATOR_STATUS_ATTENTION", operator_review.status == "ATTENTION"),
            (
                "CONTINUATION_STABILITY_GUARDED",
                observation_review.continuation.continuation_stability == "GUARDED",
            ),
            ("RISK_LEVEL_MODERATE", observation_review.risk_level == "MODERATE"),
            ("READINESS_BELOW_READY_THRESHOLD", observation_review.readiness_score < 80),
        )
        for reason, active in ordered_reasons:
            if active:
                return reason
        return "TRACE_WARNING_UNSPECIFIED"

    def _not_ready_root_cause(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
    ) -> str:
        ordered_reasons = (
            ("VALIDATION_STATUS_FAILED", validation_evidence.status == "FAILED"),
            ("OPERATOR_STATUS_CRITICAL", operator_review.status == "CRITICAL"),
            ("RISK_LEVEL_CRITICAL", observation_review.risk_level == "CRITICAL"),
            ("OPERATOR_STATUS_REVIEW_REQUIRED", operator_review.status == "REVIEW_REQUIRED"),
            (
                "CONTINUATION_UNSTABLE",
                observation_review.continuation.continuation_stability == "UNSTABLE",
            ),
            ("RISK_LEVEL_HIGH", observation_review.risk_level == "HIGH"),
            ("MERGE_NOT_READY", merge_readiness.status == "NOT_READY"),
            ("READINESS_BELOW_READY_THRESHOLD", observation_review.readiness_score < 70),
        )
        for reason, active in ordered_reasons:
            if active:
                return reason
        return "TRACE_BLOCKER_UNSPECIFIED"

    def _trace_chain(
        self,
        *,
        observation_review: RuntimeReadinessFrame,
        operator_review: OperatorReviewFrame,
        merge_readiness: MergeReadinessFrame,
        repository_readiness: RepositoryReadinessFrame,
    ) -> tuple[str, ...]:
        tokens = (
            self._status_token("REPOSITORY", repository_readiness.status),
            self._status_token("MERGE", merge_readiness.status),
            self._status_token("OPERATOR_STATUS", operator_review.status),
            self._status_token("RISK_LEVEL", observation_review.risk_level),
            f"READINESS_SCORE_{observation_review.readiness_score}",
        )
        return tuple(tokens[:MAX_TRACE_CHAIN_LENGTH])

    def _status_token(self, prefix: str, value: str) -> str:
        return f"{prefix}_{value}"


__all__ = [
    "GovernanceTraceFrame",
    "GovernanceTraceRuntime",
    "MAX_TRACE_CHAIN_LENGTH",
    "MAX_TRACE_HISTORY_RETENTION",
    "SUPPORTED_CONTINUATION_STABILITY",
    "SUPPORTED_GOVERNANCE_TRACE_STATUSES",
]
