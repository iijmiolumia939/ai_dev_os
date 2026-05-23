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
from ai_dev_os.soak_stability import SoakStabilityRuntime
from ai_dev_os.sprint_loop import SprintLoopRuntime
from ai_dev_os.verified_execution import VerifiedExecutionRuntime

PROVIDER_COST_STABILIZATION_REQUIREMENT_IDS = tuple(
    f"FR-PROVIDERCOSTSTABILIZATION-{index:02d}" for index in range(1, 57)
) + (
    "NFR-COST-83",
    "NFR-ARCH-96",
    "NFR-SEC-67",
)
PROVIDER_COST_STABILIZATION_TEST_IDS = tuple(
    f"TC-PROVIDERCOSTSTABILIZATION-{index:02d}" for index in range(1, 57)
)

MAX_COST_WINDOW = 5
MAX_COST_HISTORY = 5
COST_BUDGET_LIMIT = 12
COST_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_COST_HISTORY = (
    "frontier-escalation",
    "retry-cost",
    "continuation-reuse",
    "orchestration-cost",
    "local-first-efficiency",
)
DEFAULT_COST_SCOPE = (
    "frontier",
    "retry",
    "continuation",
    "orchestration",
    "local-first",
)


@dataclass(frozen=True)
class FrontierEscalationSuppressionFrame:
    frontier_escalation_suppression_active: bool
    unnecessary_escalation_pressure: int
    escalation_cooldown_instability: int
    bounded_frontier_routing_pressure: int
    frontier_dependency_pressure: int
    frontier_dependency_score: int
    deterministic_frontier_cost_summary: str
    bounded_frontier_recommendation: str


@dataclass(frozen=True)
class RetryCostFlatteningFrame:
    retry_cost_flattening_active: bool
    retry_cost_accumulation: int
    retry_saturation_cost: int
    retry_cooldown_efficiency: int
    retry_recovery_reuse: int
    retry_cost_score: int
    deterministic_retry_cost_summary: str
    bounded_retry_cost_recommendation: str


@dataclass(frozen=True)
class ContinuationReuseOptimizationFrame:
    continuation_reuse_optimization_active: bool
    continuation_reuse_optimization: int
    continuation_reset_suppression: int
    continuation_persistence_reuse: int
    bounded_continuation_cost_drift: int
    continuation_reuse_score: int
    deterministic_continuation_reuse_summary: str
    bounded_continuation_reuse_recommendation: str


@dataclass(frozen=True)
class OrchestrationCostFlatteningFrame:
    orchestration_cost_flattening_active: bool
    orchestration_cost_flattening: int
    orchestration_queue_efficiency: int
    orchestration_dependency_reuse: int
    orchestration_stabilization_reuse: int
    orchestration_cost_score: int
    deterministic_orchestration_cost_summary: str
    bounded_orchestration_cost_recommendation: str


@dataclass(frozen=True)
class LocalFirstPersistenceFrame:
    local_first_persistence_active: bool
    local_first_execution_persistence: int
    bounded_provider_rebalance_cost: int
    bounded_local_execution_reuse: int
    provider_specific_reuse: int
    local_first_efficiency_score: int
    deterministic_local_first_summary: str
    bounded_local_first_recommendation: str


@dataclass(frozen=True)
class ProviderRoutingEfficiencyFrame:
    provider_routing_efficiency_active: bool
    provider_routing_efficiency: int
    provider_cost_pressure_score: int
    provider_fatigue_cost_pressure: int
    bounded_provider_routing_stabilization: bool
    provider_routing_efficiency_score: int
    deterministic_provider_routing_summary: str
    bounded_provider_routing_recommendation: str


@dataclass(frozen=True)
class RuntimeCostPressureFrame:
    runtime_cost_pressure_active: bool
    runtime_cost_drift: int
    orchestration_overhead_pressure: int
    continuation_entropy_cost: int
    soak_cost_pressure: int
    runtime_cost_pressure_score: int
    deterministic_runtime_cost_summary: str
    bounded_runtime_cost_recommendation: str


