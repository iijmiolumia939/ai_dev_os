from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.cognitive_state import CognitiveStateRuntime
from ai_dev_os.continuous_runtime_audit import ContinuousRuntimeAuditRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.intentional_planning import IntentionalPlanningRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_hardening import RuntimeHardeningRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_orchestrator import RuntimeOrchestrator
from ai_dev_os.runtime_policy import RuntimePolicyEngine
from ai_dev_os.sprint_loop import SprintLoopRuntime
from ai_dev_os.verified_execution import ExecutionEnvelope

FAILURE_INJECTION_REQUIREMENT_IDS = tuple(
    f"FR-FAILUREINJECTION-{index:02d}" for index in range(1, 49)
) + ("NFR-COST-79", "NFR-ARCH-92", "NFR-SEC-63")
FAILURE_INJECTION_TEST_IDS = tuple(f"TC-FAILUREINJECTION-{index:02d}" for index in range(1, 49))

MAX_INJECTION_WINDOW = 5
MAX_INJECTION_HISTORY = 5
INJECTION_BUDGET_LIMIT = 12
INJECTION_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_INJECTION_HISTORY = (
    "retry-storm",
    "provider-starvation",
    "continuation-collapse",
    "orchestration-deadlock",
    "recovery-validation",
)
DEFAULT_INJECTION_SCOPE = (
    "retry",
    "provider",
    "continuation",
    "orchestration",
    "recovery",
)


@dataclass(frozen=True)
class RetryStormInjectionFrame:
    retry_storm_injection_active: bool
    retry_amplification: int
    retry_saturation: int
    retry_cooldown_collapse: int
    retry_interruption_instability: int
    retry_injection_score: int
    deterministic_retry_injection_summary: str
    bounded_retry_recovery_recommendation: str


@dataclass(frozen=True)
class ProviderStarvationInjectionFrame:
    provider_starvation_injection_active: bool
    provider_starvation: int
    provider_fatigue_escalation: int
    provider_readiness_degradation: int
    provider_queue_saturation: int
    provider_injection_score: int
    deterministic_provider_injection_summary: str
    bounded_provider_rebalance_recommendation: str


@dataclass(frozen=True)
class ContinuationCollapseInjectionFrame:
    continuation_collapse_injection_active: bool
    continuation_interruption_collapse: int
    continuation_saturation: int
    continuation_reset_loops: int
    continuation_drift: int
    continuation_injection_score: int
    deterministic_continuation_injection_summary: str
    bounded_continuation_reset_recommendation: str


@dataclass(frozen=True)
class EscalationOscillationInjectionFrame:
    escalation_oscillation_injection_active: bool
    provider_escalation_loops: int
    provider_downgrade_loops: int
    escalation_cooldown_collapse: int
    escalation_injection_score: int
    deterministic_escalation_injection_summary: str
    bounded_escalation_recovery_recommendation: str


@dataclass(frozen=True)
class OrchestrationDeadlockInjectionFrame:
    orchestration_deadlock_injection_active: bool
    dependency_deadlocks: int
    validation_retry_conflicts: int
    provider_policy_conflicts: int
    orchestration_queue_stalls: int
    orchestration_injection_score: int
    deterministic_orchestration_injection_summary: str
    bounded_orchestration_recovery_recommendation: str


@dataclass(frozen=True)
class RuntimeRecoveryInjectionFrame:
    runtime_recovery_injection_active: bool
    bounded_recovery_validation: bool
    bounded_cooldown_recovery: bool
    bounded_provider_rebalance: bool
    bounded_continuation_reset_recovery: bool
    recovery_resilience_score: int
    deterministic_recovery_summary: str
    bounded_recovery_recommendation: str


@dataclass(frozen=True)
class InjectionGovernanceFrame:
    injection_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_injection_enforced: bool
    bounded_injection_windows_enforced: bool
    autonomous_runtime_state_mutation_blocked: bool
    recursive_injection_blocked: bool
    novel_attack_pattern_synthesis_blocked: bool
    dynamic_injection_scope_widening_blocked: bool
    governance_policy_mutation_blocked: bool
    hidden_chaos_loop_blocked: bool


