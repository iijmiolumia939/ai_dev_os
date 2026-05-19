from __future__ import annotations

import pytest

from ai_dev_os.retrieval.context_compaction import compact_context
from ai_dev_os.retrieval.memory_tree import MemoryTreeNode, build_memory_tree, retrieve_memory_path


def test_memory_tree_is_bounded_and_continuity_ranked() -> None:
    tree = build_memory_tree(
        (
            MemoryTreeNode(
                kind="sprint_summary",
                title="current sprint",
                summary="active retrieval implementation",
                priority=5,
                continuity_weight=0.4,
            ),
            MemoryTreeNode(
                kind="adr_summary",
                title="retrieval architecture decision",
                summary="bounded memory tree keeps summaries only",
                priority=8,
                continuity_weight=0.8,
            ),
            MemoryTreeNode(
                kind="stale_branch_summary",
                title="old branch",
                summary="stale summary retained only when explicitly requested",
                priority=1,
                continuity_weight=0.1,
                stale=True,
            ),
        ),
        max_depth=2,
    )
    path = retrieve_memory_path(tree, limit=2)

    assert [node.title for node in path] == ["retrieval architecture decision", "current sprint"]
    assert all(not node.stale for node in path)


def test_memory_tree_rejects_unbounded_depth_and_raw_replay() -> None:
    too_deep = MemoryTreeNode(
        kind="architecture_summary",
        title="root",
        summary="root summary",
        children=(
            MemoryTreeNode(
                kind="checkpoint_summary",
                title="child",
                summary="child summary",
                children=(
                    MemoryTreeNode(
                        kind="sprint_summary",
                        title="grandchild",
                        summary="grandchild summary",
                    ),
                ),
            ),
        ),
    )

    with pytest.raises(ValueError, match="depth exceeds"):
        build_memory_tree((too_deep,), max_depth=2)
    with pytest.raises(ValueError, match="summary is required"):
        build_memory_tree((MemoryTreeNode(kind="sprint_summary", title="raw", summary=""),))


def test_context_compaction_prunes_stale_and_duplicates() -> None:
    bundle = {
        "active_requirements": ["FR-RETRIEVAL-02"],
        "changed_files": ["file-a.py"],
        "active_artifacts": ["active-design"],
        "entries": [{"path": "file-a.py"}, {"path": "file-a.py"}, {"path": "file-b.py"}],
        "policy": "minimal retrieval",
        "stale_sprint_history": "stale " * 2_000,
        "inactive_adr": "inactive " * 2_000,
        "obsolete_open_questions": "obsolete " * 2_000,
        "giant_markdown": "markdown " * 2_000,
    }
    compacted, report = compact_context(bundle, max_tokens=1_000)

    assert report.after_tokens < report.before_tokens
    assert "stale_sprint_history" in report.removed_keys
    assert "inactive_adr" in report.removed_keys
    assert "obsolete_open_questions" in report.removed_keys
    assert report.duplicate_context_suppressed is True
    assert report.active_artifacts_preserved is True
    assert compacted["entries"] == [{"path": "file-a.py"}, {"path": "file-b.py"}]