@dataclass(frozen=True)
class CostGovernanceFrame:
    cost_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_cost_evaluation_enforced: bool
    bounded_cost_windows_enforced: bool
    autonomous_runtime_state_mutation_blocked: bool
    recursive_provider_optimization_blocked: bool
    novel_cost_heuristic_synthesis_blocked: bool
    dynamic_routing_scope_widening_blocked: bool
    governance_policy_mutation_blocked: bool
    hidden_optimization_loop_blocked: bool


@dataclass(frozen=True)
class CostBudgetFrame:
    cost_budget_active: bool
    cost_budget_used: int
    cost_budget_limit: int
    cost_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class CostTerminationFrame:
    cost_termination_active: bool
    provider_cost_stabilization_terminated: bool
    termination_reasons: tuple[str, ...]
    cost_budget_exceeded: bool
    recursive_optimization_detected: bool
    governance_violation_detected: bool
    cost_saturation_threshold_exceeded: bool


@dataclass(frozen=True)
class CostHistoryFrame:
    cost_history_active: bool
    cost_history: tuple[str, ...]
    cost_scope: tuple[str, ...]
    cost_history_limit: int
    compact_cost_history_summary: str
    cost_history_overflow_blocked: bool
    cost_scope_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class CostConfidenceFrame:
    cost_confidence_active: bool
    cost_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    cost_stabilization_confidence: bool


@dataclass(frozen=True)
class CostEvictionFrame:
    cost_eviction_active: bool
    evicted_cost_history_items: tuple[str, ...]
    evicted_cost_scope_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class ProviderCostStabilizationFrame:
    provider_cost_stabilization_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    frontier_escalation_suppression: FrontierEscalationSuppressionFrame
    retry_cost_flattening: RetryCostFlatteningFrame
    continuation_reuse_optimization: ContinuationReuseOptimizationFrame
    orchestration_cost_flattening: OrchestrationCostFlatteningFrame
    local_first_persistence: LocalFirstPersistenceFrame
    provider_routing_efficiency: ProviderRoutingEfficiencyFrame
    runtime_cost_pressure: RuntimeCostPressureFrame
    cost_governance: CostGovernanceFrame
    cost_budget: CostBudgetFrame
    cost_termination: CostTerminationFrame
    cost_history: CostHistoryFrame
    cost_confidence: CostConfidenceFrame
    cost_eviction: CostEvictionFrame
    frontier_dependency_score: int
    retry_cost_score: int
    continuation_reuse_score: int
    orchestration_cost_score: int
    local_first_efficiency_score: int
    provider_routing_efficiency_score: int
    runtime_cost_pressure_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    provider_cost_stabilization_mode: str
    estimated_avoided_frontier_escalation: int
    estimated_avoided_cost_drift: int
    estimated_avoided_runtime_overhead: int


