from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProviderStatus(StrEnum):
    SUCCESS = "success"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    PROVIDER_ERROR = "provider_error"
    HIGH_LATENCY = "high_latency"
    COST_SPIKE = "cost_spike"
    DEGRADED_RESPONSE = "degraded_response"
    FALLBACK = "fallback"


@dataclass(frozen=True)
class ProviderRequest:
    provider_name: str
    model_tier: str
    prompt_tokens: int
    completion_tokens: int = 0
    retrieval_context_tokens: int = 0
    compressed_context_tokens: int = 0
    scenario: str = "success"


@dataclass(frozen=True)
class ProviderUsage:
    provider_name: str
    model_tier: str
    prompt_tokens: int
    completion_tokens: int
    estimated_cost: float
    latency_ms: int
    fallback_used: bool = False
    retrieval_related_cost: float = 0.0


@dataclass(frozen=True)
class ProviderFailure:
    provider_name: str
    status: str
    failure_reason: str
    latency_ms: int
    fallback_used: bool


@dataclass(frozen=True)
class ProviderResponse:
    provider_name: str
    model_tier: str
    status: str
    content: str
    failure_reason: str = ""
    fallback_used: bool = False


@dataclass(frozen=True)
class ProviderRouteDecision:
    provider_name: str
    model_tier: str
    status: str
    failure_reason: str
    fallback_used: bool
    route_taken: tuple[str, ...]
