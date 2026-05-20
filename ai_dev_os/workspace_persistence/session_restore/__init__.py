from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.workspace_persistence.persistence_store import PersistenceStoreFrame


@dataclass(frozen=True)
class SessionRestoreFrame:
    restore_available: bool
    restored_generation: int
    stale_state_detected: bool
    pending_rollover_restored: bool
    compact_bundle_restored: bool
    recommended_action: str
    stale_persistence_auto_applied: bool


class SessionRestorePolicy:
    def restore(self, store: PersistenceStoreFrame | None) -> SessionRestoreFrame:
        if store is None:
            return SessionRestoreFrame(
                restore_available=False,
                restored_generation=0,
                stale_state_detected=False,
                pending_rollover_restored=False,
                compact_bundle_restored=False,
                recommended_action="start_clean_bounded_session",
                stale_persistence_auto_applied=False,
            )
        stale = bool(store.stale_warning_state.get("stale_session_detected", False))
        pending = bool(store.rollover_state.get("rollover_pending", False))
        compact = bool(store.last_continuity_bundle)
        action = "confirm_human_rollover" if pending or stale else "restore_bounded_state"
        return SessionRestoreFrame(
            restore_available=True,
            restored_generation=store.current_session_generation,
            stale_state_detected=stale,
            pending_rollover_restored=pending,
            compact_bundle_restored=compact,
            recommended_action=action,
            stale_persistence_auto_applied=False,
        )
