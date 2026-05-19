from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HandoffNotificationFrame:
    notifications: tuple[str, ...]
    rate_limited: bool
    emitted_count: int
    suppressed_count: int
    notification_summary: tuple[str, ...]


class HandoffNotificationPolicy:
    def notify(
        self,
        *,
        stale_context_detected: bool,
        rollover_required: bool,
        architecture_isolation_recommended: bool,
        continuity_generated: bool,
        prompt_export_ready: bool,
        max_notifications: int = 3,
    ) -> HandoffNotificationFrame:
        candidates = []
        if stale_context_detected:
            candidates.append("stale context detected")
        if rollover_required:
            candidates.append("recommended session rollover")
        if architecture_isolation_recommended:
            candidates.append("architecture isolation recommended")
        if continuity_generated:
            candidates.append("bounded continuity generated")
        if prompt_export_ready:
            candidates.append("prompt export ready")
        emitted = tuple(candidates[:max_notifications])
        suppressed = len(candidates) - len(emitted)
        return HandoffNotificationFrame(
            notifications=emitted,
            rate_limited=suppressed > 0,
            emitted_count=len(emitted),
            suppressed_count=suppressed,
            notification_summary=tuple(f"notify:{item}" for item in emitted),
        )
