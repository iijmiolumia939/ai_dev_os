from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PressureLevel(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class BudgetState:
    daily_budget: float
    weekly_budget: float
    monthly_budget: float
    daily_spend: float = 0.0
    weekly_spend: float = 0.0
    monthly_spend: float = 0.0


@dataclass(frozen=True)
class BudgetEnforcement:
    pressure: PressureLevel
    tier2_enabled: bool
    council_scope: str
    patch_only_enforced: bool
    max_context_tokens: int
    warnings: tuple[str, ...]


def pressure_for_budget(state: BudgetState) -> PressureLevel:
    ratios = [
        state.daily_spend / state.daily_budget if state.daily_budget else 1.0,
        state.weekly_spend / state.weekly_budget if state.weekly_budget else 1.0,
        state.monthly_spend / state.monthly_budget if state.monthly_budget else 1.0,
    ]
    highest = max(ratios)
    if highest >= 1.0:
        return PressureLevel.CRITICAL
    if highest >= 0.85:
        return PressureLevel.HIGH
    if highest >= 0.65:
        return PressureLevel.WARNING
    return PressureLevel.INFO


def enforcement_for_pressure(pressure: PressureLevel) -> BudgetEnforcement:
    if pressure is PressureLevel.CRITICAL:
        return BudgetEnforcement(
            pressure=pressure,
            tier2_enabled=False,
            council_scope="tier0_only",
            patch_only_enforced=True,
            max_context_tokens=8_000,
            warnings=("BUDGET_CRITICAL", "TIER2_DISABLED", "PATCH_ONLY_ENFORCED"),
        )
    if pressure is PressureLevel.HIGH:
        return BudgetEnforcement(
            pressure=pressure,
            tier2_enabled=False,
            council_scope="tier1_partial",
            patch_only_enforced=True,
            max_context_tokens=12_000,
            warnings=("BUDGET_HIGH", "TIER2_DISABLED", "COUNCIL_REDUCED"),
        )
    if pressure is PressureLevel.WARNING:
        return BudgetEnforcement(
            pressure=pressure,
            tier2_enabled=True,
            council_scope="scoped_only",
            patch_only_enforced=True,
            max_context_tokens=20_000,
            warnings=("BUDGET_WARNING", "PATCH_ONLY_ENFORCED"),
        )
    return BudgetEnforcement(
        pressure=pressure,
        tier2_enabled=True,
        council_scope="normal_scoped",
        patch_only_enforced=False,
        max_context_tokens=20_000,
        warnings=(),
    )
