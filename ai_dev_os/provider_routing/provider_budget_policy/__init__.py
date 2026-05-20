from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderBudgetFrame:
    premium_provider_daily_budget: int
    premium_reasoning_quota: int
    downgrade_threshold: int
    escalation_limit: int
    provider_burn_pressure: str
    downgrade_recommended: bool
    escalation_limited: bool
    estimated_remaining_premium_budget: int
    billing_api_used: bool
    deterministic_estimate: bool
    summary_only: bool


class ProviderBudgetPolicy:
    def __init__(
        self,
        *,
        premium_provider_daily_budget: int = 12,
        premium_reasoning_quota: int = 2,
        downgrade_threshold: int = 8,
        escalation_limit: int = 1,
    ) -> None:
        self.premium_provider_daily_budget = premium_provider_daily_budget
        self.premium_reasoning_quota = premium_reasoning_quota
        self.downgrade_threshold = downgrade_threshold
        self.escalation_limit = escalation_limit

    def evaluate(
        self,
        *,
        premium_units_used: int,
        premium_reasoning_requests: int,
        premium_escalations: int,
    ) -> ProviderBudgetFrame:
        pressure_score = max(
            premium_units_used,
            premium_reasoning_requests * self.downgrade_threshold,
            premium_escalations * self.downgrade_threshold,
        )
        if premium_units_used > self.premium_provider_daily_budget:
            pressure = "OVER_BUDGET"
        elif pressure_score >= self.downgrade_threshold:
            pressure = "HIGH"
        elif premium_units_used > 0:
            pressure = "MEDIUM"
        else:
            pressure = "LOW"
        escalation_limited = (
            premium_reasoning_requests > self.premium_reasoning_quota
            or premium_escalations > self.escalation_limit
        )
        return ProviderBudgetFrame(
            premium_provider_daily_budget=self.premium_provider_daily_budget,
            premium_reasoning_quota=self.premium_reasoning_quota,
            downgrade_threshold=self.downgrade_threshold,
            escalation_limit=self.escalation_limit,
            provider_burn_pressure=pressure,
            downgrade_recommended=pressure in {"HIGH", "OVER_BUDGET"} or escalation_limited,
            escalation_limited=escalation_limited,
            estimated_remaining_premium_budget=max(
                0,
                self.premium_provider_daily_budget - premium_units_used,
            ),
            billing_api_used=False,
            deterministic_estimate=True,
            summary_only=True,
        )
