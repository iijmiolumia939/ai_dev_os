from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_health import GovernanceHealthRuntime
from ai_dev_os.governance_trace import GovernanceTraceRuntime
from ai_dev_os.merge_readiness import MergeReadinessRuntime
from ai_dev_os.observation_review import ObservationReviewRuntime
from ai_dev_os.operator_review import OperatorReviewRuntime
from ai_dev_os.repository_readiness import RepositoryReadinessRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.validation_evidence import ValidationEvidenceRuntime

HEALTHY_OBSERVATION_INPUTS = {
    "provider_pressure": 0,
    "social_interaction_pressure": 0,
    "continuation_pressure": 30,
    "context_pressure": 65,
    "topic_pressure": 75,
    "session_pressure": 0,
    "viewer_event_saturation": 0,
    "retention_saturation": 0,
    "replay_suppression_activity": 0,
    "lifecycle_transition_pressure": 0,
    "transition_pressure": 0,
}

MODERATE_OBSERVATION_INPUTS = {
    "provider_pressure": 0,
    "social_interaction_pressure": 0,
    "continuation_pressure": 60,
    "context_pressure": 70,
    "topic_pressure": 75,
    "session_pressure": 0,
    "viewer_event_saturation": 0,
    "retention_saturation": 0,
    "replay_suppression_activity": 0,
    "lifecycle_transition_pressure": 0,
    "transition_pressure": 0,
}

CRITICAL_OBSERVATION_INPUTS = {
    "provider_pressure": 90,
    "social_interaction_pressure": 90,
    "continuation_pressure": 88,
    "context_pressure": 82,
    "topic_pressure": 81,
    "session_pressure": 84,
    "viewer_event_saturation": 85,
    "retention_saturation": 87,
    "replay_suppression_activity": 86,
    "lifecycle_transition_pressure": 83,
    "transition_pressure": 89,
}

PASSED_VALIDATION_INPUTS = {
    "pytest_passed": True,
    "ruff_passed": True,
    "audit_passed": True,
    "diff_check_passed": True,
    "unresolved_validation_issues": 0,
    "unresolved_audit_issues": 0,
}

FAILED_VALIDATION_INPUTS = {
    "pytest_passed": False,
    "ruff_passed": True,
    "audit_passed": True,
    "diff_check_passed": True,
    "unresolved_validation_issues": 1,
    "unresolved_audit_issues": 0,
}


@dataclass(frozen=True)
class GovernanceStackFrames:
    observation_review: object
    operator_review: object
    merge_readiness: object
    validation_evidence: object
    repository_readiness: object
    governance_trace: object
    governance_health: object


def _evaluate_governance_stack(
    *,
    observation_inputs: dict[str, int],
    validation_inputs: dict[str, int | bool],
) -> GovernanceStackFrames:
    observation_review = ObservationReviewRuntime().evaluate(**observation_inputs)
    operator_review = OperatorReviewRuntime().evaluate(observation_review=observation_review)
    merge_readiness = MergeReadinessRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
    )
    validation_evidence = ValidationEvidenceRuntime().evaluate(**validation_inputs)
    repository_readiness = RepositoryReadinessRuntime().evaluate(
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
    )
    governance_trace = GovernanceTraceRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
    )
    governance_health = GovernanceHealthRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
        governance_trace=governance_trace,
    )
    return GovernanceStackFrames(
        observation_review=observation_review,
        operator_review=operator_review,
        merge_readiness=merge_readiness,
        validation_evidence=validation_evidence,
        repository_readiness=repository_readiness,
        governance_trace=governance_trace,
        governance_health=governance_health,
    )


def _assert_causal_consistency(frames: GovernanceStackFrames) -> None:
    assert not (
        frames.repository_readiness.status == "READY"
        and frames.governance_health.status == "UNHEALTHY"
    )
    assert not (
        frames.merge_readiness.status == "READY"
        and frames.operator_review.status == "CRITICAL"
    )

    root_cause = frames.governance_trace.root_cause
    if root_cause == "GOVERNANCE_HEALTHY":
        assert frames.repository_readiness.status == "READY"
        assert frames.merge_readiness.status == "READY"
        assert frames.operator_review.status == "NORMAL"
        assert frames.observation_review.risk_level == "LOW"
    elif root_cause == "MERGE_READY_WITH_WARNINGS":
        assert frames.merge_readiness.status == "READY_WITH_WARNINGS"
        assert frames.repository_readiness.status == "READY_WITH_WARNINGS"
    elif root_cause == "VALIDATION_STATUS_FAILED":
        assert frames.validation_evidence.status == "FAILED"
        assert frames.repository_readiness.status == "NOT_READY"
    elif root_cause == "OPERATOR_STATUS_CRITICAL":
        assert frames.operator_review.status == "CRITICAL"
        assert frames.merge_readiness.status == "NOT_READY"


def test_scenario_a_healthy_governance() -> None:
    frames = _evaluate_governance_stack(
        observation_inputs=HEALTHY_OBSERVATION_INPUTS,
        validation_inputs=PASSED_VALIDATION_INPUTS,
    )

    assert frames.observation_review.readiness_score == 85
    assert frames.observation_review.risk_level == "LOW"
    assert frames.validation_evidence.status == "PASSED"
    assert frames.observation_review.continuation.continuation_stability == "STABLE"
    assert frames.operator_review.status == "NORMAL"
    assert frames.merge_readiness.status == "READY"
    assert frames.repository_readiness.status == "READY"
    assert frames.governance_health.status == "HEALTHY"
    assert frames.governance_trace.status == "TRACE_AVAILABLE"
    assert frames.governance_trace.trace_chain == (
        "REPOSITORY_READY",
        "MERGE_READY",
        "OPERATOR_STATUS_NORMAL",
        "RISK_LEVEL_LOW",
        "READINESS_SCORE_85",
    )
    _assert_causal_consistency(frames)


