from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.governance_trends.drift_detection import GovernanceDriftPolicy
from ai_dev_os.governance_trends.trend_window import (
    GovernanceTrendSnapshot,
    GovernanceTrendWindowPolicy,
)

ROOT = Path("extensions/ai-dev-os-vscode")


def test_drift_detection_validation() -> None:
    window = GovernanceTrendWindowPolicy().apply(
        (
            GovernanceTrendSnapshot("a", "low", "low", "HEALTHY", "stable", 90),
            GovernanceTrendSnapshot(
                "b",
                "high",
                "medium",
                "HIGH_PRESSURE",
                "unstable",
                50,
                checkpoint_pressure="high",
                persistence_pressure="high",
                architecture_isolation="recommended",
            ),
        ),
        max_window_size=5,
    )
    drift = GovernanceDriftPolicy().detect(window)

    assert drift.drift_detected is True
    assert drift.dominant_drift in {
        "governance_pressure",
        "stale_continuity",
        "persistence_accumulation",
        "checkpoint_debt",
    }
    assert drift.drift_direction == "worsening"
    assert drift.drift_velocity > 0
    assert drift.stabilization_recommended is True


def test_dashboard_delta_cli_json() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "governance-dashboard-delta", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["delta_only_summary"] is True
    assert data["raw_runtime_replay_allowed"] is False
    assert data["delta_summary"]


def test_runtime_audit_reports_governance_trends() -> None:
    from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

    report = run_runtime_enforcement_audit()

    assert report.governance_trends.governance_trend_window_active is True
    assert report.governance_trends.governance_drift_detection_active is True
    assert report.governance_trends.governance_regression_active is True
    assert report.governance_trends.governance_stability_trends_active is True
    assert report.governance_trends.dashboard_delta_active is True
    assert report.governance_trends.estimated_avoided_governance_regression > 0
    assert report.governance_trends.estimated_avoided_hidden_trend_accumulation > 0


def test_extension_trend_view_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    views = {item["id"] for item in package["contributes"]["views"]["explorer"]}

    assert "aiDevOsGovernanceTrends" in views


def test_extension_trend_source_is_bounded_observability() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))
    lowered = source.lower()

    assert "fetch(" not in lowered
    assert "xmlhttprequest" not in lowered
    assert "workbench.action.chat.submit" not in lowered
    assert "workbench.action.chat.acceptinput" not in lowered
    assert "github.copilot" not in lowered
    assert "shutdown" not in lowered
    assert "git commit" not in lowered
    assert "git push" not in lowered
    assert "telemetry" not in lowered


def test_governance_trend_docs_exist() -> None:
    for path in (
        Path("docs/governance-trend-window.md"),
        Path("docs/governance-drift-detection.md"),
        Path("docs/bounded-governance-history.md"),
    ):
        text = path.read_text(encoding="utf-8")
        assert "FR-GOVTREND" in text
        assert "TC-GOVTREND" in text
        assert "bounded" in text
