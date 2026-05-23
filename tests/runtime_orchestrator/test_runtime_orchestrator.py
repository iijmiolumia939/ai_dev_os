from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.runtime_orchestrator import (
    MAX_CONTINUATION_DEPTH,
    MAX_EXECUTION_QUEUE,
    MAX_ORCHESTRATION_HISTORY,
    MAX_PROVIDER_WINDOW,
    MAX_RETRY_QUEUE,
    MAX_VALIDATION_QUEUE,
    ORCHESTRATION_BUDGET_LIMIT,
    RETRY_AMPLIFICATION_THRESHOLD,
    RUNTIME_ORCHESTRATOR_REQUIREMENT_IDS,
    RUNTIME_ORCHESTRATOR_TEST_IDS,
    RuntimeOrchestrator,
)


def test_tc_runtimeorchestrator_01_active_runtime_is_bounded_local_patch() -> None:
    frame = RuntimeOrchestrator().evaluate()

    assert frame.runtime_orchestrator_active is True
    assert frame.requirement_ids == RUNTIME_ORCHESTRATOR_REQUIREMENT_IDS
    assert frame.test_ids == RUNTIME_ORCHESTRATOR_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.runtime_orchestrator_mode == "LOCAL_PATCH_BOUNDED_RUNTIME_ORCHESTRATION"


def test_tc_runtimeorchestrator_02_execution_scheduling_tracks_bounded_queue() -> None:
    execution_queue = tuple(f"execute_{index}" for index in range(8))
    validation_queue = tuple(f"validation_{index}" for index in range(8))
    frame = RuntimeOrchestrator().evaluate(
        execution_queue_items=execution_queue,
        validation_queue_items=validation_queue,
    )

    assert frame.execution_scheduling.execution_scheduling_active is True
    assert len(frame.execution_scheduling.execution_queue) == MAX_EXECUTION_QUEUE
    assert len(frame.execution_scheduling.validation_prerequisites) == MAX_VALIDATION_QUEUE
    assert frame.execution_scheduling.provider_readiness is True
    assert frame.orchestration_eviction.evicted_execution_items == (
        execution_queue[MAX_EXECUTION_QUEUE:]
    )


def test_tc_runtimeorchestrator_03_validation_scheduling_handles_saturation() -> None:
    frame = RuntimeOrchestrator().evaluate(
        validation_completed_count=1,
        validation_interruption_pressure=3,
        validation_saturation_pressure=4,
    )

    assert frame.validation_scheduling.validation_scheduling_active is True
    assert frame.validation_scheduling.validation_saturation >= 70
    assert frame.validation_scheduling.bounded_validation_recommendation == (
        "RESET_VALIDATION_AFTER_COOLDOWN"
    )
    assert frame.validation_schedule_score < 80


def test_tc_runtimeorchestrator_04_retry_scheduling_orders_cooldown() -> None:
    frame = RuntimeOrchestrator().evaluate(
        retry_count=4,
        retry_amplification=RETRY_AMPLIFICATION_THRESHOLD + 1,
        retry_interruption_windows=1,
    )

    assert frame.retry_scheduling.retry_scheduling_active is True
    assert len(frame.retry_scheduling.retry_order) == MAX_RETRY_QUEUE
    assert frame.retry_scheduling.hidden_retry_execution_blocked is True
    assert frame.retry_scheduling.bounded_retry_recommendation == (
        "RESET_RETRY_QUEUE_AFTER_COOLDOWN"
    )
    assert frame.orchestration_termination.retry_amplification_threshold_exceeded is True


def test_tc_runtimeorchestrator_05_continuation_scheduling_resets_depth() -> None:
    frame = RuntimeOrchestrator().evaluate(
        continuation_depth=MAX_CONTINUATION_DEPTH + 2,
        continuation_interruption_windows=2,
    )

    assert frame.continuation_scheduling.continuation_scheduling_active is True
    assert frame.continuation_scheduling.continuation_depth_limit == MAX_CONTINUATION_DEPTH
    assert frame.continuation_scheduling.continuation_reset_timing == "RESET_AFTER_COOLDOWN"
    assert frame.continuation_scheduling.bounded_continuation_recommendation == (
        "RESET_CONTINUATION_WINDOW"
    )
    assert frame.orchestration_termination.continuation_saturation_threshold_exceeded is True


def test_tc_runtimeorchestrator_06_provider_scheduling_is_bounded() -> None:
    provider_queue = tuple(f"provider_{index}" for index in range(7))
    frame = RuntimeOrchestrator().evaluate(provider_queue_items=provider_queue)

    assert frame.provider_scheduling.provider_scheduling_active is True
    assert len(frame.provider_scheduling.provider_order) == MAX_PROVIDER_WINDOW
    assert frame.provider_scheduling.provider_readiness is True
    assert frame.provider_scheduling.bounded_provider_recommendation == (
        "USE_LOCAL_PROVIDER_WINDOW"
    )
    assert frame.orchestration_eviction.evicted_provider_items == (
        provider_queue[MAX_PROVIDER_WINDOW:]
    )