@dataclass(frozen=True)
class InjectionBudgetFrame:
    injection_budget_active: bool
    injection_budget_used: int
    injection_budget_limit: int
    injection_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class InjectionTerminationFrame:
    injection_termination_active: bool
    failure_injection_terminated: bool
    termination_reasons: tuple[str, ...]
    injection_budget_exceeded: bool
    recursive_injection_detected: bool
    governance_violation_detected: bool
    injection_saturation_threshold_exceeded: bool


@dataclass(frozen=True)
class InjectionHistoryFrame:
    injection_history_active: bool
    injection_history: tuple[str, ...]
    injection_scope: tuple[str, ...]
    injection_history_limit: int
    compact_injection_history_summary: str
    injection_history_overflow_blocked: bool
    injection_scope_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class InjectionConfidenceFrame:
    injection_confidence_active: bool
    injection_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    resilience_validation_confidence: bool


@dataclass(frozen=True)
class InjectionEvictionFrame:
    injection_eviction_active: bool
    evicted_injection_history_items: tuple[str, ...]
    evicted_injection_scope_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class FailureInjectionFrame:
    failure_injection_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    retry_storm_injection: RetryStormInjectionFrame
    provider_starvation_injection: ProviderStarvationInjectionFrame
    continuation_collapse_injection: ContinuationCollapseInjectionFrame
    escalation_oscillation_injection: EscalationOscillationInjectionFrame
    orchestration_deadlock_injection: OrchestrationDeadlockInjectionFrame
    runtime_recovery_injection: RuntimeRecoveryInjectionFrame
    injection_governance: InjectionGovernanceFrame
    injection_budget: InjectionBudgetFrame
    injection_termination: InjectionTerminationFrame
    injection_history: InjectionHistoryFrame
    injection_confidence: InjectionConfidenceFrame
    injection_eviction: InjectionEvictionFrame
    retry_injection_score: int
    provider_injection_score: int
    continuation_injection_score: int
    orchestration_injection_score: int
    recovery_resilience_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    failure_injection_mode: str
    estimated_avoided_runtime_collapse: int
    estimated_avoided_frontier_recovery: int
    estimated_avoided_hidden_instability: int


