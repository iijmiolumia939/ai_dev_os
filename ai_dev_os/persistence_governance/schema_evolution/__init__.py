from __future__ import annotations

from dataclasses import dataclass

PERSISTENCE_FILES = (
    "session-boundary.json",
    "rollover-state.json",
    "continuity-index.json",
    "prompt-mode-state.json",
    "checkpoint-metadata.json",
)


@dataclass(frozen=True)
class SchemaEvolutionFrame:
    schema_version: str
    compatible_versions: tuple[str, ...]
    deprecated_versions: tuple[str, ...]
    migration_required: bool
    incompatible_state_detected: bool
    managed_files: tuple[str, ...]


class SchemaEvolutionPolicy:
    def evaluate(
        self,
        *,
        schema_version: str,
        current_version: str,
        compatible_versions: tuple[str, ...] = ("1.0", "1.1"),
        deprecated_versions: tuple[str, ...] = ("0.8", "0.9"),
    ) -> SchemaEvolutionFrame:
        migration = current_version != schema_version
        incompatible = current_version not in compatible_versions + (schema_version,)
        return SchemaEvolutionFrame(
            schema_version=schema_version,
            compatible_versions=compatible_versions,
            deprecated_versions=deprecated_versions,
            migration_required=migration or current_version in deprecated_versions,
            incompatible_state_detected=incompatible,
            managed_files=PERSISTENCE_FILES,
        )
