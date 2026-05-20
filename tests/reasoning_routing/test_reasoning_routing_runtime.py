from __future__ import annotations

from ai_dev_os.reasoning_routing import SprintReasoningRouter, SprintReasoningTask
from ai_dev_os.reasoning_routing.escalation_policy import EscalationPolicy, EscalationPolicyInput
from ai_dev_os.reasoning_routing.quality_floor import QualityFloorPolicy
from ai_dev_os.reasoning_routing.reasoning_tiers import ReasoningTask, ReasoningTierPolicy


def test_tc_reasoning_01_tier_classification_validation() -> None:
    policy = ReasoningTierPolicy()

    architecture = policy.classify(
        ReasoningTask(
            "architecture",
            "architecture rollout strategy runtime boundary design",
            architecture_sensitive=True,
        )
    )
    adapter = policy.classify(
        ReasoningTask("adapter wiring", "runtime integration adapters orchestration wiring")
    )
    docs = policy.classify(ReasoningTask("docs", "markdown checklist generation"))

    assert architecture.recommended_tier == "HIGH"
    assert adapter.recommended_tier == "MEDIUM"
    assert docs.recommended_tier == "LOW"
    assert architecture.human_visible is True
    assert architecture.provider_neutral is True


def test_tc_reasoning_02_escalation_is_bounded_and_visible() -> None:
    frame = EscalationPolicy(max_escalations_per_sprint=1).evaluate(
        EscalationPolicyInput(
            recommended_tier="HIGH",
            complexity_level="HIGH",
            escalation_required=True,
            quality_floor_tier="LOW",
            previous_escalations=1,
            cooldown_remaining=2,
        )
    )

    assert frame.escalation_required is True
    assert frame.high_reasoning_allowed is False
    assert frame.cooldown_active is True
    assert frame.human_visible_escalation is True
    assert frame.rollback_safe_escalation is True


def test_tc_reasoning_03_no_hidden_escalation_or_provider_switching() -> None:
    frame = EscalationPolicy().evaluate(
        EscalationPolicyInput(
            recommended_tier="MEDIUM",
            complexity_level="MEDIUM",
            escalation_required=False,
            quality_floor_tier="LOW",
        )
    )

    assert frame.escalation_required is False
    assert frame.hidden_provider_switching is False
    assert frame.human_visible_escalation is True


def test_tc_reasoning_05_quality_floor_blocks_unsafe_downgrade() -> None:
    frame = QualityFloorPolicy().enforce(
        "LOW",
        architecture_protection=True,
        governance_protection=True,
        embodiment_protection=True,
    )

    assert frame.selected_tier == "HIGH"
    assert frame.minimum_reasoning_floor == "HIGH"
    assert frame.unsafe_downgrade_blocked is True


def test_tc_reasoning_01_sprint_reasoning_map_is_deterministic() -> None:
    tasks = (
        SprintReasoningTask(
            "architecture",
            "architecture rollout strategy runtime boundary design",
            architecture_sensitive=True,
        ),
        SprintReasoningTask("runtime tests", "repetitive tests deterministic snapshots"),
        SprintReasoningTask("docs", "markdown checklist generation"),
        SprintReasoningTask("adapter wiring", "runtime integration adapters orchestration wiring"),
    )
    first = SprintReasoningRouter().map("42", tasks)
    second = SprintReasoningRouter().map("42", tasks)

    assert first == second
    assert first.task_tiers == {
        "architecture": "HIGH",
        "runtime tests": "LOW",
        "docs": "LOW",
        "adapter wiring": "MEDIUM",
    }
    assert first.human_visible_routing is True
    assert first.rollback_safe_routing is True
