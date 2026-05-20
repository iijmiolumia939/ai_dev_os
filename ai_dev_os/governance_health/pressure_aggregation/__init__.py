from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.pressure_primitives import GovernancePressurePrimitive

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
        primitive = GovernancePressurePrimitive().aggregate(
            retrieval_pressure=retrieval_pressure,
            persistence_pressure=persistence_pressure,
            session_pressure=session_pressure,
            architecture_pressure=architecture_pressure,
            provider_pressure=provider_pressure,
            continuity_pressure=_max_pressure(continuity_pressure, stale_context_pressure),
            checkpoint_pressure=checkpoint_pressure,
            previous_pressure=previous_pressure,
        )
        total = sum(scores.values())
        trend = tuple(f"{name}:{samples[name]}" for name in sorted(samples))
        return GovernancePressureFrame(
            aggregate_pressure=primitive.aggregated_pressure,
            dominant_pressure=primitive.dominant_pressure,
            pressure_direction=primitive.pressure_direction,
            pressure_trend=trend,
            bounded_operation_recommended=primitive.aggregated_pressure in {"high", "critical"},
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


def _max_pressure(first: str, second: str) -> str:
    return first if _level(first) >= _level(second) else second
