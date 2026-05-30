from __future__ import annotations

from ai_dev_os.runtime_audit import (
    ReleaseCheckInputs,
    audit_validation_evidence,
    run_runtime_enforcement_audit,
)
from ai_dev_os.validation_evidence import (
    MAX_EVIDENCE_HISTORY_RETENTION,
    SUPPORTED_VALIDATION_EVIDENCE_STATUSES,
    ValidationEvidenceRuntime,
)


def test_failed_mapping_is_deterministic() -> None:
    frame = ValidationEvidenceRuntime().evaluate(
        pytest_passed=False,
        ruff_passed=True,
        audit_passed=False,
        diff_check_passed=False,
        unresolved_validation_issues=2,
        unresolved_audit_issues=1,
    )

    assert frame.status == "FAILED"
    assert frame.validation_passed is False
    assert frame.reasons == (
        "PYTEST_FAILED",
        "AUDIT_FAILED",
        "DIFF_CHECK_FAILED",
        "UNRESOLVED_VALIDATION_ISSUES",
        "UNRESOLVED_AUDIT_ISSUES",
    )


def test_passed_mapping_is_deterministic() -> None:
    frame = ValidationEvidenceRuntime().evaluate(
        pytest_passed=True,
        ruff_passed=True,
        audit_passed=True,
        diff_check_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
    )

    assert frame.status == "PASSED"
    assert frame.validation_passed is True
    assert frame.reasons == ("VALIDATION_COMPLETE",)


def test_passed_with_warnings_mapping_is_deterministic() -> None:
    frame = ValidationEvidenceRuntime().evaluate(
        pytest_passed=True,
        ruff_passed=True,
        audit_passed=True,
        diff_check_passed=True,
        unresolved_validation_issues=1,
        unresolved_audit_issues=2,
    )

    assert frame.status == "PASSED_WITH_WARNINGS"
    assert frame.validation_passed is True
    assert frame.reasons == (
        "UNRESOLVED_VALIDATION_ISSUES",
        "UNRESOLVED_AUDIT_ISSUES",
        "VALIDATION_COMPLETE",
    )


def test_validation_passed_tracks_status_contract() -> None:
    failed = ValidationEvidenceRuntime().evaluate(
        pytest_passed=False,
        ruff_passed=True,
        audit_passed=True,
        diff_check_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
    )
    warnings = ValidationEvidenceRuntime().evaluate(
        pytest_passed=True,
        ruff_passed=True,
        audit_passed=True,
        diff_check_passed=True,
        unresolved_validation_issues=1,
        unresolved_audit_issues=0,
    )
    passed = ValidationEvidenceRuntime().evaluate(
        pytest_passed=True,
        ruff_passed=True,
        audit_passed=True,
        diff_check_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
    )

    assert failed.validation_passed is False
    assert warnings.validation_passed is True
    assert passed.validation_passed is True


def test_bounded_history_retention_and_deterministic_eviction() -> None:
    history = tuple(f"evidence-{index}" for index in range(6))
    frame = ValidationEvidenceRuntime().evaluate(
        pytest_passed=True,
        ruff_passed=True,
        audit_passed=True,
        diff_check_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
        evidence_history=history,
    )

    combined = history + (
        "status=PASSED;validation_passed=true;pytest=true;ruff=true;"
        "audit=true;diff=true;validation_issues=0;audit_issues=0",
    )
    assert frame.retention_limit == MAX_EVIDENCE_HISTORY_RETENTION
    assert frame.retained_evidence_history == combined[-MAX_EVIDENCE_HISTORY_RETENTION:]
    assert frame.evicted_evidence_history == combined[:-MAX_EVIDENCE_HISTORY_RETENTION]
    assert frame.evicted_evidence_history == ("evidence-0", "evidence-1", "evidence-2")
    assert frame.bounded is True
    assert frame.no_provider_calls is True
    assert frame.no_filesystem_access is True
    assert frame.no_process_execution is True
    assert frame.no_git_operations is True
    assert frame.no_autonomous_execution is True


def test_runtime_audit_projection_exposes_validation_evidence() -> None:
    report = run_runtime_enforcement_audit()
    validation_evidence = report.validation_evidence
    repository_readiness = report.repository_readiness

    assert validation_evidence.validation_evidence_active is True
    assert validation_evidence.status in SUPPORTED_VALIDATION_EVIDENCE_STATUSES
    assert validation_evidence.validation_passed is True
    assert validation_evidence.reasons == (
        "PYTEST_NOT_PROVIDED",
        "RUFF_NOT_PROVIDED",
        "AUDIT_NOT_PROVIDED",
        "DIFF_CHECK_NOT_PROVIDED",
        "RELEASE_CHECK_INPUTS_INCOMPLETE",
    )
    assert len(validation_evidence.retained_evidence_history) <= MAX_EVIDENCE_HISTORY_RETENTION
    assert repository_readiness.pytest_passed == validation_evidence.pytest_passed
    assert repository_readiness.ruff_passed == validation_evidence.ruff_passed
    assert repository_readiness.diff_check_passed == validation_evidence.diff_check_passed
    assert repository_readiness.audit_passed == validation_evidence.audit_passed
    assert (
        repository_readiness.unresolved_validation_issues
        == validation_evidence.unresolved_validation_issues
    )
    assert (
        repository_readiness.unresolved_audit_issues
        == validation_evidence.unresolved_audit_issues
    )


def test_runtime_audit_absent_release_check_inputs_do_not_pass_validation() -> None:
    frame = audit_validation_evidence()

    assert frame.status == "PASSED_WITH_WARNINGS"
    assert frame.validation_passed is True
    assert frame.pytest_passed is None
    assert frame.ruff_passed is None
    assert frame.audit_passed is None
    assert frame.diff_check_passed is None


def test_runtime_audit_failed_ruff_produces_failed_validation() -> None:
    frame = audit_validation_evidence(
        release_check_inputs=ReleaseCheckInputs(
            pytest_passed=True,
            ruff_passed=False,
            audit_passed=True,
            diff_check_passed=True,
        )
    )

    assert frame.status == "FAILED"
    assert frame.validation_passed is False
    assert "RUFF_FAILED" in frame.reasons


def test_runtime_audit_explicit_passed_release_check_inputs_produce_passed_validation() -> None:
    report = run_runtime_enforcement_audit(
        release_check_inputs=ReleaseCheckInputs(
            pytest_passed=True,
            ruff_passed=True,
            audit_passed=True,
            diff_check_passed=True,
        )
    )

    assert report.validation_evidence.status == "PASSED"
    assert report.validation_evidence.validation_passed is True
    assert report.validation_evidence.reasons == ("VALIDATION_COMPLETE",)
