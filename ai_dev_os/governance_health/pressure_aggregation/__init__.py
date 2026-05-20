from __future__ import annotations

from dataclasses import dataclass

_PRESSURE_LEVELS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


@dataclass(frozen=True)
class GovernancePressureFrame:
    aggregate_pressure: str
    dominant_pressure: str
    pressure_direction: str
    pressure_trend: tuple[str, ...]
    bounded_operation_recommended: bool
    pressure_score: int


class GovernancePressurePolicy:
    def aggregate(
        self,
        *,
        retrieval_pressure: str,
        persistence_pressure: str,
        session_pressure: str,
        architecture_pressure: str,
        provider_pressure: str,
        continuity_pressure: str,
        checkpoint_pressure: str,
        stale_context_pressure: str,
        previous_pressure: str = "low",
    ) -> GovernancePressureFrame:
        samples = {
            "retrieval": retrieval_pressure,
            "persistence": persistence_pressure,
            "session": session_pressure,
            "architecture": architecture_pressure,
            "provider": provider_pressure,
            "continuity": continuity_pressure,
            "checkpoint": checkpoint_pressure,
            "stale_context": stale_context_pressure,
        }
        scores = {name: _level(value) for name, value in samples.items()}
        total = sum(scores.values())
        average = round(total / len(scores))
        aggregate = _label(average)
        dominant = max(scores, key=scores.get)
        direction = _direction(_level(previous_pressure), _level(aggregate))
        trend = tuple(f"{name}:{samples[name]}" for name in sorted(samples))
        return GovernancePressureFrame(
            aggregate_pressure=aggregate,
            dominant_pressure=dominant,
            pressure_direction=direction,
            pressure_trend=trend,
            bounded_operation_recommended=aggregate in {"high", "critical"},
            pressure_score=total,
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
