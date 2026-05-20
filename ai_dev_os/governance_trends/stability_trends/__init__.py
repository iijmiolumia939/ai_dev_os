from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_trends.trend_window import (
    GovernanceTrendSnapshot,
    GovernanceTrendWindowFrame,
)


@dataclass(frozen=True)
class GovernanceStabilityTrendFrame:
    stability_direction: str
    stability_velocity: int
    stabilization_progress: int
    instability_pressure: str
    governance_recovery_detected: bool
    repeated_instability_bursts: int


class GovernanceStabilityTrendPolicy:
    def evaluate(self, window: GovernanceTrendWindowFrame) -> GovernanceStabilityTrendFrame:
        snapshots = window.snapshots
        if len(snapshots) < 2:
            return GovernanceStabilityTrendFrame("stable", 0, 0, "low", False, 0)
        first_score = snapshots[0].health_score
        last_score = snapshots[-1].health_score
        velocity = last_score - first_score
        instability_bursts = sum(1 for item in snapshots if item.stability_state != "stable")
        direction = _direction(velocity, snapshots)
        return GovernanceStabilityTrendFrame(
            stability_direction=direction,
            stability_velocity=abs(velocity),
            stabilization_progress=max(0, velocity),
            instability_pressure=_pressure(instability_bursts),
            governance_recovery_detected=velocity > 0 and instability_bursts < len(snapshots),
            repeated_instability_bursts=instability_bursts,
        )


def _direction(velocity: int, snapshots: tuple[GovernanceTrendSnapshot, ...]) -> str:
    if _oscillating(tuple(item.health_score for item in snapshots)):
        return "oscillating"
    if velocity > 5:
        return "improving"
    if velocity < -5:
        return "degrading"
    return "stable"


def _oscillating(values: tuple[int, ...]) -> bool:
    if len(values) < 4:
        return False
    directions = tuple(
        1 if values[index] > values[index - 1] else -1 if values[index] < values[index - 1] else 0
        for index in range(1, len(values))
    )
    non_zero = tuple(item for item in directions if item != 0)
    direction_changes = sum(
        1 for index in range(1, len(non_zero)) if non_zero[index] != non_zero[index - 1]
    )
    return direction_changes >= 2


def _pressure(count: int) -> str:
    if count >= 4:
        return "critical"
    if count >= 3:
        return "high"
    if count >= 1:
        return "medium"
    return "low"
