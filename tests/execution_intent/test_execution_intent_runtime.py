from __future__ import annotations

from ai_dev_os.execution_intent import (
    EXECUTION_INTENT_REQUIREMENT_IDS,
    EXECUTION_INTENT_TEST_IDS,
    INTENT_PRIORITY_ORDER,
    MAX_INTENT_OSCILLATION,
    MAX_INTENT_TRANSITIONS,
    ExecutionIntentRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executionintent_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionIntentRuntime().evaluate()

    assert frame.execution_intent_active is True
    assert frame.requirement_ids == EXECUTION_INTENT_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_INTENT_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_executionintent_02_default_intent_is_stable() -> None:
    frame = ExecutionIntentRuntime().evaluate()

    assert frame.termination.should_terminate_intent_transitions is False
    assert frame.confidence.confidence_label == "INTENT_STABLE"
    assert frame.bounded_intent_transition_recommendation == "ALLOW_BOUNDED_INTENT_TRANSITION"


def test_tc_executionintent_03_priority_order_is_deterministic() -> None:
    frame = ExecutionIntentRuntime().evaluate()

    assert frame.priority.deterministic_intent_order == INTENT_PRIORITY_ORDER
    assert frame.priority.active_priority_intent == "governance"
    assert frame.priority.intent_hierarchy_mutated is False


def test_tc_executionintent_04_priority_blocks_goal_systems() -> None:
    frame = ExecutionIntentRuntime().evaluate()

    assert frame.priority.bounded_intent_precedence is True
    assert frame.priority.adaptive_goal_system_created is False
    assert frame.priority.governance_safe_intent_arbitration is True


def test_tc_executionintent_05_continuation_cooldown_conflict_detected() -> None:
    frame = ExecutionIntentRuntime().evaluate(cooldown_intent="cooldown_required")

    assert frame.conflict.continuation_vs_cooldown_conflict is True
    assert frame.conflict.conflict_count >= 1
    assert frame.compact_intent_arbitration_hint == (
        "PRIORITIZE_SATURATION_RECOVERY_COOLDOWN_BEFORE_CONTINUATION"
    )


def test_tc_executionintent_06_recovery_continuation_conflict_detected() -> None:
    frame = ExecutionIntentRuntime().evaluate(active_execution_intent="recovery")

    assert frame.conflict.recovery_vs_continuation_conflict is True
    assert frame.recovery.recovery_intent_supported is True


def test_tc_executionintent_07_saturation_continuation_conflict_detected() -> None:
    frame = ExecutionIntentRuntime().evaluate(saturation_intent="terminate_when_saturated")

    assert frame.conflict.saturation_vs_continuation_conflict is True
    assert frame.conflict.deterministic_intent_resolution_recommendation == (
        "STABILIZE_INTENT_BEFORE_CONTINUATION"
    )


def test_tc_executionintent_08_coordination_recovery_conflict_detected() -> None:
    frame = ExecutionIntentRuntime().evaluate(active_execution_intent="coordination")

    assert frame.conflict.coordination_vs_recovery_conflict is True
    assert frame.conflict.compact_intent_conflict_summary.startswith("intent-conflicts=2")


def test_tc_executionintent_09_compact_intent_summary() -> None:
    frame = ExecutionIntentRuntime().evaluate(active_execution_intent="continuation")

    assert frame.deterministic_intent_summary == (
        "active=continuation;conflicts=1;terminate=false"
    )
    assert (
        frame.persistence.compact_intent_persistence_summary == frame.deterministic_intent_summary
    )


def test_tc_executionintent_10_transition_budget_tracks_bounds() -> None:
    frame = ExecutionIntentRuntime().evaluate(bounded_intent_transitions=MAX_INTENT_TRANSITIONS)

    assert frame.transition.bounded_intent_transitions == MAX_INTENT_TRANSITIONS
    assert frame.termination.intent_budget_exceeded is False


def test_tc_executionintent_11_transition_budget_exceeded_terminates() -> None:
    frame = ExecutionIntentRuntime().evaluate(
        bounded_intent_transitions=MAX_INTENT_TRANSITIONS + 1
    )

    assert frame.termination.should_terminate_intent_transitions is True
    assert frame.termination.intent_budget_exceeded is True
    assert frame.termination.termination_reason == "INTENT_BUDGET_EXCEEDED"


def test_tc_executionintent_12_recursive_intent_blocking() -> None:
    frame = ExecutionIntentRuntime().evaluate(recursive_intent_attempts=1)

    assert frame.governance.recursive_intent_generation_blocked is True
    assert frame.termination.recursive_intent_oscillation_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_INTENT_OSCILLATION_DETECTED"


def test_tc_executionintent_13_autonomous_planning_blocked() -> None:
    frame = ExecutionIntentRuntime().evaluate(autonomous_planning_attempts=1)

    assert frame.governance.autonomous_planning_systems_blocked is True
    assert frame.termination.governance_violation_risk_detected is True
    assert frame.transition.autonomous_intent_switch_allowed is False


def test_tc_executionintent_14_self_generated_goals_blocked() -> None:
    frame = ExecutionIntentRuntime().evaluate(self_generated_goal_attempts=1)

    assert frame.governance.self_generated_execution_goals_blocked is True
    assert frame.integrity.autonomous_goal_generation_detected is True
    assert frame.persistence.raw_objective_persistence_allowed is False


def test_tc_executionintent_15_repo_wide_intent_expansion_blocked() -> None:
    frame = ExecutionIntentRuntime().evaluate(repo_wide_intent_expansions=1)

    assert frame.governance.repo_wide_intent_expansion_blocked is True
    assert frame.integrity.self_expanding_objectives_detected is True
    assert frame.persistence.execution_scope_mutated is False


def test_tc_executionintent_16_retrieval_scope_not_widened() -> None:
    frame = ExecutionIntentRuntime().evaluate(retrieval_radius=3)

    assert frame.governance.bounded_retrieval_enforced is False
    assert frame.governance.retrieval_scope_widened is False
    assert frame.termination.governance_violation_risk_detected is True


def test_tc_executionintent_17_transition_cooldown_enforcement() -> None:
    frame = ExecutionIntentRuntime().evaluate(
        repeated_intent_oscillation=2,
        unstable_intent_switching=2,
        intent_amplification_pressure=1,
    )

    assert frame.transition.transition_cooldown_required is True
    assert frame.transition.transition_cooldown_recommendation == (
        "APPLY_INTENT_TRANSITION_COOLDOWN"
    )
    assert frame.cooldown.autonomous_cooldown_enforcement_allowed is False


def test_tc_executionintent_18_unstable_intent_oscillation_detection() -> None:
    frame = ExecutionIntentRuntime().evaluate(
        repeated_intent_oscillation=MAX_INTENT_OSCILLATION + 1
    )

    assert frame.termination.recursive_intent_oscillation_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_INTENT_OSCILLATION_DETECTED"
    assert frame.transition.recursive_intent_chain_regeneration_allowed is False


def test_tc_executionintent_19_transition_amplification_detection() -> None:
    frame = ExecutionIntentRuntime().evaluate(intent_amplification_pressure=1)

    assert frame.termination.unstable_transition_amplification_detected is True
    assert frame.termination.termination_reason == "UNSTABLE_TRANSITION_AMPLIFICATION_DETECTED"


def test_tc_executionintent_20_recursive_planning_integrity_blocks_repair() -> None:
    frame = ExecutionIntentRuntime().evaluate(autonomous_planning_attempts=1)

    assert frame.integrity.recursive_planning_detected is True
    assert frame.integrity.integrity_recommendation == "STOP_INTENT_EXPANSION_AND_REQUEST_REVIEW"
    assert frame.integrity.automatic_integrity_repair_allowed is False


def test_tc_executionintent_21_history_is_bounded() -> None:
    frame = ExecutionIntentRuntime().evaluate(
        history_entries=tuple(f"intent-{index}" for index in range(10))
    )

    assert frame.history.history_entry_count == 6
    assert frame.history.history_truncated is True
    assert frame.history.recursive_history_expansion_blocked is True


def test_tc_executionintent_22_eviction_is_recommendation_only() -> None:
    frame = ExecutionIntentRuntime().evaluate(
        history_entries=tuple(f"intent-{index}" for index in range(10))
    )

    assert frame.eviction.stale_intent_history_eviction_recommended is True
    assert frame.eviction.eviction_recommendation == "RECOMMEND_STALE_INTENT_METADATA_EVICTION"
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_executionintent_23_runtime_audit_exposes_required_fields_only() -> None:
    report = run_runtime_enforcement_audit().execution_intent

    assert report.execution_intent_active is True
    assert report.intent_priority_active is True
    assert report.intent_transition_active is True
    assert report.intent_conflict_active is True
    assert report.estimated_avoided_intent_oscillation == 31
    assert report.estimated_avoided_recursive_planning == 19
    assert report.estimated_avoided_execution_instability == 17


def test_tc_executionintent_24_runtime_is_deterministic_and_summary_only() -> None:
    first = ExecutionIntentRuntime().evaluate()
    second = ExecutionIntentRuntime().evaluate()

    assert first == second
    assert first.summary_only is True
    assert first.governance.deterministic_intent_signaling_enforced is True
    assert first.estimated_avoided_intent_oscillation == 31
