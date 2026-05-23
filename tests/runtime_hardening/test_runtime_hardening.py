from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.runtime_hardening import (
    ESCALATION_OSCILLATION_THRESHOLD,
    HARDENING_BUDGET_LIMIT,
    MAX_HARDENING_HISTORY,
    RETRY_AMPLIFICATION_THRESHOLD,
    RUNTIME_HARDENING_REQUIREMENT_IDS,
    RUNTIME_HARDENING_TEST_IDS,
    RuntimeHardeningRuntime,
)


def test_tc_runtimehardening_01_active_runtime_is_bounded_local_patch() -> None:
    frame = RuntimeHardeningRuntime().evaluate()

    assert frame.runtime_hardening_active is True
    assert frame.requirement_ids == RUNTIME_HARDENING_REQUIREMENT_IDS
    assert frame.test_ids == RUNTIME_HARDENING_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.runtime_hardening_mode == "LOCAL_PATCH_BOUNDED_RUNTIME_HARDENING"


def test_tc_runtimehardening_02_retry_storm_suppression() -> None:
    frame = RuntimeHardeningRuntime().evaluate(
        retry_amplification_chains=RETRY_AMPLIFICATION_THRESHOLD + 2,
        retry_recursion_pressure=2,
        retry_cooldown_collapse=2,
        retry_saturation_windows=3,
        retry_interruption_instability=2,
    )

    assert frame.retry_storm.retry_storm_active is True
    assert frame.retry_storm.retry_storm_score < 55
    assert frame.retry_storm.bounded_retry_reset_recommendation == (
        "RESET_RETRY_STORM_WINDOW_AFTER_COOLDOWN"
    )
    assert frame.cooldown_interaction.retry_cooldown_required is True
    assert frame.hardening_termination.retry_amplification_threshold_exceeded is True


def test_tc_runtimehardening_03_escalation_oscillation_suppression() -> None:
    frame = RuntimeHardeningRuntime().evaluate(
        provider_escalation_loops=ESCALATION_OSCILLATION_THRESHOLD,
        provider_downgrade_loops=2,
        repeated_escalation_chains=2,
    )

    assert frame.escalation_oscillation.escalation_oscillation_active is True
    assert frame.escalation_oscillation.bounded_provider_oscillation is False
    assert frame.escalation_oscillation.bounded_escalation_stabilization_recommendation == (
        "FREEZE_PROVIDER_ESCALATION_AND_COOLDOWN"
    )
    assert frame.cooldown_interaction.escalation_cooldown_required is True
    assert frame.hardening_termination.escalation_oscillation_threshold_exceeded is True


def test_tc_runtimehardening_04_continuation_stabilization() -> None:
    frame = RuntimeHardeningRuntime().evaluate(
        continuation_collapse_chains=3,
        continuation_saturation=60,
        continuation_interruption_instability=2,
        continuation_reset_loops=2,
        bounded_continuation_starvation=1,
    )

    assert frame.continuation_collapse.continuation_collapse_active is True
    assert frame.continuation_stability_score < 55
    assert frame.continuation_collapse.bounded_continuation_reset_recommendation == (
        "RESET_CONTINUATION_STABILIZATION_WINDOW"
    )
    assert frame.cooldown_interaction.continuation_cooldown_required is True


def test_tc_runtimehardening_05_provider_starvation_detection() -> None:
    frame = RuntimeHardeningRuntime().evaluate(
        provider_readiness_starvation=2,
        cooldown_starvation=2,
        bounded_provider_queue_saturation=3,
        provider_scheduling_instability=3,
        provider_confidence_collapse=2,
    )

    assert frame.provider_starvation.provider_starvation_active is True
    assert frame.provider_starvation_score < 55
    assert frame.provider_starvation.bounded_provider_rebalance_recommendation == (
        "REBALANCE_PROVIDER_WINDOW_AFTER_COOLDOWN"
    )
    assert frame.cooldown_interaction.provider_cooldown_required is True


def test_tc_runtimehardening_06_provider_fatigue_stabilizes_starvation_window() -> None:
    frame = RuntimeHardeningRuntime().evaluate()

    assert "fatigue=" in frame.provider_starvation.deterministic_provider_starvation_summary
    assert frame.provider_starvation.bounded_provider_rebalance_recommendation == (
        "REBALANCE_PROVIDER_WINDOW_AFTER_COOLDOWN"
    )
    assert frame.cooldown_interaction.provider_cooldown_required is True
    assert frame.provider_starvation_score < 70


