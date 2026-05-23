from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.cognitive_state import CognitiveStateRuntime
from ai_dev_os.continuous_runtime_audit import ContinuousRuntimeAuditRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.failure_injection import FailureInjectionRuntime
from ai_dev_os.intentional_planning import IntentionalPlanningRuntime
from ai_dev_os.provider_cost_stabilization import ProviderCostStabilizationRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_hardening import RuntimeHardeningRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_orchestrator import RuntimeOrchestrator
from ai_dev_os.runtime_policy import RuntimePolicyEngine
from ai_dev_os.soak_stability import SoakStabilityRuntime
from ai_dev_os.sprint_loop import SprintLoopRuntime
from ai_dev_os.verified_execution import VerifiedExecutionRuntime

MAIN_MERGE_QUALIFICATION_REQUIREMENT_IDS = tuple(
    f"FR-MAINMERGEQUALIFICATION-{index:02d}" for index in range(1, 61)
) + (
    "NFR-COST-85",
    "NFR-ARCH-98",
    "NFR-SEC-69",
)
MAIN_MERGE_QUALIFICATION_TEST_IDS = tuple(
    f"TC-MAINMERGEQUALIFICATION-{index:02d}" for index in range(1, 61)
)

MAX_QUALIFICATION_WINDOW = 5
MAX_QUALIFICATION_HISTORY = 5
QUALIFICATION_BUDGET_LIMIT = 12
QUALIFICATION_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_QUALIFICATION_HISTORY = (
    "merge-readiness",
    "governance-completeness",
    "validation-completeness",
    "runtime-coherence",
    "operational-risk",
)
DEFAULT_QUALIFICATION_SCOPE = (
    "merge",
    "governance",
    "validation",
    "coherence",
    "risk",
)


@dataclass(frozen=True)
class MergeReadinessFrame:
    merge_readiness_active: bool
    validation_readiness: int
    orchestration_readiness: int
    runtime_stability_readiness: int
    bounded_merge_qualification: int
    merge_readiness_score: int
    deterministic_merge_readiness_summary: str
    bounded_merge_readiness_recommendation: str


@dataclass(frozen=True)
class GovernanceCompletenessFrame:
    governance_completeness_active: bool
    governance_completeness: int
    policy_coherence: int
    hardening_completeness: int
    bounded_governance_drift: int
    governance_completeness_score: int
    deterministic_governance_summary: str
    bounded_governance_recommendation: str


@dataclass(frozen=True)
class ValidationCompletenessFrame:
    validation_completeness_active: bool
    validation_completeness: int
    runtime_coverage_completeness: int
    soak_failure_validation_continuity: int
    bounded_validation_drift: int
    validation_completeness_score: int
    deterministic_validation_summary: str
    bounded_validation_recommendation: str


@dataclass(frozen=True)
class RuntimeCoherenceFrame:
    runtime_coherence_active: bool
    orchestration_coherence: int
    provider_policy_coherence: int
    continuation_retry_coherence: int
    runtime_ecosystem_bounded_coherence: int
    runtime_coherence_score: int
    deterministic_runtime_coherence_summary: str
    bounded_runtime_coherence_recommendation: str


@dataclass(frozen=True)
class OperationalRiskFrame:
    operational_risk_active: bool
    runtime_collapse_risk: int
    orchestration_drift_risk: int
    provider_degradation_risk: int
    frontier_escalation_risk: int
    operational_risk_score: int
    deterministic_operational_risk_summary: str
    bounded_operational_risk_recommendation: str


@dataclass(frozen=True)
class DriftQualificationFrame:
    drift_qualification_active: bool
    bounded_runtime_drift: int
    bounded_governance_drift: int
    bounded_validation_drift: int
    bounded_frontier_dependency_drift: int
    drift_qualification_score: int
    deterministic_drift_summary: str
    bounded_drift_recommendation: str


