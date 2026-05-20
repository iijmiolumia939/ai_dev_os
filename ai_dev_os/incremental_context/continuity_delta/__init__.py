from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContinuityDeltaFrame:
    changed_continuity_bundle_export: tuple[str, ...]
    unchanged_sprint_summary_suppression: bool
    stale_continuity_deduplication: bool
    compact_continuity_diff: tuple[str, ...]
    continuity_replay_reduction: bool
    estimated_avoided_continuity_tokens: int
    summary_only: bool
    deterministic: bool


class ContinuityDeltaPolicy:
    def diff(
        self,
        *,
        previous_summaries: tuple[str, ...],
        current_summaries: tuple[str, ...],
        stale_summaries: tuple[str, ...] = (),
    ) -> ContinuityDeltaFrame:
        previous = set(previous_summaries)
        stale = set(stale_summaries)
        changed = tuple(
            dict.fromkeys(
                summary
                for summary in current_summaries
                if summary not in previous and summary not in stale
            )
        )
        compact = tuple(summary[:120] for summary in changed)
        suppressed_count = len(previous_summaries) + len(stale_summaries)
        return ContinuityDeltaFrame(
            changed_continuity_bundle_export=changed,
            unchanged_sprint_summary_suppression=bool(previous_summaries),
            stale_continuity_deduplication=bool(stale_summaries),
            compact_continuity_diff=compact,
            continuity_replay_reduction=suppressed_count > 0,
            estimated_avoided_continuity_tokens=suppressed_count * 420,
            summary_only=True,
            deterministic=True,
        )
