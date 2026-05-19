from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.providers.provider_contracts import ProviderRequest

TIER_MULTIPLIER = {"tier0": 0.000_001, "tier1": 0.000_01, "tier2": 0.000_08}


@dataclass(frozen=True)
class CostSimulationFrame:
    before_retrieval_scaling: int
    after_retrieval_scaling: int
    prompt_tokens: int
    completion_tokens: int
    tier_multiplier: float
    fallback_penalty: float
    retry_penalty: float
    estimated_before_cost: float
    estimated_after_cost: float
    estimated_savings_ratio: float
    token_burn_avoided: int


def simulate_cost(
    request: ProviderRequest,
    *,
    fallback_used: bool = False,
    retry_count: int = 0,
) -> CostSimulationFrame:
    if request.prompt_tokens < 0 or request.completion_tokens < 0:
        raise ValueError("tokens must be non-negative")
    before_tokens = (
        request.retrieval_context_tokens + request.prompt_tokens + request.completion_tokens
    )
    after_tokens = (
        request.compressed_context_tokens + request.prompt_tokens + request.completion_tokens
    )
    multiplier = TIER_MULTIPLIER.get(request.model_tier, TIER_MULTIPLIER["tier1"])
    fallback_penalty = 1.10 if fallback_used else 1.0
    retry_penalty = 1.0 + (max(0, retry_count) * 0.15)
    before_cost = before_tokens * multiplier * retry_penalty
    after_cost = after_tokens * multiplier * fallback_penalty
    savings = 1.0 - (after_cost / before_cost if before_cost else 0.0)
    return CostSimulationFrame(
        before_retrieval_scaling=before_tokens,
        after_retrieval_scaling=after_tokens,
        prompt_tokens=request.prompt_tokens,
        completion_tokens=request.completion_tokens,
        tier_multiplier=multiplier,
        fallback_penalty=fallback_penalty,
        retry_penalty=retry_penalty,
        estimated_before_cost=round(before_cost, 8),
        estimated_after_cost=round(after_cost, 8),
        estimated_savings_ratio=round(savings, 6),
        token_burn_avoided=max(0, before_tokens - after_tokens),
    )
