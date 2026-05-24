from __future__ import annotations

from dataclasses import fields

from ai_dev_os.main_merge_rehearsal import (
    MAIN_MERGE_REHEARSAL_REQUIREMENT_IDS,
    MAIN_MERGE_REHEARSAL_TEST_IDS,
    MAX_REHEARSAL_HISTORY,
    MAX_REHEARSAL_WINDOW,
    REHEARSAL_BUDGET_LIMIT,
    MainMergeRehearsalRuntime,
)
from ai_dev_os.runtime_audit import MainMergeRehearsalAuditReport, run_runtime_enforcement_audit


def test_tc_mainmergerehearsal_01_protected_branch_rehearsal() -> None:
    frame = MainMergeRehearsalRuntime().evaluate(
        protected_branch_readiness=0,
        branch_policy_readiness=1,
        bounded_merge_gate_survivability=1,
        bounded_governance_continuity=1,
    )

    assert frame.main_merge_rehearsal_active is True
    assert frame.requirement_ids == MAIN_MERGE_REHEARSAL_REQUIREMENT_IDS
    assert frame.test_ids == MAIN_MERGE_REHEARSAL_TEST_IDS
    assert frame.protected_branch_readiness_score < 60
    assert frame.protected_branch_readiness.bounded_protected_branch_recommendation == (
        "DEFER_MERGE_FOR_PROTECTED_BRANCH_READINESS"
    )
    assert frame.main_merge_rehearsal_mode == "LOCAL_PATCH_BOUNDED_MAIN_MERGE_REHEARSAL"


def test_tc_mainmergerehearsal_02_merge_conflict_visibility() -> None:
    frame = MainMergeRehearsalRuntime().evaluate(
        merge_conflict_visibility=0,
        bounded_conflict_survivability=1,
        runtime_coherence_preservation=1,
        bounded_merge_drift_resistance=1,
        merge_drift=3,
    )

    assert frame.merge_conflict_audit.merge_conflict_audit_active is True
    assert frame.merge_conflict_visibility_score < 60
    assert frame.merge_conflict_audit.bounded_conflict_recommendation == (
        "IMPROVE_CONFLICT_VISIBILITY_BEFORE_MERGE"
    )


def test_tc_mainmergerehearsal_03_rollback_survivability() -> None:
    frame = MainMergeRehearsalRuntime().evaluate(
        rollback_survivability=0,
        rollback_runtime_coherence=1,
        rollback_governance_continuity=1,
        rollback_operational_stability=1,
        rollback_drift=3,
    )

    assert frame.merge_rollback_readiness.merge_rollback_readiness_active is True
    assert frame.rollback_survivability_score < 60
    assert frame.merge_rollback_readiness.bounded_rollback_recommendation == (
        "REHEARSE_ROLLBACK_SURVIVABILITY_BEFORE_MERGE"
    )


def test_tc_mainmergerehearsal_04_post_merge_runtime_survivability() -> None:
    frame = MainMergeRehearsalRuntime().evaluate(
        post_merge_runtime_stability=0,
        post_merge_orchestration_stability=1,
        post_merge_provider_stability=1,
        post_merge_continuation_stability=1,
        post_merge_drift=3,
    )

    assert frame.post_merge_runtime_audit.post_merge_runtime_audit_active is True
    assert frame.post_merge_runtime_score < 60
    assert frame.post_merge_runtime_audit.bounded_post_merge_recommendation == (
        "STABILIZE_POST_MERGE_RUNTIME_BEFORE_MERGE"
    )


def test_tc_mainmergerehearsal_05_ci_readiness_validation() -> None:
    frame = MainMergeRehearsalRuntime().evaluate(
        ci_trigger_readiness=0,
        validation_continuity=1,
        compile_continuity=1,
        bounded_workflow_survivability=1,
        ci_drift=3,
    )

    assert frame.merge_ci_readiness.merge_ci_readiness_active is True
    assert frame.ci_readiness_score < 60
    assert frame.merge_ci_readiness.bounded_ci_recommendation == (
        "RESTORE_CI_READINESS_BEFORE_MERGE"
    )


def test_tc_mainmergerehearsal_06_recursive_rehearsal_blocking() -> None:
    frame = MainMergeRehearsalRuntime().evaluate(recursive_rehearsal_attempts=1)

    assert frame.rehearsal_governance.recursive_rehearsal_blocked is True
    assert frame.rehearsal_termination.recursive_rehearsal_detected is True
    assert "RECURSIVE_REHEARSAL_DETECTED" in frame.rehearsal_termination.termination_reasons


