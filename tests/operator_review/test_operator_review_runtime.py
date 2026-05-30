from __future__ import annotations

from ai_dev_os.observation_review import (
    ContinuationObservationFrame,
    PressureAggregationFrame,
    RuntimeReadinessFrame,
    SaturationAggregationFrame,
)
from ai_dev_os.operator_review import (
    MAX_REVIEW_HISTORY_RETENTION,
    SUPPORTED_OPERATOR_REVIEW_PRIORITIES,
    OperatorReviewRuntime,
)
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


def test_normal_mapping() -> None:
    frame = OperatorReviewRuntime().evaluate(
        observation_review=_observation_review_frame(),
    )

    assert frame.status == "NORMAL"
    assert frame.priority == "LOW"
    assert frame.requires_attention is False
    assert frame.reasons == ("NORMAL_OPERATIONAL_WINDOW",)


def test_attention_mapping() -> None:
    frame = OperatorReviewRuntime().evaluate(
        observation_review=_observation_review_frame(
            readiness_score=79,
            risk_level="MODERATE",
            action="MONITOR",
            warning_count=1,
            continuation_stability="GUARDED",
        ),
    )

    assert frame.status == "ATTENTION"
    assert frame.priority == "MEDIUM"
    assert frame.requires_attention is True
    assert frame.reasons == (
        "ESCALATION_ACTION_MONITOR",
        "RISK_LEVEL_MODERATE",
        "READINESS_BELOW_ATTENTION_THRESHOLD",
        "WARNINGS_PRESENT",
        "CONTINUATION_GUARDED",
    )


def test_review_required_mapping() -> None:
    frame = OperatorReviewRuntime().evaluate(
        observation_review=_observation_review_frame(
            readiness_score=72,
            risk_level="HIGH",
            action="THROTTLE",
            blocker_count=2,
            continuation_stability="UNSTABLE",
        ),
    )

    assert frame.status == "REVIEW_REQUIRED"
    assert frame.priority == "HIGH"
    assert frame.requires_attention is True
    assert frame.reasons == (
        "ESCALATION_ACTION_THROTTLE",
        "RISK_LEVEL_HIGH",
        "BLOCKERS_PRESENT",
        "CONTINUATION_UNSTABLE",
        "READINESS_BELOW_ATTENTION_THRESHOLD",
    )


def test_critical_mapping() -> None:
    frame = OperatorReviewRuntime().evaluate(
        observation_review=_observation_review_frame(
            readiness_score=40,
            risk_level="CRITICAL",
            action="OPERATOR_ATTENTION",
            blocker_count=3,
            warning_count=2,
            continuation_stability="UNSTABLE",
        ),
    )

    assert frame.status == "CRITICAL"
    assert frame.priority == "URGENT"
    assert frame.requires_attention is True
    assert frame.reasons[:2] == (
        "ESCALATION_ACTION_OPERATOR_ATTENTION",
        "RISK_LEVEL_CRITICAL",
    )


def test_priority_mapping_is_deterministic() -> None:
    frames = (
        OperatorReviewRuntime().evaluate(observation_review=_observation_review_frame()),
        OperatorReviewRuntime().evaluate(
            observation_review=_observation_review_frame(
                risk_level="MODERATE",
                action="MONITOR",
                warning_count=1,
            )
        ),
        OperatorReviewRuntime().evaluate(
            observation_review=_observation_review_frame(
                risk_level="HIGH",
                action="THROTTLE",
            )
        ),
        OperatorReviewRuntime().evaluate(
            observation_review=_observation_review_frame(
                risk_level="CRITICAL",
                action="OPERATOR_ATTENTION",
            )
        ),
    )

    assert tuple(frame.priority for frame in frames) == ("LOW", "MEDIUM", "HIGH", "URGENT")
    assert set(SUPPORTED_OPERATOR_REVIEW_PRIORITIES) == {"LOW", "MEDIUM", "HIGH", "URGENT"}
    assert frames[0] == OperatorReviewRuntime().evaluate(
        observation_review=_observation_review_frame()
    )


def test_bounded_history_retention_and_deterministic_eviction() -> None:
    history = tuple(f"review-{index}" for index in range(6))
    frame = OperatorReviewRuntime().evaluate(
        observation_review=_observation_review_frame(),
        review_history=history,
    )

    combined = history + ("status=NORMAL;priority=LOW;attention=false",)
    assert frame.retention_limit == MAX_REVIEW_HISTORY_RETENTION
    assert frame.retained_review_history == combined[-MAX_REVIEW_HISTORY_RETENTION:]
    assert frame.evicted_review_history == combined[:-MAX_REVIEW_HISTORY_RETENTION]
    assert frame.evicted_review_history == ("review-0", "review-1", "review-2")
    assert frame.bounded is True


def test_runtime_audit_projection_exposes_operator_review() -> None:
    report = run_runtime_enforcement_audit()
    operator_review = report.operator_review
    observation_review = report.observation_review

    assert operator_review.operator_review_active is True
    assert operator_review.status in {
        "NORMAL",
        "ATTENTION",
        "REVIEW_REQUIRED",
        "CRITICAL",
    }
    assert operator_review.priority in SUPPORTED_OPERATOR_REVIEW_PRIORITIES
    assert operator_review.requires_attention is (operator_review.status != "NORMAL")
    assert operator_review.readiness_score == observation_review.readiness_score
    assert operator_review.risk_level == observation_review.risk_level
    assert operator_review.escalation_action == observation_review.action
    assert operator_review.blocker_count == observation_review.blocker_count
    assert operator_review.warning_count == len(observation_review.operational_warnings)
    assert operator_review.continuation_stability == (
        observation_review.continuation.continuation_stability
    )
    assert len(operator_review.retained_review_history) <= MAX_REVIEW_HISTORY_RETENTION
    assert operator_review.no_provider_calls is True
    assert operator_review.no_autonomous_execution is True