def test_scenario_b_moderate_risk() -> None:
    frames = _evaluate_governance_stack(
        observation_inputs=MODERATE_OBSERVATION_INPUTS,
        validation_inputs=PASSED_VALIDATION_INPUTS,
    )

    assert frames.observation_review.readiness_score == 79
    assert frames.observation_review.risk_level == "MODERATE"
    assert frames.validation_evidence.status == "PASSED"
    assert frames.operator_review.status == "ATTENTION"
    assert frames.merge_readiness.status == "READY_WITH_WARNINGS"
    assert frames.repository_readiness.status == "READY_WITH_WARNINGS"
    assert frames.governance_health.status == "DEGRADED"
    assert frames.governance_trace.status == "TRACE_AVAILABLE"
    assert frames.governance_trace.trace_chain == (
        "REPOSITORY_READY_WITH_WARNINGS",
        "MERGE_READY_WITH_WARNINGS",
        "OPERATOR_STATUS_ATTENTION",
        "RISK_LEVEL_MODERATE",
        "READINESS_SCORE_79",
    )
    _assert_causal_consistency(frames)


def test_scenario_c_validation_failure() -> None:
    frames = _evaluate_governance_stack(
        observation_inputs=HEALTHY_OBSERVATION_INPUTS,
        validation_inputs=FAILED_VALIDATION_INPUTS,
    )

    assert frames.validation_evidence.status == "FAILED"
    assert frames.repository_readiness.status == "NOT_READY"
    assert frames.governance_health.status == "UNHEALTHY"
    assert frames.governance_trace.status == "TRACE_AVAILABLE"
    assert frames.governance_trace.root_cause == "VALIDATION_STATUS_FAILED"
    _assert_causal_consistency(frames)


def test_scenario_d_critical_escalation() -> None:
    frames = _evaluate_governance_stack(
        observation_inputs=CRITICAL_OBSERVATION_INPUTS,
        validation_inputs=PASSED_VALIDATION_INPUTS,
    )

    assert frames.observation_review.action == "OPERATOR_ATTENTION"
    assert frames.operator_review.status == "CRITICAL"
    assert frames.merge_readiness.status == "NOT_READY"
    assert frames.repository_readiness.status == "NOT_READY"
    assert frames.governance_health.status == "UNHEALTHY"
    assert frames.governance_trace.status == "TRACE_AVAILABLE"
    assert frames.governance_trace.root_cause == "OPERATOR_STATUS_CRITICAL"
    _assert_causal_consistency(frames)


def test_scenario_e_traceability_review_is_deterministic() -> None:
    first = _evaluate_governance_stack(
        observation_inputs=MODERATE_OBSERVATION_INPUTS,
        validation_inputs=PASSED_VALIDATION_INPUTS,
    )
    second = _evaluate_governance_stack(
        observation_inputs=MODERATE_OBSERVATION_INPUTS,
        validation_inputs=PASSED_VALIDATION_INPUTS,
    )

    assert first == second
    assert first.governance_trace.trace_chain == (
        "REPOSITORY_READY_WITH_WARNINGS",
        "MERGE_READY_WITH_WARNINGS",
        "OPERATOR_STATUS_ATTENTION",
        "RISK_LEVEL_MODERATE",
        "READINESS_SCORE_79",
    )
    assert first.governance_trace.deterministic is True
    _assert_causal_consistency(first)


def test_runtime_audit_contains_required_governance_sections() -> None:
    report = run_runtime_enforcement_audit()

    assert report.observation_review.observation_review_active is True
    assert report.operator_review.operator_review_active is True
    assert report.merge_readiness.merge_readiness_active is True
    assert report.validation_evidence.validation_evidence_active is True
    assert report.repository_readiness.repository_readiness_active is True
    assert report.governance_trace.governance_trace_active is True
    assert report.governance_health.governance_health_active is True
    assert report.governance_health.governance_health.repository_status == (
        report.repository_readiness.status
    )
    assert report.governance_health.governance_health.merge_status == report.merge_readiness.status
    assert report.governance_health.governance_health.operator_status == (
        report.operator_review.status
    )
    assert report.governance_health.governance_health.validation_status == (
        report.validation_evidence.status
    )
    assert report.governance_health.governance_health.governance_trace_status == (
        report.governance_trace.status
    )


def test_governance_stack_causal_consistency_holds_across_supported_states() -> None:
    scenarios = (
        _evaluate_governance_stack(
            observation_inputs=HEALTHY_OBSERVATION_INPUTS,
            validation_inputs=PASSED_VALIDATION_INPUTS,
        ),
        _evaluate_governance_stack(
            observation_inputs=MODERATE_OBSERVATION_INPUTS,
            validation_inputs=PASSED_VALIDATION_INPUTS,
        ),
        _evaluate_governance_stack(
            observation_inputs=HEALTHY_OBSERVATION_INPUTS,
            validation_inputs=FAILED_VALIDATION_INPUTS,
        ),
        _evaluate_governance_stack(
            observation_inputs=CRITICAL_OBSERVATION_INPUTS,
            validation_inputs=PASSED_VALIDATION_INPUTS,
        ),
    )

    for frames in scenarios:
        _assert_causal_consistency(frames)
