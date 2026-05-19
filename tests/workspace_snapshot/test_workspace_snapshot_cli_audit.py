from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_cli_workspace_snapshot_json_mode() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "workspace-snapshot",
            "--workspace",
            ".",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["workspace_state"]["read_only"] is True
    assert data["multi_repository"]["bounded"] is True
    assert data["rollout_tracking"]["rollout_stage"]
    assert data["architecture_hotspots"]["risk_severity"]


def test_cli_copy_ready_mode_for_workspace_snapshot() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "workspace-snapshot",
            "--workspace",
            ".",
            "--copy-ready",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "workspace_state:" in completed.stdout
    assert "multi_repository:" in completed.stdout
    assert "full repository" not in completed.stdout.lower()


def test_runtime_audit_reports_workspace_snapshot() -> None:
    report = run_runtime_enforcement_audit()

    assert report.workspace_snapshot.workspace_snapshot_active is True
    assert report.workspace_snapshot.multi_repository_continuity_active is True
    assert report.workspace_snapshot.rollout_tracking_active is True
    assert report.workspace_snapshot.known_failure_baseline_active is True
    assert report.workspace_snapshot.architecture_hotspot_detection_active is True
    assert report.workspace_snapshot.estimated_avoided_manual_workspace_context > 0
    assert report.workspace_snapshot.consumer_repository_coverage >= 0.0


def test_no_repository_mutation_from_workspace_snapshot_cli() -> None:
    root = Path(__file__).resolve().parents[2]
    before = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()
    subprocess.run(
        (
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "workspace-snapshot",
            "--workspace",
            ".",
            "--json",
        ),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    after = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()

    assert before == after
