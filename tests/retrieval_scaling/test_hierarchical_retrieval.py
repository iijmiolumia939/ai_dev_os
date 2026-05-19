from __future__ import annotations

import pytest

from ai_dev_os.retrieval.hierarchical_retrieval import (
    build_hierarchical_frame,
    frame_token_reduction,
)
from ai_dev_os.retrieval.memory_tree import MemoryTreeNode, build_memory_tree


def large_bundle() -> dict[str, object]:
    return {
        "active_requirements": ["FR-RETRIEVAL-01", "NFR-COST-02"],
        "changed_files": ["ai_dev_os/retrieval/hierarchical_retrieval/__init__.py"],
        "active_artifacts": ["retrieval-scaling-guide"],
        "entries": [{"path": f"docs/retrieval-{index}.md", "score": index} for index in range(24)],
        "policy": {"mode": "retrieval-first"},
        "stale_sprint_history": "stale sprint " * 10_000,
        "inactive_adr": "inactive adr " * 5_000,
        "obsolete_open_questions": "obsolete oq " * 5_000,
        "giant_markdown": "markdown block " * 10_000,
        "duplicate_contexts": ["docs/retrieval-1.md", "docs/retrieval-1.md"],
    }


def memory_tree() -> tuple[MemoryTreeNode, ...]:
    return build_memory_tree(
        (
            MemoryTreeNode(
                kind="architecture_summary",
                title="retrieval architecture",
                summary="retrieval-first compression keeps active architecture context",
                priority=10,
                continuity_weight=0.9,
            ),
            MemoryTreeNode(
                kind="checkpoint_summary",
                title="latest checkpoint",
                summary="continuity is preserved through bounded checkpoint summaries",
                priority=8,
                continuity_weight=0.7,
            ),
        )
    )


def test_hierarchical_retrieval_reduces_tokens_and_preserves_active_context() -> None:
    bundle = large_bundle()
    frame = build_hierarchical_frame(bundle, memory_tree(), max_context_tokens=4_000)

    assert frame.active_context["active_requirements"] == ["FR-RETRIEVAL-01", "NFR-COST-02"]
    assert frame.compaction_report.active_artifacts_preserved is True
    assert frame.compaction_report.after_tokens < frame.compaction_report.before_tokens
    assert frame_token_reduction(frame, bundle) > 0.95
    assert len(frame.summary_layers) == 2


def test_full_repository_retrieval_is_forbidden() -> None:
    bundle = large_bundle() | {"full_repository_context": "forbidden"}

    with pytest.raises(ValueError, match="full repository retrieval is forbidden"):
        build_hierarchical_frame(bundle, memory_tree())
