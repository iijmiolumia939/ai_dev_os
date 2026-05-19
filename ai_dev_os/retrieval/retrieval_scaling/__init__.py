from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.retrieval.hierarchical_retrieval import (
    HierarchicalRetrievalFrame,
    build_hierarchical_frame,
)
from ai_dev_os.retrieval.memory_tree import MemoryTreeNode, build_memory_tree
from governance.budget_runtime import (
    BudgetState,
    PressureLevel,
    enforcement_for_pressure,
    pressure_for_budget,
)
from governance.model_tiers import ModelTier
from retrieval.prune_context import estimate_tokens


@dataclass(frozen=True)
class RetrievalScalingFrame:
    retrieval_pressure: str
    memory_saturation: bool
    continuity_safe_retrieval: bool
    token_explosion_prevented: bool
    retrieval_decay: float
    tier_downgrade: bool
    additional_compaction: bool
    summary_only_mode: bool
    retrieval_fallback_mode: bool
    before_tokens: int
    after_tokens: int
    selected_tier: str
    hierarchical_frame: HierarchicalRetrievalFrame


def _pressure_for_tokens(tokens: int, max_tokens: int) -> PressureLevel:
    if tokens > max_tokens * 2:
        return PressureLevel.CRITICAL
    if tokens > max_tokens:
        return PressureLevel.HIGH
    if tokens > int(max_tokens * 0.7):
        return PressureLevel.WARNING
    return PressureLevel.INFO


def scale_retrieval(
    bundle: dict[str, object],
    memory_nodes: tuple[MemoryTreeNode, ...],
    *,
    budget_state: BudgetState,
    max_context_tokens: int = 8_000,
    max_tree_depth: int = 3,
) -> RetrievalScalingFrame:
    memory_tree = build_memory_tree(memory_nodes, max_depth=max_tree_depth)
    before_tokens = estimate_tokens(bundle)
    budget_pressure = pressure_for_budget(budget_state)
    token_pressure = _pressure_for_tokens(before_tokens, max_context_tokens)
    pressure = max(
        (budget_pressure, token_pressure), key=lambda item: list(PressureLevel).index(item)
    )
    enforcement = enforcement_for_pressure(pressure)
    effective_limit = min(max_context_tokens, enforcement.max_context_tokens)
    hierarchical_frame = build_hierarchical_frame(
        bundle,
        memory_tree,
        max_context_tokens=effective_limit,
        summary_token_budget=(
            80 if pressure in {PressureLevel.HIGH, PressureLevel.CRITICAL} else 160
        ),
    )
    after_tokens = estimate_tokens(hierarchical_frame.compressed_context) + sum(
        estimate_tokens(layer) for layer in hierarchical_frame.summary_layers
    )
    memory_saturation = len(memory_nodes) > 12 or before_tokens > max_context_tokens
    tier_downgrade = not enforcement.tier2_enabled
    selected_tier = ModelTier.TIER1 if tier_downgrade else ModelTier.TIER0
    retrieval_decay = 0.75 if memory_saturation else 1.0
    return RetrievalScalingFrame(
        retrieval_pressure=pressure.value,
        memory_saturation=memory_saturation,
        continuity_safe_retrieval=hierarchical_frame.continuity_weight > 0,
        token_explosion_prevented=after_tokens <= before_tokens
        and after_tokens <= effective_limit,
        retrieval_decay=retrieval_decay,
        tier_downgrade=tier_downgrade,
        additional_compaction=pressure in {PressureLevel.HIGH, PressureLevel.CRITICAL},
        summary_only_mode=hierarchical_frame.compaction_report.summary_only_mode,
        retrieval_fallback_mode=pressure is PressureLevel.CRITICAL,
        before_tokens=before_tokens,
        after_tokens=after_tokens,
        selected_tier=selected_tier.value,
        hierarchical_frame=hierarchical_frame,
    )