@dataclass(frozen=True)
class QualificationGovernanceFrame:
    qualification_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_qualification_enforced: bool
    bounded_qualification_windows_enforced: bool
    autonomous_merge_blocked: bool
    recursive_qualification_blocked: bool
    novel_governance_system_synthesis_blocked: bool
    dynamic_qualification_scope_widening_blocked: bool
    governance_policy_mutation_blocked: bool
    hidden_merge_orchestration_blocked: bool


@dataclass(frozen=True)
class QualificationBudgetFrame:
    qualification_budget_active: bool
    qualification_budget_used: int
    qualification_budget_limit: int
    qualification_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class QualificationTerminationFrame:
    qualification_termination_active: bool
    main_merge_qualification_terminated: bool
    termination_reasons: tuple[str, ...]
    qualification_budget_exceeded: bool
    recursive_qualification_detected: bool
    governance_violation_detected: bool
    qualification_saturation_threshold_exceeded: bool


@dataclass(frozen=True)
class QualificationHistoryFrame:
    qualification_history_active: bool
    qualification_history: tuple[str, ...]
    qualification_scope: tuple[str, ...]
    qualification_history_limit: int
    compact_qualification_history_summary: str
    qualification_history_overflow_blocked: bool
    qualification_scope_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class QualificationConfidenceFrame:
    qualification_confidence_active: bool
    qualification_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    merge_readiness_confidence: bool


@dataclass(frozen=True)
class QualificationEvictionFrame:
    qualification_eviction_active: bool
    evicted_qualification_history_items: tuple[str, ...]
    evicted_qualification_scope_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class MainMergeQualificationFrame:
    main_merge_qualification_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    merge_readiness: MergeReadinessFrame
    governance_completeness: GovernanceCompletenessFrame
    validation_completeness: ValidationCompletenessFrame
    runtime_coherence: RuntimeCoherenceFrame
    operational_risk: OperationalRiskFrame
    drift_qualification: DriftQualificationFrame
    qualification_governance: QualificationGovernanceFrame
    qualification_budget: QualificationBudgetFrame
    qualification_termination: QualificationTerminationFrame
    qualification_history: QualificationHistoryFrame
    qualification_confidence: QualificationConfidenceFrame
    qualification_eviction: QualificationEvictionFrame
    merge_readiness_score: int
    governance_completeness_score: int
    validation_completeness_score: int
    runtime_coherence_score: int
    operational_risk_score: int
    drift_qualification_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    main_merge_qualification_mode: str
    estimated_avoided_merge_regression: int
    estimated_avoided_runtime_instability: int
    estimated_avoided_frontier_dependency: int


