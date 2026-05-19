from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.providers.mock_provider import MockProviderFrame, simulate_provider_request
from ai_dev_os.providers.provider_contracts import ProviderRequest
from governance.budget_runtime import (
    BudgetState,
    PressureLevel,
    enforcement_for_pressure,
    pressure_for_budget,
)


@dataclass(frozen=True)
class FallbackSimulationFrame:
    pressure: str
    tier2_disabled: bool
    tier1_degraded: bool
    local_fallback: bool
    retrieval_only_fallback: bool
    summary_only_fallback: bool
    patch_only_fallback: bool
    route_chain: tuple[str, ...]
    provider_frame: MockProviderFrame


def simulate_fallback_chain(
    request: ProviderRequest,
    *,
    budget_state: BudgetState,
) -> FallbackSimulationFrame:
    pressure = pressure_for_budget(budget_state)
    enforcement = enforcement_for_pressure(pressure)
    provider_frame = simulate_provider_request(request)
    tier2_disabled = not enforcement.tier2_enabled
    tier1_degraded = provider_frame.response.status in {
        "rate_limit",
        "degraded_response",
        "high_latency",
    }
    local_fallback = provider_frame.usage.fallback_used or pressure is PressureLevel.CRITICAL
    retrieval_only = local_fallback and pressure in {PressureLevel.HIGH, PressureLevel.CRITICAL}
    summary_only = (
        retrieval_only and request.compressed_context_tokens < request.retrieval_context_tokens
    )
    patch_only = enforcement.patch_only_enforced
    chain = [request.provider_name]
    if tier2_disabled:
        chain.append("tier2_disabled")
    if tier1_degraded:
        chain.append("tier1_degraded")
    if local_fallback:
        chain.append("local_fallback")
    if retrieval_only:
        chain.append("retrieval_only")
    if summary_only:
        chain.append("summary_only")
    if patch_only:
        chain.append("patch_only")
    return FallbackSimulationFrame(
        pressure=pressure.value,
        tier2_disabled=tier2_disabled,
        tier1_degraded=tier1_degraded,
        local_fallback=local_fallback,
        retrieval_only_fallback=retrieval_only,
        summary_only_fallback=summary_only,
        patch_only_fallback=patch_only,
        route_chain=tuple(chain),
        provider_frame=provider_frame,
    )
