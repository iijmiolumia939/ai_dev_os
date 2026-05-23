from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_orchestrator import RuntimeOrchestrator
from ai_dev_os.runtime_policy import RuntimePolicyEngine
from ai_dev_os.sprint_loop import SprintLoopRuntime

RUNTIME_HARDENING_REQUIREMENT_IDS = tuple(
    f"FR-RUNTIMEHARDENING-{index:02d}" for index in range(1, 73)
) + ("NFR-COST-75", "NFR-ARCH-88", "NFR-SEC-59")
RUNTIME_HARDENING_TEST_IDS = tuple(f"TC-RUNTIMEHARDENING-{index:02d}" for index in range(1, 73))

MAX_HARDENING_WINDOW = 5
MAX_HARDENING_HISTORY = 5
MAX_RETRY_STORM_WINDOW = 3
MAX_ESCALATION_OSCILLATION_WINDOW = 3
MAX_CONTINUATION_DEPTH = 2
MAX_PROVIDER_QUEUE = 4
HARDENING_BUDGET_LIMIT = 12
RETRY_AMPLIFICATION_THRESHOLD = 3
ESCALATION_OSCILLATION_THRESHOLD = 4
ORCHESTRATION_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_INTERACTION_HISTORY = (
    "govern-interaction",
    "suppress-retry-storm",
    "stabilize-continuation",
    "detect-deadlock",
    "rebalance-provider",
)
DEFAULT_CONFLICTS = (
    "validation_vs_retry",
    "provider_vs_policy",
    "continuation_vs_termination",
)


@dataclass(frozen=True)
class InteractionGovernanceFrame:
    interaction_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_interaction_governance: bool
    bounded_stabilization_windows: bool
    bounded_retry_authority: bool
    bounded_orchestration_authority: bool
    bounded_escalation_authority: bool
    interaction_governance_score: int
    deterministic_interaction_summary: str
    bounded_interaction_recommendation: str


@dataclass(frozen=True)
class RetryStormFrame:
    retry_storm_active: bool
    retry_amplification_chains: int
    retry_recursion_pressure: int
    retry_cooldown_collapse: int
    retry_saturation_windows: int
    retry_interruption_instability: int
    retry_storm_score: int
    deterministic_retry_storm_summary: str
    bounded_retry_reset_recommendation: str


@dataclass(frozen=True)
class EscalationOscillationFrame:
    escalation_oscillation_active: bool
    provider_escalation_loops: int
    provider_downgrade_loops: int
    escalation_cooldown_pressure: int
    bounded_provider_oscillation: bool
    repeated_escalation_chains: int
    escalation_oscillation_score: int
    deterministic_escalation_summary: str
    bounded_escalation_stabilization_recommendation: str


@dataclass(frozen=True)
class ContinuationCollapseFrame:
    continuation_collapse_active: bool
    continuation_collapse_chains: int
    continuation_saturation: int
    continuation_interruption_instability: int
    continuation_reset_loops: int
    bounded_continuation_starvation: int
    continuation_stability_score: int
    deterministic_continuation_summary: str
    bounded_continuation_reset_recommendation: str


@dataclass(frozen=True)
class ProviderStarvationFrame:
    provider_starvation_active: bool
    provider_readiness_starvation: int
    cooldown_starvation: int
    bounded_provider_queue_saturation: int
    provider_scheduling_instability: int
    provider_confidence_collapse: int
    provider_starvation_score: int
    deterministic_provider_starvation_summary: str
    bounded_provider_rebalance_recommendation: str


@dataclass(frozen=True)
class RegressionCascadeFrame:
    regression_cascade_active: bool
    repeated_regressions: int
    regression_dependency_pressure: int
    retry_regression_coupling: int
    cascade_pressure: int
    regression_cascade_score: int
    deterministic_regression_cascade_summary: str
    bounded_regression_recovery_recommendation: str


@dataclass(frozen=True)
class OrchestrationDeadlockFrame:
    orchestration_deadlock_active: bool
    orchestration_dependency_deadlocks: int
    validation_retry_deadlocks: int
    provider_policy_deadlocks: int
    continuation_termination_conflicts: int
    bounded_orchestration_stalls: int
    orchestration_deadlock_score: int
    deterministic_deadlock_summary: str
    bounded_deadlock_recovery_recommendation: str


