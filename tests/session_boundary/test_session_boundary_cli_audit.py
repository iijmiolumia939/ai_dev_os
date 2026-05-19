from __future__ import annotations

import json
import subprocess
import sys

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_session_boundary_handoff_cli_exports_bounded_generation_metadata() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "session-boundary-handoff",
            "--workspace",
            ".",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["session_generation"]["full_history_replay_allowed"] is False
    assert data["boundary_enforcement"]["ai_response_blocking_enforced"] is False
    assert data["compact_continuity_bundle"]["bounded"] is True
    assert "session_generation_metadata" in data["compact_continuity_bundle"]["compact_bundle"]


def test_session_boundary_runtime_audit_section() -> None:
    report = run_runtime_enforcement_audit()

    assert report.session_boundary.session_boundary_active is True
    assert report.session_boundary.stale_session_detection_active is True
    assert report.session_boundary.rollover_state_active is True
    assert report.session_boundary.handoff_confirmation_active is True
    assert report.session_boundary.vscode_extension_active is True
    assert report.session_boundary.estimated_avoided_stale_continuation_tokens > 0
    assert report.session_boundary.estimated_avoided_hidden_context_drift > 0
