from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.subagent_execution import (
    SUBAGENT_EXECUTION_REQUIREMENT_IDS,
    SUBAGENT_EXECUTION_TEST_IDS,
    SubagentExecutionRuntime,
)


def test_tc_subagentexec_01_runtime_is_bounded_and_human_confirmed() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert "FR-SUBAGENTEXEC-01" in SUBAGENT_EXECUTION_REQUIREMENT_IDS
    assert "FR-SUBAGENTEXEC-14" in SUBAGENT_EXECUTION_REQUIREMENT_IDS
    assert "NFR-COST-26" in SUBAGENT_EXECUTION_REQUIREMENT_IDS
    assert "NFR-ARCH-40" in SUBAGENT_EXECUTION_REQUIREMENT_IDS
    assert "NFR-SEC-11" in SUBAGENT_EXECUTION_REQUIREMENT_IDS
    assert "TC-SUBAGENTEXEC-01" in SUBAGENT_EXECUTION_TEST_IDS
    assert frame.subagent_execution_active is True
    assert frame.bounded_delegation_only is True
    assert frame.human_confirmed_delegation_only is True
    assert frame.no_autonomous_agent_swarms is True
    assert frame.no_recursive_subagent_spawning is True
    assert frame.no_autonomous_repository_mutation is True


def test_tc_subagentexec_02_payload_is_compact_local_patch_delta_only() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.payload.max_payload_tokens <= 1600
    assert frame.payload.adjacent_runtime_only is True
    assert frame.payload.delta_only_continuity is True
    assert frame.payload.local_patch_scope is True
    assert frame.payload.repo_wide_replay_prevented is True
    assert frame.payload.full_sprint_history_prevented is True
    assert frame.scope.local_patch_only is True
    assert frame.scope.retrieval_radius == 2


def test_tc_subagentexec_03_runtime_audit_reports_subagent_flags() -> None:
    report = run_runtime_enforcement_audit().subagent_execution

    assert report.subagent_execution_active is True
    assert report.subagent_payload_active is True
    assert report.subagent_validation_active is True
    assert report.subagent_scope_active is True
    assert report.subagent_eviction_active is True
    assert report.estimated_avoided_premium_subagent_tokens > 0
    assert report.estimated_avoided_recursive_agent_explosion > 0


def test_tc_subagentexec_04_runtime_is_deterministic() -> None:
    first = SubagentExecutionRuntime().evaluate()
    second = SubagentExecutionRuntime().evaluate()

    assert first == second
    assert first.deterministic is True
    assert first.summary_only is True
