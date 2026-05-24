from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.cognitive_state import CognitiveStateRuntime
from ai_dev_os.continuous_runtime_audit import ContinuousRuntimeAuditRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.failure_injection import FailureInjectionRuntime
from ai_dev_os.intentional_planning import IntentionalPlanningRuntime
from ai_dev_os.main_merge_qualification import MainMergeQualificationRuntime
from ai_dev_os.provider_cost_stabilization import ProviderCostStabilizationRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_hardening import RuntimeHardeningRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_orchestrator import RuntimeOrchestrator
from ai_dev_os.runtime_policy import RuntimePolicyEngine
from ai_dev_os.soak_stability import SoakStabilityRuntime
from ai_dev_os.sprint_loop import SprintLoopRuntime
from ai_dev_os.verified_execution import VerifiedExecutionRuntime

MAIN_MERGE_REHEARSAL_REQUIREMENT_IDS = tuple(
    f"FR-MAINMERGEREHEARSAL-{index:02d}" for index in range(1, 61)
) + (
    "NFR-LOCALPATCH-01",
    "NFR-GOVERNANCE-01",
    "NFR-DETERMINISTIC-01",
)
MAIN_MERGE_REHEARSAL_TEST_IDS = tuple(
    f"TC-MAINMERGEREHEARSAL-{index:02d}" for index in range(1, 11)
)

MAX_REHEARSAL_WINDOW = 5
MAX_REHEARSAL_HISTORY = 5
REHEARSAL_BUDGET_LIMIT = 12
REHEARSAL_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_REHEARSAL_HISTORY = (
    "protected-branch",
    "merge-conflict",
    "rollback",
    "post-merge",
    "ci-readiness",
)
DEFAULT_REHEARSAL_SCOPE = (
    "branch-protection",
    "merge-gates",
    "rollback",
    "runtime-audit",
    "ci-validation",
)


@dataclass(frozen=True)
class ProtectedBranchReadinessFrame:
    protected_branch_readiness_active: bool
    protected_branch_readiness: int
    branch_policy_readiness: int
    bounded_merge_gate_survivability: int
    bounded_governance_continuity: int
    protected_branch_readiness_score: int
    deterministic_protected_branch_summary: str
    bounded_protected_branch_recommendation: str


@dataclass(frozen=True)
class MergeConflictAuditFrame:
    merge_conflict_audit_active: bool
    merge_conflict_visibility: int
    bounded_conflict_survivability: int
    runtime_coherence_preservation: int
    bounded_merge_drift_resistance: int
    merge_conflict_visibility_score: int
    deterministic_conflict_summary: str
    bounded_conflict_recommendation: str


@dataclass(frozen=True)
class PostMergeRuntimeAuditFrame:
    post_merge_runtime_audit_active: bool
    post_merge_runtime_stability: int
    post_merge_orchestration_stability: int
    post_merge_provider_stability: int
    post_merge_continuation_stability: int
    post_merge_runtime_score: int
    deterministic_post_merge_summary: str
    bounded_post_merge_recommendation: str


@dataclass(frozen=True)
class MergeRollbackReadinessFrame:
    merge_rollback_readiness_active: bool
    rollback_survivability: int
    rollback_runtime_coherence: int
    rollback_governance_continuity: int
    rollback_operational_stability: int
    rollback_survivability_score: int
    deterministic_rollback_summary: str
    bounded_rollback_recommendation: str


@dataclass(frozen=True)
class BranchProtectionRehearsalFrame:
    branch_protection_rehearsal_active: bool
    branch_protection_mutation_blocked: bool
    real_merge_execution_blocked: bool
    protected_branch_write_blocked: bool
    remote_policy_mutation_blocked: bool
    hidden_merge_orchestration_blocked: bool


@dataclass(frozen=True)
class MergeCIReadinessFrame:
    merge_ci_readiness_active: bool
    ci_trigger_readiness: int
    validation_continuity: int
    compile_continuity: int
    bounded_workflow_survivability: int
    ci_readiness_score: int
    deterministic_ci_summary: str
    bounded_ci_recommendation: str


@dataclass(frozen=True)
class RehearsalGovernanceFrame:
    rehearsal_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_rehearsal_enforced: bool
    bounded_rehearsal_windows_enforced: bool
    autonomous_merge_blocked: bool
    recursive_rehearsal_blocked: bool
    governance_policy_mutation_blocked: bool
    retrieval_scope_widening_blocked: bool
    novel_merge_strategy_synthesis_blocked: bool
    hidden_background_execution_blocked: bool


