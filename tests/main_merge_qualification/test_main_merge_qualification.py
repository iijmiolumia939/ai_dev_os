from __future__ import annotations

from ai_dev_os.main_merge_qualification import (
    MAIN_MERGE_QUALIFICATION_REQUIREMENT_IDS,
    MAIN_MERGE_QUALIFICATION_TEST_IDS,
    MAX_QUALIFICATION_HISTORY,
    MAX_QUALIFICATION_WINDOW,
    QUALIFICATION_BUDGET_LIMIT,
    MainMergeQualificationRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_mainmergequalification_01_active_runtime_is_bounded_local_patch() -> None:
    frame = MainMergeQualificationRuntime().evaluate()

    assert frame.main_merge_qualification_active is True
    assert frame.requirement_ids == MAIN_MERGE_QUALIFICATION_REQUIREMENT_IDS
    assert frame.test_ids == MAIN_MERGE_QUALIFICATION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.main_merge_qualification_mode == "LOCAL_PATCH_BOUNDED_MAIN_MERGE_QUALIFICATION"


def test_tc_mainmergequalification_02_merge_readiness_evaluation() -> None:
    frame = MainMergeQualificationRuntime().evaluate(
        validation_readiness=0,
        orchestration_readiness=1,
        runtime_stability_readiness=1,
        bounded_merge_qualification=1,
    )

    assert frame.merge_readiness.merge_readiness_active is True
    assert frame.merge_readiness_score < 60
    assert frame.merge_readiness.bounded_merge_readiness_recommendation == (
        "DEFER_MAIN_MERGE_FOR_READINESS"
    )


def test_tc_mainmergequalification_03_governance_completeness_evaluation() -> None:
    frame = MainMergeQualificationRuntime().evaluate(
        governance_completeness=0,
        policy_coherence=1,
        hardening_completeness=1,
        bounded_governance_drift=3,
    )

    assert frame.governance_completeness.governance_completeness_active is True
    assert frame.governance_completeness_score < 60
    assert frame.governance_completeness.bounded_governance_recommendation == (
        "COMPLETE_GOVERNANCE_BEFORE_MERGE"
    )


def test_tc_mainmergequalification_04_validation_completeness_evaluation() -> None:
    frame = MainMergeQualificationRuntime().evaluate(
        validation_completeness=0,
        runtime_coverage_completeness=1,
        soak_failure_validation_continuity=1,
        bounded_validation_drift=3,
    )

    assert frame.validation_completeness.validation_completeness_active is True
    assert frame.validation_completeness_score < 60
    assert frame.validation_completeness.bounded_validation_recommendation == (
        "COMPLETE_VALIDATION_BEFORE_MERGE"
    )


def test_tc_mainmergequalification_05_runtime_coherence_evaluation() -> None:
    frame = MainMergeQualificationRuntime().evaluate(
        orchestration_coherence=0,
        provider_policy_coherence=1,
        continuation_retry_coherence=1,
        runtime_ecosystem_bounded_coherence=1,
    )

    assert frame.runtime_coherence.runtime_coherence_active is True
    assert frame.runtime_coherence_score < 60
    assert frame.runtime_coherence.bounded_runtime_coherence_recommendation == (
        "RESTORE_RUNTIME_COHERENCE_BEFORE_MERGE"
    )


def test_tc_mainmergequalification_06_operational_risk_evaluation() -> None:
    frame = MainMergeQualificationRuntime().evaluate(
        runtime_collapse_risk=3,
        orchestration_drift_risk=3,
        provider_degradation_risk=3,
        frontier_escalation_risk=3,
    )

    assert frame.operational_risk.operational_risk_active is True
    assert frame.operational_risk_score < 60
    assert frame.operational_risk.bounded_operational_risk_recommendation == (
        "BOUND_OPERATIONAL_RISK_BEFORE_MERGE"
    )


def test_tc_mainmergequalification_07_recursive_qualification_blocking() -> None:
    frame = MainMergeQualificationRuntime().evaluate(recursive_qualification_attempts=1)

    assert frame.qualification_governance.recursive_qualification_blocked is True
    assert frame.qualification_termination.recursive_qualification_detected is True
    assert (
        "RECURSIVE_QUALIFICATION_DETECTED" in frame.qualification_termination.termination_reasons
    )


def test_tc_mainmergequalification_08_qualification_governance_enforcement() -> None:
    frame = MainMergeQualificationRuntime().evaluate(
        autonomous_merge_attempts=1,
        novel_governance_system_synthesis_attempts=1,
        dynamic_qualification_scope_widening_attempts=1,
        governance_policy_mutation_attempts=1,
        hidden_merge_orchestration_attempts=1,
    )

    assert frame.qualification_governance.local_patch_scope_enforced is True
    assert frame.qualification_governance.deterministic_qualification_enforced is True
    assert frame.qualification_governance.autonomous_merge_blocked is True
    assert frame.qualification_governance.novel_governance_system_synthesis_blocked is True
    assert frame.qualification_governance.dynamic_qualification_scope_widening_blocked is True
    assert frame.qualification_governance.hidden_merge_orchestration_blocked is True
    assert frame.qualification_termination.governance_violation_detected is True


def test_tc_mainmergequalification_09_qualification_termination_handling() -> None:
    history = tuple(f"history_{index}" for index in range(12))
    scope = tuple(f"scope_{index}" for index in range(12))
    frame = MainMergeQualificationRuntime().evaluate(
        qualification_history_items=history,
        qualification_scope_items=scope,
        qualification_budget_used=QUALIFICATION_BUDGET_LIMIT + 1,
        validation_readiness=0,
        runtime_collapse_risk=3,
        orchestration_coherence=0,
    )

    assert frame.qualification_termination.main_merge_qualification_terminated is True
    assert frame.qualification_termination.qualification_budget_exceeded is True
    assert frame.qualification_termination.qualification_saturation_threshold_exceeded is True
    assert "QUALIFICATION_BUDGET_EXCEEDED" in frame.qualification_termination.termination_reasons


def test_tc_mainmergequalification_10_bounded_qualification_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    scope = tuple(f"scope_{index}" for index in range(9))
    frame = MainMergeQualificationRuntime().evaluate(
        qualification_history_items=history,
        qualification_scope_items=scope,
    )

    assert len(frame.qualification_history.qualification_history) == MAX_QUALIFICATION_HISTORY
    assert len(frame.qualification_history.qualification_scope) == MAX_QUALIFICATION_WINDOW
    assert frame.qualification_history.qualification_history_overflow_blocked is True
    assert frame.qualification_history.qualification_scope_overflow_blocked is True
    assert (
        frame.qualification_eviction.evicted_qualification_history_items
        == history[MAX_QUALIFICATION_HISTORY:]
    )
    assert (
        frame.qualification_eviction.evicted_qualification_scope_items
        == scope[MAX_QUALIFICATION_WINDOW:]
    )


def test_tc_mainmergequalification_11_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().main_merge_qualification

    assert report.main_merge_qualification_active is True
    assert 0 <= report.merge_readiness_score <= 100
    assert 0 <= report.governance_completeness_score <= 100
    assert 0 <= report.validation_completeness_score <= 100
    assert 0 <= report.runtime_coherence_score <= 100
    assert 0 <= report.operational_risk_score <= 100
    assert report.estimated_avoided_merge_regression > 0
    assert report.estimated_avoided_runtime_instability > 0
    assert report.estimated_avoided_frontier_dependency > 0


def test_tc_mainmergequalification_12_runtime_is_deterministic() -> None:
    first = MainMergeQualificationRuntime().evaluate()
    second = MainMergeQualificationRuntime().evaluate()

    assert first == second
    assert first.qualification_confidence.deterministic_confidence is True
    assert first.qualification_confidence.merge_readiness_confidence is True
    assert first.qualification_governance.autonomous_merge_blocked is True
