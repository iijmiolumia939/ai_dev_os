from __future__ import annotations

import json
import subprocess
import sys

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_cli_json_mode() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "session-mode", "--workspace", ".", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["recommended_mode"]
    assert data["fallback_mode"] == "bounded_implementation"
    assert data["compact_mode"] is True


def test_cli_copy_ready_mode() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "reasoning-profile",
            "--workspace",
            ".",
            "--copy-ready",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "reasoning_depth:" in completed.stdout
    assert "retrieval_budget:" in completed.stdout
    assert "unrestricted" not in completed.stdout.lower()


def test_prompt_pack_copy_ready_contains_mode_controls() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "prompt-pack",
            "--project",
            "ai_dev_os",
            "--sprint",
            "42",
            "--copy-ready",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Prompt shape:" in completed.stdout
    assert "Continuity depth:" in completed.stdout
    assert "Architecture allowance:" in completed.stdout
    assert "Retrieval budget:" in completed.stdout


def test_runtime_audit_reports_prompt_modes() -> None:
    report = run_runtime_enforcement_audit()

    assert report.prompt_modes.reasoning_profile_active is True
    assert report.prompt_modes.prompt_shape_active is True
    assert report.prompt_modes.review_intensity_active is True
    assert report.prompt_modes.context_depth_active is True
    assert report.prompt_modes.session_mode_router_active is True
    assert report.prompt_modes.estimated_avoided_reasoning_token_burn > 0
    assert report.prompt_modes.estimated_avoided_architecture_escalation >= 0
