from __future__ import annotations

from dataclasses import dataclass

_PRESSURE_LEVELS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


@dataclass(frozen=True)
class GovernancePressurePrimitiveFrame:
    aggregated_pressure: str
    dominant_pressure: str
    pressure_direction: str
    pressure_severity: int
    bounded_pressure_state: bool
    pressure_trend: tuple[str, ...]


class GovernancePressurePrimitive:
    def aggregate(
        self,
        *,
        retrieval_pressure: str = "low",
        persistence_pressure: str = "low",
        architecture_pressure: str = "low",
        session_pressure: str = "low",
        checkpoint_pressure: str = "low",
        provider_pressure: str = "low",
        continuity_pressure: str = "low",
        previous_pressure: str = "low",
    ) -> GovernancePressurePrimitiveFrame:
        samples = {
            "retrieval": retrieval_pressure,
            "persistence": persistence_pressure,
            "architecture": architecture_pressure,
            "session": session_pressure,
            "checkpoint": checkpoint_pressure,
            "provider": provider_pressure,
            "continuity": continuity_pressure,
        }
        scores = {name: _level(value) for name, value in samples.items()}
        average = round(sum(scores.values()) / len(scores))
        aggregate = _label(average)
        dominant = max(scores, key=scores.get)
        return GovernancePressurePrimitiveFrame(
            aggregated_pressure=aggregate,
            dominant_pressure=dominant,
            pressure_direction=_direction(_level(previous_pressure), _level(aggregate)),
            pressure_severity=sum(scores.values()),
            bounded_pressure_state=aggregate in {"low", "medium", "high", "critical"},
            pressure_trend=tuple(f"{name}:{samples[name]}" for name in sorted(samples)),
        )


def _level(value: str) -> int:
    return _PRESSURE_LEVELS.get(value.lower(), _PRESSURE_LEVELS["medium"])


def _label(value: int) -> str:
    if value >= 4:
        return "critical"
    if value >= 3:
        return "high"
    if value >= 2:
        return "medium"
    return "low"


def _direction(previous: int, current: int) -> str:
    if current > previous:
        return "rising"
    if current < previous:
        return "falling"
    return "steady"
