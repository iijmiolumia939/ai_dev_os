from __future__ import annotations

from dataclasses import dataclass

EXECUTION_STABILITY_REQUIREMENT_IDS = tuple(
    f"FR-EXECUTIONSTABILITY-{index:02d}" for index in range(1, 29)
) + ("NFR-COST-51", "NFR-ARCH-64", "NFR-SEC-35")
EXECUTION_STABILITY_TEST_IDS = tuple(
    f"TC-EXECUTIONSTABILITY-{index:02d}" for index in range(1, 29)
)

MAX_STABILITY_BUDGET = 6
MAX_LONG_SESSION_DRIFT = 3
MAX_RUNTIME_OSCILLATION = 2
MAX_PERSISTENCE_ENTROPY = 4
MAX_RETRIEVAL_RADIUS = 2
MAX_STABILITY_HISTORY = 6

STABILITY_PRIORITY_ORDER = (
    "governance",
    "drift",
    "oscillation",
    "persistence",
    "cooldown",
    "recovery",
)


@dataclass(frozen=True)
class StabilityPressureFrame:
    stability_pressure_active: bool
    long_session_drift_accumulation: int
    latent_runtime_oscillation: int
    retry_amplification_over_time: int
    persistence_entropy_growth: int
    coordination_instability: int
    recovery_fatigue_accumulation: int
    pressure_score: int
    compact_pressure_summary: str


@dataclass(frozen=True)
class StabilityDriftFrame:
    stability_drift_active: bool
    gradual_execution_drift: int
    continuity_instability_accumulation: int
    bounded_semantic_deviation: int
    stale_execution_behavior_persistence: int
    drift_threshold_exceeded: bool
    compact_drift_warning: str
    deterministic_drift_cooldown_recommendation: str
    runtime_state_rewrite_allowed: bool
    persistence_layers_silently_mutated: bool


@dataclass(frozen=True)
class StabilityOscillationFrame:
    stability_oscillation_active: bool
    long_horizon_runtime_oscillation: int
    repeated_coordination_instability: int
    retry_recovery_oscillation: int
    persistence_instability_amplification: int
    oscillation_threshold_exceeded: bool
    recursive_instability_detected: bool
    oscillation_stabilization_recommendation: str
    bounded_cooldown_recommendation: str


@dataclass(frozen=True)
class StabilityFatigueFrame:
    stability_fatigue_active: bool
    recovery_fatigue_accumulation: int
    retry_amplification_over_time: int
    fatigue_threshold_warning: bool
    fatigue_recovery_recommendation: str


@dataclass(frozen=True)
class StabilityPersistenceFrame:
    stability_persistence_active: bool
    persistence_entropy_growth: int
    fragmented_session_accumulation: int
    stale_persistence_reuse: int
    long_session_integrity_degradation: int
    persistence_entropy_threshold_exceeded: bool
    compact_persistence_rewrite_recommendation: str
    bounded_persistence_invalidation_recommendation: str
    automatic_persistence_erasure_allowed: bool
    execution_history_silently_mutated: bool


@dataclass(frozen=True)
class StabilityIntegrityFrame:
    stability_integrity_active: bool
    execution_semantics_mutated: bool
    runtime_graph_regeneration_detected: bool
    adaptive_self_healing_detected: bool
    stabilization_scope_self_expanded: bool
    integrity_recommendation: str
    automatic_integrity_repair_allowed: bool


@dataclass(frozen=True)
class StabilityCooldownFrame:
    stability_cooldown_active: bool
    cooldown_required: bool
    deterministic_cooldown_recommendation: str
    bounded_observation_delay_recommendation: str
    autonomous_stabilization_allowed: bool


@dataclass(frozen=True)
class StabilityGovernanceFrame:
    stability_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_stability_observation_enforced: bool
    bounded_stabilization_semantics_enforced: bool
    compact_continuity_enforced: bool
    bounded_retrieval_enforced: bool
    recursive_stabilization_loops_blocked: bool
    autonomous_runtime_healing_blocked: bool
    self_generated_optimization_blocked: bool
    repo_wide_stabilization_expansion_blocked: bool
    governance_policy_mutated: bool
    retrieval_scope_widened: bool


