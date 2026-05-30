from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.bounded_retention import GovernanceBoundedRetentionPrimitive
from ai_dev_os.merge_readiness import MergeReadinessFrame
from ai_dev_os.validation_evidence import ValidationEvidenceFrame, ValidationEvidenceRuntime

MAX_REPOSITORY_HISTORY_RETENTION = 4
MAX_REPOSITORY_REASONS = 8
SUPPORTED_REPOSITORY_READINESS_STATUSES = (
    "NOT_READY",
    "READY_WITH_WARNINGS",
    "READY",
)
SUPPORTED_REPOSITORY_RECOMMENDATIONS = (
    "DO_NOT_MERGE",
    "REVIEW_BEFORE_MERGE",
    "MERGE_CANDIDATE",
)


@dataclass(frozen=True)
class RepositoryReadinessFrame:
    repository_readiness_active: bool
    status: str
    recommendation: str
    reasons: tuple[str, ...]
    retained_repository_history: tuple[str, ...]
    evicted_repository_history: tuple[str, ...]
    retention_limit: int
    merge_status: str
    merge_recommendation: str
    pytest_passed: bool | None
    ruff_passed: bool | None
    diff_check_passed: bool | None
    audit_passed: bool | None
    unresolved_validation_issues: int
    unresolved_audit_issues: int
    deterministic: bool
    bounded: bool
    local_only: bool
    no_provider_calls: bool
    no_autonomous_execution: bool
    no_git_operations: bool
    no_filesystem_mutation: bool


