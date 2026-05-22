from __future__ import annotations

from ai_dev_os.adaptive_provider_routing import AdaptiveProviderRoutingRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_adaptiverouting_01_runtime_is_bounded_and_human_confirmed() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.adaptive_provider_routing_active is True
    assert frame.human_confirmed_only is True
    assert frame.adaptive.human_confirmed_only is True
    assert frame.adaptive.bounded_recommendations is True
    assert frame.adaptive.no_hidden_provider_switching is True
    assert frame.adaptive.no_recursive_routing_loops is True
    assert frame.adaptive.no_unrestricted_provider_escalation is True
    assert "hidden provider switching" in frame.adaptive.blocked_behaviors


def test_tc_adaptiverouting_02_recommendations_route_known_workloads() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.recommendation.provider_recommendation_active is True
    assert frame.recommendation.primary_recommendation == "qwen2.5-coder:7b"
    assert frame.recommendation.provider_recommendation_ranking[0] == "qwen2.5-coder:7b"
    assert (
        frame.recommendation.workload_recommendations["LOW bounded implementation patch"]
        == "qwen2.5-coder:7b"
    )
    assert (
        frame.recommendation.workload_recommendations["larger repetitive workload"]
        == "qwen2.5-coder:14b"
    )
    assert frame.recommendation.human_confirmation_required is True


def test_tc_adaptiverouting_03_stability_weighting_keeps_local_first() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.stability_weighted.stability_weighted_routing_active is True
    assert frame.stability_weighted.stability_weighted_ranking[0] == "qwen2.5-coder:7b"
    assert frame.stability_weighted.low_bounded_provider == "qwen2.5-coder:7b"
    assert frame.stability_weighted.repetitive_workload_provider == "qwen2.5-coder:14b"
    assert frame.stability_weighted.governance_summary_provider == "gemma3:12b"
    assert frame.stability_weighted.high_reasoning_provider == "GPT-5.5 reference"


def test_tc_adaptiverouting_04_drift_aware_routing_penalizes_risk() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.drift_aware_routing_active is True
    assert frame.drift_aware.drift_aware_routing_result == (
        "DRIFT_LOW_LOCAL_FIRST_ESCALATION_GUARDED"
    )
    assert frame.drift_aware.drift_confidence_penalty["qwen2.5-coder:7b"] < (
        frame.drift_aware.drift_confidence_penalty["GPT-5.5 reference"]
    )
    assert frame.drift_aware.retrieval_radius_inflation["GPT-5.5 reference"] > 0


def test_tc_adaptiverouting_05_governance_weighting_blocks_escalation() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.governance_weighted_routing_active is True
    assert frame.governance_weighted.governance_weighted_ranking[0] == "qwen2.5-coder:7b"
    assert frame.governance_weighted.escalation_blocked_by_governance is True
    assert frame.governance_weighted.governance_weighted_routing_result == (
        "GOVERNANCE_WEIGHTED_LOCAL_PATCH_PREFERRED"
    )
    assert frame.governance.local_patch_discipline is True


def test_tc_adaptiverouting_06_compactness_routes_with_fallback_hints() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.compactness.compactness_routing_active is True
    assert frame.compactness.compactness_scores["qwen2.5-coder:7b"] == 94
    assert frame.compactness.giant_payloads_evicted is True
    assert frame.compactness.compact_continuity_preserved is True
    assert any("gemma3:12b" in hint for hint in frame.compactness.compact_fallback_hints)


def test_tc_adaptiverouting_07_fallback_pressure_never_escalates_unbounded() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.fallback_pressure.fallback_pressure_routing_active is True
    assert frame.fallback_pressure.fallback_frequency["qwen2.5-coder:7b"] == 1
    assert frame.fallback_pressure.unrestricted_fallback_escalation_allowed is False
    assert frame.fallback_pressure.fallback_pressure_penalty["GPT-5.5 reference"] > (
        frame.fallback_pressure.fallback_pressure_penalty["qwen2.5-coder:7b"]
    )


def test_tc_adaptiverouting_08_long_session_routing_preserves_continuity() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.long_session_routing_active is True
    assert frame.long_session.repeated_sprint_degradation["qwen2.5-coder:7b"] == 4
    assert frame.long_session.continuity_corruption_risk["GPT-5.5 reference"] == 14
    assert frame.long_session.stability_weighted_recommendations[0] == "qwen2.5-coder:7b"
    downgrade_suggestions = frame.long_session.governance_safe_downgrade_suggestions
    assert any("qwen2.5-coder:14b" in hint for hint in downgrade_suggestions)


def test_tc_adaptiverouting_09_confidence_labels_are_deterministic() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.routing_confidence_active is True
    assert frame.confidence.overall_confidence == "STABLE_LOCAL"
    assert frame.confidence.confidence_label_by_provider["qwen2.5-coder:7b"] == "STABLE_LOCAL"
    assert frame.confidence.confidence_label_by_provider["gemma3:12b"] == "STABLE_GOVERNANCE"
    assert frame.confidence.confidence_label_by_provider["GPT-5.5 reference"] == (
        "HIGH_ESCALATION_REQUIRED"
    )
    assert (
        frame.confidence.confidence_label_by_provider["OpenMythos placeholder:not_loaded"]
        == "LOW_CONFIDENCE"
    )


def test_tc_adaptiverouting_10_history_is_bounded_and_evictable() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.history.routing_history_active is True
    assert frame.history.bounded_history_size == 8
    assert len(frame.history.provider_recommendation_history) <= frame.history.bounded_history_size
    assert frame.eviction.routing_eviction_active is True
    assert frame.eviction.stale_routing_history_evicted is True
    assert frame.eviction.oversized_recommendation_payloads_evicted is True


def test_tc_adaptiverouting_11_pressure_blocks_recursive_rerouting() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.pressure.routing_pressure_active is True
    assert frame.pressure.recursive_pressure_detected is True
    assert frame.pressure.escalation_pressure == "GUARDED"
    assert frame.pressure.escalation_blocked is True
    assert frame.governance.autonomous_execution_enabled is False
    assert frame.governance.governance_runtime_bypassed is False


def test_tc_adaptiverouting_12_runtime_audit_exposes_adaptive_flags() -> None:
    report = run_runtime_enforcement_audit().adaptive_provider_routing

    assert report.adaptive_provider_routing_active is True
    assert report.drift_aware_routing_active is True
    assert report.governance_weighted_routing_active is True
    assert report.long_session_routing_active is True
    assert report.routing_confidence_active is True
    assert report.estimated_avoided_provider_drift == 14
    assert report.estimated_avoided_recursive_routing == 9
    assert report.estimated_avoided_premium_burn == 18


def test_tc_adaptiverouting_13_runtime_is_deterministic() -> None:
    first = AdaptiveProviderRoutingRuntime().evaluate()
    second = AdaptiveProviderRoutingRuntime().evaluate()

    assert first == second
    assert first.deterministic is True
    assert first.rollback_safe is True
    assert first.local_only is True
    assert first.summary_only is True


def test_tc_adaptiverouting_14_openmythos_remains_placeholder_only() -> None:
    frame = AdaptiveProviderRoutingRuntime().evaluate()

    assert frame.adaptive.openmythos_placeholder_only is True
    assert frame.stability_weighted.openmythos_placeholder_provider == (
        "OpenMythos placeholder:not_loaded"
    )
    assert (
        frame.recommendation.workload_recommendations["OpenMythos placeholder evaluation"]
        == "OpenMythos placeholder:not_loaded"
    )
    assert frame.recommendation.automatic_switching_allowed is False
    assert frame.recommendation.premium_escalation_silent is False
