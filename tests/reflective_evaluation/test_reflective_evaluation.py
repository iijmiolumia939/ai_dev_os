from __future__ import annotations

from ai_dev_os.reflective_evaluation import (
    MAX_REFLECTIVE_HISTORY,
    MAX_REFLECTIVE_WINDOW_ITEMS,
    REFLECTIVE_EVALUATION_REQUIREMENT_IDS,
    REFLECTIVE_EVALUATION_TEST_IDS,
    ReflectiveEvaluationRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_reflectiveevaluation_01_active_runtime_is_bounded_local_patch() -> None:
    frame = ReflectiveEvaluationRuntime().evaluate()

    assert frame.reflective_evaluation_active is True
    assert frame.requirement_ids == REFLECTIVE_EVALUATION_REQUIREMENT_IDS
    assert frame.test_ids == REFLECTIVE_EVALUATION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.provider_routing == "LOCAL_FIRST_NO_FRONTIER_REFLECTION"


def test_tc_reflectiveevaluation_02_execution_quality_scoring_is_bounded() -> None:
    frame = ReflectiveEvaluationRuntime().evaluate(
        execution_failure_frequency=1,
        retry_amplification_pressure=2,
    )

    assert 0 <= frame.execution_quality_score <= 100
    assert frame.execution_quality.execution_quality_score == frame.execution_quality_score
    assert frame.execution_quality.execution_consistency == "WATCH"
    assert frame.execution_quality.verified_execution_continuity is True
    assert frame.execution_quality.runtime_mediation_stability == "WATCH"


def test_tc_reflectiveevaluation_03_cognitive_coherence_evaluation_is_deterministic() -> None:
    first = ReflectiveEvaluationRuntime().evaluate()
    second = ReflectiveEvaluationRuntime().evaluate()

    assert first.cognitive_coherence_score == second.cognitive_coherence_score
    assert first.cognitive_coherence.cognitive_coherence_active is True
    assert first.cognitive_coherence.execution_focus_consistency is True
    assert first.cognitive_coherence.cognitive_decay_pressure == "STABLE"


def test_tc_reflectiveevaluation_04_continuation_validity_tracking_terminates() -> None:
    frame = ReflectiveEvaluationRuntime().evaluate(
        stale_continuation_chains=2,
        invalid_continuation_depth=2,
        abandoned_recovery_chains=1,
        continuation_interruption_pressure=2,
    )

    assert frame.continuation_validity_score <= 45
    assert frame.continuation_validity.continuation_runtime_active is True
    assert frame.reflective_termination.continuation_invalidation_threshold_exceeded is True
    assert (
        "CONTINUATION_INVALIDATION_THRESHOLD_EXCEEDED"
        in frame.reflective_termination.termination_reasons
    )


def test_tc_reflectiveevaluation_05_planning_integrity_evaluates_planning_runtime() -> None:
    frame = ReflectiveEvaluationRuntime().evaluate(planning_decay_pressure=2)

    assert frame.planning_integrity.planning_integrity_active is True
    assert frame.planning_integrity.bounded_goal_hierarchy_integrity is True
    assert frame.planning_integrity.planning_continuation_consistency == "MEDIUM"
    assert 0 <= frame.planning_integrity_score <= 100


def test_tc_reflectiveevaluation_06_recursive_reflection_and_governance_are_blocked() -> None:
    frame = ReflectiveEvaluationRuntime().evaluate(
        recursive_evaluation_attempts=1,
        autonomous_self_improvement_attempts=1,
        recursive_optimization_attempts=1,
        hidden_reflective_execution_attempts=1,
        self_expanding_evaluation_attempts=1,
        governance_mutation_attempts=1,
        objective_synthesis_attempts=1,
        retrieval_scope_widening_attempts=1,
    )

    assert frame.reflective_governance.autonomous_self_improvement_blocked is True
    assert frame.reflective_governance.recursive_optimization_blocked is True
    assert frame.reflective_governance.hidden_reflective_execution_blocked is True
    assert frame.reflective_governance.self_expanding_evaluation_chains_blocked is True
    assert frame.reflective_governance.governance_policy_mutation_blocked is True
    assert frame.reflective_governance.objective_synthesis_blocked is True
    assert frame.reflective_governance.retrieval_scope_widening_blocked is True
    assert frame.reflective_termination.recursive_evaluation_detected is True
    assert frame.reflective_termination.governance_violation_detected is True


def test_tc_reflectiveevaluation_07_reflective_termination_handles_budget_and_saturation() -> None:
    frame = ReflectiveEvaluationRuntime().evaluate(
        reflective_budget_used=16,
        reflective_window_items=tuple(f"window_{index}" for index in range(10)),
        recursive_evaluation_attempts=1,
    )

    assert frame.reflective_termination.reflective_terminated is True
    assert frame.reflective_termination.budget_exceeded is True
    assert frame.reflective_termination.saturation_threshold_exceeded is True
    assert "REFLECTIVE_BUDGET_EXCEEDED" in frame.reflective_termination.termination_reasons
    assert "REFLECTIVE_SATURATION_EXCEEDED" in frame.reflective_termination.termination_reasons


def test_tc_reflectiveevaluation_08_reflective_windows_and_history_are_bounded() -> None:
    window = tuple(f"window_{index}" for index in range(8))
    history = tuple(f"history_{index}" for index in range(9))
    frame = ReflectiveEvaluationRuntime().evaluate(
        reflective_window_items=window,
        reflective_history_items=history,
        raw_transcript_replay_attempts=1,
    )

    assert len(frame.reflective_window.reflective_window_items) == MAX_REFLECTIVE_WINDOW_ITEMS
    assert len(frame.reflective_history.reflective_history) == MAX_REFLECTIVE_HISTORY
    assert frame.reflective_window.evicted_window_items == window[MAX_REFLECTIVE_WINDOW_ITEMS:]
    assert frame.reflective_eviction.evicted_history_items == history[MAX_REFLECTIVE_HISTORY:]
    assert frame.reflective_history.raw_transcript_replay_blocked is True
    assert frame.reflective_history.recursive_history_expansion_blocked is True


def test_tc_reflectiveevaluation_09_bounded_scoring_enforcement() -> None:
    frame = ReflectiveEvaluationRuntime().evaluate(
        execution_failure_frequency=20,
        retry_amplification_pressure=20,
        stale_continuation_chains=20,
        invalid_continuation_depth=20,
        planning_decay_pressure=20,
        runtime_conflict_pressure=20,
    )

    scores = (
        frame.execution_quality_score,
        frame.cognitive_coherence_score,
        frame.continuation_validity_score,
        frame.planning_integrity_score,
        frame.runtime_integrity.runtime_integrity_score,
        frame.recovery_effectiveness.recovery_effectiveness_score,
        frame.coordination_stability.coordination_stability_score,
    )
    assert all(0 <= score <= 100 for score in scores)
    assert frame.reflective_governance.bounded_scoring_ranges_enforced is True


def test_tc_reflectiveevaluation_10_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().reflective_evaluation

    assert report.reflective_evaluation_active is True
    assert 0 <= report.execution_quality_score <= 100
    assert 0 <= report.cognitive_coherence_score <= 100
    assert 0 <= report.continuation_validity_score <= 100
    assert 0 <= report.planning_integrity_score <= 100
    assert report.estimated_avoided_recursive_reflection > 0
    assert report.estimated_avoided_self_optimization > 0
    assert report.estimated_avoided_frontier_evaluation > 0


def test_tc_reflectiveevaluation_11_runtime_is_deterministic() -> None:
    first = ReflectiveEvaluationRuntime().evaluate()
    second = ReflectiveEvaluationRuntime().evaluate()

    assert first == second
    assert first.reflective_budget.local_first_budget is True
    assert first.reflective_budget.high_tier_evaluation_blocked is True
