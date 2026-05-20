from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    name: str
    status: str
    passed: int = 0
    details: str = ""


@dataclass(frozen=True)
class ValidationCompactionFrame:
    validation_aggregation: bool
    compact_validation_projection: str
    expandable_details: tuple[str, ...]
    total_passed: int
    failed_count: int
    runtime_audit_active: bool
    deterministic: bool


class ValidationCompactionPolicy:
    def compact(self, results: tuple[ValidationResult, ...]) -> ValidationCompactionFrame:
        total_passed = sum(max(0, result.passed) for result in results)
        failed = tuple(
            result for result in results if result.status.lower() not in {"pass", "success"}
        )
        status = "pass" if not failed else "attention"
        projection = f"Validation: {status} ({total_passed} passed total)"
        details = tuple(
            f"{result.name}: {result.status}"
            + (f" ({result.passed} passed)" if result.passed else "")
            + (f" - {result.details}" if result.details else "")
            for result in results
        )
        return ValidationCompactionFrame(
            validation_aggregation=bool(results),
            compact_validation_projection=projection,
            expandable_details=details,
            total_passed=total_passed,
            failed_count=len(failed),
            runtime_audit_active=any(result.name == "runtime audit" for result in results),
            deterministic=True,
        )
