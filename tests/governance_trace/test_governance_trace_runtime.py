from __future__ import annotations

from ai_dev_os.governance_trace import (
    MAX_TRACE_HISTORY_RETENTION,
    SUPPORTED_GOVERNANCE_TRACE_STATUSES,
    GovernanceTraceRuntime,
)
from ai_dev_os.merge_readiness import MergeReadinessFrame
from ai_dev_os.observation_review import (
    ContinuationObservationFrame,
    PressureAggregationFrame,
    RuntimeReadinessFrame,
    SaturationAggregationFrame,
)
from ai_dev_os.operator_review import OperatorReviewFrame
from ai_dev_os.repository_readiness import RepositoryReadinessFrame
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.validation_evidence import ValidationEvidenceFrame


def _observation_review_frame(
    *,
    readiness_score: int = 90,
    risk_level: str = "LOW",
    continuation_stability: str = "STABLE",
    blocker_count: int = 0,
    warning_count: int = 0,
) -> RuntimeReadinessFrame:
    warnings = tuple(f"warning-{index}" for index in range(warning_count))
    return RuntimeReadinessFrame(
        observation_review_active=True,
        pressure=PressureAggregationFrame(
            pressure_aggregation_active=True,
            provider_pressure=10,
            continuation_pressure=10,
            context_pressure=10,
            topic_pressure=10,
            session_pressure=10,
            aggregate_pressure=10,
            pressure_level="LOW",
            pressure_summary="provider=10;continuation=10;context=10;topic=10;session=10",
        ),
        saturation=SaturationAggregationFrame(
            saturation_aggregation_active=True,
            queue_saturation=10,
            retention_saturation=10,
            replay_saturation=10,
            lifecycle_saturation=10,
            aggregate_saturation=10,
            saturation_level="LOW",
            saturation_summary="queue=10;retention=10;replay=10;lifecycle=10",
        ),
        continuation=ContinuationObservationFrame(
            continuation_observation_active=True,
            continuation_pressure=10,
            transition_pressure=10,
            lifecycle_transition_pressure=10,
            replay_suppression_activity=10,
            continuation_score=90,
            continuation_stability=continuation_stability,
            continuation_summary=(
                "continuation=10;transition=10;lifecycle=10;replay=10;"
                f"score=90;stability={continuation_stability}"
            ),
        ),
        readiness_score=readiness_score,
        risk_level=risk_level,
        action="NONE",
        merge_readiness="READY_FOR_MAIN_MERGE",
        blocker_count=blocker_count,
        merge_blockers=tuple(f"blocker-{index}" for index in range(blocker_count)),
        operational_warnings=warnings,
        pressure_summary="pressure-summary",
        saturation_summary="saturation-summary",
        continuation_summary="continuation-summary",
        action_summary="action-summary",
        operational_risk_summary="operational-risk-summary",
        retained_observations=("provider-pressure",),
        evicted_observations=(),
        retained_action_history=("NONE",),
        evicted_action_history=(),
        retention_limit=6,
        action_retention_limit=4,
        no_autonomous_execution=True,
        deterministic=True,
        bounded=True,
    )


def _operator_review_frame(
    *,
    status: str = "NORMAL",
    priority: str = "LOW",
    requires_attention: bool = False,
    observation_review: RuntimeReadinessFrame | None = None,
) -> OperatorReviewFrame:
    source = observation_review or _observation_review_frame()
    return OperatorReviewFrame(
        operator_review_active=True,
        status=status,
        priority=priority,
        requires_attention=requires_attention,
        reasons=("reason",),
        retained_review_history=(f"status={status}",),
        evicted_review_history=(),
        retention_limit=4,
        readiness_score=source.readiness_score,
        risk_level=source.risk_level,
        escalation_action=source.action,
        blocker_count=source.blocker_count,
        warning_count=len(source.operational_warnings),
        continuation_stability=source.continuation.continuation_stability,
        deterministic=True,
        bounded=True,
        local_only=True,
        no_provider_calls=True,
        no_autonomous_execution=True,
    )


def _merge_readiness_frame(
    *,
    status: str = "READY",
    recommendation: str = "MERGE_CANDIDATE",
    observation_review: RuntimeReadinessFrame | None = None,
    operator_review: OperatorReviewFrame | None = None,
) -> MergeReadinessFrame:
    source_observation = observation_review or _observation_review_frame()
    source_operator = operator_review or _operator_review_frame(
        observation_review=source_observation
    )
    return MergeReadinessFrame(
        merge_readiness_active=True,
        status=status,
        recommendation=recommendation,
        reasons=("reason",),
        retained_merge_history=(f"status={status}",),
        evicted_merge_history=(),
        retention_limit=4,
        readiness_score=source_observation.readiness_score,
        risk_level=source_observation.risk_level,
        action=source_observation.action,
        blocker_count=source_observation.blocker_count,
        warning_count=len(source_observation.operational_warnings),
        continuation_stability=source_observation.continuation.continuation_stability,
        operator_status=source_operator.status,
        operator_priority=source_operator.priority,
        requires_attention=source_operator.requires_attention,
        deterministic=True,
        bounded=True,
        local_only=True,
        no_provider_calls=True,
        no_autonomous_execution=True,
    )


