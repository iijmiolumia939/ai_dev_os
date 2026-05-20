from __future__ import annotations

from ai_dev_os.reasoning_routing.task_complexity import (
    TaskComplexityInput,
    TaskComplexityPolicy,
)


def test_tc_reasoning_01_task_complexity_outputs_bounded_metadata() -> None:
    frame = TaskComplexityPolicy().evaluate(
        TaskComplexityInput(
            architecture_density=3,
            cross_runtime_scope=2,
            continuity_size=2,
            reasoning_depth=3,
            dependency_breadth=2,
            governance_sensitivity=3,
            runtime_authority_risk=1,
        )
    )

    assert frame.complexity_level == "HIGH"
    assert frame.reasoning_recommendation == "HIGH"
    assert frame.escalation_required is True
    assert frame.estimated_reasoning_burn > 0
    assert frame.bounded_metadata is True


def test_tc_reasoning_05_task_complexity_is_deterministic_and_bounded() -> None:
    data = TaskComplexityInput(
        architecture_density=99,
        cross_runtime_scope=99,
        continuity_size=99,
        reasoning_depth=99,
        dependency_breadth=99,
        governance_sensitivity=99,
        runtime_authority_risk=99,
    )

    first = TaskComplexityPolicy().evaluate(data)
    second = TaskComplexityPolicy().evaluate(data)

    assert first == second
    assert set(first.scoring_breakdown.values()) == {3}
    assert first.complexity_level == "HIGH"
