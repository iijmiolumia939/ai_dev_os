from __future__ import annotations

from ai_dev_os.merge_readiness import MergeReadinessFrame
from ai_dev_os.repository_readiness import (
    MAX_REPOSITORY_HISTORY_RETENTION,
    SUPPORTED_REPOSITORY_READINESS_STATUSES,
    SUPPORTED_REPOSITORY_RECOMMENDATIONS,
    RepositoryReadinessRuntime,
)
from ai_dev_os.runtime_audit import ReleaseCheckInputs, run_runtime_enforcement_audit
from ai_dev_os.validation_evidence import ValidationEvidenceRuntime


def _merge_readiness_frame(
    *,
    status: str = "READY",
    recommendation: str = "MERGE_CANDIDATE",
) -> MergeReadinessFrame:
    return MergeReadinessFrame(
        merge_readiness_active=True,
        status=status,
        recommendation=recommendation,
        reasons=("reason",),
        retained_merge_history=(f"status={status}",),
        evicted_merge_history=(),
        retention_limit=4,
        readiness_score=90,
        risk_level="LOW",
        action="NONE",
        blocker_count=0,
        warning_count=0,
        continuation_stability="STABLE",
        operator_status="NORMAL",
        operator_priority="LOW",
        requires_attention=status != "READY",
        deterministic=True,
        bounded=True,
        local_only=True,
        no_provider_calls=True,
        no_autonomous_execution=True,
    )


def test_ready_mapping() -> None:
    frame = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(),
        pytest_passed=True,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
    )

    assert frame.status == "READY"
    assert frame.recommendation == "MERGE_CANDIDATE"
    assert frame.reasons == (
        "MERGE_READY_CONFIRMED",
        "PYTEST_PASSED",
        "RUFF_PASSED",
        "DIFF_CHECK_PASSED",
        "AUDIT_PASSED",
        "NO_UNRESOLVED_VALIDATION_ISSUES",
        "NO_UNRESOLVED_AUDIT_ISSUES",
    )


def test_ready_with_warnings_mapping() -> None:
    frame = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(
            status="READY_WITH_WARNINGS",
            recommendation="REVIEW_BEFORE_MERGE",
        ),
        pytest_passed=True,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=1,
        unresolved_audit_issues=2,
    )

    assert frame.status == "READY_WITH_WARNINGS"
    assert frame.recommendation == "REVIEW_BEFORE_MERGE"
    assert frame.reasons == (
        "MERGE_READY_WITH_WARNINGS",
        "UNRESOLVED_VALIDATION_ISSUES",
        "UNRESOLVED_AUDIT_ISSUES",
    )


def test_not_ready_mapping() -> None:
    frame = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(
            status="NOT_READY",
            recommendation="DO_NOT_MERGE",
        ),
        pytest_passed=False,
        ruff_passed=True,
        diff_check_passed=False,
        audit_passed=False,
        unresolved_validation_issues=3,
        unresolved_audit_issues=1,
    )

    assert frame.status == "NOT_READY"
    assert frame.recommendation == "DO_NOT_MERGE"
    assert frame.reasons == (
        "MERGE_NOT_READY",
        "PYTEST_FAILED",
        "DIFF_CHECK_FAILED",
        "AUDIT_FAILED",
    )


def test_recommendation_mapping_is_deterministic() -> None:
    ready = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(),
        pytest_passed=True,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
    )
    guarded = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(
            status="READY_WITH_WARNINGS",
            recommendation="REVIEW_BEFORE_MERGE",
        ),
        pytest_passed=True,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=1,
        unresolved_audit_issues=0,
    )
    blocked = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(
            status="NOT_READY",
            recommendation="DO_NOT_MERGE",
        ),
        pytest_passed=False,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
    )

    assert ready.status in SUPPORTED_REPOSITORY_READINESS_STATUSES
    assert guarded.status in SUPPORTED_REPOSITORY_READINESS_STATUSES
    assert blocked.status in SUPPORTED_REPOSITORY_READINESS_STATUSES
    assert tuple(frame.recommendation for frame in (blocked, guarded, ready)) == (
        "DO_NOT_MERGE",
        "REVIEW_BEFORE_MERGE",
        "MERGE_CANDIDATE",
    )
    assert set(SUPPORTED_REPOSITORY_RECOMMENDATIONS) == {
        "DO_NOT_MERGE",
        "REVIEW_BEFORE_MERGE",
        "MERGE_CANDIDATE",
    }
    assert ready == RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(),
        pytest_passed=True,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
    )


