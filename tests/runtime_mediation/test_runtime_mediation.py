from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.runtime_mediation import (
    MAX_EXECUTION_CHAIN,
    MAX_EXECUTION_QUEUE,
    MAX_HISTORY,
    MAX_RETRIES,
    RUNTIME_MEDIATION_REQUIREMENT_IDS,
    RUNTIME_MEDIATION_TEST_IDS,
    ExecutionSequencer,
)


def test_tc_runtimemediation_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionSequencer().mediate()

    assert frame.runtime_mediation_active is True
    assert frame.requirement_ids == RUNTIME_MEDIATION_REQUIREMENT_IDS
    assert frame.test_ids == RUNTIME_MEDIATION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_runtimemediation_02_deterministic_sequencing() -> None:
    frame = ExecutionSequencer().mediate(("git", "command", "test", "filesystem"))

    assert frame.execution_sequencer_active is True
    assert frame.priority.ordered_actions == ("test", "command", "filesystem", "git")
    assert frame.window.compact_execution_window == frame.priority.ordered_actions


def test_tc_runtimemediation_03_runtime_arbitration() -> None:
    frame = ExecutionSequencer().mediate(("command", "test", "git", "filesystem"))

    assert frame.arbitration.arbitration_active is True
    assert frame.arbitration.command_vs_test_arbitrated is True
    assert frame.arbitration.git_vs_filesystem_conflict_arbitrated is True
    assert frame.conflict.command_test_conflict is True
    assert frame.conflict.git_filesystem_conflict is True


def test_tc_runtimemediation_04_retry_governance() -> None:
    frame = ExecutionSequencer().mediate(retry_count=MAX_RETRIES + 1)

    assert frame.retry_governance_active is True
    assert frame.retry.bounded_retries_enforced is False
    assert frame.retry.retry_amplification_blocked is True
    assert frame.termination.retry_amplification_detected is True
    assert frame.termination.termination_reason == "RETRY_AMPLIFICATION_DETECTED"


def test_tc_runtimemediation_05_cooldown_enforcement() -> None:
    frame = ExecutionSequencer().mediate(
        execution_cooldown_pressure=3,
        runtime_saturation_cooldown=1,
        retry_cooldown_accumulation=1,
    )

    assert frame.cooldown_governance_active is True
    assert frame.cooldown_governance.cooldown_required is True
    assert frame.cooldown.cooldown_stable is False
    assert frame.cooldown.autonomous_scheduling_optimization_blocked is True


def test_tc_runtimemediation_06_execution_saturation_blocking() -> None:
    actions = tuple(f"action-{index}" for index in range(MAX_EXECUTION_QUEUE + 2))
    frame = ExecutionSequencer().mediate(actions)

    assert frame.queue.queue_saturated is True
    assert frame.queue.queue_saturation_blocked is True
    assert frame.termination.execution_saturation_threshold_exceeded is True
    assert frame.termination.termination_reason == "EXECUTION_SATURATION_THRESHOLD_EXCEEDED"


def test_tc_runtimemediation_07_recursive_execution_blocking() -> None:
    frame = ExecutionSequencer().mediate(recursive_execution_attempts=1)

    assert frame.governance.recursive_orchestration_blocked is True
    assert frame.termination.recursive_execution_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_EXECUTION_DETECTED"


def test_tc_runtimemediation_08_bounded_execution_windows() -> None:
    frame = ExecutionSequencer().mediate(("command", "test", "git", "filesystem", "retry"))

    assert frame.window.window_limit == 4
    assert frame.window.window_truncated is True
    assert len(frame.window.compact_execution_window) == 4
    assert frame.window.self_expanded_window_blocked is False


def test_tc_runtimemediation_09_mediation_governance_enforcement() -> None:
    frame = ExecutionSequencer().mediate(
        direct_unmediated_execution_attempts=1,
        autonomous_execution_attempts=1,
        hidden_background_execution_attempts=1,
        repo_wide_mediation_expansions=1,
    )

    assert frame.governance.autonomous_execution_authority_blocked is True
    assert frame.governance.hidden_background_execution_blocked is True
    assert frame.governance.repo_wide_mediation_expansion_blocked is True
    assert frame.integrity.direct_unmediated_execution_blocked is True
    assert frame.termination.governance_violation_detected is True


