from __future__ import annotations

import json
import subprocess
import sys

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_workspace_persistence_cli_restore_json() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "restore-session-state",
            "--workspace",
            ".",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["restore_available"] is True
    assert data["stale_persistence_auto_applied"] is False
    assert data["recommended_action"] in {"confirm_human_rollover", "restore_bounded_state"}


def test_workspace_persistence_runtime_audit_section() -> None:
    report = run_runtime_enforcement_audit()

    assert report.workspace_persistence.persistence_store_active is True
    assert report.workspace_persistence.session_restore_active is True
    assert report.workspace_persistence.continuity_index_active is True
    assert report.workspace_persistence.persistence_cleanup_active is True
    assert report.workspace_persistence.local_workspace_persistence_active is True
    assert report.workspace_persistence.estimated_avoided_manual_recovery_tokens > 0
    assert report.workspace_persistence.estimated_avoided_stale_persistence_tokens > 0