def test_bounded_history_retention_and_deterministic_eviction() -> None:
    history = tuple(f"repository-{index}" for index in range(6))
    frame = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(),
        pytest_passed=True,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=0,
        unresolved_audit_issues=0,
        repository_history=history,
    )

    combined = history + (
        "status=READY;recommendation=MERGE_CANDIDATE;"
        "merge_status=READY;validation_issues=0;audit_issues=0",
    )
    assert frame.retention_limit == MAX_REPOSITORY_HISTORY_RETENTION
    assert frame.retained_repository_history == combined[-MAX_REPOSITORY_HISTORY_RETENTION:]
    assert frame.evicted_repository_history == combined[:-MAX_REPOSITORY_HISTORY_RETENTION]
    assert frame.evicted_repository_history == (
        "repository-0",
        "repository-1",
        "repository-2",
    )
    assert frame.bounded is True
    assert frame.no_provider_calls is True
    assert frame.no_autonomous_execution is True
    assert frame.no_git_operations is True
    assert frame.no_filesystem_mutation is True


def test_validation_evidence_runtime_output_preserves_repository_behavior() -> None:
    validation_evidence = ValidationEvidenceRuntime().evaluate(
        pytest_passed=True,
        ruff_passed=True,
        audit_passed=True,
        diff_check_passed=True,
        unresolved_validation_issues=1,
        unresolved_audit_issues=2,
    )

    explicit = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(
            status="READY_WITH_WARNINGS",
            recommendation="REVIEW_BEFORE_MERGE",
        ),
        pytest_passed=True,
        ruff_passed=True,
        diff_check_passed=True,
        audit_passed=True,
        unresolved_validation_issues=1,
        unresolved_audit_issues=2,
    )
    via_evidence = RepositoryReadinessRuntime().evaluate(
        merge_readiness=_merge_readiness_frame(
            status="READY_WITH_WARNINGS",
            recommendation="REVIEW_BEFORE_MERGE",
        ),
        validation_evidence=validation_evidence,
    )

    assert via_evidence == explicit


def test_runtime_audit_projection_exposes_repository_readiness() -> None:
    report = run_runtime_enforcement_audit()
    repository_readiness = report.repository_readiness
    merge_readiness = report.merge_readiness
    validation_evidence = report.validation_evidence

    assert repository_readiness.repository_readiness_active is True
    assert repository_readiness.status in SUPPORTED_REPOSITORY_READINESS_STATUSES
    assert repository_readiness.recommendation in SUPPORTED_REPOSITORY_RECOMMENDATIONS
    assert repository_readiness.merge_status == merge_readiness.status
    assert repository_readiness.merge_recommendation == merge_readiness.recommendation
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
    assert len(repository_readiness.retained_repository_history) <= (
        MAX_REPOSITORY_HISTORY_RETENTION
    )


def test_runtime_audit_failed_validation_propagates_repository_not_ready() -> None:
    report = run_runtime_enforcement_audit(
        release_check_inputs=ReleaseCheckInputs(
            pytest_passed=True,
            ruff_passed=False,
            audit_passed=True,
            diff_check_passed=True,
        )
    )

    assert report.validation_evidence.status == "FAILED"
    assert report.repository_readiness.status == "NOT_READY"
    assert report.repository_readiness.recommendation == "DO_NOT_MERGE"
    assert "RUFF_FAILED" in report.repository_readiness.reasons
