from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.runtime_policy import (
    CONTINUATION_SATURATION_THRESHOLD,
    MAX_ESCALATION_DEPTH,
    MAX_POLICY_HISTORY,
    POLICY_BUDGET_LIMIT,
    REFLECTIVE_SATURATION_THRESHOLD,
    RETRY_AMPLIFICATION_THRESHOLD,
    RUNTIME_POLICY_REQUIREMENT_IDS,
    RUNTIME_POLICY_TEST_IDS,
    RuntimePolicyEngine,
)


def test_tc_runtimepolicy_01_active_runtime_is_bounded_local_patch() -> None:
    frame = RuntimePolicyEngine().evaluate()

    assert frame.runtime_policy_active is True
    assert frame.requirement_ids == RUNTIME_POLICY_REQUIREMENT_IDS
    assert frame.test_ids == RUNTIME_POLICY_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.runtime_policy_mode == "LOCAL_PATCH_UNIFIED_RUNTIME_POLICY"


def test_tc_runtimepolicy_02_execution_policy_enforcement() -> None:
    frame = RuntimePolicyEngine().evaluate()

    assert frame.execution_policy.execution_policy_active is True
    assert frame.execution_policy.bounded_subprocess_execution is True
    assert frame.execution_policy.bounded_filesystem_access is True
    assert frame.execution_policy.verified_execution_only_operations is True
    assert frame.execution_policy.deterministic_execution_windows is True
    assert frame.execution_policy_score >= 80
    assert frame.execution_policy.bounded_execution_recommendation == (
        "FOLLOW_VERIFIED_EXECUTION_WINDOW"
    )


def test_tc_runtimepolicy_03_retry_policy_enforcement() -> None:
    frame = RuntimePolicyEngine().evaluate(
        retry_count=RETRY_AMPLIFICATION_THRESHOLD + 1,
        retry_cooldown_pressure=2,
        retry_interruption_pressure=1,
    )

    assert frame.retry_policy.retry_policy_active is True
    assert frame.retry_policy.bounded_retry_chains is False
    assert frame.retry_policy.retry_cooldown_enforced is True
    assert frame.policy_termination.retry_amplification_threshold_exceeded is True
    assert frame.retry_policy.bounded_retry_reset_recommendation == (
        "RESET_RETRY_CHAIN_AND_APPLY_POLICY_COOLDOWN"
    )


def test_tc_runtimepolicy_04_provider_policy_governance() -> None:
    frame = RuntimePolicyEngine().evaluate(
        escalation_depth=MAX_ESCALATION_DEPTH + 1,
        provider_cost_pressure=72,
        provider_fatigue_pressure=3,
    )

    assert frame.provider_policy.provider_policy_active is True
    assert frame.provider_policy.local_first_routing is True
    assert frame.provider_policy.bounded_escalation_depth is False
    assert frame.escalation_policy.escalation_depth_exceeded is True
    assert frame.cost_policy.cost_pressure == "HIGH"
    assert frame.provider_policy.bounded_provider_routing_recommendation == (
        "LOCAL_FIRST_AND_BLOCK_FRONTIER_ESCALATION"
    )


def test_tc_runtimepolicy_05_continuation_policy_enforcement() -> None:
    frame = RuntimePolicyEngine().evaluate(
        continuation_depth=3,
        continuation_saturation=CONTINUATION_SATURATION_THRESHOLD,
    )

    assert frame.continuation_policy.continuation_policy_active is True
    assert frame.continuation_policy.bounded_continuation_depth is False
    assert frame.policy_termination.continuation_saturation_threshold_exceeded is True
    assert frame.continuation_policy.bounded_continuation_reset_recommendation == (
        "RESET_CONTINUATION_POLICY_WINDOW"
    )


def test_tc_runtimepolicy_06_reflection_policy_governance() -> None:
    frame = RuntimePolicyEngine().evaluate(
        reflective_saturation=REFLECTIVE_SATURATION_THRESHOLD,
    )

    assert frame.reflection_policy.reflection_policy_active is True
    assert frame.reflection_policy.bounded_reflective_scoring is True
    assert frame.reflection_policy.bounded_reflective_windows is True
    assert frame.policy_termination.reflective_saturation_threshold_exceeded is True
    assert frame.reflection_policy.bounded_reflective_reset_recommendation == (
        "RESET_REFLECTIVE_POLICY_WINDOW"
    )