def _validation_evidence_frame(
    *,
    status: str = "PASSED",
    validation_passed: bool = True,
) -> ValidationEvidenceFrame:
    return ValidationEvidenceFrame(
        validation_evidence_active=True,
        status=status,
        validation_passed=validation_passed,
        reasons=("reason",),
        retained_evidence_history=(f"status={status}",),
        evicted_evidence_history=(),
        retention_limit=4,
        pytest_passed=status != "FAILED",
        ruff_passed=True,
        audit_passed=status != "FAILED",
        diff_check_passed=status != "FAILED",
        unresolved_validation_issues=0 if status == "PASSED" else 1,
        unresolved_audit_issues=0 if status == "PASSED" else 1,
        deterministic=True,
        bounded=True,
        local_only=True,
        no_provider_calls=True,
        no_filesystem_access=True,
        no_process_execution=True,
        no_git_operations=True,
        no_autonomous_execution=True,
    )


def _repository_readiness_frame(
    *,
    status: str = "READY",
    recommendation: str = "MERGE_CANDIDATE",
    merge_readiness: MergeReadinessFrame | None = None,
    validation_evidence: ValidationEvidenceFrame | None = None,
) -> RepositoryReadinessFrame:
    source_merge = merge_readiness or _merge_readiness_frame()
    source_validation = validation_evidence or _validation_evidence_frame()
    return RepositoryReadinessFrame(
        repository_readiness_active=True,
        status=status,
        recommendation=recommendation,
        reasons=("reason",),
        retained_repository_history=(f"status={status}",),
        evicted_repository_history=(),
        retention_limit=4,
        merge_status=source_merge.status,
        merge_recommendation=source_merge.recommendation,
        pytest_passed=source_validation.pytest_passed,
        ruff_passed=source_validation.ruff_passed,
        diff_check_passed=source_validation.diff_check_passed,
        audit_passed=source_validation.audit_passed,
        unresolved_validation_issues=source_validation.unresolved_validation_issues,
        unresolved_audit_issues=source_validation.unresolved_audit_issues,
        deterministic=True,
        bounded=True,
        local_only=True,
        no_provider_calls=True,
        no_autonomous_execution=True,
        no_git_operations=True,
        no_filesystem_mutation=True,
    )


def test_ready_trace_is_deterministic() -> None:
    observation_review = _observation_review_frame(readiness_score=90, risk_level="LOW")
    operator_review = _operator_review_frame(observation_review=observation_review)
    merge_readiness = _merge_readiness_frame(
        observation_review=observation_review,
        operator_review=operator_review,
    )
    validation_evidence = _validation_evidence_frame()
    repository_readiness = _repository_readiness_frame(
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
    )

    frame = GovernanceTraceRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
    )

    assert frame.status == "TRACE_AVAILABLE"
    assert frame.root_cause == "GOVERNANCE_HEALTHY"
    assert frame.trace_chain == (
        "REPOSITORY_READY",
        "MERGE_READY",
        "OPERATOR_STATUS_NORMAL",
        "RISK_LEVEL_LOW",
        "READINESS_SCORE_90",
    )


def test_ready_with_warnings_trace_uses_first_non_normal_upstream_reason() -> None:
    observation_review = _observation_review_frame(
        readiness_score=79,
        risk_level="MODERATE",
        continuation_stability="GUARDED",
        warning_count=1,
    )
    operator_review = _operator_review_frame(
        status="ATTENTION",
        priority="MEDIUM",
        requires_attention=True,
        observation_review=observation_review,
    )
    merge_readiness = _merge_readiness_frame(
        status="READY_WITH_WARNINGS",
        recommendation="REVIEW_BEFORE_MERGE",
        observation_review=observation_review,
        operator_review=operator_review,
    )
    validation_evidence = _validation_evidence_frame()
    repository_readiness = _repository_readiness_frame(
        status="READY_WITH_WARNINGS",
        recommendation="REVIEW_BEFORE_MERGE",
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
    )

    frame = GovernanceTraceRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
    )

    assert frame.status == "TRACE_AVAILABLE"
    assert frame.root_cause == "MERGE_READY_WITH_WARNINGS"
    assert frame.trace_chain == (
        "REPOSITORY_READY_WITH_WARNINGS",
        "MERGE_READY_WITH_WARNINGS",
        "OPERATOR_STATUS_ATTENTION",
        "RISK_LEVEL_MODERATE",
        "READINESS_SCORE_79",
    )


