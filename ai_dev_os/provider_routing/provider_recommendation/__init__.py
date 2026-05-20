from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderRecommendationFrame:
    recommended_provider: str
    recommended_provider_class: str
    gpt55_only_when_required: bool
    claude_for_medium_recommendation: bool
    gemini_for_low_recommendation: bool
    compact_implementation_routing: bool
    premium_provider_preservation_recommendation: bool
    no_automatic_provider_execution: bool
    no_hidden_escalation: bool
    summary_only: bool
    deterministic: bool


class ProviderRecommendationPolicy:
    def recommend(
        self,
        *,
        cognition_tier: str,
        architecture_required: bool = False,
        compact_implementation: bool = False,
        preserve_premium: bool = True,
    ) -> ProviderRecommendationFrame:
        normalized = cognition_tier.upper()
        if compact_implementation or normalized == "LOW":
            provider = "Gemini-class low provider"
            provider_class = "LOW"
        elif normalized == "MEDIUM" or not architecture_required:
            provider = "Claude-class medium provider"
            provider_class = "MEDIUM"
        else:
            provider = "GPT-5.5 premium provider"
            provider_class = "HIGH"
        premium_preserved = preserve_premium and provider_class != "HIGH"
        return ProviderRecommendationFrame(
            recommended_provider=provider,
            recommended_provider_class=provider_class,
            gpt55_only_when_required=provider_class != "HIGH" or architecture_required,
            claude_for_medium_recommendation=provider_class == "MEDIUM",
            gemini_for_low_recommendation=provider_class == "LOW",
            compact_implementation_routing=compact_implementation and provider_class == "LOW",
            premium_provider_preservation_recommendation=premium_preserved,
            no_automatic_provider_execution=True,
            no_hidden_escalation=True,
            summary_only=True,
            deterministic=True,
        )
