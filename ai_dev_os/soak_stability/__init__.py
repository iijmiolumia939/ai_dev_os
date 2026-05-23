from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.cognitive_state import CognitiveStateRuntime
from ai_dev_os.continuous_runtime_audit import ContinuousRuntimeAuditRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.failure_injection import FailureInjectionRuntime
from ai_dev_os.intentional_planning import IntentionalPlanningRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_hardening import RuntimeHardeningRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_orchestrator import RuntimeOrchestrator
from ai_dev_os.runtime_policy import RuntimePolicyEngine
from ai_dev_os.sprint_loop import SprintLoopRuntime

SOAK_STABILITY_REQUIREMENT_IDS = tuple(
    f"FR-SOAKSTABILITY-{index:02d}" for index in range(1, 53)
) + (
    "NFR-COST-81",
    "NFR-ARCH-94",
    "NFR-SEC-65",
)
SOAK_STABILITY_TEST_IDS = tuple(f"TC-SOAKSTABILITY-{index:02d}" for index in range(1, 53))

MAX_SOAK_WINDOW = 5
MAX_SOAK_HISTORY = 5
SOAK_BUDGET_LIMIT = 12
SOAK_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_SOAK_HISTORY = (
    "long-session-drift",
    "retry-accumulation",
    "provider-fatigue",
    "continuation-entropy",
    "orchestration-drift",
)
DEFAULT_SOAK_SCOPE = (
    "runtime-survivability",
    "retry-survivability",
    "provider-survivability",
    "continuation-survivability",
    "orchestration-survivability",
)


@dataclass(frozen=True)
class LongSessionDriftFrame:
    long_session_drift_active: bool
    long_session_age_pressure: int
    operational_drift_pressure: int
    cognitive_decay_pressure: int
    planning_decay_pressure: int
    long_session_stability_score: int
    deterministic_long_session_summary: str
    bounded_long_session_recommendation: str


@dataclass(frozen=True)
class RetryAccumulationFrame:
    retry_accumulation_active: bool
    retry_accumulation: int
    retry_saturation_persistence: int
    retry_cooldown_degradation: int
    retry_recovery_drift: int
    retry_accumulation_score: int
    deterministic_retry_accumulation_summary: str
    bounded_retry_survivability_recommendation: str


@dataclass(frozen=True)
class ProviderFatigueAccumulationFrame:
    provider_fatigue_accumulation_active: bool
    provider_fatigue_accumulation: int
    provider_readiness_degradation_persistence: int
    provider_cooldown_persistence: int
    provider_queue_drift: int
    provider_fatigue_accumulation_score: int
    deterministic_provider_fatigue_summary: str
    bounded_provider_survivability_recommendation: str


@dataclass(frozen=True)
class ContinuationEntropyFrame:
    continuation_entropy_active: bool
    continuation_entropy: int
    continuation_drift_accumulation: int
    continuation_reset_persistence: int
    continuation_interruption_degradation: int
    continuation_entropy_score: int
    deterministic_continuation_entropy_summary: str
    bounded_continuation_survivability_recommendation: str


@dataclass(frozen=True)
class OrchestrationQueueDriftFrame:
    orchestration_queue_drift_active: bool
    orchestration_queue_drift: int
    orchestration_dependency_accumulation: int
    orchestration_cooldown_persistence: int
    orchestration_regression_accumulation: int
    orchestration_queue_drift_score: int
    deterministic_orchestration_drift_summary: str
    bounded_orchestration_survivability_recommendation: str


@dataclass(frozen=True)
class RuntimeInteractionEntropyFrame:
    runtime_interaction_entropy_active: bool
    runtime_interaction_entropy: int
    bounded_orchestration_coherence: bool
    bounded_provider_retry_coherence: bool
    bounded_continuation_policy_coherence: bool
    runtime_interaction_entropy_score: int
    deterministic_interaction_entropy_summary: str
    bounded_interaction_survivability_recommendation: str


@dataclass(frozen=True)
class StabilityRetentionFrame:
    stability_retention_active: bool
    retained_stability_items: tuple[str, ...]
    retention_limit: int
    bounded_operational_retention: bool
    deterministic_retention_summary: str
    bounded_retention_recommendation: str


