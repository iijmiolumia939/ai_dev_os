from __future__ import annotations

from ai_dev_os.intentional_planning import (
    INTENTIONAL_PLANNING_REQUIREMENT_IDS,
    INTENTIONAL_PLANNING_TEST_IDS,
    MAX_ACTIVE_GOALS,
    MAX_CONTINUATION_DEPTH,
    MAX_PLANNING_WINDOW_ITEMS,
    IntentionalPlanningRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_intentionalplanning_01_active_runtime_is_bounded_local_patch() -> None:
    frame = IntentionalPlanningRuntime().evaluate()

    assert frame.intentional_planning_active is True
    assert frame.requirement_ids == INTENTIONAL_PLANNING_REQUIREMENT_IDS
    assert frame.test_ids == INTENTIONAL_PLANNING_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.provider_routing == "LOCAL_FIRST_NO_FRONTIER_INTENTIONALITY"


def test_tc_intentionalplanning_02_goal_hierarchy_is_bounded() -> None:
    goals = tuple(f"goal_{index}" for index in range(9))
    frame = IntentionalPlanningRuntime().evaluate(active_goals=goals)

    assert frame.active_goal_count == MAX_ACTIVE_GOALS
    assert frame.goal_hierarchy.active_goals == goals[:MAX_ACTIVE_GOALS]
    assert frame.goal_hierarchy.bounded_goal_hierarchy is True
    assert frame.planning_eviction.evicted_goals == goals[MAX_ACTIVE_GOALS:]
    assert frame.planning_eviction.bounded_eviction_active is True


def test_tc_intentionalplanning_03_goal_priority_is_deterministic() -> None:
    priorities = {"tests": 30, "runtime": 50, "audit": 20, "vscode": 10}
    first = IntentionalPlanningRuntime().evaluate(goal_priorities=priorities)
    second = IntentionalPlanningRuntime().evaluate(goal_priorities=priorities)

    assert first.goal_priority.priority_order == second.goal_priority.priority_order
    assert first.goal_priority.primary_goal == "runtime"
    assert first.goal_priority.deterministic_goal_prioritization is True


def test_tc_intentionalplanning_04_planning_window_is_bounded() -> None:
    window = tuple(f"window_{index}" for index in range(8))
    frame = IntentionalPlanningRuntime().evaluate(planning_window_items=window)

    assert len(frame.planning_window.planning_window_items) == MAX_PLANNING_WINDOW_ITEMS
    assert frame.planning_window.window_limit == MAX_PLANNING_WINDOW_ITEMS
    assert frame.planning_window.planning_window_pressure == "HIGH"
    assert frame.planning_eviction.evicted_window_items == window[MAX_PLANNING_WINDOW_ITEMS:]


def test_tc_intentionalplanning_05_task_salience_blocks_scope_widening() -> None:
    frame = IntentionalPlanningRuntime().evaluate(
        retrieval_scope_widening_attempts=1,
        dynamic_objective_attempts=1,
    )

    assert frame.task_salience.bounded_context_relevance is True
    assert frame.task_salience.retrieval_scope_widening_blocked is True
    assert frame.task_salience.dynamic_objective_synthesis_blocked is True
    assert frame.planning_governance.retrieval_scope_widening_blocked is True


def test_tc_intentionalplanning_06_continuation_depth_is_bounded() -> None:
    chain = ("one", "two", "three", "four", "five")
    frame = IntentionalPlanningRuntime().evaluate(continuation_chain=chain)

    assert frame.planning_continuation.continuation_depth == MAX_CONTINUATION_DEPTH
    assert frame.planning_continuation.continuation_chain == chain[:MAX_CONTINUATION_DEPTH]
    assert frame.planning_continuation.recursive_continuation_blocked is True
    assert "CONTINUATION_DEPTH_EXCEEDED" in frame.planning_termination.termination_reasons


def test_tc_intentionalplanning_07_interruption_and_decay_are_tracked() -> None:
    frame = IntentionalPlanningRuntime().evaluate(
        interrupted_goals=("blocked_validation",),
        stale_plans=("old_plan", "stale_followup"),
        decayed_goals=("expired_goal",),
        interruption_duration=20,
        abandoned_continuation_chains=1,
    )

    assert frame.planning_interruption.interruption_count == 1
    assert frame.planning_decay.planning_decay_status == "RESET_RECOMMENDED"
    assert frame.planning_recovery.recovery_required is True
    assert frame.planning_decay.bounded_reset_recommendation.startswith("TERMINATE")


def test_tc_intentionalplanning_08_governance_blocks_recursive_and_hidden_planning() -> None:
    frame = IntentionalPlanningRuntime().evaluate(
        recursive_planning_attempts=1,
        autonomous_goal_expansion_attempts=1,
        hidden_background_planning_attempts=1,
        self_expanding_tree_attempts=1,
        governance_mutation_attempts=1,
        repo_wide_reprioritization_attempts=1,
    )

    assert frame.active_goal.recursive_goal_synthesis_blocked is True
    assert frame.planning_governance.recursive_planning_blocked is True
    assert frame.planning_governance.autonomous_goal_expansion_blocked is True
    assert frame.planning_governance.hidden_background_planning_blocked is True
    assert frame.planning_governance.governance_policy_mutation_blocked is True
    assert frame.goal_priority.autonomous_reprioritization_blocked is True


def test_tc_intentionalplanning_09_termination_handles_budget_and_saturation() -> None:
    frame = IntentionalPlanningRuntime().evaluate(
        active_goals=tuple(f"goal_{index}" for index in range(10)),
        planning_window_items=tuple(f"window_{index}" for index in range(10)),
        planning_budget_used=16,
        recursive_planning_attempts=1,
    )

    assert frame.planning_termination.planning_terminated is True
    assert frame.planning_termination.budget_exceeded is True
    assert frame.planning_termination.recursive_planning_detected is True
    assert frame.planning_termination.saturation_threshold_exceeded is True
    assert "PLANNING_BUDGET_EXCEEDED" in frame.planning_termination.termination_reasons


def test_tc_intentionalplanning_10_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().intentional_planning

    assert report.intentional_planning_active is True
    assert report.active_goal_count == MAX_ACTIVE_GOALS
    assert report.planning_window_pressure == "MEDIUM"
    assert report.planning_decay_status == "STABLE"
    assert report.planning_interruption_pressure == "LOW"
    assert report.estimated_avoided_recursive_planning > 0
    assert report.estimated_avoided_goal_explosion > 0
    assert report.estimated_avoided_frontier_reasoning > 0


def test_tc_intentionalplanning_11_runtime_is_deterministic() -> None:
    first = IntentionalPlanningRuntime().evaluate()
    second = IntentionalPlanningRuntime().evaluate()

    assert first == second
    assert first.planning_budget.local_first_budget is True
    assert first.planning_budget.high_tier_reasoning_blocked is True
