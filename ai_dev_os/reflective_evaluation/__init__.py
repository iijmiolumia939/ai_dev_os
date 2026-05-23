from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.cognitive_state import CognitiveStateRuntime
from ai_dev_os.execution_continuation import ExecutionContinuationRuntime
from ai_dev_os.execution_coordination import ExecutionCoordinationRuntime
from ai_dev_os.execution_recovery import ExecutionRecoveryRuntime
from ai_dev_os.intentional_planning import IntentionalPlanningRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.verified_execution import VerifiedExecutionRuntime

REFLECTIVE_EVALUATION_REQUIREMENT_IDS = tuple(
    f"FR-REFLECTIVEEVALUATION-{index:02d}" for index in range(1, 47)
) + ("NFR-COST-63", "NFR-ARCH-76", "NFR-SEC-47")
REFLECTIVE_EVALUATION_TEST_IDS = tuple(
    f"TC-REFLECTIVEEVALUATION-{index:02d}" for index in range(1, 47)
)

MAX_REFLECTIVE_WINDOW_ITEMS = 5
MAX_REFLECTIVE_HISTORY = 5
REFLECTIVE_BUDGET_LIMIT = 12
REFLECTIVE_SATURATION_THRESHOLD = 84
CONTINUATION_INVALIDATION_THRESHOLD = 45
MAX_SCORE = 100
MIN_SCORE = 0


@dataclass(frozen=True)
class ExecutionQualityFrame:
    execution_quality_active: bool
    execution_quality_score: int
    execution_consistency: str
    verified_execution_continuity: bool
    execution_failure_frequency: int
    retry_amplification_pressure: int
    runtime_mediation_stability: str
    deterministic_execution_quality_summary: str
    bounded_reset_recommendation: str


@dataclass(frozen=True)
class CognitiveCoherenceFrame:
    cognitive_coherence_active: bool
    cognitive_coherence_score: int
    working_memory_coherence: str
    task_attention_consistency: str
    cognitive_decay_pressure: str
    context_salience_stability: str
    execution_focus_consistency: bool
    deterministic_cognitive_coherence_summary: str
    bounded_cognitive_reset_recommendation: str


@dataclass(frozen=True)
class ContinuationValidityFrame:
    continuation_validity_active: bool
    continuation_validity_score: int
    stale_continuation_chains: int
    invalid_continuation_depth: int
    abandoned_recovery_chains: int
    continuation_interruption_pressure: int
    continuation_runtime_active: bool
    deterministic_continuation_validity_summary: str
    bounded_continuation_reset_recommendation: str


@dataclass(frozen=True)
class PlanningIntegrityFrame:
    planning_integrity_active: bool
    planning_integrity_score: int
    bounded_goal_hierarchy_integrity: bool
    planning_continuation_consistency: str
    interruption_stability: str
    planning_decay_pressure: str
    deterministic_planning_integrity_summary: str
    bounded_planning_reset_recommendation: str


@dataclass(frozen=True)
class RuntimeIntegrityFrame:
    runtime_integrity_active: bool
    runtime_integrity_score: int
    verified_execution_active: bool
    runtime_mediation_active: bool
    cognitive_state_active: bool
    intentional_planning_active: bool
    local_patch_integrity: bool
    deterministic_runtime_integrity_summary: str


@dataclass(frozen=True)
class RecoveryEffectivenessFrame:
    recovery_effectiveness_active: bool
    recovery_effectiveness_score: int
    execution_recovery_active: bool
    rollback_safe_recovery: bool
    abandoned_recovery_chains: int
    deterministic_recovery_effectiveness_summary: str


@dataclass(frozen=True)
class CoordinationStabilityFrame:
    coordination_stability_active: bool
    coordination_stability_score: int
    execution_coordination_active: bool
    runtime_conflict_pressure: int
    coordination_stable: bool
    deterministic_coordination_stability_summary: str


@dataclass(frozen=True)
class ReflectiveBudgetFrame:
    reflective_budget_active: bool
    reflective_budget_used: int
    reflective_budget_limit: int
    budget_pressure: str
    budget_exceeded: bool
    local_first_budget: bool
    high_tier_evaluation_blocked: bool


@dataclass(frozen=True)
class ReflectiveWindowFrame:
    reflective_window_active: bool
    reflective_window_items: tuple[str, ...]
    reflective_window_limit: int
    reflective_window_pressure: str
    reflective_saturation_score: int
    reflective_saturation_threshold: int
    bounded_reflective_window: bool
    evicted_window_items: tuple[str, ...]