def test_tc_runtimemediation_10_execution_budget_termination() -> None:
    frame = ExecutionSequencer().mediate(execution_steps=MAX_EXECUTION_CHAIN + 1)

    assert frame.budget.execution_budget_exceeded is True
    assert frame.termination.should_terminate is True
    assert frame.termination.termination_reason == "EXECUTION_BUDGET_EXCEEDED"


def test_tc_runtimemediation_11_retry_window_expiration() -> None:
    frame = ExecutionSequencer().mediate(retry_count=MAX_RETRIES)

    assert frame.retry.retry_window_expired is True
    assert frame.retry.retry_amplification_blocked is False


def test_tc_runtimemediation_12_recursive_retry_termination() -> None:
    frame = ExecutionSequencer().mediate(recursive_retry_attempts=1)

    assert frame.retry.recursive_retry_detected is True
    assert frame.termination.retry_amplification_detected is True
    assert frame.termination.termination_reason == "RETRY_AMPLIFICATION_DETECTED"


def test_tc_runtimemediation_13_continuation_termination_arbitration() -> None:
    frame = ExecutionSequencer().mediate(("continuation", "termination"))

    assert frame.arbitration.continuation_vs_termination_arbitrated is True
    assert frame.conflict.continuation_termination_conflict is True


def test_tc_runtimemediation_14_self_modifying_orchestration_blocked() -> None:
    frame = ExecutionSequencer().mediate(adaptive_self_modifying_orchestration_attempts=1)

    assert frame.integrity.adaptive_self_modifying_orchestration_blocked is True
    assert frame.integrity.integrity_failure is True
    assert frame.governance.governance_policy_mutated is False


def test_tc_runtimemediation_15_self_prioritization_and_window_expansion_blocked() -> None:
    frame = ExecutionSequencer().mediate(
        self_prioritization_attempts=1, self_expanded_window_attempts=1
    )

    assert frame.priority.self_prioritized_execution_blocked is True
    assert frame.window.self_expanded_window_blocked is True


def test_tc_runtimemediation_16_history_is_bounded() -> None:
    frame = ExecutionSequencer().mediate(
        history_entries=tuple(f"mediation-{index}" for index in range(20))
    )

    assert frame.history.history_entry_count == MAX_HISTORY
    assert frame.history.history_truncated is True
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_runtimemediation_17_retrieval_scope_not_widened() -> None:
    frame = ExecutionSequencer().mediate(retrieval_radius=3)

    assert frame.governance.retrieval_scope_widened is False
    assert frame.termination.governance_violation_detected is True
    assert frame.termination.termination_reason == "GOVERNANCE_VIOLATION_DETECTED"


def test_tc_runtimemediation_18_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().runtime_mediation

    assert report.runtime_mediation_active is True
    assert report.execution_sequencer_active is True
    assert report.retry_governance_active is True
    assert report.cooldown_governance_active is True
    assert report.execution_arbitration_active is True
    assert report.estimated_avoided_recursive_execution == 67
    assert report.estimated_avoided_retry_amplification == 41
    assert report.estimated_avoided_execution_saturation == 38


def test_tc_runtimemediation_19_runtime_is_deterministic() -> None:
    first = ExecutionSequencer().mediate(("git", "test", "command"))
    second = ExecutionSequencer().mediate(("git", "test", "command"))

    assert first == second
    assert first.confidence.confidence_label == "MEDIATION_BOUNDED"
    assert first.compact_runtime_mediation_summary == (
        "runtime mediation active; no direct LLM execution authority"
    )


def test_tc_runtimemediation_20_eviction_is_recommendation_only() -> None:
    actions = tuple(f"action-{index}" for index in range(MAX_EXECUTION_QUEUE + 2))
    frame = ExecutionSequencer().mediate(actions)

    assert frame.eviction.queue_metadata_eviction_recommended is True
    assert frame.eviction.eviction_recommendation == (
        "RECOMMEND_BOUNDED_MEDIATION_METADATA_EVICTION_REVIEW"
    )
    assert frame.eviction.automatic_eviction_performed is False
