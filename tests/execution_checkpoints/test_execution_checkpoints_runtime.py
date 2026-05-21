from __future__ import annotations

from ai_dev_os.dev_execution import DevelopmentExecutionRuntime


def test_tc_devexecution_05_checkpoint_tracks_safe_progression() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    checkpoint = frame.checkpoint

    assert checkpoint.validation_stability == "WATCH"
    assert checkpoint.sprint_checkpoint_safe is True
    assert "pre_patch_state" in checkpoint.rollback_safe_boundaries
    assert "continue_from_last_validated_stage" in checkpoint.execution_continuity
    assert "do_not_reset_user_changes" in checkpoint.rollback_reminders
    assert "validate_before_expand" in checkpoint.bounded_progression_guidance


def test_tc_devexecution_06_eviction_preserves_compact_execution_heuristics() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    eviction = frame.eviction

    assert eviction.execution_eviction_active is True
    assert eviction.compact_useful_execution_heuristics_only is True
    assert eviction.evicted_stale_execution_plans == ("stale-plan-alpha",)
    assert eviction.evicted_oversized_execution_history == ("giant-execution-history",)
    assert "checkpoint_before_validation" in eviction.preserved_compact_execution_heuristics


def test_tc_devexecution_07_stability_keeps_rollback_safe_local_patch() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    stability = frame.stability

    assert stability.execution_stability == "STABLE"
    assert stability.checkpoint_ready is True
    assert stability.validation_stable is True
    assert stability.rollback_safe is True
    assert stability.local_patch_sustainable is True
    assert stability.provider_routing_governed is True
    assert stability.human_confirmed_execution is True
