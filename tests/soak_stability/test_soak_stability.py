from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.soak_stability import (
    MAX_SOAK_HISTORY,
    MAX_SOAK_WINDOW,
    SOAK_BUDGET_LIMIT,
    SOAK_STABILITY_REQUIREMENT_IDS,
    SOAK_STABILITY_TEST_IDS,
    SoakStabilityRuntime,
)


def test_tc_soakstability_01_active_runtime_is_bounded_local_patch() -> None:
    frame = SoakStabilityRuntime().evaluate()

    assert frame.soak_stability_active is True
    assert frame.requirement_ids == SOAK_STABILITY_REQUIREMENT_IDS
    assert frame.test_ids == SOAK_STABILITY_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.soak_stability_mode == "LOCAL_PATCH_BOUNDED_SOAK_STABILITY"


def test_tc_soakstability_02_long_session_drift_evaluation() -> None:
    frame = SoakStabilityRuntime().evaluate(
        long_session_age_pressure=48,
        operational_drift_pressure=3,
    )

    assert frame.long_session_drift.long_session_drift_active is True
    assert frame.long_session_stability_score < 60
    assert frame.long_session_drift.bounded_long_session_recommendation == (
        "RESET_LONG_SESSION_WINDOW"
    )


def test_tc_soakstability_03_retry_accumulation_evaluation() -> None:
    frame = SoakStabilityRuntime().evaluate(
        retry_accumulation=4,
        retry_saturation_persistence=3,
        retry_cooldown_degradation=2,
        retry_recovery_drift=2,
    )

    assert frame.retry_accumulation.retry_accumulation_active is True
    assert frame.retry_accumulation_score < 60
    assert frame.retry_accumulation.bounded_retry_survivability_recommendation == (
        "RECOVER_RETRY_ACCUMULATION"
    )


def test_tc_soakstability_04_provider_fatigue_accumulation_evaluation() -> None:
    frame = SoakStabilityRuntime().evaluate(
        provider_fatigue_accumulation=3,
        provider_readiness_degradation_persistence=2,
        provider_cooldown_persistence=2,
        provider_queue_drift=3,
    )

    assert frame.provider_fatigue_accumulation.provider_fatigue_accumulation_active is True
    assert frame.provider_fatigue_accumulation_score < 60
    assert "fatigue=" in frame.provider_fatigue_accumulation.deterministic_provider_fatigue_summary
    assert frame.provider_fatigue_accumulation.bounded_provider_survivability_recommendation == (
        "REBALANCE_PROVIDER_FATIGUE"
    )


def test_tc_soakstability_05_continuation_entropy_evaluation() -> None:
    frame = SoakStabilityRuntime().evaluate(
        continuation_entropy=3,
        continuation_drift_accumulation=3,
        continuation_reset_persistence=2,
        continuation_interruption_degradation=2,
    )

    assert frame.continuation_entropy.continuation_entropy_active is True
    assert frame.continuation_entropy_score < 60
    assert frame.continuation_entropy.bounded_continuation_survivability_recommendation == (
        "RESET_CONTINUATION_ENTROPY"
    )


def test_tc_soakstability_06_orchestration_queue_drift_evaluation() -> None:
    frame = SoakStabilityRuntime().evaluate(
        orchestration_queue_drift=3,
        orchestration_dependency_accumulation=2,
        orchestration_cooldown_persistence=2,
        orchestration_regression_accumulation=3,
    )

    assert frame.orchestration_queue_drift.orchestration_queue_drift_active is True
    assert frame.orchestration_queue_drift_score < 60
    assert frame.orchestration_queue_drift.bounded_orchestration_survivability_recommendation == (
        "RECOVER_ORCHESTRATION_QUEUE"
    )


def test_tc_soakstability_07_runtime_interaction_entropy_evaluation() -> None:
    frame = SoakStabilityRuntime().evaluate(runtime_interaction_entropy=6)

    assert frame.runtime_interaction_entropy.runtime_interaction_entropy_active is True
    assert frame.runtime_interaction_entropy_score < 75
    assert frame.runtime_interaction_entropy.bounded_interaction_survivability_recommendation == (
        "SURFACE_RUNTIME_INTERACTION_ENTROPY"
    )


