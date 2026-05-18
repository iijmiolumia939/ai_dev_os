from __future__ import annotations

from dataclasses import dataclass

from governance.budget_runtime import BudgetEnforcement
from governance.model_tiers import ModelTier


@dataclass(frozen=True)
class ProviderModel:
    provider: str
    model: str
    tier: ModelTier
    expensive: bool = False


@dataclass(frozen=True)
class LiteLLMRoute:
    provider: str
    model: str
    tier: ModelTier
    fallback_chain: tuple[str, ...]
    warnings: tuple[str, ...]


DEFAULT_MODELS = (
    ProviderModel("local", "local-small", ModelTier.TIER0),
    ProviderModel("openrouter", "cheap-fast", ModelTier.TIER0),
    ProviderModel("anthropic", "claude-sonnet-class", ModelTier.TIER1),
    ProviderModel("openai-compatible", "gpt-5.5", ModelTier.TIER2, expensive=True),
)


class LiteLLMBridge:
    def __init__(self, models: tuple[ProviderModel, ...] = DEFAULT_MODELS) -> None:
        self.models = models

    def route(self, requested_tier: ModelTier, budget: BudgetEnforcement) -> LiteLLMRoute:
        target_tier = requested_tier
        warnings: list[str] = []
        if requested_tier is ModelTier.TIER2 and not budget.tier2_enabled:
            target_tier = ModelTier.TIER1
            warnings.append("TIER2_DISABLED_BY_BUDGET")

        candidates = [model for model in self.models if model.tier is target_tier]
        if not candidates:
            candidates = [model for model in self.models if model.tier is ModelTier.TIER0]
            warnings.append("FALLBACK_TO_TIER0")

        selected = candidates[0]
        fallback_chain = tuple(
            model.model for model in self.models if model.tier.value <= selected.tier.value
        )
        return LiteLLMRoute(
            provider=selected.provider,
            model=selected.model,
            tier=selected.tier,
            fallback_chain=fallback_chain,
            warnings=tuple(warnings),
        )

    def complete(self, prompt: str, route: LiteLLMRoute) -> dict[str, str | int]:
        return {
            "provider": route.provider,
            "model": route.model,
            "prompt_size": len(prompt),
            "mode": "isolated_optional_litellm",
        }
