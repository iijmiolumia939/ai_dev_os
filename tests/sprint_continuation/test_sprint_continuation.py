from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.sprint_continuation import (
    CONTINUATION_BUDGET_LIMIT,
    DEPENDENCY_PRESSURE_THRESHOLD,
    MAX_BACKLOG_ITEMS,
    MAX_CONTINUATION_HISTORY,
    MAX_DEPENDENCY_ITEMS,
    MAX_NEXT_SPRINT_OPTIONS,
    MAX_OPERATIONAL_CARRYOVER_ITEMS,
    MAX_REGRESSION_ITEMS,
    REGRESSION_CONTINUATION_THRESHOLD,
    SPRINT_CONTINUATION_REQUIREMENT_IDS,
    SPRINT_CONTINUATION_TEST_IDS,
    SprintContinuationRuntime,
)


def test_tc_sprintcontinuation_01_bounded_next_sprint_selection() -> None:
    candidates = tuple(f"sprint_{index}" for index in range(8))
    frame = SprintContinuationRuntime().evaluate(candidate_sprints=candidates)

    assert frame.sprint_continuation_active is True
    assert frame.requirement_ids == SPRINT_CONTINUATION_REQUIREMENT_IDS
    assert frame.test_ids == SPRINT_CONTINUATION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.sprint_continuation_mode == "LOCAL_PATCH_BOUNDED_SPRINT_CONTINUATION"
    assert len(frame.selection.candidate_sprints) == MAX_NEXT_SPRINT_OPTIONS
    assert frame.selection.selected_sprint == "sprint_0"
    assert frame.selection.selection_overflow_blocked is True
    assert frame.eviction.evicted_candidate_sprints == candidates[MAX_NEXT_SPRINT_OPTIONS:]


def test_tc_sprintcontinuation_02_backlog_continuation_is_bounded() -> None:
    backlog = tuple(f"backlog_{index}" for index in range(9))
    frame = SprintContinuationRuntime().evaluate(backlog_items=backlog)

    assert frame.backlog.backlog_priority_active is True
    assert len(frame.backlog.backlog_items) == MAX_BACKLOG_ITEMS
    assert frame.backlog.backlog_overflow_blocked is True
    assert frame.backlog.bounded_backlog_recommendation == "CARRY_BOUNDED_BACKLOG_ONLY"
    assert frame.eviction.evicted_backlog_items == backlog[MAX_BACKLOG_ITEMS:]


def test_tc_sprintcontinuation_03_dependency_continuation_is_visible_and_bounded() -> None:
    dependencies = tuple(f"dependency_{index}" for index in range(7))
    frame = SprintContinuationRuntime().evaluate(
        dependency_items=dependencies,
        dependency_pressure=DEPENDENCY_PRESSURE_THRESHOLD,
    )

    assert frame.dependency.dependency_continuation_active is True
    assert len(frame.dependency.dependency_items) == MAX_DEPENDENCY_ITEMS
    assert frame.dependency.dependency_overflow_blocked is True
    assert frame.dependency.bounded_dependency_recommendation == (
        "STABILIZE_DEPENDENCIES_BEFORE_CONTINUATION"
    )
    assert frame.termination.dependency_pressure_threshold_exceeded is True
    assert "DEPENDENCY_PRESSURE_THRESHOLD_EXCEEDED" in frame.termination.termination_reasons
    assert frame.eviction.evicted_dependency_items == dependencies[MAX_DEPENDENCY_ITEMS:]


def test_tc_sprintcontinuation_04_regression_continuation_is_visible_and_bounded() -> None:
    regressions = tuple(f"regression_{index}" for index in range(7))
    frame = SprintContinuationRuntime().evaluate(
        regression_items=regressions,
        regression_pressure=REGRESSION_CONTINUATION_THRESHOLD,
    )

    assert frame.regression.regression_continuation_active is True
    assert len(frame.regression.regression_items) == MAX_REGRESSION_ITEMS
    assert frame.regression.regression_overflow_blocked is True
    assert frame.regression.bounded_regression_recommendation == (
        "STABILIZE_REGRESSION_BEFORE_NEXT_SPRINT"
    )
    assert frame.termination.regression_continuation_threshold_exceeded is True
    assert "REGRESSION_CONTINUATION_THRESHOLD_EXCEEDED" in frame.termination.termination_reasons
    assert frame.eviction.evicted_regression_items == regressions[MAX_REGRESSION_ITEMS:]