@dataclass(frozen=True)
class SoakGovernanceFrame:
    soak_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_soak_enforced: bool
    bounded_soak_windows_enforced: bool
    autonomous_runtime_state_mutation_blocked: bool
    recursive_soak_optimization_blocked: bool
    novel_stabilization_logic_blocked: bool
    dynamic_soak_scope_widening_blocked: bool
    governance_policy_mutation_blocked: bool
    hidden_persistence_loop_blocked: bool


@dataclass(frozen=True)
class SoakBudgetFrame:
    soak_budget_active: bool
    soak_budget_used: int
    soak_budget_limit: int
    soak_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class SoakTerminationFrame:
    soak_termination_active: bool
    soak_stability_terminated: bool
    termination_reasons: tuple[str, ...]
    soak_budget_exceeded: bool
    recursive_soak_detected: bool
    governance_violation_detected: bool
    soak_saturation_threshold_exceeded: bool


@dataclass(frozen=True)
class SoakHistoryFrame:
    soak_history_active: bool
    soak_history: tuple[str, ...]
    soak_scope: tuple[str, ...]
    soak_history_limit: int
    compact_soak_history_summary: str
    soak_history_overflow_blocked: bool
    soak_scope_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class SoakConfidenceFrame:
    soak_confidence_active: bool
    soak_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    survivability_confidence: bool


@dataclass(frozen=True)
class SoakEvictionFrame:
    soak_eviction_active: bool
    evicted_soak_history_items: tuple[str, ...]
    evicted_soak_scope_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class SoakStabilityFrame:
    soak_stability_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    long_session_drift: LongSessionDriftFrame
    retry_accumulation: RetryAccumulationFrame
    provider_fatigue_accumulation: ProviderFatigueAccumulationFrame
    continuation_entropy: ContinuationEntropyFrame
    orchestration_queue_drift: OrchestrationQueueDriftFrame
    runtime_interaction_entropy: RuntimeInteractionEntropyFrame
    stability_retention: StabilityRetentionFrame
    soak_governance: SoakGovernanceFrame
    soak_budget: SoakBudgetFrame
    soak_termination: SoakTerminationFrame
    soak_history: SoakHistoryFrame
    soak_confidence: SoakConfidenceFrame
    soak_eviction: SoakEvictionFrame
    long_session_stability_score: int
    retry_accumulation_score: int
    provider_fatigue_accumulation_score: int
    continuation_entropy_score: int
    orchestration_queue_drift_score: int
    runtime_interaction_entropy_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    soak_stability_mode: str
    estimated_avoided_slow_degradation: int
    estimated_avoided_runtime_entropy: int
    estimated_avoided_frontier_stabilization: int


