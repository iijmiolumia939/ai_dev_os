from __future__ import annotations

from ai_dev_os.execution_stability import (
    EXECUTION_STABILITY_REQUIREMENT_IDS,
    EXECUTION_STABILITY_TEST_IDS,
    MAX_LONG_SESSION_DRIFT,
    MAX_PERSISTENCE_ENTROPY,
    MAX_RUNTIME_OSCILLATION,
    MAX_STABILITY_BUDGET,
    ExecutionStabilityRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_executionstability_01_runtime_is_bounded_and_local_patch() -> None:
    frame = ExecutionStabilityRuntime().evaluate()

    assert frame.execution_stability_active is True
    assert frame.requirement_ids == EXECUTION_STABILITY_REQUIREMENT_IDS
    assert frame.test_ids == EXECUTION_STABILITY_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True


def test_tc_executionstability_02_default_stability_is_bounded() -> None:
    frame = ExecutionStabilityRuntime().evaluate()

    assert frame.termination.should_terminate_stability_observation is False
    assert frame.confidence.confidence_label == "STABILITY_BOUNDED"
    assert frame.bounded_stabilization_recommendation == ("MAINTAIN_BOUNDED_STABILITY_OBSERVATION")


def test_tc_executionstability_03_tracks_only_required_pressure_inputs() -> None:
    frame = ExecutionStabilityRuntime().evaluate(
        long_session_drift_accumulation=2,
        latent_runtime_oscillation=1,
        retry_amplification_over_time=2,
        persistence_entropy_growth=2,
        coordination_instability=1,
        recovery_fatigue_accumulation=2,
    )

    assert frame.pressure.long_session_drift_accumulation == 2
    assert frame.pressure.latent_runtime_oscillation == 1
    assert frame.pressure.retry_amplification_over_time == 2
    assert frame.pressure.persistence_entropy_growth == 2
    assert frame.pressure.coordination_instability == 1
    assert frame.pressure.recovery_fatigue_accumulation == 2


def test_tc_executionstability_04_compact_stability_summary() -> None:
    frame = ExecutionStabilityRuntime().evaluate()

    assert frame.deterministic_stability_summary == (
        "drift=2;oscillation=0;entropy=1;fatigue=2;terminate=false"
    )
    assert frame.compact_stability_arbitration_hint == (
        "FOLLOW_DETERMINISTIC_STABILITY_PRIORITY_ORDER"
    )


def test_tc_executionstability_05_long_session_drift_detection() -> None:
    frame = ExecutionStabilityRuntime().evaluate(
        long_session_drift_accumulation=MAX_LONG_SESSION_DRIFT + 1
    )

    assert frame.drift.drift_threshold_exceeded is True
    assert frame.drift.compact_drift_warning == "LONG_SESSION_DRIFT_BOUNDED_WARNING"
    assert frame.cooldown.cooldown_required is True


def test_tc_executionstability_06_drift_cooldown_recommendation_only() -> None:
    frame = ExecutionStabilityRuntime().evaluate(gradual_execution_drift=4)

    assert frame.drift.deterministic_drift_cooldown_recommendation == (
        "APPLY_DETERMINISTIC_DRIFT_COOLDOWN"
    )
    assert frame.drift.runtime_state_rewrite_allowed is False
    assert frame.drift.persistence_layers_silently_mutated is False


def test_tc_executionstability_07_continuity_instability_detection() -> None:
    frame = ExecutionStabilityRuntime().evaluate(continuity_instability_accumulation=4)

    assert frame.drift.drift_threshold_exceeded is True
    assert frame.bounded_stabilization_recommendation == ("RECOMMEND_BOUNDED_STABILITY_COOLDOWN")


def test_tc_executionstability_08_semantic_deviation_is_bounded() -> None:
    frame = ExecutionStabilityRuntime().evaluate(bounded_semantic_deviation=4)

    assert frame.drift.drift_threshold_exceeded is True
    assert frame.integrity.execution_semantics_mutated is False


def test_tc_executionstability_09_stale_behavior_persistence_detected() -> None:
    frame = ExecutionStabilityRuntime().evaluate(stale_execution_behavior_persistence=4)

    assert frame.drift.drift_threshold_exceeded is True
    assert frame.eviction.stale_stability_metadata_eviction_recommended is True


def test_tc_executionstability_10_oscillation_detection() -> None:
    frame = ExecutionStabilityRuntime().evaluate(
        latent_runtime_oscillation=MAX_RUNTIME_OSCILLATION + 1
    )

    assert frame.oscillation.oscillation_threshold_exceeded is True
    assert frame.termination.termination_reason == ("OSCILLATION_AMPLIFICATION_THRESHOLD_EXCEEDED")


def test_tc_executionstability_11_coordination_instability_oscillation_detected() -> None:
    frame = ExecutionStabilityRuntime().evaluate(repeated_coordination_instability=3)

    assert frame.oscillation.repeated_coordination_instability == 3
    assert frame.oscillation.oscillation_stabilization_recommendation == (
        "RECOMMEND_BOUNDED_OSCILLATION_STABILIZATION_REVIEW"
    )


def test_tc_executionstability_12_retry_recovery_oscillation_detected() -> None:
    frame = ExecutionStabilityRuntime().evaluate(retry_recovery_oscillation=3)

    assert frame.oscillation.retry_recovery_oscillation == 3
    assert frame.oscillation.bounded_cooldown_recommendation == (
        "APPLY_BOUNDED_OSCILLATION_COOLDOWN"
    )


def test_tc_executionstability_13_persistence_instability_amplification_detected() -> None:
    frame = ExecutionStabilityRuntime().evaluate(persistence_instability_amplification=3)

    assert frame.oscillation.persistence_instability_amplification == 3
    assert frame.termination.oscillation_amplification_threshold_exceeded is True


def test_tc_executionstability_14_recursive_stabilization_blocking() -> None:
    frame = ExecutionStabilityRuntime().evaluate(recursive_stabilization_attempts=1)

    assert frame.governance.recursive_stabilization_loops_blocked is True
    assert frame.termination.recursive_stabilization_risk_detected is True
    assert frame.termination.termination_reason == "RECURSIVE_STABILIZATION_RISK_DETECTED"


def test_tc_executionstability_15_runtime_graph_regeneration_blocked() -> None:
    frame = ExecutionStabilityRuntime().evaluate(runtime_graph_regeneration_attempts=1)

    assert frame.integrity.runtime_graph_regeneration_detected is True
    assert frame.oscillation.recursive_instability_detected is True
    assert frame.integrity.automatic_integrity_repair_allowed is False


def test_tc_executionstability_16_persistence_entropy_detection() -> None:
    frame = ExecutionStabilityRuntime().evaluate(
        persistence_entropy_growth=MAX_PERSISTENCE_ENTROPY + 1
    )

    assert frame.persistence.persistence_entropy_threshold_exceeded is True
    assert frame.termination.termination_reason == "PERSISTENCE_ENTROPY_THRESHOLD_EXCEEDED"
    assert frame.eviction.entropy_metadata_eviction_recommended is True


def test_tc_executionstability_17_fragmented_session_accumulation_detected() -> None:
    frame = ExecutionStabilityRuntime().evaluate(fragmented_session_accumulation=2)

    assert frame.persistence.fragmented_session_accumulation == 2
    assert frame.persistence.compact_persistence_rewrite_recommendation == (
        "RECOMMEND_COMPACT_PERSISTENCE_REWRITE_REVIEW"
    )


def test_tc_executionstability_18_stale_persistence_reuse_detected() -> None:
    frame = ExecutionStabilityRuntime().evaluate(stale_persistence_reuse=2)

    assert frame.persistence.stale_persistence_reuse == 2
    assert frame.persistence.automatic_persistence_erasure_allowed is False


def test_tc_executionstability_19_long_session_integrity_degradation_detected() -> None:
    frame = ExecutionStabilityRuntime().evaluate(long_session_integrity_degradation=2)

    assert frame.persistence.long_session_integrity_degradation == 2
    assert frame.persistence.execution_history_silently_mutated is False


def test_tc_executionstability_20_persistence_invalidation_recommendation_only() -> None:
    frame = ExecutionStabilityRuntime().evaluate(persistence_entropy_growth=5)

    assert frame.persistence.bounded_persistence_invalidation_recommendation == (
        "RECOMMEND_BOUNDED_PERSISTENCE_INVALIDATION_REVIEW"
    )
    assert frame.persistence.automatic_persistence_erasure_allowed is False


def test_tc_executionstability_21_autonomous_runtime_healing_blocked() -> None:
    frame = ExecutionStabilityRuntime().evaluate(autonomous_runtime_healing_attempts=1)

    assert frame.governance.autonomous_runtime_healing_blocked is True
    assert frame.integrity.adaptive_self_healing_detected is True
    assert frame.cooldown.autonomous_stabilization_allowed is False


def test_tc_executionstability_22_self_generated_optimization_blocked() -> None:
    frame = ExecutionStabilityRuntime().evaluate(self_generated_optimization_attempts=1)

    assert frame.governance.self_generated_optimization_blocked is True
    assert frame.termination.governance_violation_risk_detected is True
    assert frame.governance.governance_policy_mutated is False


def test_tc_executionstability_23_repo_wide_stabilization_expansion_blocked() -> None:
    frame = ExecutionStabilityRuntime().evaluate(repo_wide_stabilization_expansions=1)

    assert frame.governance.repo_wide_stabilization_expansion_blocked is True
    assert frame.integrity.stabilization_scope_self_expanded is True
    assert frame.bounded is True


def test_tc_executionstability_24_retrieval_scope_not_widened() -> None:
    frame = ExecutionStabilityRuntime().evaluate(retrieval_radius=3)

    assert frame.governance.bounded_retrieval_enforced is False
    assert frame.governance.retrieval_scope_widened is False
    assert frame.termination.governance_violation_risk_detected is True


def test_tc_executionstability_25_stability_budget_exceeded_terminates() -> None:
    frame = ExecutionStabilityRuntime().evaluate(
        stability_observation_steps=MAX_STABILITY_BUDGET + 1
    )

    assert frame.termination.stability_budget_exceeded is True
    assert frame.termination.termination_reason == "STABILITY_BUDGET_EXCEEDED"


def test_tc_executionstability_26_history_is_bounded() -> None:
    frame = ExecutionStabilityRuntime().evaluate(
        history_entries=tuple(f"stability-{index}" for index in range(10))
    )

    assert frame.history.history_entry_count == 6
    assert frame.history.history_truncated is True
    assert frame.history.recursive_history_expansion_blocked is True


def test_tc_executionstability_27_runtime_audit_exposes_required_fields_only() -> None:
    report = run_runtime_enforcement_audit().execution_stability

    assert report.execution_stability_active is True
    assert report.stability_drift_active is True
    assert report.stability_oscillation_active is True
    assert report.stability_persistence_active is True
    assert report.estimated_avoided_long_session_drift == 43
    assert report.estimated_avoided_recursive_stabilization == 29
    assert report.estimated_avoided_persistence_entropy == 23


def test_tc_executionstability_28_runtime_is_deterministic_and_summary_only() -> None:
    first = ExecutionStabilityRuntime().evaluate()
    second = ExecutionStabilityRuntime().evaluate()

    assert first == second
    assert first.summary_only is True
    assert first.governance.deterministic_stability_observation_enforced is True
    assert first.estimated_avoided_persistence_entropy == 23
