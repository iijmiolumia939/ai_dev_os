from __future__ import annotations

import inspect
import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.governance_trends.dashboard_delta import GovernanceDashboardDeltaPolicy
from ai_dev_os.governance_trends.regression_detection import GovernanceRegressionPolicy
from ai_dev_os.governance_trends.stability_trends import GovernanceStabilityTrendPolicy
from ai_dev_os.governance_trends.trend_window import (
    GovernanceTrendSnapshot,
    GovernanceTrendWindowPolicy,
)

ROOT = Path("extensions/ai-dev-os-vscode")


def _snapshots() -> tuple[GovernanceTrendSnapshot, ...]:
    return (
        GovernanceTrendSnapshot("s-1", "low", "low", "HEALTHY", "stable", 92),
        GovernanceTrendSnapshot("s-2", "medium", "medium", "STABLE_WARNING", "warning", 76),
        GovernanceTrendSnapshot("s-3", "high", "medium", "HIGH_PRESSURE", "unstable", 54),
        GovernanceTrendSnapshot("s-4", "medium", "high", "STABLE_WARNING", "warning", 68),
        GovernanceTrendSnapshot("s-5", "high", "high", "HIGH_PRESSURE", "unstable", 48),
        GovernanceTrendSnapshot("s-6", "critical", "high", "CRITICAL_GOVERNANCE", "degraded", 30),
    )


def test_bounded_window_enforcement() -> None:
    frame = GovernanceTrendWindowPolicy().apply(_snapshots(), max_window_size=4)

    assert frame.active_window_size == 4
    assert frame.bounded_window_maintained is True
    assert frame.full_historical_replay_allowed is False
    assert len(frame.snapshots) == 4


def test_oldest_first_eviction_validation() -> None:
    frame = GovernanceTrendWindowPolicy().apply(_snapshots(), max_window_size=3)

    assert frame.evicted_snapshots == ("s-1", "s-2", "s-3")
    assert tuple(item.snapshot_id for item in frame.snapshots) == ("s-4", "s-5", "s-6")


def test_regression_and_oscillation_detection_validation() -> None:
    frame = GovernanceTrendWindowPolicy().apply(_snapshots(), max_window_size=5)
    regression = GovernanceRegressionPolicy().detect(frame)

    assert regression.regression_detected is True
    assert regression.regression_severity in {"high", "critical"}
    assert regression.oscillation_detected is True
    assert regression.bounded_recovery_possible is True
    assert regression.compact_governance_recommended is True


def test_stability_trend_validation() -> None:
    frame = GovernanceTrendWindowPolicy().apply(_snapshots(), max_window_size=5)
    stability = GovernanceStabilityTrendPolicy().evaluate(frame)

    assert stability.stability_direction in {"degrading", "oscillating"}
    assert stability.stability_velocity > 0
    assert stability.instability_pressure in {"high", "critical"}
    assert stability.repeated_instability_bursts >= 3


def test_dashboard_delta_validation() -> None:
    previous = GovernanceTrendSnapshot("p", "medium", "medium", "STABLE_WARNING", "warning", 76)
    current = GovernanceTrendSnapshot(
        "c",
        "high",
        "high",
        "HIGH_PRESSURE",
        "unstable",
        50,
        checkpoint_pressure="high",
        persistence_pressure="high",
        architecture_isolation="recommended",
    )
    delta = GovernanceDashboardDeltaPolicy().summarize(previous=previous, current=current)

    assert delta.delta_only_summary is True
    assert delta.raw_runtime_replay_allowed is False
    assert delta.pressure_delta > 0
    assert "pressure:worse" in delta.delta_summary
    assert delta.architecture_isolation_delta == "changed"


def test_governance_trends_cli_json() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "governance-trends", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["bounded_window_maintained"] is True
    assert data["full_historical_replay_allowed"] is False
    assert data["active_window_size"] <= data["max_window_size"]


def test_no_hidden_long_term_persistence_or_autonomous_enforcement() -> None:
    import ai_dev_os.governance_trends.dashboard_delta as delta
    import ai_dev_os.governance_trends.drift_detection as drift
    import ai_dev_os.governance_trends.regression_detection as regression
    import ai_dev_os.governance_trends.stability_trends as stability
    import ai_dev_os.governance_trends.trend_window as window

    source = "\n".join(
        inspect.getsource(module) for module in (delta, drift, regression, stability, window)
    ).lower()

    assert "requests" not in source
    assert "http" not in source
    assert "subprocess" not in source
    assert "write_text" not in source
    assert "open(" not in source
    assert "git commit" not in source
    assert "git push" not in source
    assert "shutdown" not in source
    assert "upload(" not in source


def test_vscode_trend_commands_and_rate_limit() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}
    notification_source = (
        ROOT / "src" / "notifications" / "rateLimitedNotifications.ts"
    ).read_text(encoding="utf-8")
    trend_source = (ROOT / "src" / "governance" / "trends.ts").read_text(encoding="utf-8")

    assert {
        "aiDevOs.showGovernanceTrends",
        "aiDevOs.showGovernanceDrift",
        "aiDevOs.showGovernanceRegression",
        "aiDevOs.showDashboardDelta",
        "aiDevOs.compactGovernanceWindow",
        "aiDevOs.resetGovernanceTrendWindow",
    }.issubset(commands)
    assert "minIntervalMs = 30000" in notification_source
    assert "maxWindowSize = 5" in trend_source
    assert "automaticActionAllowed: false" in trend_source
