from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardSnapshot:
    provider_usage: dict[str, int]
    routing_distribution: dict[str, int]
    retrieval_hit_rate: float
    fallback_frequency: int


def snapshot(records: list[dict[str, object]]) -> DashboardSnapshot:
    provider_usage: dict[str, int] = {}
    routing_distribution: dict[str, int] = {}
    for record in records:
        provider = str(record.get("provider", "unknown"))
        tier = str(record.get("model_tier", "unknown"))
        provider_usage[provider] = provider_usage.get(provider, 0) + 1
        routing_distribution[tier] = routing_distribution.get(tier, 0) + 1
    total = len(records) or 1
    return DashboardSnapshot(
        provider_usage=provider_usage,
        routing_distribution=routing_distribution,
        retrieval_hit_rate=sum(1 for record in records if record.get("retrieval_hit")) / total,
        fallback_frequency=sum(1 for record in records if record.get("fallback_used")),
    )