class RepositoryReadinessRuntime:
    _RECOMMENDATION_BY_STATUS = {
        "NOT_READY": "DO_NOT_MERGE",
        "READY_WITH_WARNINGS": "REVIEW_BEFORE_MERGE",
        "READY": "MERGE_CANDIDATE",
    }

    def evaluate(
        self,
        *,
        merge_readiness: MergeReadinessFrame,
        pytest_passed: bool | None = None,
        ruff_passed: bool | None = None,
        diff_check_passed: bool | None = None,
        audit_passed: bool | None = None,
        unresolved_validation_issues: int | None = None,
        unresolved_audit_issues: int | None = None,
        validation_evidence: ValidationEvidenceFrame | None = None,
        repository_history: tuple[str, ...] = (),
    ) -> RepositoryReadinessFrame:
        if merge_readiness.status not in SUPPORTED_REPOSITORY_READINESS_STATUSES:
            raise ValueError(f"unsupported merge readiness status: {merge_readiness.status}")
        source_evidence = self._resolve_validation_evidence(
            pytest_passed=pytest_passed,
            ruff_passed=ruff_passed,
            diff_check_passed=diff_check_passed,
            audit_passed=audit_passed,
            unresolved_validation_issues=unresolved_validation_issues,
            unresolved_audit_issues=unresolved_audit_issues,
            validation_evidence=validation_evidence,
        )

        status = self._status_for(
            merge_readiness=merge_readiness,
            validation_evidence=source_evidence,
        )
        recommendation = self._RECOMMENDATION_BY_STATUS[status]
        reasons = self._reasons_for(
            merge_readiness=merge_readiness,
            status=status,
            validation_evidence=source_evidence,
        )
        history_entry = (
            f"status={status};recommendation={recommendation};"
            f"merge_status={merge_readiness.status};"
            f"validation_issues={source_evidence.unresolved_validation_issues};"
            f"audit_issues={source_evidence.unresolved_audit_issues}"
        )
        bounded_history = GovernanceBoundedRetentionPrimitive().apply(
            repository_history + (history_entry,),
            retention_limit=MAX_REPOSITORY_HISTORY_RETENTION,
        )
        return RepositoryReadinessFrame(
            repository_readiness_active=True,
            status=status,
            recommendation=recommendation,
            reasons=reasons,
            retained_repository_history=bounded_history.retained_items,
            evicted_repository_history=bounded_history.evicted_items,
            retention_limit=MAX_REPOSITORY_HISTORY_RETENTION,
            merge_status=merge_readiness.status,
            merge_recommendation=merge_readiness.recommendation,
            pytest_passed=source_evidence.pytest_passed,
            ruff_passed=source_evidence.ruff_passed,
            diff_check_passed=source_evidence.diff_check_passed,
            audit_passed=source_evidence.audit_passed,
            unresolved_validation_issues=source_evidence.unresolved_validation_issues,
            unresolved_audit_issues=source_evidence.unresolved_audit_issues,
            deterministic=True,
            bounded=bounded_history.bounded_growth_maintained
            and len(reasons) <= MAX_REPOSITORY_REASONS,
            local_only=True,
            no_provider_calls=True,
            no_autonomous_execution=True,
            no_git_operations=True,
            no_filesystem_mutation=True,
        )

    def _status_for(
        self,
        *,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
    ) -> str:
        if self._is_not_ready(
            merge_readiness=merge_readiness,
            validation_evidence=validation_evidence,
        ):
            return "NOT_READY"
        if self._is_ready(
            merge_readiness=merge_readiness,
            validation_evidence=validation_evidence,
        ):
            return "READY"
        return "READY_WITH_WARNINGS"

    def _is_ready(
        self,
        *,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
    ) -> bool:
        return all(
            (
                merge_readiness.status == "READY",
                validation_evidence.status == "PASSED",
            )
        )

    def _is_not_ready(
        self,
        *,
        merge_readiness: MergeReadinessFrame,
        validation_evidence: ValidationEvidenceFrame,
    ) -> bool:
        return any(
            (
                validation_evidence.status == "FAILED",
                merge_readiness.status == "NOT_READY",
            )
        )

    def _reasons_for(
        self,
        *,
        merge_readiness: MergeReadinessFrame,
        status: str,
        validation_evidence: ValidationEvidenceFrame,
    ) -> tuple[str, ...]:
        if status == "READY":
            ordered_reasons = (
                ("MERGE_READY_CONFIRMED", merge_readiness.status == "READY"),
                ("PYTEST_PASSED", validation_evidence.pytest_passed is True),
                ("RUFF_PASSED", validation_evidence.ruff_passed is True),
                ("DIFF_CHECK_PASSED", validation_evidence.diff_check_passed is True),
                ("AUDIT_PASSED", validation_evidence.audit_passed is True),
                (
                    "NO_UNRESOLVED_VALIDATION_ISSUES",
                    validation_evidence.unresolved_validation_issues == 0,
                ),
                ("NO_UNRESOLVED_AUDIT_ISSUES", validation_evidence.unresolved_audit_issues == 0),
            )
        elif status == "READY_WITH_WARNINGS":
            ordered_reasons = (
                (
                    "MERGE_READY_WITH_WARNINGS",
                    merge_readiness.status == "READY_WITH_WARNINGS",
                ),
                (
                    "VALIDATION_EVIDENCE_INCOMPLETE",
                    self._has_missing_release_checks(validation_evidence),
                ),
                (
                    "UNRESOLVED_VALIDATION_ISSUES",
                    validation_evidence.unresolved_validation_issues > 0,
                ),
                ("UNRESOLVED_AUDIT_ISSUES", validation_evidence.unresolved_audit_issues > 0),
            )
        else:
            ordered_reasons = (
                ("MERGE_NOT_READY", merge_readiness.status == "NOT_READY"),
                ("PYTEST_FAILED", validation_evidence.pytest_passed is False),
                ("RUFF_FAILED", validation_evidence.ruff_passed is False),
                ("DIFF_CHECK_FAILED", validation_evidence.diff_check_passed is False),
                ("AUDIT_FAILED", validation_evidence.audit_passed is False),
            )
        reasons = tuple(
            reason for reason, active in ordered_reasons if active
        )[:MAX_REPOSITORY_REASONS]
        if reasons:
            return reasons
        return ("REPOSITORY_REVIEW_REQUIRED",)

    def _has_missing_release_checks(
        self,
        validation_evidence: ValidationEvidenceFrame,
    ) -> bool:
        return any(
            (
                validation_evidence.pytest_passed is None,
                validation_evidence.ruff_passed is None,
                validation_evidence.diff_check_passed is None,
                validation_evidence.audit_passed is None,
            )
        )

    def _resolve_validation_evidence(
        self,
        *,
        pytest_passed: bool | None,
        ruff_passed: bool | None,
        diff_check_passed: bool | None,
        audit_passed: bool | None,
        unresolved_validation_issues: int | None,
        unresolved_audit_issues: int | None,
        validation_evidence: ValidationEvidenceFrame | None,
    ) -> ValidationEvidenceFrame:
        if validation_evidence is not None:
            self._validate_optional_consistency(
                pytest_passed=pytest_passed,
                ruff_passed=ruff_passed,
                diff_check_passed=diff_check_passed,
                audit_passed=audit_passed,
                unresolved_validation_issues=unresolved_validation_issues,
                unresolved_audit_issues=unresolved_audit_issues,
                validation_evidence=validation_evidence,
            )
            return validation_evidence

        required_values = (
            pytest_passed,
            ruff_passed,
            diff_check_passed,
            audit_passed,
            unresolved_validation_issues,
            unresolved_audit_issues,
        )
        if any(value is None for value in required_values):
            raise ValueError(
                "validation evidence or all explicit validation inputs are required"
            )
        return ValidationEvidenceRuntime().evaluate(
            pytest_passed=pytest_passed,
            ruff_passed=ruff_passed,
            audit_passed=audit_passed,
            diff_check_passed=diff_check_passed,
            unresolved_validation_issues=unresolved_validation_issues,
            unresolved_audit_issues=unresolved_audit_issues,
        )

    def _validate_optional_consistency(
        self,
        *,
        pytest_passed: bool | None,
        ruff_passed: bool | None,
        diff_check_passed: bool | None,
        audit_passed: bool | None,
        unresolved_validation_issues: int | None,
        unresolved_audit_issues: int | None,
        validation_evidence: ValidationEvidenceFrame,
    ) -> None:
        comparisons = (
            ("pytest_passed", pytest_passed, validation_evidence.pytest_passed),
            ("ruff_passed", ruff_passed, validation_evidence.ruff_passed),
            ("diff_check_passed", diff_check_passed, validation_evidence.diff_check_passed),
            ("audit_passed", audit_passed, validation_evidence.audit_passed),
            (
                "unresolved_validation_issues",
                unresolved_validation_issues,
                validation_evidence.unresolved_validation_issues,
            ),
            (
                "unresolved_audit_issues",
                unresolved_audit_issues,
                validation_evidence.unresolved_audit_issues,
            ),
        )
        for field_name, provided_value, evidence_value in comparisons:
            if provided_value is not None and provided_value != evidence_value:
                raise ValueError(
                    f"{field_name} does not match validation evidence input"
                )


__all__ = [
    "MAX_REPOSITORY_HISTORY_RETENTION",
    "MAX_REPOSITORY_REASONS",
    "RepositoryReadinessFrame",
    "RepositoryReadinessRuntime",
    "SUPPORTED_REPOSITORY_READINESS_STATUSES",
    "SUPPORTED_REPOSITORY_RECOMMENDATIONS",
]
