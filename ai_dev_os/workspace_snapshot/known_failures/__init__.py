from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnownFailureFrame:
    known_ci_failures: tuple[str, ...]
    known_unity_license_failures: tuple[str, ...]
    known_lint_debt: tuple[str, ...]
    known_formatting_debt: tuple[str, ...]
    known_vendor_exclusions: tuple[str, ...]
    acknowledged_temporary_failures: tuple[str, ...]
    baseline_failures: tuple[str, ...]
    new_failures: tuple[str, ...]
    unresolved_failures: tuple[str, ...]
    ignored_failures: tuple[str, ...]
    read_only: bool


class KnownFailurePolicy:
    def classify(
        self,
        *,
        current_failures: tuple[str, ...] = (),
        known_ci_failures: tuple[str, ...] = (),
        known_unity_license_failures: tuple[str, ...] = (),
        known_lint_debt: tuple[str, ...] = (),
        known_formatting_debt: tuple[str, ...] = (),
        known_vendor_exclusions: tuple[str, ...] = (),
        acknowledged_temporary_failures: tuple[str, ...] = (),
    ) -> KnownFailureFrame:
        baseline = (
            known_ci_failures
            + known_unity_license_failures
            + known_lint_debt
            + known_formatting_debt
            + known_vendor_exclusions
            + acknowledged_temporary_failures
        )
        new_failures = tuple(
            failure for failure in current_failures if not self._matches_any(failure, baseline)
        )
        unresolved = tuple(
            failure for failure in current_failures if self._matches_any(failure, baseline)
        )
        ignored = tuple(
            failure
            for failure in current_failures
            if self._matches_any(failure, known_vendor_exclusions)
        )
        return KnownFailureFrame(
            known_ci_failures=known_ci_failures,
            known_unity_license_failures=known_unity_license_failures,
            known_lint_debt=known_lint_debt,
            known_formatting_debt=known_formatting_debt,
            known_vendor_exclusions=known_vendor_exclusions,
            acknowledged_temporary_failures=acknowledged_temporary_failures,
            baseline_failures=baseline,
            new_failures=new_failures,
            unresolved_failures=unresolved,
            ignored_failures=ignored,
            read_only=True,
        )

    def from_workspace(self, workspace: str | Path = ".") -> KnownFailureFrame:
        return self.classify(
            current_failures=(),
            known_ci_failures=("remote CI status unknown until verification",),
            known_unity_license_failures=("Unity license failure is external infrastructure",),
            known_lint_debt=(),
            known_formatting_debt=(),
            known_vendor_exclusions=("vendor and generated artifacts excluded",),
            acknowledged_temporary_failures=(),
        )

    def _matches_any(self, failure: str, baseline: tuple[str, ...]) -> bool:
        normalized = failure.lower()
        return any(item.lower() in normalized or normalized in item.lower() for item in baseline)
