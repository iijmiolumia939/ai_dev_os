from __future__ import annotations

from ai_dev_os.reasoning_routing.cost_budget_policy import CostBudgetPolicy, ReasoningUsageSample


def test_tc_reasoning_04_budget_estimation_validation() -> None:
    frame = CostBudgetPolicy().evaluate(
        (
            ReasoningUsageSample("architecture", "HIGH"),
            ReasoningUsageSample("adapter wiring", "MEDIUM"),
            ReasoningUsageSample("docs", "LOW"),
            ReasoningUsageSample("runtime tests", "LOW"),
        ),
        daily_budget_units=20,
        monthly_budget_units=500,
    )

    assert frame.estimated_daily_burn == 13
    assert frame.estimated_monthly_burn == 286
    assert frame.reasoning_tier_distribution == {"HIGH": 1, "MEDIUM": 1, "LOW": 2}
    assert frame.deterministic_estimate is True
    assert frame.billing_api_used is False
    assert frame.estimated_avoided_premium_burn == 19


def test_tc_reasoning_04_budget_pressure_and_recommendations() -> None:
    frame = CostBudgetPolicy().evaluate(
        (
            ReasoningUsageSample("architecture", "HIGH", count=3),
            ReasoningUsageSample("docs", "LOW", count=2),
        ),
        daily_budget_units=20,
        monthly_budget_units=400,
    )

    assert frame.over_budget is True
    assert frame.budget_pressure == "OVER_BUDGET"
    assert frame.compaction_recommendation is True
    assert frame.downgrade_recommendation is True
