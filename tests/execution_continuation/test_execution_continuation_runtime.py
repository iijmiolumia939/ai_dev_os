from __future__ import annotations

from ai_dev_os.execution_continuation import (
    EXECUTION_CONTINUATION_REQUIREMENT_IDS,
    EXECUTION_CONTINUATION_TEST_IDS,
    MAX_CONTINUATION_STEPS,
    ExecutionContinuationInput,
    ExecutionContinuationRuntime,
    PendingStep,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executioncontinuation_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.execution_continuation_active is True
    assert frame.bounded is True
    assert frame.local_only is True
    assert frame.rollback_safe is True
    assert frame.continuation.requirement_ids == EXECUTION_CONTINUATION_REQUIREMENT_IDS
    assert frame.continuation.test_ids == EXECUTION_CONTINUATION_TEST_IDS


def test_tc_executioncontinuation_02_continues_after_successful_tool_execution() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.state.continuation_after_tool_execution is True
    assert frame.tool_execution.continue_after_success is True
    assert frame.continuation.bounded_continuation_recommendation == "CONTINUE_NEXT_PENDING_STEP"


def test_tc_executioncontinuation_03_persists_deterministic_state() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.state.deterministic_state_key == "steps:2:2:tools:2"
    assert frame.state.hidden_background_execution is False
    assert frame.progress.step_by_step_persistence is True


def test_tc_executioncontinuation_04_pending_steps_are_bounded() -> None:
    pending_steps = tuple(
        PendingStep(f"step-{index}", "bounded", "ai_dev_os/execution_continuation", True)
        for index in range(8)
    )
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(pending_steps=pending_steps)
    )

    assert frame.pending_step.bounded_pending_step_count == 4
    assert frame.pending_step.recursively_generated_steps is False


def test_tc_executioncontinuation_05_checkpoint_is_compact_only() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.checkpoint.continuation_checkpoint_active is True
    assert frame.checkpoint.compact_execution_state == (
        "inspect-adjacent-runtime",
        "apply-local-patch",
    )
    assert frame.checkpoint.raw_conversation_persisted is False
    assert frame.checkpoint.recursive_execution_plan_persisted is False


def test_tc_executioncontinuation_06_budget_tracks_step_count() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.budget.max_steps == MAX_CONTINUATION_STEPS
    assert frame.budget.used_steps == 4
    assert frame.budget.remaining_steps == 1
    assert frame.budget.deterministic_termination_hint == "CONTINUATION_WITHIN_BOUNDS"


def test_tc_executioncontinuation_07_budget_exceeded_terminates() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(
            completed_steps=("one", "two", "three", "four"),
            successful_tool_executions=3,
        )
    )

    assert frame.termination.should_terminate is True
    assert frame.termination.budget_exceeded is True
    assert frame.termination.termination_reason == "CONTINUATION_BUDGET_EXCEEDED"


def test_tc_executioncontinuation_08_recursive_loop_is_blocked() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(recursive_continuation_attempts=1)
    )

    assert frame.guard.recursive_loop_blocked is True
    assert frame.termination.recursive_risk_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_CONTINUATION_RISK_DETECTED"


def test_tc_executioncontinuation_09_repo_wide_scope_is_blocked() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(repo_wide_edit_attempts=1)
    )

    assert frame.guard.repo_wide_scope_blocked is True
    assert frame.termination.bounded_scope_exceeded is True
    assert frame.governance.repo_wide_autonomous_edits_blocked is True


def test_tc_executioncontinuation_10_hidden_background_execution_is_blocked() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(hidden_background_attempts=1)
    )

    assert frame.guard.hidden_background_agent_blocked is True
    assert frame.governance.hidden_background_execution_blocked is True
    assert frame.termination.governance_violation_risk_detected is True


def test_tc_executioncontinuation_11_tool_saturation_terminates() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(successful_tool_executions=4, failed_tool_executions=2)
    )

    assert frame.tool_execution.tool_execution_saturation >= 70
    assert frame.guard.uncontrolled_tool_loop_blocked is True
    assert frame.termination.execution_saturation_detected is True


def test_tc_executioncontinuation_12_failed_step_retry_is_recommendation_only() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(failed_tool_executions=1)
    )

    assert frame.tool_execution.retry_recommendation == "RETRY_FAILED_STEP_ONCE_WITH_CHECKPOINT"
    assert frame.recovery.failed_step_retry_recommendation == (
        "RETRY_FAILED_STEP_ONCE_AFTER_COMPACT_CHECKPOINT"
    )
    assert frame.recovery.autonomous_provider_reroute_allowed is False


def test_tc_executioncontinuation_13_governance_enforces_local_patch() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.governance.continuation_governance_active is True
    assert frame.governance.local_patch_scope_enforced is True
    assert frame.governance.bounded_retrieval_enforced is True
    assert frame.governance.compact_continuity_enforced is True
    assert frame.governance.governance_rules_mutated is False


def test_tc_executioncontinuation_14_retrieval_radius_overflow_terminates() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(retrieval_radius=4)
    )

    assert frame.termination.should_terminate is True
    assert frame.termination.bounded_scope_exceeded is True
    assert frame.guard.governance_violation_risk_detected is True


def test_tc_executioncontinuation_15_decay_tracks_loop_and_retrieval_pressure() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(repeated_continuation_loops=2, retrieval_radius=3)
    )

    assert frame.decay.continuation_decay_active is True
    assert frame.decay.loop_decay_score == 20
    assert frame.decay.retrieval_decay_score == 12
    assert frame.decay.continuation_decay_guard_active is True


def test_tc_executioncontinuation_16_completion_requires_validation() -> None:
    frame = ExecutionContinuationRuntime().evaluate(
        ExecutionContinuationInput(pending_steps=())
    )

    assert frame.completion.continuation_completion_active is True
    assert frame.completion.bounded_completion_ready is True
    assert frame.completion.validation_required_before_completion is True


def test_tc_executioncontinuation_17_recovery_supports_safe_resume_only() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.recovery.safe_resume_supported is True
    assert frame.recovery.rollback_safe_recovery is True
    assert frame.recovery.compact_continuation_reset is True
    assert frame.recovery.recursive_graph_regeneration_allowed is False


def test_tc_executioncontinuation_18_confidence_is_deterministic() -> None:
    first = ExecutionContinuationRuntime().evaluate()
    second = ExecutionContinuationRuntime().evaluate()

    assert first == second
    assert first.confidence.confidence_score == 60
    assert first.confidence.confidence_label == "CONTINUATION_GUARDED"


def test_tc_executioncontinuation_19_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().execution_continuation

    assert report.execution_continuation_active is True
    assert report.continuation_budget_active is True
    assert report.continuation_governance_active is True
    assert report.continuation_checkpoint_active is True
    assert report.continuation_termination_active is True
    assert report.estimated_avoided_execution_stalls == 24
    assert report.estimated_avoided_recursive_loops == 17
    assert report.estimated_avoided_agent_explosions == 13


def test_tc_executioncontinuation_20_runtime_is_summary_only_and_governance_preserving() -> None:
    frame = ExecutionContinuationRuntime().evaluate()

    assert frame.summary_only is True
    assert frame.deterministic is True
    assert frame.governance.recursive_execution_loops_blocked is True
    assert frame.governance.uncontrolled_continuation_chains_blocked is True
    assert frame.governance.governance_rules_mutated is False