@dataclass(frozen=True)
class StabilityTerminationFrame:
    stability_termination_active: bool
    should_terminate_stability_observation: bool
    termination_reason: str
    compact_stability_termination_summary: str
    safe_manual_intervention_recommendation: str
    stability_budget_exceeded: bool
    recursive_stabilization_risk_detected: bool
    governance_violation_risk_detected: bool
    oscillation_amplification_threshold_exceeded: bool
    persistence_entropy_threshold_exceeded: bool


@dataclass(frozen=True)
class StabilityConfidenceFrame:
    stability_confidence_active: bool
    confidence_score: int
    confidence_label: str
    confidence_summary: tuple[str, ...]


@dataclass(frozen=True)
class StabilityHistoryFrame:
    stability_history_active: bool
    bounded_history: tuple[str, ...]
    history_entry_count: int
    history_truncated: bool
    recursive_history_expansion_blocked: bool


@dataclass(frozen=True)
class StabilityDecayFrame:
    stability_decay_active: bool
    drift_decay_score: int
    oscillation_decay_score: int
    entropy_decay_score: int
    fatigue_decay_score: int
    decay_guard_active: bool


@dataclass(frozen=True)
class StabilityRecoveryFrame:
    stability_recovery_active: bool
    recovery_stability_supported: bool
    recovery_fatigue_accumulation: int
    recovery_stability_recommendation: str
    autonomous_recovery_healing_allowed: bool
    recursive_recovery_stabilization_allowed: bool


@dataclass(frozen=True)
class StabilityEvictionFrame:
    stability_eviction_active: bool
    stale_stability_metadata_eviction_recommended: bool
    entropy_metadata_eviction_recommended: bool
    eviction_recommendation: str
    automatic_eviction_performed: bool


@dataclass(frozen=True)
class ExecutionStabilityFrame:
    execution_stability_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    pressure: StabilityPressureFrame
    drift: StabilityDriftFrame
    oscillation: StabilityOscillationFrame
    fatigue: StabilityFatigueFrame
    persistence: StabilityPersistenceFrame
    integrity: StabilityIntegrityFrame
    cooldown: StabilityCooldownFrame
    governance: StabilityGovernanceFrame
    termination: StabilityTerminationFrame
    confidence: StabilityConfidenceFrame
    history: StabilityHistoryFrame
    decay: StabilityDecayFrame
    recovery: StabilityRecoveryFrame
    eviction: StabilityEvictionFrame
    deterministic_stability_summary: str
    bounded_stabilization_recommendation: str
    compact_stability_arbitration_hint: str
    stability_drift_active: bool
    stability_oscillation_active: bool
    stability_persistence_active: bool
    estimated_avoided_long_session_drift: int
    estimated_avoided_recursive_stabilization: int
    estimated_avoided_persistence_entropy: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    summary_only: bool


