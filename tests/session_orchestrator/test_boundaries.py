from __future__ import annotations

from pathlib import Path


def test_session_orchestrator_has_no_network_dependency() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "session_orchestrator").rglob("*.py")) + [
        root / "ai_dev_os" / "cli.py"
    ]
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)


def test_no_generated_artifact_committed() -> None:
    root = Path(__file__).resolve().parents[2]
    patterns = (
        "*session_orchestrator*.json",
        "*session_orchestrator*.log",
        "*session_cli*.json",
        "task_output.json",
    )
    artifacts = [path for pattern in patterns for path in root.rglob(pattern)]

    assert artifacts == []
