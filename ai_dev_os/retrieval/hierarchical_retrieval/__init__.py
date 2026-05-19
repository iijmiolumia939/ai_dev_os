from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.retrieval.context_compaction import CompactionReport, compact_context
from ai_dev_os.retrieval.local_summarization import summarize_locally
from ai_dev_os.retrieval.memory_tree import MemoryTreeNode, retrieve_memory_path
from governance.model_tiers import ModelTier
from retrieval.prune_context import estimate_tokens


@dataclass(frozen=True)
class HierarchicalRetrievalFrame:
    active_context: dict[str, object]
    compressed_context: dict[str, object]
    summary_layers: tuple[str, ...]
    retrieval_priority: int
    continuity_weight: float
    compaction_report: CompactionReport


def build_hierarchical_frame(
    bundle: dict[str, object],
    memory_tree: tuple[MemoryTreeNode, ...],
    *,
    max_context_tokens: int = 8_000,
    summary_token_budget: int = 160,
) -> HierarchicalRetrievalFrame:
    if "full_repository_context" in bundle:
        raise ValueError("full repository retrieval is forbidden")
    compressed, report = compact_context(bundle, max_tokens=max_context_tokens)
    continuity_nodes = retrieve_memory_path(memory_tree, limit=4)
    summaries = tuple(
        summarize_locally(
            node.summary, tier=ModelTier.TIER0, token_budget=summary_token_budget
        ).summary
        for node in continuity_nodes
    )
    continuity_weight = sum(node.continuity_weight for node in continuity_nodes)
    retrieval_priority = len(compressed.get("changed_files", ())) + len(
        compressed.get("entries", ())
    )
    active_context = {
        key: bundle[key]
        for key in bundle
        if key in {"active_requirements", "changed_files", "active_artifacts"}
    }
    return HierarchicalRetrievalFrame(
        active_context=active_context,
        compressed_context=compressed,
        summary_layers=summaries,
        retrieval_priority=retrieval_priority,
        continuity_weight=round(continuity_weight, 4),
        compaction_report=report,
    )


def frame_token_reduction(
    frame: HierarchicalRetrievalFrame, original_bundle: dict[str, object]
) -> float:
    before = estimate_tokens(original_bundle)
    after = estimate_tokens(frame.compressed_context) + sum(
        estimate_tokens(layer) for layer in frame.summary_layers
    )
    return 1.0 - (after / before if before else 0.0)