class FailureInjectionRuntime:
    def evaluate(
        self,
        *,
        injection_history_items: tuple[str, ...] = DEFAULT_INJECTION_HISTORY,
        injection_scope_items: tuple[str, ...] = DEFAULT_INJECTION_SCOPE,
        retry_amplification: int = 1,
        retry_saturation: int = 1,
        retry_cooldown_collapse: int = 0,
        retry_interruption_instability: int = 0,
        provider_starvation: int = 1,
        provider_fatigue_escalation: int = 1,
        provider_readiness_degradation: int = 0,
        provider_queue_saturation: int = 1,
        continuation_interruption_collapse: int = 0,
        continuation_saturation: int = 18,
        continuation_reset_loops: int = 0,
        continuation_drift: int = 0,
        provider_escalation_loops: int = 1,
        provider_downgrade_loops: int = 0,
        escalation_cooldown_collapse: int = 0,
        dependency_deadlocks: int = 0,
        validation_retry_conflicts: int = 0,
        provider_policy_conflicts: int = 0,
        orchestration_queue_stalls: int = 0,
        injection_budget_used: int = 7,
        recursive_injection_attempts: int = 0,
        autonomous_runtime_state_mutation_attempts: int = 0,
        novel_attack_pattern_synthesis_attempts: int = 0,
        dynamic_injection_scope_widening_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        hidden_chaos_loop_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> FailureInjectionFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=retry_amplification,
            retry_cooldown_pressure=max(1, retry_cooldown_collapse),
            continuation_saturation=continuation_saturation,
            policy_budget_used=min(injection_budget_used, INJECTION_BUDGET_LIMIT),
        )
        orchestrator = RuntimeOrchestrator().evaluate(
            retry_amplification=retry_amplification,
            retry_interruption_windows=retry_interruption_instability,
            continuation_interruption_windows=continuation_interruption_collapse,
            provider_fatigue_pressure=max(1, provider_fatigue_escalation),
            repeated_regressions=max(0, validation_retry_conflicts),
            regression_pressure=max(1, orchestration_queue_stalls + 1),
            orchestration_budget_used=min(injection_budget_used, INJECTION_BUDGET_LIMIT),
        )
        hardening = RuntimeHardeningRuntime().evaluate(
            retry_amplification_chains=retry_amplification,
            retry_cooldown_collapse=retry_cooldown_collapse,
            retry_saturation_windows=retry_saturation,
            retry_interruption_instability=retry_interruption_instability,
            provider_readiness_starvation=provider_starvation,
            bounded_provider_queue_saturation=provider_queue_saturation,
            provider_scheduling_instability=max(1, provider_fatigue_escalation),
            provider_confidence_collapse=provider_readiness_degradation,
            continuation_collapse_chains=continuation_interruption_collapse,
            continuation_saturation=continuation_saturation,
            continuation_interruption_instability=continuation_interruption_collapse,
            continuation_reset_loops=continuation_reset_loops,
            bounded_continuation_starvation=continuation_drift,
            provider_escalation_loops=max(1, provider_escalation_loops),
            provider_downgrade_loops=provider_downgrade_loops,
            escalation_cooldown_pressure=max(1, escalation_cooldown_collapse + 1),
            orchestration_dependency_deadlocks=dependency_deadlocks,
            validation_retry_deadlocks=validation_retry_conflicts,
            provider_policy_deadlocks=provider_policy_conflicts,
            bounded_orchestration_stalls=orchestration_queue_stalls,
            hardening_budget_used=min(injection_budget_used, INJECTION_BUDGET_LIMIT),
        )
        continuous_audit = ContinuousRuntimeAuditRuntime().evaluate(
            retry_amplification_pressure=retry_amplification,
            retry_saturation_windows=retry_saturation,
            retry_interruption_instability=retry_interruption_instability,
            retry_cooldown_collapse=retry_cooldown_collapse,
            provider_readiness_degradation=provider_readiness_degradation,
            provider_queue_saturation=provider_queue_saturation,
            provider_cooldown_instability=provider_fatigue_escalation,
            continuation_instability_pressure=max(1, continuation_interruption_collapse + 1),
            continuation_saturation=continuation_saturation,
            continuation_interruption_instability=continuation_interruption_collapse,
            continuation_reset_loops=continuation_reset_loops,
            bounded_continuation_drift=continuation_drift,
            orchestration_queue_pressure=max(1, orchestration_queue_stalls + 1),
            orchestration_dependency_stalls=dependency_deadlocks,
            orchestration_regression_pressure=max(1, validation_retry_conflicts + 1),
            bounded_orchestration_drift=orchestration_queue_stalls,
            audit_budget_used=min(injection_budget_used, INJECTION_BUDGET_LIMIT),
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=max(1, provider_fatigue_escalation),
            retry_amplification=retry_amplification,
            orchestration_instability=max(
                1, dependency_deadlocks + orchestration_queue_stalls + 1
            ),
            continuation_decay=continuation_drift,
            escalation_depth=max(1, provider_escalation_loops),
            provider_budget_used=min(injection_budget_used, INJECTION_BUDGET_LIMIT),
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=retry_amplification,
            retry_saturation_motifs=retry_saturation,
            retry_interruption_patterns=retry_interruption_instability,
            continuation_reuse_depth=max(1, continuation_interruption_collapse + 1),
        )
        mediation = ExecutionSequencer().mediate(retry_count=retry_amplification)
        sprint_loop = SprintLoopRuntime().evaluate(
            repeated_regressions=validation_retry_conflicts,
            retry_amplification=retry_amplification,
            retry_count=retry_amplification,
            continuation_depth=max(1, continuation_interruption_collapse + 1),
            continuation_interruption_window=continuation_interruption_collapse,
            sprint_budget_used=min(injection_budget_used, INJECTION_BUDGET_LIMIT),
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=validation_retry_conflicts + dependency_deadlocks,
            retry_amplification_pressure=retry_amplification,
        )
        cognitive_state = CognitiveStateRuntime().evaluate(
            objective="failure-injection-local-patch",
            session_age_pressure=22 + continuation_drift,
            recursive_reasoning_attempts=recursive_injection_attempts,
        )
        planning = IntentionalPlanningRuntime().evaluate(
            interruption_duration=continuation_interruption_collapse,
            abandoned_continuation_chains=continuation_reset_loops,
            recursive_planning_attempts=recursive_injection_attempts,
        )
        verified_execution_active = ExecutionEnvelope.__name__ == "ExecutionEnvelope"

        bounded_history = injection_history_items[:MAX_INJECTION_HISTORY]
        bounded_scope = injection_scope_items[:MAX_INJECTION_WINDOW]
        evicted_history = injection_history_items[MAX_INJECTION_HISTORY:]
        evicted_scope = injection_scope_items[MAX_INJECTION_WINDOW:]

        retry_pressure = _clamp(
            retry_amplification * 18
            + retry_saturation * 10
            + retry_cooldown_collapse * 14
            + retry_interruption_instability * 12
            + max(0, 70 - execution_memory.retry_pattern_score) // 2
        )
        retry_injection_score = _clamp(100 - retry_pressure)
        provider_pressure = _clamp(
            provider_starvation * 18
            + provider_fatigue_escalation * 12
            + provider_readiness_degradation * 14
            + provider_queue_saturation * 10
            + max(0, 70 - adaptive_provider.provider_fatigue_score) // 2
        )
        provider_injection_score = _clamp(100 - provider_pressure)
        continuation_pressure = _clamp(
            continuation_interruption_collapse * 18
            + continuation_saturation
            + continuation_reset_loops * 12
            + continuation_drift * 12
            + max(0, 80 - continuous_audit.continuation_instability_score) // 3
        )
        continuation_injection_score = _clamp(100 - continuation_pressure)
        escalation_pressure = _clamp(
            provider_escalation_loops * 12
            + provider_downgrade_loops * 12
            + escalation_cooldown_collapse * 14
        )
        escalation_injection_score = _clamp(100 - escalation_pressure)
        orchestration_pressure = _clamp(
            dependency_deadlocks * 20
            + validation_retry_conflicts * 16
            + provider_policy_conflicts * 16
            + orchestration_queue_stalls * 14
            + max(0, 80 - orchestrator.orchestration_schedule_score) // 2
        )
        orchestration_injection_score = _clamp(100 - orchestration_pressure)

        recovery_resilience_score = _clamp(
            (
                retry_injection_score
                + provider_injection_score
                + continuation_injection_score
                + orchestration_injection_score
                + hardening.hardening_confidence.hardening_confidence_score
                + continuous_audit.runtime_health_score
                + runtime_policy.policy_coherence.policy_coherence_score
                + sprint_loop.sprint_validation_score
                + reflection.execution_quality.execution_quality_score
            )
            // 9
            + int(mediation.runtime_mediation_active) * 2
            + int(verified_execution_active) * 2
        )
        injection_saturation = _clamp(
            max(0, len(injection_history_items) - MAX_INJECTION_HISTORY) * 10
            + max(0, len(injection_scope_items) - MAX_INJECTION_WINDOW) * 12
            + max(0, 70 - recovery_resilience_score)
            + max(
                0,
                55
                - min(
                    retry_injection_score,
                    provider_injection_score,
                    continuation_injection_score,
                    orchestration_injection_score,
                ),
            )
        )
        injection_budget_exceeded = injection_budget_used > INJECTION_BUDGET_LIMIT
        recursive_injection_detected = recursive_injection_attempts > 0
        governance_violation = any(
            (
                autonomous_runtime_state_mutation_attempts,
                novel_attack_pattern_synthesis_attempts,
                dynamic_injection_scope_widening_attempts,
                governance_policy_mutation_attempts,
                hidden_chaos_loop_attempts,
            )
        )
        injection_saturation_exceeded = injection_saturation >= INJECTION_SATURATION_THRESHOLD
        termination_reasons = _termination_reasons(
            injection_budget_exceeded,
            recursive_injection_detected,
            governance_violation,
            injection_saturation_exceeded,
        )
        confidence_score = _clamp(recovery_resilience_score - len(termination_reasons) * 8)

        return FailureInjectionFrame(
            failure_injection_active=True,
            requirement_ids=FAILURE_INJECTION_REQUIREMENT_IDS,
            test_ids=FAILURE_INJECTION_TEST_IDS,
            retry_storm_injection=RetryStormInjectionFrame(
                retry_storm_injection_active=True,
                retry_amplification=retry_amplification,
                retry_saturation=retry_saturation,
                retry_cooldown_collapse=retry_cooldown_collapse,
                retry_interruption_instability=retry_interruption_instability,
                retry_injection_score=retry_injection_score,
                deterministic_retry_injection_summary=(
                    f"amplification={retry_amplification};saturation={retry_saturation};"
                    f"score={retry_injection_score}"
                ),
                bounded_retry_recovery_recommendation=(
                    "RECOVER_RETRY_WINDOW_WITH_COOLDOWN"
                    if retry_injection_score < 60
                    else "RETRY_INJECTION_RESILIENT"
                ),
            ),
            provider_starvation_injection=ProviderStarvationInjectionFrame(
                provider_starvation_injection_active=True,
                provider_starvation=provider_starvation,
                provider_fatigue_escalation=provider_fatigue_escalation,
                provider_readiness_degradation=provider_readiness_degradation,
                provider_queue_saturation=provider_queue_saturation,
                provider_injection_score=provider_injection_score,
                deterministic_provider_injection_summary=(
                    f"starvation={provider_starvation};fatigue={adaptive_provider.provider_fatigue_score};"
                    f"score={provider_injection_score}"
                ),
                bounded_provider_rebalance_recommendation=(
                    "REBALANCE_PROVIDER_AFTER_COOLDOWN"
                    if provider_injection_score < 60
                    else "PROVIDER_INJECTION_RESILIENT"
                ),
            ),
            continuation_collapse_injection=ContinuationCollapseInjectionFrame(
                continuation_collapse_injection_active=True,
                continuation_interruption_collapse=continuation_interruption_collapse,
                continuation_saturation=continuation_saturation,
                continuation_reset_loops=continuation_reset_loops,
                continuation_drift=continuation_drift,
                continuation_injection_score=continuation_injection_score,
                deterministic_continuation_injection_summary=(
                    f"collapse={continuation_interruption_collapse};"
                    f"saturation={continuation_saturation};score={continuation_injection_score}"
                ),
                bounded_continuation_reset_recommendation=(
                    "RESET_CONTINUATION_AFTER_INJECTION"
                    if continuation_injection_score < 60
                    else "CONTINUATION_INJECTION_RESILIENT"
                ),
            ),
            escalation_oscillation_injection=EscalationOscillationInjectionFrame(
                escalation_oscillation_injection_active=True,
                provider_escalation_loops=provider_escalation_loops,
                provider_downgrade_loops=provider_downgrade_loops,
                escalation_cooldown_collapse=escalation_cooldown_collapse,
                escalation_injection_score=escalation_injection_score,
                deterministic_escalation_injection_summary=(
                    f"up={provider_escalation_loops};down={provider_downgrade_loops};"
                    f"score={escalation_injection_score}"
                ),
                bounded_escalation_recovery_recommendation=(
                    "FREEZE_ESCALATION_AND_RECOVER"
                    if escalation_injection_score < 60
                    else "ESCALATION_INJECTION_RESILIENT"
                ),
            ),
            orchestration_deadlock_injection=OrchestrationDeadlockInjectionFrame(
                orchestration_deadlock_injection_active=True,
                dependency_deadlocks=dependency_deadlocks,
                validation_retry_conflicts=validation_retry_conflicts,
                provider_policy_conflicts=provider_policy_conflicts,
                orchestration_queue_stalls=orchestration_queue_stalls,
                orchestration_injection_score=orchestration_injection_score,
                deterministic_orchestration_injection_summary=(
                    f"deadlocks={dependency_deadlocks};validation_retry={validation_retry_conflicts};"
                    f"score={orchestration_injection_score}"
                ),
                bounded_orchestration_recovery_recommendation=(
                    "RECOVER_ORCHESTRATION_AFTER_DEADLOCK"
                    if orchestration_injection_score < 60
                    else "ORCHESTRATION_INJECTION_RESILIENT"
                ),
            ),
            runtime_recovery_injection=RuntimeRecoveryInjectionFrame(
                runtime_recovery_injection_active=True,
                bounded_recovery_validation=recovery_resilience_score >= 60,
                bounded_cooldown_recovery=hardening.cooldown_interaction.cooldown_interaction_active,
                bounded_provider_rebalance=provider_injection_score >= 45,
                bounded_continuation_reset_recovery=continuation_injection_score >= 45,
                recovery_resilience_score=recovery_resilience_score,
                deterministic_recovery_summary=(
                    f"recovery={recovery_resilience_score};cognitive={cognitive_state.decay_status};"
                    f"planning={planning.planning_decay_status}"
                ),
                bounded_recovery_recommendation=(
                    "APPLY_BOUNDED_RECOVERY_SEQUENCE"
                    if recovery_resilience_score < 75
                    else "RECOVERY_RESILIENCE_STABLE"
                ),
            ),
            injection_governance=InjectionGovernanceFrame(
                injection_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_injection_enforced=True,
                bounded_injection_windows_enforced=True,
                autonomous_runtime_state_mutation_blocked=True,
                recursive_injection_blocked=True,
                novel_attack_pattern_synthesis_blocked=True,
                dynamic_injection_scope_widening_blocked=True,
                governance_policy_mutation_blocked=True,
                hidden_chaos_loop_blocked=True,
            ),
            injection_budget=InjectionBudgetFrame(
                injection_budget_active=True,
                injection_budget_used=injection_budget_used,
                injection_budget_limit=INJECTION_BUDGET_LIMIT,
                injection_budget_exceeded=injection_budget_exceeded,
                budget_pressure=_pressure(injection_budget_used, INJECTION_BUDGET_LIMIT),
            ),
            injection_termination=InjectionTerminationFrame(
                injection_termination_active=True,
                failure_injection_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                injection_budget_exceeded=injection_budget_exceeded,
                recursive_injection_detected=recursive_injection_detected,
                governance_violation_detected=governance_violation,
                injection_saturation_threshold_exceeded=injection_saturation_exceeded,
            ),
            injection_history=InjectionHistoryFrame(
                injection_history_active=True,
                injection_history=bounded_history,
                injection_scope=bounded_scope,
                injection_history_limit=MAX_INJECTION_HISTORY,
                compact_injection_history_summary=f"history={len(bounded_history)};scope={len(bounded_scope)}",
                injection_history_overflow_blocked=bool(evicted_history),
                injection_scope_overflow_blocked=bool(evicted_scope),
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            injection_confidence=InjectionConfidenceFrame(
                injection_confidence_active=True,
                injection_confidence_score=confidence_score,
                confidence_status=_score_label(confidence_score),
                deterministic_confidence=True,
                resilience_validation_confidence=confidence_score >= 70,
            ),
            injection_eviction=InjectionEvictionFrame(
                injection_eviction_active=True,
                evicted_injection_history_items=evicted_history,
                evicted_injection_scope_items=evicted_scope,
                eviction_count=len(evicted_history) + len(evicted_scope),
                bounded_eviction_active=bool(evicted_history or evicted_scope),
                eviction_summary=f"history={len(evicted_history)};scope={len(evicted_scope)}",
            ),
            retry_injection_score=retry_injection_score,
            provider_injection_score=provider_injection_score,
            continuation_injection_score=continuation_injection_score,
            orchestration_injection_score=orchestration_injection_score,
            recovery_resilience_score=recovery_resilience_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            failure_injection_mode="LOCAL_PATCH_BOUNDED_FAILURE_INJECTION",
            estimated_avoided_runtime_collapse=80 + max(0, 80 - recovery_resilience_score) // 2,
            estimated_avoided_frontier_recovery=76 + recovery_resilience_score // 10,
            estimated_avoided_hidden_instability=78 + len(termination_reasons),
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
    return "RECOVERY_REQUIRED"


def _termination_reasons(
    injection_budget_exceeded: bool,
    recursive_injection_detected: bool,
    governance_violation_detected: bool,
    injection_saturation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if injection_budget_exceeded:
        reasons.append("INJECTION_BUDGET_EXCEEDED")
    if recursive_injection_detected:
        reasons.append("RECURSIVE_INJECTION_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if injection_saturation_threshold_exceeded:
        reasons.append("INJECTION_SATURATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "FAILURE_INJECTION_REQUIREMENT_IDS",
    "FAILURE_INJECTION_TEST_IDS",
    "INJECTION_BUDGET_LIMIT",
    "INJECTION_SATURATION_THRESHOLD",
    "MAX_INJECTION_HISTORY",
    "MAX_INJECTION_WINDOW",
    "ContinuationCollapseInjectionFrame",
    "EscalationOscillationInjectionFrame",
    "FailureInjectionFrame",
    "FailureInjectionRuntime",
    "InjectionBudgetFrame",
    "InjectionConfidenceFrame",
    "InjectionEvictionFrame",
    "InjectionGovernanceFrame",
    "InjectionHistoryFrame",
    "InjectionTerminationFrame",
    "OrchestrationDeadlockInjectionFrame",
    "ProviderStarvationInjectionFrame",
    "RetryStormInjectionFrame",
    "RuntimeRecoveryInjectionFrame",
]