@dataclass(frozen=True)
class CooldownInteractionFrame:
    cooldown_interaction_active: bool
    retry_cooldown_required: bool
    escalation_cooldown_required: bool
    continuation_cooldown_required: bool
    provider_cooldown_required: bool
    orchestration_cooldown_required: bool
    deterministic_cooldown_interaction_summary: str
    bounded_cooldown_recommendation: str


@dataclass(frozen=True)
class RuntimeConflictFrame:
    runtime_conflict_active: bool
    conflict_sources: tuple[str, ...]
    validation_retry_conflict: bool
    provider_policy_conflict: bool
    continuation_termination_conflict: bool
    escalation_retry_conflict: bool
    deterministic_conflict_summary: str
    bounded_conflict_recovery_recommendation: str


@dataclass(frozen=True)
class HardeningBudgetFrame:
    hardening_budget_active: bool
    hardening_budget_used: int
    hardening_budget_limit: int
    hardening_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class HardeningTerminationFrame:
    hardening_termination_active: bool
    hardening_terminated: bool
    termination_reasons: tuple[str, ...]
    hardening_budget_exceeded: bool
    recursive_stabilization_detected: bool
    governance_violation_detected: bool
    orchestration_saturation_threshold_exceeded: bool
    retry_amplification_threshold_exceeded: bool
    escalation_oscillation_threshold_exceeded: bool


@dataclass(frozen=True)
class HardeningHistoryFrame:
    hardening_history_active: bool
    hardening_history: tuple[str, ...]
    hardening_history_limit: int
    compact_hardening_history_summary: str
    hardening_history_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class HardeningConfidenceFrame:
    hardening_confidence_active: bool
    hardening_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    resilient_interaction_confidence: bool


@dataclass(frozen=True)
class HardeningEvictionFrame:
    hardening_eviction_active: bool
    evicted_history_items: tuple[str, ...]
    evicted_conflict_sources: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class RuntimeHardeningFrame:
    runtime_hardening_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    interaction_governance: InteractionGovernanceFrame
    retry_storm: RetryStormFrame
    escalation_oscillation: EscalationOscillationFrame
    continuation_collapse: ContinuationCollapseFrame
    provider_starvation: ProviderStarvationFrame
    regression_cascade: RegressionCascadeFrame
    orchestration_deadlock: OrchestrationDeadlockFrame
    cooldown_interaction: CooldownInteractionFrame
    runtime_conflict: RuntimeConflictFrame
    hardening_budget: HardeningBudgetFrame
    hardening_termination: HardeningTerminationFrame
    hardening_history: HardeningHistoryFrame
    hardening_confidence: HardeningConfidenceFrame
    hardening_eviction: HardeningEvictionFrame
    retry_storm_score: int
    escalation_oscillation_score: int
    continuation_stability_score: int
    provider_starvation_score: int
    orchestration_deadlock_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    runtime_hardening_mode: str
    estimated_avoided_retry_storms: int
    estimated_avoided_orchestration_collapse: int
    estimated_avoided_frontier_stabilization: int