@dataclass(frozen=True)
class ReflectiveGovernanceFrame:
    reflective_governance_active: bool
    local_patch_scope_enforced: bool
    bounded_reflective_windows_enforced: bool
    deterministic_evaluation_enforced: bool
    bounded_scoring_ranges_enforced: bool
    bounded_reflective_history_enforced: bool
    autonomous_self_improvement_blocked: bool
    recursive_optimization_blocked: bool
    hidden_reflective_execution_blocked: bool
    self_expanding_evaluation_chains_blocked: bool
    governance_policy_mutation_blocked: bool
    objective_synthesis_blocked: bool
    retrieval_scope_widening_blocked: bool


@dataclass(frozen=True)
class ReflectiveTerminationFrame:
    reflective_terminated: bool
    termination_reasons: tuple[str, ...]
    budget_exceeded: bool
    recursive_evaluation_detected: bool
    governance_violation_detected: bool
    saturation_threshold_exceeded: bool
    continuation_invalidation_threshold_exceeded: bool


@dataclass(frozen=True)
class ReflectiveConfidenceFrame:
    reflective_confidence_active: bool
    confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    frontier_evaluation_dependency_reduced: bool


@dataclass(frozen=True)
class ReflectiveHistoryFrame:
    reflective_history_active: bool
    reflective_history: tuple[str, ...]
    history_limit: int
    compact_history_summary: str
    raw_transcript_replay_blocked: bool
    recursive_history_expansion_blocked: bool


@dataclass(frozen=True)
class ReflectiveEvictionFrame:
    reflective_eviction_active: bool
    evicted_history_items: tuple[str, ...]
    evicted_window_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class ReflectiveEvaluationFrame:
    reflective_evaluation_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    execution_quality: ExecutionQualityFrame
    cognitive_coherence: CognitiveCoherenceFrame
    continuation_validity: ContinuationValidityFrame
    planning_integrity: PlanningIntegrityFrame
    runtime_integrity: RuntimeIntegrityFrame
    recovery_effectiveness: RecoveryEffectivenessFrame
    coordination_stability: CoordinationStabilityFrame
    reflective_budget: ReflectiveBudgetFrame
    reflective_window: ReflectiveWindowFrame
    reflective_governance: ReflectiveGovernanceFrame
    reflective_termination: ReflectiveTerminationFrame
    reflective_confidence: ReflectiveConfidenceFrame
    reflective_history: ReflectiveHistoryFrame
    reflective_eviction: ReflectiveEvictionFrame
    execution_quality_score: int
    cognitive_coherence_score: int
    continuation_validity_score: int
    planning_integrity_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    provider_routing: str
    estimated_avoided_recursive_reflection: int
    estimated_avoided_self_optimization: int
    estimated_avoided_frontier_evaluation: int


