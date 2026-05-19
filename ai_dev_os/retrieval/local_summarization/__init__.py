from __future__ import annotations

from dataclasses import dataclass

from governance.model_tiers import ModelTier
from retrieval.prune_context import estimate_tokens


@dataclass(frozen=True)
class SummaryFrame:
    summary: str
    source_tokens: int
    summary_tokens: int
    tier: str
    local_preferred: bool
    budget_enforced: bool


def summarize_locally(
    text: str,
    *,
    tier: ModelTier = ModelTier.TIER0,
    token_budget: int = 160,
) -> SummaryFrame:
    if tier is ModelTier.TIER2:
        raise ValueError("Tier2 summarization is forbidden for routine compression")
    if token_budget <= 0:
        raise ValueError("summary token budget must be positive")

    words = text.replace("\n", " ").split()
    budgeted_words = words[: max(1, token_budget * 4 // 5)]
    summary = " ".join(budgeted_words)
    if len(words) > len(budgeted_words):
        summary = f"{summary} ..."
    while estimate_tokens(summary) > token_budget and len(budgeted_words) > 1:
        budgeted_words = budgeted_words[:-1]
        summary = f"{' '.join(budgeted_words)} ..."
    if not summary:
        summary = "empty"
    return SummaryFrame(
        summary=summary,
        source_tokens=estimate_tokens(text),
        summary_tokens=estimate_tokens(summary),
        tier=tier.value,
        local_preferred=True,
        budget_enforced=estimate_tokens(summary) <= token_budget,
    )
