from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_policy import RuntimePolicyEngine

SPRINT_LOOP_REQUIREMENT_IDS = tuple(f"FR-SPRINTLOOP-{index:02d}" for index in range(1, 65)) + (
    "NFR-COST-71",
    "NFR-ARCH-84",
    "NFR-SEC-55",
)
SPRINT_LOOP_TEST_IDS = tuple(f"TC-SPRINTLOOP-{index:02d}" for index in range(1, 65))

MAX_SPRINT_TASK_WINDOW = 5
MAX_VALIDATION_QUEUE = 5
MAX_RETRY_WINDOW = 3
MAX_CONTINUATION_DEPTH = 2
MAX_SPRINT_HISTORY = 5
SPRINT_BUDGET_LIMIT = 12
REGRESSION_SATURATION_THRESHOLD = 78
RETRY_AMPLIFICATION_THRESHOLD = 3
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_ACTIVE_SCOPE = "runtime-managed-local-patch-sprint"
DEFAULT_TASK_WINDOW = (
    "inspect-runtime",
    "apply-local-patch",
    "run-targeted-tests",
    "run-runtime-audit",
    "prepare-commit",
)
DEFAULT_VALIDATION_QUEUE = (
    "targeted_pytest",
    "adjacent_pytest",
    "runtime_audit",
    "vscode_compile",
    "diff_check",
)
DEFAULT_RUNTIME_DEPENDENCIES = (
    "runtime_policy",
    "execution_memory",
    "adaptive_provider",
    "reflective_evaluation",
)
DEFAULT_SPRINT_HISTORY = (
    "plan",
    "implement",
    "validate",
    "commit",
    "push",
)


@dataclass(frozen=True)
class SprintPlanningFrame:
    sprint_planning_active: bool
    active_sprint_scope: str
    bounded_task_window: tuple[str, ...]
    bounded_validation_queue: tuple[str, ...]
    bounded_runtime_dependencies: tuple[str, ...]
    bounded_retry_window: int
    sprint_planning_score: int
    deterministic_sprint_summary: str
    bounded_sprint_recommendation: str


@dataclass(frozen=True)
class SprintScopeFrame:
    sprint_scope_active: bool
    local_patch_scope_enforced: bool
    active_scope: str
    task_window_limit: int
    validation_queue_limit: int
    sprint_scope_expansion_blocked: bool
    dynamic_scope_widening_blocked: bool
    deterministic_scope_summary: str


@dataclass(frozen=True)
class SprintValidationFrame:
    sprint_validation_active: bool
    validation_sequence: tuple[str, ...]
    validation_saturation: int
    validation_interruption_pressure: int
    validation_cooldown_window: int
    validation_regression_pressure: int
    sprint_validation_score: int
    deterministic_validation_summary: str
    bounded_validation_reset_recommendation: str


@dataclass(frozen=True)
class SprintRegressionFrame:
    sprint_regression_active: bool
    repeated_regressions: int
    retry_amplification: int
    regression_cooldown_pressure: int
    bounded_failure_recurrence: int
    bounded_dependency_instability: int
    sprint_regression_score: int
    deterministic_regression_summary: str
    bounded_stabilization_recommendation: str


@dataclass(frozen=True)
class SprintRetryFrame:
    sprint_retry_active: bool
    retry_count: int
    retry_window_limit: int
    bounded_retry_governance: bool
    retry_amplification_blocked: bool
    hidden_retry_execution_blocked: bool
    deterministic_retry_summary: str
    bounded_retry_recommendation: str


@dataclass(frozen=True)
class SprintContinuationFrame:
    sprint_continuation_active: bool
    continuation_depth: int
    continuation_depth_limit: int
    bounded_continuation_depth: bool
    bounded_continuation_resets: bool
    continuation_interruption_window: int
    continuation_cooldown_required: bool
    sprint_continuation_score: int
    deterministic_continuation_summary: str
    bounded_continuation_reset_recommendation: str


@dataclass(frozen=True)
class SprintCooldownFrame:
    sprint_cooldown_active: bool
    validation_cooldown_required: bool
    regression_cooldown_required: bool
    continuation_cooldown_required: bool
    retry_cooldown_required: bool
    deterministic_cooldown_summary: str
    bounded_cooldown_recommendation: str


