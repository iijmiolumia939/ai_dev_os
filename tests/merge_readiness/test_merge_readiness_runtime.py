from __future__ import annotations

from ai_dev_os.merge_readiness import (
    MAX_MERGE_HISTORY_RETENTION,
    SUPPORTED_MERGE_READINESS_STATUSES,
    SUPPORTED_MERGE_RECOMMENDATIONS,
    MergeReadinessRuntime,
)
from ai_dev_os.observation_review import (
    ContinuationObservationFrame,
    PressureAggregationFrame,
    RuntimeReadinessFrame,
    SaturationAggregationFrame,
)
from ai_dev_os.operator_review import OperatorReviewFrame
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def _observation_review_frame(
    *,
    readiness_score: int = 90,
    risk_level: str = "LOW",
    action: str = "NONE",
    blocker_count: int = 0,
    warning_count: int = 0,
    continuation_stability: str = "STABLE",
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
            pressure_summary=(
                "provider=10;continuation=10;context=10;"
                "topic=10;session=10;aggregate=10;level=LOW"
            ),
        ),
        saturation=SaturationAggregationFrame(
            saturation_aggregation_active=True,
            queue_saturation=10,
            retention_saturation=10,
            replay_saturation=10,
            lifecycle_saturation=10,
            aggregate_saturation=10,
            saturation_level="LOW",
            saturation_summary=(
                "queue=10;retention=10;replay=10;lifecycle=10;aggregate=10;level=LOW"
            ),
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
                f"continuation=10;transition=10;lifecycle=10;replay=10;score=90;stability={continuation_stability}"
            ),
        ),
        readiness_score=readiness_score,
        risk_level=risk_level,
        action=action,
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
        retained_action_history=(action,),
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
    source_frame = observation_review or _observation_review_frame()
    return OperatorReviewFrame(
        operator_review_active=True,
        status=status,
        priority=priority,
        requires_attention=requires_attention,
        reasons=("reason",),
        retained_review_history=(f"status={status}",),
        evicted_review_history=(),
        retention_limit=4,
        readiness_score=source_frame.readiness_score,
        risk_level=source_frame.risk_level,
        escalation_action=source_frame.action,
        blocker_count=source_frame.blocker_count,
        warning_count=len(source_frame.operational_warnings),
        continuation_stability=source_frame.continuation.continuation_stability,
        deterministic=True,
        bounded=True,
        local_only=True,
        no_provider_calls=True,
        no_autonomous_execution=True,
    )


def test_ready_mapping() -> None:
    observation_review = _observation_review_frame()
    operator_review = _operator_review_frame(observation_review=observation_review)

    frame = MergeReadinessRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
    )

    assert frame.status == "READY"
    assert frame.recommendation == "MERGE_CANDIDATE"
    assert frame.reasons == (
        "LOW_RISK_CONFIRMED",
        "NO_BLOCKERS_PRESENT",
        "OPERATOR_REVIEW_NORMAL",
        "READINESS_SCORE_READY",
        "CONTINUATION_STABLE",
    )


def test_ready_with_warnings_mapping() -> None:
    observation_review = _observation_review_frame(
        readiness_score=79,
        risk_level="MODERATE",
        action="MONITOR",
        warning_count=1,
    )
    operator_review = _operator_review_frame(
        status="ATTENTION",
        priority="MEDIUM",
        requires_attention=True,
        observation_review=observation_review,
    )

    frame = MergeReadinessRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
    )

    assert frame.status == "READY_WITH_WARNINGS"
    assert frame.recommendation == "REVIEW_BEFORE_MERGE"
    assert frame.reasons == (
        "RISK_LEVEL_MODERATE",
        "READINESS_BELOW_READY_THRESHOLD",
        "OPERATOR_STATUS_ATTENTION",
        "WARNINGS_PRESENT",
    )


def test_not_ready_mapping() -> None:
    observation_review = _observation_review_frame(
        readiness_score=45,
        risk_level="CRITICAL",
        action="OPERATOR_ATTENTION",
        blocker_count=2,
        warning_count=2,
        continuation_stability="UNSTABLE",
    )
    operator_review = _operator_review_frame(
        status="CRITICAL",
        priority="URGENT",
        requires_attention=True,
        observation_review=observation_review,
    )

    frame = MergeReadinessRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
    )

    assert frame.status == "NOT_READY"
    assert frame.recommendation == "DO_NOT_MERGE"
    assert frame.reasons == (
        "BLOCKERS_PRESENT",
        "ESCALATION_ACTION_OPERATOR_ATTENTION",
        "OPERATOR_STATUS_CRITICAL",
        "RISK_LEVEL_CRITICAL",
        "CONTINUATION_UNSTABLE",
    )


