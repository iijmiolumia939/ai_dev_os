from __future__ import annotations

from ai_dev_os.provider_routing.provider_budget_policy import ProviderBudgetPolicy
from ai_dev_os.provider_routing.provider_downgrade import ProviderDowngradePolicy


def test_tc_providerrouting_02_budget_policy_detects_burn_pressure() -> None:
    frame = ProviderBudgetPolicy().evaluate(
        premium_units_used=13,
        premium_reasoning_requests=3,
        premium_escalations=2,
    )

    assert frame.premium_provider_daily_budget == 12
    assert frame.premium_reasoning_quota == 2
    assert frame.downgrade_threshold == 8
    assert frame.escalation_limit == 1
    assert frame.provider_burn_pressure == "OVER_BUDGET"
    assert frame.downgrade_recommended is True
    assert frame.billing_api_used is False


def test_tc_providerrouting_05_downgrade_preserves_quality_floor() -> None:
    frame = ProviderDowngradePolicy().recommend(
        current_provider_class="HIGH",
        quality_floor="MEDIUM",
        compact_summary=True,
        repetitive_task=True,
        local_patch=True,
        pressure_level="HIGH",
    )

    assert frame.recommended_provider_class == "MEDIUM"
    assert frame.quality_floor_aware_downgrade is True
    assert frame.local_patch_downgrade is True
    assert frame.compact_summary_downgrade is True
    assert frame.repetitive_task_downgrade is True
