from __future__ import annotations

from ai_dev_os.dev_policy import DevelopmentPolicyRuntime


def test_tc_devpolicy_07_embodiment_policy_protects_low_motion_realism() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    embodiment = frame.embodiment

    assert embodiment.animation_authority_creep is True
    assert embodiment.exaggerated_reaction_escalation is True
    assert embodiment.procedural_acting_pressure is True
    assert "prefer_low_motion_presence" in embodiment.low_motion_realism_reminders
    assert "preserve_subtle_reaction_band" in embodiment.subtle_continuity_recommendations
    assert embodiment.theatrical_embodiment_escalation_prevented is True
    assert embodiment.procedural_acting_systems_prevented is True
    assert embodiment.autonomous_social_scripting_prevented is True


def test_tc_devpolicy_08_bounded_cognition_policy_blocks_giant_replay() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    cognition = frame.cognition

    assert cognition.repo_wide_reasoning_attempts == 1
    assert cognition.giant_continuity_payloads == 1
    assert cognition.oversized_sprint_synthesis_attempts == 1
    assert cognition.retrieval_explosion_patterns == 1
    assert cognition.recursive_planning_attempts == 1
    assert "delta_only_governance" in cognition.delta_only_reminders
    assert cognition.giant_cognition_replay_prevented is True
    assert cognition.hidden_memory_accumulation_prevented is True
    assert cognition.recursive_roadmap_synthesis_prevented is True


def test_tc_devpolicy_09_rollout_safety_policy_blocks_hidden_migration() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    rollout = frame.rollout

    assert rollout.rollout_friction == "MEDIUM"
    assert rollout.stale_extension_state is True
    assert rollout.continuity_mismatch is True
    assert rollout.unsafe_migration_attempts == 1
    assert "keep_rollback_file_level" in rollout.rollback_safe_recommendations
    assert rollout.unsafe_rollout_escalation_prevented is True
    assert rollout.hidden_migration_mutations_prevented is True
    assert rollout.uncontrolled_rollout_automation_prevented is True
