from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_trends.trend_window import GovernanceTrendWindowFrame

_PRESSURE = {"low": 1, "medium": 2, "high": 3, "critical": 4}
_HEALTH = {"HEALTHY": 1, "STABLE_WARNING": 2, "HIGH_PRESSURE": 3, "CRITICAL_GOVERNANCE": 4}


@dataclass(frozen=True)
class GovernanceRegressionFrame:
    regression_detected: bool
    regression_severity: str
    oscillation_detected: bool
    bounded_recovery_possible: bool
    compact_governance_recommended: bool
    repeated_instability_count: int


class GovernanceRegressionPolicy:
    def detect(self, window: GovernanceTrendWindowFrame) -> GovernanceRegressionFrame:
        snapshots = window.snapshots
        pressure_values = tuple(_PRESSURE.get(item.pressure, 2) for item in snapshots)
        health_values = tuple(_HEALTH.get(item.health_state, 2) for item in snapshots)
        repeated_instability = sum(1 for item in snapshots if item.stability_state != "stable")
        worsening_pressure = len(pressure_values) >= 2 and pressure_values[-1] > pressure_values[0]
        degraded_health = len(health_values) >= 2 and health_values[-1] > health_values[0]
        repeated_rollover_pressure = repeated_instability >= 3
        repeated_checkpoint_pressure = (
            sum(1 for item in snapshots if item.checkpoint_pressure in {"high", "critical"}) >= 2
        )
        oscillation = _oscillates(pressure_values) or _oscillates(health_values)
        detected = bool(
            worsening_pressure
            or degraded_health
            or oscillation
            or repeated_rollover_pressure
            or repeated_checkpoint_pressure
        )
        severity = _severity(
            sum(
                (
                    worsening_pressure,
                    degraded_health,
                    oscillation,
                    repeated_rollover_pressure,
                    repeated_checkpoint_pressure,
                )
            )
        )
        return GovernanceRegressionFrame(
            regression_detected=detected,
            regression_severity=severity,
            oscillation_detected=oscillation,
            bounded_recovery_possible=window.bounded_window_maintained,
            compact_governance_recommended=detected and window.bounded_window_maintained,
            repeated_instability_count=repeated_instability,
        )


def _oscillates(values: tuple[int, ...]) -> bool:
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


def _severity(signal_count: int) -> str:
    if signal_count >= 4:
        return "critical"
    if signal_count >= 2:
        return "high"
    if signal_count == 1:
        return "medium"
    return "low"
