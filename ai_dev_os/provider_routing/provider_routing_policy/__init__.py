from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderRoutingFrame:
    recommended_provider_class: str
    routing_reason: str
    architecture_isolation_routing: bool
    local_patch_routing: bool
    hidden_provider_switching: bool
    automatic_provider_execution: bool
    human_visible_recommendation: bool
    deterministic: bool
    summary_only: bool


class ProviderRoutingPolicy:
    def route(
        self,
        *,
        cognition_tier: str,
        architecture_isolation: bool = False,
        local_patch: bool = False,
        compact_summary: bool = False,
    ) -> ProviderRoutingFrame:
        normalized = cognition_tier.upper()
        if local_patch or compact_summary or normalized == "LOW":
            recommended = "LOW"
            reason = "cheap_provider_for_local_or_compact_work"
        elif normalized == "MEDIUM":
            recommended = "MEDIUM"
            reason = "balanced_provider_for_bounded_implementation"
        else:
            recommended = "HIGH"
            reason = "premium_provider_for_required_high_cognition"
        if architecture_isolation and normalized == "HIGH" and not local_patch:
            reason = "architecture_isolation_requires_visible_premium_review"
        return ProviderRoutingFrame(
            recommended_provider_class=recommended,
            routing_reason=reason,
            architecture_isolation_routing=architecture_isolation,
            local_patch_routing=local_patch,
            hidden_provider_switching=False,
            automatic_provider_execution=False,
            human_visible_recommendation=True,
            deterministic=True,
            summary_only=True,
        )
