from __future__ import annotations

from ai_dev_os.execution_coordination import (
    EXECUTION_COORDINATION_REQUIREMENT_IDS,
    EXECUTION_COORDINATION_TEST_IDS,
    MAX_COORDINATION_OSCILLATION,
    MAX_COORDINATION_STEPS,
    RUNTIME_PRIORITY_ORDER,
    ExecutionCoordinationRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executioncoordination_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionCoordinationRuntime().evaluate()

    assert frame.execution_coordination_active is True
    assert frame.requirement_ids == EXECUTION_COORDINATION_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_COORDINATION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_executioncoordination_02_default_coordination_is_stable() -> None:
    frame = ExecutionCoordinationRuntime().evaluate()

    assert frame.termination.should_terminate_coordination is False
    assert frame.confidence.confidence_label == "COORDINATION_STABLE"
    assert frame.bounded_coordination_recommendation == (
        "COORDINATE_BOUNDED_RUNTIME_RECOMMENDATIONS"
    )


def test_tc_executioncoordination_03_priority_order_is_deterministic() -> None:
    frame = ExecutionCoordinationRuntime().evaluate()

    assert frame.priority.deterministic_priority_order == RUNTIME_PRIORITY_ORDER
    assert frame.priority.highest_priority_runtime == "governance"
    assert frame.priority.runtime_hierarchy_mutated is False


def test_tc_executioncoordination_04_priority_blocks_dominance_loops() -> None:
    frame = ExecutionCoordinationRuntime().evaluate()

    assert frame.priority.bounded_runtime_conflict_arbitration is True
    assert frame.priority.adaptive_dominance_loops_created is False
    assert frame.priority.governance_safe_coordination_precedence is True


def test_tc_executioncoordination_05_continuation_saturation_conflict_detected() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        continuation_recommendation="CONTINUE_NEXT_PENDING_STEP",
        saturation_recommendation="TERMINATE_CONTINUATION_BEFORE_RETRY_EXPANSION",
    )

    assert frame.conflict.continuation_vs_saturation_conflict is True
    assert frame.conflict.conflict_count == 1
    assert frame.resolution.selected_runtime_precedence == "saturation"


def test_tc_executioncoordination_06_recovery_fatigue_conflict_detected() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        recovery_recommendation="RESUME_SAFE_RECOVERY_FROM_COMPACT_CHECKPOINT",
        fatigue_recommendation="RECOVERY_REQUIRED",
    )

    assert frame.conflict.recovery_vs_fatigue_conflict is True
    assert frame.integrity.incompatible_recovery_continuation_detected is True


def test_tc_executioncoordination_07_load_balancing_cooldown_conflict_detected() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        load_balancing_recommendation="INCREASE_PARALLEL_RUNTIME_BALANCE",
        runtime_coordination_saturation=3,
    )

    assert frame.conflict.load_balancing_vs_cooldown_conflict is True
    assert frame.conflict.compact_coordination_warning == "COORDINATION_CONFLICTS_BOUNDED"


def test_tc_executioncoordination_08_checkpoint_continuation_conflict_detected() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(checkpoint_integrity_valid=False)

    assert frame.conflict.checkpoint_integrity_vs_continuation_conflict is True
    assert frame.integrity.conflicting_recommendations_detected is True


def test_tc_executioncoordination_09_compact_arbitration_summary() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        checkpoint_integrity_valid=False,
    )

    assert frame.compact_conflict_resolution_summary == (
        "conflicts=1;precedence=saturation;terminate=false"
    )
    assert frame.conflict.deterministic_arbitration_recommendation == (
        "PRIORITIZE_SATURATION_RECOVERY_BEFORE_CONTINUATION"
    )


def test_tc_executioncoordination_10_budget_tracks_coordination_steps() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(coordination_steps=MAX_COORDINATION_STEPS)

    assert frame.budget.used_coordination_steps == MAX_COORDINATION_STEPS
    assert frame.budget.remaining_coordination_steps == 0
    assert frame.budget.coordination_budget_exceeded is False


def test_tc_executioncoordination_11_budget_exceeded_terminates() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(coordination_steps=MAX_COORDINATION_STEPS + 1)

    assert frame.termination.should_terminate_coordination is True
    assert frame.termination.coordination_budget_exceeded is True
    assert frame.termination.termination_reason == "COORDINATION_BUDGET_EXCEEDED"


def test_tc_executioncoordination_12_recursive_coordination_blocking() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(recursive_coordination_attempts=1)

    assert frame.governance.recursive_runtime_coordination_blocked is True
    assert frame.termination.recursive_coordination_risk_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_COORDINATION_RISK_DETECTED"


