from __future__ import annotations

import pytest

from governance import BudgetState, ModelTier, PressureLevel, pressure_for_budget, route_tier
from governance.budget_runtime import enforcement_for_pressure
from governance.gpt55_guard import GPT55PolicyViolationError, enforce


def test_budget_pressure_disables_tier2_at_high_pressure() -> None:
    pressure = pressure_for_budget(BudgetState(100.0, 500.0, 1500.0, daily_spend=90.0))
    enforcement = enforcement_for_pressure(pressure)

    assert pressure is PressureLevel.HIGH
    assert enforcement.tier2_enabled is False


def test_model_tier_routing_and_gpt55_guard() -> None:
    assert route_tier("tiny patch") is ModelTier.TIER0
    with pytest.raises(GPT55PolicyViolationError):
        enforce("tiny_patch", "gpt-5.5")