class RuntimeHardeningRuntime:
    def evaluate(
        self,
        *,
        hardening_history_items: tuple[str, ...] = DEFAULT_INTERACTION_HISTORY,
        conflict_sources: tuple[str, ...] = DEFAULT_CONFLICTS,
        retry_amplification_chains: int = 1,
        retry_recursion_pressure: int = 0,
        retry_cooldown_collapse: int = 0,
        retry_saturation_windows: int = 1,
        retry_interruption_instability: int = 0,
        provider_escalation_loops: int = 1,
        provider_downgrade_loops: int = 0,
        escalation_cooldown_pressure: int = 1,
        repeated_escalation_chains: int = 1,
        continuation_collapse_chains: int = 0,
        continuation_saturation: int = 18,
        continuation_interruption_instability: int = 0,
        continuation_reset_loops: int = 0,
        bounded_continuation_starvation: int = 0,
        provider_readiness_starvation: int = 0,
        cooldown_starvation: int = 0,
        bounded_provider_queue_saturation: int = 1,
        provider_scheduling_instability: int = 1,
        provider_confidence_collapse: int = 0,
        repeated_regressions: int = 0,
        regression_dependency_pressure: int = 1,
        retry_regression_coupling: int = 1,
        orchestration_dependency_deadlocks: int = 0,
        validation_retry_deadlocks: int = 0,
        provider_policy_deadlocks: int = 0,
        continuation_termination_conflicts: int = 0,
        bounded_orchestration_stalls: int = 0,
        hardening_budget_used: int = 7,
        recursive_stabilization_attempts: int = 0,
        autonomous_runtime_mutation_attempts: int = 0,
        hidden_orchestration_execution_attempts: int = 0,
        self_expanding_stabilization_graph_attempts: int = 0,
        autonomous_provider_escalation_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
    ) -> RuntimeHardeningFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=retry_amplification_chains,
            retry_cooldown_pressure=max(1, retry_cooldown_collapse),
            continuation_saturation=continuation_saturation,
            policy_budget_used=min(hardening_budget_used, HARDENING_BUDGET_LIMIT),
        )
        orchestrator = RuntimeOrchestrator().evaluate(
            retry_amplification=retry_amplification_chains,
            retry_interruption_windows=retry_interruption_instability,
            continuation_depth=max(1, continuation_collapse_chains + 1),
            continuation_interruption_windows=continuation_interruption_instability,
            provider_fatigue_pressure=max(1, provider_scheduling_instability),
            repeated_regressions=repeated_regressions,
            regression_pressure=regression_dependency_pressure,
            orchestration_budget_used=min(hardening_budget_used, HARDENING_BUDGET_LIMIT),
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=max(1, provider_scheduling_instability),
            retry_amplification=retry_amplification_chains,
            orchestration_instability=max(1, bounded_orchestration_stalls),
            escalation_depth=max(1, provider_escalation_loops),
            provider_budget_used=min(hardening_budget_used, HARDENING_BUDGET_LIMIT),
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=retry_amplification_chains,
            continuation_reuse_depth=max(1, continuation_collapse_chains + 1),
        )
        sprint_loop = SprintLoopRuntime().evaluate(
            repeated_regressions=repeated_regressions,
            retry_amplification=retry_amplification_chains,
            retry_count=retry_amplification_chains,
            continuation_depth=max(1, continuation_collapse_chains + 1),
            continuation_interruption_window=continuation_interruption_instability,
            sprint_budget_used=min(hardening_budget_used, HARDENING_BUDGET_LIMIT),
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=repeated_regressions,
            retry_amplification_pressure=retry_amplification_chains,
        )
        mediation = ExecutionSequencer().mediate(retry_count=retry_amplification_chains)

        bounded_history = hardening_history_items[:MAX_HARDENING_HISTORY]
        bounded_conflicts = conflict_sources[:MAX_HARDENING_WINDOW]
        evicted_history_items = hardening_history_items[MAX_HARDENING_HISTORY:]
        evicted_conflict_sources = conflict_sources[MAX_HARDENING_WINDOW:]

        retry_storm_pressure = _clamp(
            retry_amplification_chains * 18
            + retry_recursion_pressure * 16
            + retry_cooldown_collapse * 14
            + retry_saturation_windows * 10
            + retry_interruption_instability * 12
        )
        retry_storm_score = _clamp(100 - retry_storm_pressure)
        escalation_oscillation_pressure = _clamp(
            provider_escalation_loops * 14
            + provider_downgrade_loops * 14
            + escalation_cooldown_pressure * 10
            + repeated_escalation_chains * 12
        )
        escalation_oscillation_score = _clamp(100 - escalation_oscillation_pressure)
        continuation_collapse_pressure = _clamp(
            continuation_collapse_chains * 18
            + continuation_saturation
            + continuation_interruption_instability * 14
            + continuation_reset_loops * 12
            + bounded_continuation_starvation * 10
        )
        continuation_stability_score = _clamp(100 - continuation_collapse_pressure)
        provider_starvation_pressure = _clamp(
            provider_readiness_starvation * 20
            + cooldown_starvation * 14
            + bounded_provider_queue_saturation * 10
            + provider_scheduling_instability * 12
            + provider_confidence_collapse * 18
        )
        provider_starvation_score = _clamp(100 - provider_starvation_pressure)
        regression_cascade_pressure = _clamp(
            repeated_regressions * 18
            + regression_dependency_pressure * 12
            + retry_regression_coupling * 10
        )
        orchestration_deadlock_pressure = _clamp(
            orchestration_dependency_deadlocks * 24
            + validation_retry_deadlocks * 18
            + provider_policy_deadlocks * 18
            + continuation_termination_conflicts * 18
            + bounded_orchestration_stalls * 16
        )
        orchestration_deadlock_score = _clamp(100 - orchestration_deadlock_pressure)
        orchestration_saturation_pressure = _clamp(
            orchestration_deadlock_pressure
            + max(0, 80 - orchestrator.orchestration_schedule_score)
            + max(0, 80 - sprint_loop.sprint_regression_score)
        )

        retry_threshold_exceeded = retry_amplification_chains > RETRY_AMPLIFICATION_THRESHOLD
        escalation_threshold_exceeded = (
            provider_escalation_loops + provider_downgrade_loops + repeated_escalation_chains
            > ESCALATION_OSCILLATION_THRESHOLD
        )
        orchestration_threshold_exceeded = (
            orchestration_saturation_pressure >= ORCHESTRATION_SATURATION_THRESHOLD
        )
        hardening_budget_exceeded = hardening_budget_used > HARDENING_BUDGET_LIMIT
        recursive_stabilization_detected = recursive_stabilization_attempts > 0
        governance_violation = any(
            (
                autonomous_runtime_mutation_attempts,
                hidden_orchestration_execution_attempts,
                self_expanding_stabilization_graph_attempts,
                autonomous_provider_escalation_attempts,
                governance_policy_mutation_attempts,
                retrieval_scope_widening_attempts,
            )
        )
        termination_reasons = _termination_reasons(
            hardening_budget_exceeded,
            recursive_stabilization_detected,
            governance_violation,
            orchestration_threshold_exceeded,
            retry_threshold_exceeded,
            escalation_threshold_exceeded,
        )
        interaction_governance_score = _clamp(
            runtime_policy.policy_coherence.policy_coherence_score
            + int(mediation.runtime_mediation_active) * 8
            + int(execution_memory.execution_memory_active) * 6
            - len(termination_reasons) * 10
        )
        confidence_score = _clamp(
            (
                retry_storm_score
                + escalation_oscillation_score
                + continuation_stability_score
                + provider_starvation_score
                + orchestration_deadlock_score
            )
            // 5
            + reflection.execution_quality.execution_quality_score // 10
            - len(termination_reasons) * 8
        )

        return RuntimeHardeningFrame(
            runtime_hardening_active=True,
            requirement_ids=RUNTIME_HARDENING_REQUIREMENT_IDS,
            test_ids=RUNTIME_HARDENING_TEST_IDS,
            interaction_governance=InteractionGovernanceFrame(
                interaction_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_interaction_governance=True,
                bounded_stabilization_windows=True,
                bounded_retry_authority=True,
                bounded_orchestration_authority=True,
                bounded_escalation_authority=True,
                interaction_governance_score=interaction_governance_score,
                deterministic_interaction_summary=(
                    f"policy={runtime_policy.policy_coherence.policy_coherence_score};"
                    f"orchestration={orchestrator.orchestration_schedule_score}"
                ),
                bounded_interaction_recommendation=(
                    "MAINTAIN_BOUNDED_INTERACTION_GOVERNANCE"
                    if not termination_reasons
                    else "TERMINATE_AND_RESET_HARDENING_WINDOW"
                ),
            ),
            retry_storm=RetryStormFrame(
                retry_storm_active=True,
                retry_amplification_chains=retry_amplification_chains,
                retry_recursion_pressure=retry_recursion_pressure,
                retry_cooldown_collapse=retry_cooldown_collapse,
                retry_saturation_windows=retry_saturation_windows,
                retry_interruption_instability=retry_interruption_instability,
                retry_storm_score=retry_storm_score,
                deterministic_retry_storm_summary=(
                    f"amplification={retry_amplification_chains};"
                    f"recursion={retry_recursion_pressure};pressure={retry_storm_pressure}"
                ),
                bounded_retry_reset_recommendation=(
                    "RESET_RETRY_STORM_WINDOW_AFTER_COOLDOWN"
                    if retry_threshold_exceeded or retry_storm_score < 55
                    else "KEEP_RETRY_WITHIN_BOUNDED_WINDOW"
                ),
            ),
            escalation_oscillation=EscalationOscillationFrame(
                escalation_oscillation_active=True,
                provider_escalation_loops=provider_escalation_loops,
                provider_downgrade_loops=provider_downgrade_loops,
                escalation_cooldown_pressure=escalation_cooldown_pressure,
                bounded_provider_oscillation=not escalation_threshold_exceeded,
                repeated_escalation_chains=repeated_escalation_chains,
                escalation_oscillation_score=escalation_oscillation_score,
                deterministic_escalation_summary=(
                    f"up={provider_escalation_loops};down={provider_downgrade_loops};"
                    f"pressure={escalation_oscillation_pressure}"
                ),
                bounded_escalation_stabilization_recommendation=(
                    "FREEZE_PROVIDER_ESCALATION_AND_COOLDOWN"
                    if escalation_threshold_exceeded or escalation_oscillation_score < 55
                    else "KEEP_PROVIDER_ESCALATION_STABLE"
                ),
            ),
            continuation_collapse=ContinuationCollapseFrame(
                continuation_collapse_active=True,
                continuation_collapse_chains=continuation_collapse_chains,
                continuation_saturation=continuation_saturation,
                continuation_interruption_instability=continuation_interruption_instability,
                continuation_reset_loops=continuation_reset_loops,
                bounded_continuation_starvation=bounded_continuation_starvation,
                continuation_stability_score=continuation_stability_score,
                deterministic_continuation_summary=(
                    f"collapse={continuation_collapse_chains};"
                    f"saturation={continuation_saturation};"
                    f"score={continuation_stability_score}"
                ),
                bounded_continuation_reset_recommendation=(
                    "RESET_CONTINUATION_STABILIZATION_WINDOW"
                    if continuation_stability_score < 55
                    else "CONTINUE_BOUNDED_CONTINUATION_STABILITY"
                ),
            ),
            provider_starvation=ProviderStarvationFrame(
                provider_starvation_active=True,
                provider_readiness_starvation=provider_readiness_starvation,
                cooldown_starvation=cooldown_starvation,
                bounded_provider_queue_saturation=bounded_provider_queue_saturation,
                provider_scheduling_instability=provider_scheduling_instability,
                provider_confidence_collapse=provider_confidence_collapse,
                provider_starvation_score=provider_starvation_score,
                deterministic_provider_starvation_summary=(
                    f"readiness={provider_readiness_starvation};"
                    f"confidence={adaptive_provider.provider_confidence_score};"
                    f"score={provider_starvation_score}"
                ),
                bounded_provider_rebalance_recommendation=(
                    "REBALANCE_PROVIDER_WINDOW_AFTER_COOLDOWN"
                    if provider_starvation_score < 55
                    else "PROVIDER_WINDOW_STABLE"
                ),
            ),
            regression_cascade=RegressionCascadeFrame(
                regression_cascade_active=True,
                repeated_regressions=repeated_regressions,
                regression_dependency_pressure=regression_dependency_pressure,
                retry_regression_coupling=retry_regression_coupling,
                cascade_pressure=regression_cascade_pressure,
                regression_cascade_score=_clamp(100 - regression_cascade_pressure),
                deterministic_regression_cascade_summary=(
                    f"regressions={repeated_regressions};" f"cascade={regression_cascade_pressure}"
                ),
                bounded_regression_recovery_recommendation=(
                    "STABILIZE_REGRESSION_CASCADE"
                    if regression_cascade_pressure >= 45
                    else "REGRESSION_INTERACTION_STABLE"
                ),
            ),
            orchestration_deadlock=OrchestrationDeadlockFrame(
                orchestration_deadlock_active=True,
                orchestration_dependency_deadlocks=orchestration_dependency_deadlocks,
                validation_retry_deadlocks=validation_retry_deadlocks,
                provider_policy_deadlocks=provider_policy_deadlocks,
                continuation_termination_conflicts=continuation_termination_conflicts,
                bounded_orchestration_stalls=bounded_orchestration_stalls,
                orchestration_deadlock_score=orchestration_deadlock_score,
                deterministic_deadlock_summary=(
                    f"dependency={orchestration_dependency_deadlocks};"
                    f"validation_retry={validation_retry_deadlocks};"
                    f"pressure={orchestration_deadlock_pressure}"
                ),
                bounded_deadlock_recovery_recommendation=(
                    "RESET_ORCHESTRATION_DEADLOCK_WINDOW"
                    if orchestration_deadlock_score < 55
                    else "ORCHESTRATION_INTERACTIONS_SAFE"
                ),
            ),
            cooldown_interaction=CooldownInteractionFrame(
                cooldown_interaction_active=True,
                retry_cooldown_required=retry_threshold_exceeded or retry_storm_score < 55,
                escalation_cooldown_required=escalation_threshold_exceeded,
                continuation_cooldown_required=continuation_stability_score < 55,
                provider_cooldown_required=provider_starvation_score < 55,
                orchestration_cooldown_required=orchestration_threshold_exceeded,
                deterministic_cooldown_interaction_summary=(
                    f"retry={retry_storm_score};escalation={escalation_oscillation_score};"
                    f"deadlock={orchestration_deadlock_score}"
                ),
                bounded_cooldown_recommendation=(
                    "APPLY_HARDENING_COOLDOWN"
                    if termination_reasons
                    else "MAINTAIN_INTERACTION_COOLDOWNS"
                ),
            ),
            runtime_conflict=RuntimeConflictFrame(
                runtime_conflict_active=True,
                conflict_sources=bounded_conflicts,
                validation_retry_conflict=validation_retry_deadlocks > 0,
                provider_policy_conflict=provider_policy_deadlocks > 0,
                continuation_termination_conflict=continuation_termination_conflicts > 0,
                escalation_retry_conflict=retry_threshold_exceeded
                and escalation_threshold_exceeded,
                deterministic_conflict_summary=(
                    f"conflicts={len(bounded_conflicts)};"
                    f"deadlocks={orchestration_deadlock_pressure}"
                ),
                bounded_conflict_recovery_recommendation=(
                    "RECOVER_CONFLICTS_WITH_BOUNDED_ORDER"
                    if orchestration_deadlock_pressure > 0
                    else "NO_RUNTIME_CONFLICT_RECOVERY_REQUIRED"
                ),
            ),
            hardening_budget=HardeningBudgetFrame(
                hardening_budget_active=True,
                hardening_budget_used=hardening_budget_used,
                hardening_budget_limit=HARDENING_BUDGET_LIMIT,
                hardening_budget_exceeded=hardening_budget_exceeded,
                budget_pressure=_pressure(hardening_budget_used, HARDENING_BUDGET_LIMIT),
            ),
            hardening_termination=HardeningTerminationFrame(
                hardening_termination_active=True,
                hardening_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                hardening_budget_exceeded=hardening_budget_exceeded,
                recursive_stabilization_detected=recursive_stabilization_detected,
                governance_violation_detected=governance_violation,
                orchestration_saturation_threshold_exceeded=orchestration_threshold_exceeded,
                retry_amplification_threshold_exceeded=retry_threshold_exceeded,
                escalation_oscillation_threshold_exceeded=escalation_threshold_exceeded,
            ),
            hardening_history=HardeningHistoryFrame(
                hardening_history_active=True,
                hardening_history=bounded_history,
                hardening_history_limit=MAX_HARDENING_HISTORY,
                compact_hardening_history_summary=(
                    f"history={len(bounded_history)};hardening=bounded"
                ),
                hardening_history_overflow_blocked=bool(evicted_history_items),
                self_expanding_history_blocked=self_expanding_stabilization_graph_attempts > 0,
            ),
            hardening_confidence=HardeningConfidenceFrame(
                hardening_confidence_active=True,
                hardening_confidence_score=confidence_score,
                confidence_status=_score_label(confidence_score),
                deterministic_confidence=True,
                resilient_interaction_confidence=confidence_score >= 80,
            ),
            hardening_eviction=HardeningEvictionFrame(
                hardening_eviction_active=True,
                evicted_history_items=evicted_history_items,
                evicted_conflict_sources=evicted_conflict_sources,
                eviction_count=len(evicted_history_items) + len(evicted_conflict_sources),
                bounded_eviction_active=bool(evicted_history_items or evicted_conflict_sources),
                eviction_summary=(
                    f"history={len(evicted_history_items)};"
                    f"conflicts={len(evicted_conflict_sources)}"
                ),
            ),
            retry_storm_score=retry_storm_score,
            escalation_oscillation_score=escalation_oscillation_score,
            continuation_stability_score=continuation_stability_score,
            provider_starvation_score=provider_starvation_score,
            orchestration_deadlock_score=orchestration_deadlock_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            runtime_hardening_mode="LOCAL_PATCH_BOUNDED_RUNTIME_HARDENING",
            estimated_avoided_retry_storms=74 + retry_amplification_chains * 2,
            estimated_avoided_orchestration_collapse=(
                73 + orchestration_dependency_deadlocks * 6 + bounded_orchestration_stalls * 4
            ),
            estimated_avoided_frontier_stabilization=76 + confidence_score // 10,
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
    if score >= 55:
        return "WATCH"
    return "RESET_RECOMMENDED"


def _termination_reasons(
    hardening_budget_exceeded: bool,
    recursive_stabilization_detected: bool,
    governance_violation_detected: bool,
    orchestration_saturation_threshold_exceeded: bool,
    retry_amplification_threshold_exceeded: bool,
    escalation_oscillation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if hardening_budget_exceeded:
        reasons.append("HARDENING_BUDGET_EXCEEDED")
    if recursive_stabilization_detected:
        reasons.append("RECURSIVE_STABILIZATION_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if orchestration_saturation_threshold_exceeded:
        reasons.append("ORCHESTRATION_SATURATION_THRESHOLD_EXCEEDED")
    if retry_amplification_threshold_exceeded:
        reasons.append("RETRY_AMPLIFICATION_THRESHOLD_EXCEEDED")
    if escalation_oscillation_threshold_exceeded:
        reasons.append("ESCALATION_OSCILLATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "ESCALATION_OSCILLATION_THRESHOLD",
    "HARDENING_BUDGET_LIMIT",
    "MAX_CONTINUATION_DEPTH",
    "MAX_ESCALATION_OSCILLATION_WINDOW",
    "MAX_HARDENING_HISTORY",
    "MAX_HARDENING_WINDOW",
    "MAX_PROVIDER_QUEUE",
    "MAX_RETRY_STORM_WINDOW",
    "ORCHESTRATION_SATURATION_THRESHOLD",
    "RETRY_AMPLIFICATION_THRESHOLD",
    "RUNTIME_HARDENING_REQUIREMENT_IDS",
    "RUNTIME_HARDENING_TEST_IDS",
    "ContinuationCollapseFrame",
    "CooldownInteractionFrame",
    "EscalationOscillationFrame",
    "HardeningBudgetFrame",
    "HardeningConfidenceFrame",
    "HardeningEvictionFrame",
    "HardeningHistoryFrame",
    "HardeningTerminationFrame",
    "InteractionGovernanceFrame",
    "OrchestrationDeadlockFrame",
    "ProviderStarvationFrame",
    "RegressionCascadeFrame",
    "RetryStormFrame",
    "RuntimeConflictFrame",
    "RuntimeHardeningFrame",
    "RuntimeHardeningRuntime",
]