@dataclass(frozen=True)
class RehearsalBudgetFrame:
    rehearsal_budget_active: bool
    rehearsal_budget_used: int
    rehearsal_budget_limit: int
    rehearsal_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class RehearsalTerminationFrame:
    rehearsal_termination_active: bool
    main_merge_rehearsal_terminated: bool
    termination_reasons: tuple[str, ...]
    rehearsal_budget_exceeded: bool
    recursive_rehearsal_detected: bool
    governance_violation_detected: bool
    rehearsal_saturation_threshold_exceeded: bool


@dataclass(frozen=True)
class RehearsalHistoryFrame:
    rehearsal_history_active: bool
    rehearsal_history: tuple[str, ...]
    rehearsal_scope: tuple[str, ...]
    rehearsal_history_limit: int
    compact_rehearsal_history_summary: str
    rehearsal_history_overflow_blocked: bool
    rehearsal_scope_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class RehearsalConfidenceFrame:
    rehearsal_confidence_active: bool
    rehearsal_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    protected_branch_confidence: bool


@dataclass(frozen=True)
class RehearsalEvictionFrame:
    rehearsal_eviction_active: bool
    evicted_rehearsal_history_items: tuple[str, ...]
    evicted_rehearsal_scope_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class MainMergeRehearsalFrame:
    main_merge_rehearsal_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    protected_branch_readiness: ProtectedBranchReadinessFrame
    merge_conflict_audit: MergeConflictAuditFrame
    post_merge_runtime_audit: PostMergeRuntimeAuditFrame
    merge_rollback_readiness: MergeRollbackReadinessFrame
    branch_protection_rehearsal: BranchProtectionRehearsalFrame
    merge_ci_readiness: MergeCIReadinessFrame
    rehearsal_governance: RehearsalGovernanceFrame
    rehearsal_budget: RehearsalBudgetFrame
    rehearsal_termination: RehearsalTerminationFrame
    rehearsal_history: RehearsalHistoryFrame
    rehearsal_confidence: RehearsalConfidenceFrame
    rehearsal_eviction: RehearsalEvictionFrame
    protected_branch_readiness_score: int
    merge_conflict_visibility_score: int
    rollback_survivability_score: int
    post_merge_runtime_score: int
    ci_readiness_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    main_merge_rehearsal_mode: str
    estimated_avoided_merge_instability: int
    estimated_avoided_post_merge_regression: int
    estimated_avoided_frontier_recovery: int


