from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from governance.budget_runtime import BudgetEnforcement, PressureLevel

EXPENSIVE_TIER2_MODEL_MARKER = "gpt-" + "5.5"


class IntegrationStatus(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    OFFLINE = "offline"


@dataclass(frozen=True)
class IntegrationHealth:
    name: str
    status: IntegrationStatus
    provider_available: bool
    offline_fallback: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class IntegrationDecision:
    provider: str
    model: str
    status: IntegrationStatus
    fallback_used: bool
    warnings: tuple[str, ...]


class IntegrationRuntime:
    def __init__(self, health: dict[str, IntegrationHealth] | None = None) -> None:
        self.health = health or {}

    def register(self, health: IntegrationHealth) -> None:
        self.health[health.name] = health

    def check_health(self, name: str) -> IntegrationHealth:
        return self.health.get(
            name,
            IntegrationHealth(
                name=name,
                status=IntegrationStatus.OFFLINE,
                provider_available=False,
                offline_fallback="local_stub",
                warnings=("PROVIDER_UNREGISTERED",),
            ),
        )

    def route_with_fallback(
        self,
        *,
        provider: str,
        model: str,
        budget: BudgetEnforcement,
    ) -> IntegrationDecision:
        health = self.check_health(provider)
        warnings = list(health.warnings)
        selected_model = model
        fallback_used = False

        if (
            budget.pressure
            in {
                PressureLevel.HIGH,
                PressureLevel.CRITICAL,
            }
            and EXPENSIVE_TIER2_MODEL_MARKER in model
        ):
            selected_model = (
                "tier1-balanced-fallback" if budget.tier2_enabled else "tier0-local-fallback"
            )
            fallback_used = True
            warnings.append("BUDGET_AWARE_DOWNGRADE")

        if not health.provider_available:
            fallback_used = True
            selected_model = health.offline_fallback
            warnings.append("OFFLINE_FALLBACK_USED")

        return IntegrationDecision(
            provider=provider,
            model=selected_model,
            status=health.status,
            fallback_used=fallback_used,
            warnings=tuple(dict.fromkeys(warnings)),
        )


def safe_call(default: object, callback, *args, **kwargs) -> object:
    try:
        return callback(*args, **kwargs)
    except Exception:
        return default
