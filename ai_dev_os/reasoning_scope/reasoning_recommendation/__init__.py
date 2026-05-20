from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.reasoning_scope.reasoning_pressure import ReasoningPressureFrame


@dataclass(frozen=True)
class ReasoningRecommendationFrame:
    downgrade_to_local_recommendation: bool
    downgrade_to_medium_depth_recommendation: bool
    compact_patch_session_recommendation: bool
    isolated_architecture_session_recommendation: bool
    premium_reasoning_avoidance_recommendation: bool
    recommended_next_action: str
    summary_only: bool
    deterministic: bool


class ReasoningRecommendationPolicy:
    def recommend(
        self,
        *,
        complexity: str,
        pressure: ReasoningPressureFrame,
        architecture_sensitive: bool = False,
    ) -> ReasoningRecommendationFrame:
        normalized = complexity.upper()
        downgrade_local = normalized == "LOW" or pressure.unnecessary_escalation_detection
        downgrade_medium = normalized == "MEDIUM" and pressure.deep_reasoning_explosion_detection
        isolated = normalized == "HIGH" and architecture_sensitive
        if downgrade_local:
            action = "use_local_patch_mode"
        elif downgrade_medium:
            action = "cap_reasoning_at_medium_depth"
        elif isolated:
            action = "open_isolated_architecture_session"
        else:
            action = "continue_compact_reasoning"
        return ReasoningRecommendationFrame(
            downgrade_to_local_recommendation=downgrade_local,
            downgrade_to_medium_depth_recommendation=downgrade_medium,
            compact_patch_session_recommendation=normalized in {"LOW", "MEDIUM"},
            isolated_architecture_session_recommendation=isolated,
            premium_reasoning_avoidance_recommendation=(
                pressure.premium_reasoning_avoidance_recommended
            ),
            recommended_next_action=action,
            summary_only=True,
            deterministic=True,
        )
