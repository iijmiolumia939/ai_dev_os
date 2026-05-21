from __future__ import annotations

from ai_dev_os.dev_strategy import DevelopmentStrategyRuntime


def test_tc_devstrategy_06_provider_efficiency_keeps_high_zones_bounded() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()
    provider = frame.provider_efficiency

    assert provider.safe_high_only_zones == (
        "governance_stabilization",
        "roadmap_boundary_analysis",
        "cognition_explosion_prevention",
    )
    assert provider.repeated_premium_provider_waste is True
    assert provider.provider_routing_efficiency == "MEDIUM"
    assert "LOW_for_cleanup_summary" in provider.compact_routing_recommendations
    assert "visible_escalation_reason_required" in provider.bounded_escalation_hints
    assert provider.no_hidden_provider_switching is True


def test_tc_devstrategy_07_sprint_density_prevents_oversized_strategy_surfaces() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()
    density = frame.sprint_density

    assert density.sprint_size == "MEDIUM"
    assert density.retrieval_radius == 2
    assert (
        "cap_next_sprint_to_one_runtime_neighborhood" in density.bounded_sprint_sizing_suggestions
    )
    assert "radius_2_for_boundary_check" in density.retrieval_scope_hints
    assert density.oversized_sprint_expansion_prevented is True
    assert density.giant_validation_surface_prevented is True
    assert density.repo_wide_cognition_prevented is True
