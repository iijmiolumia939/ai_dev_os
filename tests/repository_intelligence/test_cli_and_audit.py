from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_cli_repo_intel_json_mode_works() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "repo-intel", "--repo-path", ".", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["git"]["read_only"] is True
    assert data["runtime_discovery"]["runtime_packages"]
    assert data["ci_context"]["latest_workflow_name"] == "CI"


def test_cli_copy_ready_mode_works_for_continuity_export() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "continuity-export",
            "--project",
            "aituber",
            "--copy-ready",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Sprint boundary:" in completed.stdout
    assert "full_history" in completed.stdout
    assert "history history" not in completed.stdout


def test_cli_sprint_import_json_mode(tmp_path: Path) -> None:
    sprint_file = tmp_path / "sprint.yml"
    sprint_file.write_text(
        "sprint_id: 44\nactive_fr_tc: [FR-REPOINTEL-02, TC-REPOINTEL-02]\n",
        encoding="utf-8",
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "sprint-import",
            "--from-file",
            str(sprint_file),
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["sprint_id"] == "44"
    assert data["active_fr_tc"] == ["FR-REPOINTEL-02", "TC-REPOINTEL-02"]


def test_runtime_audit_reports_repository_intelligence() -> None:
    report = run_runtime_enforcement_audit()

    assert report.repository_intelligence.repository_intelligence_active is True
    assert report.repository_intelligence.git_collector_active is True
    assert report.repository_intelligence.runtime_discovery_active is True
    assert report.repository_intelligence.validation_collector_active is True
    assert report.repository_intelligence.ci_context_active is True
    assert report.repository_intelligence.automated_sprint_metadata_coverage == 1.0
    assert report.repository_intelligence.estimated_avoided_manual_context_tokens > 0
