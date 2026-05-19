from __future__ import annotations

from pathlib import Path


def test_no_network_dependency() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "context_subset").rglob("*.py"))
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)


def test_bounded_continuity_enforcement() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "context_subset").rglob("*.py"))
    forbidden_snippets = (
        "full_workspace_continuation_allowed",
        "giant_continuity_summary_allowed",
        "raw dump",
        "full file tree",
    )

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(snippet not in text for snippet in forbidden_snippets)


def test_no_generated_context_subset_artifacts() -> None:
    root = Path(__file__).resolve().parents[2]
    artifacts = [
        path
        for pattern in ("*context_subset*.json", "*context-subset*.log")
        for path in root.rglob(pattern)
    ]

    assert artifacts == []
