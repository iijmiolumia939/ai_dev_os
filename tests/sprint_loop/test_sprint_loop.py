from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.sprint_loop import (
    MAX_CONTINUATION_DEPTH,
    MAX_SPRINT_HISTORY,
    MAX_SPRINT_TASK_WINDOW,
    MAX_VALIDATION_QUEUE,
    REGRESSION_SATURATION_THRESHOLD,
    RETRY_AMPLIFICATION_THRESHOLD,
    SPRINT_BUDGET_LIMIT,
    SPRINT_LOOP_REQUIREMENT_IDS,
    SPRINT_LOOP_TEST_IDS,
    SprintLoopRuntime,
)


def test_tc_sprintloop_01_active_runtime_is_bounded_local_patch() -> None:
    frame = SprintLoopRuntime().evaluate()

    assert frame.sprint_loop_active is True
    assert frame.requirement_ids == SPRINT_LOOP_REQUIREMENT_IDS
    assert frame.test_ids == SPRINT_LOOP_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.sprint_loop_mode == "LOCAL_PATCH_BOUNDED_SPRINT_LOOP"


def test_tc_sprintloop_02_sprint_planning_tracks_bounded_windows() -> None:
    tasks = tuple(f"task_{index}" for index in range(8))
    validations = tuple(f"validation_{index}" for index in range(8))
    frame = SprintLoopRuntime().evaluate(
        task_window_items=tasks,
        validation_queue_items=validations,
    )

    assert frame.sprint_planning.sprint_planning_active is True
    assert len(frame.sprint_planning.bounded_task_window) == MAX_SPRINT_TASK_WINDOW
    assert len(frame.sprint_planning.bounded_validation_queue) == MAX_VALIDATION_QUEUE
    assert frame.sprint_scope.local_patch_scope_enforced is True
    assert frame.sprint_eviction.evicted_task_window_items == tasks[MAX_SPRINT_TASK_WINDOW:]
    assert frame.sprint_eviction.evicted_validation_items == validations[MAX_VALIDATION_QUEUE:]


def test_tc_sprintloop_03_validation_sequencing_and_reset() -> None:
    frame = SprintLoopRuntime().evaluate(
        validation_completed_count=1,
        validation_interruption_pressure=3,
        validation_regression_pressure=4,
    )

    assert frame.sprint_validation.sprint_validation_active is True
    assert frame.sprint_validation.validation_saturation >= 70
    assert frame.sprint_validation.bounded_validation_reset_recommendation == (
        "RESET_VALIDATION_QUEUE_AFTER_COOLDOWN"
    )
    assert frame.sprint_validation_score < 80


def test_tc_sprintloop_04_regression_stabilization() -> None:
    frame = SprintLoopRuntime().evaluate(
        repeated_regressions=3,
        retry_amplification=2,
        regression_cooldown_pressure=2,
        bounded_failure_recurrence=2,
        bounded_dependency_instability=1,
    )

    assert frame.sprint_regression.sprint_regression_active is True
    assert frame.sprint_regression_score < 45
    assert frame.sprint_regression.bounded_stabilization_recommendation == (
        "STABILIZE_REGRESSION_BEFORE_COMMIT"
    )


def test_tc_sprintloop_05_retry_governance() -> None:
    frame = SprintLoopRuntime().evaluate(
        retry_count=4,
        retry_amplification=RETRY_AMPLIFICATION_THRESHOLD + 1,
    )

    assert frame.sprint_retry.sprint_retry_active is True
    assert frame.sprint_retry.bounded_retry_governance is False
    assert frame.sprint_retry.retry_amplification_blocked is True
    assert frame.sprint_retry.hidden_retry_execution_blocked is True
    assert frame.sprint_termination.retry_amplification_threshold_exceeded is True


def test_tc_sprintloop_06_continuation_governance() -> None:
    frame = SprintLoopRuntime().evaluate(
        continuation_depth=MAX_CONTINUATION_DEPTH + 1,
        continuation_interruption_window=1,
    )

    assert frame.sprint_continuation.sprint_continuation_active is True
    assert frame.sprint_continuation.bounded_continuation_depth is False
    assert frame.sprint_continuation.continuation_cooldown_required is True
    assert frame.sprint_continuation.bounded_continuation_reset_recommendation == (
        "RESET_SPRINT_CONTINUATION_WINDOW"
    )
    assert frame.sprint_termination.continuation_depth_exceeded is True