def test_tc_executioncoordination_13_hidden_orchestration_blocked() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(hidden_orchestration_layers=1)

    assert frame.governance.hidden_orchestration_layers_blocked is True
    assert frame.termination.governance_violation_risk_detected is True
    assert frame.resolution.orchestration_loop_created is False


def test_tc_executioncoordination_14_autonomous_arbitration_blocked() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(autonomous_arbitration_attempts=1)

    assert frame.governance.autonomous_runtime_arbitration_blocked is True
    assert frame.termination.termination_reason == (
        "COORDINATION_GOVERNANCE_VIOLATION_RISK_DETECTED"
    )
    assert frame.resolution.autonomous_coordination_action_allowed is False


def test_tc_executioncoordination_15_repo_wide_coordination_expansion_blocked() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(repo_wide_coordination_expansions=1)

    assert frame.governance.repo_wide_coordination_expansion_blocked is True
    assert frame.governance.governance_policy_mutated is False
    assert frame.resolution.runtime_hierarchy_self_expanded is False


def test_tc_executioncoordination_16_retrieval_scope_not_widened() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(retrieval_radius=3)

    assert frame.governance.bounded_retrieval_enforced is False
    assert frame.governance.retrieval_scope_widened is False
    assert frame.termination.governance_violation_risk_detected is True


def test_tc_executioncoordination_17_coordination_cooldown_enforcement() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        runtime_coordination_saturation=2,
        repeated_coordination_oscillation=2,
        conflicting_runtime_retry_pressure=2,
    )

    assert frame.cooldown.cooldown_required is True
    assert frame.cooldown.coordination_cooldown_recommendation == "APPLY_COORDINATION_COOLDOWN"
    assert frame.cooldown.autonomous_runtime_suppression_allowed is False


def test_tc_executioncoordination_18_runtime_oscillation_detection() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        repeated_coordination_oscillation=MAX_COORDINATION_OSCILLATION + 1
    )

    assert frame.termination.runtime_oscillation_threshold_exceeded is True
    assert frame.termination.termination_reason == "RUNTIME_OSCILLATION_THRESHOLD_EXCEEDED"
    assert frame.cooldown.recursive_rebalance_allowed is False


def test_tc_executioncoordination_19_coordination_amplification_detection() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(coordination_amplification_risk=1)

    assert frame.termination.coordination_amplification_detected is True
    assert frame.termination.termination_reason == "COORDINATION_AMPLIFICATION_DETECTED"


def test_tc_executioncoordination_20_runtime_graph_synthesis_blocked() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(runtime_graph_synthesis_attempts=1)

    assert frame.integrity.runtime_graph_synthesis_detected is True
    assert frame.resolution.runtime_graph_regeneration_allowed is False
    assert frame.integrity.integrity_recommendation == "STOP_COORDINATION_GRAPH_SYNTHESIS"


def test_tc_executioncoordination_21_history_is_bounded() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        history_entries=tuple(f"coordination-{index}" for index in range(10))
    )

    assert frame.history.history_entry_count == 6
    assert frame.history.history_truncated is True
    assert frame.history.recursive_history_expansion_blocked is True


def test_tc_executioncoordination_22_eviction_is_recommendation_only() -> None:
    frame = ExecutionCoordinationRuntime().evaluate(
        history_entries=tuple(f"coordination-{index}" for index in range(10))
    )

    assert frame.eviction.stale_coordination_history_eviction_recommended is True
    assert frame.eviction.eviction_recommendation == (
        "RECOMMEND_STALE_COORDINATION_METADATA_EVICTION"
    )
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_executioncoordination_23_runtime_audit_exposes_required_fields_only() -> None:
    report = run_runtime_enforcement_audit().execution_coordination

    assert report.execution_coordination_active is True
    assert report.coordination_conflict_active is True
    assert report.coordination_priority_active is True
    assert report.coordination_termination_active is True
    assert report.estimated_avoided_runtime_conflicts == 29
    assert report.estimated_avoided_recursive_coordination == 17
    assert report.estimated_avoided_runtime_oscillation == 15


def test_tc_executioncoordination_24_runtime_is_deterministic_and_summary_only() -> None:
    first = ExecutionCoordinationRuntime().evaluate()
    second = ExecutionCoordinationRuntime().evaluate()

    assert first == second
    assert first.summary_only is True
    assert first.governance.deterministic_conflict_resolution_enforced is True
    assert first.estimated_avoided_runtime_oscillation == 15
