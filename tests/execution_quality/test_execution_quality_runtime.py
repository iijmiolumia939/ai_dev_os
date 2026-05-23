from __future__ import annotations

from ai_dev_os.execution_quality import (
    EXECUTION_QUALITY_REQUIREMENT_IDS,
    EXECUTION_QUALITY_TEST_IDS,
    MAX_PERSISTENCE_QUALITY_ENTROPY,
    MAX_QUALITY_BUDGET,
    MAX_QUALITY_DRIFT,
    MAX_REDUNDANCY_AMPLIFICATION,
    ExecutionQualityRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executionquality_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionQualityRuntime().evaluate()

    assert frame.execution_quality_active is True
    assert frame.requirement_ids == EXECUTION_QUALITY_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_QUALITY_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_executionquality_02_default_quality_is_bounded() -> None:
    frame = ExecutionQualityRuntime().evaluate()

    assert frame.termination.should_terminate_quality_observation is False
    assert frame.confidence.confidence_label == "QUALITY_BOUNDED"
    assert frame.bounded_quality_recommendation == "MAINTAIN_BOUNDED_QUALITY_OBSERVATION"


def test_tc_executionquality_03_tracks_only_required_quality_inputs() -> None:
    frame = ExecutionQualityRuntime().evaluate(
        repetitive_low_value_execution=2,
        shallow_retry_behavior=2,
        degraded_continuation_quality=1,
        execution_redundancy=2,
        recovery_churn=1,
        low_signal_persistence=2,
    )

    assert frame.pressure.repetitive_low_value_execution == 2
    assert frame.pressure.shallow_retry_behavior == 2
    assert frame.pressure.degraded_continuation_quality == 1
    assert frame.pressure.execution_redundancy == 2
    assert frame.pressure.recovery_churn == 1
    assert frame.pressure.low_signal_persistence == 2


def test_tc_executionquality_04_compact_quality_summary() -> None:
    frame = ExecutionQualityRuntime().evaluate()

    assert frame.deterministic_quality_summary == (
        "drift=1;redundancy=2;entropy=2;low-value=2;terminate=false"
    )
    assert frame.compact_execution_quality_hint == ("FOLLOW_DETERMINISTIC_QUALITY_PRIORITY_ORDER")


def test_tc_executionquality_05_execution_redundancy_detection() -> None:
    frame = ExecutionQualityRuntime().evaluate(
        repeated_execution_redundancy=MAX_REDUNDANCY_AMPLIFICATION + 1
    )

    assert frame.redundancy.redundancy_amplification_threshold_exceeded is True
    assert frame.redundancy.redundancy_reduction_recommendation == (
        "RECOMMEND_REDUNDANCY_REDUCTION_REVIEW"
    )
    assert frame.termination.termination_reason == ("REDUNDANCY_AMPLIFICATION_THRESHOLD_EXCEEDED")


def test_tc_executionquality_06_duplicate_continuation_detection() -> None:
    frame = ExecutionQualityRuntime().evaluate(duplicate_continuation_behavior=4)

    assert frame.redundancy.duplicate_continuation_behavior == 4
    assert frame.redundancy.bounded_execution_narrowing_recommendation == (
        "RECOMMEND_BOUNDED_EXECUTION_NARROWING"
    )


def test_tc_executionquality_07_low_value_retry_detection() -> None:
    frame = ExecutionQualityRuntime().evaluate(low_value_retry_repetition=4)

    assert frame.redundancy.low_value_retry_repetition == 4
    assert frame.redundancy.recursive_low_value_execution_detected is False
    assert frame.cooldown.cooldown_required is True


def test_tc_executionquality_08_repetitive_low_value_execution_detection() -> None:
    frame = ExecutionQualityRuntime().evaluate(repetitive_low_value_execution=5)

    assert frame.redundancy.recursive_low_value_execution_detected is True
    assert frame.bounded_quality_recommendation == "RECOMMEND_BOUNDED_QUALITY_NARROWING"


def test_tc_executionquality_09_quality_drift_detection() -> None:
    frame = ExecutionQualityRuntime().evaluate(
        gradual_execution_quality_degradation=MAX_QUALITY_DRIFT + 1
    )

    assert frame.drift.quality_drift_threshold_exceeded is True
    assert frame.drift.compact_quality_drift_warning == "QUALITY_DRIFT_BOUNDED_WARNING"


def test_tc_executionquality_10_semantic_quality_drift_bounded() -> None:
    frame = ExecutionQualityRuntime().evaluate(bounded_semantic_quality_drift=4)

    assert frame.drift.quality_drift_threshold_exceeded is True
    assert frame.integrity.runtime_semantics_mutated is False


def test_tc_executionquality_11_repetitive_execution_persistence_detected() -> None:
    frame = ExecutionQualityRuntime().evaluate(repetitive_execution_persistence=4)

    assert frame.drift.repetitive_execution_persistence == 4
    assert frame.drift.deterministic_cooldown_recommendation == (
        "APPLY_DETERMINISTIC_QUALITY_COOLDOWN"
    )


def test_tc_executionquality_12_stale_low_value_continuation_detected() -> None:
    frame = ExecutionQualityRuntime().evaluate(stale_low_value_continuation_behavior=4)

    assert frame.drift.stale_low_value_continuation_behavior == 4
    assert frame.eviction.stale_quality_metadata_eviction_recommended is True


def test_tc_executionquality_13_drift_does_not_rewrite_logic() -> None:
    frame = ExecutionQualityRuntime().evaluate(gradual_execution_quality_degradation=4)

    assert frame.drift.execution_logic_rewrite_allowed is False
    assert frame.drift.runtime_state_silently_mutated is False


def test_tc_executionquality_14_persistence_quality_entropy_detection() -> None:
    frame = ExecutionQualityRuntime().evaluate(
        persistence_quality_entropy=MAX_PERSISTENCE_QUALITY_ENTROPY + 1
    )

    assert frame.entropy.entropy_threshold_exceeded is True
    assert frame.termination.termination_reason == (
        "PERSISTENCE_QUALITY_ENTROPY_THRESHOLD_EXCEEDED"
    )


def test_tc_executionquality_15_degraded_session_reuse_detected() -> None:
    frame = ExecutionQualityRuntime().evaluate(degraded_session_reuse=2)

    assert frame.persistence.degraded_session_reuse == 2
    assert frame.persistence.compact_persistence_rewrite_recommendation == (
        "RECOMMEND_COMPACT_QUALITY_PERSISTENCE_REWRITE_REVIEW"
    )


def test_tc_executionquality_16_fragmented_execution_quality_detected() -> None:
    frame = ExecutionQualityRuntime().evaluate(fragmented_execution_quality=2)

    assert frame.persistence.fragmented_execution_quality == 2
    assert frame.persistence.execution_history_silently_mutated is False


def test_tc_executionquality_17_low_signal_persistence_detected() -> None:
    frame = ExecutionQualityRuntime().evaluate(low_signal_persistence_accumulation=2)

    assert frame.persistence.low_signal_persistence_accumulation == 2
    assert frame.persistence.automatic_persistence_erasure_allowed is False


def test_tc_executionquality_18_persistence_invalidation_recommendation_only() -> None:
    frame = ExecutionQualityRuntime().evaluate(persistence_quality_entropy=5)

    assert frame.persistence.bounded_persistence_invalidation_recommendation == (
        "RECOMMEND_BOUNDED_QUALITY_PERSISTENCE_INVALIDATION_REVIEW"
    )
    assert frame.persistence.automatic_persistence_erasure_allowed is False


def test_tc_executionquality_19_recovery_churn_cooldown() -> None:
    frame = ExecutionQualityRuntime().evaluate(recovery_churn=3)

    assert frame.recovery.recovery_quality_recommendation == "RECOMMEND_RECOVERY_CHURN_COOLDOWN"
    assert frame.recovery.autonomous_recovery_optimization_allowed is False


def test_tc_executionquality_20_quality_budget_exceeded_terminates() -> None:
    frame = ExecutionQualityRuntime().evaluate(quality_observation_steps=MAX_QUALITY_BUDGET + 1)

    assert frame.termination.quality_budget_exceeded is True
    assert frame.termination.termination_reason == "QUALITY_BUDGET_EXCEEDED"


def test_tc_executionquality_21_recursive_optimization_blocking() -> None:
    frame = ExecutionQualityRuntime().evaluate(recursive_optimization_attempts=1)

    assert frame.governance.recursive_self_improvement_loops_blocked is True
    assert frame.termination.recursive_optimization_risk_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_OPTIMIZATION_RISK_DETECTED"


def test_tc_executionquality_22_strategy_regeneration_blocked() -> None:
    frame = ExecutionQualityRuntime().evaluate(execution_strategy_regeneration_attempts=1)

    assert frame.integrity.execution_strategy_regeneration_detected is True
    assert frame.integrity.automatic_integrity_repair_allowed is False
    assert frame.termination.recursive_optimization_risk_detected is True


def test_tc_executionquality_23_autonomous_quality_optimization_blocked() -> None:
    frame = ExecutionQualityRuntime().evaluate(autonomous_quality_optimization_attempts=1)

    assert frame.governance.autonomous_quality_optimization_blocked is True
    assert frame.integrity.adaptive_self_improvement_detected is True
    assert frame.cooldown.autonomous_quality_optimization_allowed is False


def test_tc_executionquality_24_self_generated_heuristics_blocked() -> None:
    frame = ExecutionQualityRuntime().evaluate(self_generated_execution_heuristics=1)

    assert frame.governance.self_generated_execution_heuristics_blocked is True
    assert frame.termination.governance_violation_risk_detected is True
    assert frame.governance.governance_policy_mutated is False


def test_tc_executionquality_25_repo_wide_quality_expansion_blocked() -> None:
    frame = ExecutionQualityRuntime().evaluate(repo_wide_quality_expansions=1)

    assert frame.governance.repo_wide_quality_expansion_blocked is True
    assert frame.integrity.quality_scope_self_expanded is True
    assert frame.bounded is True


def test_tc_executionquality_26_retrieval_scope_not_widened() -> None:
    frame = ExecutionQualityRuntime().evaluate(retrieval_radius=3)

    assert frame.governance.bounded_retrieval_enforced is False
    assert frame.governance.retrieval_scope_widened is False
    assert frame.termination.governance_violation_risk_detected is True


def test_tc_executionquality_27_history_is_bounded() -> None:
    frame = ExecutionQualityRuntime().evaluate(
        history_entries=tuple(f"quality-{index}" for index in range(10))
    )

    assert frame.history.history_entry_count == 6
    assert frame.history.history_truncated is True
    assert frame.history.recursive_history_expansion_blocked is True


def test_tc_executionquality_28_eviction_is_recommendation_only() -> None:
    frame = ExecutionQualityRuntime().evaluate(repeated_execution_redundancy=4)

    assert frame.eviction.redundancy_metadata_eviction_recommended is True
    assert frame.eviction.eviction_recommendation == "RECOMMEND_QUALITY_METADATA_EVICTION_REVIEW"
    assert frame.eviction.automatic_eviction_performed is False


def test_tc_executionquality_29_runtime_audit_exposes_required_fields_only() -> None:
    report = run_runtime_enforcement_audit().execution_quality

    assert report.execution_quality_active is True
    assert report.quality_drift_active is True
    assert report.quality_redundancy_active is True
    assert report.quality_persistence_active is True
    assert report.estimated_avoided_low_value_execution == 47
    assert report.estimated_avoided_recursive_optimization == 31
    assert report.estimated_avoided_execution_redundancy == 29


def test_tc_executionquality_30_runtime_is_deterministic_and_summary_only() -> None:
    first = ExecutionQualityRuntime().evaluate()
    second = ExecutionQualityRuntime().evaluate()

    assert first == second
    assert first.summary_only is True
    assert first.governance.deterministic_quality_observation_enforced is True
    assert first.estimated_avoided_execution_redundancy == 29
