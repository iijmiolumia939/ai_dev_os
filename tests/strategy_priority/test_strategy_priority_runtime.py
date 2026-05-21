from __future__ import annotations

from ai_dev_os.dev_strategy import DevelopmentStrategyRuntime


def test_tc_devstrategy_04_priority_ordering_keeps_governance_and_cost_first() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()
    priority = frame.priority

    assert priority.priority_ordering[:3] == (
        "governance_stability",
        "cost_reduction",
        "bounded_sprint_continuity",
    )
    assert "provider_efficiency" in priority.priority_ordering
    assert "LOCAL_PATCH_sustainability" in priority.priority_ordering
    assert priority.human_confirmed_prioritization is True
    assert priority.local_patch_sustainability is True


def test_tc_devstrategy_05_cost_reduction_preserves_quality_boundaries() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()
    cost = frame.cost_reduction

    assert cost.provider_usage_distribution == {"HIGH": 3, "MEDIUM": 3, "LOW": 3}
    assert cost.premium_provider_pressure == "MEDIUM"
    assert "HIGH_only_for_boundary_risk" in cost.downgrade_safe_recommendations
    assert "route_repetitive_formatting_to_LOW" in cost.bounded_provider_routing_suggestions
    assert cost.unsafe_reasoning_downgrades_prevented is True
    assert cost.governance_quality_preserved is True
    assert cost.architecture_quality_preserved is True
