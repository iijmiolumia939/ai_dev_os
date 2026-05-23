from __future__ import annotations

from ai_dev_os.continuous_runtime_audit import (
    AUDIT_BUDGET_LIMIT,
    CONTINUOUS_RUNTIME_AUDIT_REQUIREMENT_IDS,
    CONTINUOUS_RUNTIME_AUDIT_TEST_IDS,
    MAX_AUDIT_HISTORY,
    MAX_TELEMETRY_WINDOW,
    ContinuousRuntimeAuditRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_continuousaudit_01_active_runtime_is_bounded_local_patch() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate()

    assert frame.continuous_runtime_audit_active is True
    assert frame.requirement_ids == CONTINUOUS_RUNTIME_AUDIT_REQUIREMENT_IDS
    assert frame.test_ids == CONTINUOUS_RUNTIME_AUDIT_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.continuous_runtime_audit_mode == "LOCAL_PATCH_BOUNDED_CONTINUOUS_AUDIT"


def test_tc_continuousaudit_02_retry_telemetry_surfaces_pressure() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate(
        retry_amplification_pressure=4,
        retry_saturation_windows=3,
        retry_interruption_instability=2,
        retry_cooldown_collapse=2,
        retry_recovery_instability=2,
    )

    assert frame.retry_pressure.retry_pressure_active is True
    assert frame.retry_pressure_score < 60
    assert frame.retry_pressure.bounded_retry_visibility_recommendation == (
        "SURFACE_RETRY_PRESSURE_AND_RESET_WINDOW"
    )


def test_tc_continuousaudit_03_provider_telemetry_tracks_fatigue() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate(
        provider_readiness_degradation=2,
        provider_queue_saturation=3,
        provider_cooldown_instability=2,
        bounded_provider_confidence_collapse=2,
    )

    assert frame.provider_fatigue_telemetry.provider_fatigue_telemetry_active is True
    assert frame.provider_fatigue_score < 60
    assert "adjacent_fatigue=" in (
        frame.provider_fatigue_telemetry.deterministic_provider_fatigue_summary
    )
    assert frame.provider_fatigue_telemetry.bounded_provider_visibility_recommendation == (
        "SURFACE_PROVIDER_FATIGUE_AND_REBALANCE"
    )


def test_tc_continuousaudit_04_continuation_telemetry_tracks_instability() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate(
        continuation_instability_pressure=3,
        continuation_saturation=58,
        continuation_interruption_instability=2,
        continuation_reset_loops=2,
        bounded_continuation_drift=2,
    )

    assert frame.continuation_instability.continuation_instability_active is True
    assert frame.continuation_instability_score < 60
    assert frame.continuation_instability.bounded_continuation_visibility_recommendation == (
        "SURFACE_CONTINUATION_INSTABILITY_AND_RESET"
    )


def test_tc_continuousaudit_05_orchestration_telemetry_tracks_pressure() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate(
        orchestration_queue_pressure=3,
        orchestration_dependency_stalls=2,
        orchestration_cooldown_pressure=2,
        orchestration_regression_pressure=2,
        bounded_orchestration_drift=2,
    )

    assert frame.orchestration_pressure.orchestration_pressure_active is True
    assert frame.orchestration_pressure_score < 60
    assert frame.orchestration_pressure.bounded_orchestration_visibility_recommendation == (
        "SURFACE_ORCHESTRATION_PRESSURE_AND_STALLS"
    )


def test_tc_continuousaudit_06_runtime_health_evaluation() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate()

    assert frame.runtime_health.runtime_health_active is True
    assert frame.runtime_health.bounded_runtime_coherence is True
    assert frame.runtime_health.bounded_orchestration_stability is True
    assert frame.runtime_health.bounded_retry_stability is True
    assert frame.runtime_health.bounded_provider_stability is True
    assert frame.runtime_health.bounded_continuation_stability is True
    assert frame.runtime_health_score >= 75


def test_tc_continuousaudit_07_recursive_telemetry_blocking() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate(recursive_telemetry_attempts=1)

    assert frame.audit_termination.recursive_telemetry_detected is True
    assert "RECURSIVE_TELEMETRY_DETECTED" in frame.audit_termination.termination_reasons
    assert frame.audit_governance.recursive_telemetry_optimization_blocked is True


def test_tc_continuousaudit_08_audit_governance_enforcement() -> None:
    frame = ContinuousRuntimeAuditRuntime().evaluate(
        autonomous_runtime_alteration_attempts=1,
        recursive_telemetry_optimization_attempts=1,
        novel_metric_synthesis_attempts=1,
        dynamic_telemetry_scope_widening_attempts=1,
        governance_policy_mutation_attempts=1,
        hidden_background_execution_attempts=1,
    )

    assert frame.audit_governance.local_patch_scope_enforced is True
    assert frame.audit_governance.deterministic_telemetry_enforced is True
    assert frame.audit_governance.autonomous_runtime_alteration_blocked is True
    assert frame.audit_governance.novel_metric_synthesis_blocked is True
    assert frame.audit_governance.dynamic_telemetry_scope_widening_blocked is True
    assert frame.audit_governance.hidden_background_execution_blocked is True
    assert frame.audit_termination.governance_violation_detected is True


def test_tc_continuousaudit_09_audit_termination_handling() -> None:
    telemetry_scope = tuple(f"scope_{index}" for index in range(12))
    frame = ContinuousRuntimeAuditRuntime().evaluate(
        telemetry_scope_items=telemetry_scope,
        audit_budget_used=AUDIT_BUDGET_LIMIT + 1,
        retry_amplification_pressure=4,
        continuation_saturation=80,
        orchestration_dependency_stalls=3,
    )

    assert frame.audit_termination.continuous_audit_terminated is True
    assert frame.audit_termination.audit_budget_exceeded is True
    assert frame.audit_termination.telemetry_saturation_threshold_exceeded is True
    assert "AUDIT_BUDGET_EXCEEDED" in frame.audit_termination.termination_reasons


def test_tc_continuousaudit_10_bounded_telemetry_retention() -> None:
    telemetry_scope = tuple(f"scope_{index}" for index in range(9))
    history = tuple(f"history_{index}" for index in range(9))
    frame = ContinuousRuntimeAuditRuntime().evaluate(
        telemetry_scope_items=telemetry_scope,
        audit_history_items=history,
    )

    assert len(frame.runtime_telemetry.telemetry_scope) == MAX_TELEMETRY_WINDOW
    assert len(frame.audit_history.audit_history) == MAX_AUDIT_HISTORY
    assert frame.runtime_telemetry.telemetry_scope_overflow_blocked is True
    assert frame.audit_history.audit_history_overflow_blocked is True
    assert (
        frame.audit_eviction.evicted_telemetry_scope_items
        == telemetry_scope[MAX_TELEMETRY_WINDOW:]
    )
    assert frame.audit_eviction.evicted_audit_history_items == history[MAX_AUDIT_HISTORY:]


def test_tc_continuousaudit_11_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().continuous_runtime_audit

    assert report.continuous_runtime_audit_active is True
    assert 0 <= report.runtime_health_score <= 100
    assert 0 <= report.retry_pressure_score <= 100
    assert 0 <= report.provider_fatigue_score <= 100
    assert 0 <= report.continuation_instability_score <= 100
    assert 0 <= report.orchestration_pressure_score <= 100
    assert report.estimated_avoided_runtime_blindness > 0
    assert report.estimated_avoided_orchestration_collapse > 0
    assert report.estimated_avoided_frontier_observability > 0


def test_tc_continuousaudit_12_runtime_is_deterministic() -> None:
    first = ContinuousRuntimeAuditRuntime().evaluate()
    second = ContinuousRuntimeAuditRuntime().evaluate()

    assert first == second
    assert first.runtime_telemetry.bounded_runtime_telemetry is True
    assert first.audit_confidence.deterministic_confidence is True
    assert first.audit_confidence.operational_visibility_confidence is True