class MainMergeRehearsalRuntime:
    def evaluate(
        self,
        *,
        rehearsal_history_items: tuple[str, ...] = DEFAULT_REHEARSAL_HISTORY,
        rehearsal_scope_items: tuple[str, ...] = DEFAULT_REHEARSAL_SCOPE,
        protected_branch_readiness: int = 4,
        branch_policy_readiness: int = 4,
        bounded_merge_gate_survivability: int = 4,
        bounded_governance_continuity: int = 4,
        merge_conflict_visibility: int = 4,
        bounded_conflict_survivability: int = 4,
        runtime_coherence_preservation: int = 4,
        bounded_merge_drift_resistance: int = 4,
        rollback_survivability: int = 4,
        rollback_runtime_coherence: int = 4,
        rollback_governance_continuity: int = 4,
        rollback_operational_stability: int = 4,
        post_merge_runtime_stability: int = 4,
        post_merge_orchestration_stability: int = 4,
        post_merge_provider_stability: int = 4,
        post_merge_continuation_stability: int = 4,
        ci_trigger_readiness: int = 4,
        validation_continuity: int = 4,
        compile_continuity: int = 4,
        bounded_workflow_survivability: int = 4,
        protected_branch_drift: int = 0,
        merge_drift: int = 0,
        rollback_drift: int = 0,
        post_merge_drift: int = 0,
        ci_drift: int = 0,
        rehearsal_budget_used: int = 7,
        recursive_rehearsal_attempts: int = 0,
        autonomous_merge_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
        novel_merge_strategy_synthesis_attempts: int = 0,
        hidden_background_execution_attempts: int = 0,
        branch_protection_mutation_attempts: int = 0,
        protected_branch_write_attempts: int = 0,
        remote_policy_mutation_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> MainMergeRehearsalFrame:
        bounded_budget = min(rehearsal_budget_used, REHEARSAL_BUDGET_LIMIT)
        runtime_policy = RuntimePolicyEngine().evaluate(policy_budget_used=bounded_budget)
        orchestrator = RuntimeOrchestrator().evaluate(
            retry_amplification=max(1, 5 - post_merge_continuation_stability),
            repeated_regressions=max(0, 4 - validation_continuity),
            regression_pressure=max(1, merge_drift + 1),
            orchestration_budget_used=bounded_budget,
        )
        hardening = RuntimeHardeningRuntime().evaluate(hardening_budget_used=bounded_budget)
        continuous_audit = ContinuousRuntimeAuditRuntime().evaluate(
            audit_budget_used=bounded_budget
        )
        failure_injection = FailureInjectionRuntime().evaluate(
            dependency_deadlocks=max(0, merge_drift - 1),
            validation_retry_conflicts=max(0, 4 - validation_continuity),
            injection_budget_used=bounded_budget,
        )
        soak_stability = SoakStabilityRuntime().evaluate(
            runtime_interaction_entropy=max(1, post_merge_drift + 1),
            soak_budget_used=bounded_budget,
        )
        provider_cost = ProviderCostStabilizationRuntime().evaluate(
            frontier_dependency_pressure=max(1, post_merge_drift + 1),
            runtime_cost_drift=max(1, ci_drift + 1),
            cost_budget_used=bounded_budget,
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=max(1, post_merge_drift + 1),
            orchestration_instability=max(1, merge_drift + 1),
            provider_budget_used=bounded_budget,
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            retry_interruption_patterns=max(0, rollback_drift),
            execution_memory_budget_used=bounded_budget,
        )
        mediation = ExecutionSequencer().mediate(retry_count=max(1, 5 - rollback_survivability))
        sprint_loop = SprintLoopRuntime().evaluate(
            repeated_regressions=max(0, 4 - validation_continuity),
            sprint_budget_used=bounded_budget,
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=max(0, 4 - rollback_operational_stability)
        )
        cognitive_state = CognitiveStateRuntime().evaluate(
            objective="main-merge-rehearsal-local-patch",
            session_age_pressure=18 + post_merge_drift,
            recursive_reasoning_attempts=recursive_rehearsal_attempts,
        )
        planning = IntentionalPlanningRuntime().evaluate(
            interruption_duration=max(0, merge_drift),
            recursive_planning_attempts=recursive_rehearsal_attempts,
        )
        verified_execution = VerifiedExecutionRuntime().evaluate()
        qualification = MainMergeQualificationRuntime().evaluate(
            qualification_budget_used=bounded_budget
        )

        bounded_history = rehearsal_history_items[:MAX_REHEARSAL_HISTORY]
        bounded_scope = rehearsal_scope_items[:MAX_REHEARSAL_WINDOW]
        evicted_history = rehearsal_history_items[MAX_REHEARSAL_HISTORY:]
        evicted_scope = rehearsal_scope_items[MAX_REHEARSAL_WINDOW:]

        protected_branch_readiness_score = _readiness_score(
            protected_branch_readiness,
            branch_policy_readiness,
            bounded_merge_gate_survivability,
            bounded_governance_continuity,
            drift=protected_branch_drift,
            ecosystem_score=runtime_policy.policy_coherence.policy_coherence_score,
        )
        merge_conflict_visibility_score = _readiness_score(
            merge_conflict_visibility,
            bounded_conflict_survivability,
            runtime_coherence_preservation,
            bounded_merge_drift_resistance,
            drift=merge_drift,
            ecosystem_score=orchestrator.orchestration_confidence.orchestration_confidence_score,
        )
        rollback_survivability_score = _readiness_score(
            rollback_survivability,
            rollback_runtime_coherence,
            rollback_governance_continuity,
            rollback_operational_stability,
            drift=rollback_drift,
            ecosystem_score=failure_injection.recovery_resilience_score,
        )
        post_merge_runtime_score = _readiness_score(
            post_merge_runtime_stability,
            post_merge_orchestration_stability,
            post_merge_provider_stability,
            post_merge_continuation_stability,
            drift=post_merge_drift,
            ecosystem_score=soak_stability.long_session_stability_score,
        )
        ci_readiness_score = _readiness_score(
            ci_trigger_readiness,
            validation_continuity,
            compile_continuity,
            bounded_workflow_survivability,
            drift=ci_drift,
            ecosystem_score=verified_execution.confidence.confidence_score,
        )

        rehearsal_budget_exceeded = rehearsal_budget_used > REHEARSAL_BUDGET_LIMIT
        recursive_rehearsal_detected = recursive_rehearsal_attempts > 0
        governance_violation = any(
            (
                autonomous_merge_attempts,
                governance_policy_mutation_attempts,
                retrieval_scope_widening_attempts,
                novel_merge_strategy_synthesis_attempts,
                hidden_background_execution_attempts,
                branch_protection_mutation_attempts,
                protected_branch_write_attempts,
                remote_policy_mutation_attempts,
            )
        )
        ecosystem_average = _clamp(
            (
                continuous_audit.runtime_health_score
                + hardening.hardening_confidence.hardening_confidence_score
                + adaptive_provider.provider_confidence_score
                + execution_memory.execution_reuse_score
                + sprint_loop.sprint_validation_score
                + reflection.execution_quality.execution_quality_score
                + provider_cost.runtime_cost_pressure_score
                + qualification.merge_readiness_score
            )
            // 8
            + int(mediation.runtime_mediation_active) * 2
        )
        rehearsal_confidence_score = _clamp(
            (
                protected_branch_readiness_score
                + merge_conflict_visibility_score
                + rollback_survivability_score
                + post_merge_runtime_score
                + ci_readiness_score
                + ecosystem_average
            )
            // 6
        )
        cognitive_penalty = max(0, 60 - cognitive_state.decay.decay_score)
        planning_penalty = 0 if planning.planning_decay_status == "STABLE" else 8
        rehearsal_confidence_score = _clamp(
            rehearsal_confidence_score - cognitive_penalty // 5 - planning_penalty
        )
        rehearsal_saturation = _clamp(
            max(0, len(rehearsal_history_items) - MAX_REHEARSAL_HISTORY) * 10
            + max(0, len(rehearsal_scope_items) - MAX_REHEARSAL_WINDOW) * 12
            + max(0, 70 - rehearsal_confidence_score)
            + max(
                0,
                55
                - min(
                    protected_branch_readiness_score,
                    merge_conflict_visibility_score,
                    rollback_survivability_score,
                    post_merge_runtime_score,
                    ci_readiness_score,
                ),
            )
        )
        rehearsal_saturation_exceeded = rehearsal_saturation >= REHEARSAL_SATURATION_THRESHOLD
        termination_reasons = _termination_reasons(
            rehearsal_budget_exceeded,
            recursive_rehearsal_detected,
            governance_violation,
            rehearsal_saturation_exceeded,
        )
        final_confidence_score = _clamp(rehearsal_confidence_score - len(termination_reasons) * 8)

        return MainMergeRehearsalFrame(
            main_merge_rehearsal_active=True,
            requirement_ids=MAIN_MERGE_REHEARSAL_REQUIREMENT_IDS,
            test_ids=MAIN_MERGE_REHEARSAL_TEST_IDS,
            protected_branch_readiness=ProtectedBranchReadinessFrame(
                protected_branch_readiness_active=True,
                protected_branch_readiness=protected_branch_readiness,
                branch_policy_readiness=branch_policy_readiness,
                bounded_merge_gate_survivability=bounded_merge_gate_survivability,
                bounded_governance_continuity=bounded_governance_continuity,
                protected_branch_readiness_score=protected_branch_readiness_score,
                deterministic_protected_branch_summary=(
                    f"protected={protected_branch_readiness};policy={branch_policy_readiness};"
                    f"score={protected_branch_readiness_score}"
                ),
                bounded_protected_branch_recommendation=(
                    "DEFER_MERGE_FOR_PROTECTED_BRANCH_READINESS"
                    if protected_branch_readiness_score < 60
                    else "PROTECTED_BRANCH_REHEARSAL_READY"
                ),
            ),
            merge_conflict_audit=MergeConflictAuditFrame(
                merge_conflict_audit_active=True,
                merge_conflict_visibility=merge_conflict_visibility,
                bounded_conflict_survivability=bounded_conflict_survivability,
                runtime_coherence_preservation=runtime_coherence_preservation,
                bounded_merge_drift_resistance=bounded_merge_drift_resistance,
                merge_conflict_visibility_score=merge_conflict_visibility_score,
                deterministic_conflict_summary=(
                    f"visibility={merge_conflict_visibility};survivability="
                    f"{bounded_conflict_survivability};score={merge_conflict_visibility_score}"
                ),
                bounded_conflict_recommendation=(
                    "IMPROVE_CONFLICT_VISIBILITY_BEFORE_MERGE"
                    if merge_conflict_visibility_score < 60
                    else "MERGE_CONFLICT_VISIBILITY_BOUNDED"
                ),
            ),
            post_merge_runtime_audit=PostMergeRuntimeAuditFrame(
                post_merge_runtime_audit_active=True,
                post_merge_runtime_stability=post_merge_runtime_stability,
                post_merge_orchestration_stability=post_merge_orchestration_stability,
                post_merge_provider_stability=post_merge_provider_stability,
                post_merge_continuation_stability=post_merge_continuation_stability,
                post_merge_runtime_score=post_merge_runtime_score,
                deterministic_post_merge_summary=(
                    f"runtime={post_merge_runtime_stability};orchestration="
                    f"{post_merge_orchestration_stability};score={post_merge_runtime_score}"
                ),
                bounded_post_merge_recommendation=(
                    "STABILIZE_POST_MERGE_RUNTIME_BEFORE_MERGE"
                    if post_merge_runtime_score < 60
                    else "POST_MERGE_RUNTIME_REHEARSAL_SAFE"
                ),
            ),
            merge_rollback_readiness=MergeRollbackReadinessFrame(
                merge_rollback_readiness_active=True,
                rollback_survivability=rollback_survivability,
                rollback_runtime_coherence=rollback_runtime_coherence,
                rollback_governance_continuity=rollback_governance_continuity,
                rollback_operational_stability=rollback_operational_stability,
                rollback_survivability_score=rollback_survivability_score,
                deterministic_rollback_summary=(
                    f"rollback={rollback_survivability};runtime="
                    f"{rollback_runtime_coherence};score={rollback_survivability_score}"
                ),
                bounded_rollback_recommendation=(
                    "REHEARSE_ROLLBACK_SURVIVABILITY_BEFORE_MERGE"
                    if rollback_survivability_score < 60
                    else "ROLLBACK_SURVIVABILITY_REHEARSED"
                ),
            ),
            branch_protection_rehearsal=BranchProtectionRehearsalFrame(
                branch_protection_rehearsal_active=True,
                branch_protection_mutation_blocked=True,
                real_merge_execution_blocked=True,
                protected_branch_write_blocked=True,
                remote_policy_mutation_blocked=True,
                hidden_merge_orchestration_blocked=True,
            ),
            merge_ci_readiness=MergeCIReadinessFrame(
                merge_ci_readiness_active=True,
                ci_trigger_readiness=ci_trigger_readiness,
                validation_continuity=validation_continuity,
                compile_continuity=compile_continuity,
                bounded_workflow_survivability=bounded_workflow_survivability,
                ci_readiness_score=ci_readiness_score,
                deterministic_ci_summary=(
                    f"trigger={ci_trigger_readiness};validation={validation_continuity};"
                    f"score={ci_readiness_score}"
                ),
                bounded_ci_recommendation=(
                    "RESTORE_CI_READINESS_BEFORE_MERGE"
                    if ci_readiness_score < 60
                    else "CI_READINESS_REHEARSED"
                ),
            ),
            rehearsal_governance=RehearsalGovernanceFrame(
                rehearsal_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_rehearsal_enforced=True,
                bounded_rehearsal_windows_enforced=True,
                autonomous_merge_blocked=True,
                recursive_rehearsal_blocked=True,
                governance_policy_mutation_blocked=True,
                retrieval_scope_widening_blocked=True,
                novel_merge_strategy_synthesis_blocked=True,
                hidden_background_execution_blocked=True,
            ),
            rehearsal_budget=RehearsalBudgetFrame(
                rehearsal_budget_active=True,
                rehearsal_budget_used=rehearsal_budget_used,
                rehearsal_budget_limit=REHEARSAL_BUDGET_LIMIT,
                rehearsal_budget_exceeded=rehearsal_budget_exceeded,
                budget_pressure=_pressure(rehearsal_budget_used, REHEARSAL_BUDGET_LIMIT),
            ),
            rehearsal_termination=RehearsalTerminationFrame(
                rehearsal_termination_active=True,
                main_merge_rehearsal_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                rehearsal_budget_exceeded=rehearsal_budget_exceeded,
                recursive_rehearsal_detected=recursive_rehearsal_detected,
                governance_violation_detected=governance_violation,
                rehearsal_saturation_threshold_exceeded=rehearsal_saturation_exceeded,
            ),
            rehearsal_history=RehearsalHistoryFrame(
                rehearsal_history_active=True,
                rehearsal_history=bounded_history,
                rehearsal_scope=bounded_scope,
                rehearsal_history_limit=MAX_REHEARSAL_HISTORY,
                compact_rehearsal_history_summary=(
                    f"history={len(bounded_history)};scope={len(bounded_scope)}"
                ),
                rehearsal_history_overflow_blocked=bool(evicted_history),
                rehearsal_scope_overflow_blocked=bool(evicted_scope),
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            rehearsal_confidence=RehearsalConfidenceFrame(
                rehearsal_confidence_active=True,
                rehearsal_confidence_score=final_confidence_score,
                confidence_status=_score_label(final_confidence_score),
                deterministic_confidence=True,
                protected_branch_confidence=final_confidence_score >= 70,
            ),
            rehearsal_eviction=RehearsalEvictionFrame(
                rehearsal_eviction_active=True,
                evicted_rehearsal_history_items=evicted_history,
                evicted_rehearsal_scope_items=evicted_scope,
                eviction_count=len(evicted_history) + len(evicted_scope),
                bounded_eviction_active=bool(evicted_history or evicted_scope),
                eviction_summary=f"history={len(evicted_history)};scope={len(evicted_scope)}",
            ),
            protected_branch_readiness_score=protected_branch_readiness_score,
            merge_conflict_visibility_score=merge_conflict_visibility_score,
            rollback_survivability_score=rollback_survivability_score,
            post_merge_runtime_score=post_merge_runtime_score,
            ci_readiness_score=ci_readiness_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            main_merge_rehearsal_mode="LOCAL_PATCH_BOUNDED_MAIN_MERGE_REHEARSAL",
            estimated_avoided_merge_instability=80
            + max(0, 80 - merge_conflict_visibility_score) // 2,
            estimated_avoided_post_merge_regression=79
            + max(0, 80 - post_merge_runtime_score) // 2,
            estimated_avoided_frontier_recovery=78
            + max(0, 80 - provider_cost.frontier_dependency_score) // 2,
        )


def _readiness_score(
    first: int,
    second: int,
    third: int,
    fourth: int,
    *,
    drift: int,
    ecosystem_score: int,
) -> int:
    pressure = _clamp(
        max(0, 4 - first) * 14
        + max(0, 4 - second) * 12
        + max(0, 4 - third) * 12
        + max(0, 4 - fourth) * 10
        + drift * 14
        + max(0, 85 - ecosystem_score) // 3
    )
    return _clamp(100 - pressure)


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
    return "REHEARSAL_RECOVERY_REQUIRED"


def _termination_reasons(
    rehearsal_budget_exceeded: bool,
    recursive_rehearsal_detected: bool,
    governance_violation_detected: bool,
    rehearsal_saturation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if rehearsal_budget_exceeded:
        reasons.append("REHEARSAL_BUDGET_EXCEEDED")
    if recursive_rehearsal_detected:
        reasons.append("RECURSIVE_REHEARSAL_DETECTED")
    if governance_violation_detected:
        reasons.append("REHEARSAL_GOVERNANCE_VIOLATION_DETECTED")
    if rehearsal_saturation_threshold_exceeded:
        reasons.append("REHEARSAL_SATURATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "MAIN_MERGE_REHEARSAL_REQUIREMENT_IDS",
    "MAIN_MERGE_REHEARSAL_TEST_IDS",
    "MAX_REHEARSAL_HISTORY",
    "MAX_REHEARSAL_WINDOW",
    "REHEARSAL_BUDGET_LIMIT",
    "REHEARSAL_SATURATION_THRESHOLD",
    "BranchProtectionRehearsalFrame",
    "MainMergeRehearsalFrame",
    "MainMergeRehearsalRuntime",
    "MergeCIReadinessFrame",
    "MergeConflictAuditFrame",
    "MergeRollbackReadinessFrame",
    "PostMergeRuntimeAuditFrame",
    "ProtectedBranchReadinessFrame",
    "RehearsalBudgetFrame",
    "RehearsalConfidenceFrame",
    "RehearsalEvictionFrame",
    "RehearsalGovernanceFrame",
    "RehearsalHistoryFrame",
    "RehearsalTerminationFrame",
]