@dataclass(frozen=True)
class SprintCommitReadinessFrame:
    sprint_commit_readiness_active: bool
    validation_completion: bool
    regression_stabilized: bool
    runtime_coherence: bool
    bounded_policy_compliance: bool
    bounded_audit_integrity: bool
    sprint_commit_readiness_score: int
    deterministic_commit_readiness_summary: str
    bounded_commit_recommendation: str
    autonomous_commit_blocked: bool
    autonomous_push_blocked: bool
    autonomous_merge_blocked: bool


@dataclass(frozen=True)
class SprintExecutionFrame:
    sprint_execution_active: bool
    deterministic_sprint_execution: bool
    bounded_validation_authority: bool
    bounded_retry_authority: bool
    bounded_continuation_authority: bool
    hidden_background_execution_blocked: bool
    deterministic_execution_summary: str


@dataclass(frozen=True)
class SprintGovernanceFrame:
    sprint_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_sprint_execution_enforced: bool
    bounded_sprint_windows_enforced: bool
    bounded_retry_authority_enforced: bool
    bounded_validation_authority_enforced: bool
    bounded_continuation_authority_enforced: bool
    recursive_sprint_generation_blocked: bool
    hidden_sprint_execution_blocked: bool
    autonomous_branch_mutation_blocked: bool
    autonomous_governance_mutation_blocked: bool
    self_expanding_sprint_loops_blocked: bool
    retrieval_scope_widening_blocked: bool


@dataclass(frozen=True)
class SprintTerminationFrame:
    sprint_termination_active: bool
    sprint_loop_terminated: bool
    termination_reasons: tuple[str, ...]
    sprint_budget_exceeded: bool
    recursive_sprint_detected: bool
    governance_violation_detected: bool
    regression_saturation_threshold_exceeded: bool
    retry_amplification_threshold_exceeded: bool
    continuation_depth_exceeded: bool


@dataclass(frozen=True)
class SprintBudgetFrame:
    sprint_budget_active: bool
    sprint_budget_used: int
    sprint_budget_limit: int
    sprint_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class SprintHistoryFrame:
    sprint_history_active: bool
    sprint_history: tuple[str, ...]
    sprint_history_limit: int
    compact_sprint_history_summary: str
    sprint_history_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class SprintConfidenceFrame:
    sprint_confidence_active: bool
    sprint_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    commit_readiness_confidence: bool


@dataclass(frozen=True)
class SprintEvictionFrame:
    sprint_eviction_active: bool
    evicted_task_window_items: tuple[str, ...]
    evicted_validation_items: tuple[str, ...]
    evicted_history_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class SprintLoopFrame:
    sprint_loop_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    sprint_planning: SprintPlanningFrame
    sprint_scope: SprintScopeFrame
    sprint_validation: SprintValidationFrame
    sprint_regression: SprintRegressionFrame
    sprint_retry: SprintRetryFrame
    sprint_continuation: SprintContinuationFrame
    sprint_cooldown: SprintCooldownFrame
    sprint_commit_readiness: SprintCommitReadinessFrame
    sprint_execution: SprintExecutionFrame
    sprint_governance: SprintGovernanceFrame
    sprint_termination: SprintTerminationFrame
    sprint_budget: SprintBudgetFrame
    sprint_history: SprintHistoryFrame
    sprint_confidence: SprintConfidenceFrame
    sprint_eviction: SprintEvictionFrame
    sprint_validation_score: int
    sprint_regression_score: int
    sprint_commit_readiness_score: int
    sprint_continuation_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    sprint_loop_mode: str
    estimated_avoided_manual_orchestration: int
    estimated_avoided_recursive_sprints: int
    estimated_avoided_frontier_supervision: int


