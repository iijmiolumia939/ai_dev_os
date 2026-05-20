from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderUsageSample:
    task_name: str
    provider_class: str
    estimated_premium_units: int = 0
    escalation: bool = False
    premium_required: bool = False


@dataclass(frozen=True)
class ProviderPressureFrame:
    premium_provider_overuse_detection: bool
    repeated_premium_escalation_detection: bool
    unnecessary_high_tier_provider_usage: bool
    provider_concentration_pressure: bool
    estimated_premium_provider_burn: int
    estimated_unnecessary_high_tier_usage: int
    provider_pressure: str
    deterministic: bool
    summary_only: bool


class ProviderPressurePolicy:
    def evaluate(
        self,
        samples: tuple[ProviderUsageSample, ...],
        *,
        premium_budget: int = 12,
        escalation_limit: int = 1,
    ) -> ProviderPressureFrame:
        premium_samples = tuple(sample for sample in samples if sample.provider_class == "HIGH")
        premium_burn = sum(sample.estimated_premium_units for sample in premium_samples)
        escalation_count = sum(1 for sample in premium_samples if sample.escalation)
        unnecessary_high = tuple(
            sample for sample in premium_samples if not sample.premium_required
        )
        distribution = Counter(sample.provider_class for sample in samples)
        dominant = max(distribution.values(), default=0)
        concentration = bool(samples) and dominant / len(samples) >= 0.75
        overuse = premium_burn > premium_budget
        repeated = escalation_count > escalation_limit
        unnecessary_units = sum(sample.estimated_premium_units for sample in unnecessary_high)
        total_pressure = premium_burn + unnecessary_units + repeated * 4 + concentration * 2
        if overuse or total_pressure >= 18:
            pressure = "HIGH"
        elif total_pressure > 0:
            pressure = "MEDIUM"
        else:
            pressure = "LOW"
        return ProviderPressureFrame(
            premium_provider_overuse_detection=overuse,
            repeated_premium_escalation_detection=repeated,
            unnecessary_high_tier_provider_usage=bool(unnecessary_high),
            provider_concentration_pressure=concentration,
            estimated_premium_provider_burn=premium_burn,
            estimated_unnecessary_high_tier_usage=unnecessary_units,
            provider_pressure=pressure,
            deterministic=True,
            summary_only=True,
        )
