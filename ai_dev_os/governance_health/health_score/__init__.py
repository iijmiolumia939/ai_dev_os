from __future__ import annotations

from dataclasses import dataclass

_PRESSURE_WEIGHT = {
    "low": 8,
    "medium": 22,
    "high": 42,
    "critical": 62,
}


@dataclass(frozen=True)
class GovernanceHealthFrame:
    governance_health_score: int
    governance_health_state: str
    governance_stability: str
    governance_degradation_detected: bool
    governance_attention_required: bool
    pressure_average: int
    risk_signal_count: int


class GovernanceHealthPolicy:
    def score(
        self,
        *,
        session_lifecycle: str,
        stale_context_pressure: str,
        persistence_pressure: str,
        retrieval_scaling_pressure: str,
        provider_simulation_pressure: str,
        architecture_isolation_pressure: str,
        schema_migration_pressure: str,
        checkpoint_rotation_pressure: str,
        workspace_contamination_risk: bool,
    ) -> GovernanceHealthFrame:
        pressures = (
            session_lifecycle,
            stale_context_pressure,
            persistence_pressure,
            retrieval_scaling_pressure,
            provider_simulation_pressure,
            architecture_isolation_pressure,
            schema_migration_pressure,
            checkpoint_rotation_pressure,
        )
        pressure_values = tuple(_pressure_value(item) for item in pressures)
        average = round(sum(pressure_values) / len(pressure_values))
        risk_count = sum(1 for item in pressure_values if item >= _PRESSURE_WEIGHT["high"])
        if workspace_contamination_risk:
            risk_count += 1
        penalty = average + risk_count * 7 + (10 if workspace_contamination_risk else 0)
        score = max(0, min(100, 100 - penalty))
        state = _state_for_score(score, risk_count)
        degradation = state in {"HIGH_PRESSURE", "CRITICAL_GOVERNANCE"}
        return GovernanceHealthFrame(
            governance_health_score=score,
            governance_health_state=state,
            governance_stability="stable" if score >= 70 else "degraded",
            governance_degradation_detected=degradation,
            governance_attention_required=state != "HEALTHY",
            pressure_average=average,
            risk_signal_count=risk_count,
        )


def _pressure_value(value: str) -> int:
    return _PRESSURE_WEIGHT.get(value.lower(), _PRESSURE_WEIGHT["medium"])


def _state_for_score(score: int, risk_count: int) -> str:
    if score <= 35 or risk_count >= 5:
        return "CRITICAL_GOVERNANCE"
    if score <= 55 or risk_count >= 3:
        return "HIGH_PRESSURE"
    if score <= 75 or risk_count >= 1:
        return "STABLE_WARNING"
    return "HEALTHY"
