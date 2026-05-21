from __future__ import annotations

from ai_dev_os.dev_strategy import DevelopmentStrategyRuntime


def test_tc_devstrategy_08_governance_strategy_blocks_roadmap_generation() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()
    governance = frame.governance_stability

    assert governance.sprint_governance_stability == "WATCH"
    assert governance.continuity_accumulation_pressure == "MEDIUM"
    assert governance.roadmap_branching_pressure == "MEDIUM"
    assert governance.cognition_explosion_attempts == 2
    assert "no_autonomous_roadmap_generation" in governance.governance_hardening_reminders
    assert governance.roadmap_boundary_protected is True


def test_tc_devstrategy_09_embodiment_focus_stays_renderer_neutral() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()
    embodiment = frame.embodiment_focus

    assert "preserve_low_motion_presence" in embodiment.embodiment_realism_hints
    assert "prefer_subtle_waiting_signals" in embodiment.low_motion_continuity_hints
    assert (
        "strategy_must_not_require_animation_authority"
        in embodiment.renderer_neutral_evolution_hints
    )
    assert embodiment.theatrical_escalation_prevented is True
    assert embodiment.animation_authority_creep_prevented is True
    assert embodiment.procedural_acting_pressure_prevented is True


def test_tc_devstrategy_10_strategy_eviction_keeps_only_compact_heuristics() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()
    eviction = frame.eviction

    assert eviction.strategy_eviction_active is True
    assert eviction.compact_useful_heuristics_only is True
    assert eviction.evicted_oversized_recommendation_trees == ("recursive-roadmap-tree",)
    assert eviction.evicted_obsolete_provider_heuristics == ("old-high-default",)
    assert "human_confirmed_strategy_only" in eviction.preserved_compact_useful_heuristics
    assert frame.pressure.bounded_cognition_only is True
