from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.bounded_retention import GovernanceBoundedRetentionPrimitive

MAX_EVIDENCE_HISTORY_RETENTION = 4
MAX_VALIDATION_EVIDENCE_REASONS = 7
SUPPORTED_VALIDATION_EVIDENCE_STATUSES = (
    "FAILED",
    "PASSED_WITH_WARNINGS",
    "PASSED",
)


@dataclass(frozen=True)
class ValidationEvidenceFrame:
    validation_evidence_active: bool
    status: str
    validation_passed: bool
    reasons: tuple[str, ...]
    retained_evidence_history: tuple[str, ...]
    evicted_evidence_history: tuple[str, ...]
    retention_limit: int
    pytest_passed: bool | None
    ruff_passed: bool | None
    audit_passed: bool | None
    diff_check_passed: bool | None
    unresolved_validation_issues: int
    unresolved_audit_issues: int
    deterministic: bool
    bounded: bool
    local_only: bool
    no_provider_calls: bool
    no_filesystem_access: bool
    no_process_execution: bool
    no_git_operations: bool
    no_autonomous_execution: bool


class ValidationEvidenceRuntime:
    def evaluate(
        self,
        *,
        pytest_passed: bool | None,
        ruff_passed: bool | None,
        audit_passed: bool | None,
        diff_check_passed: bool | None,
        unresolved_validation_issues: int,
        unresolved_audit_issues: int,
        evidence_history: tuple[str, ...] = (),
    ) -> ValidationEvidenceFrame:
        if unresolved_validation_issues < 0:
            raise ValueError("unresolved_validation_issues must be non-negative")
        if unresolved_audit_issues < 0:
            raise ValueError("unresolved_audit_issues must be non-negative")

        status = self._status_for(
            pytest_passed=pytest_passed,
            ruff_passed=ruff_passed,
            audit_passed=audit_passed,
            diff_check_passed=diff_check_passed,
            unresolved_validation_issues=unresolved_validation_issues,
            unresolved_audit_issues=unresolved_audit_issues,
        )
        validation_passed = status != "FAILED"
        reasons = self._reasons_for(
            pytest_passed=pytest_passed,
            ruff_passed=ruff_passed,
            audit_passed=audit_passed,
            diff_check_passed=diff_check_passed,
            unresolved_validation_issues=unresolved_validation_issues,
            unresolved_audit_issues=unresolved_audit_issues,
            validation_passed=validation_passed,
        )
        history_entry = (
            f"status={status};validation_passed={str(validation_passed).lower()};"
            f"pytest={str(pytest_passed).lower()};"
            f"ruff={str(ruff_passed).lower()};"
            f"audit={str(audit_passed).lower()};"
            f"diff={str(diff_check_passed).lower()};"
            f"validation_issues={unresolved_validation_issues};"
            f"audit_issues={unresolved_audit_issues}"
        )
        bounded_history = GovernanceBoundedRetentionPrimitive().apply(
            evidence_history + (history_entry,),
            retention_limit=MAX_EVIDENCE_HISTORY_RETENTION,
        )
        return ValidationEvidenceFrame(
            validation_evidence_active=True,
            status=status,
            validation_passed=validation_passed,
            reasons=reasons,
            retained_evidence_history=bounded_history.retained_items,
            evicted_evidence_history=bounded_history.evicted_items,
            retention_limit=MAX_EVIDENCE_HISTORY_RETENTION,
            pytest_passed=pytest_passed,
            ruff_passed=ruff_passed,
            audit_passed=audit_passed,
            diff_check_passed=diff_check_passed,
            unresolved_validation_issues=unresolved_validation_issues,
            unresolved_audit_issues=unresolved_audit_issues,
            deterministic=True,
            bounded=bounded_history.bounded_growth_maintained
            and len(reasons) <= MAX_VALIDATION_EVIDENCE_REASONS,
            local_only=True,
            no_provider_calls=True,
            no_filesystem_access=True,
            no_process_execution=True,
            no_git_operations=True,
            no_autonomous_execution=True,
        )

    def _status_for(
        self,
        *,
        pytest_passed: bool | None,
        ruff_passed: bool | None,
        audit_passed: bool | None,
        diff_check_passed: bool | None,
        unresolved_validation_issues: int,
        unresolved_audit_issues: int,
    ) -> str:
        if any(
            (
                pytest_passed is False,
                ruff_passed is False,
                audit_passed is False,
                diff_check_passed is False,
            )
        ):
            return "FAILED"
        if all(
            (
                pytest_passed is True,
                ruff_passed is True,
                audit_passed is True,
                diff_check_passed is True,
                unresolved_validation_issues == 0,
                unresolved_audit_issues == 0,
            )
        ):
            return "PASSED"
        return "PASSED_WITH_WARNINGS"

    def _reasons_for(
        self,
        *,
        pytest_passed: bool | None,
        ruff_passed: bool | None,
        audit_passed: bool | None,
        diff_check_passed: bool | None,
        unresolved_validation_issues: int,
        unresolved_audit_issues: int,
        validation_passed: bool,
    ) -> tuple[str, ...]:
        reasons: list[str] = []
        release_check_inputs_incomplete = any(
            (
                pytest_passed is None,
                ruff_passed is None,
                audit_passed is None,
                diff_check_passed is None,
            )
        )
        ordered_reasons = (
            ("PYTEST_FAILED", pytest_passed is False),
            ("RUFF_FAILED", ruff_passed is False),
            ("AUDIT_FAILED", audit_passed is False),
            ("DIFF_CHECK_FAILED", diff_check_passed is False),
            ("PYTEST_NOT_PROVIDED", pytest_passed is None),
            ("RUFF_NOT_PROVIDED", ruff_passed is None),
            ("AUDIT_NOT_PROVIDED", audit_passed is None),
            ("DIFF_CHECK_NOT_PROVIDED", diff_check_passed is None),
            ("UNRESOLVED_VALIDATION_ISSUES", unresolved_validation_issues > 0),
            ("UNRESOLVED_AUDIT_ISSUES", unresolved_audit_issues > 0),
            (
                "RELEASE_CHECK_INPUTS_INCOMPLETE",
                release_check_inputs_incomplete,
            ),
            (
                "VALIDATION_COMPLETE",
                validation_passed and not release_check_inputs_incomplete,
            ),
        )
        for reason, active in ordered_reasons:
            if reason == "VALIDATION_COMPLETE" and not validation_passed:
                continue
            if active:
                reasons.append(reason)
        return tuple(reasons[:MAX_VALIDATION_EVIDENCE_REASONS])


__all__ = [
    "MAX_EVIDENCE_HISTORY_RETENTION",
    "MAX_VALIDATION_EVIDENCE_REASONS",
    "SUPPORTED_VALIDATION_EVIDENCE_STATUSES",
    "ValidationEvidenceFrame",
    "ValidationEvidenceRuntime",
]
