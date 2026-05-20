from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEPRECATED_KEYS = {
    "raw_transcript",
    "full_prompt_history",
    "provider_responses",
    "full_architecture_history",
    "telemetry_uploads",
}


@dataclass(frozen=True)
class SchemaMigrationFrame:
    from_version: str
    to_version: str
    version_upgraded: bool
    deprecated_keys_removed: tuple[str, ...]
    compact_migration: bool
    incompatible_field_detected: bool
    stale_persistence_quarantined: bool
    restore_fallback: bool
    compact_reset_recommended: bool
    migrated_state: dict[str, Any]
    raw_persistence_replay_allowed: bool


class SchemaMigrationPolicy:
    def migrate(
        self,
        *,
        state: dict[str, Any],
        from_version: str,
        to_version: str,
        incompatible_fields: tuple[str, ...] = (),
    ) -> SchemaMigrationFrame:
        removed = tuple(key for key in state if key in DEPRECATED_KEYS)
        migrated = {key: value for key, value in state.items() if key not in DEPRECATED_KEYS}
        incompatible = bool(incompatible_fields)
        quarantine = incompatible or bool(state.get("stale_persistence", False))
        if quarantine:
            migrated = {
                "schema_version": to_version,
                "quarantine": True,
                "summary_only": True,
            }
        else:
            migrated["schema_version"] = to_version
            migrated["summary_only"] = True
        return SchemaMigrationFrame(
            from_version=from_version,
            to_version=to_version,
            version_upgraded=from_version != to_version,
            deprecated_keys_removed=removed,
            compact_migration=True,
            incompatible_field_detected=incompatible,
            stale_persistence_quarantined=quarantine,
            restore_fallback=quarantine,
            compact_reset_recommended=quarantine,
            migrated_state=migrated,
            raw_persistence_replay_allowed=False,
        )