def test_recommendation_mapping_is_deterministic() -> None:
    ready = MergeReadinessRuntime().evaluate(
        observation_review=_observation_review_frame(),
        operator_review=_operator_review_frame(),
    )
    guarded_observation = _observation_review_frame(
        readiness_score=79,
        risk_level="MODERATE",
        warning_count=1,
    )
    guarded = MergeReadinessRuntime().evaluate(
        observation_review=guarded_observation,
        operator_review=_operator_review_frame(
            status="ATTENTION",
            priority="MEDIUM",
            requires_attention=True,
            observation_review=guarded_observation,
        ),
    )
    blocked_observation = _observation_review_frame(
        readiness_score=60,
        risk_level="HIGH",
        action="THROTTLE",
        blocker_count=1,
        continuation_stability="UNSTABLE",
    )
    blocked = MergeReadinessRuntime().evaluate(
        observation_review=blocked_observation,
        operator_review=_operator_review_frame(
            status="REVIEW_REQUIRED",
            priority="HIGH",
            requires_attention=True,
            observation_review=blocked_observation,
        ),
    )

    assert ready.status in SUPPORTED_MERGE_READINESS_STATUSES
    assert guarded.status in SUPPORTED_MERGE_READINESS_STATUSES
    assert blocked.status in SUPPORTED_MERGE_READINESS_STATUSES
    assert tuple(frame.recommendation for frame in (blocked, guarded, ready)) == (
        "DO_NOT_MERGE",
        "REVIEW_BEFORE_MERGE",
        "MERGE_CANDIDATE",
    )
    assert set(SUPPORTED_MERGE_RECOMMENDATIONS) == {
        "DO_NOT_MERGE",
        "REVIEW_BEFORE_MERGE",
        "MERGE_CANDIDATE",
    }
    assert ready == MergeReadinessRuntime().evaluate(
        observation_review=_observation_review_frame(),
        operator_review=_operator_review_frame(),
    )


def test_bounded_history_retention_and_deterministic_eviction() -> None:
    history = tuple(f"merge-{index}" for index in range(6))
    frame = MergeReadinessRuntime().evaluate(
        observation_review=_observation_review_frame(),
        operator_review=_operator_review_frame(),
        merge_history=history,
    )

    combined = history + (
        "status=READY;recommendation=MERGE_CANDIDATE;operator_status=NORMAL",
    )
    assert frame.retention_limit == MAX_MERGE_HISTORY_RETENTION
    assert frame.retained_merge_history == combined[-MAX_MERGE_HISTORY_RETENTION:]
    assert frame.evicted_merge_history == combined[:-MAX_MERGE_HISTORY_RETENTION]
    assert frame.evicted_merge_history == ("merge-0", "merge-1", "merge-2")
    assert frame.bounded is True
    assert frame.no_provider_calls is True
    assert frame.no_autonomous_execution is True


def test_runtime_audit_projection_exposes_merge_readiness() -> None:
    report = run_runtime_enforcement_audit()
    merge_readiness = report.merge_readiness
    observation_review = report.observation_review
    operator_review = report.operator_review

    assert merge_readiness.merge_readiness_active is True
    assert merge_readiness.status in SUPPORTED_MERGE_READINESS_STATUSES
    assert merge_readiness.recommendation in SUPPORTED_MERGE_RECOMMENDATIONS
    assert merge_readiness.readiness_score == observation_review.readiness_score
    assert merge_readiness.risk_level == observation_review.risk_level
    assert merge_readiness.action == observation_review.action
    assert merge_readiness.blocker_count == observation_review.blocker_count
    assert merge_readiness.warning_count == len(observation_review.operational_warnings)
    assert merge_readiness.continuation_stability == (
        observation_review.continuation.continuation_stability
    )
    assert merge_readiness.operator_status == operator_review.status
    assert merge_readiness.operator_priority == operator_review.priority
    assert merge_readiness.requires_attention == operator_review.requires_attention
    assert len(merge_readiness.retained_merge_history) <= MAX_MERGE_HISTORY_RETENTION
