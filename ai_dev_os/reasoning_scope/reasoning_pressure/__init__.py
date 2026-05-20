from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReasoningPressureFrame:
    deep_reasoning_explosion_detection: bool
    unnecessary_escalation_detection: bool
    broad_synthesis_pressure: bool
    repeated_architecture_reasoning_detection: bool
    estimated_premium_reasoning_burn: int
    estimated_unnecessary_architecture_reasoning: int
    pressure_level: str
    premium_reasoning_avoidance_recommended: bool
    deterministic: bool
    summary_only: bool


class ReasoningPressurePolicy:
    def evaluate(
        self,
        *,
        requested_depth: int,
        depth_cap: int,
        requested_runtime_count: int,
        neighborhood_cap: int,
        repeated_architecture_sections: int,
        escalation_requested: bool,
    ) -> ReasoningPressureFrame:
        deep = requested_depth > depth_cap
        broad = requested_runtime_count > neighborhood_cap
        repeated = repeated_architecture_sections > 0
        unnecessary = escalation_requested and (deep or broad or repeated)
        premium_burn = (
            max(0, requested_depth - depth_cap) * 900
            + max(0, requested_runtime_count - neighborhood_cap) * 420
        )
        architecture_burn = repeated_architecture_sections * 760 + (680 if broad else 0)
        if premium_burn + architecture_burn >= 2_400:
            pressure = "HIGH"
        elif premium_burn + architecture_burn > 0:
            pressure = "MEDIUM"
        else:
            pressure = "LOW"
        return ReasoningPressureFrame(
            deep_reasoning_explosion_detection=deep,
            unnecessary_escalation_detection=unnecessary,
            broad_synthesis_pressure=broad,
            repeated_architecture_reasoning_detection=repeated,
            estimated_premium_reasoning_burn=premium_burn,
            estimated_unnecessary_architecture_reasoning=architecture_burn,
            pressure_level=pressure,
            premium_reasoning_avoidance_recommended=pressure != "LOW",
            deterministic=True,
            summary_only=True,
        )
