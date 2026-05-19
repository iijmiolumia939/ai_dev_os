from __future__ import annotations

from pathlib import Path


def test_no_network_dependency_required() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "workspace_snapshot").rglob("*.py"))
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)


def test_no_full_repository_indexing_or_tree_export() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "workspace_snapshot").rglob("*.py"))
    forbidden_snippets = ("rglob('*')", 'rglob("*")', "os.walk", "full file tree")

    for path in files:
        text = path.read_text(encoding="utf-8")
        assert all(snippet not in text for snippet in forbidden_snippets)


def test_no_generated_workspace_snapshot_artifacts_committed() -> None:
    root = Path(__file__).resolve().parents[2]
    artifacts = [
        path
        for pattern in ("*workspace_snapshot*.json", "*workspace-snapshot*.log")
        for path in root.rglob(pattern)
    ]

    assert artifacts == []