class SprintLoopRuntime:
    def evaluate(
        self,
        *,
        active_sprint_scope: str = DEFAULT_ACTIVE_SCOPE,
        task_window_items: tuple[str, ...] = DEFAULT_TASK_WINDOW,
        validation_queue_items: tuple[str, ...] = DEFAULT_VALIDATION_QUEUE,
        runtime_dependencies: tuple[str, ...] = DEFAULT_RUNTIME_DEPENDENCIES,
        sprint_history_items: tuple[str, ...] = DEFAULT_SPRINT_HISTORY,
        validation_completed_count: int = 5,
        validation_interruption_pressure: int = 0,
        validation_cooldown_window: int = 1,
        validation_regression_pressure: int = 1,
        repeated_regressions: int = 0,
        retry_amplification: int = 1,
        regression_cooldown_pressure: int = 1,
        bounded_failure_recurrence: int = 0,
        bounded_dependency_instability: int = 0,
        retry_count: int = 1,
        continuation_depth: int = 1,
        continuation_interruption_window: int = 0,
        sprint_budget_used: int = 7,
        recursive_sprint_attempts: int = 0,
        sprint_scope_expansion_attempts: int = 0,
        hidden_sprint_execution_attempts: int = 0,
        autonomous_branch_mutation_attempts: int = 0,
        autonomous_governance_mutation_attempts: int = 0,
        self_expanding_sprint_loop_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
    ) -> SprintLoopFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=retry_count,
            continuation_depth=continuation_depth,
            policy_budget_used=min(sprint_budget_used, SPRINT_BUDGET_LIMIT),
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=retry_count,
            continuation_reuse_depth=continuation_depth,
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=repeated_regressions,
            retry_amplification_pressure=retry_amplification,
        )
        mediation = ExecutionSequencer().mediate(retry_count=retry_count)

        bounded_task_window = task_window_items[:MAX_SPRINT_TASK_WINDOW]
        bounded_validation_queue = validation_queue_items[:MAX_VALIDATION_QUEUE]
        bounded_runtime_dependencies = runtime_dependencies[:MAX_SPRINT_TASK_WINDOW]
        bounded_history = sprint_history_items[:MAX_SPRINT_HISTORY]
        evicted_task_items = task_window_items[MAX_SPRINT_TASK_WINDOW:]
        evicted_validation_items = validation_queue_items[MAX_VALIDATION_QUEUE:]
        evicted_history_items = sprint_history_items[MAX_SPRINT_HISTORY:]

        validation_saturation = _clamp(
            max(0, len(validation_queue_items) - validation_completed_count) * 16
            + validation_interruption_pressure * 12
            + validation_regression_pressure * 10
            + max(0, len(validation_queue_items) - MAX_VALIDATION_QUEUE) * 8
        )
        sprint_validation_score = _clamp(
            96
            - validation_saturation // 2
            - validation_interruption_pressure * 8
            + int(runtime_policy.runtime_policy_active) * 4
        )
        regression_pressure = _clamp(
            repeated_regressions * 18
            + retry_amplification * 12
            + regression_cooldown_pressure * 8
            + bounded_failure_recurrence * 14
            + bounded_dependency_instability * 12
        )
        sprint_regression_score = _clamp(100 - regression_pressure)
        sprint_continuation_score = _clamp(
            92
            - max(0, continuation_depth - 1) * 16
            - continuation_interruption_window * 8
            - int(continuation_depth > MAX_CONTINUATION_DEPTH) * 22
        )
        validation_completion = validation_completed_count >= len(bounded_validation_queue)
        regression_stabilized = regression_pressure < 45
        runtime_coherence = (
            runtime_policy.runtime_policy_active
            and reflection.runtime_integrity.runtime_integrity_score >= 80
        )
        policy_compliance = runtime_policy.policy_coherence.policy_coherence_score >= 60
        audit_integrity = (
            execution_memory.execution_memory_active and mediation.runtime_mediation_active
        )
        sprint_commit_readiness_score = _clamp(
            int(validation_completion) * 24
            + int(regression_stabilized) * 22
            + int(runtime_coherence) * 20
            + int(policy_compliance) * 18
            + int(audit_integrity) * 16
            - validation_interruption_pressure * 4
        )
        recursive_sprint_detected = recursive_sprint_attempts > 0
        governance_violation = any(
            (
                sprint_scope_expansion_attempts,
                hidden_sprint_execution_attempts,
                autonomous_branch_mutation_attempts,
                autonomous_governance_mutation_attempts,
                self_expanding_sprint_loop_attempts,
                retrieval_scope_widening_attempts,
            )
        )
        retry_amplification_exceeded = retry_amplification > RETRY_AMPLIFICATION_THRESHOLD
        regression_saturation_exceeded = regression_pressure >= REGRESSION_SATURATION_THRESHOLD
        continuation_depth_exceeded = continuation_depth > MAX_CONTINUATION_DEPTH
        termination_reasons = _termination_reasons(
            sprint_budget_used > SPRINT_BUDGET_LIMIT,
            recursive_sprint_detected,
            governance_violation,
            regression_saturation_exceeded,
            retry_amplification_exceeded,
            continuation_depth_exceeded,
        )
        confidence_score = _clamp(
            (sprint_validation_score + sprint_regression_score + sprint_continuation_score) // 3
            + sprint_commit_readiness_score // 8
            - len(termination_reasons) * 8
        )

        return SprintLoopFrame(
            sprint_loop_active=True,
            requirement_ids=SPRINT_LOOP_REQUIREMENT_IDS,
            test_ids=SPRINT_LOOP_TEST_IDS,
            sprint_planning=SprintPlanningFrame(
                sprint_planning_active=True,
                active_sprint_scope=active_sprint_scope,
                bounded_task_window=bounded_task_window,
                bounded_validation_queue=bounded_validation_queue,
                bounded_runtime_dependencies=bounded_runtime_dependencies,
                bounded_retry_window=MAX_RETRY_WINDOW,
                sprint_planning_score=_clamp(
                    len(bounded_task_window) * 10
                    + len(bounded_validation_queue) * 8
                    + len(bounded_runtime_dependencies) * 7
                ),
                deterministic_sprint_summary=(
                    f"scope={active_sprint_scope};tasks={len(bounded_task_window)};validation={len(bounded_validation_queue)}"
                ),
                bounded_sprint_recommendation="FOLLOW_BOUNDED_SPRINT_SEQUENCE",
            ),
            sprint_scope=SprintScopeFrame(
                sprint_scope_active=True,
                local_patch_scope_enforced=True,
                active_scope=active_sprint_scope,
                task_window_limit=MAX_SPRINT_TASK_WINDOW,
                validation_queue_limit=MAX_VALIDATION_QUEUE,
                sprint_scope_expansion_blocked=sprint_scope_expansion_attempts > 0,
                dynamic_scope_widening_blocked=retrieval_scope_widening_attempts > 0,
                deterministic_scope_summary=f"tasks={len(bounded_task_window)};local_patch=true",
            ),
            sprint_validation=SprintValidationFrame(
                sprint_validation_active=True,
                validation_sequence=bounded_validation_queue,
                validation_saturation=validation_saturation,
                validation_interruption_pressure=validation_interruption_pressure,
                validation_cooldown_window=validation_cooldown_window,
                validation_regression_pressure=validation_regression_pressure,
                sprint_validation_score=sprint_validation_score,
                deterministic_validation_summary=(
                    f"completed={validation_completed_count};queue={len(bounded_validation_queue)};saturation={validation_saturation}"
                ),
                bounded_validation_reset_recommendation=(
                    "RESET_VALIDATION_QUEUE_AFTER_COOLDOWN"
                    if validation_saturation >= 70
                    else "CONTINUE_BOUNDED_VALIDATION_SEQUENCE"
                ),
            ),
            sprint_regression=SprintRegressionFrame(
                sprint_regression_active=True,
                repeated_regressions=repeated_regressions,
                retry_amplification=retry_amplification,
                regression_cooldown_pressure=regression_cooldown_pressure,
                bounded_failure_recurrence=bounded_failure_recurrence,
                bounded_dependency_instability=bounded_dependency_instability,
                sprint_regression_score=sprint_regression_score,
                deterministic_regression_summary=(
                    f"regressions={repeated_regressions};retry={retry_amplification};pressure={regression_pressure}"
                ),
                bounded_stabilization_recommendation=(
                    "STABILIZE_REGRESSION_BEFORE_COMMIT"
                    if regression_pressure >= 45
                    else "REGRESSION_STABLE_FOR_COMMIT_READINESS"
                ),
            ),
            sprint_retry=SprintRetryFrame(
                sprint_retry_active=True,
                retry_count=retry_count,
                retry_window_limit=MAX_RETRY_WINDOW,
                bounded_retry_governance=retry_count <= MAX_RETRY_WINDOW,
                retry_amplification_blocked=retry_amplification_exceeded,
                hidden_retry_execution_blocked=True,
                deterministic_retry_summary=(
                    f"retry={retry_count};amplification={retry_amplification}"
                ),
                bounded_retry_recommendation=(
                    "RESET_RETRY_WINDOW_AND_COOLDOWN"
                    if retry_amplification_exceeded
                    else "RETRY_WITHIN_BOUNDED_WINDOW"
                ),
            ),
            sprint_continuation=SprintContinuationFrame(
                sprint_continuation_active=True,
                continuation_depth=continuation_depth,
                continuation_depth_limit=MAX_CONTINUATION_DEPTH,
                bounded_continuation_depth=not continuation_depth_exceeded,
                bounded_continuation_resets=True,
                continuation_interruption_window=continuation_interruption_window,
                continuation_cooldown_required=(
                    continuation_depth_exceeded or continuation_interruption_window > 0
                ),
                sprint_continuation_score=sprint_continuation_score,
                deterministic_continuation_summary=(
                    f"depth={continuation_depth};interrupt={continuation_interruption_window}"
                ),
                bounded_continuation_reset_recommendation=(
                    "RESET_SPRINT_CONTINUATION_WINDOW"
                    if continuation_depth_exceeded
                    else "CONTINUE_BOUNDED_SPRINT_LOOP"
                ),
            ),
            sprint_cooldown=SprintCooldownFrame(
                sprint_cooldown_active=True,
                validation_cooldown_required=validation_saturation >= 70,
                regression_cooldown_required=regression_pressure >= 45,
                continuation_cooldown_required=continuation_depth_exceeded,
                retry_cooldown_required=retry_amplification_exceeded,
                deterministic_cooldown_summary=(
                    f"validation={validation_saturation};regression={regression_pressure};retry={retry_amplification}"
                ),
                bounded_cooldown_recommendation=(
                    "APPLY_SPRINT_COOLDOWN"
                    if regression_pressure >= 45 or retry_amplification_exceeded
                    else "MAINTAIN_SPRINT_FLOW"
                ),
            ),
            sprint_commit_readiness=SprintCommitReadinessFrame(
                sprint_commit_readiness_active=True,
                validation_completion=validation_completion,
                regression_stabilized=regression_stabilized,
                runtime_coherence=runtime_coherence,
                bounded_policy_compliance=policy_compliance,
                bounded_audit_integrity=audit_integrity,
                sprint_commit_readiness_score=sprint_commit_readiness_score,
                deterministic_commit_readiness_summary=(
                    f"validation={str(validation_completion).lower()};regression={str(regression_stabilized).lower()};score={sprint_commit_readiness_score}"
                ),
                bounded_commit_recommendation=(
                    "READY_FOR_HUMAN_AUTHORIZED_COMMIT"
                    if sprint_commit_readiness_score >= 80 and not termination_reasons
                    else "DEFER_COMMIT_UNTIL_VALIDATION_STABLE"
                ),
                autonomous_commit_blocked=True,
                autonomous_push_blocked=True,
                autonomous_merge_blocked=True,
            ),
            sprint_execution=SprintExecutionFrame(
                sprint_execution_active=True,
                deterministic_sprint_execution=True,
                bounded_validation_authority=True,
                bounded_retry_authority=True,
                bounded_continuation_authority=True,
                hidden_background_execution_blocked=True,
                deterministic_execution_summary=(
                    "sprint execution bounded; no hidden background execution"
                ),
            ),
            sprint_governance=SprintGovernanceFrame(
                sprint_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_sprint_execution_enforced=True,
                bounded_sprint_windows_enforced=True,
                bounded_retry_authority_enforced=True,
                bounded_validation_authority_enforced=True,
                bounded_continuation_authority_enforced=True,
                recursive_sprint_generation_blocked=True,
                hidden_sprint_execution_blocked=True,
                autonomous_branch_mutation_blocked=True,
                autonomous_governance_mutation_blocked=True,
                self_expanding_sprint_loops_blocked=True,
                retrieval_scope_widening_blocked=True,
            ),
            sprint_termination=SprintTerminationFrame(
                sprint_termination_active=True,
                sprint_loop_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                sprint_budget_exceeded=sprint_budget_used > SPRINT_BUDGET_LIMIT,
                recursive_sprint_detected=recursive_sprint_detected,
                governance_violation_detected=governance_violation,
                regression_saturation_threshold_exceeded=regression_saturation_exceeded,
                retry_amplification_threshold_exceeded=retry_amplification_exceeded,
                continuation_depth_exceeded=continuation_depth_exceeded,
            ),
            sprint_budget=SprintBudgetFrame(
                sprint_budget_active=True,
                sprint_budget_used=sprint_budget_used,
                sprint_budget_limit=SPRINT_BUDGET_LIMIT,
                sprint_budget_exceeded=sprint_budget_used > SPRINT_BUDGET_LIMIT,
                budget_pressure=_pressure(sprint_budget_used, SPRINT_BUDGET_LIMIT),
            ),
            sprint_history=SprintHistoryFrame(
                sprint_history_active=True,
                sprint_history=bounded_history,
                sprint_history_limit=MAX_SPRINT_HISTORY,
                compact_sprint_history_summary=f"history={len(bounded_history)};loop=bounded",
                sprint_history_overflow_blocked=bool(evicted_history_items),
                self_expanding_history_blocked=self_expanding_sprint_loop_attempts > 0,
            ),
            sprint_confidence=SprintConfidenceFrame(
                sprint_confidence_active=True,
                sprint_confidence_score=confidence_score,
                confidence_status=_score_label(confidence_score),
                deterministic_confidence=True,
                commit_readiness_confidence=sprint_commit_readiness_score >= 80,
            ),
            sprint_eviction=SprintEvictionFrame(
                sprint_eviction_active=True,
                evicted_task_window_items=evicted_task_items,
                evicted_validation_items=evicted_validation_items,
                evicted_history_items=evicted_history_items,
                eviction_count=(
                    len(evicted_task_items)
                    + len(evicted_validation_items)
                    + len(evicted_history_items)
                ),
                bounded_eviction_active=bool(
                    evicted_task_items or evicted_validation_items or evicted_history_items
                ),
                eviction_summary=(
                    f"tasks={len(evicted_task_items)};validation={len(evicted_validation_items)};history={len(evicted_history_items)}"
                ),
            ),
            sprint_validation_score=sprint_validation_score,
            sprint_regression_score=sprint_regression_score,
            sprint_commit_readiness_score=sprint_commit_readiness_score,
            sprint_continuation_score=sprint_continuation_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            sprint_loop_mode="LOCAL_PATCH_BOUNDED_SPRINT_LOOP",
            estimated_avoided_manual_orchestration=76,
            estimated_avoided_recursive_sprints=69 + recursive_sprint_attempts * 8,
            estimated_avoided_frontier_supervision=72 + sprint_commit_readiness_score // 10,
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
    sprint_budget_exceeded: bool,
    recursive_sprint_detected: bool,
    governance_violation_detected: bool,
    regression_saturation_threshold_exceeded: bool,
    retry_amplification_threshold_exceeded: bool,
    continuation_depth_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if sprint_budget_exceeded:
        reasons.append("SPRINT_BUDGET_EXCEEDED")
    if recursive_sprint_detected:
        reasons.append("RECURSIVE_SPRINT_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if regression_saturation_threshold_exceeded:
        reasons.append("REGRESSION_SATURATION_THRESHOLD_EXCEEDED")
    if retry_amplification_threshold_exceeded:
        reasons.append("RETRY_AMPLIFICATION_THRESHOLD_EXCEEDED")
    if continuation_depth_exceeded:
        reasons.append("CONTINUATION_DEPTH_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "SPRINT_LOOP_REQUIREMENT_IDS",
    "SPRINT_LOOP_TEST_IDS",
    "MAX_CONTINUATION_DEPTH",
    "MAX_RETRY_WINDOW",
    "MAX_SPRINT_HISTORY",
    "MAX_SPRINT_TASK_WINDOW",
    "MAX_VALIDATION_QUEUE",
    "REGRESSION_SATURATION_THRESHOLD",
    "RETRY_AMPLIFICATION_THRESHOLD",
    "SPRINT_BUDGET_LIMIT",
    "SprintBudgetFrame",
    "SprintCommitReadinessFrame",
    "SprintConfidenceFrame",
    "SprintContinuationFrame",
    "SprintCooldownFrame",
    "SprintEvictionFrame",
    "SprintExecutionFrame",
    "SprintGovernanceFrame",
    "SprintHistoryFrame",
    "SprintLoopFrame",
    "SprintLoopRuntime",
    "SprintPlanningFrame",
    "SprintRegressionFrame",
    "SprintRetryFrame",
    "SprintScopeFrame",
    "SprintTerminationFrame",
    "SprintValidationFrame",
]