def test_tc_sprintcontinuation_05_recursive_continuation_is_blocked() -> None:
    frame = SprintContinuationRuntime().evaluate(recursive_continuation_attempts=1)

    assert frame.governance.recursive_continuation_blocked is True
    assert frame.termination.recursive_continuation_detected is True
    assert frame.termination.continuation_terminated is True
    assert "RECURSIVE_CONTINUATION_DETECTED" in frame.termination.termination_reasons


def test_tc_sprintcontinuation_06_continuation_governance_is_enforced() -> None:
    frame = SprintContinuationRuntime().evaluate(
        hidden_continuation_execution_attempts=1,
        autonomous_branch_mutation_attempts=1,
        autonomous_governance_mutation_attempts=1,
        self_expanding_sprint_chain_attempts=1,
        frontier_planning_attempts=1,
    )

    assert frame.governance.local_patch_scope_enforced is True
    assert frame.governance.deterministic_selection_enforced is True
    assert frame.governance.hidden_continuation_execution_blocked is True
    assert frame.governance.autonomous_branch_mutation_blocked is True
    assert frame.governance.autonomous_governance_mutation_blocked is True
    assert frame.governance.self_expanding_sprint_chain_blocked is True
    assert frame.governance.frontier_planning_blocked is True
    assert frame.termination.governance_violation_detected is True


def test_tc_sprintcontinuation_07_continuation_termination_handles_budget_and_depth() -> None:
    frame = SprintContinuationRuntime().evaluate(
        continuation_budget_used=CONTINUATION_BUDGET_LIMIT + 1,
        continuation_depth=3,
    )

    assert frame.budget.continuation_budget_exceeded is True
    assert frame.budget.budget_pressure == "OVER_BUDGET"
    assert frame.termination.continuation_terminated is True
    assert frame.termination.continuation_budget_exceeded is True
    assert frame.termination.continuation_depth_exceeded is True
    assert "CONTINUATION_BUDGET_EXCEEDED" in frame.termination.termination_reasons
    assert "CONTINUATION_DEPTH_EXCEEDED" in frame.termination.termination_reasons


def test_tc_sprintcontinuation_08_bounded_continuation_retention_and_operational_carryover() -> (
    None
):
    history = tuple(f"history_{index}" for index in range(9))
    operational = tuple(f"operational_{index}" for index in range(7))
    frame = SprintContinuationRuntime().evaluate(
        continuation_history_items=history,
        operational_carryover_items=operational,
        self_expanding_history_attempts=1,
    )

    assert len(frame.history.continuation_history) == MAX_CONTINUATION_HISTORY
    assert frame.history.continuation_history_overflow_blocked is True
    assert frame.history.self_expanding_history_blocked is True
    assert len(frame.operational.operational_items) == MAX_OPERATIONAL_CARRYOVER_ITEMS
    assert frame.operational.operational_overflow_blocked is True
    assert frame.eviction.evicted_history_items == history[MAX_CONTINUATION_HISTORY:]
    assert (
        frame.eviction.evicted_operational_items == operational[MAX_OPERATIONAL_CARRYOVER_ITEMS:]
    )


def test_tc_sprintcontinuation_09_runtime_audit_exposes_only_required_projection_fields() -> None:
    report = run_runtime_enforcement_audit().sprint_continuation

    assert tuple(report.__dict__) == (
        "sprint_continuation_active",
        "continuation_selection_score",
        "backlog_continuation_score",
        "dependency_continuation_score",
        "regression_continuation_score",
        "operational_carryover_score",
        "estimated_avoided_continuation_drift",
        "estimated_avoided_recursive_sprinting",
        "estimated_avoided_frontier_planning",
    )
    assert report.sprint_continuation_active is True
    assert 0 <= report.continuation_selection_score <= 100
    assert 0 <= report.backlog_continuation_score <= 100
    assert 0 <= report.dependency_continuation_score <= 100
    assert 0 <= report.regression_continuation_score <= 100
    assert 0 <= report.operational_carryover_score <= 100
    assert report.estimated_avoided_continuation_drift > 0
    assert report.estimated_avoided_recursive_sprinting > 0
    assert report.estimated_avoided_frontier_planning > 0


def test_tc_sprintcontinuation_10_runtime_is_deterministic() -> None:
    first = SprintContinuationRuntime().evaluate()
    second = SprintContinuationRuntime().evaluate()

    assert first == second
    assert first.confidence.deterministic_confidence is True
    assert first.confidence.next_sprint_confidence is True
