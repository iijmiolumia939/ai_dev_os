from __future__ import annotations

from ai_dev_os.dev_execution import (
    DEV_EXECUTION_REQUIREMENT_IDS,
    DEV_EXECUTION_TEST_IDS,
    DevelopmentExecutionRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_devexecution_01_runtime_is_bounded_and_human_confirmed() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()

    assert "FR-DEVEXECUTION-01" in DEV_EXECUTION_REQUIREMENT_IDS
    assert "FR-DEVEXECUTION-12" in DEV_EXECUTION_REQUIREMENT_IDS
    assert "NFR-COST-25" in DEV_EXECUTION_REQUIREMENT_IDS
    assert "TC-DEVEXECUTION-01" in DEV_EXECUTION_TEST_IDS
    assert frame.dev_execution_active is True
    assert frame.bounded_execution_only is True
    assert frame.human_confirmed_execution_only is True
    assert frame.no_autonomous_coding_authority is True
    assert frame.no_hidden_repository_mutation is True
    assert frame.no_recursive_execution_expansion is True


def test_tc_devexecution_02_recommendations_are_compact_non_binding() -> None:
    first = DevelopmentExecutionRuntime().evaluate()
    second = DevelopmentExecutionRuntime().evaluate()

    assert first == second
    assert first.recommendation.non_binding is True
    assert first.recommendation.human_confirmed is True
    assert first.recommendation.compact is True
    assert first.recommendation.deterministic is True
    assert len(first.recommendation.bounded_sequence_recommendations) <= 4
    assert first.local_only is True
    assert first.summary_only is True


def test_tc_devexecution_03_runtime_audit_reports_execution_flags() -> None:
    report = run_runtime_enforcement_audit().dev_execution

    assert report.dev_execution_active is True
    assert report.execution_plan_active is True
    assert report.execution_checkpoint_active is True
    assert report.execution_validation_active is True
    assert report.execution_rollback_active is True
    assert report.execution_pacing_active is True
    assert report.execution_scope_active is True
    assert report.execution_failure_active is True
    assert report.execution_eviction_active is True
    assert report.estimated_avoided_execution_overhead == 3960
    assert report.estimated_avoided_execution_explosion == 3280


def test_tc_devexecution_04_plan_is_adjacent_runtime_and_provider_aware() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    plan = frame.plan

    assert plan.compact_stage_count == 5
    assert "checkpoint_before_validation" in plan.implementation_sequence
    assert "targeted_tests_before_full_suite" in plan.validation_ordering
    assert "HIGH_for_rollback_and_governance" in plan.provider_pacing
    assert plan.giant_execution_tree_prevented is True
    assert plan.recursive_implementation_expansion_prevented is True
    assert plan.autonomous_roadmap_mutation_prevented is True
