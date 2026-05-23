from __future__ import annotations

import sys

import pytest

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.verified_execution import (
    MAX_HISTORY,
    VERIFIED_EXECUTION_REQUIREMENT_IDS,
    VERIFIED_EXECUTION_TEST_IDS,
    CommandRuntime,
    EvidenceRuntime,
    ExecutionGovernanceError,
    FileRuntime,
    GitRuntime,
    TestRuntime as VerifiedTestRuntime,
    VerifiedExecutionRuntime,
)


def test_tc_verifiedexecution_01_runtime_is_bounded_and_local_patch(tmp_path) -> None:
    frame = VerifiedExecutionRuntime(tmp_path).evaluate()

    assert frame.envelope_active is True
    assert frame.requirement_ids == VERIFIED_EXECUTION_REQUIREMENT_IDS
    assert frame.test_ids == VERIFIED_EXECUTION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_verifiedexecution_02_subprocess_execution_verification(tmp_path) -> None:
    result = CommandRuntime(tmp_path).run((sys.executable, "-c", "print('grounded')"))

    assert result.stdout.strip() == "grounded"
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.execution_timestamp
    assert result.timed_out is False


def test_tc_verifiedexecution_03_stdout_stderr_capture(tmp_path) -> None:
    result = CommandRuntime(tmp_path).run(
        (sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)")
    )

    assert "out" in result.stdout
    assert "err" in result.stderr
    assert result.exit_code == 0


def test_tc_verifiedexecution_04_exit_code_verification(tmp_path) -> None:
    result = CommandRuntime(tmp_path).run((sys.executable, "-c", "raise SystemExit(7)"))

    assert result.exit_code == 7
    assert result.timed_out is False


def test_tc_verifiedexecution_05_fake_execution_rejection(tmp_path) -> None:
    runtime = VerifiedExecutionRuntime(tmp_path)

    assert runtime.evidence_runtime.reject_synthetic_completion('{"commit_SHA":"fake"}') is True
    assert runtime.command_runtime.reject_unverified_claim("all tests passed") is True


def test_tc_verifiedexecution_06_fake_pytest_rejection(tmp_path) -> None:
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    test_runtime = VerifiedTestRuntime(tmp_path)
    result = test_runtime.run_pytest("test_sample.py")

    assert test_runtime.verify_pytest_output(result, "test_sample.py") is True
    fake = result.__class__(
        command=result.command,
        stdout="1 passed in 0.01s",
        stderr="",
        exit_code=0,
        execution_timestamp=result.execution_timestamp,
        timed_out=False,
        output_truncated=False,
    )
    assert test_runtime.verify_pytest_output(fake, "test_sample.py") is False


def test_tc_verifiedexecution_07_fake_git_evidence_rejection(tmp_path) -> None:
    git = GitRuntime(tmp_path)

    assert git.verify_commit_sha("a1b2c3") is False
    assert git.verify_commit_sha("g" * 40) is False


def test_tc_verifiedexecution_08_bounded_filesystem_verification(tmp_path) -> None:
    file_path = tmp_path / "evidence.txt"
    file_path.write_text("actual evidence", encoding="utf-8")
    files = FileRuntime(tmp_path)

    assert files.verify_file_claim("evidence.txt", required_text="actual") is True
    assert files.verify_file_claim("missing.txt") is False
    with pytest.raises(ExecutionGovernanceError):
        files.read_text(tmp_path.parent / "outside.txt")


def test_tc_verifiedexecution_09_execution_timeout_handling(tmp_path) -> None:
    result = CommandRuntime(tmp_path).run(
        (sys.executable, "-c", "import time; time.sleep(2)"), timeout_seconds=0.1
    )

    assert result.timed_out is True
    assert result.exit_code == -1


def test_tc_verifiedexecution_10_governance_enforcement(tmp_path) -> None:
    runtime = VerifiedExecutionRuntime(tmp_path)
    frame = runtime.evaluate(command=("powershell", "Get-ChildItem"))

    assert frame.termination.terminated is True
    assert frame.termination.governance_violation_detected is True
    assert frame.termination.termination_reason == "UNBOUNDED_SHELL_ACCESS_BLOCKED"


def test_tc_verifiedexecution_11_recursive_execution_blocking(tmp_path) -> None:
    runtime = VerifiedExecutionRuntime(tmp_path)
    frame = runtime.evaluate(command=(sys.executable, "-m", "ai_dev_os.verified_execution"))

    assert frame.termination.recursive_execution_risk_detected is True
    assert frame.governance.recursive_execution_blocked is True


def test_tc_verifiedexecution_12_output_truncation(tmp_path) -> None:
    result = CommandRuntime(tmp_path).run(
        (sys.executable, "-c", "print('x' * 200)"), max_output_chars=20
    )

    assert len(result.stdout) == 20
    assert result.output_truncated is True


def test_tc_verifiedexecution_13_history_is_bounded(tmp_path) -> None:
    frame = VerifiedExecutionRuntime(tmp_path).evaluate(
        history_entries=tuple(f"evidence-{index}" for index in range(20))
    )

    assert frame.history.history_entry_count == MAX_HISTORY
    assert frame.history.history_truncated is True
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_verifiedexecution_14_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().verified_execution

    assert report.verified_execution_active is True
    assert report.command_runtime_active is True
    assert report.filesystem_runtime_active is True
    assert report.pytest_runtime_active is True
    assert report.git_runtime_active is True
    assert report.evidence_runtime_active is True
    assert report.estimated_avoided_fake_execution == 61
    assert report.estimated_avoided_hallucinated_pytest == 37
    assert report.estimated_avoided_synthetic_git_state == 34


def test_tc_verifiedexecution_15_evidence_confidence_scoring(tmp_path) -> None:
    frame = VerifiedExecutionRuntime(tmp_path).evaluate()

    assert frame.confidence.confidence_label == "EXECUTION_GROUNDED"
    assert frame.confidence.confidence_score == 92
    assert frame.integrity.synthetic_execution_rejected is True


def test_tc_verifiedexecution_16_bounded_evidence_governance(tmp_path) -> None:
    frame = VerifiedExecutionRuntime(tmp_path).evaluate()

    assert frame.governance.local_patch_scope_enforced is True
    assert frame.governance.bounded_subprocess_execution is True
    assert frame.governance.unbounded_shell_access_blocked is True
    assert frame.governance.repo_wide_mutation_blocked is True
    assert frame.governance.governance_policy_mutated is False


def test_tc_verifiedexecution_17_prose_only_completion_rejected() -> None:
    assert EvidenceRuntime().reject_synthetic_completion("pytest passed and CI is green") is True


def test_tc_verifiedexecution_18_no_prose_only_execution_completion(tmp_path) -> None:
    frame = VerifiedExecutionRuntime(tmp_path).evaluate()

    assert "no model-claimed evidence" in frame.bounded_evidence_summary
    assert frame.verification.fake_execution_rejected is True