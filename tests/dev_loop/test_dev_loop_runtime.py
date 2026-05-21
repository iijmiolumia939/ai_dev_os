from __future__ import annotations

from ai_dev_os.dev_loop import DEV_LOOP_REQUIREMENT_IDS, DEV_LOOP_TEST_IDS, SprintDevLoopRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_aidevloop_01_planning_is_bounded_and_local_patch() -> None:
    frame = SprintDevLoopRuntime().evaluate(objective_seed="ship sprint runtime")

    assert "FR-AIDEVLOOP-01" in DEV_LOOP_REQUIREMENT_IDS
    assert "TC-AIDEVLOOP-01" in DEV_LOOP_TEST_IDS
    assert frame.planning.bounded_sprint_objective.startswith("Bounded sprint:")
    assert frame.planning.local_patch_recommendation is True
    assert frame.planning.no_roadmap_explosion is True
    assert frame.planning.no_repo_wide_sprint_synthesis is True
    assert frame.planning.no_giant_architecture_replay is True
    assert frame.planning.no_autonomous_scope_expansion is True


def test_tc_aidevloop_02_scope_complexity_and_provider_routing_are_bounded() -> None:
    frame = SprintDevLoopRuntime().evaluate(architecture_sensitive=True)

    assert frame.scope.adjacent_runtime_scope == (
        "dev_loop",
        "session_orchestrator",
        "provider_routing",
    )
    assert frame.scope.repo_wide_synthesis_forbidden is True
    assert frame.complexity.provider_routing_recommendation == "HIGH"
    assert frame.complexity.retrieval_radius_recommendation == 2
    assert frame.complexity.no_hidden_provider_switching is True
    assert frame.provider_routing_distribution == {"HIGH": 3, "MEDIUM": 3, "LOW": 3}


def test_tc_aidevloop_03_runtime_audit_reports_dev_loop_flags() -> None:
    report = run_runtime_enforcement_audit().dev_loop

    assert report.dev_loop_active is True
    assert report.sprint_planning_active is True
    assert report.sprint_lifecycle_active is True
    assert report.sprint_rollover_active is True
    assert report.sprint_bootstrap_active is True
    assert report.sprint_governance_active is True
    assert report.estimated_avoided_manual_orchestration_tokens > 0
    assert report.estimated_avoided_sprint_explosion > 0
    assert report.no_hidden_provider_switching is True
