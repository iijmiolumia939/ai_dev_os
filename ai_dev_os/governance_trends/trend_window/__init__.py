from __future__ import annotations

from dataclasses import dataclass

_PRESSURE = {"low": 1, "medium": 2, "high": 3, "critical": 4}
_STABILITY = {"stable": 3, "warning": 2, "unstable": 1, "degraded": 0}


@dataclass(frozen=True)
class GovernanceTrendSnapshot:
    snapshot_id: str
    pressure: str
    risk: str
    health_state: str
    stability_state: str
    health_score: int
    checkpoint_pressure: str = "low"
    persistence_pressure: str = "low"
    architecture_isolation: str = "not_required"


@dataclass(frozen=True)
class GovernanceTrendWindowFrame:
    active_window_size: int
    evicted_snapshots: tuple[str, ...]
    trend_window_pressure: str
    trend_window_stability: str
    bounded_window_maintained: bool
    snapshots: tuple[GovernanceTrendSnapshot, ...]
    max_window_size: int
    full_historical_replay_allowed: bool


class GovernanceTrendWindowPolicy:
    def apply(
        self,
        snapshots: tuple[GovernanceTrendSnapshot, ...],
        *,
        max_window_size: int = 5,
    ) -> GovernanceTrendWindowFrame:
        max_size = max(1, max_window_size)
        retained = snapshots[-max_size:]
        evicted = snapshots[: max(0, len(snapshots) - max_size)]
        return GovernanceTrendWindowFrame(
            active_window_size=len(retained),
            evicted_snapshots=tuple(item.snapshot_id for item in evicted),
            trend_window_pressure=_pressure_label(retained),
            trend_window_stability=_stability_label(retained),
            bounded_window_maintained=len(retained) <= max_size,
            snapshots=retained,
            max_window_size=max_size,
            full_historical_replay_allowed=False,
        )


def _pressure_label(snapshots: tuple[GovernanceTrendSnapshot, ...]) -> str:
    if not snapshots:
        return "low"
    average = round(sum(_PRESSURE.get(item.pressure, 2) for item in snapshots) / len(snapshots))
    return {1: "low", 2: "medium", 3: "high", 4: "critical"}[max(1, min(4, average))]


def _stability_label(snapshots: tuple[GovernanceTrendSnapshot, ...]) -> str:
    if not snapshots:
        return "stable"
    average = round(
        sum(_STABILITY.get(item.stability_state, 2) for item in snapshots) / len(snapshots)
    )
    if average >= 3:
        return "stable"
    if average == 2:
        return "warning"
    if average == 1:
        return "unstable"
    return "degraded"
