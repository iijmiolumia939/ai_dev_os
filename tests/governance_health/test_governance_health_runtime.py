from __future__ import annotations

import inspect

import pytest

from ai_dev_os.governance_health import (
    MAX_HEALTH_HISTORY_RETENTION,
    GovernanceHealthRuntime,
)
from ai_dev_os.governance_health.health_score import GovernanceHealthPolicy
from ai_dev_os.governance_health.pressure_aggregation import GovernancePressurePolicy
from ai_dev_os.governance_health.risk_aggregation import GovernanceRiskPolicy
from ai_dev_os.governance_health.stability_assessment import GovernanceStabilityPolicy
from ai_dev_os.governance_trace import GovernanceTraceRuntime
from ai_dev_os.merge_readiness import MergeReadinessRuntime
from ai_dev_os.observation_review import ObservationReviewRuntime
from ai_dev_os.operator_review import OperatorReviewRuntime
from ai_dev_os.repository_readiness import RepositoryReadinessRuntime
from ai_dev_os.runtime_audit import ReleaseCheckInputs, run_runtime_enforcement_audit
from ai_dev_os.validation_evidence import ValidationEvidenceRuntime


def _evaluate_governance_health(
    *,
    pytest_passed: bool = True,
    ruff_passed: bool = True,
    audit_passed: bool = True,
    diff_check_passed: bool = True,
    unresolved_validation_issues: int = 0,
    unresolved_audit_issues: int = 0,
    health_history: tuple[str, ...] = (),
):
    observation_review = ObservationReviewRuntime().evaluate(
        provider_pressure=10,
        social_interaction_pressure=10,
        continuation_pressure=10,
        context_pressure=10,
        topic_pressure=10,
        session_pressure=10,
        viewer_event_saturation=10,
        retention_saturation=10,
        replay_suppression_activity=10,
        lifecycle_transition_pressure=10,
        transition_pressure=10,
    )
    operator_review = OperatorReviewRuntime().evaluate(observation_review=observation_review)
    merge_readiness = MergeReadinessRuntime().evaluate(
        observation_review=observation_review,
        operator_review=operator_review,
    )
    validation_evidence = ValidationEvidenceRuntime().evaluate(
        pytest_passed=pytest_passed,
        ruff_passed=ruff_passed,
        audit_passed=audit_passed,
        diff_check_passed=diff_check_passed,
        unresolved_validation_issues=unresolved_validation_issues,
        unresolved_audit_issues=unresolved_audit_issues,
    )
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
        health_history=health_history,
    )
    return governance_health, governance_trace


def test_governance_score_validation() -> None:
    frame = GovernanceHealthPolicy().score(
        session_lifecycle="low",
        stale_context_pressure="medium",
        persistence_pressure="medium",
        retrieval_scaling_pressure="low",
        provider_simulation_pressure="low",
        architecture_isolation_pressure="low",
        schema_migration_pressure="medium",
        checkpoint_rotation_pressure="low",
        workspace_contamination_risk=False,
    )

    assert 0 <= frame.governance_health_score <= 100
    assert frame.governance_health_state in {
        "HEALTHY",
        "STABLE_WARNING",
        "HIGH_PRESSURE",
        "CRITICAL_GOVERNANCE",
    }
    assert frame.governance_attention_required is (frame.governance_health_state != "HEALTHY")


def test_pressure_aggregation_validation() -> None:
    frame = GovernancePressurePolicy().aggregate(
        retrieval_pressure="medium",
        persistence_pressure="high",
        session_pressure="medium",
        architecture_pressure="low",
        provider_pressure="low",
        continuity_pressure="high",
        checkpoint_pressure="high",
        stale_context_pressure="medium",
        previous_pressure="low",
    )

    assert frame.aggregate_pressure in {"medium", "high"}
    assert frame.dominant_pressure in {
        "persistence",
        "continuity",
        "checkpoint",
    }
    assert frame.pressure_direction == "rising"
    assert frame.pressure_trend


def test_risk_aggregation_validation() -> None:
    frame = GovernanceRiskPolicy().aggregate(
        stale_continuity_risk=True,
        hidden_context_drift=True,
        architecture_contamination=True,
        retrieval_explosion=False,
        persistence_explosion=True,
        checkpoint_explosion=True,
        provider_lock_in_risk=False,
        governance_runtime_drift=True,
        prompt_mode_drift=True,
    )

    assert frame.aggregate_risk in {"high", "critical"}
    assert frame.highest_risk == "architecture_contamination"
    assert frame.isolation_recommended is True
    assert frame.compact_recommended is True
    assert frame.rollover_recommended is True


def test_stability_assessment_validation() -> None:
    frame = GovernanceStabilityPolicy().assess(
        bounded_governance_maintained=True,
        uncontrolled_expansion_detected=False,
        stale_governance_accumulation=True,
        governance_oscillation=False,
        repeated_rollover_instability=True,
        persistence_instability=True,
        retrieval_instability=False,
    )

    assert frame.stability_score < 100
    assert frame.instability_detected is True
    assert frame.stabilization_recommended is True
    assert frame.compact_governance_recommended is True


def test_governance_health_runtime_maps_healthy_state() -> None:
    governance_health, _ = _evaluate_governance_health()

    assert governance_health.status == "HEALTHY"
    assert governance_health.summary == "GOVERNANCE_HEALTHY"
    assert governance_health.reasons == ("ROOT_CAUSE_GOVERNANCE_HEALTHY",)


