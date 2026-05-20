from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.stale_detection import GovernanceStaleDetectionPrimitive


@dataclass(frozen=True)
class PersistenceCleanupFrame:
    cleaned_entries: tuple[str, ...]
    retained_entries: tuple[str, ...]
    estimated_saved_storage: int
    stale_persistence_detected: bool


class PersistenceCleanupPolicy:
    def cleanup(
        self,
        *,
        entries: tuple[str, ...],
        active_entries: tuple[str, ...],
        expired_entries: tuple[str, ...] = (),
        duplicate_entries: tuple[str, ...] = (),
    ) -> PersistenceCleanupFrame:
        shared_stale = GovernanceStaleDetectionPrimitive().detect(entries)
        cleanup_candidates = tuple(
            dict.fromkeys(
                item
                for item in (*expired_entries, *duplicate_entries, *entries)
                if item not in active_entries
                and (self._is_stale(item) or shared_stale.stale_detected)
            )
        )
        retained = tuple(item for item in entries if item not in cleanup_candidates)
        return PersistenceCleanupFrame(
            cleaned_entries=cleanup_candidates,
            retained_entries=retained,
            estimated_saved_storage=sum(max(128, len(item) * 12) for item in cleanup_candidates),
            stale_persistence_detected=bool(cleanup_candidates),
        )

    def _is_stale(self, entry: str) -> bool:
        return any(
            marker in entry
            for marker in (
                "obsolete",
                "stale",
                "expired",
                "duplicate",
                "inactive",
            )
        )
