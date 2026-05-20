from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from ai_dev_os.provider_routing.provider_pressure import ProviderUsageSample


@dataclass(frozen=True)
class ProviderObservabilityFrame:
    provider_usage_distribution_summary: dict[str, int]
    premium_vs_cheap_ratio: float
    bounded_provider_trend_summary: tuple[str, ...]
    no_real_billing_integration: bool
    deterministic_estimated_burn_only: bool
    estimated_premium_provider_burn: int
    summary_only: bool
    local_only: bool


class ProviderObservabilityPolicy:
    def summarize(
        self,
        samples: tuple[ProviderUsageSample, ...],
        *,
        previous_distribution: tuple[str, ...] = (),
    ) -> ProviderObservabilityFrame:
        distribution = Counter(sample.provider_class for sample in samples)
        cheap = max(1, distribution.get("LOW", 0))
        ratio = round(distribution.get("HIGH", 0) / cheap, 4)
        trend = tuple(previous_distribution[-3:]) + tuple(
            f"{provider_class}:{count}" for provider_class, count in sorted(distribution.items())
        )
        burn = sum(sample.estimated_premium_units for sample in samples)
        return ProviderObservabilityFrame(
            provider_usage_distribution_summary=dict(sorted(distribution.items())),
            premium_vs_cheap_ratio=ratio,
            bounded_provider_trend_summary=trend[-6:],
            no_real_billing_integration=True,
            deterministic_estimated_burn_only=True,
            estimated_premium_provider_burn=burn,
            summary_only=True,
            local_only=True,
        )