def test_governance_health_runtime_maps_degraded_state() -> None:
    governance_health, governance_trace = _evaluate_governance_health(
        unresolved_validation_issues=1
    )

    assert governance_health.status == "DEGRADED"
    assert governance_health.summary == "GOVERNANCE_DEGRADED"
    assert governance_trace.root_cause == "VALIDATION_STATUS_PASSED_WITH_WARNINGS"
    assert governance_health.reasons == (
        "REPOSITORY_READY_WITH_WARNINGS",
        "VALIDATION_PASSED_WITH_WARNINGS",
        "ROOT_CAUSE_VALIDATION_STATUS_PASSED_WITH_WARNINGS",
    )


def test_governance_health_runtime_maps_unhealthy_state() -> None:
    governance_health, governance_trace = _evaluate_governance_health(pytest_passed=False)

    assert governance_health.status == "UNHEALTHY"
    assert governance_health.summary == "GOVERNANCE_UNHEALTHY"
    assert governance_trace.root_cause == "VALIDATION_STATUS_FAILED"
    assert governance_health.reasons == (
        "REPOSITORY_NOT_READY",
        "VALIDATION_FAILED",
        "ROOT_CAUSE_VALIDATION_STATUS_FAILED",
    )


@pytest.mark.parametrize(
    ("runtime_kwargs", "expected_summary"),
    (
        ({}, "GOVERNANCE_HEALTHY"),
        ({"unresolved_validation_issues": 1}, "GOVERNANCE_DEGRADED"),
        ({"pytest_passed": False}, "GOVERNANCE_UNHEALTHY"),
    ),
)
def test_governance_health_summary_mapping_is_deterministic(
    runtime_kwargs: dict[str, object],
    expected_summary: str,
) -> None:
    governance_health, _ = _evaluate_governance_health(**runtime_kwargs)

    assert governance_health.summary == expected_summary


def test_governance_health_history_retention_is_bounded_and_oldest_first() -> None:
    history = ("history-1", "history-2", "history-3", "history-4", "history-5")

    governance_health, _ = _evaluate_governance_health(health_history=history)

    assert governance_health.retention_limit == MAX_HEALTH_HISTORY_RETENTION
    assert governance_health.evicted_health_history == ("history-1", "history-2")
    assert governance_health.retained_health_history[:3] == (
        "history-3",
        "history-4",
        "history-5",
    )
    assert governance_health.retained_health_history[-1].startswith(
        "status=HEALTHY;summary=GOVERNANCE_HEALTHY;"
    )


def test_no_network_dependency_or_autonomous_enforcement() -> None:
    import ai_dev_os.governance_health as governance_health_runtime
    import ai_dev_os.governance_health.governance_dashboard as dashboard
    import ai_dev_os.governance_health.health_score as health
    import ai_dev_os.governance_health.pressure_aggregation as pressure
    import ai_dev_os.governance_health.risk_aggregation as risk
    import ai_dev_os.governance_health.stability_assessment as stability

    source = "\n".join(
        inspect.getsource(module)
        for module in (
            governance_health_runtime,
            dashboard,
            health,
            pressure,
            risk,
            stability,
        )
    ).lower()

    assert "requests" not in source
    assert "http" not in source
    assert "subprocess" not in source
    assert "shutdown" not in source
    assert "git commit" not in source
    assert "git push" not in source
    assert "upload(" not in source


def test_runtime_audit_projects_canonical_governance_health_surface() -> None:
    report = run_runtime_enforcement_audit()

    assert report.governance_health.governance_health_active is True
    assert report.governance_health.governance_pressure_active is True
    assert report.governance_health.governance_risk_active is True
    assert report.governance_health.governance_dashboard_active is True
    assert report.governance_health.governance_stability_active is True
    assert report.governance_health.estimated_avoided_governance_drift > 0
    assert report.governance_health.governance_health.status == "DEGRADED"
    assert report.governance_health.governance_health.summary == "GOVERNANCE_DEGRADED"
    assert report.governance_health.governance_health.reasons == (
        "REPOSITORY_READY_WITH_WARNINGS",
        "VALIDATION_PASSED_WITH_WARNINGS",
        "MERGE_READY_WITH_WARNINGS",
        "READINESS_BELOW_READY_THRESHOLD",
        "OPERATOR_STATUS_ATTENTION",
        "RISK_LEVEL_MODERATE",
        "ROOT_CAUSE_VALIDATION_STATUS_PASSED_WITH_WARNINGS",
    )


def test_runtime_audit_failed_validation_propagates_unhealthy_governance() -> None:
    report = run_runtime_enforcement_audit(
        release_check_inputs=ReleaseCheckInputs(
            pytest_passed=True,
            ruff_passed=False,
            audit_passed=True,
            diff_check_passed=True,
        )
    )

    assert report.validation_evidence.status == "FAILED"
    assert report.repository_readiness.status == "NOT_READY"
    assert report.governance_health.governance_health.status == "UNHEALTHY"
    assert report.governance_health.governance_health.summary == "GOVERNANCE_UNHEALTHY"
    assert "VALIDATION_FAILED" in report.governance_health.governance_health.reasons
