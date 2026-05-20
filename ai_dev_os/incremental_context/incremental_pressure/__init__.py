from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IncrementalPressureFrame:
    repeated_replay_detection: bool
    duplicate_architecture_cognition_detection: bool
    repeated_runtime_graph_replay_detection: bool
    continuity_replay_pressure: str
    estimated_repeated_input_token_burn: int
    estimated_duplicate_runtime_cognition: int
    pressure_level: str
    summary_only: bool
    deterministic: bool


class IncrementalPressurePolicy:
    def evaluate(
        self,
        *,
        repeated_context_count: int,
        duplicate_architecture_sections: int,
        runtime_graph_replay_count: int,
        continuity_replay_count: int,
    ) -> IncrementalPressureFrame:
        token_burn = (
            repeated_context_count * 520
            + duplicate_architecture_sections * 680
            + runtime_graph_replay_count * 480
            + continuity_replay_count * 420
        )
        duplicate_cognition = duplicate_architecture_sections * 2 + runtime_graph_replay_count
        if token_burn >= 2_400 or duplicate_cognition >= 4:
            level = "HIGH"
        elif token_burn >= 900:
            level = "MEDIUM"
        else:
            level = "LOW"
        return IncrementalPressureFrame(
            repeated_replay_detection=repeated_context_count > 0,
            duplicate_architecture_cognition_detection=duplicate_architecture_sections > 0,
            repeated_runtime_graph_replay_detection=runtime_graph_replay_count > 0,
            continuity_replay_pressure=level,
            estimated_repeated_input_token_burn=token_burn,
            estimated_duplicate_runtime_cognition=duplicate_cognition,
            pressure_level=level,
            summary_only=True,
            deterministic=True,
        )
