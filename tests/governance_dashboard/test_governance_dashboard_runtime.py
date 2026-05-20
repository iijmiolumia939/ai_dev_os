from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.governance_health.governance_dashboard import GovernanceDashboardPolicy
from ai_dev_os.governance_health.health_score import GovernanceHealthPolicy
from ai_dev_os.governance_health.pressure_aggregation import GovernancePressurePolicy
from ai_dev_os.governance_health.risk_aggregation import GovernanceRiskPolicy

ROOT = Path("extensions/ai-dev-os-vscode")


def test_dashboard_validation() -> None:
    health = GovernanceHealthPolicy().score(
        session_lifecycle="medium",
        stale_context_pressure="high",
        persistence_pressure="high",
        retrieval_scaling_pressure="medium",
        provider_simulation_pressure="low",
        architecture_isolation_pressure="low",
        schema_migration_pressure="medium",
        checkpoint_rotation_pressure="high",
        workspace_contamination_risk=False,
    )
    pressure = GovernancePressurePolicy().aggregate(
        retrieval_pressure="medium",
        persistence_pressure="high",
        session_pressure="high",
        architecture_pressure="low",
        provider_pressure="low",
        continuity_pressure="high",
        checkpoint_pressure="high",
        stale_context_pressure="high",
    )
    risk = GovernanceRiskPolicy().aggregate(
        stale_continuity_risk=True,
        hidden_context_drift=True,
        architecture_contamination=False,
        retrieval_explosion=False,
        persistence_explosion=True,
        checkpoint_explosion=True,
        provider_lock_in_risk=False,
        governance_runtime_drift=False,
        prompt_mode_drift=False,
    )

    frame = GovernanceDashboardPolicy().build(
        health=health,
        pressure=pressure,
        risk=risk,
        stale_session_active=True,
        persistence_budget_state="high",
        checkpoint_pressure="high",
        architecture_isolation_required=False,
        workspace_dirty=False,
        rollout_stability="stable rollout",
    )

    assert frame.summary_only is True
    assert frame.raw_runtime_replay_allowed is False
    assert frame.active_warnings
    assert frame.pressure_summary.startswith("aggregate=")
    assert frame.risk_summary.startswith("aggregate=")


def test_governance_cli_dashboard_json() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "governance-dashboard", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["summary_only"] is True
    assert data["raw_runtime_replay_allowed"] is False
    assert "governance_health" in data


def test_vscode_governance_commands_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}

    assert {
        "aiDevOs.showGovernanceDashboard",
        "aiDevOs.showGovernanceHealth",
        "aiDevOs.showGovernanceRisks",
        "aiDevOs.showGovernancePressure",
        "aiDevOs.runGovernanceStabilityAudit",
        "aiDevOs.compactGovernanceContext",
        "aiDevOs.showArchitectureIsolationState",
    }.issubset(commands)


def test_vscode_governance_dashboard_view_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    views = {item["id"] for item in package["contributes"]["views"]["explorer"]}

    assert "aiDevOsGovernanceDashboard" in views


def test_notification_rate_limiting_and_status_bar() -> None:
    notification_source = (
        ROOT / "src" / "notifications" / "rateLimitedNotifications.ts"
    ).read_text(encoding="utf-8")
    health_source = (ROOT / "src" / "governance" / "health.ts").read_text(encoding="utf-8")

    assert "minIntervalMs = 30000" in notification_source
    assert "createStatusBarItem" in health_source
    assert "automaticActionAllowed: false" in health_source


def test_extension_bounded_observability_static() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))
    lowered = source.lower()

    assert "fetch(" not in lowered
    assert "xmlhttprequest" not in lowered
    assert "workbench.action.chat" not in lowered
    assert "github.copilot" not in lowered
    assert "shutdown" not in lowered
    assert "git commit" not in lowered
    assert "git push" not in lowered
    assert "telemetry" not in lowered


def test_governance_docs_exist() -> None:
    for path in (
        Path("docs/governance-health-runtime.md"),
        Path("docs/governance-pressure-model.md"),
        Path("docs/governance-observability.md"),
    ):
        text = path.read_text(encoding="utf-8")
        assert "FR-GOVHEALTH" in text
        assert "TC-GOVHEALTH" in text
        assert "bounded" in text