class ReflectiveEvaluationRuntime:
    def evaluate(
        self,
        *,
        execution_failure_frequency: int = 0,
        retry_amplification_pressure: int = 1,
        stale_continuation_chains: int = 0,
        invalid_continuation_depth: int = 0,
        abandoned_recovery_chains: int = 0,
        continuation_interruption_pressure: int = 0,
        planning_decay_pressure: int = 0,
        runtime_conflict_pressure: int = 0,
        reflective_budget_used: int = 7,
        reflective_window_items: tuple[str, ...] = (
            "execution_quality",
            "cognitive_coherence",
            "continuation_validity",
            "planning_integrity",
            "runtime_integrity",
        ),
        reflective_history_items: tuple[str, ...] = (
            "verified_execution",
            "runtime_mediation",
            "cognitive_state",
            "intentional_planning",
        ),
        recursive_evaluation_attempts: int = 0,
        autonomous_self_improvement_attempts: int = 0,
        recursive_optimization_attempts: int = 0,
        hidden_reflective_execution_attempts: int = 0,
        self_expanding_evaluation_attempts: int = 0,
        governance_mutation_attempts: int = 0,
        objective_synthesis_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
        raw_transcript_replay_attempts: int = 0,
    ) -> ReflectiveEvaluationFrame:
        verified = VerifiedExecutionRuntime().evaluate()
        mediation = ExecutionSequencer().mediate()
        cognitive = CognitiveStateRuntime().evaluate()
        planning = IntentionalPlanningRuntime().evaluate()
        continuation = ExecutionContinuationRuntime().evaluate()
        recovery = ExecutionRecoveryRuntime().evaluate()
        coordination = ExecutionCoordinationRuntime().evaluate()

        bounded_window = reflective_window_items[:MAX_REFLECTIVE_WINDOW_ITEMS]
        evicted_window_items = reflective_window_items[MAX_REFLECTIVE_WINDOW_ITEMS:]
        bounded_history = reflective_history_items[:MAX_REFLECTIVE_HISTORY]
        evicted_history_items = reflective_history_items[MAX_REFLECTIVE_HISTORY:]
        window_pressure = _pressure(len(reflective_window_items), MAX_REFLECTIVE_WINDOW_ITEMS)
        saturation_score = _clamp(
            len(reflective_window_items) * 11
            + recursive_evaluation_attempts * 35
            + autonomous_self_improvement_attempts * 22
            + self_expanding_evaluation_attempts * 18
        )
        execution_quality_score = _clamp(
            95
            - execution_failure_frequency * 18
            - retry_amplification_pressure * 5
            - int(not verified.verification.pytest_verified) * 25
            - int(not mediation.runtime_mediation_active) * 30
        )
        cognitive_coherence_score = _clamp(
            94
            - _status_penalty(cognitive.decay_status)
            - _pressure_penalty(cognitive.memory_pressure)
            - int(not cognitive.execution_focus.execution_focus_active) * 20
        )
        continuation_validity_score = _clamp(
            92
            - stale_continuation_chains * 16
            - invalid_continuation_depth * 18
            - abandoned_recovery_chains * 12
            - continuation_interruption_pressure * 5
            - int(not continuation.execution_continuation_active) * 25
        )
        planning_integrity_score = _clamp(
            93
            - planning_decay_pressure * 12
            - _status_penalty(planning.planning_decay_status)
            - _pressure_penalty(planning.planning_interruption_pressure)
            - int(not planning.goal_hierarchy.bounded_goal_hierarchy) * 30
        )
        recovery_effectiveness_score = _clamp(
            90
            - abandoned_recovery_chains * 14
            - int(not recovery.execution_recovery_active) * 30
            - int(not recovery.rollback_safe) * 25
        )
        coordination_stability_score = _clamp(
            91
            - runtime_conflict_pressure * 12
            - int(not coordination.execution_coordination_active) * 30
        )
        runtime_integrity_score = min(
            execution_quality_score,
            cognitive_coherence_score,
            continuation_validity_score,
            planning_integrity_score,
            recovery_effectiveness_score,
            coordination_stability_score,
        )
        governance_violation = any(
            (
                autonomous_self_improvement_attempts,
                recursive_optimization_attempts,
                hidden_reflective_execution_attempts,
                self_expanding_evaluation_attempts,
                governance_mutation_attempts,
                objective_synthesis_attempts,
                retrieval_scope_widening_attempts,
            )
        )
        termination_reasons = _termination_reasons(
            reflective_budget_used > REFLECTIVE_BUDGET_LIMIT,
            recursive_evaluation_attempts > 0,
            governance_violation,
            saturation_score >= REFLECTIVE_SATURATION_THRESHOLD,
            continuation_validity_score <= CONTINUATION_INVALIDATION_THRESHOLD,
        )
        confidence_score = _clamp(
            min(
                execution_quality_score,
                cognitive_coherence_score,
                continuation_validity_score,
                planning_integrity_score,
            )
            - len(termination_reasons) * 12
        )

        return ReflectiveEvaluationFrame(
            reflective_evaluation_active=True,
            requirement_ids=REFLECTIVE_EVALUATION_REQUIREMENT_IDS,
            test_ids=REFLECTIVE_EVALUATION_TEST_IDS,
            execution_quality=ExecutionQualityFrame(
                execution_quality_active=True,
                execution_quality_score=execution_quality_score,
                execution_consistency=_score_label(execution_quality_score),
                verified_execution_continuity=verified.envelope_active,
                execution_failure_frequency=execution_failure_frequency,
                retry_amplification_pressure=retry_amplification_pressure,
                runtime_mediation_stability=_score_label(execution_quality_score),
                deterministic_execution_quality_summary=(
                    f"failures={execution_failure_frequency};retry={retry_amplification_pressure}"
                ),
                bounded_reset_recommendation=_reset_recommendation(execution_quality_score),
            ),
            cognitive_coherence=CognitiveCoherenceFrame(
                cognitive_coherence_active=True,
                cognitive_coherence_score=cognitive_coherence_score,
                working_memory_coherence=_score_label(cognitive_coherence_score),
                task_attention_consistency=cognitive.active_focus,
                cognitive_decay_pressure=cognitive.decay_status,
                context_salience_stability=_score_label(cognitive_coherence_score),
                execution_focus_consistency=cognitive.execution_focus.execution_focus_active,
                deterministic_cognitive_coherence_summary=(
                    f"memory={cognitive.memory_pressure};decay={cognitive.decay_status}"
                ),
                bounded_cognitive_reset_recommendation=(
                    _reset_recommendation(cognitive_coherence_score)
                ),
            ),
            continuation_validity=ContinuationValidityFrame(
                continuation_validity_active=True,
                continuation_validity_score=continuation_validity_score,
                stale_continuation_chains=stale_continuation_chains,
                invalid_continuation_depth=invalid_continuation_depth,
                abandoned_recovery_chains=abandoned_recovery_chains,
                continuation_interruption_pressure=continuation_interruption_pressure,
                continuation_runtime_active=continuation.execution_continuation_active,
                deterministic_continuation_validity_summary=(
                    f"stale={stale_continuation_chains};invalid_depth={invalid_continuation_depth}"
                ),
                bounded_continuation_reset_recommendation=(
                    _reset_recommendation(continuation_validity_score)
                ),
            ),
            planning_integrity=PlanningIntegrityFrame(
                planning_integrity_active=True,
                planning_integrity_score=planning_integrity_score,
                bounded_goal_hierarchy_integrity=(planning.goal_hierarchy.bounded_goal_hierarchy),
                planning_continuation_consistency=(
                    planning.planning_continuation.continuation_pressure
                ),
                interruption_stability=planning.planning_interruption_pressure,
                planning_decay_pressure=planning.planning_decay_status,
                deterministic_planning_integrity_summary=(
                    f"goals={planning.active_goal_count};decay={planning.planning_decay_status}"
                ),
                bounded_planning_reset_recommendation=(
                    _reset_recommendation(planning_integrity_score)
                ),
            ),
            runtime_integrity=RuntimeIntegrityFrame(
                runtime_integrity_active=True,
                runtime_integrity_score=runtime_integrity_score,
                verified_execution_active=verified.envelope_active,
                runtime_mediation_active=mediation.runtime_mediation_active,
                cognitive_state_active=cognitive.cognitive_state_active,
                intentional_planning_active=planning.intentional_planning_active,
                local_patch_integrity=True,
                deterministic_runtime_integrity_summary=(
                    "verified+mediation+cognitive+planning observed only"
                ),
            ),
            recovery_effectiveness=RecoveryEffectivenessFrame(
                recovery_effectiveness_active=True,
                recovery_effectiveness_score=recovery_effectiveness_score,
                execution_recovery_active=recovery.execution_recovery_active,
                rollback_safe_recovery=recovery.rollback_safe,
                abandoned_recovery_chains=abandoned_recovery_chains,
                deterministic_recovery_effectiveness_summary=(
                    f"recovery={recovery.execution_recovery_active};abandoned={abandoned_recovery_chains}"
                ),
            ),
            coordination_stability=CoordinationStabilityFrame(
                coordination_stability_active=True,
                coordination_stability_score=coordination_stability_score,
                execution_coordination_active=coordination.execution_coordination_active,
                runtime_conflict_pressure=runtime_conflict_pressure,
                coordination_stable=coordination_stability_score >= 70,
                deterministic_coordination_stability_summary=(
                    f"conflict_pressure={runtime_conflict_pressure}"
                ),
            ),
            reflective_budget=ReflectiveBudgetFrame(
                reflective_budget_active=True,
                reflective_budget_used=reflective_budget_used,
                reflective_budget_limit=REFLECTIVE_BUDGET_LIMIT,
                budget_pressure=_pressure(reflective_budget_used, REFLECTIVE_BUDGET_LIMIT),
                budget_exceeded=reflective_budget_used > REFLECTIVE_BUDGET_LIMIT,
                local_first_budget=True,
                high_tier_evaluation_blocked=True,
            ),
            reflective_window=ReflectiveWindowFrame(
                reflective_window_active=True,
                reflective_window_items=bounded_window,
                reflective_window_limit=MAX_REFLECTIVE_WINDOW_ITEMS,
                reflective_window_pressure=window_pressure,
                reflective_saturation_score=saturation_score,
                reflective_saturation_threshold=REFLECTIVE_SATURATION_THRESHOLD,
                bounded_reflective_window=True,
                evicted_window_items=evicted_window_items,
            ),
            reflective_governance=ReflectiveGovernanceFrame(
                reflective_governance_active=True,
                local_patch_scope_enforced=True,
                bounded_reflective_windows_enforced=True,
                deterministic_evaluation_enforced=True,
                bounded_scoring_ranges_enforced=True,
                bounded_reflective_history_enforced=True,
                autonomous_self_improvement_blocked=(autonomous_self_improvement_attempts > 0),
                recursive_optimization_blocked=recursive_optimization_attempts > 0,
                hidden_reflective_execution_blocked=(hidden_reflective_execution_attempts > 0),
                self_expanding_evaluation_chains_blocked=(self_expanding_evaluation_attempts > 0),
                governance_policy_mutation_blocked=governance_mutation_attempts > 0,
                objective_synthesis_blocked=objective_synthesis_attempts > 0,
                retrieval_scope_widening_blocked=retrieval_scope_widening_attempts > 0,
            ),
            reflective_termination=ReflectiveTerminationFrame(
                reflective_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                budget_exceeded=reflective_budget_used > REFLECTIVE_BUDGET_LIMIT,
                recursive_evaluation_detected=recursive_evaluation_attempts > 0,
                governance_violation_detected=governance_violation,
                saturation_threshold_exceeded=(
                    saturation_score >= REFLECTIVE_SATURATION_THRESHOLD
                ),
                continuation_invalidation_threshold_exceeded=(
                    continuation_validity_score <= CONTINUATION_INVALIDATION_THRESHOLD
                ),
            ),
            reflective_confidence=ReflectiveConfidenceFrame(
                reflective_confidence_active=True,
                confidence_score=confidence_score,
                confidence_status=_score_label(confidence_score),
                deterministic_confidence=True,
                frontier_evaluation_dependency_reduced=True,
            ),
            reflective_history=ReflectiveHistoryFrame(
                reflective_history_active=True,
                reflective_history=bounded_history,
                history_limit=MAX_REFLECTIVE_HISTORY,
                compact_history_summary=(
                    f"history={len(bounded_history)};window={len(bounded_window)}"
                ),
                raw_transcript_replay_blocked=raw_transcript_replay_attempts > 0,
                recursive_history_expansion_blocked=(
                    len(reflective_history_items) > MAX_REFLECTIVE_HISTORY
                ),
            ),
            reflective_eviction=ReflectiveEvictionFrame(
                reflective_eviction_active=True,
                evicted_history_items=evicted_history_items,
                evicted_window_items=evicted_window_items,
                eviction_count=len(evicted_history_items) + len(evicted_window_items),
                bounded_eviction_active=bool(evicted_history_items or evicted_window_items),
                eviction_summary=(
                    f"history={len(evicted_history_items)};window={len(evicted_window_items)}"
                ),
            ),
            execution_quality_score=execution_quality_score,
            cognitive_coherence_score=cognitive_coherence_score,
            continuation_validity_score=continuation_validity_score,
            planning_integrity_score=planning_integrity_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            provider_routing="LOCAL_FIRST_NO_FRONTIER_REFLECTION",
            estimated_avoided_recursive_reflection=66 + recursive_evaluation_attempts * 8,
            estimated_avoided_self_optimization=61 + autonomous_self_improvement_attempts * 7,
            estimated_avoided_frontier_evaluation=73,
        )


