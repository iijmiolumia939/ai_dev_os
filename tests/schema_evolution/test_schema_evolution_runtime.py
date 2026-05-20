from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.persistence_governance.schema_evolution import SchemaEvolutionPolicy
from ai_dev_os.persistence_governance.schema_migration import SchemaMigrationPolicy


def test_schema_version_validation() -> None:
    frame = SchemaEvolutionPolicy().evaluate(schema_version="1.1", current_version="1.0")

    assert frame.schema_version == "1.1"
    assert frame.migration_required is True
    assert frame.incompatible_state_detected is False
    assert "session-boundary.json" in frame.managed_files


def test_incompatible_persistence_quarantine() -> None:
    evolution = SchemaEvolutionPolicy().evaluate(schema_version="1.1", current_version="0.1")
    migration = SchemaMigrationPolicy().migrate(
        state={"schema_version": "0.1", "stale_persistence": True},
        from_version="0.1",
        to_version="1.1",
        incompatible_fields=("unknown_raw_blob",),
    )

    assert evolution.incompatible_state_detected is True
    assert migration.stale_persistence_quarantined is True
    assert migration.restore_fallback is True
    assert migration.compact_reset_recommended is True
    assert migration.raw_persistence_replay_allowed is False


def test_migration_removes_deprecated_keys() -> None:
    frame = SchemaMigrationPolicy().migrate(
        state={"raw_transcript": "raw", "summary": "kept", "telemetry_uploads": "no"},
        from_version="0.9",
        to_version="1.1",
    )

    assert frame.version_upgraded is True
    assert "raw_transcript" in frame.deprecated_keys_removed
    assert "telemetry_uploads" in frame.deprecated_keys_removed
    assert "summary" in frame.migrated_state
    assert "raw_transcript" not in frame.migrated_state


def test_schema_cli_json() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "schema-migration", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["version_upgraded"] is True
    assert data["raw_persistence_replay_allowed"] is False


def test_schema_assets_are_gitignored() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    assert ".ai-dev-os/" in gitignore


def test_schema_docs_exist() -> None:
    for path in (
        Path("docs/persistence-retention-governance.md"),
        Path("docs/schema-evolution-runtime.md"),
        Path("docs/checkpoint-rotation-policy.md"),
    ):
        text = path.read_text(encoding="utf-8")
        assert "FR-RETENTION" in text
        assert "TC-RETENTION" in text
        assert "workspace-local" in text or "bounded" in text
