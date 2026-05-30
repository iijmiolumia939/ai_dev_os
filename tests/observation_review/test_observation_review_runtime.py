from __future__ import annotations

from ai_dev_os.observation_review import (
    MAX_ACTION_HISTORY_RETENTION,
    MAX_OBSERVATION_RETENTION,
    SUPPORTED_OBSERVATION_ACTIONS,
    ObservationEscalationPolicy,
    ObservationReviewRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_readiness_calculation_is_bounded_and_high_for_low_pressure_inputs() -> None:
    frame = ObservationReviewRuntime().evaluate(
        provider_pressure=0,
        social_interaction_pressure=0,
        continuation_pressure=0,
        context_pressure=0,
        topic_pressure=0,
        session_pressure=0,
        viewer_event_saturation=0,
        retention_saturation=0,
        replay_suppression_activity=0,
        lifecycle_transition_pressure=0,
        transition_pressure=0,
    )

    assert frame.readiness_score == 100
    assert frame.risk_level == "LOW"
    assert frame.action == "NONE"
    assert frame.merge_readiness == "READY_FOR_MAIN_MERGE"
    assert frame.blocker_count == 0
    assert frame.operational_risk_summary.startswith("risk=LOW;score=100")


def test_pressure_aggregation_summary_is_deterministic() -> None:
    frame = ObservationReviewRuntime().evaluate(
        provider_pressure=60,
        continuation_pressure=50,
        context_pressure=40,
        topic_pressure=30,
        session_pressure=20,
    )

    assert frame.pressure.aggregate_pressure == 42
    assert frame.pressure.pressure_level == "LOW"
    assert (
        frame.pressure_summary
        == "provider=60;continuation=50;context=40;topic=30;session=20;aggregate=42;level=LOW"
    )


def test_saturation_aggregation_summary_is_deterministic() -> None:
    frame = ObservationReviewRuntime().evaluate(
        viewer_event_saturation=80,
        retention_saturation=70,
        replay_suppression_activity=60,
        lifecycle_transition_pressure=50,
    )

    assert frame.saturation.aggregate_saturation == 67
    assert frame.saturation.saturation_level == "MEDIUM"
    assert (
        frame.saturation_summary
        == "queue=80;retention=70;replay=60;lifecycle=50;aggregate=67;level=MEDIUM"
    )


def test_runtime_output_is_deterministic() -> None:
    first = ObservationReviewRuntime().evaluate()
    second = ObservationReviewRuntime().evaluate()

    assert first == second
    assert first.deterministic is True


def test_bounded_retention_evicts_oldest_observations() -> None:
    history = tuple(f"observation-{index}" for index in range(8))
    frame = ObservationReviewRuntime().evaluate(observation_history=history)

    assert frame.retention_limit == MAX_OBSERVATION_RETENTION
    assert frame.retained_observations == history[-MAX_OBSERVATION_RETENTION:]
    assert frame.evicted_observations == history[:-MAX_OBSERVATION_RETENTION]
    assert frame.bounded is True


def test_bounded_action_history_evicts_oldest_actions() -> None:
    history = ("NONE", "MONITOR", "THROTTLE", "PAUSE_REVIEW", "MONITOR")
    frame = ObservationReviewRuntime().evaluate(action_history=history)

    combined = history + (frame.action,)
    assert frame.action_retention_limit == MAX_ACTION_HISTORY_RETENTION
    assert frame.retained_action_history == combined[-MAX_ACTION_HISTORY_RETENTION:]
    assert frame.evicted_action_history == combined[:-MAX_ACTION_HISTORY_RETENTION]
    assert frame.no_autonomous_execution is True
    assert frame.bounded is True


def test_observation_escalation_policy_maps_risk_levels_to_actions() -> None:
    policy = ObservationEscalationPolicy()

    assert policy.recommend(risk_level="LOW").action == "NONE"
    assert policy.recommend(risk_level="MODERATE").action == "MONITOR"
    assert policy.recommend(risk_level="HIGH").action == "THROTTLE"
    assert policy.recommend(risk_level="CRITICAL").action == "OPERATOR_ATTENTION"


def test_runtime_recommends_throttle_for_high_risk_inputs() -> None:
    frame = ObservationReviewRuntime().evaluate(provider_pressure=80)

    assert frame.risk_level == "HIGH"
    assert frame.action == "THROTTLE"
    assert frame.operational_risk_summary.startswith("risk=HIGH")


def test_merge_recommendation_generation_blocks_critical_risk_inputs() -> None:
    frame = ObservationReviewRuntime().evaluate(
        provider_pressure=90,
        continuation_pressure=88,
        context_pressure=82,
        topic_pressure=81,
        session_pressure=84,
        viewer_event_saturation=85,
        retention_saturation=87,
        replay_suppression_activity=86,
        lifecycle_transition_pressure=83,
        transition_pressure=89,
        social_interaction_pressure=90,
    )

    assert frame.readiness_score < 70
    assert frame.risk_level == "CRITICAL"
    assert frame.action == "OPERATOR_ATTENTION"
    assert frame.merge_readiness == "BLOCKED_FOR_MAIN_MERGE"
    assert frame.blocker_count >= 5
    assert "PROVIDER_PRESSURE_BLOCKER" in frame.merge_blockers
    assert "QUEUE_SATURATION_BLOCKER" in frame.merge_blockers
    assert frame.operational_risk_summary.startswith("risk=CRITICAL")


def test_runtime_audit_exposes_observation_review_output() -> None:
    report = run_runtime_enforcement_audit().observation_review

    assert 0 <= report.readiness_score <= 100
    assert report.merge_readiness in {
        "BLOCKED_FOR_MAIN_MERGE",
        "READY_FOR_MAIN_MERGE",
        "READY_WITH_WARNINGS",
        "CONTINUE_OBSERVATION_BEFORE_MAIN_MERGE",
    }
    assert report.blocker_count == len(report.merge_blockers)
    assert report.action in SUPPORTED_OBSERVATION_ACTIONS
    assert report.retained_action_history
    assert isinstance(report.pressure_summary, str) and report.pressure_summary
    assert isinstance(report.saturation_summary, str) and report.saturation_summary
    assert isinstance(report.continuation_summary, str) and report.continuation_summary
    assert isinstance(report.action_summary, str) and report.action_summary
    assert isinstance(report.operational_risk_summary, str) and report.operational_risk_summary