def _clamp(score: int) -> int:
    return max(MIN_SCORE, min(MAX_SCORE, score))


def _pressure(value: int, limit: int) -> str:
    if value > limit:
        return "HIGH"
    if value >= max(1, limit - 1):
        return "MEDIUM"
    return "LOW"


def _pressure_penalty(pressure: str) -> int:
    return {"LOW": 0, "MEDIUM": 10, "HIGH": 24}.get(pressure, 12)


def _status_penalty(status: str) -> int:
    return {"STABLE": 0, "WATCH": 15, "RESET_RECOMMENDED": 34}.get(status, 12)


def _score_label(score: int) -> str:
    if score >= 80:
        return "STABLE"
    if score >= 55:
        return "WATCH"
    return "RESET_RECOMMENDED"


def _reset_recommendation(score: int) -> str:
    if score < 55:
        return "COMPACT_REFLECTIVE_WINDOW_AND_RESET_BOUNDARY"
    if score < 80:
        return "WATCH_REFLECTIVE_PRESSURE_AND_KEEP_LOCAL_PATCH"
    return "CONTINUE_BOUNDED_REFLECTION"


def _termination_reasons(
    budget_exceeded: bool,
    recursive_evaluation_detected: bool,
    governance_violation_detected: bool,
    saturation_threshold_exceeded: bool,
    continuation_invalidation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if budget_exceeded:
        reasons.append("REFLECTIVE_BUDGET_EXCEEDED")
    if recursive_evaluation_detected:
        reasons.append("RECURSIVE_EVALUATION_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if saturation_threshold_exceeded:
        reasons.append("REFLECTIVE_SATURATION_EXCEEDED")
    if continuation_invalidation_threshold_exceeded:
        reasons.append("CONTINUATION_INVALIDATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)