def test_tc_runtimeorchestrator_07_orchestration_coordination_orders_conflicts() -> None:
    frame = RuntimeOrchestrator().evaluate()

    assert frame.orchestration_coordination.orchestration_coordination_active is True
    assert frame.orchestration_coordination.validation_vs_retry_ordering == (
        "VALIDATION_BEFORE_RETRY_RESET"
    )
    assert frame.orchestration_coordination.continuation_vs_termination_ordering == (
        "TERMINATION_BEFORE_CONTINUATION"
    )
    assert frame.orchestration_coordination.commit_readiness_vs_validation_ordering == (
        "VALIDATION_BEFORE_COMMIT_READY"
    )
    assert frame.orchestration_coordination.orchestration_coordination_score >= 80


def test_tc_runtimeorchestrator_08_recursive_orchestration_blocking() -> None:
    frame = RuntimeOrchestrator().evaluate(recursive_orchestration_attempts=1)

    assert frame.orchestration_governance.recursive_orchestration_blocked is True
    assert frame.orchestration_termination.recursive_orchestration_detected is True
    assert "RECURSIVE_ORCHESTRATION_DETECTED" in (
        frame.orchestration_termination.termination_reasons
    )


def test_tc_runtimeorchestrator_09_orchestration_governance_enforcement() -> None:
    frame = RuntimeOrchestrator().evaluate(
        orchestration_scope_expansion_attempts=1,
        hidden_orchestration_execution_attempts=1,
        autonomous_branch_mutation_attempts=1,
        autonomous_governance_mutation_attempts=1,
        self_expanding_orchestration_graph_attempts=1,
        retrieval_scope_widening_attempts=1,
    )

    assert frame.orchestration_governance.local_patch_scope_enforced is True
    assert frame.orchestration_governance.deterministic_orchestration_enforced is True
    assert frame.orchestration_governance.hidden_orchestration_execution_blocked is True
    assert frame.orchestration_governance.autonomous_branch_mutation_blocked is True
    assert frame.orchestration_governance.autonomous_governance_mutation_blocked is True
    assert frame.orchestration_governance.self_expanding_orchestration_graphs_blocked is True
    assert frame.orchestration_governance.retrieval_scope_widening_blocked is True
    assert frame.orchestration_termination.governance_violation_detected is True


def test_tc_runtimeorchestrator_10_orchestration_termination_handling() -> None:
    validations = tuple(f"validation_{index}" for index in range(12))
    frame = RuntimeOrchestrator().evaluate(
        validation_queue_items=validations,
        validation_completed_count=0,
        orchestration_budget_used=ORCHESTRATION_BUDGET_LIMIT + 1,
        retry_amplification=RETRY_AMPLIFICATION_THRESHOLD + 1,
        continuation_depth=MAX_CONTINUATION_DEPTH + 2,
    )

    assert frame.orchestration_termination.orchestration_terminated is True
    assert frame.orchestration_termination.orchestration_budget_exceeded is True
    assert frame.orchestration_termination.retry_amplification_threshold_exceeded is True
    assert frame.orchestration_termination.continuation_saturation_threshold_exceeded is True
    assert frame.orchestration_termination.orchestration_queue_saturation_exceeded is True
    assert "ORCHESTRATION_BUDGET_EXCEEDED" in (frame.orchestration_termination.termination_reasons)


def test_tc_runtimeorchestrator_11_bounded_orchestration_history_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    frame = RuntimeOrchestrator().evaluate(orchestration_history_items=history)

    assert len(frame.orchestration_history.orchestration_history) == MAX_ORCHESTRATION_HISTORY
    assert frame.orchestration_history.orchestration_history_overflow_blocked is True
    assert frame.orchestration_eviction.evicted_history_items == (
        history[MAX_ORCHESTRATION_HISTORY:]
    )
    assert frame.orchestration_eviction.bounded_eviction_active is True


def test_tc_runtimeorchestrator_12_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().runtime_orchestrator

    assert report.runtime_orchestrator_active is True
    assert 0 <= report.orchestration_schedule_score <= 100
    assert 0 <= report.validation_schedule_score <= 100
    assert 0 <= report.retry_schedule_score <= 100
    assert 0 <= report.continuation_schedule_score <= 100
    assert report.estimated_avoided_manual_scheduling > 0
    assert report.estimated_avoided_recursive_orchestration > 0
    assert report.estimated_avoided_frontier_next_step_reasoning > 0


def test_tc_runtimeorchestrator_13_runtime_is_deterministic() -> None:
    first = RuntimeOrchestrator().evaluate()
    second = RuntimeOrchestrator().evaluate()

    assert first == second
    assert first.execution_scheduling.execution_scheduling_active is True
    assert first.orchestration_governance.deterministic_orchestration_enforced is True
    assert first.orchestration_confidence.next_step_confidence is True
