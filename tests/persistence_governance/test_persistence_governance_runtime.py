from __future__ import annotations

from ai_dev_os.persistence_governance.checkpoint_rotation import CheckpointRotationPolicy
from ai_dev_os.persistence_governance.persistence_budget import PersistenceBudgetPolicy
from ai_dev_os.persistence_governance.retention_policy import RetentionPolicy


def test_retention_enforcement_validation() -> None:
    frame = RetentionPolicy().apply(
        checkpoint_generations=tuple(f"checkpoint-{index}" for index in range(8)),
        continuity_lineage=tuple(f"lineage-{index}" for index in range(10)),
        stale_rollovers=("stale-1", "stale-2", "stale-3"),
        inactive_sprints=("inactive-1", "inactive-2", "inactive-3", "inactive-4"),
        prompt_exports=tuple(f"prompt-{index}" for index in range(7)),
        compact_bundles=tuple(f"bundle-{index}" for index in range(9)),
    )

    assert frame.cleanup_required is True
    assert frame.expired_entries
    assert frame.retention_pressure in {"low", "medium", "high"}
    assert len(frame.retained_entries) < 41
    assert frame.estimated_saved_storage > 0


def test_persistence_budget_validation() -> None:
    frame = PersistenceBudgetPolicy().evaluate(
        checkpoint_storage=18_000,
        continuity_index_storage=9_000,
        prompt_export_storage=12_000,
        stale_persistence_storage=16_000,
        schema_metadata_storage=2_000,
    )

    assert frame.current_budget_usage == 57_000
    assert frame.retention_pressure == "high"
    assert frame.compact_required is True
    assert frame.cleanup_required is True
    assert frame.storage_budget_remaining == 7_000


def test_checkpoint_rotation_validation() -> None:
    frame = CheckpointRotationPolicy().rotate(
        checkpoints=tuple(f"checkpoint-{index}" for index in range(10)),
        max_active=3,
        max_archived=4,
    )

    assert len(frame.active_checkpoints) == 3
    assert len(frame.archived_checkpoints) == 4
    assert len(frame.expired_checkpoints) == 3
    assert frame.checkpoint_compaction is True
    assert frame.rotation_required is True


def test_bounded_persistence_enforcement() -> None:
    retention = RetentionPolicy().apply(
        checkpoint_generations=tuple(f"checkpoint-{index}" for index in range(30)),
        continuity_lineage=tuple(f"lineage-{index}" for index in range(30)),
    )
    budget = PersistenceBudgetPolicy().evaluate(
        checkpoint_storage=40_000,
        continuity_index_storage=20_000,
        prompt_export_storage=10_000,
        stale_persistence_storage=20_000,
        schema_metadata_storage=2_000,
    )

    assert retention.cleanup_required is True
    assert budget.cleanup_required is True
    assert budget.storage_budget_remaining == 0


def test_no_network_or_telemetry_imports() -> None:
    import inspect

    from ai_dev_os.persistence_governance import (
        checkpoint_rotation,
        persistence_budget,
        retention_policy,
        schema_evolution,
        schema_migration,
    )

    source = "\n".join(
        inspect.getsource(module)
        for module in (
            checkpoint_rotation,
            persistence_budget,
            retention_policy,
            schema_evolution,
            schema_migration,
        )
    )

    assert "requests" not in source
    assert "http" not in source
    assert "upload(" not in source.lower()


def test_runtime_audit_reports_persistence_governance() -> None:
    from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

    report = run_runtime_enforcement_audit()

    assert report.persistence_governance.retention_policy_active is True
    assert report.persistence_governance.persistence_budget_active is True
    assert report.persistence_governance.schema_evolution_active is True
    assert report.persistence_governance.schema_migration_active is True
    assert report.persistence_governance.checkpoint_rotation_active is True
    assert report.persistence_governance.estimated_avoided_stale_persistence_growth > 0
    assert report.persistence_governance.estimated_avoided_checkpoint_explosion > 0
