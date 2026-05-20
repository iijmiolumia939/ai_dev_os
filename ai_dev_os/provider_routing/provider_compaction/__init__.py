from __future__ import annotations

from dataclasses import dataclass


def _deduplicate(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


@dataclass(frozen=True)
class ProviderCompactionFrame:
    compact_provider_routing_summaries: tuple[str, ...]
    compact_escalation_reasons: tuple[str, ...]
    deduplicated_provider_recommendations: tuple[str, ...]
    expandable_provider_details: tuple[str, ...]
    summary_only: bool
    deterministic: bool


class ProviderCompactionPolicy:
    def compact(
        self,
        *,
        routing_summaries: tuple[str, ...],
        escalation_reasons: tuple[str, ...],
        provider_recommendations: tuple[str, ...],
        provider_details: tuple[str, ...] = (),
    ) -> ProviderCompactionFrame:
        return ProviderCompactionFrame(
            compact_provider_routing_summaries=_deduplicate(routing_summaries)[:6],
            compact_escalation_reasons=_deduplicate(escalation_reasons)[:4],
            deduplicated_provider_recommendations=_deduplicate(provider_recommendations)[:6],
            expandable_provider_details=_deduplicate(provider_details)[:8],
            summary_only=True,
            deterministic=True,
        )
