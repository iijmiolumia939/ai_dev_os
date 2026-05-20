from __future__ import annotations

import inspect
import json
from pathlib import Path

from ai_dev_os.consumer_rollout import (
    CompatibilityProjectionPolicy,
    ConsumerRolloutAuditPolicy,
    GovernanceReadinessPolicy,
    MigrationFrictionPolicy,
    RollbackRehearsalPolicy,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

ROOT = Path("extensions/ai-dev-os-vscode")


def test_tc_rollout_01_runtime_audit_includes_consumer_rollout_section() -> None:
    report = run_runtime_enforcement_audit()

    assert report.consumer_rollout.consumer_rollout_active is True
    assert report.consumer_rollout.rollout_audit_active is True
    assert report.consumer_rollout.migration_friction_active is True
    assert report.consumer_rollout.compatibility_projection_active is True
    assert report.consumer_rollout.governance_readiness_active is True
    assert report.consumer_rollout.rollback_rehearsal_active is True
    assert report.consumer_rollout.estimated_avoided_rollout_failure > 0
    assert report.consumer_rollout.estimated_avoided_stale_migration_state > 0


def test_tc_rollout_02_extension_rollout_commands_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}
    activation = set(package["activationEvents"])

    for command in (
        "aiDevOs.showRolloutReadiness",
        "aiDevOs.showMigrationFriction",
        "aiDevOs.showGovernanceReadiness",
        "aiDevOs.showRollbackRehearsal",
    ):
        assert command in commands
        assert f"onCommand:{command}" in activation


def test_tc_rollout_03_extension_rollout_views_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    views = {item["id"] for item in package["contributes"]["views"]["explorer"]}

    assert {
        "aiDevOsRolloutReadiness",
        "aiDevOsMigrationFriction",
        "aiDevOsGovernanceReadiness",
        "aiDevOsRollbackRehearsal",
    }.issubset(views)


def test_tc_rollout_04_no_repository_mutation_or_hidden_external_signal() -> None:
    modules = (
        ConsumerRolloutAuditPolicy,
        MigrationFrictionPolicy,
        CompatibilityProjectionPolicy,
        GovernanceReadinessPolicy,
        RollbackRehearsalPolicy,
    )
    source = "\n".join(inspect.getsource(module) for module in modules)
    extension_source = (ROOT / "src" / "rollout" / "consumerRollout.ts").read_text(
        encoding="utf-8"
    )

    forbidden = ("write_text", "unlink", "rmtree", "fetch(", "XMLHttpRequest", "playwright")
    assert all(item not in source for item in forbidden)
    assert "writeFile" not in extension_source
    assert "workspace.applyEdit" not in extension_source
    assert "github.copilot" not in extension_source.lower()


def test_tc_rollout_05_rollout_rehearsal_is_summary_only() -> None:
    source = (ROOT / "src" / "rollout" / "consumerRollout.ts").read_text(encoding="utf-8")

    assert "summaryOnly: true" in source
    assert "dryRunOnly: true" in source
    assert "automaticMigrationUsed: false" in source
    assert "RateLimitedNotifications" in source


def test_tc_rollout_05_rollout_rehearsal_docs_define_boundaries() -> None:
    text = Path("docs/consumer-rollout/rollout-rehearsal.md").read_text(encoding="utf-8")

    assert "FR-ROLLOUT" in text
    assert "TC-ROLLOUT" in text
    assert "summary-only" in text
    assert "automatic migration" in text
    assert "rollback" in text.lower()