class MainMergeQualificationRuntime:
    def evaluate(
        self,
        *,
        qualification_history_items: tuple[str, ...] = DEFAULT_QUALIFICATION_HISTORY,
        qualification_scope_items: tuple[str, ...] = DEFAULT_QUALIFICATION_SCOPE,
        validation_readiness: int = 4,
        orchestration_readiness: int = 4,
        runtime_stability_readiness: int = 4,
        bounded_merge_qualification: int = 4,
        governance_completeness: int = 4,
        policy_coherence: int = 4,
        hardening_completeness: int = 4,
        bounded_governance_drift: int = 0,
        validation_completeness: int = 4,
        runtime_coverage_completeness: int = 4,
        soak_failure_validation_continuity: int = 4,
        bounded_validation_drift: int = 0,
        orchestration_coherence: int = 4,
        provider_policy_coherence: int = 4,
        continuation_retry_coherence: int = 4,
        runtime_ecosystem_bounded_coherence: int = 4,
        runtime_collapse_risk: int = 0,
        orchestration_drift_risk: int = 0,
        provider_degradation_risk: int = 0,
        frontier_escalation_risk: int = 0,
        bounded_runtime_drift: int = 1,
        bounded_frontier_dependency_drift: int = 1,
        qualification_budget_used: int = 7,
        recursive_qualification_attempts: int = 0,
        autonomous_merge_attempts: int = 0,
        novel_governance_system_synthesis_attempts: int = 0,
        dynamic_qualification_scope_widening_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        hidden_merge_orchestration_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> MainMergeQualificationFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=max(1, 5 - continuation_retry_coherence),
            retry_cooldown_pressure=max(1, bounded_validation_drift + 1),
            continuation_saturation=max(18, 22 - continuation_retry_coherence),
            policy_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        orchestrator = RuntimeOrchestrator().evaluate(
            retry_amplification=max(1, 5 - continuation_retry_coherence),
            retry_interruption_windows=bounded_validation_drift,
            continuation_interruption_windows=bounded_runtime_drift,
            provider_fatigue_pressure=max(1, provider_degradation_risk),
            repeated_regressions=max(0, 4 - validation_readiness),
            regression_pressure=max(1, orchestration_drift_risk),
            orchestration_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        hardening = RuntimeHardeningRuntime().evaluate(
            retry_amplification_chains=max(1, 5 - continuation_retry_coherence),
            retry_cooldown_collapse=bounded_validation_drift,
            retry_saturation_windows=max(1, 5 - continuation_retry_coherence),
            retry_interruption_instability=bounded_runtime_drift,
            provider_readiness_starvation=max(0, provider_degradation_risk - 1),
            bounded_provider_queue_saturation=max(1, frontier_escalation_risk),
            provider_scheduling_instability=max(1, provider_degradation_risk),
            continuation_saturation=max(18, 22 - continuation_retry_coherence),
            continuation_interruption_instability=bounded_runtime_drift,
            continuation_reset_loops=bounded_validation_drift,
            bounded_continuation_starvation=bounded_runtime_drift,
            repeated_regressions=max(0, 4 - validation_completeness),
            regression_dependency_pressure=max(1, orchestration_drift_risk),
            orchestration_dependency_deadlocks=max(0, orchestration_drift_risk - 1),
            bounded_orchestration_stalls=max(0, 4 - orchestration_coherence),
            hardening_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        continuous_audit = ContinuousRuntimeAuditRuntime().evaluate(
            retry_amplification_pressure=max(1, 5 - continuation_retry_coherence),
            retry_saturation_windows=max(1, 5 - continuation_retry_coherence),
            retry_cooldown_collapse=bounded_validation_drift,
            retry_recovery_instability=bounded_runtime_drift,
            provider_readiness_degradation=max(0, provider_degradation_risk - 1),
            provider_queue_saturation=max(1, frontier_escalation_risk),
            provider_cooldown_instability=bounded_governance_drift,
            continuation_instability_pressure=max(1, bounded_runtime_drift),
            continuation_saturation=max(18, 22 - continuation_retry_coherence),
            continuation_interruption_instability=bounded_runtime_drift,
            continuation_reset_loops=bounded_validation_drift,
            bounded_continuation_drift=bounded_runtime_drift,
            orchestration_queue_pressure=max(1, orchestration_drift_risk),
            orchestration_dependency_stalls=max(0, orchestration_drift_risk - 1),
            orchestration_cooldown_pressure=max(1, bounded_governance_drift + 1),
            orchestration_regression_pressure=max(1, 5 - validation_completeness),
            bounded_orchestration_drift=bounded_runtime_drift,
            audit_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        failure_injection = FailureInjectionRuntime().evaluate(
            retry_amplification=max(1, 5 - continuation_retry_coherence),
            retry_saturation=max(1, 5 - continuation_retry_coherence),
            retry_cooldown_collapse=bounded_validation_drift,
            retry_interruption_instability=bounded_runtime_drift,
            provider_fatigue_escalation=max(1, provider_degradation_risk),
            provider_readiness_degradation=max(0, provider_degradation_risk - 1),
            provider_queue_saturation=max(1, frontier_escalation_risk),
            continuation_saturation=max(18, 22 - continuation_retry_coherence),
            continuation_reset_loops=bounded_validation_drift,
            continuation_drift=bounded_runtime_drift,
            dependency_deadlocks=max(0, orchestration_drift_risk - 1),
            orchestration_queue_stalls=max(0, 4 - orchestration_coherence),
            validation_retry_conflicts=max(0, 4 - validation_completeness),
            injection_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        soak_stability = SoakStabilityRuntime().evaluate(
            retry_accumulation=max(1, 5 - continuation_retry_coherence),
            retry_saturation_persistence=max(1, 5 - continuation_retry_coherence),
            retry_cooldown_degradation=bounded_validation_drift,
            retry_recovery_drift=bounded_runtime_drift,
            provider_fatigue_accumulation=max(1, provider_degradation_risk),
            provider_queue_drift=max(1, frontier_escalation_risk),
            continuation_entropy=max(1, bounded_runtime_drift),
            continuation_drift_accumulation=bounded_runtime_drift,
            continuation_reset_persistence=bounded_validation_drift,
            orchestration_queue_drift=max(1, orchestration_drift_risk),
            orchestration_dependency_accumulation=max(0, orchestration_drift_risk - 1),
            orchestration_cooldown_persistence=max(1, bounded_governance_drift + 1),
            orchestration_regression_accumulation=max(1, 5 - validation_completeness),
            runtime_interaction_entropy=bounded_runtime_drift,
            soak_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        provider_cost = ProviderCostStabilizationRuntime().evaluate(
            unnecessary_escalation_pressure=max(1, frontier_escalation_risk),
            escalation_cooldown_instability=bounded_governance_drift,
            bounded_frontier_routing_pressure=max(1, frontier_escalation_risk),
            frontier_dependency_pressure=max(1, bounded_frontier_dependency_drift),
            retry_cost_accumulation=max(1, 5 - continuation_retry_coherence),
            retry_saturation_cost=max(1, 5 - continuation_retry_coherence),
            retry_cooldown_efficiency=max(1, continuation_retry_coherence),
            retry_recovery_reuse=max(1, continuation_retry_coherence),
            continuation_reuse_optimization=max(1, continuation_retry_coherence),
            continuation_reset_suppression=max(1, 4 - bounded_validation_drift),
            continuation_persistence_reuse=max(1, runtime_ecosystem_bounded_coherence),
            bounded_continuation_cost_drift=bounded_runtime_drift,
            orchestration_cost_flattening=max(1, orchestration_coherence),
            orchestration_queue_efficiency=max(1, orchestration_coherence),
            orchestration_dependency_reuse=max(1, orchestration_coherence),
            orchestration_stabilization_reuse=max(1, hardening_completeness),
            local_first_execution_persistence=max(1, runtime_ecosystem_bounded_coherence),
            bounded_provider_rebalance_cost=max(1, provider_degradation_risk),
            bounded_local_execution_reuse=max(1, runtime_ecosystem_bounded_coherence),
            provider_specific_reuse=max(1, provider_policy_coherence),
            provider_routing_efficiency=max(1, provider_policy_coherence),
            runtime_cost_drift=bounded_runtime_drift,
            orchestration_overhead_pressure=orchestration_drift_risk,
            cost_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=max(1, bounded_runtime_drift),
            retry_amplification=max(1, 5 - continuation_retry_coherence),
            orchestration_instability=max(1, orchestration_drift_risk),
            continuation_decay=bounded_runtime_drift,
            estimated_token_pressure=20 + frontier_escalation_risk * 8,
            bounded_reasoning_cost=12 + frontier_escalation_risk * 4,
            bounded_execution_cost=10 + provider_degradation_risk * 3,
            bounded_escalation_pressure=max(1, frontier_escalation_risk),
            provider_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
            escalation_depth=max(1, frontier_escalation_risk),
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=max(1, 5 - continuation_retry_coherence),
            retry_cooldown_reuse=max(1, continuation_retry_coherence),
            retry_saturation_motifs=max(1, 5 - continuation_retry_coherence),
            retry_interruption_patterns=bounded_runtime_drift,
            continuation_reuse_depth=max(1, continuation_retry_coherence),
            execution_memory_budget_used=min(
                qualification_budget_used, QUALIFICATION_BUDGET_LIMIT
            ),
        )
        mediation = ExecutionSequencer().mediate(
            retry_count=max(1, 5 - continuation_retry_coherence)
        )
        sprint_loop = SprintLoopRuntime().evaluate(
            repeated_regressions=max(0, 4 - validation_completeness),
            retry_amplification=max(1, 5 - continuation_retry_coherence),
            retry_count=max(1, 5 - continuation_retry_coherence),
            continuation_depth=max(1, continuation_retry_coherence),
            continuation_interruption_window=bounded_runtime_drift,
            sprint_budget_used=min(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=max(0, 4 - validation_completeness),
            retry_amplification_pressure=max(1, 5 - continuation_retry_coherence),
        )
        cognitive_state = CognitiveStateRuntime().evaluate(
            objective="main-merge-qualification-local-patch",
            session_age_pressure=18 + bounded_runtime_drift,
            recursive_reasoning_attempts=recursive_qualification_attempts,
        )
        planning = IntentionalPlanningRuntime().evaluate(
            interruption_duration=bounded_runtime_drift,
            abandoned_continuation_chains=bounded_validation_drift,
            recursive_planning_attempts=recursive_qualification_attempts,
        )
        verified_execution = VerifiedExecutionRuntime().evaluate()

        bounded_history = qualification_history_items[:MAX_QUALIFICATION_HISTORY]
        bounded_scope = qualification_scope_items[:MAX_QUALIFICATION_WINDOW]
        evicted_history = qualification_history_items[MAX_QUALIFICATION_HISTORY:]
        evicted_scope = qualification_scope_items[MAX_QUALIFICATION_WINDOW:]

        merge_pressure = _clamp(
            max(0, 4 - validation_readiness) * 14
            + max(0, 4 - orchestration_readiness) * 12
            + max(0, 4 - runtime_stability_readiness) * 12
            + max(0, 4 - bounded_merge_qualification) * 10
            + max(0, 85 - sprint_loop.sprint_validation_score) // 3
        )
        merge_readiness_score = _clamp(100 - merge_pressure)
        governance_pressure = _clamp(
            max(0, 4 - governance_completeness) * 14
            + max(0, 4 - policy_coherence) * 12
            + max(0, 4 - hardening_completeness) * 12
            + bounded_governance_drift * 14
            + max(0, 85 - runtime_policy.policy_coherence.policy_coherence_score) // 3
        )
        governance_completeness_score = _clamp(100 - governance_pressure)
        validation_pressure = _clamp(
            max(0, 4 - validation_completeness) * 14
            + max(0, 4 - runtime_coverage_completeness) * 12
            + max(0, 4 - soak_failure_validation_continuity) * 12
            + bounded_validation_drift * 14
            + max(0, 85 - verified_execution.confidence.confidence_score) // 3
        )
        validation_completeness_score = _clamp(100 - validation_pressure)
        coherence_pressure = _clamp(
            max(0, 4 - orchestration_coherence) * 14
            + max(0, 4 - provider_policy_coherence) * 12
            + max(0, 4 - continuation_retry_coherence) * 12
            + max(0, 4 - runtime_ecosystem_bounded_coherence) * 10
            + max(0, 80 - execution_memory.execution_reuse_score) // 3
        )
        runtime_coherence_score = _clamp(100 - coherence_pressure)
        operational_risk_score = _clamp(
            100
            - (
                runtime_collapse_risk * 18
                + orchestration_drift_risk * 14
                + provider_degradation_risk * 12
                + frontier_escalation_risk * 12
                + max(0, 80 - failure_injection.recovery_resilience_score) // 2
                + max(0, 80 - provider_cost.frontier_dependency_score) // 2
            )
        )
        drift_qualification_score = _clamp(
            100
            - (
                bounded_runtime_drift * 14
                + bounded_governance_drift * 14
                + bounded_validation_drift * 14
                + bounded_frontier_dependency_drift * 12
                + max(0, 80 - soak_stability.long_session_stability_score) // 3
            )
        )
        qualification_confidence_score = _clamp(
            (
                merge_readiness_score
                + governance_completeness_score
                + validation_completeness_score
                + runtime_coherence_score
                + operational_risk_score
                + drift_qualification_score
                + continuous_audit.runtime_health_score
                + hardening.hardening_confidence.hardening_confidence_score
                + orchestrator.orchestration_confidence.orchestration_confidence_score
                + adaptive_provider.provider_confidence_score
                + reflection.execution_quality.execution_quality_score
                + provider_cost.runtime_cost_pressure_score
            )
            // 12
            + int(mediation.runtime_mediation_active) * 2
        )
        cognitive_penalty = max(0, 60 - cognitive_state.decay.decay_score)
        planning_penalty = 0 if planning.planning_decay_status == "STABLE" else 8
        qualification_confidence_score = _clamp(
            qualification_confidence_score - cognitive_penalty // 5 - planning_penalty
        )
        qualification_saturation = _clamp(
            max(0, len(qualification_history_items) - MAX_QUALIFICATION_HISTORY) * 10
            + max(0, len(qualification_scope_items) - MAX_QUALIFICATION_WINDOW) * 12
            + max(0, 70 - qualification_confidence_score)
            + max(
                0,
                55
                - min(
                    merge_readiness_score,
                    governance_completeness_score,
                    validation_completeness_score,
                    runtime_coherence_score,
                    operational_risk_score,
                ),
            )
        )
        qualification_budget_exceeded = qualification_budget_used > QUALIFICATION_BUDGET_LIMIT
        recursive_qualification_detected = recursive_qualification_attempts > 0
        governance_violation = any(
            (
                autonomous_merge_attempts,
                novel_governance_system_synthesis_attempts,
                dynamic_qualification_scope_widening_attempts,
                governance_policy_mutation_attempts,
                hidden_merge_orchestration_attempts,
            )
        )
        qualification_saturation_exceeded = (
            qualification_saturation >= QUALIFICATION_SATURATION_THRESHOLD
        )
        termination_reasons = _termination_reasons(
            qualification_budget_exceeded,
            recursive_qualification_detected,
            governance_violation,
            qualification_saturation_exceeded,
        )
        final_confidence_score = _clamp(
            qualification_confidence_score - len(termination_reasons) * 8
        )

        return MainMergeQualificationFrame(
            main_merge_qualification_active=True,
            requirement_ids=MAIN_MERGE_QUALIFICATION_REQUIREMENT_IDS,
            test_ids=MAIN_MERGE_QUALIFICATION_TEST_IDS,
            merge_readiness=MergeReadinessFrame(
                merge_readiness_active=True,
                validation_readiness=validation_readiness,
                orchestration_readiness=orchestration_readiness,
                runtime_stability_readiness=runtime_stability_readiness,
                bounded_merge_qualification=bounded_merge_qualification,
                merge_readiness_score=merge_readiness_score,
                deterministic_merge_readiness_summary=(
                    f"validation={validation_readiness};orchestration={orchestration_readiness};"
                    f"score={merge_readiness_score}"
                ),
                bounded_merge_readiness_recommendation=(
                    "DEFER_MAIN_MERGE_FOR_READINESS"
                    if merge_readiness_score < 60
                    else "MAIN_MERGE_READINESS_BOUNDED"
                ),
            ),
            governance_completeness=GovernanceCompletenessFrame(
                governance_completeness_active=True,
                governance_completeness=governance_completeness,
                policy_coherence=policy_coherence,
                hardening_completeness=hardening_completeness,
                bounded_governance_drift=bounded_governance_drift,
                governance_completeness_score=governance_completeness_score,
                deterministic_governance_summary=(
                    f"governance={governance_completeness};policy={policy_coherence};"
                    f"score={governance_completeness_score}"
                ),
                bounded_governance_recommendation=(
                    "COMPLETE_GOVERNANCE_BEFORE_MERGE"
                    if governance_completeness_score < 60
                    else "GOVERNANCE_COMPLETE_FOR_MERGE"
                ),
            ),
            validation_completeness=ValidationCompletenessFrame(
                validation_completeness_active=True,
                validation_completeness=validation_completeness,
                runtime_coverage_completeness=runtime_coverage_completeness,
                soak_failure_validation_continuity=soak_failure_validation_continuity,
                bounded_validation_drift=bounded_validation_drift,
                validation_completeness_score=validation_completeness_score,
                deterministic_validation_summary=(
                    f"validation={validation_completeness};coverage={runtime_coverage_completeness};"
                    f"score={validation_completeness_score}"
                ),
                bounded_validation_recommendation=(
                    "COMPLETE_VALIDATION_BEFORE_MERGE"
                    if validation_completeness_score < 60
                    else "VALIDATION_COMPLETE_FOR_MERGE"
                ),
            ),
            runtime_coherence=RuntimeCoherenceFrame(
                runtime_coherence_active=True,
                orchestration_coherence=orchestration_coherence,
                provider_policy_coherence=provider_policy_coherence,
                continuation_retry_coherence=continuation_retry_coherence,
                runtime_ecosystem_bounded_coherence=runtime_ecosystem_bounded_coherence,
                runtime_coherence_score=runtime_coherence_score,
                deterministic_runtime_coherence_summary=(
                    f"orchestration={orchestration_coherence};provider_policy={provider_policy_coherence};"
                    f"score={runtime_coherence_score}"
                ),
                bounded_runtime_coherence_recommendation=(
                    "RESTORE_RUNTIME_COHERENCE_BEFORE_MERGE"
                    if runtime_coherence_score < 60
                    else "RUNTIME_COHERENCE_BOUNDED"
                ),
            ),
            operational_risk=OperationalRiskFrame(
                operational_risk_active=True,
                runtime_collapse_risk=runtime_collapse_risk,
                orchestration_drift_risk=orchestration_drift_risk,
                provider_degradation_risk=provider_degradation_risk,
                frontier_escalation_risk=frontier_escalation_risk,
                operational_risk_score=operational_risk_score,
                deterministic_operational_risk_summary=(
                    f"collapse={runtime_collapse_risk};orchestration={orchestration_drift_risk};"
                    f"score={operational_risk_score}"
                ),
                bounded_operational_risk_recommendation=(
                    "BOUND_OPERATIONAL_RISK_BEFORE_MERGE"
                    if operational_risk_score < 60
                    else "OPERATIONAL_RISK_BOUNDED"
                ),
            ),
            drift_qualification=DriftQualificationFrame(
                drift_qualification_active=True,
                bounded_runtime_drift=bounded_runtime_drift,
                bounded_governance_drift=bounded_governance_drift,
                bounded_validation_drift=bounded_validation_drift,
                bounded_frontier_dependency_drift=bounded_frontier_dependency_drift,
                drift_qualification_score=drift_qualification_score,
                deterministic_drift_summary=(
                    f"runtime={bounded_runtime_drift};governance={bounded_governance_drift};"
                    f"score={drift_qualification_score}"
                ),
                bounded_drift_recommendation=(
                    "QUALIFY_DRIFT_BEFORE_MERGE"
                    if drift_qualification_score < 60
                    else "DRIFT_QUALIFICATION_BOUNDED"
                ),
            ),
            qualification_governance=QualificationGovernanceFrame(
                qualification_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_qualification_enforced=True,
                bounded_qualification_windows_enforced=True,
                autonomous_merge_blocked=True,
                recursive_qualification_blocked=True,
                novel_governance_system_synthesis_blocked=True,
                dynamic_qualification_scope_widening_blocked=True,
                governance_policy_mutation_blocked=True,
                hidden_merge_orchestration_blocked=True,
            ),
            qualification_budget=QualificationBudgetFrame(
                qualification_budget_active=True,
                qualification_budget_used=qualification_budget_used,
                qualification_budget_limit=QUALIFICATION_BUDGET_LIMIT,
                qualification_budget_exceeded=qualification_budget_exceeded,
                budget_pressure=_pressure(qualification_budget_used, QUALIFICATION_BUDGET_LIMIT),
            ),
            qualification_termination=QualificationTerminationFrame(
                qualification_termination_active=True,
                main_merge_qualification_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                qualification_budget_exceeded=qualification_budget_exceeded,
                recursive_qualification_detected=recursive_qualification_detected,
                governance_violation_detected=governance_violation,
                qualification_saturation_threshold_exceeded=qualification_saturation_exceeded,
            ),
            qualification_history=QualificationHistoryFrame(
                qualification_history_active=True,
                qualification_history=bounded_history,
                qualification_scope=bounded_scope,
                qualification_history_limit=MAX_QUALIFICATION_HISTORY,
                compact_qualification_history_summary=f"history={len(bounded_history)};scope={len(bounded_scope)}",
                qualification_history_overflow_blocked=bool(evicted_history),
                qualification_scope_overflow_blocked=bool(evicted_scope),
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            qualification_confidence=QualificationConfidenceFrame(
                qualification_confidence_active=True,
                qualification_confidence_score=final_confidence_score,
                confidence_status=_score_label(final_confidence_score),
                deterministic_confidence=True,
                merge_readiness_confidence=final_confidence_score >= 70,
            ),
            qualification_eviction=QualificationEvictionFrame(
                qualification_eviction_active=True,
                evicted_qualification_history_items=evicted_history,
                evicted_qualification_scope_items=evicted_scope,
                eviction_count=len(evicted_history) + len(evicted_scope),
                bounded_eviction_active=bool(evicted_history or evicted_scope),
                eviction_summary=f"history={len(evicted_history)};scope={len(evicted_scope)}",
            ),
            merge_readiness_score=merge_readiness_score,
            governance_completeness_score=governance_completeness_score,
            validation_completeness_score=validation_completeness_score,
            runtime_coherence_score=runtime_coherence_score,
            operational_risk_score=operational_risk_score,
            drift_qualification_score=drift_qualification_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            main_merge_qualification_mode="LOCAL_PATCH_BOUNDED_MAIN_MERGE_QUALIFICATION",
            estimated_avoided_merge_regression=79 + max(0, 80 - merge_readiness_score) // 2,
            estimated_avoided_runtime_instability=78 + max(0, 80 - runtime_coherence_score) // 2,
            estimated_avoided_frontier_dependency=77
            + max(0, 80 - provider_cost.frontier_dependency_score) // 2,
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
    return "QUALIFICATION_RECOVERY_REQUIRED"


def _termination_reasons(
    qualification_budget_exceeded: bool,
    recursive_qualification_detected: bool,
    governance_violation_detected: bool,
    qualification_saturation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if qualification_budget_exceeded:
        reasons.append("QUALIFICATION_BUDGET_EXCEEDED")
    if recursive_qualification_detected:
        reasons.append("RECURSIVE_QUALIFICATION_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if qualification_saturation_threshold_exceeded:
        reasons.append("QUALIFICATION_SATURATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "MAIN_MERGE_QUALIFICATION_REQUIREMENT_IDS",
    "MAIN_MERGE_QUALIFICATION_TEST_IDS",
    "MAX_QUALIFICATION_HISTORY",
    "MAX_QUALIFICATION_WINDOW",
    "QUALIFICATION_BUDGET_LIMIT",
    "QUALIFICATION_SATURATION_THRESHOLD",
    "DriftQualificationFrame",
    "GovernanceCompletenessFrame",
    "MainMergeQualificationFrame",
    "MainMergeQualificationRuntime",
    "MergeReadinessFrame",
    "OperationalRiskFrame",
    "QualificationBudgetFrame",
    "QualificationConfidenceFrame",
    "QualificationEvictionFrame",
    "QualificationGovernanceFrame",
    "QualificationHistoryFrame",
    "QualificationTerminationFrame",
    "RuntimeCoherenceFrame",
    "ValidationCompletenessFrame",
]