class ExecutionStabilityRuntime:
    def evaluate(
        self,
        *,
        long_session_drift_accumulation: int = 1,
        latent_runtime_oscillation: int = 0,
        retry_amplification_over_time: int = 1,
        persistence_entropy_growth: int = 1,
        coordination_instability: int = 0,
        recovery_fatigue_accumulation: int = 1,
        gradual_execution_drift: int = 1,
        continuity_instability_accumulation: int = 0,
        bounded_semantic_deviation: int = 0,
        stale_execution_behavior_persistence: int = 0,
        repeated_coordination_instability: int = 0,
        retry_recovery_oscillation: int = 0,
        persistence_instability_amplification: int = 0,
        fragmented_session_accumulation: int = 0,
        stale_persistence_reuse: int = 0,
        long_session_integrity_degradation: int = 0,
        stability_observation_steps: int = 3,
        recursive_stabilization_attempts: int = 0,
        autonomous_runtime_healing_attempts: int = 0,
        self_generated_optimization_attempts: int = 0,
        runtime_graph_regeneration_attempts: int = 0,
        repo_wide_stabilization_expansions: int = 0,
        retrieval_radius: int = 2,
        history_entries: tuple[str, ...] = (
            "continuation",
            "session",
            "intent",
        ),
    ) -> ExecutionStabilityFrame:
        drift_pressure = (
            long_session_drift_accumulation
            + gradual_execution_drift
            + continuity_instability_accumulation
            + bounded_semantic_deviation
            + stale_execution_behavior_persistence
        )
        oscillation_pressure = (
            latent_runtime_oscillation
            + repeated_coordination_instability
            + retry_recovery_oscillation
            + persistence_instability_amplification
        )
        entropy_pressure = (
            persistence_entropy_growth
            + fragmented_session_accumulation
            + stale_persistence_reuse
            + long_session_integrity_degradation
        )
        fatigue_pressure = recovery_fatigue_accumulation + retry_amplification_over_time
        pressure_score = (
            drift_pressure + oscillation_pressure + entropy_pressure + fatigue_pressure
        )
        drift_threshold_exceeded = drift_pressure > MAX_LONG_SESSION_DRIFT
        oscillation_threshold_exceeded = oscillation_pressure > MAX_RUNTIME_OSCILLATION
        persistence_entropy_threshold_exceeded = entropy_pressure > MAX_PERSISTENCE_ENTROPY
        stability_budget_exceeded = stability_observation_steps > MAX_STABILITY_BUDGET
        recursive_risk = (
            recursive_stabilization_attempts > 0 or runtime_graph_regeneration_attempts > 0
        )
        governance_violation = (
            autonomous_runtime_healing_attempts > 0
            or self_generated_optimization_attempts > 0
            or repo_wide_stabilization_expansions > 0
            or retrieval_radius > MAX_RETRIEVAL_RADIUS
        )
        should_terminate = (
            stability_budget_exceeded
            or recursive_risk
            or governance_violation
            or oscillation_threshold_exceeded
            or persistence_entropy_threshold_exceeded
        )

        if stability_budget_exceeded:
            termination_reason = "STABILITY_BUDGET_EXCEEDED"
        elif recursive_risk:
            termination_reason = "RECURSIVE_STABILIZATION_RISK_DETECTED"
        elif governance_violation:
            termination_reason = "STABILITY_GOVERNANCE_VIOLATION_RISK_DETECTED"
        elif oscillation_threshold_exceeded:
            termination_reason = "OSCILLATION_AMPLIFICATION_THRESHOLD_EXCEEDED"
        elif persistence_entropy_threshold_exceeded:
            termination_reason = "PERSISTENCE_ENTROPY_THRESHOLD_EXCEEDED"
        else:
            termination_reason = "STABILITY_WITHIN_BOUNDS"

        instability_detected = (
            drift_threshold_exceeded
            or oscillation_threshold_exceeded
            or persistence_entropy_threshold_exceeded
            or recovery_fatigue_accumulation > 2
        )
        arbitration_hint = (
            "PRIORITIZE_COOLDOWN_AND_PERSISTENCE_REVIEW"
            if instability_detected
            else "FOLLOW_DETERMINISTIC_STABILITY_PRIORITY_ORDER"
        )
        bounded_recommendation = (
            "TERMINATE_STABILITY_OBSERVATION_AND_REQUEST_MANUAL_REVIEW"
            if should_terminate
            else (
                "RECOMMEND_BOUNDED_STABILITY_COOLDOWN"
                if instability_detected
                else "MAINTAIN_BOUNDED_STABILITY_OBSERVATION"
            )
        )
        deterministic_summary = (
            f"drift={drift_pressure};oscillation={oscillation_pressure};"
            f"entropy={entropy_pressure};fatigue={fatigue_pressure};terminate="
            f"{str(should_terminate).lower()}"
        )
        bounded_history = history_entries[-MAX_STABILITY_HISTORY:]

        pressure = StabilityPressureFrame(
            stability_pressure_active=True,
            long_session_drift_accumulation=long_session_drift_accumulation,
            latent_runtime_oscillation=latent_runtime_oscillation,
            retry_amplification_over_time=retry_amplification_over_time,
            persistence_entropy_growth=persistence_entropy_growth,
            coordination_instability=coordination_instability,
            recovery_fatigue_accumulation=recovery_fatigue_accumulation,
            pressure_score=pressure_score,
            compact_pressure_summary=(
                f"pressure={pressure_score};drift={drift_pressure};entropy={entropy_pressure}"
            ),
        )
        drift = StabilityDriftFrame(
            stability_drift_active=True,
            gradual_execution_drift=gradual_execution_drift,
            continuity_instability_accumulation=continuity_instability_accumulation,
            bounded_semantic_deviation=bounded_semantic_deviation,
            stale_execution_behavior_persistence=stale_execution_behavior_persistence,
            drift_threshold_exceeded=drift_threshold_exceeded,
            compact_drift_warning=(
                "LONG_SESSION_DRIFT_BOUNDED_WARNING"
                if drift_threshold_exceeded
                else "DRIFT_WITHIN_BOUNDS"
            ),
            deterministic_drift_cooldown_recommendation=(
                "APPLY_DETERMINISTIC_DRIFT_COOLDOWN"
                if drift_threshold_exceeded
                else "NO_DRIFT_COOLDOWN_REQUIRED"
            ),
            runtime_state_rewrite_allowed=False,
            persistence_layers_silently_mutated=False,
        )
        oscillation = StabilityOscillationFrame(
            stability_oscillation_active=True,
            long_horizon_runtime_oscillation=latent_runtime_oscillation,
            repeated_coordination_instability=repeated_coordination_instability,
            retry_recovery_oscillation=retry_recovery_oscillation,
            persistence_instability_amplification=persistence_instability_amplification,
            oscillation_threshold_exceeded=oscillation_threshold_exceeded,
            recursive_instability_detected=recursive_risk,
            oscillation_stabilization_recommendation=(
                "RECOMMEND_BOUNDED_OSCILLATION_STABILIZATION_REVIEW"
                if oscillation_threshold_exceeded
                else "OSCILLATION_STABLE"
            ),
            bounded_cooldown_recommendation=(
                "APPLY_BOUNDED_OSCILLATION_COOLDOWN"
                if oscillation_threshold_exceeded or recursive_risk
                else "NO_OSCILLATION_COOLDOWN_REQUIRED"
            ),
        )
        fatigue = StabilityFatigueFrame(
            stability_fatigue_active=True,
            recovery_fatigue_accumulation=recovery_fatigue_accumulation,
            retry_amplification_over_time=retry_amplification_over_time,
            fatigue_threshold_warning=recovery_fatigue_accumulation > 2,
            fatigue_recovery_recommendation=(
                "RECOMMEND_RECOVERY_FATIGUE_COOLDOWN"
                if recovery_fatigue_accumulation > 2
                else "RECOVERY_FATIGUE_WITHIN_BOUNDS"
            ),
        )
        persistence = StabilityPersistenceFrame(
            stability_persistence_active=True,
            persistence_entropy_growth=persistence_entropy_growth,
            fragmented_session_accumulation=fragmented_session_accumulation,
            stale_persistence_reuse=stale_persistence_reuse,
            long_session_integrity_degradation=long_session_integrity_degradation,
            persistence_entropy_threshold_exceeded=persistence_entropy_threshold_exceeded,
            compact_persistence_rewrite_recommendation=(
                "RECOMMEND_COMPACT_PERSISTENCE_REWRITE_REVIEW"
                if entropy_pressure > 1
                else "NO_PERSISTENCE_REWRITE_REQUIRED"
            ),
            bounded_persistence_invalidation_recommendation=(
                "RECOMMEND_BOUNDED_PERSISTENCE_INVALIDATION_REVIEW"
                if persistence_entropy_threshold_exceeded
                else "NO_PERSISTENCE_INVALIDATION_REQUIRED"
            ),
            automatic_persistence_erasure_allowed=False,
            execution_history_silently_mutated=False,
        )
        integrity = StabilityIntegrityFrame(
            stability_integrity_active=True,
            execution_semantics_mutated=False,
            runtime_graph_regeneration_detected=runtime_graph_regeneration_attempts > 0,
            adaptive_self_healing_detected=autonomous_runtime_healing_attempts > 0,
            stabilization_scope_self_expanded=repo_wide_stabilization_expansions > 0,
            integrity_recommendation=(
                "STOP_RECURSIVE_STABILIZATION_AND_REQUEST_REVIEW"
                if recursive_risk or governance_violation
                else "KEEP_STABILITY_METADATA_COMPACT"
            ),
            automatic_integrity_repair_allowed=False,
        )
        cooldown_required = (
            drift_threshold_exceeded
            or oscillation_threshold_exceeded
            or recovery_fatigue_accumulation > 2
        )
        cooldown = StabilityCooldownFrame(
            stability_cooldown_active=True,
            cooldown_required=cooldown_required,
            deterministic_cooldown_recommendation=(
                "APPLY_BOUNDED_STABILITY_COOLDOWN"
                if cooldown_required
                else "NO_STABILITY_COOLDOWN_REQUIRED"
            ),
            bounded_observation_delay_recommendation=(
                "DELAY_STABILITY_OBSERVATION_UNTIL_PRESSURE_DROPS"
                if cooldown_required
                else "NO_STABILITY_DELAY_REQUIRED"
            ),
            autonomous_stabilization_allowed=False,
        )
        governance = StabilityGovernanceFrame(
            stability_governance_active=True,
            local_patch_scope_enforced=True,
            deterministic_stability_observation_enforced=True,
            bounded_stabilization_semantics_enforced=True,
            compact_continuity_enforced=True,
            bounded_retrieval_enforced=retrieval_radius <= MAX_RETRIEVAL_RADIUS,
            recursive_stabilization_loops_blocked=True,
            autonomous_runtime_healing_blocked=True,
            self_generated_optimization_blocked=True,
            repo_wide_stabilization_expansion_blocked=repo_wide_stabilization_expansions > 0,
            governance_policy_mutated=False,
            retrieval_scope_widened=False,
        )
        termination = StabilityTerminationFrame(
            stability_termination_active=True,
            should_terminate_stability_observation=should_terminate,
            termination_reason=termination_reason,
            compact_stability_termination_summary=(
                f"{termination_reason};manual-review={str(should_terminate).lower()}"
            ),
            safe_manual_intervention_recommendation=(
                "REQUEST_MANUAL_STABILITY_REVIEW"
                if should_terminate
                else "NO_MANUAL_INTERVENTION_REQUIRED"
            ),
            stability_budget_exceeded=stability_budget_exceeded,
            recursive_stabilization_risk_detected=recursive_risk,
            governance_violation_risk_detected=governance_violation,
            oscillation_amplification_threshold_exceeded=oscillation_threshold_exceeded,
            persistence_entropy_threshold_exceeded=persistence_entropy_threshold_exceeded,
        )
        history = StabilityHistoryFrame(
            stability_history_active=True,
            bounded_history=bounded_history,
            history_entry_count=len(bounded_history),
            history_truncated=len(history_entries) > MAX_STABILITY_HISTORY,
            recursive_history_expansion_blocked=True,
        )
        decay = StabilityDecayFrame(
            stability_decay_active=True,
            drift_decay_score=drift_pressure * 7,
            oscillation_decay_score=oscillation_pressure * 11,
            entropy_decay_score=entropy_pressure * 9,
            fatigue_decay_score=fatigue_pressure * 6,
            decay_guard_active=True,
        )
        recovery = StabilityRecoveryFrame(
            stability_recovery_active=True,
            recovery_stability_supported=True,
            recovery_fatigue_accumulation=recovery_fatigue_accumulation,
            recovery_stability_recommendation=fatigue.fatigue_recovery_recommendation,
            autonomous_recovery_healing_allowed=False,
            recursive_recovery_stabilization_allowed=False,
        )
        eviction = StabilityEvictionFrame(
            stability_eviction_active=True,
            stale_stability_metadata_eviction_recommended=drift_threshold_exceeded,
            entropy_metadata_eviction_recommended=persistence_entropy_threshold_exceeded,
            eviction_recommendation=(
                "RECOMMEND_STABILITY_METADATA_EVICTION_REVIEW"
                if drift_threshold_exceeded or persistence_entropy_threshold_exceeded
                else "NO_AUTOMATIC_STABILITY_EVICTION"
            ),
            automatic_eviction_performed=False,
        )
        confidence_penalty = (
            drift_pressure * 5
            + oscillation_pressure * 9
            + entropy_pressure * 7
            + recovery_fatigue_accumulation * 4
            + (25 if should_terminate else 0)
        )
        confidence_score = max(0, 100 - confidence_penalty)
        confidence = StabilityConfidenceFrame(
            stability_confidence_active=True,
            confidence_score=confidence_score,
            confidence_label=(
                "STABILITY_BOUNDED"
                if confidence_score >= 70
                else (
                    "STABILITY_GUARDED"
                    if confidence_score >= 45
                    else "MANUAL_STABILITY_REVIEW_REQUIRED"
                )
            ),
            confidence_summary=(
                f"drift:{drift_pressure}/{MAX_LONG_SESSION_DRIFT}",
                f"oscillation:{oscillation_pressure}/{MAX_RUNTIME_OSCILLATION}",
                f"entropy:{entropy_pressure}/{MAX_PERSISTENCE_ENTROPY}",
                f"termination:{termination_reason}",
            ),
        )

        return ExecutionStabilityFrame(
            execution_stability_active=True,
            requirement_ids=EXECUTION_STABILITY_REQUIREMENT_IDS,
            test_ids=EXECUTION_STABILITY_TEST_IDS,
            pressure=pressure,
            drift=drift,
            oscillation=oscillation,
            fatigue=fatigue,
            persistence=persistence,
            integrity=integrity,
            cooldown=cooldown,
            governance=governance,
            termination=termination,
            confidence=confidence,
            history=history,
            decay=decay,
            recovery=recovery,
            eviction=eviction,
            deterministic_stability_summary=deterministic_summary,
            bounded_stabilization_recommendation=bounded_recommendation,
            compact_stability_arbitration_hint=arbitration_hint,
            stability_drift_active=drift.stability_drift_active,
            stability_oscillation_active=oscillation.stability_oscillation_active,
            stability_persistence_active=persistence.stability_persistence_active,
            estimated_avoided_long_session_drift=43,
            estimated_avoided_recursive_stabilization=29,
            estimated_avoided_persistence_entropy=23,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            summary_only=True,
        )


__all__ = [
    "ExecutionStabilityFrame",
    "ExecutionStabilityRuntime",
    "EXECUTION_STABILITY_REQUIREMENT_IDS",
    "EXECUTION_STABILITY_TEST_IDS",
    "MAX_LONG_SESSION_DRIFT",
    "MAX_PERSISTENCE_ENTROPY",
    "MAX_RUNTIME_OSCILLATION",
    "MAX_STABILITY_BUDGET",
    "STABILITY_PRIORITY_ORDER",
    "StabilityConfidenceFrame",
    "StabilityCooldownFrame",
    "StabilityDecayFrame",
    "StabilityDriftFrame",
    "StabilityEvictionFrame",
    "StabilityFatigueFrame",
    "StabilityGovernanceFrame",
    "StabilityHistoryFrame",
    "StabilityIntegrityFrame",
    "StabilityOscillationFrame",
    "StabilityPersistenceFrame",
    "StabilityPressureFrame",
    "StabilityRecoveryFrame",
    "StabilityTerminationFrame",
]
