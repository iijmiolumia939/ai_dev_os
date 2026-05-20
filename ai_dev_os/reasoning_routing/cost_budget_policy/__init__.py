from __future__ import annotations

from dataclasses import dataclass

REASONING_BURN_UNITS = {"HIGH": 8, "MEDIUM": 3, "LOW": 1}


@dataclass(frozen=True)
class ReasoningUsageSample:
    task_name: str
    tier: str
    count: int = 1


@dataclass(frozen=True)
class CostBudgetFrame:
    estimated_daily_burn: int
    estimated_monthly_burn: int
    reasoning_tier_distribution: dict[str, int]
    budget_pressure: str
    over_budget: bool
    compaction_recommendation: bool
    downgrade_recommendation: bool
    estimated_avoided_premium_burn: int
    estimated_avoided_unnecessary_escalation: int
    deterministic_estimate: bool
    billing_api_used: bool


class CostBudgetPolicy:
    def evaluate(
        self,
        samples: tuple[ReasoningUsageSample, ...],
        *,
        daily_budget_units: int = 40,
        monthly_budget_units: int = 800,
    ) -> CostBudgetFrame:
        distribution = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for sample in samples:
            tier = sample.tier.upper()
            if tier not in distribution:
                raise ValueError(f"unknown reasoning tier: {sample.tier}")
            distribution[tier] += max(0, sample.count)
        daily_burn = sum(distribution[tier] * REASONING_BURN_UNITS[tier] for tier in distribution)
        monthly_burn = daily_burn * 22
        daily_ratio = daily_burn / max(1, daily_budget_units)
        monthly_ratio = monthly_burn / max(1, monthly_budget_units)
        pressure_ratio = max(daily_ratio, monthly_ratio)
        if pressure_ratio >= 1.0:
            pressure = "OVER_BUDGET"
        elif pressure_ratio >= 0.85:
            pressure = "HIGH"
        elif pressure_ratio >= 0.65:
            pressure = "WARNING"
        else:
            pressure = "NORMAL"
        total_tasks = sum(distribution.values())
        all_premium_burn = total_tasks * REASONING_BURN_UNITS["HIGH"]
        avoided_premium = max(0, all_premium_burn - daily_burn)
        avoidable_escalation = distribution["MEDIUM"] + distribution["LOW"]
        return CostBudgetFrame(
            estimated_daily_burn=daily_burn,
            estimated_monthly_burn=monthly_burn,
            reasoning_tier_distribution=distribution,
            budget_pressure=pressure,
            over_budget=pressure == "OVER_BUDGET",
            compaction_recommendation=pressure in {"HIGH", "OVER_BUDGET"}
            or distribution["HIGH"] >= 2,
            downgrade_recommendation=pressure in {"WARNING", "HIGH", "OVER_BUDGET"}
            and distribution["LOW"] > 0,
            estimated_avoided_premium_burn=avoided_premium,
            estimated_avoided_unnecessary_escalation=avoidable_escalation,
            deterministic_estimate=True,
            billing_api_used=False,
        )