def test_not_ready_trace_selects_highest_severity_root_cause() -> None:
    observation_review = _observation_review_frame(
        readiness_score=45,
        risk_level="CRITICAL",
        continuation_stability="UNSTABLE",
        blocker_count=2,
        warning_count=2,
    )
    operator_review = _operator_review_frame(
        status="CRITICAL",
        priority="URGENT",
        requires_attention=True,
        observation_review=observation_review,
    )
    merge_readiness = _merge_readiness_frame(
        status="NOT_READY",
        recommendation="DO_NOT_MERGE",
        observation_review=observation_review,
        operator_review=operator_review,
    )
    validation_evidence = _validation_evidence_frame(
        status="FAILED",
        validation_passed=False,
    )
    repository_readiness = _repository_readiness_frame(
        status="NOT_READY",
        recommendation="DO_NOT_MERGE",
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
    )

    frame = GovernanceTraceRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
    )

    assert frame.status == "TRACE_AVAILABLE"
    assert frame.root_cause == "VALIDATION_STATUS_FAILED"
    assert frame.trace_chain == (
        "REPOSITORY_NOT_READY",
        "MERGE_NOT_READY",
        "OPERATOR_STATUS_CRITICAL",
        "RISK_LEVEL_CRITICAL",
        "READINESS_SCORE_45",
    )


def test_root_cause_uses_validation_warning_when_merge_surface_is_normal() -> None:
    observation_review = _observation_review_frame(readiness_score=90, risk_level="LOW")
    operator_review = _operator_review_frame(observation_review=observation_review)
    merge_readiness = _merge_readiness_frame(
        observation_review=observation_review,
        operator_review=operator_review,
    )
    validation_evidence = _validation_evidence_frame(
        status="PASSED_WITH_WARNINGS",
        validation_passed=True,
    )
    repository_readiness = _repository_readiness_frame(
        status="READY_WITH_WARNINGS",
        recommendation="REVIEW_BEFORE_MERGE",
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
    )

    frame = GovernanceTraceRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
    )

    assert frame.root_cause == "VALIDATION_STATUS_PASSED_WITH_WARNINGS"


def test_bounded_history_retention_and_deterministic_eviction() -> None:
    history = tuple(f"trace-{index}" for index in range(6))
    observation_review = _observation_review_frame()
    operator_review = _operator_review_frame(observation_review=observation_review)
    merge_readiness = _merge_readiness_frame(
        observation_review=observation_review,
        operator_review=operator_review,
    )
    validation_evidence = _validation_evidence_frame()
    repository_readiness = _repository_readiness_frame(
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
    )

    frame = GovernanceTraceRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
        trace_history=history,
    )

    assert frame.retention_limit == MAX_TRACE_HISTORY_RETENTION
    assert frame.retained_trace_history[-1].startswith("status=TRACE_AVAILABLE;")
    assert frame.retained_trace_history == (history + (frame.retained_trace_history[-1],))[
        -MAX_TRACE_HISTORY_RETENTION:
    ]
    assert frame.evicted_trace_history == ("trace-0", "trace-1", "trace-2")
    assert frame.bounded is True
    assert frame.read_only is True
    assert frame.no_provider_calls is True
    assert frame.no_filesystem_access is True
    assert frame.no_process_execution is True
    assert frame.no_git_operations is True
    assert frame.no_autonomous_execution is True


def test_runtime_audit_projection_exposes_governance_trace() -> None:
    report = run_runtime_enforcement_audit()
    governance_trace = report.governance_trace

    assert governance_trace.governance_trace_active is True
    assert governance_trace.status in SUPPORTED_GOVERNANCE_TRACE_STATUSES
    assert governance_trace.repository_status == report.repository_readiness.status
    assert governance_trace.repository_recommendation == report.repository_readiness.recommendation
    assert governance_trace.merge_status == report.merge_readiness.status
    assert governance_trace.merge_recommendation == report.merge_readiness.recommendation
    assert governance_trace.operator_status == report.operator_review.status
    assert governance_trace.operator_priority == report.operator_review.priority
    assert governance_trace.validation_status == report.validation_evidence.status
    assert governance_trace.validation_passed == report.validation_evidence.validation_passed
    assert governance_trace.risk_level == report.observation_review.risk_level
    assert governance_trace.readiness_score == report.observation_review.readiness_score
    assert governance_trace.continuation_stability == (
        report.observation_review.continuation.continuation_stability
    )
    assert governance_trace.trace_chain == (
        f"REPOSITORY_{report.repository_readiness.status}",
        f"MERGE_{report.merge_readiness.status}",
        f"OPERATOR_STATUS_{report.operator_review.status}",
        f"RISK_LEVEL_{report.observation_review.risk_level}",
        f"READINESS_SCORE_{report.observation_review.readiness_score}",
    )
    assert len(governance_trace.retained_trace_history) <= MAX_TRACE_HISTORY_RETENTION
