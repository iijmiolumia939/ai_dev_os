from __future__ import annotations

from ai_dev_os.provider_cost_stabilization import (
    COST_BUDGET_LIMIT,
    MAX_COST_HISTORY,
    MAX_COST_WINDOW,
    PROVIDER_COST_STABILIZATION_REQUIREMENT_IDS,
    PROVIDER_COST_STABILIZATION_TEST_IDS,
    ProviderCostStabilizationRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_providercoststabilization_01_active_runtime_is_bounded_local_patch() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate()

    assert frame.provider_cost_stabilization_active is True
    assert frame.requirement_ids == PROVIDER_COST_STABILIZATION_REQUIREMENT_IDS
    assert frame.test_ids == PROVIDER_COST_STABILIZATION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.provider_cost_stabilization_mode == (
        "LOCAL_PATCH_BOUNDED_PROVIDER_COST_STABILIZATION"
    )


def test_tc_providercoststabilization_02_frontier_escalation_suppression() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate(
        unnecessary_escalation_pressure=3,
        escalation_cooldown_instability=2,
        bounded_frontier_routing_pressure=2,
        frontier_dependency_pressure=2,
    )

    assert frame.frontier_escalation_suppression.frontier_escalation_suppression_active is True
    assert frame.frontier_dependency_score < 60
    assert frame.frontier_escalation_suppression.bounded_frontier_recommendation == (
        "SUPPRESS_FRONTIER_ESCALATION"
    )


def test_tc_providercoststabilization_03_retry_cost_flattening() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate(
        retry_cost_accumulation=4,
        retry_saturation_cost=3,
        retry_cooldown_efficiency=1,
        retry_recovery_reuse=1,
    )

    assert frame.retry_cost_flattening.retry_cost_flattening_active is True
    assert frame.retry_cost_score < 60
    assert frame.retry_cost_flattening.bounded_retry_cost_recommendation == (
        "FLATTEN_RETRY_COST_WINDOW"
    )


def test_tc_providercoststabilization_04_continuation_reuse_optimization() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate(
        continuation_reuse_optimization=0,
        continuation_reset_suppression=1,
        continuation_persistence_reuse=1,
        bounded_continuation_cost_drift=3,
    )

    assert frame.continuation_reuse_optimization.continuation_reuse_optimization_active is True
    assert frame.continuation_reuse_score < 60
    assert frame.continuation_reuse_optimization.bounded_continuation_reuse_recommendation == (
        "OPTIMIZE_CONTINUATION_REUSE"
    )


def test_tc_providercoststabilization_05_orchestration_cost_flattening() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate(
        orchestration_cost_flattening=0,
        orchestration_queue_efficiency=1,
        orchestration_dependency_reuse=1,
        orchestration_stabilization_reuse=1,
        orchestration_overhead_pressure=3,
    )

    assert frame.orchestration_cost_flattening.orchestration_cost_flattening_active is True
    assert frame.orchestration_cost_score < 60
    assert frame.orchestration_cost_flattening.bounded_orchestration_cost_recommendation == (
        "FLATTEN_ORCHESTRATION_COST"
    )


def test_tc_providercoststabilization_06_local_first_efficiency() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate(
        local_first_execution_persistence=0,
        bounded_provider_rebalance_cost=4,
        bounded_local_execution_reuse=1,
        provider_specific_reuse=1,
    )

    assert frame.local_first_persistence.local_first_persistence_active is True
    assert frame.local_first_efficiency_score < 60
    assert frame.local_first_persistence.bounded_local_first_recommendation == (
        "PERSIST_LOCAL_FIRST_EXECUTION"
    )


def test_tc_providercoststabilization_07_recursive_optimization_blocking() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate(recursive_provider_optimization_attempts=1)

    assert frame.cost_governance.recursive_provider_optimization_blocked is True
    assert frame.cost_termination.recursive_optimization_detected is True
    assert "RECURSIVE_PROVIDER_OPTIMIZATION_DETECTED" in frame.cost_termination.termination_reasons


def test_tc_providercoststabilization_08_cost_governance_enforcement() -> None:
    frame = ProviderCostStabilizationRuntime().evaluate(
        autonomous_runtime_state_mutation_attempts=1,
        novel_cost_heuristic_synthesis_attempts=1,
        dynamic_routing_scope_widening_attempts=1,
        governance_policy_mutation_attempts=1,
        hidden_optimization_loop_attempts=1,
    )

    assert frame.cost_governance.local_patch_scope_enforced is True
    assert frame.cost_governance.deterministic_cost_evaluation_enforced is True
    assert frame.cost_governance.autonomous_runtime_state_mutation_blocked is True
    assert frame.cost_governance.novel_cost_heuristic_synthesis_blocked is True
    assert frame.cost_governance.dynamic_routing_scope_widening_blocked is True
    assert frame.cost_governance.hidden_optimization_loop_blocked is True
    assert frame.cost_termination.governance_violation_detected is True


def test_tc_providercoststabilization_09_cost_termination_handling() -> None:
    history = tuple(f"history_{index}" for index in range(12))
    scope = tuple(f"scope_{index}" for index in range(12))
    frame = ProviderCostStabilizationRuntime().evaluate(
        cost_history_items=history,
        cost_scope_items=scope,
        cost_budget_used=COST_BUDGET_LIMIT + 1,
        retry_cost_accumulation=4,
        unnecessary_escalation_pressure=3,
        orchestration_cost_flattening=0,
    )

    assert frame.cost_termination.provider_cost_stabilization_terminated is True
    assert frame.cost_termination.cost_budget_exceeded is True
    assert frame.cost_termination.cost_saturation_threshold_exceeded is True
    assert "COST_BUDGET_EXCEEDED" in frame.cost_termination.termination_reasons


def test_tc_providercoststabilization_10_bounded_cost_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    scope = tuple(f"scope_{index}" for index in range(9))
    frame = ProviderCostStabilizationRuntime().evaluate(
        cost_history_items=history,
        cost_scope_items=scope,
    )

    assert len(frame.cost_history.cost_history) == MAX_COST_HISTORY
    assert len(frame.cost_history.cost_scope) == MAX_COST_WINDOW
    assert frame.cost_history.cost_history_overflow_blocked is True
    assert frame.cost_history.cost_scope_overflow_blocked is True
    assert frame.cost_eviction.evicted_cost_history_items == history[MAX_COST_HISTORY:]
    assert frame.cost_eviction.evicted_cost_scope_items == scope[MAX_COST_WINDOW:]


def test_tc_providercoststabilization_11_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().provider_cost_stabilization

    assert report.provider_cost_stabilization_active is True
    assert 0 <= report.frontier_dependency_score <= 100
    assert 0 <= report.retry_cost_score <= 100
    assert 0 <= report.continuation_reuse_score <= 100
    assert 0 <= report.orchestration_cost_score <= 100
    assert 0 <= report.local_first_efficiency_score <= 100
    assert report.estimated_avoided_frontier_escalation > 0
    assert report.estimated_avoided_cost_drift > 0
    assert report.estimated_avoided_runtime_overhead > 0


def test_tc_providercoststabilization_12_runtime_is_deterministic() -> None:
    first = ProviderCostStabilizationRuntime().evaluate()
    second = ProviderCostStabilizationRuntime().evaluate()

    assert first == second
    assert first.cost_confidence.deterministic_confidence is True
    assert first.provider_routing_efficiency.bounded_provider_routing_stabilization is True
    assert first.runtime_cost_pressure.runtime_cost_pressure_active is True
