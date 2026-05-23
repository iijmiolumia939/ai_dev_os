from __future__ import annotations

from ai_dev_os.adaptive_provider import (
    ADAPTIVE_PROVIDER_REQUIREMENT_IDS,
    ADAPTIVE_PROVIDER_TEST_IDS,
    MAX_PROVIDER_HISTORY,
    MAX_SPECIALIZATIONS,
    AdaptiveProviderRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_adaptiveprovider_01_active_runtime_is_bounded_local_patch() -> None:
    frame = AdaptiveProviderRuntime().evaluate()

    assert frame.adaptive_provider_active is True
    assert frame.requirement_ids == ADAPTIVE_PROVIDER_REQUIREMENT_IDS
    assert frame.test_ids == ADAPTIVE_PROVIDER_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.provider_routing_mode == "LOCAL_FIRST_BOUNDED_ADAPTATION"


def test_tc_adaptiveprovider_02_provider_capability_scoring() -> None:
    frame = AdaptiveProviderRuntime().evaluate(
        provider_capabilities={
            "execution": 30,
            "orchestration": 25,
            "planning": 20,
            "reflection": 15,
        }
    )

    assert 0 <= frame.provider_capability_score <= 100
    assert frame.provider_capability.provider_capability_active is True
    assert frame.provider_capability.deterministic_execution_success is True
    assert frame.provider_capability.verified_execution_quality == "STABLE"
    assert frame.provider_capability.bounded_routing_recommendation.startswith("LOCAL_FIRST")


def test_tc_adaptiveprovider_03_provider_fatigue_tracking() -> None:
    frame = AdaptiveProviderRuntime().evaluate(
        long_session_degradation=3,
        retry_amplification=2,
        orchestration_instability=2,
        continuation_decay=1,
        reflective_saturation=1,
    )

    assert frame.provider_fatigue.provider_fatigue_active is True
    assert frame.provider_fatigue_score >= 70
    assert (
        frame.provider_fatigue.bounded_cooldown_recommendation
        == "COOLDOWN_AND_LOCAL_FIRST_COMPACTION"
    )
    assert frame.provider_termination.provider_instability_threshold_exceeded is True


def test_tc_adaptiveprovider_04_provider_cost_awareness() -> None:
    frame = AdaptiveProviderRuntime().evaluate(
        estimated_token_pressure=62,
        bounded_reasoning_cost=28,
        bounded_execution_cost=18,
        bounded_escalation_pressure=2,
    )

    assert frame.provider_cost.provider_cost_active is True
    assert frame.provider_cost_pressure == "HIGH"
    assert (
        frame.provider_cost.bounded_local_first_recommendation
        == "LOCAL_FIRST_AND_BLOCK_SILENT_ESCALATION"
    )
    assert frame.provider_routing.recommended_provider == "local_compact"


def test_tc_adaptiveprovider_05_provider_routing_recommendations_are_deterministic() -> None:
    first = AdaptiveProviderRuntime().evaluate()
    second = AdaptiveProviderRuntime().evaluate()

    assert (
        first.provider_routing.routing_recommendations
        == second.provider_routing.routing_recommendations
    )
    assert first.provider_routing.deterministic_routing is True
    assert first.provider_routing.bounded_provider_window is True
    assert (
        first.provider_confidence.provider_confidence_score
        == second.provider_confidence.provider_confidence_score
    )


def test_tc_adaptiveprovider_06_recursive_escalation_is_blocked() -> None:
    frame = AdaptiveProviderRuntime().evaluate(
        recursive_escalation_attempts=1,
        escalation_depth=4,
    )

    assert frame.provider_escalation.recursive_escalation_blocked is True
    assert frame.provider_termination.recursive_escalation_detected is True
    assert frame.provider_termination.escalation_depth_exceeded is True
    assert "RECURSIVE_ESCALATION_DETECTED" in frame.provider_termination.termination_reasons
    assert "ESCALATION_DEPTH_EXCEEDED" in frame.provider_termination.termination_reasons


def test_tc_adaptiveprovider_07_provider_governance_enforcement() -> None:
    frame = AdaptiveProviderRuntime().evaluate(
        hidden_provider_switching_attempts=1,
        autonomous_escalation_attempts=1,
        recursive_provider_optimization_attempts=1,
        provider_policy_mutation_attempts=1,
        retrieval_scope_widening_attempts=1,
        hidden_provider_history_attempts=1,
    )

    assert frame.provider_governance.hidden_provider_switching_blocked is True
    assert frame.provider_governance.autonomous_escalation_blocked is True
    assert frame.provider_governance.recursive_provider_optimization_blocked is True
    assert frame.provider_governance.provider_policy_mutation_blocked is True
    assert frame.provider_governance.retrieval_scope_widening_blocked is True
    assert frame.provider_history.hidden_provider_history_blocked is True
    assert frame.provider_termination.governance_violation_detected is True


def test_tc_adaptiveprovider_08_provider_termination_handles_budget_and_instability() -> None:
    frame = AdaptiveProviderRuntime().evaluate(
        provider_budget_used=16,
        long_session_degradation=4,
        retry_amplification=4,
        orchestration_instability=4,
        reflective_saturation=2,
    )

    assert frame.provider_termination.provider_terminated is True
    assert frame.provider_termination.provider_budget_exceeded is True
    assert frame.provider_termination.provider_instability_threshold_exceeded is True
    assert "PROVIDER_BUDGET_EXCEEDED" in frame.provider_termination.termination_reasons
    assert (
        "PROVIDER_INSTABILITY_THRESHOLD_EXCEEDED" in frame.provider_termination.termination_reasons
    )


def test_tc_adaptiveprovider_09_bounded_provider_history_enforcement() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    specializations = tuple(f"specialization_{index}" for index in range(7))
    frame = AdaptiveProviderRuntime().evaluate(
        provider_history_items=history,
        provider_specializations=specializations,
    )

    assert len(frame.provider_history.provider_history) == MAX_PROVIDER_HISTORY
    assert len(frame.provider_specialization.specialization_memory) == MAX_SPECIALIZATIONS
    assert frame.provider_history.history_overflow_blocked is True
    assert frame.provider_specialization.specialization_overflow_blocked is True
    assert frame.provider_eviction.evicted_history_items == history[MAX_PROVIDER_HISTORY:]
    assert frame.provider_eviction.evicted_specializations == specializations[MAX_SPECIALIZATIONS:]


def test_tc_adaptiveprovider_10_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().adaptive_provider

    assert report.adaptive_provider_active is True
    assert 0 <= report.provider_capability_score <= 100
    assert 0 <= report.provider_fatigue_score <= 100
    assert report.provider_cost_pressure in {"LOW", "MEDIUM", "HIGH"}
    assert 0 <= report.provider_confidence_score <= 100
    assert report.estimated_avoided_frontier_provider_usage > 0
    assert report.estimated_avoided_recursive_escalation > 0
    assert report.estimated_avoided_provider_instability > 0


def test_tc_adaptiveprovider_11_runtime_is_deterministic() -> None:
    first = AdaptiveProviderRuntime().evaluate()
    second = AdaptiveProviderRuntime().evaluate()

    assert first == second
    assert first.provider_budget.local_first_budget is True
    assert first.provider_governance.deterministic_routing_enforced is True
