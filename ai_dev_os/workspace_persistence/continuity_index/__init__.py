from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContinuityIndexFrame:
    continuity_bundle_ids: tuple[str, ...]
    generation_mapping: dict[str, int]
    sprint_mapping: dict[str, str]
    prompt_export_references: tuple[str, ...]
    rollover_lineage: tuple[str, ...]
    stale_continuity_flags: tuple[str, ...]
    summary_only: bool
    raw_export_replay_allowed: bool


class ContinuityIndexPolicy:
    def index(
        self,
        *,
        continuity_bundle_ids: tuple[str, ...],
        generation_mapping: dict[str, int],
        sprint_mapping: dict[str, str],
        prompt_export_references: tuple[str, ...],
        rollover_lineage: tuple[str, ...],
        stale_continuity_flags: tuple[str, ...] = (),
        max_entries: int = 20,
    ) -> ContinuityIndexFrame:
        ids = tuple(dict.fromkeys(continuity_bundle_ids))[:max_entries]
        return ContinuityIndexFrame(
            continuity_bundle_ids=ids,
            generation_mapping={
                key: generation_mapping[key] for key in ids if key in generation_mapping
            },
            sprint_mapping={key: sprint_mapping[key] for key in ids if key in sprint_mapping},
            prompt_export_references=prompt_export_references[:max_entries],
            rollover_lineage=rollover_lineage[:max_entries],
            stale_continuity_flags=stale_continuity_flags[:max_entries],
            summary_only=True,
            raw_export_replay_allowed=False,
        )
