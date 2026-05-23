from __future__ import annotations

from ai_dev_os.execution_saturation import (
    EXECUTION_SATURATION_REQUIREMENT_IDS,
    EXECUTION_SATURATION_TEST_IDS,
    MAX_CHECKPOINT_COUNT,
    MAX_CONTINUATION_ACCUMULATION,
    MAX_RETRY_OSCILLATION,
    MAX_TOOL_BURST,
    ExecutionSaturationRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executionsaturation_01_runtime_is_local_patch_compatible() -> None:
    frame = ExecutionSaturationRuntime().evaluate()

    assert frame.execution_saturation_active is True
    assert frame.requirement_ids == EXECUTION_SATURATION_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_SATURATION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_executionsaturation_02_default_pressure_is_low_and_bounded() -> None:
    frame = ExecutionSaturationRuntime().evaluate()

    assert frame.pressure.pressure_label == "SATURATION_LOW"
    assert frame.bounded_saturation_warning == "SATURATION_LOW"
    assert frame.termination.should_terminate is False


def test_tc_executionsaturation_03_continuation_congestion_detection() -> None:
    frame = ExecutionSaturationRuntime().evaluate(
        continuation_accumulation=MAX_CONTINUATION_ACCUMULATION + 1
    )

    assert frame.continuation_congestion.continuation_congestion_detected is True
    assert frame.termination.should_terminate is True
    assert frame.termination.termination_reason == "CONTINUATION_CONGESTION_THRESHOLD_EXCEEDED"


def test_tc_executionsaturation_04_recursive_continuation_is_blocked() -> None:
    frame = ExecutionSaturationRuntime().evaluate(recursive_continuation_pressure=1)

    assert frame.continuation_congestion.recursive_continuation_chain_blocked is True
    assert frame.termination.recursive_continuation_blocked is True
    assert frame.termination.termination_reason == "RECURSIVE_CONTINUATION_CHAIN_BLOCKED"


def test_tc_executionsaturation_05_retry_oscillation_detection() -> None:
    frame = ExecutionSaturationRuntime().evaluate(
        repeated_retry_loops=MAX_RETRY_OSCILLATION,
        retry_recovery_oscillation=1,
        failed_continuation_attempts=1,
    )

    assert frame.retry_oscillation.retry_oscillation_detected is True
    assert frame.retry_oscillation.termination_required is True
    assert frame.termination.retry_oscillation_threshold_exceeded is True


def test_tc_executionsaturation_06_recursive_retry_behavior_terminates() -> None:
    frame = ExecutionSaturationRuntime().evaluate(
        repeated_retry_loops=2,
        failed_continuation_attempts=2,
    )

    assert frame.retry_oscillation.recursive_retry_behavior_detected is True
    assert frame.termination.should_terminate is True


def test_tc_executionsaturation_07_checkpoint_inflation_detection() -> None:
    frame = ExecutionSaturationRuntime().evaluate(checkpoint_count=MAX_CHECKPOINT_COUNT + 1)

    assert frame.checkpoint_inflation.checkpoint_inflation_detected is True
    assert frame.checkpoint_inflation.checkpoint_cleanup_recommendation == (
        "RECOMMEND_CHECKPOINT_CLEANUP"
    )
    assert frame.checkpoint_inflation.checkpoints_erased_automatically is False


def test_tc_executionsaturation_08_compact_state_inflation_rewrite_only() -> None:
    frame = ExecutionSaturationRuntime().evaluate(compact_state_units=5)

    assert frame.checkpoint_inflation.checkpoint_inflation_detected is True
    assert frame.checkpoint_inflation.compact_checkpoint_rewrite_recommendation == (
        "REWRITE_COMPACT_CHECKPOINT_SUMMARY"
    )
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_executionsaturation_09_stale_checkpoint_persistence_recommends_cleanup() -> None:
    frame = ExecutionSaturationRuntime().evaluate(stale_checkpoint_count=1)

    assert frame.checkpoint_inflation.stale_checkpoint_persistence == 1
    assert frame.eviction.stale_checkpoint_eviction_recommended is True
    assert frame.eviction.eviction_recommendation == (
        "RECOMMEND_STALE_CHECKPOINT_AND_HISTORY_EVICTION"
    )


def test_tc_executionsaturation_10_tool_congestion_detection() -> None:
    frame = ExecutionSaturationRuntime().evaluate(tool_execution_bursts=MAX_TOOL_BURST + 1)

    assert frame.tool_congestion.tool_congestion_detected is True
    assert frame.tool_congestion.bounded_cooldown_recommendation == (
        "COOLDOWN_BEFORE_NEXT_TOOL_BURST"
    )
    assert frame.tool_congestion.deterministic_slowdown_recommendation == (
        "SLOW_CONTINUATION_TO_SINGLE_TOOL_STEP"
    )


def test_tc_executionsaturation_11_tool_queue_inflation_detection() -> None:
    frame = ExecutionSaturationRuntime().evaluate(tool_queue_depth=6)

    assert frame.tool_congestion.tool_congestion_detected is True
    assert frame.termination.tool_congestion_risk_detected is True
    assert frame.termination.should_terminate is False


def test_tc_executionsaturation_12_deterministic_termination_priority() -> None:
    frame = ExecutionSaturationRuntime().evaluate(
        repeated_retry_loops=4,
        recursive_continuation_pressure=1,
    )

    assert frame.termination.should_terminate is True
    assert frame.termination.termination_reason == "RETRY_OSCILLATION_THRESHOLD_EXCEEDED"
    assert frame.deterministic_termination_recommendation == (
        "TERMINATE_CONTINUATION_BEFORE_RETRY_EXPANSION"
    )


def test_tc_executionsaturation_13_governance_enforces_local_patch() -> None:
    frame = ExecutionSaturationRuntime().evaluate()

    assert frame.governance.saturation_governance_active is True
    assert frame.governance.local_patch_limits_enforced is True
    assert frame.governance.compact_continuity_enforced is True
    assert frame.governance.governance_policy_mutated is False


def test_tc_executionsaturation_14_repo_wide_expansion_is_blocked() -> None:
    frame = ExecutionSaturationRuntime().evaluate(repo_wide_continuation_expansions=1)

    assert frame.governance.repo_wide_continuation_expansion_blocked is True
    assert frame.termination.should_terminate is True
    assert frame.termination.termination_reason == "SATURATION_GOVERNANCE_BLOCKED"


def test_tc_executionsaturation_15_hidden_background_continuation_is_blocked() -> None:
    frame = ExecutionSaturationRuntime().evaluate(hidden_background_continuations=1)

    assert frame.governance.hidden_background_continuation_blocked is True
    assert frame.termination.should_terminate is True
    assert frame.governance.governance_policy_mutated is False


def test_tc_executionsaturation_16_retrieval_scope_is_not_widened() -> None:
    frame = ExecutionSaturationRuntime().evaluate(retrieval_radius=3)

    assert frame.governance.bounded_retrieval_enforced is False
    assert frame.governance.retrieval_scope_widened is False
    assert frame.termination.termination_reason == "SATURATION_GOVERNANCE_BLOCKED"


def test_tc_executionsaturation_17_history_is_bounded() -> None:
    frame = ExecutionSaturationRuntime().evaluate(
        history_entries=tuple(f"entry-{index}" for index in range(10))
    )

    assert frame.history.history_entry_count == 6
    assert frame.history.history_truncated is True
    assert frame.history.recursive_history_expansion_blocked is True


def test_tc_executionsaturation_18_recovery_is_recommendation_only() -> None:
    frame = ExecutionSaturationRuntime().evaluate(recursive_continuation_pressure=1)

    assert frame.recovery.saturation_recovery_active is True
    assert frame.compact_recovery_recommendation == "COMPACT_CONTINUATION_RESET_AND_COOLDOWN"
    assert frame.recovery.autonomous_provider_reroute_allowed is False
    assert frame.recovery.recursive_graph_regeneration_allowed is False


def test_tc_executionsaturation_19_runtime_audit_exposes_required_fields_only() -> None:
    report = run_runtime_enforcement_audit().execution_saturation

    assert report.execution_saturation_active is True
    assert report.retry_oscillation_active is True
    assert report.tool_congestion_active is True
    assert report.checkpoint_inflation_active is True
    assert report.saturation_termination_active is True
    assert report.estimated_avoided_recursive_execution == 31
    assert report.estimated_avoided_retry_loops == 19
    assert report.estimated_avoided_checkpoint_explosion == 11


def test_tc_executionsaturation_20_runtime_is_deterministic_and_summary_only() -> None:
    first = ExecutionSaturationRuntime().evaluate()
    second = ExecutionSaturationRuntime().evaluate()

    assert first == second
    assert first.summary_only is True
    assert first.budget.max_retry_oscillation == MAX_RETRY_OSCILLATION
    assert first.estimated_avoided_recursive_execution == 31
