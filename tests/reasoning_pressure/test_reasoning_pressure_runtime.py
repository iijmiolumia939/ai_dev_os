from __future__ import annotations

from ai_dev_os.reasoning_scope.reasoning_pressure import ReasoningPressurePolicy
from ai_dev_os.reasoning_scope.reasoning_recommendation import ReasoningRecommendationPolicy


def test_tc_reasoningscope_07_pressure_recommends_premium_reasoning_avoidance() -> None:
    pressure = ReasoningPressurePolicy().evaluate(
        requested_depth=5,
        depth_cap=1,
        requested_runtime_count=6,
        neighborhood_cap=1,
        repeated_architecture_sections=2,
        escalation_requested=True,
    )
    recommendation = ReasoningRecommendationPolicy().recommend(
        complexity="LOW",
        pressure=pressure,
    )

    assert pressure.deep_reasoning_explosion_detection is True
    assert pressure.unnecessary_escalation_detection is True
    assert pressure.broad_synthesis_pressure is True
    assert pressure.repeated_architecture_reasoning_detection is True
    assert pressure.estimated_premium_reasoning_burn > 0
    assert pressure.estimated_unnecessary_architecture_reasoning > 0
    assert recommendation.downgrade_to_local_recommendation is True
    assert recommendation.compact_patch_session_recommendation is True
    assert recommendation.premium_reasoning_avoidance_recommendation is True
