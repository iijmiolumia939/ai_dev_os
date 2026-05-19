from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_cli_json_mode() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "context-subset", "--workspace", ".", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["repository_subset"]["summary_only"] is True
    assert data["continuity_scope"]["summary_only_required"] is True
    assert "full_workspace_continuation" in data["continuity_scope"]["excluded_context"]
    assert data["session_focus"]["recommended_session_type"]


def test_cli_copy_ready_mode() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "context-subset",
            "--workspace",
            ".",
            "--copy-ready",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "repository_subset:" in completed.stdout
    assert "continuity_scope:" in completed.stdout
    assert "giant continuity summary" not in completed.stdout.lower()


def test_runtime_audit_reports_context_subset() -> None:
    report = run_runtime_enforcement_audit()

    assert report.context_subset.repository_subset_active is True
    assert report.context_subset.topic_isolation_active is True
    assert report.context_subset.continuity_scope_active is True
    assert report.context_subset.stale_topic_eviction_active is True
    assert report.context_subset.session_focus_governance_active is True
    assert report.context_subset.estimated_avoided_stale_context_tokens > 0
    assert report.context_subset.estimated_avoided_architecture_drift_tokens >= 0


def test_no_workspace_mutation_from_cli() -> None:
    root = Path(__file__).resolve().parents[2]
    before = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()
    subprocess.run(
        (sys.executable, "-m", "ai_dev_os.cli", "context-subset", "--workspace", ".", "--json"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    after = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()

    assert before == after
