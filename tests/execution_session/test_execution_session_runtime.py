from __future__ import annotations

from ai_dev_os.execution_session import (
    EXECUTION_SESSION_REQUIREMENT_IDS,
    EXECUTION_SESSION_TEST_IDS,
    MAX_ACTIVE_EXECUTION_SESSIONS,
    MAX_STALE_EXECUTION_SESSIONS,
    SESSION_LIFECYCLE_ORDER,
    ExecutionSessionRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executionsession_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionSessionRuntime().evaluate()

    assert frame.execution_session_active is True
    assert frame.requirement_ids == EXECUTION_SESSION_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_SESSION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_executionsession_02_default_session_is_stable() -> None:
    frame = ExecutionSessionRuntime().evaluate()

    assert frame.termination.should_terminate_sessions is False
    assert frame.confidence.confidence_label == "SESSION_STABLE"
    assert frame.bounded_lifecycle_recommendation == (
        "PERSIST_BOUNDED_EXECUTION_SESSION_LIFECYCLE"
    )


def test_tc_executionsession_03_lifecycle_order_is_deterministic() -> None:
    frame = ExecutionSessionRuntime().evaluate()

    assert frame.lifecycle.deterministic_lifecycle_order == SESSION_LIFECYCLE_ORDER
    assert frame.lifecycle.active_lifecycle_stage == "active"
    assert frame.lifecycle.lifecycle_hierarchy_mutated is False


def test_tc_executionsession_04_lifecycle_blocks_adaptive_persistence() -> None:
    frame = ExecutionSessionRuntime().evaluate()

    assert frame.lifecycle.bounded_lifecycle_persistence is True
    assert frame.lifecycle.adaptive_persistence_system_created is False
    assert frame.lifecycle.governance_safe_session_transitions is True


def test_tc_executionsession_05_persistence_tracks_only_required_sessions() -> None:
    frame = ExecutionSessionRuntime().evaluate(
        active_execution_sessions=3,
        bounded_continuation_sessions=2,
        recovery_lifecycle_sessions=1,
        cooldown_persistence_sessions=1,
        stale_execution_sessions=1,
        orphaned_continuation_sessions=1,
    )

    assert frame.persistence.active_execution_sessions == 3
    assert frame.persistence.bounded_continuation_sessions == 2
    assert frame.persistence.recovery_lifecycle_sessions == 1
    assert frame.persistence.cooldown_persistence_sessions == 1
    assert frame.persistence.stale_execution_sessions == 1
    assert frame.persistence.orphaned_continuation_sessions == 1


def test_tc_executionsession_06_persistence_does_not_create_agents() -> None:
    frame = ExecutionSessionRuntime().evaluate()

    assert frame.persistence.persistent_agents_created is False
    assert frame.persistence.hidden_persistent_sessions_spawned is False


def test_tc_executionsession_07_continuation_terminated_conflict_detected() -> None:
    frame = ExecutionSessionRuntime().evaluate(terminated_session_persistence=True)

    assert frame.conflict.continuation_vs_terminated_session_conflict is True
    assert frame.continuation.autonomous_continuation_resume_allowed is False
    assert frame.compact_session_arbitration_hint == (
        "PRIORITIZE_STALE_OR_ORPHANED_SESSION_INVALIDATION_REVIEW"
    )


def test_tc_executionsession_08_recovery_stale_conflict_detected() -> None:
    frame = ExecutionSessionRuntime().evaluate(stale_execution_sessions=1)

    assert frame.conflict.recovery_vs_stale_session_conflict is True
    assert frame.recovery.recovery_lifecycle_recommendation == "REVIEW_STALE_RECOVERY_SESSION"


def test_tc_executionsession_09_cooldown_continuation_conflict_detected() -> None:
    frame = ExecutionSessionRuntime().evaluate(cooldown_persistence_sessions=1)

    assert frame.conflict.cooldown_vs_continuation_persistence_conflict is True
    assert frame.cooldown.cooldown_persistence_recommendation == (
        "REVIEW_COOLDOWN_BEFORE_CONTINUATION_PERSISTENCE"
    )


def test_tc_executionsession_10_orphaned_session_detection() -> None:
    frame = ExecutionSessionRuntime().evaluate(orphaned_continuation_sessions=1)

    assert frame.conflict.orphaned_session_persistence_conflict is True
    assert frame.integrity.orphaned_lifecycle_state_detected is True
    assert frame.eviction.orphaned_continuation_eviction_recommended is True


def test_tc_executionsession_11_compact_session_summary() -> None:
    frame = ExecutionSessionRuntime().evaluate(
        active_execution_sessions=1,
        bounded_continuation_sessions=0,
        recovery_lifecycle_sessions=0,
    )

    assert frame.deterministic_session_summary == (
        "active=1;continuation=0;recovery=0;stale=0;orphaned=0;terminate=false"
    )
    assert frame.compact_session_arbitration_hint == (
        "FOLLOW_DETERMINISTIC_SESSION_LIFECYCLE_ORDER"
    )


def test_tc_executionsession_12_session_budget_tracks_bounds() -> None:
    frame = ExecutionSessionRuntime().evaluate(
        active_execution_sessions=MAX_ACTIVE_EXECUTION_SESSIONS
    )

    assert frame.budget.used_active_execution_sessions == MAX_ACTIVE_EXECUTION_SESSIONS
    assert frame.budget.remaining_active_execution_sessions == 0
    assert frame.budget.session_budget_exceeded is False


def test_tc_executionsession_13_session_budget_exceeded_terminates() -> None:
    frame = ExecutionSessionRuntime().evaluate(
        active_execution_sessions=MAX_ACTIVE_EXECUTION_SESSIONS + 1
    )

    assert frame.termination.should_terminate_sessions is True
    assert frame.termination.session_budget_exceeded is True
    assert frame.termination.termination_reason == "SESSION_BUDGET_EXCEEDED"


def test_tc_executionsession_14_recursive_persistence_blocking() -> None:
    frame = ExecutionSessionRuntime().evaluate(recursive_session_persistence_attempts=1)

    assert frame.governance.recursive_session_spawning_blocked is True
    assert frame.termination.recursive_session_persistence_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_SESSION_PERSISTENCE_DETECTED"


def test_tc_executionsession_15_hidden_persistent_execution_blocked() -> None:
    frame = ExecutionSessionRuntime().evaluate(hidden_persistent_execution_attempts=1)

    assert frame.governance.hidden_persistent_execution_blocked is True
    assert frame.termination.governance_violation_risk_detected is True
    assert frame.persistence.hidden_persistent_sessions_spawned is False


def test_tc_executionsession_16_autonomous_resurrection_blocked() -> None:
    frame = ExecutionSessionRuntime().evaluate(autonomous_lifecycle_resurrection_attempts=1)

    assert frame.governance.autonomous_lifecycle_resurrection_blocked is True
    assert frame.recovery.terminated_execution_resurrection_allowed is False
    assert frame.termination.termination_reason == ("SESSION_GOVERNANCE_VIOLATION_RISK_DETECTED")


def test_tc_executionsession_17_repo_wide_session_expansion_blocked() -> None:
    frame = ExecutionSessionRuntime().evaluate(repo_wide_session_expansions=1)

    assert frame.governance.repo_wide_session_expansion_blocked is True
    assert frame.governance.governance_policy_mutated is False
    assert frame.termination.governance_violation_risk_detected is True


def test_tc_executionsession_18_retrieval_scope_not_widened() -> None:
    frame = ExecutionSessionRuntime().evaluate(retrieval_radius=3)

    assert frame.governance.bounded_retrieval_enforced is False
    assert frame.governance.retrieval_scope_widened is False
    assert frame.termination.governance_violation_risk_detected is True


def test_tc_executionsession_19_stale_threshold_terminates() -> None:
    frame = ExecutionSessionRuntime().evaluate(
        stale_execution_sessions=MAX_STALE_EXECUTION_SESSIONS + 1
    )

    assert frame.termination.stale_persistence_threshold_exceeded is True
    assert frame.termination.termination_reason == "STALE_PERSISTENCE_THRESHOLD_EXCEEDED"


def test_tc_executionsession_20_orphaned_amplification_terminates() -> None:
    frame = ExecutionSessionRuntime().evaluate(orphaned_continuation_sessions=2)

    assert frame.termination.orphaned_session_amplification_detected is True
    assert frame.termination.termination_reason == "ORPHANED_SESSION_AMPLIFICATION_DETECTED"


def test_tc_executionsession_21_fragmented_lifecycle_detection() -> None:
    frame = ExecutionSessionRuntime().evaluate(fragmented_continuation_sessions=1)

    assert frame.integrity.fragmented_continuation_sessions_detected is True
    assert frame.integrity.compact_session_rewrite_recommendation == (
        "RECOMMEND_COMPACT_SESSION_REWRITE_REVIEW"
    )
    assert frame.integrity.execution_history_silently_mutated is False


def test_tc_executionsession_22_inconsistent_sessions_rewrite_recommendation() -> None:
    frame = ExecutionSessionRuntime().evaluate(inconsistent_execution_sessions=1)

    assert frame.integrity.inconsistent_execution_sessions_detected is True
    assert frame.integrity.automatic_session_erasure_allowed is False
    assert frame.integrity.bounded_session_invalidation_recommendation == (
        "NO_SESSION_INVALIDATION_REQUIRED"
    )


def test_tc_executionsession_23_stale_cleanup_recommendation_only() -> None:
    frame = ExecutionSessionRuntime().evaluate(stale_execution_sessions=1)

    assert frame.integrity.stale_session_persistence_detected is True
    assert frame.integrity.bounded_session_invalidation_recommendation == (
        "RECOMMEND_BOUNDED_SESSION_INVALIDATION_REVIEW"
    )
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_executionsession_24_history_is_bounded() -> None:
    frame = ExecutionSessionRuntime().evaluate(
        history_entries=tuple(f"session-{index}" for index in range(10))
    )

    assert frame.history.history_entry_count == 6
    assert frame.history.history_truncated is True
    assert frame.history.recursive_history_expansion_blocked is True


def test_tc_executionsession_25_runtime_audit_exposes_required_fields_only() -> None:
    report = run_runtime_enforcement_audit().execution_session

    assert report.execution_session_active is True
    assert report.session_lifecycle_active is True
    assert report.session_integrity_active is True
    assert report.session_termination_active is True
    assert report.estimated_avoided_orphaned_sessions == 37
    assert report.estimated_avoided_recursive_persistence == 23
    assert report.estimated_avoided_session_fragmentation == 19


def test_tc_executionsession_26_runtime_is_deterministic_and_summary_only() -> None:
    first = ExecutionSessionRuntime().evaluate()
    second = ExecutionSessionRuntime().evaluate()

    assert first == second
    assert first.summary_only is True
    assert first.governance.deterministic_lifecycle_persistence_enforced is True
    assert first.estimated_avoided_session_fragmentation == 19