class ProviderCostStabilizationRuntime:
    def evaluate(
        self,
        *,
        cost_history_items: tuple[str, ...] = DEFAULT_COST_HISTORY,
        cost_scope_items: tuple[str, ...] = DEFAULT_COST_SCOPE,
        unnecessary_escalation_pressure: int = 1,
        escalation_cooldown_instability: int = 0,
        bounded_frontier_routing_pressure: int = 1,
        frontier_dependency_pressure: int = 1,
        retry_cost_accumulation: int = 1,
        retry_saturation_cost: int = 1,
        retry_cooldown_efficiency: int = 4,
        retry_recovery_reuse: int = 4,
        continuation_reuse_optimization: int = 4,
        continuation_reset_suppression: int = 4,
        continuation_persistence_reuse: int = 4,
        bounded_continuation_cost_drift: int = 0,
        orchestration_cost_flattening: int = 4,
        orchestration_queue_efficiency: int = 4,
        orchestration_dependency_reuse: int = 4,
        orchestration_stabilization_reuse: int = 4,
        local_first_execution_persistence: int = 4,
        bounded_provider_rebalance_cost: int = 1,
        bounded_local_execution_reuse: int = 4,
        provider_specific_reuse: int = 4,
        provider_routing_efficiency: int = 4,
        runtime_cost_drift: int = 1,
        orchestration_overhead_pressure: int = 1,
        cost_budget_used: int = 7,
        recursive_provider_optimization_attempts: int = 0,
        autonomous_runtime_state_mutation_attempts: int = 0,
        novel_cost_heuristic_synthesis_attempts: int = 0,
        dynamic_routing_scope_widening_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        hidden_optimization_loop_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> ProviderCostStabilizationFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=retry_cost_accumulation,
            retry_cooldown_pressure=max(1, 5 - retry_cooldown_efficiency),
            continuation_saturation=max(18, 22 - continuation_reuse_optimization),
            policy_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        orchestrator = RuntimeOrchestrator().evaluate(
            retry_amplification=retry_cost_accumulation,
            retry_interruption_windows=max(0, retry_saturation_cost - retry_recovery_reuse),
            continuation_interruption_windows=max(0, bounded_continuation_cost_drift),
            provider_fatigue_pressure=max(1, bounded_provider_rebalance_cost),
            repeated_regressions=max(0, orchestration_overhead_pressure),
            regression_pressure=max(1, orchestration_overhead_pressure),
            orchestration_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        hardening = RuntimeHardeningRuntime().evaluate(
            retry_amplification_chains=retry_cost_accumulation,
            retry_cooldown_collapse=max(0, 4 - retry_cooldown_efficiency),
            retry_saturation_windows=retry_saturation_cost,
            retry_interruption_instability=max(0, retry_saturation_cost - retry_recovery_reuse),
            provider_readiness_starvation=max(0, bounded_provider_rebalance_cost - 1),
            bounded_provider_queue_saturation=bounded_frontier_routing_pressure,
            provider_scheduling_instability=max(1, bounded_provider_rebalance_cost),
            continuation_saturation=max(18, 22 - continuation_reuse_optimization),
            continuation_interruption_instability=bounded_continuation_cost_drift,
            continuation_reset_loops=max(0, 4 - continuation_reset_suppression),
            bounded_continuation_starvation=bounded_continuation_cost_drift,
            repeated_regressions=orchestration_overhead_pressure,
            regression_dependency_pressure=max(1, frontier_dependency_pressure),
            orchestration_dependency_deadlocks=max(0, frontier_dependency_pressure - 1),
            bounded_orchestration_stalls=max(0, 4 - orchestration_queue_efficiency),
            hardening_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        continuous_audit = ContinuousRuntimeAuditRuntime().evaluate(
            retry_amplification_pressure=retry_cost_accumulation,
            retry_saturation_windows=retry_saturation_cost,
            retry_cooldown_collapse=max(0, 4 - retry_cooldown_efficiency),
            retry_recovery_instability=max(0, retry_saturation_cost - retry_recovery_reuse),
            provider_readiness_degradation=max(0, bounded_provider_rebalance_cost - 1),
            provider_queue_saturation=bounded_frontier_routing_pressure,
            provider_cooldown_instability=escalation_cooldown_instability,
            continuation_instability_pressure=max(1, bounded_continuation_cost_drift + 1),
            continuation_saturation=max(18, 22 - continuation_reuse_optimization),
            continuation_interruption_instability=bounded_continuation_cost_drift,
            continuation_reset_loops=max(0, 4 - continuation_reset_suppression),
            bounded_continuation_drift=bounded_continuation_cost_drift,
            orchestration_queue_pressure=max(1, 5 - orchestration_queue_efficiency),
            orchestration_dependency_stalls=max(0, frontier_dependency_pressure - 1),
            orchestration_cooldown_pressure=max(1, 5 - orchestration_stabilization_reuse),
            orchestration_regression_pressure=orchestration_overhead_pressure,
            bounded_orchestration_drift=runtime_cost_drift,
            audit_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        failure_injection = FailureInjectionRuntime().evaluate(
            retry_amplification=retry_cost_accumulation,
            retry_saturation=retry_saturation_cost,
            retry_cooldown_collapse=max(0, 4 - retry_cooldown_efficiency),
            retry_interruption_instability=max(0, retry_saturation_cost - retry_recovery_reuse),
            provider_fatigue_escalation=max(1, bounded_provider_rebalance_cost),
            provider_readiness_degradation=max(0, bounded_provider_rebalance_cost - 1),
            provider_queue_saturation=bounded_frontier_routing_pressure,
            continuation_saturation=max(18, 22 - continuation_reuse_optimization),
            continuation_reset_loops=max(0, 4 - continuation_reset_suppression),
            continuation_drift=bounded_continuation_cost_drift,
            dependency_deadlocks=max(0, frontier_dependency_pressure - 1),
            orchestration_queue_stalls=max(0, 4 - orchestration_queue_efficiency),
            validation_retry_conflicts=orchestration_overhead_pressure,
            injection_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        soak_stability = SoakStabilityRuntime().evaluate(
            retry_accumulation=retry_cost_accumulation,
            retry_saturation_persistence=retry_saturation_cost,
            retry_cooldown_degradation=max(0, 4 - retry_cooldown_efficiency),
            retry_recovery_drift=max(0, retry_saturation_cost - retry_recovery_reuse),
            provider_fatigue_accumulation=max(1, bounded_provider_rebalance_cost),
            provider_queue_drift=bounded_frontier_routing_pressure,
            continuation_entropy=max(1, bounded_continuation_cost_drift + 1),
            continuation_drift_accumulation=bounded_continuation_cost_drift,
            continuation_reset_persistence=max(0, 4 - continuation_reset_suppression),
            orchestration_queue_drift=max(1, 5 - orchestration_queue_efficiency),
            orchestration_dependency_accumulation=max(0, frontier_dependency_pressure - 1),
            orchestration_cooldown_persistence=max(1, 5 - orchestration_stabilization_reuse),
            orchestration_regression_accumulation=orchestration_overhead_pressure,
            runtime_interaction_entropy=runtime_cost_drift,
            soak_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=max(1, runtime_cost_drift),
            retry_amplification=retry_cost_accumulation,
            orchestration_instability=max(1, orchestration_overhead_pressure),
            continuation_decay=bounded_continuation_cost_drift,
            estimated_token_pressure=20 + unnecessary_escalation_pressure * 8,
            bounded_reasoning_cost=12 + bounded_frontier_routing_pressure * 4,
            bounded_execution_cost=10 + bounded_provider_rebalance_cost * 3,
            bounded_escalation_pressure=unnecessary_escalation_pressure,
            provider_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
            escalation_depth=max(1, unnecessary_escalation_pressure),
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=retry_cost_accumulation,
            retry_cooldown_reuse=retry_cooldown_efficiency,
            retry_saturation_motifs=retry_saturation_cost,
            retry_interruption_patterns=max(0, retry_saturation_cost - retry_recovery_reuse),
            continuation_reuse_depth=max(1, 5 - bounded_continuation_cost_drift),
            execution_memory_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        mediation = ExecutionSequencer().mediate(retry_count=retry_cost_accumulation)
        sprint_loop = SprintLoopRuntime().evaluate(
            repeated_regressions=orchestration_overhead_pressure,
            retry_amplification=retry_cost_accumulation,
            retry_count=retry_cost_accumulation,
            continuation_depth=max(1, 5 - bounded_continuation_cost_drift),
            continuation_interruption_window=bounded_continuation_cost_drift,
            sprint_budget_used=min(cost_budget_used, COST_BUDGET_LIMIT),
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=orchestration_overhead_pressure,
            retry_amplification_pressure=retry_cost_accumulation,
        )
        cognitive_state = CognitiveStateRuntime().evaluate(
            objective="provider-cost-stabilization-local-patch",
            session_age_pressure=18 + runtime_cost_drift,
            recursive_reasoning_attempts=recursive_provider_optimization_attempts,
        )
        planning = IntentionalPlanningRuntime().evaluate(
            interruption_duration=bounded_continuation_cost_drift,
            abandoned_continuation_chains=max(0, 4 - continuation_reset_suppression),
            recursive_planning_attempts=recursive_provider_optimization_attempts,
        )
        verified_execution = VerifiedExecutionRuntime().evaluate()

        bounded_history = cost_history_items[:MAX_COST_HISTORY]
        bounded_scope = cost_scope_items[:MAX_COST_WINDOW]
        evicted_history = cost_history_items[MAX_COST_HISTORY:]
        evicted_scope = cost_scope_items[MAX_COST_WINDOW:]

        frontier_pressure = _clamp(
            unnecessary_escalation_pressure * 18
            + escalation_cooldown_instability * 14
            + bounded_frontier_routing_pressure * 10
            + frontier_dependency_pressure * 12
            + max(0, 70 - adaptive_provider.provider_confidence_score) // 3
        )
        frontier_dependency_score = _clamp(100 - frontier_pressure)
        retry_pressure = _clamp(
            retry_cost_accumulation * 15
            + retry_saturation_cost * 11
            + max(0, 4 - retry_cooldown_efficiency) * 12
            + max(0, 4 - retry_recovery_reuse) * 10
            + max(0, 70 - execution_memory.retry_pattern_score) // 3
        )
        retry_cost_score = _clamp(100 - retry_pressure)
        continuation_pressure = _clamp(
            max(0, 4 - continuation_reuse_optimization) * 14
            + max(0, 4 - continuation_reset_suppression) * 10
            + max(0, 4 - continuation_persistence_reuse) * 10
            + bounded_continuation_cost_drift * 14
            + max(0, 75 - soak_stability.continuation_entropy_score) // 3
        )
        continuation_reuse_score = _clamp(100 - continuation_pressure)
        orchestration_pressure = _clamp(
            max(0, 4 - orchestration_cost_flattening) * 14
            + max(0, 4 - orchestration_queue_efficiency) * 12
            + max(0, 4 - orchestration_dependency_reuse) * 12
            + max(0, 4 - orchestration_stabilization_reuse) * 10
            + orchestration_overhead_pressure * 10
            + max(0, 80 - orchestrator.orchestration_schedule_score) // 2
        )
        orchestration_cost_score = _clamp(100 - orchestration_pressure)
        local_first_pressure = _clamp(
            max(0, 4 - local_first_execution_persistence) * 12
            + bounded_provider_rebalance_cost * 10
            + max(0, 4 - bounded_local_execution_reuse) * 12
            + max(0, 4 - provider_specific_reuse) * 10
            + max(0, 70 - execution_memory.provider_execution_memory_score) // 3
        )
        local_first_efficiency_score = _clamp(100 - local_first_pressure)
        provider_routing_efficiency_score = _clamp(
            (
                adaptive_provider.provider_confidence_score
                + runtime_policy.provider_policy_score
                + local_first_efficiency_score
                + frontier_dependency_score
            )
            // 4
            + provider_routing_efficiency * 2
            - bounded_provider_rebalance_cost * 3
        )
        runtime_cost_pressure_score = _clamp(
            (
                continuous_audit.runtime_health_score
                + failure_injection.recovery_resilience_score
                + soak_stability.runtime_interaction_entropy_score
                + hardening.hardening_confidence.hardening_confidence_score
                + sprint_loop.sprint_validation_score
                + reflection.execution_quality.execution_quality_score
                + verified_execution.confidence.confidence_score
            )
            // 7
            - runtime_cost_drift * 5
            - orchestration_overhead_pressure * 3
            + int(mediation.runtime_mediation_active) * 2
        )
        cognitive_cost_penalty = max(0, 60 - cognitive_state.decay.decay_score)
        planning_cost_penalty = 0 if planning.planning_decay_status == "STABLE" else 8
        confidence_score = _clamp(
            (
                frontier_dependency_score
                + retry_cost_score
                + continuation_reuse_score
                + orchestration_cost_score
                + local_first_efficiency_score
                + provider_routing_efficiency_score
                + runtime_cost_pressure_score
            )
            // 7
            - cognitive_cost_penalty // 5
            - planning_cost_penalty
        )
        cost_saturation = _clamp(
            max(0, len(cost_history_items) - MAX_COST_HISTORY) * 10
            + max(0, len(cost_scope_items) - MAX_COST_WINDOW) * 12
            + max(0, 70 - confidence_score)
            + max(
                0,
                55
                - min(
                    frontier_dependency_score,
                    retry_cost_score,
                    continuation_reuse_score,
                    orchestration_cost_score,
                    local_first_efficiency_score,
                ),
            )
        )
        cost_budget_exceeded = cost_budget_used > COST_BUDGET_LIMIT
        recursive_optimization_detected = recursive_provider_optimization_attempts > 0
        governance_violation = any(
            (
                autonomous_runtime_state_mutation_attempts,
                novel_cost_heuristic_synthesis_attempts,
                dynamic_routing_scope_widening_attempts,
                governance_policy_mutation_attempts,
                hidden_optimization_loop_attempts,
            )
        )
        cost_saturation_exceeded = cost_saturation >= COST_SATURATION_THRESHOLD
        termination_reasons = _termination_reasons(
            cost_budget_exceeded,
            recursive_optimization_detected,
            governance_violation,
            cost_saturation_exceeded,
        )
        final_confidence_score = _clamp(confidence_score - len(termination_reasons) * 8)

        return ProviderCostStabilizationFrame(
            provider_cost_stabilization_active=True,
            requirement_ids=PROVIDER_COST_STABILIZATION_REQUIREMENT_IDS,
            test_ids=PROVIDER_COST_STABILIZATION_TEST_IDS,
            frontier_escalation_suppression=FrontierEscalationSuppressionFrame(
                frontier_escalation_suppression_active=True,
                unnecessary_escalation_pressure=unnecessary_escalation_pressure,
                escalation_cooldown_instability=escalation_cooldown_instability,
                bounded_frontier_routing_pressure=bounded_frontier_routing_pressure,
                frontier_dependency_pressure=frontier_dependency_pressure,
                frontier_dependency_score=frontier_dependency_score,
                deterministic_frontier_cost_summary=(
                    f"escalation={unnecessary_escalation_pressure};dependency={frontier_dependency_pressure};"
                    f"score={frontier_dependency_score}"
                ),
                bounded_frontier_recommendation=(
                    "SUPPRESS_FRONTIER_ESCALATION"
                    if frontier_dependency_score < 60
                    else "FRONTIER_DEPENDENCY_BOUNDED"
                ),
            ),
            retry_cost_flattening=RetryCostFlatteningFrame(
                retry_cost_flattening_active=True,
                retry_cost_accumulation=retry_cost_accumulation,
                retry_saturation_cost=retry_saturation_cost,
                retry_cooldown_efficiency=retry_cooldown_efficiency,
                retry_recovery_reuse=retry_recovery_reuse,
                retry_cost_score=retry_cost_score,
                deterministic_retry_cost_summary=(
                    f"accumulation={retry_cost_accumulation};saturation={retry_saturation_cost};"
                    f"score={retry_cost_score}"
                ),
                bounded_retry_cost_recommendation=(
                    "FLATTEN_RETRY_COST_WINDOW" if retry_cost_score < 60 else "RETRY_COST_FLAT"
                ),
            ),
            continuation_reuse_optimization=ContinuationReuseOptimizationFrame(
                continuation_reuse_optimization_active=True,
                continuation_reuse_optimization=continuation_reuse_optimization,
                continuation_reset_suppression=continuation_reset_suppression,
                continuation_persistence_reuse=continuation_persistence_reuse,
                bounded_continuation_cost_drift=bounded_continuation_cost_drift,
                continuation_reuse_score=continuation_reuse_score,
                deterministic_continuation_reuse_summary=(
                    f"reuse={continuation_reuse_optimization};reset={continuation_reset_suppression};"
                    f"score={continuation_reuse_score}"
                ),
                bounded_continuation_reuse_recommendation=(
                    "OPTIMIZE_CONTINUATION_REUSE"
                    if continuation_reuse_score < 60
                    else "CONTINUATION_REUSE_STABLE"
                ),
            ),
            orchestration_cost_flattening=OrchestrationCostFlatteningFrame(
                orchestration_cost_flattening_active=True,
                orchestration_cost_flattening=orchestration_cost_flattening,
                orchestration_queue_efficiency=orchestration_queue_efficiency,
                orchestration_dependency_reuse=orchestration_dependency_reuse,
                orchestration_stabilization_reuse=orchestration_stabilization_reuse,
                orchestration_cost_score=orchestration_cost_score,
                deterministic_orchestration_cost_summary=(
                    f"flattening={orchestration_cost_flattening};queue={orchestration_queue_efficiency};"
                    f"score={orchestration_cost_score}"
                ),
                bounded_orchestration_cost_recommendation=(
                    "FLATTEN_ORCHESTRATION_COST"
                    if orchestration_cost_score < 60
                    else "ORCHESTRATION_COST_FLAT"
                ),
            ),
            local_first_persistence=LocalFirstPersistenceFrame(
                local_first_persistence_active=True,
                local_first_execution_persistence=local_first_execution_persistence,
                bounded_provider_rebalance_cost=bounded_provider_rebalance_cost,
                bounded_local_execution_reuse=bounded_local_execution_reuse,
                provider_specific_reuse=provider_specific_reuse,
                local_first_efficiency_score=local_first_efficiency_score,
                deterministic_local_first_summary=(
                    f"local={local_first_execution_persistence};reuse={bounded_local_execution_reuse};"
                    f"score={local_first_efficiency_score}"
                ),
                bounded_local_first_recommendation=(
                    "PERSIST_LOCAL_FIRST_EXECUTION"
                    if local_first_efficiency_score < 60
                    else "LOCAL_FIRST_EFFICIENT"
                ),
            ),
            provider_routing_efficiency=ProviderRoutingEfficiencyFrame(
                provider_routing_efficiency_active=True,
                provider_routing_efficiency=provider_routing_efficiency,
                provider_cost_pressure_score=(
                    100 if adaptive_provider.provider_cost_pressure == "HIGH" else 50
                ),
                provider_fatigue_cost_pressure=adaptive_provider.provider_fatigue_score,
                bounded_provider_routing_stabilization=provider_routing_efficiency_score >= 60,
                provider_routing_efficiency_score=provider_routing_efficiency_score,
                deterministic_provider_routing_summary=(
                    f"provider={adaptive_provider.provider_confidence_score};"
                    f"policy={runtime_policy.provider_policy_score};score={provider_routing_efficiency_score}"
                ),
                bounded_provider_routing_recommendation=(
                    "STABILIZE_PROVIDER_ROUTING_COST"
                    if provider_routing_efficiency_score < 60
                    else "PROVIDER_ROUTING_COST_STABLE"
                ),
            ),
            runtime_cost_pressure=RuntimeCostPressureFrame(
                runtime_cost_pressure_active=True,
                runtime_cost_drift=runtime_cost_drift,
                orchestration_overhead_pressure=orchestration_overhead_pressure,
                continuation_entropy_cost=max(0, 100 - soak_stability.continuation_entropy_score),
                soak_cost_pressure=max(0, 100 - soak_stability.long_session_stability_score),
                runtime_cost_pressure_score=runtime_cost_pressure_score,
                deterministic_runtime_cost_summary=(
                    f"drift={runtime_cost_drift};overhead={orchestration_overhead_pressure};"
                    f"score={runtime_cost_pressure_score}"
                ),
                bounded_runtime_cost_recommendation=(
                    "COMPACT_RUNTIME_COST_PRESSURE"
                    if runtime_cost_pressure_score < 75
                    else "RUNTIME_COST_PRESSURE_BOUNDED"
                ),
            ),
            cost_governance=CostGovernanceFrame(
                cost_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_cost_evaluation_enforced=True,
                bounded_cost_windows_enforced=True,
                autonomous_runtime_state_mutation_blocked=True,
                recursive_provider_optimization_blocked=True,
                novel_cost_heuristic_synthesis_blocked=True,
                dynamic_routing_scope_widening_blocked=True,
                governance_policy_mutation_blocked=True,
                hidden_optimization_loop_blocked=True,
            ),
            cost_budget=CostBudgetFrame(
                cost_budget_active=True,
                cost_budget_used=cost_budget_used,
                cost_budget_limit=COST_BUDGET_LIMIT,
                cost_budget_exceeded=cost_budget_exceeded,
                budget_pressure=_pressure(cost_budget_used, COST_BUDGET_LIMIT),
            ),
            cost_termination=CostTerminationFrame(
                cost_termination_active=True,
                provider_cost_stabilization_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                cost_budget_exceeded=cost_budget_exceeded,
                recursive_optimization_detected=recursive_optimization_detected,
                governance_violation_detected=governance_violation,
                cost_saturation_threshold_exceeded=cost_saturation_exceeded,
            ),
            cost_history=CostHistoryFrame(
                cost_history_active=True,
                cost_history=bounded_history,
                cost_scope=bounded_scope,
                cost_history_limit=MAX_COST_HISTORY,
                compact_cost_history_summary=f"history={len(bounded_history)};scope={len(bounded_scope)}",
                cost_history_overflow_blocked=bool(evicted_history),
                cost_scope_overflow_blocked=bool(evicted_scope),
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            cost_confidence=CostConfidenceFrame(
                cost_confidence_active=True,
                cost_confidence_score=final_confidence_score,
                confidence_status=_score_label(final_confidence_score),
                deterministic_confidence=True,
                cost_stabilization_confidence=final_confidence_score >= 70,
            ),
            cost_eviction=CostEvictionFrame(
                cost_eviction_active=True,
                evicted_cost_history_items=evicted_history,
                evicted_cost_scope_items=evicted_scope,
                eviction_count=len(evicted_history) + len(evicted_scope),
                bounded_eviction_active=bool(evicted_history or evicted_scope),
                eviction_summary=f"history={len(evicted_history)};scope={len(evicted_scope)}",
            ),
            frontier_dependency_score=frontier_dependency_score,
            retry_cost_score=retry_cost_score,
            continuation_reuse_score=continuation_reuse_score,
            orchestration_cost_score=orchestration_cost_score,
            local_first_efficiency_score=local_first_efficiency_score,
            provider_routing_efficiency_score=provider_routing_efficiency_score,
            runtime_cost_pressure_score=runtime_cost_pressure_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            provider_cost_stabilization_mode="LOCAL_PATCH_BOUNDED_PROVIDER_COST_STABILIZATION",
            estimated_avoided_frontier_escalation=79 + max(0, 80 - frontier_dependency_score) // 2,
            estimated_avoided_cost_drift=78 + max(0, 80 - runtime_cost_pressure_score) // 2,
            estimated_avoided_runtime_overhead=76 + final_confidence_score // 10,
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
    return "COST_RECOVERY_REQUIRED"


def _termination_reasons(
    cost_budget_exceeded: bool,
    recursive_optimization_detected: bool,
    governance_violation_detected: bool,
    cost_saturation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if cost_budget_exceeded:
        reasons.append("COST_BUDGET_EXCEEDED")
    if recursive_optimization_detected:
        reasons.append("RECURSIVE_PROVIDER_OPTIMIZATION_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if cost_saturation_threshold_exceeded:
        reasons.append("COST_SATURATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "COST_BUDGET_LIMIT",
    "COST_SATURATION_THRESHOLD",
    "MAX_COST_HISTORY",
    "MAX_COST_WINDOW",
    "PROVIDER_COST_STABILIZATION_REQUIREMENT_IDS",
    "PROVIDER_COST_STABILIZATION_TEST_IDS",
    "ContinuationReuseOptimizationFrame",
    "CostBudgetFrame",
    "CostConfidenceFrame",
    "CostEvictionFrame",
    "CostGovernanceFrame",
    "CostHistoryFrame",
    "CostTerminationFrame",
    "FrontierEscalationSuppressionFrame",
    "LocalFirstPersistenceFrame",
    "OrchestrationCostFlatteningFrame",
    "ProviderCostStabilizationFrame",
    "ProviderCostStabilizationRuntime",
    "ProviderRoutingEfficiencyFrame",
    "RetryCostFlatteningFrame",
    "RuntimeCostPressureFrame",
]
