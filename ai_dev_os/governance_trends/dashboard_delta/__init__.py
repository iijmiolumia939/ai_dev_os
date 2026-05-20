from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_trends.trend_window import GovernanceTrendSnapshot

_LEVEL = {"low": 1, "medium": 2, "high": 3, "critical": 4}
_HEALTH = {"HEALTHY": 1, "STABLE_WARNING": 2, "HIGH_PRESSURE": 3, "CRITICAL_GOVERNANCE": 4}
_STABILITY = {"stable": 3, "warning": 2, "unstable": 1, "degraded": 0}


@dataclass(frozen=True)
class GovernanceDashboardDeltaFrame:
    health_delta: int
    pressure_delta: int
    risk_delta: int
    stability_delta: int
    checkpoint_pressure_delta: int
    persistence_pressure_delta: int
    architecture_isolation_delta: str
    delta_summary: tuple[str, ...]
    delta_only_summary: bool
    raw_runtime_replay_allowed: bool


class GovernanceDashboardDeltaPolicy:
    def summarize(
        self,
        *,
        previous: GovernanceTrendSnapshot,
        current: GovernanceTrendSnapshot,
    ) -> GovernanceDashboardDeltaFrame:
        health_delta = _HEALTH.get(current.health_state, 2) - _HEALTH.get(previous.health_state, 2)
        pressure_delta = _LEVEL.get(current.pressure, 2) - _LEVEL.get(previous.pressure, 2)
        risk_delta = _LEVEL.get(current.risk, 2) - _LEVEL.get(previous.risk, 2)
        stability_delta = _STABILITY.get(current.stability_state, 2) - _STABILITY.get(
            previous.stability_state, 2
        )
        checkpoint_delta = _LEVEL.get(current.checkpoint_pressure, 1) - _LEVEL.get(
            previous.checkpoint_pressure, 1
        )
        persistence_delta = _LEVEL.get(current.persistence_pressure, 1) - _LEVEL.get(
            previous.persistence_pressure, 1
        )
        architecture_delta = (
            "changed"
            if current.architecture_isolation != previous.architecture_isolation
            else "unchanged"
        )
        return GovernanceDashboardDeltaFrame(
            health_delta=health_delta,
            pressure_delta=pressure_delta,
            risk_delta=risk_delta,
            stability_delta=stability_delta,
            checkpoint_pressure_delta=checkpoint_delta,
            persistence_pressure_delta=persistence_delta,
            architecture_isolation_delta=architecture_delta,
            delta_summary=tuple(
                item
                for item in (
                    _summary("health", health_delta),
                    _summary("pressure", pressure_delta),
                    _summary("risk", risk_delta),
                    _summary("stability", -stability_delta),
                    _summary("checkpoint", checkpoint_delta),
                    _summary("persistence", persistence_delta),
                    f"architecture:{architecture_delta}",
                )
                if item
            ),
            delta_only_summary=True,
            raw_runtime_replay_allowed=False,
        )


def _summary(name: str, delta: int) -> str:
    if delta > 0:
        return f"{name}:worse"
    if delta < 0:
        return f"{name}:better"
    return f"{name}:unchanged"
