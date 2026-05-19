from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationCollectorFrame:
    pytest_summary: str
    scoped_pytest: tuple[str, ...]
    ruff_status: str
    black_status: str
    architecture_gates: tuple[str, ...]
    runtime_isolation_gates: tuple[str, ...]
    diff_check: str
    remote_ci_summary: str
    all_passed: bool


class ValidationCollectorPolicy:
    def collect(
        self,
        *,
        pytest_summary: str = "unknown",
        scoped_pytest: tuple[str, ...] = (),
        ruff_status: str = "unknown",
        black_status: str = "unknown",
        architecture_gates: tuple[str, ...] = (),
        runtime_isolation_gates: tuple[str, ...] = (),
        diff_check: str = "unknown",
        remote_ci_summary: str = "unknown",
    ) -> ValidationCollectorFrame:
        statuses = (
            pytest_summary,
            ruff_status,
            black_status,
            diff_check,
            remote_ci_summary,
            *scoped_pytest,
            *architecture_gates,
            *runtime_isolation_gates,
        )
        all_passed = all(self._is_pass(value) for value in statuses if value != "unknown")
        return ValidationCollectorFrame(
            pytest_summary=pytest_summary,
            scoped_pytest=scoped_pytest,
            ruff_status=ruff_status,
            black_status=black_status,
            architecture_gates=architecture_gates,
            runtime_isolation_gates=runtime_isolation_gates,
            diff_check=diff_check,
            remote_ci_summary=remote_ci_summary,
            all_passed=all_passed,
        )

    def _is_pass(self, value: str) -> bool:
        normalized = value.lower()
        return any(marker in normalized for marker in ("pass", "passed", "success", "clean"))
