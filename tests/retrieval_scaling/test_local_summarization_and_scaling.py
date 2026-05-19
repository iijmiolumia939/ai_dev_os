from __future__ import annotations

import pytest

from ai_dev_os.retrieval.local_summarization import summarize_locally
from ai_dev_os.retrieval.memory_tree import MemoryTreeNode
from ai_dev_os.retrieval.retrieval_scaling import scale_retrieval
from governance.budget_runtime import BudgetState
from governance.model_tiers import ModelTier


def scaling_bundle() -> dict[str, object]:
    return {
        "active_requirements": ["FR-RETRIEVAL-05"],
        "changed_files": ["ai_dev_os/retrieval/retrieval_scaling/__init__.py"],
        "active_artifacts": ["continuity-policy"],
        "entries": [{"path": f"memory/{index}.md", "score": index} for index in range(40)],
        "policy": "bounded continuity",
        "stale_sprint_history": "stale " * 14_000,
        "inactive_adr": "inactive " * 8_000,
        "obsolete_open_questions": "obsolete " * 8_000,
        "giant_markdown": "markdown " * 14_000,
        "unrelated_summaries": "summary " * 6_000,
    }


def continuity_nodes(count: int = 14) -> tuple[MemoryTreeNode, ...]:
    return tuple(
        MemoryTreeNode(
            kind="checkpoint_summary" if index % 2 else "architecture_summary",
            title=f"continuity-{index:02d}",
            summary=f"bounded continuity summary {index}",
            priority=index,
            continuity_weight=1.0 - (index * 0.03),
        )
        for index in range(count)
    )


def test_local_summarization_is_bounded_and_tier_aware() -> None:
    frame = summarize_locally("token " * 1_000, tier=ModelTier.TIER0, token_budget=40)

    assert frame.local_preferred is True
    assert frame.budget_enforced is True
    assert frame.summary_tokens <= 40
    with pytest.raises(ValueError, match="Tier2 summarization is forbidden"):
        summarize_locally("expensive", tier=ModelTier.TIER2)


def test_retrieval_scaling_prevents_token_explosion_and_preserves_continuity() -> None:
    frame = scale_retrieval(
        scaling_bundle(),
        continuity_nodes(),
        budget_state=BudgetState(100.0, 500.0, 1500.0, daily_spend=96.0),
        max_context_tokens=4_000,
    )

    assert frame.retrieval_pressure in {"HIGH", "CRITICAL"}
    assert frame.memory_saturation is True
    assert frame.continuity_safe_retrieval is True
    assert frame.token_explosion_prevented is True
    assert frame.tier_downgrade is True
    assert frame.additional_compaction is True
    assert frame.retrieval_fallback_mode is True
    assert frame.after_tokens < frame.before_tokens


def test_retrieval_scaling_is_deterministic() -> None:
    first = scale_retrieval(
        scaling_bundle(),
        continuity_nodes(),
        budget_state=BudgetState(100.0, 500.0, 1500.0, daily_spend=96.0),
        max_context_tokens=4_000,
    )
    second = scale_retrieval(
        scaling_bundle(),
        continuity_nodes(),
        budget_state=BudgetState(100.0, 500.0, 1500.0, daily_spend=96.0),
        max_context_tokens=4_000,
    )

    assert first == second