def test_tc_sprintloop_07_commit_readiness_evaluation() -> None:
    frame = SprintLoopRuntime().evaluate()

    assert frame.sprint_commit_readiness.sprint_commit_readiness_active is True
    assert frame.sprint_commit_readiness.validation_completion is True
    assert frame.sprint_commit_readiness.regression_stabilized is True
    assert frame.sprint_commit_readiness.runtime_coherence is True
    assert frame.sprint_commit_readiness.bounded_policy_compliance is True
    assert frame.sprint_commit_readiness.bounded_audit_integrity is True
    assert frame.sprint_commit_readiness_score >= 80
    assert frame.sprint_commit_readiness.autonomous_commit_blocked is True
    assert frame.sprint_commit_readiness.autonomous_push_blocked is True
    assert frame.sprint_commit_readiness.autonomous_merge_blocked is True


def test_tc_sprintloop_08_recursive_sprint_blocking() -> None:
    frame = SprintLoopRuntime().evaluate(recursive_sprint_attempts=1)

    assert frame.sprint_governance.recursive_sprint_generation_blocked is True
    assert frame.sprint_termination.recursive_sprint_detected is True
    assert "RECURSIVE_SPRINT_DETECTED" in frame.sprint_termination.termination_reasons


def test_tc_sprintloop_09_sprint_governance_enforcement() -> None:
    frame = SprintLoopRuntime().evaluate(
        sprint_scope_expansion_attempts=1,
        hidden_sprint_execution_attempts=1,
        autonomous_branch_mutation_attempts=1,
        autonomous_governance_mutation_attempts=1,
        self_expanding_sprint_loop_attempts=1,
        retrieval_scope_widening_attempts=1,
    )

    assert frame.sprint_governance.local_patch_scope_enforced is True
    assert frame.sprint_governance.hidden_sprint_execution_blocked is True
    assert frame.sprint_governance.autonomous_branch_mutation_blocked is True
    assert frame.sprint_governance.autonomous_governance_mutation_blocked is True
    assert frame.sprint_governance.self_expanding_sprint_loops_blocked is True
    assert frame.sprint_governance.retrieval_scope_widening_blocked is True
    assert frame.sprint_termination.governance_violation_detected is True


def test_tc_sprintloop_10_sprint_termination_handling() -> None:
    frame = SprintLoopRuntime().evaluate(
        sprint_budget_used=SPRINT_BUDGET_LIMIT + 1,
        repeated_regressions=4,
        retry_amplification=RETRY_AMPLIFICATION_THRESHOLD + 1,
        continuation_depth=MAX_CONTINUATION_DEPTH + 1,
    )

    assert frame.sprint_termination.sprint_loop_terminated is True
    assert frame.sprint_termination.sprint_budget_exceeded is True
    assert frame.sprint_termination.regression_saturation_threshold_exceeded is True
    assert frame.sprint_termination.retry_amplification_threshold_exceeded is True
    assert frame.sprint_termination.continuation_depth_exceeded is True
    assert "SPRINT_BUDGET_EXCEEDED" in frame.sprint_termination.termination_reasons
    assert "REGRESSION_SATURATION_THRESHOLD_EXCEEDED" in (
        frame.sprint_termination.termination_reasons
    )


def test_tc_sprintloop_11_bounded_sprint_history_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    frame = SprintLoopRuntime().evaluate(sprint_history_items=history)

    assert len(frame.sprint_history.sprint_history) == MAX_SPRINT_HISTORY
    assert frame.sprint_history.sprint_history_overflow_blocked is True
    assert frame.sprint_eviction.evicted_history_items == history[MAX_SPRINT_HISTORY:]
    assert frame.sprint_eviction.bounded_eviction_active is True


def test_tc_sprintloop_12_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().sprint_loop

    assert report.sprint_loop_active is True
    assert 0 <= report.sprint_validation_score <= 100
    assert 0 <= report.sprint_regression_score <= 100
    assert 0 <= report.sprint_commit_readiness_score <= 100
    assert 0 <= report.sprint_continuation_score <= 100
    assert report.estimated_avoided_manual_orchestration > 0
    assert report.estimated_avoided_recursive_sprints > 0
    assert report.estimated_avoided_frontier_supervision > 0


def test_tc_sprintloop_13_runtime_is_deterministic() -> None:
    first = SprintLoopRuntime().evaluate()
    second = SprintLoopRuntime().evaluate()

    assert first == second
    assert first.sprint_execution.deterministic_sprint_execution is True
    assert first.sprint_governance.deterministic_sprint_execution_enforced is True
    assert first.sprint_regression.sprint_regression_score >= REGRESSION_SATURATION_THRESHOLD
