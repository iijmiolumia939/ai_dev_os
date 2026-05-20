from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetentionPolicyFrame:
    max_checkpoint_generations: int
    max_continuity_lineage_depth: int
    stale_rollover_expiration: int
    inactive_sprint_retention: int
    prompt_export_retention: int
    compact_bundle_retention: int
    retained_entries: tuple[str, ...]
    expired_entries: tuple[str, ...]
    cleanup_required: bool
    retention_pressure: str
    estimated_saved_storage: int


class RetentionPolicy:
    def apply(
        self,
        *,
        checkpoint_generations: tuple[str, ...],
        continuity_lineage: tuple[str, ...],
        stale_rollovers: tuple[str, ...] = (),
        inactive_sprints: tuple[str, ...] = (),
        prompt_exports: tuple[str, ...] = (),
        compact_bundles: tuple[str, ...] = (),
        max_checkpoint_generations: int = 5,
        max_continuity_lineage_depth: int = 8,
        stale_rollover_expiration: int = 2,
        inactive_sprint_retention: int = 3,
        prompt_export_retention: int = 5,
        compact_bundle_retention: int = 8,
    ) -> RetentionPolicyFrame:
        expired = []
        expired.extend(checkpoint_generations[max_checkpoint_generations:])
        expired.extend(continuity_lineage[max_continuity_lineage_depth:])
        expired.extend(stale_rollovers[stale_rollover_expiration:])
        expired.extend(inactive_sprints[inactive_sprint_retention:])
        expired.extend(prompt_exports[prompt_export_retention:])
        expired.extend(compact_bundles[compact_bundle_retention:])
        expired_entries = tuple(dict.fromkeys(expired))
        all_entries = tuple(
            dict.fromkeys(
                checkpoint_generations
                + continuity_lineage
                + stale_rollovers
                + inactive_sprints
                + prompt_exports
                + compact_bundles
            )
        )
        retained_entries = tuple(entry for entry in all_entries if entry not in expired_entries)
        pressure = self._pressure(len(expired_entries), len(all_entries))
        return RetentionPolicyFrame(
            max_checkpoint_generations=max_checkpoint_generations,
            max_continuity_lineage_depth=max_continuity_lineage_depth,
            stale_rollover_expiration=stale_rollover_expiration,
            inactive_sprint_retention=inactive_sprint_retention,
            prompt_export_retention=prompt_export_retention,
            compact_bundle_retention=compact_bundle_retention,
            retained_entries=retained_entries,
            expired_entries=expired_entries,
            cleanup_required=bool(expired_entries),
            retention_pressure=pressure,
            estimated_saved_storage=sum(max(128, len(entry) * 16) for entry in expired_entries),
        )

    def _pressure(self, expired_count: int, total_count: int) -> str:
        if total_count == 0 or expired_count == 0:
            return "low"
        ratio = expired_count / total_count
        if ratio >= 0.5:
            return "high"
        if ratio >= 0.25:
            return "medium"
        return "low"
