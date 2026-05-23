from __future__ import annotations

from ai_dev_os.failure_injection import (
    FAILURE_INJECTION_REQUIREMENT_IDS,
    FAILURE_INJECTION_TEST_IDS,
    INJECTION_BUDGET_LIMIT,
    MAX_INJECTION_HISTORY,
    MAX_INJECTION_WINDOW,
    FailureInjectionRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_failureinjection_01_active_runtime_is_bounded_local_patch() -> None:
    frame = FailureInjectionRuntime().evaluate()

    assert frame.failure_injection_active is True
    assert frame.requirement_ids == FAILURE_INJECTION_REQUIREMENT_IDS
    assert frame.test_ids == FAILURE_INJECTION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.failure_injection_mode == "LOCAL_PATCH_BOUNDED_FAILURE_INJECTION"


def test_tc_failureinjection_02_retry_storm_injection() -> None:
    frame = FailureInjectionRuntime().evaluate(
        retry_amplification=4,
        retry_saturation=3,
        retry_cooldown_collapse=2,
        retry_interruption_instability=2,
    )

    assert frame.retry_storm_injection.retry_storm_injection_active is True
    assert frame.retry_injection_score < 60
    assert frame.retry_storm_injection.bounded_retry_recovery_recommendation == (
        "RECOVER_RETRY_WINDOW_WITH_COOLDOWN"
    )


def test_tc_failureinjection_03_provider_starvation_injection() -> None:
    frame = FailureInjectionRuntime().evaluate(
        provider_starvation=3,
        provider_fatigue_escalation=3,
        provider_readiness_degradation=2,
        provider_queue_saturation=3,
    )

    assert frame.provider_starvation_injection.provider_starvation_injection_active is True
    assert frame.provider_injection_score < 60
    assert (
        "fatigue=" in frame.provider_starvation_injection.deterministic_provider_injection_summary
    )
    assert frame.provider_starvation_injection.bounded_provider_rebalance_recommendation == (
        "REBALANCE_PROVIDER_AFTER_COOLDOWN"
    )


def test_tc_failureinjection_04_continuation_collapse_injection() -> None:
    frame = FailureInjectionRuntime().evaluate(
        continuation_interruption_collapse=3,
        continuation_saturation=62,
        continuation_reset_loops=2,
        continuation_drift=2,
    )

    assert frame.continuation_collapse_injection.continuation_collapse_injection_active is True
    assert frame.continuation_injection_score < 60
    assert frame.continuation_collapse_injection.bounded_continuation_reset_recommendation == (
        "RESET_CONTINUATION_AFTER_INJECTION"
    )


def test_tc_failureinjection_05_orchestration_deadlock_injection() -> None:
    frame = FailureInjectionRuntime().evaluate(
        dependency_deadlocks=2,
        validation_retry_conflicts=2,
        provider_policy_conflicts=2,
        orchestration_queue_stalls=2,
    )

    assert frame.orchestration_deadlock_injection.orchestration_deadlock_injection_active is True
    assert frame.orchestration_injection_score < 60
    assert (
        frame.orchestration_deadlock_injection.bounded_orchestration_recovery_recommendation
        == ("RECOVER_ORCHESTRATION_AFTER_DEADLOCK")
    )


def test_tc_failureinjection_06_recovery_validation() -> None:
    frame = FailureInjectionRuntime().evaluate()

    assert frame.runtime_recovery_injection.runtime_recovery_injection_active is True
    assert frame.runtime_recovery_injection.bounded_recovery_validation is True
    assert frame.runtime_recovery_injection.bounded_cooldown_recovery is True
    assert frame.runtime_recovery_injection.bounded_provider_rebalance is True
    assert frame.runtime_recovery_injection.bounded_continuation_reset_recovery is True
    assert frame.recovery_resilience_score >= 80


def test_tc_failureinjection_07_recursive_injection_blocking() -> None:
    frame = FailureInjectionRuntime().evaluate(recursive_injection_attempts=1)

    assert frame.injection_governance.recursive_injection_blocked is True
    assert frame.injection_termination.recursive_injection_detected is True
    assert "RECURSIVE_INJECTION_DETECTED" in frame.injection_termination.termination_reasons


def test_tc_failureinjection_08_injection_governance_enforcement() -> None:
    frame = FailureInjectionRuntime().evaluate(
        autonomous_runtime_state_mutation_attempts=1,
        novel_attack_pattern_synthesis_attempts=1,
        dynamic_injection_scope_widening_attempts=1,
        governance_policy_mutation_attempts=1,
        hidden_chaos_loop_attempts=1,
    )

    assert frame.injection_governance.local_patch_scope_enforced is True
    assert frame.injection_governance.deterministic_injection_enforced is True
    assert frame.injection_governance.autonomous_runtime_state_mutation_blocked is True
    assert frame.injection_governance.novel_attack_pattern_synthesis_blocked is True
    assert frame.injection_governance.dynamic_injection_scope_widening_blocked is True
    assert frame.injection_governance.hidden_chaos_loop_blocked is True
    assert frame.injection_termination.governance_violation_detected is True


def test_tc_failureinjection_09_injection_termination_handling() -> None:
    history = tuple(f"history_{index}" for index in range(12))
    scope = tuple(f"scope_{index}" for index in range(12))
    frame = FailureInjectionRuntime().evaluate(
        injection_history_items=history,
        injection_scope_items=scope,
        injection_budget_used=INJECTION_BUDGET_LIMIT + 1,
        retry_amplification=4,
        continuation_saturation=82,
        dependency_deadlocks=3,
    )

    assert frame.injection_termination.failure_injection_terminated is True
    assert frame.injection_termination.injection_budget_exceeded is True
    assert frame.injection_termination.injection_saturation_threshold_exceeded is True
    assert "INJECTION_BUDGET_EXCEEDED" in frame.injection_termination.termination_reasons


def test_tc_failureinjection_10_bounded_injection_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    scope = tuple(f"scope_{index}" for index in range(9))
    frame = FailureInjectionRuntime().evaluate(
        injection_history_items=history,
        injection_scope_items=scope,
    )

    assert len(frame.injection_history.injection_history) == MAX_INJECTION_HISTORY
    assert len(frame.injection_history.injection_scope) == MAX_INJECTION_WINDOW
    assert frame.injection_history.injection_history_overflow_blocked is True
    assert frame.injection_history.injection_scope_overflow_blocked is True
    assert (
        frame.injection_eviction.evicted_injection_history_items == history[MAX_INJECTION_HISTORY:]
    )
    assert frame.injection_eviction.evicted_injection_scope_items == scope[MAX_INJECTION_WINDOW:]


def test_tc_failureinjection_11_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().failure_injection

    assert report.failure_injection_active is True
    assert 0 <= report.retry_injection_score <= 100
    assert 0 <= report.provider_injection_score <= 100
    assert 0 <= report.continuation_injection_score <= 100
    assert 0 <= report.orchestration_injection_score <= 100
    assert 0 <= report.recovery_resilience_score <= 100
    assert report.estimated_avoided_runtime_collapse > 0
    assert report.estimated_avoided_frontier_recovery > 0
    assert report.estimated_avoided_hidden_instability > 0


def test_tc_failureinjection_12_runtime_is_deterministic() -> None:
    first = FailureInjectionRuntime().evaluate()
    second = FailureInjectionRuntime().evaluate()

    assert first == second
    assert first.injection_confidence.deterministic_confidence is True
    assert first.injection_confidence.resilience_validation_confidence is True
    assert first.runtime_recovery_injection.bounded_recovery_validation is True
