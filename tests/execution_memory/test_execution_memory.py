from __future__ import annotations

from ai_dev_os.execution_memory import (
    EXECUTION_MEMORY_BUDGET_LIMIT,
    EXECUTION_MEMORY_REQUIREMENT_IDS,
    EXECUTION_MEMORY_TEST_IDS,
    MAX_CONTINUATION_REUSE_DEPTH,
    MAX_EXECUTION_HISTORY,
    MAX_EXECUTION_MOTIFS,
    MAX_PROVIDER_EXECUTION_MOTIFS,
    ExecutionMemoryRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executionmemory_01_active_runtime_is_bounded_local_patch() -> None:
    frame = ExecutionMemoryRuntime().evaluate()

    assert frame.execution_memory_active is True
    assert frame.requirement_ids == EXECUTION_MEMORY_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_MEMORY_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.execution_memory_mode == "LOCAL_PATCH_BOUNDED_EXECUTION_MEMORY"


def test_tc_executionmemory_02_execution_pattern_tracking() -> None:
    frame = ExecutionMemoryRuntime().evaluate(
        successful_execution_motifs=("inspect", "edit", "test"),
        failure_motifs=("timeout",),
        retry_motifs=("retry_once",),
        provider_execution_outcomes=("local_patch:stable",),
    )

    assert frame.execution_pattern.execution_pattern_active is True
    assert frame.execution_pattern.verified_successful_execution_motifs == (
        "inspect",
        "edit",
        "test",
    )
    assert frame.execution_pattern.repeated_failure_motifs == ("timeout",)
    assert frame.execution_pattern.provider_specific_execution_outcomes == ("local_patch:stable",)
    assert 0 <= frame.execution_pattern_score <= 100
    assert frame.success_pattern.verified_execution_grounded is True


def test_tc_executionmemory_03_retry_pattern_tracking() -> None:
    frame = ExecutionMemoryRuntime().evaluate(
        repeated_retry_chains=3,
        retry_cooldown_reuse=2,
        retry_saturation_motifs=1,
        retry_interruption_patterns=1,
    )

    assert frame.retry_pattern.retry_pattern_active is True
    assert frame.retry_pattern_score >= 70
    assert frame.retry_pattern.bounded_retry_reset_recommendation == (
        "RESET_RETRY_CHAIN_AND_COOLDOWN"
    )
    assert "chains=3" in frame.retry_pattern.deterministic_retry_summary


def test_tc_executionmemory_04_execution_history_reuse() -> None:
    frame = ExecutionMemoryRuntime().evaluate(
        execution_history_items=("inspect", "edit", "test", "audit")
    )

    assert frame.execution_reuse.execution_reuse_active is True
    assert frame.execution_reuse.bounded_execution_history_reuse is True
    assert frame.execution_reuse_score >= 70
    assert frame.execution_reuse.deterministic_reuse_recommendations[0] == (
        "REUSE_KNOWN_LOCAL_PATCH_EXECUTION_MOTIF"
    )


def test_tc_executionmemory_05_provider_specific_execution_memory() -> None:
    motifs = tuple(f"provider_motif_{index}" for index in range(7))
    frame = ExecutionMemoryRuntime().evaluate(provider_execution_motifs=motifs)

    assert len(frame.provider_execution_pattern.provider_execution_motifs) == (
        MAX_PROVIDER_EXECUTION_MOTIFS
    )
    assert frame.provider_execution_pattern.provider_specific_reuse is True
    assert frame.provider_execution_pattern.provider_memory_overflow_blocked is True
    assert (
        frame.execution_eviction.evicted_provider_motifs == motifs[MAX_PROVIDER_EXECUTION_MOTIFS:]
    )
    assert 0 <= frame.provider_execution_memory_score <= 100


def test_tc_executionmemory_06_recursive_reuse_is_blocked() -> None:
    frame = ExecutionMemoryRuntime().evaluate(
        recursive_reuse_attempts=1,
        continuation_reuse_depth=MAX_CONTINUATION_REUSE_DEPTH + 1,
    )

    assert frame.continuation_pattern.recursive_continuation_reuse_blocked is True
    assert frame.execution_termination.recursive_reuse_detected is True
    assert frame.execution_termination.continuation_reuse_depth_exceeded is True
    assert "RECURSIVE_REUSE_DETECTED" in frame.execution_termination.termination_reasons
    assert "CONTINUATION_REUSE_DEPTH_EXCEEDED" in (frame.execution_termination.termination_reasons)


def test_tc_executionmemory_07_execution_governance_enforcement() -> None:
    frame = ExecutionMemoryRuntime().evaluate(
        autonomous_learning_attempts=1,
        recursive_execution_optimization_attempts=1,
        hidden_memory_expansion_attempts=1,
        self_expanding_history_attempts=1,
        governance_policy_mutation_attempts=1,
        retrieval_scope_widening_attempts=1,
    )

    assert frame.execution_governance.local_patch_scope_enforced is True
    assert frame.execution_governance.autonomous_learning_blocked is True
    assert frame.execution_governance.recursive_execution_optimization_blocked is True
    assert frame.execution_governance.hidden_memory_expansion_blocked is True
    assert frame.execution_governance.self_expanding_execution_histories_blocked is True
    assert frame.execution_governance.governance_policy_mutation_blocked is True
    assert frame.execution_governance.retrieval_scope_widening_blocked is True
    assert frame.execution_termination.governance_violation_detected is True


def test_tc_executionmemory_08_execution_termination_handling() -> None:
    frame = ExecutionMemoryRuntime().evaluate(
        execution_memory_budget_used=EXECUTION_MEMORY_BUDGET_LIMIT + 1,
        repeated_retry_chains=4,
        retry_saturation_motifs=2,
    )

    assert frame.execution_termination.execution_memory_terminated is True
    assert frame.execution_termination.execution_memory_budget_exceeded is True
    assert frame.execution_termination.execution_memory_saturation_threshold_exceeded is True
    assert "EXECUTION_MEMORY_BUDGET_EXCEEDED" in (frame.execution_termination.termination_reasons)
    assert "EXECUTION_MEMORY_SATURATION_THRESHOLD_EXCEEDED" in (
        frame.execution_termination.termination_reasons
    )


def test_tc_executionmemory_09_bounded_execution_memory_retention() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    motifs = tuple(f"motif_{index}" for index in range(7))
    frame = ExecutionMemoryRuntime().evaluate(
        execution_history_items=history,
        successful_execution_motifs=motifs,
    )

    assert len(frame.execution_history.execution_history) == MAX_EXECUTION_HISTORY
    assert len(frame.execution_motif.execution_motifs) == MAX_EXECUTION_MOTIFS
    assert frame.execution_history.history_overflow_blocked is True
    assert frame.execution_motif.motif_overflow_blocked is True
    assert frame.execution_eviction.evicted_history_items == history[MAX_EXECUTION_HISTORY:]
    assert frame.execution_eviction.evicted_execution_motifs == motifs[MAX_EXECUTION_MOTIFS:]


def test_tc_executionmemory_10_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().execution_memory

    assert report.execution_memory_active is True
    assert 0 <= report.execution_pattern_score <= 100
    assert 0 <= report.retry_pattern_score <= 100
    assert 0 <= report.execution_reuse_score <= 100
    assert 0 <= report.provider_execution_memory_score <= 100
    assert report.estimated_avoided_retry_repetition > 0
    assert report.estimated_avoided_frontier_replanning > 0
    assert report.estimated_avoided_execution_instability > 0


def test_tc_executionmemory_11_runtime_is_deterministic() -> None:
    first = ExecutionMemoryRuntime().evaluate()
    second = ExecutionMemoryRuntime().evaluate()

    assert first == second
    assert first.execution_reuse.autonomous_plan_generation_blocked is True
    assert first.execution_reuse.recursive_motif_evolution_blocked is True
    assert first.execution_governance.deterministic_execution_reuse_enforced is True
