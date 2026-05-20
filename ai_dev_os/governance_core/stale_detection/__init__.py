from __future__ import annotations

from dataclasses import dataclass

_STALE_MARKERS = {
    "continuity": ("stale_continuity", "old_continuity"),
    "persistence": ("stale_persistence", "expired_persistence"),
    "checkpoints": ("stale_checkpoint", "expired_checkpoint"),
    "sprint_context": ("old_sprint", "stale_sprint"),
    "governance_signals": ("stale_governance", "governance_drift"),
    "retrieval_summaries": (
        "retrieval_drift",
        "retrieval drift",
        "stale_retrieval",
        "stale retrieval",
    ),
}


@dataclass(frozen=True)
class GovernanceStaleDetectionFrame:
    stale_detected: bool
    stale_categories: tuple[str, ...]
    stale_pressure: str
    stale_cleanup_recommended: bool
    summary_only: bool


class GovernanceStaleDetectionPrimitive:
    def detect(
        self,
        signals: tuple[str, ...],
        *,
        max_categories: int = 6,
    ) -> GovernanceStaleDetectionFrame:
        normalized = tuple(signal.lower() for signal in signals)
        categories = tuple(
            category
            for category, markers in _STALE_MARKERS.items()
            if any(marker in signal for marker in markers for signal in normalized)
        )[:max_categories]
        pressure = "high" if len(categories) >= 4 else "medium" if categories else "low"
        return GovernanceStaleDetectionFrame(
            stale_detected=bool(categories),
            stale_categories=categories,
            stale_pressure=pressure,
            stale_cleanup_recommended=pressure in {"medium", "high"},
            summary_only=True,
        )
