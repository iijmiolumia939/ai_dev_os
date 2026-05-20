from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os import __version__
from ai_dev_os.release_readiness import (
    ExtensionReadinessPolicy,
    GovernanceFreezeStatusPolicy,
    ReleaseReadinessPolicy,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

ROOT = Path(".")
EXTENSION = ROOT / "extensions" / "ai-dev-os-vscode"


def test_release_readiness_validation() -> None:
    frame = ReleaseReadinessPolicy().evaluate(ROOT)

    assert frame.release_version == "0.1.0a3"
    assert __version__ == "0.1.0a3"
    assert frame.github_prerelease_tag == "0.1.0-alpha.3"
    assert frame.release_ready is True
    assert frame.blocking_risks == ()
    assert frame.bounded_release_confirmed is True
    assert frame.consumer_safe is True
    assert frame.migration_ready is True
    assert frame.rollback_safe_release_prep is True
    assert frame.local_first_governance is True


def test_release_readiness_runtime_checks_are_active() -> None:
    frame = ReleaseReadinessPolicy().evaluate(ROOT)

    assert frame.runtime_audit_active is True
    assert frame.governance_core_active is True
    assert frame.bounded_retention_active is True
    assert frame.session_lifecycle_active is True
    assert frame.vscode_extension_buildable is True
    assert frame.provider_simulation_isolated is True
    assert frame.no_telemetry is True
    assert frame.no_hidden_persistence is True
    assert frame.no_artifact_leakage is True
    assert frame.compatibility_matrix_active is True


def test_extension_readiness_validation() -> None:
    frame = ExtensionReadinessPolicy().evaluate(ROOT)

    assert frame.extension_compile_declared is True
    assert frame.vsix_packaging_supported is True
    assert frame.bounded_local_persistence is True
    assert frame.no_hidden_network_dependency is True
    assert frame.no_hidden_signal_export is True
    assert frame.clean_vscodeignore is True
    assert frame.extension_release_ready is True


def test_governance_freeze_status_validation() -> None:
    frame = GovernanceFreezeStatusPolicy().evaluate(ROOT)

    assert frame.governance_freeze_active is True
    assert frame.alpha_boundary_declared is True
    assert frame.api_freeze_not_guaranteed is True
    assert "runtime audit report shape" in frame.stabilized_contracts
    assert "summary-only output" in frame.bounded_api_expectations


def test_runtime_audit_reports_release_readiness_section() -> None:
    report = run_runtime_enforcement_audit()

    assert report.release_readiness.release_readiness_active is True
    assert report.release_readiness.consumer_rollout_active is True
    assert report.release_readiness.extension_release_ready is True
    assert report.release_readiness.governance_freeze_active is True
    assert report.release_readiness.bounded_release_confirmed is True
    assert report.release_readiness.estimated_avoided_rollout_confusion > 0
    assert report.release_readiness.estimated_avoided_stale_migration_context > 0
    assert report.release_readiness.no_hidden_automation is True


def test_release_readiness_cli_json_and_copy_ready() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "release-readiness", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["release_ready"] is True
    assert data["github_prerelease_tag"] == "0.1.0-alpha.3"
    assert data["blocking_risks"] == []

    copy_ready = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "release-readiness", "--copy-ready"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "AI_DEV_OS 0.1.0-alpha.3 release readiness" in copy_ready.stdout
    assert "blocking_risks: none" in copy_ready.stdout


def test_no_artifact_leakage_rules_cover_release_outputs() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    vscodeignore = (EXTENSION / ".vscodeignore").read_text(encoding="utf-8")

    assert "dist/" in gitignore
    assert "build/" in gitignore
    assert "*.vsix" in gitignore
    assert "*.vsix" in vscodeignore
    assert "*.log" in gitignore
    assert "runtime_audit_report*.json" in gitignore
