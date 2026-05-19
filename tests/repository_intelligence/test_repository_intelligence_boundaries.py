from __future__ import annotations

import subprocess
from pathlib import Path


def test_no_network_dependency_required() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "repository_intelligence").rglob("*.py"))
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)


def test_no_repository_mutation_from_cli_repo_intel() -> None:
    root = Path(__file__).resolve().parents[2]
    before = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()
    subprocess.run(
        ("python", "-m", "ai_dev_os.cli", "repo-intel", "--repo-path", ".", "--json"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    after = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()

    assert before == after


def test_no_generated_artifact_committed() -> None:
    root = Path(__file__).resolve().parents[2]
    artifacts = [
        path
        for pattern in ("*repo_intel*.json", "*repository_intelligence*.log", "task_output.json")
        for path in root.rglob(pattern)
    ]

    assert artifacts == []