def test_tc_runtimehardening_07_orchestration_deadlock_detection() -> None:
    frame = RuntimeHardeningRuntime().evaluate(
        orchestration_dependency_deadlocks=2,
        validation_retry_deadlocks=1,
        provider_policy_deadlocks=1,
        continuation_termination_conflicts=1,
        bounded_orchestration_stalls=1,
    )

    assert frame.orchestration_deadlock.orchestration_deadlock_active is True
    assert frame.orchestration_deadlock_score < 55
    assert frame.orchestration_deadlock.bounded_deadlock_recovery_recommendation == (
        "RESET_ORCHESTRATION_DEADLOCK_WINDOW"
    )
    assert frame.runtime_conflict.validation_retry_conflict is True
    assert frame.runtime_conflict.provider_policy_conflict is True
    assert frame.runtime_conflict.continuation_termination_conflict is True


def test_tc_runtimehardening_08_recursive_stabilization_blocking() -> None:
    frame = RuntimeHardeningRuntime().evaluate(recursive_stabilization_attempts=1)

    assert frame.interaction_governance.deterministic_interaction_governance is True
    assert frame.hardening_termination.recursive_stabilization_detected is True
    assert "RECURSIVE_STABILIZATION_DETECTED" in (frame.hardening_termination.termination_reasons)


def test_tc_runtimehardening_09_runtime_governance_enforcement() -> None:
    frame = RuntimeHardeningRuntime().evaluate(
        autonomous_runtime_mutation_attempts=1,
        hidden_orchestration_execution_attempts=1,
        self_expanding_stabilization_graph_attempts=1,
        autonomous_provider_escalation_attempts=1,
        governance_policy_mutation_attempts=1,
        retrieval_scope_widening_attempts=1,
    )

    assert frame.interaction_governance.local_patch_scope_enforced is True
    assert frame.interaction_governance.bounded_retry_authority is True
    assert frame.interaction_governance.bounded_orchestration_authority is True
    assert frame.interaction_governance.bounded_escalation_authority is True
    assert frame.hardening_termination.governance_violation_detected is True
    assert "GOVERNANCE_VIOLATION_DETECTED" in frame.hardening_termination.termination_reasons


def test_tc_runtimehardening_10_hardening_termination_handling() -> None:
    frame = RuntimeHardeningRuntime().evaluate(
        hardening_budget_used=HARDENING_BUDGET_LIMIT + 1,
        retry_amplification_chains=RETRY_AMPLIFICATION_THRESHOLD + 1,
        provider_escalation_loops=ESCALATION_OSCILLATION_THRESHOLD,
        provider_downgrade_loops=1,
        repeated_escalation_chains=1,
        orchestration_dependency_deadlocks=3,
        bounded_orchestration_stalls=2,
    )

    assert frame.hardening_termination.hardening_terminated is True
    assert frame.hardening_termination.hardening_budget_exceeded is True
    assert frame.hardening_termination.retry_amplification_threshold_exceeded is True
    assert frame.hardening_termination.escalation_oscillation_threshold_exceeded is True
    assert frame.hardening_termination.orchestration_saturation_threshold_exceeded is True
    assert "HARDENING_BUDGET_EXCEEDED" in frame.hardening_termination.termination_reasons


def test_tc_runtimehardening_11_bounded_hardening_history_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    frame = RuntimeHardeningRuntime().evaluate(hardening_history_items=history)

    assert len(frame.hardening_history.hardening_history) == MAX_HARDENING_HISTORY
    assert frame.hardening_history.hardening_history_overflow_blocked is True
    assert frame.hardening_eviction.evicted_history_items == history[MAX_HARDENING_HISTORY:]
    assert frame.hardening_eviction.bounded_eviction_active is True


def test_tc_runtimehardening_12_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().runtime_hardening

    assert report.runtime_hardening_active is True
    assert 0 <= report.retry_storm_score <= 100
    assert 0 <= report.escalation_oscillation_score <= 100
    assert 0 <= report.continuation_stability_score <= 100
    assert 0 <= report.provider_starvation_score <= 100
    assert 0 <= report.orchestration_deadlock_score <= 100
    assert report.estimated_avoided_retry_storms > 0
    assert report.estimated_avoided_orchestration_collapse > 0
    assert report.estimated_avoided_frontier_stabilization > 0


def test_tc_runtimehardening_13_runtime_is_deterministic() -> None:
    first = RuntimeHardeningRuntime().evaluate()
    second = RuntimeHardeningRuntime().evaluate()

    assert first == second
    assert first.interaction_governance.deterministic_interaction_governance is True
    assert first.hardening_confidence.resilient_interaction_confidence is True
    assert first.orchestration_deadlock.orchestration_deadlock_score >= 80
