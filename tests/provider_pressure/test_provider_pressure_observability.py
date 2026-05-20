from __future__ import annotations

from ai_dev_os.provider_routing.provider_observability import ProviderObservabilityPolicy
from ai_dev_os.provider_routing.provider_pressure import (
    ProviderPressurePolicy,
    ProviderUsageSample,
)


def _samples() -> tuple[ProviderUsageSample, ...]:
    return (
        ProviderUsageSample("architecture", "HIGH", 8, escalation=True, premium_required=True),
        ProviderUsageSample("routine patch", "HIGH", 6, escalation=True),
        ProviderUsageSample("docs", "LOW"),
        ProviderUsageSample("tests", "LOW"),
    )


def test_tc_providerrouting_04_pressure_detects_premium_overuse() -> None:
    frame = ProviderPressurePolicy().evaluate(_samples(), premium_budget=10, escalation_limit=1)

    assert frame.premium_provider_overuse_detection is True
    assert frame.repeated_premium_escalation_detection is True
    assert frame.unnecessary_high_tier_provider_usage is True
    assert frame.estimated_premium_provider_burn == 14
    assert frame.estimated_unnecessary_high_tier_usage == 6
    assert frame.provider_pressure == "HIGH"


def test_tc_providerrouting_08_observability_is_summary_only_without_billing() -> None:
    frame = ProviderObservabilityPolicy().summarize(
        _samples(),
        previous_distribution=("LOW:1", "MEDIUM:1"),
    )

    assert frame.provider_usage_distribution_summary == {"HIGH": 2, "LOW": 2}
    assert frame.premium_vs_cheap_ratio == 1.0
    assert frame.bounded_provider_trend_summary
    assert frame.no_real_billing_integration is True
    assert frame.deterministic_estimated_burn_only is True
    assert frame.summary_only is True