def test_tc_soakstability_08_recursive_soak_blocking() -> None:
    frame = SoakStabilityRuntime().evaluate(recursive_soak_attempts=1)

    assert frame.soak_governance.recursive_soak_optimization_blocked is True
    assert frame.soak_termination.recursive_soak_detected is True
    assert "RECURSIVE_SOAK_DETECTED" in frame.soak_termination.termination_reasons


def test_tc_soakstability_09_soak_governance_enforcement() -> None:
    frame = SoakStabilityRuntime().evaluate(
        autonomous_runtime_state_mutation_attempts=1,
        novel_stabilization_logic_attempts=1,
        dynamic_soak_scope_widening_attempts=1,
        governance_policy_mutation_attempts=1,
        hidden_persistence_loop_attempts=1,
    )

    assert frame.soak_governance.local_patch_scope_enforced is True
    assert frame.soak_governance.deterministic_soak_enforced is True
    assert frame.soak_governance.autonomous_runtime_state_mutation_blocked is True
    assert frame.soak_governance.novel_stabilization_logic_blocked is True
    assert frame.soak_governance.dynamic_soak_scope_widening_blocked is True
    assert frame.soak_governance.hidden_persistence_loop_blocked is True
    assert frame.soak_termination.governance_violation_detected is True


def test_tc_soakstability_10_soak_termination_handling() -> None:
    history = tuple(f"history_{index}" for index in range(12))
    scope = tuple(f"scope_{index}" for index in range(12))
    frame = SoakStabilityRuntime().evaluate(
        soak_history_items=history,
        soak_scope_items=scope,
        soak_budget_used=SOAK_BUDGET_LIMIT + 1,
        retry_accumulation=4,
        continuation_entropy=5,
        orchestration_queue_drift=4,
    )

    assert frame.soak_termination.soak_stability_terminated is True
    assert frame.soak_termination.soak_budget_exceeded is True
    assert frame.soak_termination.soak_saturation_threshold_exceeded is True
    assert "SOAK_BUDGET_EXCEEDED" in frame.soak_termination.termination_reasons


def test_tc_soakstability_11_bounded_soak_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    scope = tuple(f"scope_{index}" for index in range(9))
    frame = SoakStabilityRuntime().evaluate(
        soak_history_items=history,
        soak_scope_items=scope,
    )

    assert len(frame.soak_history.soak_history) == MAX_SOAK_HISTORY
    assert len(frame.soak_history.soak_scope) == MAX_SOAK_WINDOW
    assert frame.soak_history.soak_history_overflow_blocked is True
    assert frame.soak_history.soak_scope_overflow_blocked is True
    assert frame.soak_eviction.evicted_soak_history_items == history[MAX_SOAK_HISTORY:]
    assert frame.soak_eviction.evicted_soak_scope_items == scope[MAX_SOAK_WINDOW:]


def test_tc_soakstability_12_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().soak_stability

    assert report.soak_stability_active is True
    assert 0 <= report.long_session_stability_score <= 100
    assert 0 <= report.retry_accumulation_score <= 100
    assert 0 <= report.provider_fatigue_accumulation_score <= 100
    assert 0 <= report.continuation_entropy_score <= 100
    assert 0 <= report.orchestration_queue_drift_score <= 100
    assert report.estimated_avoided_slow_degradation > 0
    assert report.estimated_avoided_runtime_entropy > 0
    assert report.estimated_avoided_frontier_stabilization > 0


def test_tc_soakstability_13_runtime_is_deterministic() -> None:
    first = SoakStabilityRuntime().evaluate()
    second = SoakStabilityRuntime().evaluate()

    assert first == second
    assert first.soak_confidence.deterministic_confidence is True
    assert first.stability_retention.bounded_operational_retention is True
    assert first.runtime_interaction_entropy.bounded_continuation_policy_coherence is True
