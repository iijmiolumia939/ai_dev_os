from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CIContextFrame:
    latest_ci_status: str
    latest_workflow_name: str
    platform_matrix_summary: tuple[str, ...]
    optional_dependency_status: str
    release_verification_status: str
    known_failures: tuple[str, ...]
    unity_license_failure_detected: bool
    remote_required: bool


class CIContextPolicy:
    def from_summary(
        self,
        *,
        latest_ci_status: str = "unknown",
        latest_workflow_name: str = "CI",
        platform_matrix_summary: tuple[str, ...] = (),
        optional_dependency_status: str = "unknown",
        release_verification_status: str = "unknown",
        known_failures: tuple[str, ...] = (),
    ) -> CIContextFrame:
        unity_license = any(
            "unity" in failure.lower() and "license" in failure.lower()
            for failure in known_failures
        )
        remote_required = latest_ci_status == "unknown" or bool(known_failures)
        return CIContextFrame(
            latest_ci_status=latest_ci_status,
            latest_workflow_name=latest_workflow_name,
            platform_matrix_summary=platform_matrix_summary,
            optional_dependency_status=optional_dependency_status,
            release_verification_status=release_verification_status,
            known_failures=known_failures,
            unity_license_failure_detected=unity_license,
            remote_required=remote_required,
        )

    def default_local(self) -> CIContextFrame:
        return self.from_summary(
            latest_ci_status="unknown",
            latest_workflow_name="CI",
            platform_matrix_summary=("ubuntu", "macos", "windows"),
            optional_dependency_status="unknown",
            release_verification_status="not_checked",
            known_failures=(),
        )
