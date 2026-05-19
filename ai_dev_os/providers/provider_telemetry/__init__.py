from __future__ import annotations

from dataclasses import asdict, dataclass

from ai_dev_os.providers.mock_provider import MockProviderFrame


@dataclass(frozen=True)
class ProviderTelemetryFrame:
    provider_usage_count: dict[str, int]
    tier_usage_distribution: dict[str, int]
    token_burn_estimate: int
    cost_estimate: float
    latency_distribution: dict[str, int]
    fallback_frequency: int
    failure_frequency: int
    retrieval_related_cost: float
    machine_readable_summary: dict[str, object]


def aggregate_provider_telemetry(frames: tuple[MockProviderFrame, ...]) -> ProviderTelemetryFrame:
    provider_usage: dict[str, int] = {}
    tier_distribution: dict[str, int] = {}
    latency_distribution = {"fast": 0, "normal": 0, "slow": 0}
    token_burn = 0
    cost = 0.0
    retrieval_cost = 0.0
    fallback_frequency = 0
    failure_frequency = 0
    for frame in frames:
        usage = frame.usage
        provider_usage[usage.provider_name] = provider_usage.get(usage.provider_name, 0) + 1
        tier_distribution[usage.model_tier] = tier_distribution.get(usage.model_tier, 0) + 1
        token_burn += usage.prompt_tokens + usage.completion_tokens
        cost += usage.estimated_cost
        retrieval_cost += usage.retrieval_related_cost
        fallback_frequency += int(usage.fallback_used)
        failure_frequency += int(frame.simulated_failure is not None)
        if usage.latency_ms < 250:
            latency_distribution["fast"] += 1
        elif usage.latency_ms < 1_000:
            latency_distribution["normal"] += 1
        else:
            latency_distribution["slow"] += 1

    summary = {
        "provider_usage_count": provider_usage,
        "tier_usage_distribution": tier_distribution,
        "token_burn_estimate": token_burn,
        "cost_estimate": round(cost, 8),
        "fallback_frequency": fallback_frequency,
        "failure_frequency": failure_frequency,
        "retrieval_related_cost": round(retrieval_cost, 8),
        "frames": [asdict(frame.response) for frame in frames],
    }
    return ProviderTelemetryFrame(
        provider_usage_count=provider_usage,
        tier_usage_distribution=tier_distribution,
        token_burn_estimate=token_burn,
        cost_estimate=round(cost, 8),
        latency_distribution=latency_distribution,
        fallback_frequency=fallback_frequency,
        failure_frequency=failure_frequency,
        retrieval_related_cost=round(retrieval_cost, 8),
        machine_readable_summary=summary,
    )
