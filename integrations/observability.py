from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationUsageSample:
    provider: str
    model_tier: str
    tokens: int = 0
    cost: float = 0.0
    retrieval_hit: bool = False
    fallback_used: bool = False
    expensive_model: bool = False


@dataclass(frozen=True)
class IntegrationUsageReport:
    provider_usage: dict[str, int]
    routing_distribution: dict[str, int]
    expensive_model_ratio: float
    retrieval_hit_rate: float
    token_total: int
    cost_total: float
    fallback_frequency: int


def aggregate_usage(samples: list[IntegrationUsageSample]) -> IntegrationUsageReport:
    provider_usage: dict[str, int] = {}
    routing_distribution: dict[str, int] = {}
    for sample in samples:
        provider_usage[sample.provider] = provider_usage.get(sample.provider, 0) + 1
        routing_distribution[sample.model_tier] = (
            routing_distribution.get(sample.model_tier, 0) + 1
        )
    total = len(samples) or 1
    return IntegrationUsageReport(
        provider_usage=provider_usage,
        routing_distribution=routing_distribution,
        expensive_model_ratio=sum(1 for sample in samples if sample.expensive_model) / total,
        retrieval_hit_rate=sum(1 for sample in samples if sample.retrieval_hit) / total,
        token_total=sum(sample.tokens for sample in samples),
        cost_total=sum(sample.cost for sample in samples),
        fallback_frequency=sum(1 for sample in samples if sample.fallback_used),
    )
