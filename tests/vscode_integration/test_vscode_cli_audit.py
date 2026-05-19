from __future__ import annotations

import json
import subprocess
import sys

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_handoff_session_cli_json_mode() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "handoff-session",
            "--workspace",
            ".",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["recommended_new_session"] is True
    assert data["full_history_included"] is False
    assert data["continuity_bundle"]["repository_subset"]


def test_export_prompt_cli_copy_ready_mode() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "export-prompt",
            "--workspace",
            ".",
            "--copy-ready",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "AI_DEV_OS Session Handoff" in completed.stdout
    assert "Do not replay full history" in completed.stdout
    assert "full transcript" not in completed.stdout.lower()


def test_vscode_state_cli_json_mode() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "vscode-state", "--workspace", ".", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["network_used"] is False
    assert data["telemetry_collected"] is False
    assert data["export_availability"] is True


def test_runtime_audit_reports_vscode_integration() -> None:
    report = run_runtime_enforcement_audit()

    assert report.vscode_integration.session_handoff_active is True
    assert report.vscode_integration.prompt_export_active is True
    assert report.vscode_integration.clipboard_runtime_active is True
    assert report.vscode_integration.handoff_notifications_active is True
    assert report.vscode_integration.ide_state_runtime_active is True
    assert report.vscode_integration.estimated_avoided_manual_rollover_tokens > 0
    assert report.vscode_integration.estimated_avoided_stale_continuation_tokens >= 0
