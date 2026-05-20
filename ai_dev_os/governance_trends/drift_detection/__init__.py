from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_trends.trend_window import GovernanceTrendWindowFrame

_LEVEL = {"low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(frozen=True)
class GovernanceDriftFrame:
    drift_detected: bool
    dominant_drift: str
    drift_direction: str
    drift_velocity: int
    stabilization_recommended: bool
    evaluated_window_size: int


class GovernanceDriftPolicy:
    def detect(self, window: GovernanceTrendWindowFrame) -> GovernanceDriftFrame:
        snapshots = window.snapshots
        if len(snapshots) < 2:
            return GovernanceDriftFrame(False, "none", "stable", 0, False, len(snapshots))
        first = snapshots[0]
        last = snapshots[-1]
        deltas = {
            "governance_pressure": _delta(first.pressure, last.pressure),
            "retrieval_pressure": 0,
            "persistence_accumulation": _delta(
                first.persistence_pressure, last.persistence_pressure
            ),
            "stale_continuity": _state_delta(first.health_state, last.health_state),
            "architecture_contamination": _arch_delta(
                first.architecture_isolation, last.architecture_isolation
            ),
            "checkpoint_debt": _delta(first.checkpoint_pressure, last.checkpoint_pressure),
            "prompt_mode": 0,
        }
        dominant = max(deltas, key=lambda key: abs(deltas[key]))
        velocity = deltas[dominant]
        direction = "worsening" if velocity > 0 else "improving" if velocity < 0 else "stable"
        return GovernanceDriftFrame(
            drift_detected=velocity != 0,
            dominant_drift=dominant if velocity != 0 else "none",
            drift_direction=direction,
            drift_velocity=abs(velocity),
            stabilization_recommended=velocity > 0,
            evaluated_window_size=len(snapshots),
        )


def _delta(before: str, after: str) -> int:
    return _LEVEL.get(after, 2) - _LEVEL.get(before, 2)


def _state_delta(before: str, after: str) -> int:
    rank = {"HEALTHY": 1, "STABLE_WARNING": 2, "HIGH_PRESSURE": 3, "CRITICAL_GOVERNANCE": 4}
    return rank.get(after, 2) - rank.get(before, 2)


def _arch_delta(before: str, after: str) -> int:
    rank = {"not_required": 1, "recommended": 2, "required": 3}
    return rank.get(after, 1) - rank.get(before, 1)