def test_tc_runtimepolicy_07_recursive_governance_blocking() -> None:
    frame = RuntimePolicyEngine().evaluate(
        recursive_governance_attempts=1,
        hidden_governance_mutation_attempts=1,
        recursive_policy_optimization_attempts=1,
        self_expanding_governance_graph_attempts=1,
        policy_driven_autonomous_execution_attempts=1,
        policy_mutation_attempts=1,
        retrieval_scope_widening_attempts=1,
    )

    assert frame.governance_policy.hidden_governance_mutation_blocked is True
    assert frame.governance_policy.recursive_policy_optimization_blocked is True
    assert frame.governance_policy.self_expanding_governance_graphs_blocked is True
    assert frame.governance_policy.policy_driven_autonomous_execution_blocked is True
    assert frame.governance_policy.policy_mutation_blocked is True
    assert frame.governance_policy.retrieval_scope_widening_blocked is True
    assert frame.policy_termination.recursive_governance_detected is True
    assert "RECURSIVE_GOVERNANCE_DETECTED" in frame.policy_termination.termination_reasons
    assert "GOVERNANCE_VIOLATION_DETECTED" in frame.policy_termination.termination_reasons


def test_tc_runtimepolicy_08_escalation_blocking() -> None:
    frame = RuntimePolicyEngine().evaluate(
        escalation_depth=MAX_ESCALATION_DEPTH + 2,
        autonomous_escalation_attempts=1,
    )

    assert frame.escalation_policy.autonomous_escalation_blocked is True
    assert frame.escalation_policy.frontier_escalation_guarded is True
    assert frame.policy_termination.escalation_depth_exceeded is True
    assert frame.governance_policy.autonomous_escalation_blocked is True
    assert "ESCALATION_DEPTH_EXCEEDED" in frame.policy_termination.termination_reasons


def test_tc_runtimepolicy_09_policy_arbitration() -> None:
    frame = RuntimePolicyEngine().evaluate(
        escalation_depth=2,
        provider_cost_pressure=72,
        retry_count=2,
        retry_cooldown_pressure=2,
    )

    assert frame.policy_conflict.policy_conflict_active is True
    assert frame.policy_conflict.retry_vs_cooldown_conflict is True
    assert frame.policy_conflict.escalation_vs_cost_conflict is True
    assert frame.policy_conflict.bounded_arbitration_recommendation == (
        "COST_POLICY_OVERRIDES_ESCALATION"
    )


def test_tc_runtimepolicy_10_bounded_policy_history_retention() -> None:
    history = tuple(f"policy_{index}" for index in range(9))
    frame = RuntimePolicyEngine().evaluate(policy_history_items=history)

    assert len(frame.policy_history.policy_history) == MAX_POLICY_HISTORY
    assert frame.policy_history.policy_history_overflow_blocked is True
    assert frame.policy_eviction.evicted_policy_history_items == history[MAX_POLICY_HISTORY:]
    assert frame.policy_eviction.bounded_eviction_active is True


def test_tc_runtimepolicy_11_policy_budget_termination() -> None:
    frame = RuntimePolicyEngine().evaluate(policy_budget_used=POLICY_BUDGET_LIMIT + 1)

    assert frame.policy_budget.policy_budget_exceeded is True
    assert frame.policy_termination.policy_budget_exceeded is True
    assert frame.policy_termination.policy_terminated is True
    assert "POLICY_BUDGET_EXCEEDED" in frame.policy_termination.termination_reasons


def test_tc_runtimepolicy_12_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().runtime_policy

    assert report.runtime_policy_active is True
    assert 0 <= report.execution_policy_score <= 100
    assert 0 <= report.retry_policy_score <= 100
    assert 0 <= report.provider_policy_score <= 100
    assert 0 <= report.continuation_policy_score <= 100
    assert 0 <= report.reflective_policy_score <= 100
    assert report.estimated_avoided_recursive_governance > 0
    assert report.estimated_avoided_frontier_escalation > 0
    assert report.estimated_avoided_policy_fragmentation > 0


def test_tc_runtimepolicy_13_runtime_is_deterministic() -> None:
    first = RuntimePolicyEngine().evaluate()
    second = RuntimePolicyEngine().evaluate()

    assert first == second
    assert first.policy_coherence.policy_coherence_active is True
    assert first.governance_policy.deterministic_bounded_governance is True
