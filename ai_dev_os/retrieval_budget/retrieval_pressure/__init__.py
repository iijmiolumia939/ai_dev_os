from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalPressureFrame:
    retrieval_explosion_detected: bool
    broad_architecture_leakage_detected: bool
    giant_continuity_retrieval_detected: bool
    estimated_hidden_input_token_burn: int
    retrieval_downgrade_recommendation: bool
    pressure_level: str
    no_hidden_provider_routing: bool
    no_automatic_retrieval_escalation: bool
    deterministic: bool


class RetrievalPressurePolicy:
    def evaluate(
        self,
        *,
        selected_runtime_count: int,
        all_runtime_count: int,
        continuity_size: int,
        max_runtime_count: int,
        max_continuity_size: int,
        architecture_isolation: bool = False,
    ) -> RetrievalPressureFrame:
        explosion = selected_runtime_count > max_runtime_count
        leakage = architecture_isolation and selected_runtime_count > max(
            1, max_runtime_count // 2
        )
        giant_continuity = continuity_size > max_continuity_size
        burn = max(0, (all_runtime_count - selected_runtime_count) * 320) + max(
            0, continuity_size - max_continuity_size
        )
        if explosion or giant_continuity:
            pressure = "HIGH"
        elif leakage:
            pressure = "MEDIUM"
        else:
            pressure = "LOW"
        return RetrievalPressureFrame(
            retrieval_explosion_detected=explosion,
            broad_architecture_leakage_detected=leakage,
            giant_continuity_retrieval_detected=giant_continuity,
            estimated_hidden_input_token_burn=burn,
            retrieval_downgrade_recommendation=pressure in {"MEDIUM", "HIGH"},
            pressure_level=pressure,
            no_hidden_provider_routing=True,
            no_automatic_retrieval_escalation=True,
            deterministic=True,
        )
