from __future__ import annotations

from ai_dev_os.execution_recovery import (
    EXECUTION_RECOVERY_REQUIREMENT_IDS,
    EXECUTION_RECOVERY_TEST_IDS,
    MAX_CHECKPOINT_CORRUPTION,
    MAX_RECOVERY_STEPS,
    MAX_RETRY_RECOVERY_ATTEMPTS,
    MAX_ROLLBACK_CHECKPOINTS,
    ExecutionRecoveryRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executionrecovery_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionRecoveryRuntime().evaluate()

    assert frame.execution_recovery_active is True
    assert frame.requirement_ids == EXECUTION_RECOVERY_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_RECOVERY_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_executionrecovery_02_default_recovery_is_safe() -> None:
    frame = ExecutionRecoveryRuntime().evaluate()

    assert frame.termination.should_terminate_recovery is False
    assert frame.deterministic_recovery_recommendation == (
        "RESUME_SAFE_RECOVERY_FROM_COMPACT_CHECKPOINT"
    )
    assert frame.resume.safe_resume_supported is True


def test_tc_executionrecovery_03_bounded_rollback_recovery() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(
        bounded_rollback_checkpoints=MAX_ROLLBACK_CHECKPOINTS
    )

    assert frame.rollback.recovery_rollback_active is True
    assert frame.rollback.deterministic_rollback_recovery is True
    assert frame.rollback.rollback_safe_continuation_reset is True
    assert frame.rollback.rollback_unrelated_files_allowed is False


def test_tc_executionrecovery_04_rollback_budget_exceeded_terminates() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(
        bounded_rollback_checkpoints=MAX_ROLLBACK_CHECKPOINTS + 1
    )

    assert frame.budget.budget_exceeded is True
    assert frame.termination.should_terminate_recovery is True
    assert frame.termination.termination_reason == "RECOVERY_BUDGET_EXCEEDED"


def test_tc_executionrecovery_05_recovery_budget_exceeded_terminates() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(recovery_steps=MAX_RECOVERY_STEPS + 1)

    assert frame.budget.recovery_budget_active is True
    assert frame.budget.remaining_recovery_steps == 0
    assert frame.termination.recovery_budget_exceeded is True


def test_tc_executionrecovery_06_checkpoint_integrity_detection() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(checkpoint_corruption_risk=1)

    assert frame.integrity.checkpoint_corruption_detected is True
    assert frame.checkpoint.checkpoint_integrity_valid is True
    assert frame.checkpoint.checkpoints_erased_automatically is False


def test_tc_executionrecovery_07_checkpoint_corruption_threshold_terminates() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(
        checkpoint_corruption_risk=MAX_CHECKPOINT_CORRUPTION + 1
    )

    assert frame.termination.checkpoint_corruption_threshold_exceeded is True
    assert frame.termination.termination_reason == ("CHECKPOINT_CORRUPTION_THRESHOLD_EXCEEDED")
    assert frame.checkpoint.checkpoint_invalidation_recommendation == (
        "INVALIDATE_CORRUPT_CHECKPOINT_FOR_MANUAL_REVIEW"
    )


def test_tc_executionrecovery_08_stale_checkpoint_reuse_rewrites_only() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(stale_checkpoint_reuse=1)

    assert frame.integrity.stale_checkpoint_reuse_detected is True
    assert frame.compact_recovery_checkpoint_recommendation == (
        "REWRITE_COMPACT_RECOVERY_CHECKPOINT"
    )
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_executionrecovery_09_inconsistent_continuation_state_detected() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(inconsistent_continuation_state=1)

    assert frame.integrity.inconsistent_continuation_detected is True
    assert frame.checkpoint.execution_state_mutated_silently is False
    assert frame.checkpoint.compact_checkpoint_rewrite_recommendation == (
        "REWRITE_COMPACT_RECOVERY_CHECKPOINT"
    )


def test_tc_executionrecovery_10_retry_cooldown_enforcement() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(
        retry_cooldown_pressure=2,
        recovery_saturation=2,
        continuation_recovery_fatigue=2,
    )

    assert frame.cooldown.cooldown_required is True
    assert frame.cooldown.cooldown_recommendation == "APPLY_RECOVERY_COOLDOWN"
    assert frame.cooldown.bounded_retry_window_recommendation == (
        "LIMIT_RECOVERY_TO_SINGLE_RETRY_WINDOW"
    )


def test_tc_executionrecovery_11_repeated_failed_recovery_attempts_cooldown() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(repeated_failed_recovery_attempts=3)

    assert frame.cooldown.repeated_failed_recovery_attempts == 3
    assert frame.cooldown.cooldown_required is True
    assert frame.retry.retry_recommendation == "STOP_RETRY_RECOVERY"


def test_tc_executionrecovery_12_retry_amplification_terminates() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(
        retry_recovery_pressure=MAX_RETRY_RECOVERY_ATTEMPTS,
        repeated_failed_recovery_attempts=1,
    )

    assert frame.retry.bounded_retry_window_exceeded is True
    assert frame.termination.retry_amplification_detected is True
    assert frame.termination.termination_reason == "RETRY_AMPLIFICATION_DETECTED"


def test_tc_executionrecovery_13_recursive_recovery_blocking() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(recursive_recovery_attempts=1)

    assert frame.governance.recursive_recovery_loops_blocked is True
    assert frame.termination.recursive_recovery_risk_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_RECOVERY_RISK_DETECTED"


def test_tc_executionrecovery_14_autonomous_architecture_repair_blocked() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(autonomous_architecture_repair_attempts=1)

    assert frame.governance.autonomous_architecture_repair_blocked is True
    assert frame.termination.governance_violation_risk_detected is True
    assert frame.governance.governance_policy_mutated is False


def test_tc_executionrecovery_15_repo_wide_recovery_expansion_blocked() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(repo_wide_recovery_expansions=1)

    assert frame.governance.repo_wide_recovery_expansion_blocked is True
    assert frame.termination.termination_reason == ("RECOVERY_GOVERNANCE_VIOLATION_RISK_DETECTED")
    assert frame.rollback.repo_wide_rollback_allowed is False


def test_tc_executionrecovery_16_hidden_recovery_loops_blocked() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(hidden_recovery_loops=1)

    assert frame.governance.hidden_recovery_loops_blocked is True
    assert frame.termination.governance_violation_risk_detected is True
    assert frame.resume.autonomous_continue_allowed is False


def test_tc_executionrecovery_17_retrieval_scope_not_widened() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(retrieval_radius=3)

    assert frame.termination.governance_violation_risk_detected is True
    assert frame.governance.retrieval_scope_widened is False
    assert frame.governance.local_patch_scope_enforced is True


def test_tc_executionrecovery_18_history_is_bounded() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(
        history_entries=tuple(f"recovery-{index}" for index in range(10))
    )

    assert frame.history.history_entry_count == 6
    assert frame.history.history_truncated is True
    assert frame.history.recursive_history_expansion_blocked is True


def test_tc_executionrecovery_19_recovery_eviction_is_recommendation_only() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(stale_checkpoint_reuse=1)

    assert frame.eviction.stale_checkpoint_eviction_recommended is True
    assert frame.eviction.eviction_recommendation == ("RECOMMEND_STALE_RECOVERY_STATE_EVICTION")
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_executionrecovery_20_termination_summary_is_compact() -> None:
    frame = ExecutionRecoveryRuntime().evaluate(recursive_recovery_attempts=1)

    assert frame.termination.compact_recovery_termination_summary == (
        "RECURSIVE_RECOVERY_RISK_DETECTED;manual-review=true"
    )
    assert frame.termination.safe_manual_intervention_recommendation == (
        "REQUEST_MANUAL_RECOVERY_REVIEW"
    )


def test_tc_executionrecovery_21_runtime_audit_exposes_required_fields_only() -> None:
    report = run_runtime_enforcement_audit().execution_recovery

    assert report.execution_recovery_active is True
    assert report.recovery_cooldown_active is True
    assert report.recovery_checkpoint_integrity_active is True
    assert report.recovery_termination_active is True
    assert report.estimated_avoided_recovery_loops == 23
    assert report.estimated_avoided_checkpoint_corruption == 17
    assert report.estimated_avoided_recursive_repair == 13


def test_tc_executionrecovery_22_runtime_is_deterministic_and_summary_only() -> None:
    first = ExecutionRecoveryRuntime().evaluate()
    second = ExecutionRecoveryRuntime().evaluate()

    assert first == second
    assert first.summary_only is True
    assert first.governance.deterministic_recovery_enforced is True
    assert first.estimated_avoided_recursive_repair == 13
