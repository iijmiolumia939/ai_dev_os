from __future__ import annotations

from pathlib import Path

from ai_dev_os.consumer_rollout import (
    CompatibilityProjectionPolicy,
    ConsumerRolloutAuditPolicy,
    GovernanceReadinessPolicy,
    MigrationFrictionPolicy,
    RollbackRehearsalPolicy,
)


def _consumer(root: Path) -> Path:
    consumer = root / "AITuber"
    (consumer / ".ai-dev-os").mkdir(parents=True)
    (consumer / ".vscode").mkdir()
    (consumer / "docs").mkdir()
    (consumer / ".gitignore").write_text(".ai-dev-os/\n.env\n", encoding="utf-8")
    (consumer / "pyproject.toml").write_text('requires-python = ">=3.11"\n', encoding="utf-8")
    (consumer / ".vscode" / "tasks.json").write_text("{}\n", encoding="utf-8")
    (consumer / "docs" / "rollout.md").write_text(
        "governance rollout continuity rollover compact stale runtime audit bounded",
        encoding="utf-8",
    )
    return consumer


def _platform(root: Path) -> Path:
    platform = root / "ai_dev_os"
    (platform / "extensions" / "ai-dev-os-vscode").mkdir(parents=True)
    (platform / "ai_dev_os" / "runtime_graph").mkdir(parents=True)
    (platform / "docs" / "consumer-rollout").mkdir(parents=True)
    (platform / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    (platform / "extensions" / "ai-dev-os-vscode" / "package.json").write_text(
        """
        {
          "main": "./out/extension.js",
          "engines": {"vscode": "^1.90.0"},
          "activationEvents": [],
          "contributes": {
            "commands": [
              {"command": "aiDevOs.showGovernancePresence"},
              {"command": "aiDevOs.showRuntimeGraph"},
              {"command": "aiDevOs.showSimplificationRecommendations"},
              {"command": "aiDevOs.showGovernanceDashboard"},
              {"command": "aiDevOs.showStaleSessionWarning"},
              {"command": "aiDevOs.copyContinuityBundle"},
              {"command": "aiDevOs.compactCurrentSession"},
              {"command": "aiDevOs.resetLocalSessionState"}
            ]
          }
        }
        """,
        encoding="utf-8",
    )
    (platform / "docs" / "consumer-rollout" / "rollback.md").write_text(
        "uninstall vsix rollback procedure .ai-dev-os cleanup persistence reset "
        "session lifecycle reset governance runtime removal",
        encoding="utf-8",
    )
    return platform


def test_tc_rollout_01_rollout_audit_is_summary_only(tmp_path: Path) -> None:
    consumer = _consumer(tmp_path)
    platform = _platform(tmp_path)

    frame = ConsumerRolloutAuditPolicy().evaluate(consumer, platform_repo=platform)

    assert frame.install_state_active is True
    assert frame.vscode_extension_state_active is True
    assert frame.workspace_persistence_compatible is True
    assert frame.runtime_graph_compatible is True
    assert frame.bounded_rollout_confirmed is True
    assert frame.summary_only is True
    assert frame.hidden_mutation_used is False
    assert frame.automatic_migration_used is False


def test_tc_rollout_02_migration_friction_detects_missing_setup(tmp_path: Path) -> None:
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    platform = _platform(tmp_path)

    frame = MigrationFrictionPolicy().evaluate(consumer, platform_repo=platform)

    assert frame.friction_level in {"MEDIUM", "HIGH", "BLOCKED"}
    assert "missing_gitignore_persistence_rule" in frame.friction_categories
    assert "missing_session_lifecycle_setup" in frame.friction_categories
    assert frame.recommended_human_actions
    assert frame.automatic_migration_used is False
    assert frame.workspace_mutation_used is False


def test_tc_rollout_03_compatibility_projection_is_bounded(tmp_path: Path) -> None:
    consumer = _consumer(tmp_path)
    platform = _platform(tmp_path)

    frame = CompatibilityProjectionPolicy().evaluate(consumer, platform_repo=platform)

    assert frame.compatibility_level == "FULL"
    assert frame.incompatible_components == ()
    assert frame.bounded_compatibility_confirmed is True
    assert frame.summary_only is True


def test_tc_rollout_04_governance_readiness_reports_missing_components(tmp_path: Path) -> None:
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    platform = _platform(tmp_path)

    frame = GovernanceReadinessPolicy().evaluate(consumer, platform_repo=platform)

    assert frame.governance_ready is False
    assert "session_rollover_workflow" in frame.missing_governance_components
    assert frame.rollout_pressure in {"MEDIUM", "HIGH"}
    assert frame.governance_training_required is True
    assert frame.automatic_governance_enforcement is False


def test_tc_rollout_05_rollback_rehearsal_is_dry_run(tmp_path: Path) -> None:
    consumer = _consumer(tmp_path)
    platform = _platform(tmp_path)

    frame = RollbackRehearsalPolicy().evaluate(consumer, platform_repo=platform)

    assert frame.rollback_ready is True
    assert frame.rollback_risk == "LOW"
    assert frame.orphaned_state_risk == "LOW"
    assert frame.bounded_rollback_confirmed is True
    assert frame.dry_run_only is True
    assert frame.mutation_performed is False
