from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.incremental_context.incremental_pressure import IncrementalPressureFrame


@dataclass(frozen=True)
class IncrementalRecommendationFrame:
    delta_only_session_recommendation: bool
    compact_incremental_continuation_recommendation: str
    repeated_context_downgrade_recommendation: bool
    unchanged_runtime_suppression_recommendation: bool
    architecture_isolation_preservation: bool
    recommended_next_action: str
    summary_only: bool
    deterministic: bool


class IncrementalRecommendationPolicy:
    def recommend(
        self,
        *,
        pressure: IncrementalPressureFrame,
        unchanged_runtimes: tuple[str, ...],
        architecture_isolation: bool,
    ) -> IncrementalRecommendationFrame:
        downgrade = pressure.pressure_level in {"MEDIUM", "HIGH"}
        action = "continue_with_delta_only_context" if downgrade else "continue_incrementally"
        return IncrementalRecommendationFrame(
            delta_only_session_recommendation=True,
            compact_incremental_continuation_recommendation=action,
            repeated_context_downgrade_recommendation=downgrade,
            unchanged_runtime_suppression_recommendation=bool(unchanged_runtimes),
            architecture_isolation_preservation=architecture_isolation,
            recommended_next_action=action,
            summary_only=True,
            deterministic=True,
        )