def test_tc_mainmergerehearsal_07_rehearsal_governance_enforcement() -> None:
    frame = MainMergeRehearsalRuntime().evaluate(
        autonomous_merge_attempts=1,
        governance_policy_mutation_attempts=1,
        retrieval_scope_widening_attempts=1,
        novel_merge_strategy_synthesis_attempts=1,
        hidden_background_execution_attempts=1,
        branch_protection_mutation_attempts=1,
        protected_branch_write_attempts=1,
        remote_policy_mutation_attempts=1,
    )

    assert frame.branch_protection_rehearsal.branch_protection_mutation_blocked is True
    assert frame.branch_protection_rehearsal.real_merge_execution_blocked is True
    assert frame.rehearsal_governance.local_patch_scope_enforced is True
    assert frame.rehearsal_governance.autonomous_merge_blocked is True
    assert frame.rehearsal_governance.retrieval_scope_widening_blocked is True
    assert frame.rehearsal_governance.hidden_background_execution_blocked is True
    assert frame.rehearsal_termination.governance_violation_detected is True


def test_tc_mainmergerehearsal_08_rehearsal_termination_handling() -> None:
    history = tuple(f"history_{index}" for index in range(12))
    scope = tuple(f"scope_{index}" for index in range(12))
    frame = MainMergeRehearsalRuntime().evaluate(
        rehearsal_history_items=history,
        rehearsal_scope_items=scope,
        rehearsal_budget_used=REHEARSAL_BUDGET_LIMIT + 1,
        protected_branch_readiness=0,
        merge_conflict_visibility=0,
        rollback_survivability=0,
        post_merge_runtime_stability=0,
        ci_trigger_readiness=0,
    )

    assert frame.rehearsal_termination.main_merge_rehearsal_terminated is True
    assert frame.rehearsal_termination.rehearsal_budget_exceeded is True
    assert frame.rehearsal_termination.rehearsal_saturation_threshold_exceeded is True
    assert "REHEARSAL_BUDGET_EXCEEDED" in frame.rehearsal_termination.termination_reasons


def test_tc_mainmergerehearsal_09_bounded_rehearsal_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    scope = tuple(f"scope_{index}" for index in range(9))
    frame = MainMergeRehearsalRuntime().evaluate(
        rehearsal_history_items=history,
        rehearsal_scope_items=scope,
    )

    assert len(frame.rehearsal_history.rehearsal_history) == MAX_REHEARSAL_HISTORY
    assert len(frame.rehearsal_history.rehearsal_scope) == MAX_REHEARSAL_WINDOW
    assert frame.rehearsal_history.rehearsal_history_overflow_blocked is True
    assert frame.rehearsal_history.rehearsal_scope_overflow_blocked is True
    assert (
        frame.rehearsal_eviction.evicted_rehearsal_history_items == history[MAX_REHEARSAL_HISTORY:]
    )
    assert frame.rehearsal_eviction.evicted_rehearsal_scope_items == scope[MAX_REHEARSAL_WINDOW:]


def test_tc_mainmergerehearsal_10_runtime_audit_exposes_only_required_fields() -> None:
    report = run_runtime_enforcement_audit().main_merge_rehearsal

    assert tuple(field.name for field in fields(MainMergeRehearsalAuditReport)) == (
        "main_merge_rehearsal_active",
        "protected_branch_readiness_score",
        "merge_conflict_visibility_score",
        "rollback_survivability_score",
        "post_merge_runtime_score",
        "ci_readiness_score",
        "estimated_avoided_merge_instability",
        "estimated_avoided_post_merge_regression",
        "estimated_avoided_frontier_recovery",
    )
    assert report.main_merge_rehearsal_active is True
    assert 0 <= report.protected_branch_readiness_score <= 100
    assert 0 <= report.merge_conflict_visibility_score <= 100
    assert 0 <= report.rollback_survivability_score <= 100
    assert 0 <= report.post_merge_runtime_score <= 100
    assert 0 <= report.ci_readiness_score <= 100
    assert report.estimated_avoided_merge_instability > 0
    assert report.estimated_avoided_post_merge_regression > 0
    assert report.estimated_avoided_frontier_recovery > 0


def test_tc_mainmergerehearsal_11_runtime_is_deterministic() -> None:
    first = MainMergeRehearsalRuntime().evaluate()
    second = MainMergeRehearsalRuntime().evaluate()

    assert first == second
    assert first.deterministic is True
    assert first.bounded is True
    assert first.rollback_safe is True
    assert first.governance_preserving is True
    assert first.local_patch_compatible is True
    assert first.rehearsal_confidence.deterministic_confidence is True
