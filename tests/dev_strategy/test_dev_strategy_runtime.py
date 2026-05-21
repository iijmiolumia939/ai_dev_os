from __future__ import annotations

from ai_dev_os.dev_strategy import (
    DEV_STRATEGY_REQUIREMENT_IDS,
    DEV_STRATEGY_TEST_IDS,
    DevelopmentStrategyRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_devstrategy_01_runtime_is_bounded_and_human_confirmed() -> None:
    frame = DevelopmentStrategyRuntime().evaluate()

    assert "FR-DEVSTRATEGY-01" in DEV_STRATEGY_REQUIREMENT_IDS
    assert "NFR-COST-23" in DEV_STRATEGY_REQUIREMENT_IDS
    assert "TC-DEVSTRATEGY-01" in DEV_STRATEGY_TEST_IDS
    assert frame.dev_strategy_active is True
    assert frame.bounded_strategy_only is True
    assert frame.human_confirmed_strategy_only is True
    assert frame.no_autonomous_roadmap_generation is True
    assert frame.no_recursive_future_sprint_synthesis is True
    assert frame.no_giant_strategic_replay is True


def test_tc_devstrategy_02_recommendations_are_compact_non_binding_and_deterministic() -> None:
    first = DevelopmentStrategyRuntime().evaluate()
    second = DevelopmentStrategyRuntime().evaluate()

    assert first == second
    assert first.recommendation.non_binding is True
    assert first.recommendation.human_confirmed is True
    assert first.recommendation.compact is True
    assert first.recommendation.deterministic is True
    assert len(first.recommendation.next_bounded_recommendation_candidates) <= 5
    assert first.local_only is True
    assert first.summary_only is True


def test_tc_devstrategy_03_runtime_audit_reports_strategy_flags() -> None:
    report = run_runtime_enforcement_audit().dev_strategy

    assert report.dev_strategy_active is True
    assert report.strategy_priority_active is True
    assert report.cost_reduction_strategy_active is True
    assert report.governance_stability_strategy_active is True
    assert report.provider_efficiency_strategy_active is True
    assert report.sprint_density_strategy_active is True
    assert report.embodiment_focus_strategy_active is True
    assert report.strategy_eviction_active is True
    assert report.estimated_avoided_strategy_overhead == 3240
    assert report.estimated_avoided_roadmap_explosion == 2400
