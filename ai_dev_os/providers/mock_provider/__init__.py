from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.providers.cost_simulation import simulate_cost
from ai_dev_os.providers.provider_contracts import (
    ProviderFailure,
    ProviderRequest,
    ProviderResponse,
    ProviderRouteDecision,
    ProviderStatus,
    ProviderUsage,
)

SCENARIO_STATUS = {
    "success": ProviderStatus.SUCCESS,
    "timeout": ProviderStatus.TIMEOUT,
    "rate_limit": ProviderStatus.RATE_LIMIT,
    "provider_error": ProviderStatus.PROVIDER_ERROR,
    "high_latency": ProviderStatus.HIGH_LATENCY,
    "cost_spike": ProviderStatus.COST_SPIKE,
    "degraded_response": ProviderStatus.DEGRADED_RESPONSE,
}
SCENARIO_LATENCY_MS = {
    "success": 120,
    "timeout": 5_000,
    "rate_limit": 350,
    "provider_error": 240,
    "high_latency": 2_500,
    "cost_spike": 180,
    "degraded_response": 300,
}
FAILURE_REASONS = {
    ProviderStatus.TIMEOUT: "PROVIDER_TIMEOUT",
    ProviderStatus.RATE_LIMIT: "PROVIDER_RATE_LIMIT",
    ProviderStatus.PROVIDER_ERROR: "PROVIDER_ERROR",
}


@dataclass(frozen=True)
class MockProviderFrame:
    request: ProviderRequest
    response: ProviderResponse
    usage: ProviderUsage
    simulated_latency_ms: int
    simulated_cost: float
    simulated_failure: ProviderFailure | None
    route_taken: ProviderRouteDecision
    no_real_provider_call: bool


def simulate_provider_request(request: ProviderRequest) -> MockProviderFrame:
    status = SCENARIO_STATUS.get(request.scenario, ProviderStatus.PROVIDER_ERROR)
    latency = SCENARIO_LATENCY_MS.get(request.scenario, 240)
    failure_reason = FAILURE_REASONS.get(status, "")
    fallback_used = status in {
        ProviderStatus.TIMEOUT,
        ProviderStatus.RATE_LIMIT,
        ProviderStatus.PROVIDER_ERROR,
    }
    cost_frame = simulate_cost(
        request,
        fallback_used=fallback_used,
        retry_count=1 if status is ProviderStatus.RATE_LIMIT else 0,
    )
    if status is ProviderStatus.COST_SPIKE:
        estimated_cost = round(cost_frame.estimated_after_cost * 2.5, 8)
    else:
        estimated_cost = cost_frame.estimated_after_cost
    content = "mock provider response"
    if status is ProviderStatus.DEGRADED_RESPONSE:
        content = "degraded mock response"
    if fallback_used:
        content = "fallback required"

    response = ProviderResponse(
        provider_name=request.provider_name,
        model_tier=request.model_tier,
        status=status.value,
        content=content,
        failure_reason=failure_reason,
        fallback_used=fallback_used,
    )
    usage = ProviderUsage(
        provider_name=request.provider_name,
        model_tier=request.model_tier,
        prompt_tokens=request.prompt_tokens,
        completion_tokens=request.completion_tokens,
        estimated_cost=estimated_cost,
        latency_ms=latency,
        fallback_used=fallback_used,
        retrieval_related_cost=round(
            request.compressed_context_tokens
            * cost_frame.tier_multiplier
            * cost_frame.fallback_penalty,
            8,
        ),
    )
    failure = (
        ProviderFailure(
            provider_name=request.provider_name,
            status=status.value,
            failure_reason=failure_reason,
            latency_ms=latency,
            fallback_used=True,
        )
        if fallback_used
        else None
    )
    route_taken = ProviderRouteDecision(
        provider_name=request.provider_name,
        model_tier=request.model_tier,
        status=status.value,
        failure_reason=failure_reason,
        fallback_used=fallback_used,
        route_taken=(
            (request.provider_name, "local_fallback")
            if fallback_used
            else (request.provider_name,)
        ),
    )
    return MockProviderFrame(
        request=request,
        response=response,
        usage=usage,
        simulated_latency_ms=latency,
        simulated_cost=estimated_cost,
        simulated_failure=failure,
        route_taken=route_taken,
        no_real_provider_call=True,
    )