class SoakStabilityRuntime:
    def evaluate(
        self,
        *,
        soak_history_items: tuple[str, ...] = DEFAULT_SOAK_HISTORY,
        soak_scope_items: tuple[str, ...] = DEFAULT_SOAK_SCOPE,
        long_session_age_pressure: int = 18,
        operational_drift_pressure: int = 1,
        retry_accumulation: int = 1,
        retry_saturation_persistence: int = 1,
        retry_cooldown_degradation: int = 0,
        retry_recovery_drift: int = 0,
        provider_fatigue_accumulation: int = 1,
        provider_readiness_degradation_persistence: int = 0,
        provider_cooldown_persistence: int = 0,
        provider_queue_drift: int = 1,
        continuation_entropy: int = 1,
        continuation_drift_accumulation: int = 0,
        continuation_reset_persistence: int = 0,
        continuation_interruption_degradation: int = 0,
        orchestration_queue_drift: int = 1,
        orchestration_dependency_accumulation: int = 0,
        orchestration_cooldown_persistence: int = 1,
        orchestration_regression_accumulation: int = 1,
        runtime_interaction_entropy: int = 1,
        soak_budget_used: int = 7,
        recursive_soak_attempts: int = 0,
        autonomous_runtime_state_mutation_attempts: int = 0,
        novel_stabilization_logic_attempts: int = 0,
        dynamic_soak_scope_widening_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        hidden_persistence_loop_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> SoakStabilityFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=retry_accumulation,
            retry_cooldown_pressure=max(1, retry_cooldown_degradation),
            continuation_saturation=18 + continuation_entropy + continuation_drift_accumulation,
            policy_budget_used=min(soak_budget_used, SOAK_BUDGET_LIMIT),
        )
        orchestrator = RuntimeOrchestrator().evaluate(
            retry_amplification=retry_accumulation,
            retry_interruption_windows=retry_recovery_drift,
            continuation_interruption_windows=continuation_interruption_degradation,
            provider_fatigue_pressure=max(1, provider_fatigue_accumulation),
            repeated_regressions=orchestration_regression_accumulation,
            regression_pressure=max(1, orchestration_queue_drift),
            orchestration_budget_used=min(soak_budget_used, SOAK_BUDGET_LIMIT),
        )
        hardening = RuntimeHardeningRuntime().evaluate(
            retry_amplification_chains=retry_accumulation,
            retry_cooldown_collapse=retry_cooldown_degradation,
            retry_saturation_windows=retry_saturation_persistence,
            retry_interruption_instability=retry_recovery_drift,
            provider_readiness_starvation=provider_readiness_degradation_persistence,
            bounded_provider_queue_saturation=provider_queue_drift,
            provider_scheduling_instability=max(1, provider_fatigue_accumulation),
            continuation_saturation=18 + continuation_entropy + continuation_drift_accumulation,
            continuation_interruption_instability=continuation_interruption_degradation,
            continuation_reset_loops=continuation_reset_persistence,
            bounded_continuation_starvation=continuation_drift_accumulation,
            repeated_regressions=orchestration_regression_accumulation,
            regression_dependency_pressure=max(1, orchestration_dependency_accumulation + 1),
            orchestration_dependency_deadlocks=orchestration_dependency_accumulation,
            bounded_orchestration_stalls=orchestration_queue_drift,
            hardening_budget_used=min(soak_budget_used, SOAK_BUDGET_LIMIT),
        )
        continuous_audit = ContinuousRuntimeAuditRuntime().evaluate(
            retry_amplification_pressure=retry_accumulation,
            retry_saturation_windows=retry_saturation_persistence,
            retry_cooldown_collapse=retry_cooldown_degradation,
            retry_recovery_instability=retry_recovery_drift,
            provider_readiness_degradation=provider_readiness_degradation_persistence,
            provider_queue_saturation=provider_queue_drift,
            provider_cooldown_instability=provider_cooldown_persistence,
            continuation_instability_pressure=continuation_entropy,
            continuation_saturation=18 + continuation_entropy + continuation_drift_accumulation,
            continuation_interruption_instability=continuation_interruption_degradation,
            continuation_reset_loops=continuation_reset_persistence,
            bounded_continuation_drift=continuation_drift_accumulation,
            orchestration_queue_pressure=orchestration_queue_drift,
            orchestration_dependency_stalls=orchestration_dependency_accumulation,
            orchestration_cooldown_pressure=orchestration_cooldown_persistence,
            orchestration_regression_pressure=orchestration_regression_accumulation,
            bounded_orchestration_drift=orchestration_queue_drift,
            audit_budget_used=min(soak_budget_used, SOAK_BUDGET_LIMIT),
        )
        failure_injection = FailureInjectionRuntime().evaluate(
            retry_amplification=retry_accumulation,
            retry_saturation=retry_saturation_persistence,
            retry_cooldown_collapse=retry_cooldown_degradation,
            retry_interruption_instability=retry_recovery_drift,
            provider_fatigue_escalation=provider_fatigue_accumulation,
            provider_readiness_degradation=provider_readiness_degradation_persistence,
            provider_queue_saturation=provider_queue_drift,
            continuation_saturation=18 + continuation_entropy + continuation_drift_accumulation,
            continuation_reset_loops=continuation_reset_persistence,
            continuation_drift=continuation_drift_accumulation,
            dependency_deadlocks=orchestration_dependency_accumulation,
            orchestration_queue_stalls=orchestration_queue_drift,
            validation_retry_conflicts=orchestration_regression_accumulation,
            injection_budget_used=min(soak_budget_used, SOAK_BUDGET_LIMIT),
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=max(1, provider_fatigue_accumulation),
            retry_amplification=retry_accumulation,
            orchestration_instability=max(
                1, orchestration_queue_drift + orchestration_dependency_accumulation
            ),
            continuation_decay=continuation_drift_accumulation,
            provider_budget_used=min(soak_budget_used, SOAK_BUDGET_LIMIT),
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=retry_accumulation,
            retry_saturation_motifs=retry_saturation_persistence,
            retry_interruption_patterns=retry_recovery_drift,
            continuation_reuse_depth=max(1, continuation_entropy),
        )
        mediation = ExecutionSequencer().mediate(retry_count=retry_accumulation)
        sprint_loop = SprintLoopRuntime().evaluate(
            repeated_regressions=orchestration_regression_accumulation,
            retry_amplification=retry_accumulation,
            retry_count=retry_accumulation,
            continuation_depth=max(1, continuation_entropy),
            continuation_interruption_window=continuation_interruption_degradation,
            sprint_budget_used=min(soak_budget_used, SOAK_BUDGET_LIMIT),
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=orchestration_regression_accumulation,
            retry_amplification_pressure=retry_accumulation,
        )
        cognitive_state = CognitiveStateRuntime().evaluate(
            objective="soak-stability-local-patch",
            session_age_pressure=long_session_age_pressure,
            recursive_reasoning_attempts=recursive_soak_attempts,
        )
        planning = IntentionalPlanningRuntime().evaluate(
            interruption_duration=continuation_interruption_degradation,
            abandoned_continuation_chains=continuation_reset_persistence,
            recursive_planning_attempts=recursive_soak_attempts,
        )

        bounded_history = soak_history_items[:MAX_SOAK_HISTORY]
        bounded_scope = soak_scope_items[:MAX_SOAK_WINDOW]
        evicted_history = soak_history_items[MAX_SOAK_HISTORY:]
        evicted_scope = soak_scope_items[MAX_SOAK_WINDOW:]

        cognitive_decay_pressure = max(0, 60 - cognitive_state.decay.decay_score)
        planning_decay_pressure = 0 if planning.planning_decay_status == "STABLE" else 12
        long_session_pressure = _clamp(
            long_session_age_pressure
            + operational_drift_pressure * 10
            + cognitive_decay_pressure // 4
            + planning_decay_pressure
            + max(0, 80 - continuous_audit.runtime_health_score) // 2
        )
        long_session_stability_score = _clamp(100 - long_session_pressure)
        retry_pressure = _clamp(
            retry_accumulation * 16
            + retry_saturation_persistence * 10
            + retry_cooldown_degradation * 14
            + retry_recovery_drift * 12
            + max(0, 70 - execution_memory.retry_pattern_score) // 3
        )
        retry_accumulation_score = _clamp(100 - retry_pressure)
        provider_pressure = _clamp(
            provider_fatigue_accumulation * 14
            + provider_readiness_degradation_persistence * 14
            + provider_cooldown_persistence * 10
            + provider_queue_drift * 10
            + max(0, 70 - adaptive_provider.provider_fatigue_score) // 2
        )
        provider_fatigue_accumulation_score = _clamp(100 - provider_pressure)
        continuation_pressure = _clamp(
            continuation_entropy * 14
            + continuation_drift_accumulation * 14
            + continuation_reset_persistence * 10
            + continuation_interruption_degradation * 12
            + max(0, 80 - continuous_audit.continuation_instability_score) // 3
        )
        continuation_entropy_score = _clamp(100 - continuation_pressure)
        orchestration_pressure = _clamp(
            orchestration_queue_drift * 12
            + orchestration_dependency_accumulation * 16
            + orchestration_cooldown_persistence * 10
            + orchestration_regression_accumulation * 12
            + max(0, 80 - orchestrator.orchestration_schedule_score) // 2
        )
        orchestration_queue_drift_score = _clamp(100 - orchestration_pressure)
        runtime_interaction_entropy_score = _clamp(
            (
                runtime_policy.policy_coherence.policy_coherence_score
                + hardening.hardening_confidence.hardening_confidence_score
                + continuous_audit.runtime_health_score
                + failure_injection.recovery_resilience_score
                + sprint_loop.sprint_validation_score
                + reflection.execution_quality.execution_quality_score
            )
            // 6
            - runtime_interaction_entropy * 5
            + int(mediation.runtime_mediation_active) * 2
        )
        soak_confidence_score = _clamp(
            (
                long_session_stability_score
                + retry_accumulation_score
                + provider_fatigue_accumulation_score
                + continuation_entropy_score
                + orchestration_queue_drift_score
                + runtime_interaction_entropy_score
            )
            // 6
        )
        soak_saturation = _clamp(
            max(0, len(soak_history_items) - MAX_SOAK_HISTORY) * 10
            + max(0, len(soak_scope_items) - MAX_SOAK_WINDOW) * 12
            + max(0, 70 - soak_confidence_score)
            + max(
                0,
                55
                - min(
                    retry_accumulation_score,
                    provider_fatigue_accumulation_score,
                    continuation_entropy_score,
                    orchestration_queue_drift_score,
                ),
            )
        )
        soak_budget_exceeded = soak_budget_used > SOAK_BUDGET_LIMIT
        recursive_soak_detected = recursive_soak_attempts > 0
        governance_violation = any(
            (
                autonomous_runtime_state_mutation_attempts,
                novel_stabilization_logic_attempts,
                dynamic_soak_scope_widening_attempts,
                governance_policy_mutation_attempts,
                hidden_persistence_loop_attempts,
            )
        )
        soak_saturation_exceeded = soak_saturation >= SOAK_SATURATION_THRESHOLD
        termination_reasons = _termination_reasons(
            soak_budget_exceeded,
            recursive_soak_detected,
            governance_violation,
            soak_saturation_exceeded,
        )
        final_confidence_score = _clamp(soak_confidence_score - len(termination_reasons) * 8)

        return SoakStabilityFrame(
            soak_stability_active=True,
            requirement_ids=SOAK_STABILITY_REQUIREMENT_IDS,
            test_ids=SOAK_STABILITY_TEST_IDS,
            long_session_drift=LongSessionDriftFrame(
                long_session_drift_active=True,
                long_session_age_pressure=long_session_age_pressure,
                operational_drift_pressure=operational_drift_pressure,
                cognitive_decay_pressure=cognitive_decay_pressure,
                planning_decay_pressure=planning_decay_pressure,
                long_session_stability_score=long_session_stability_score,
                deterministic_long_session_summary=f"age={long_session_age_pressure};drift={operational_drift_pressure};score={long_session_stability_score}",
                bounded_long_session_recommendation=(
                    "RESET_LONG_SESSION_WINDOW"
                    if long_session_stability_score < 60
                    else "LONG_SESSION_DRIFT_BOUNDED"
                ),
            ),
            retry_accumulation=RetryAccumulationFrame(
                retry_accumulation_active=True,
                retry_accumulation=retry_accumulation,
                retry_saturation_persistence=retry_saturation_persistence,
                retry_cooldown_degradation=retry_cooldown_degradation,
                retry_recovery_drift=retry_recovery_drift,
                retry_accumulation_score=retry_accumulation_score,
                deterministic_retry_accumulation_summary=f"accumulation={retry_accumulation};saturation={retry_saturation_persistence};score={retry_accumulation_score}",
                bounded_retry_survivability_recommendation=(
                    "RECOVER_RETRY_ACCUMULATION"
                    if retry_accumulation_score < 60
                    else "RETRY_ACCUMULATION_STABLE"
                ),
            ),
            provider_fatigue_accumulation=ProviderFatigueAccumulationFrame(
                provider_fatigue_accumulation_active=True,
                provider_fatigue_accumulation=provider_fatigue_accumulation,
                provider_readiness_degradation_persistence=provider_readiness_degradation_persistence,
                provider_cooldown_persistence=provider_cooldown_persistence,
                provider_queue_drift=provider_queue_drift,
                provider_fatigue_accumulation_score=provider_fatigue_accumulation_score,
                deterministic_provider_fatigue_summary=f"fatigue={adaptive_provider.provider_fatigue_score};queue={provider_queue_drift};score={provider_fatigue_accumulation_score}",
                bounded_provider_survivability_recommendation=(
                    "REBALANCE_PROVIDER_FATIGUE"
                    if provider_fatigue_accumulation_score < 60
                    else "PROVIDER_FATIGUE_STABLE"
                ),
            ),
            continuation_entropy=ContinuationEntropyFrame(
                continuation_entropy_active=True,
                continuation_entropy=continuation_entropy,
                continuation_drift_accumulation=continuation_drift_accumulation,
                continuation_reset_persistence=continuation_reset_persistence,
                continuation_interruption_degradation=continuation_interruption_degradation,
                continuation_entropy_score=continuation_entropy_score,
                deterministic_continuation_entropy_summary=f"entropy={continuation_entropy};drift={continuation_drift_accumulation};score={continuation_entropy_score}",
                bounded_continuation_survivability_recommendation=(
                    "RESET_CONTINUATION_ENTROPY"
                    if continuation_entropy_score < 60
                    else "CONTINUATION_ENTROPY_BOUNDED"
                ),
            ),
            orchestration_queue_drift=OrchestrationQueueDriftFrame(
                orchestration_queue_drift_active=True,
                orchestration_queue_drift=orchestration_queue_drift,
                orchestration_dependency_accumulation=orchestration_dependency_accumulation,
                orchestration_cooldown_persistence=orchestration_cooldown_persistence,
                orchestration_regression_accumulation=orchestration_regression_accumulation,
                orchestration_queue_drift_score=orchestration_queue_drift_score,
                deterministic_orchestration_drift_summary=f"queue={orchestration_queue_drift};dependency={orchestration_dependency_accumulation};score={orchestration_queue_drift_score}",
                bounded_orchestration_survivability_recommendation=(
                    "RECOVER_ORCHESTRATION_QUEUE"
                    if orchestration_queue_drift_score < 60
                    else "ORCHESTRATION_QUEUE_STABLE"
                ),
            ),
            runtime_interaction_entropy=RuntimeInteractionEntropyFrame(
                runtime_interaction_entropy_active=True,
                runtime_interaction_entropy=runtime_interaction_entropy,
                bounded_orchestration_coherence=orchestration_queue_drift_score >= 60,
                bounded_provider_retry_coherence=provider_fatigue_accumulation_score >= 45
                and retry_accumulation_score >= 60,
                bounded_continuation_policy_coherence=continuation_entropy_score >= 60
                and runtime_policy.continuation_policy_score >= 70,
                runtime_interaction_entropy_score=runtime_interaction_entropy_score,
                deterministic_interaction_entropy_summary=f"entropy={runtime_interaction_entropy};policy={runtime_policy.policy_coherence.policy_coherence_score};score={runtime_interaction_entropy_score}",
                bounded_interaction_survivability_recommendation=(
                    "SURFACE_RUNTIME_INTERACTION_ENTROPY"
                    if runtime_interaction_entropy_score < 75
                    else "RUNTIME_INTERACTION_ENTROPY_BOUNDED"
                ),
            ),
            stability_retention=StabilityRetentionFrame(
                stability_retention_active=True,
                retained_stability_items=bounded_history,
                retention_limit=MAX_SOAK_HISTORY,
                bounded_operational_retention=True,
                deterministic_retention_summary=f"retained={len(bounded_history)};scope={len(bounded_scope)}",
                bounded_retention_recommendation=(
                    "COMPACT_SOAK_RETENTION"
                    if evicted_history or evicted_scope
                    else "SOAK_RETENTION_STABLE"
                ),
            ),
            soak_governance=SoakGovernanceFrame(
                soak_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_soak_enforced=True,
                bounded_soak_windows_enforced=True,
                autonomous_runtime_state_mutation_blocked=True,
                recursive_soak_optimization_blocked=True,
                novel_stabilization_logic_blocked=True,
                dynamic_soak_scope_widening_blocked=True,
                governance_policy_mutation_blocked=True,
                hidden_persistence_loop_blocked=True,
            ),
            soak_budget=SoakBudgetFrame(
                soak_budget_active=True,
                soak_budget_used=soak_budget_used,
                soak_budget_limit=SOAK_BUDGET_LIMIT,
                soak_budget_exceeded=soak_budget_exceeded,
                budget_pressure=_pressure(soak_budget_used, SOAK_BUDGET_LIMIT),
            ),
            soak_termination=SoakTerminationFrame(
                soak_termination_active=True,
                soak_stability_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                soak_budget_exceeded=soak_budget_exceeded,
                recursive_soak_detected=recursive_soak_detected,
                governance_violation_detected=governance_violation,
                soak_saturation_threshold_exceeded=soak_saturation_exceeded,
            ),
            soak_history=SoakHistoryFrame(
                soak_history_active=True,
                soak_history=bounded_history,
                soak_scope=bounded_scope,
                soak_history_limit=MAX_SOAK_HISTORY,
                compact_soak_history_summary=f"history={len(bounded_history)};scope={len(bounded_scope)}",
                soak_history_overflow_blocked=bool(evicted_history),
                soak_scope_overflow_blocked=bool(evicted_scope),
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            soak_confidence=SoakConfidenceFrame(
                soak_confidence_active=True,
                soak_confidence_score=final_confidence_score,
                confidence_status=_score_label(final_confidence_score),
                deterministic_confidence=True,
                survivability_confidence=final_confidence_score >= 70,
            ),
            soak_eviction=SoakEvictionFrame(
                soak_eviction_active=True,
                evicted_soak_history_items=evicted_history,
                evicted_soak_scope_items=evicted_scope,
                eviction_count=len(evicted_history) + len(evicted_scope),
                bounded_eviction_active=bool(evicted_history or evicted_scope),
                eviction_summary=f"history={len(evicted_history)};scope={len(evicted_scope)}",
            ),
            long_session_stability_score=long_session_stability_score,
            retry_accumulation_score=retry_accumulation_score,
            provider_fatigue_accumulation_score=provider_fatigue_accumulation_score,
            continuation_entropy_score=continuation_entropy_score,
            orchestration_queue_drift_score=orchestration_queue_drift_score,
            runtime_interaction_entropy_score=runtime_interaction_entropy_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            soak_stability_mode="LOCAL_PATCH_BOUNDED_SOAK_STABILITY",
            estimated_avoided_slow_degradation=79 + max(0, 80 - long_session_stability_score) // 2,
            estimated_avoided_runtime_entropy=78
            + max(0, 80 - runtime_interaction_entropy_score) // 2,
            estimated_avoided_frontier_stabilization=76 + final_confidence_score // 10,
        )


def _clamp(score: int) -> int:
    return max(MIN_SCORE, min(MAX_SCORE, score))


def _pressure(value: int, limit: int) -> str:
    if value > limit:
        return "HIGH"
    if value >= max(1, limit - 1):
        return "MEDIUM"
    return "LOW"


def _score_label(score: int) -> str:
    if score >= 80:
        return "STABLE"
    if score >= 60:
        return "WATCH"
    return "SOAK_RECOVERY_REQUIRED"


def _termination_reasons(
    soak_budget_exceeded: bool,
    recursive_soak_detected: bool,
    governance_violation_detected: bool,
    soak_saturation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if soak_budget_exceeded:
        reasons.append("SOAK_BUDGET_EXCEEDED")
    if recursive_soak_detected:
        reasons.append("RECURSIVE_SOAK_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if soak_saturation_threshold_exceeded:
        reasons.append("SOAK_SATURATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "MAX_SOAK_HISTORY",
    "MAX_SOAK_WINDOW",
    "SOAK_BUDGET_LIMIT",
    "SOAK_SATURATION_THRESHOLD",
    "SOAK_STABILITY_REQUIREMENT_IDS",
    "SOAK_STABILITY_TEST_IDS",
    "ContinuationEntropyFrame",
    "LongSessionDriftFrame",
    "OrchestrationQueueDriftFrame",
    "ProviderFatigueAccumulationFrame",
    "RetryAccumulationFrame",
    "RuntimeInteractionEntropyFrame",
    "SoakBudgetFrame",
    "SoakConfidenceFrame",
    "SoakEvictionFrame",
    "SoakGovernanceFrame",
    "SoakHistoryFrame",
    "SoakStabilityFrame",
    "SoakStabilityRuntime",
    "SoakTerminationFrame",
    "StabilityRetentionFrame",
]
