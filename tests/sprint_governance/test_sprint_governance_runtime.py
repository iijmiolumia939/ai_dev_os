from __future__ import annotations

from ai_dev_os.dev_loop import SprintDevLoopRuntime


def test_tc_aidevloop_07_next_sprint_proposal_blocks_branching() -> None:
    frame = SprintDevLoopRuntime().evaluate(completed_sprint_count=4)

    assert frame.proposal.adjacent_runtime_only_continuation == (
        "dev_loop",
        "session_orchestrator",
    )
    assert frame.proposal.provider_aware_implementation_recommendation == "LOW"
    assert frame.proposal.infinite_sprint_chaining_prevented is True
    assert frame.proposal.giant_roadmap_branching_prevented is True
    assert frame.proposal.architecture_wide_planning_forbidden is True


def test_tc_aidevloop_08_bootstrap_is_enter_only_and_bounded() -> None:
    frame = SprintDevLoopRuntime().evaluate(validation_passed=True)

    assert frame.bootstrap.enter_only_continuation_workflow is True
    assert frame.bootstrap.bounded_bootstrap_payload is True
    assert frame.bootstrap.provider_aware_bootstrap_summary is True
    assert "LOCAL_PATCH_REQUIRED" in frame.bootstrap.local_patch_reminder
    assert "hidden_switching=forbidden" in frame.bootstrap.provider_routing_summary


def test_tc_aidevloop_09_governance_tracks_pressures_and_downgrades() -> None:
    frame = SprintDevLoopRuntime().evaluate(
        lifecycle_state="VALIDATING",
        validation_passed=False,
        stale_sprints=("old-sprint",),
    )

    assert frame.governance.sprint_explosion_pressure in {"LOW", "MEDIUM", "HIGH"}
    assert frame.governance.cognition_expansion_pressure in {"LOW", "MEDIUM", "HIGH"}
    assert frame.governance.provider_escalation_pressure in {"LOW", "MEDIUM", "HIGH"}
    assert frame.governance.roadmap_branching_pressure == "LOW"
    assert "prefer_LOW_for_closure" in frame.governance.downgrade_recommendations
    assert "LOCAL_PATCH_REQUIRED" in frame.governance.local_patch_enforcement_reminders


def test_tc_aidevloop_10_runtime_preserves_anti_explosion_invariants() -> None:
    first = SprintDevLoopRuntime().evaluate()
    second = SprintDevLoopRuntime().evaluate()

    assert first == second
    assert first.dev_loop_active is True
    assert first.local_only is True
    assert first.deterministic is True
    assert first.summary_only is True
    assert first.bounded_cognition_only is True
    assert first.human_confirmed_orchestration_only is True
    assert first.no_autonomous_roadmap_expansion is True
    assert first.no_hidden_provider_switching is True
    assert first.no_giant_continuity_replay is True
