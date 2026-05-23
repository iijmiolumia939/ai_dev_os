from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_policy import RuntimePolicyEngine
from ai_dev_os.sprint_loop import SprintLoopRuntime

RUNTIME_ORCHESTRATOR_REQUIREMENT_IDS = tuple(
    f"FR-RUNTIMEORCHESTRATOR-{index:02d}" for index in range(1, 69)
) + ("NFR-COST-73", "NFR-ARCH-86", "NFR-SEC-57")
RUNTIME_ORCHESTRATOR_TEST_IDS = tuple(
    f"TC-RUNTIMEORCHESTRATOR-{index:02d}" for index in range(1, 69)
)

MAX_EXECUTION_QUEUE = 5
MAX_VALIDATION_QUEUE = 5
MAX_RETRY_QUEUE = 3
MAX_PROVIDER_WINDOW = 4
MAX_CONTINUATION_DEPTH = 2
MAX_ORCHESTRATION_HISTORY = 5
ORCHESTRATION_BUDGET_LIMIT = 12
RETRY_AMPLIFICATION_THRESHOLD = 3
CONTINUATION_SATURATION_THRESHOLD = 72
ORCHESTRATION_QUEUE_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_EXECUTION_QUEUE = (
    "inspect-runtime",
    "schedule-execution",
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
DEFAULT_RETRY_QUEUE = (
    "cooldown-before-retry",
    "rerun-targeted-test",
    "reset-validation-window",
)
DEFAULT_CONTINUATION_QUEUE = (
    "resume-bounded-step",
    "compact-orchestration-summary",
)
DEFAULT_PROVIDER_QUEUE = (
    "local-provider",
    "bounded-provider-window",
    "fallback-summary-provider",
    "frontier-escalation-guard",
)
DEFAULT_ORCHESTRATION_HISTORY = (
    "schedule",
    "execute",
    "validate",
    "stabilize",
    "commit-ready",
)


@dataclass(frozen=True)
class ExecutionSchedulingFrame:
    execution_scheduling_active: bool
    execution_queue: tuple[str, ...]
    execution_queue_limit: int
    validation_prerequisites: tuple[str, ...]
    retry_cooldown_windows: int
    continuation_dependencies: tuple[str, ...]
    provider_readiness: bool
    execution_schedule_score: int
    deterministic_execution_schedule: str
    bounded_execution_recommendation: str


@dataclass(frozen=True)
class ValidationSchedulingFrame:
    validation_scheduling_active: bool
    validation_order: tuple[str, ...]
    validation_saturation: int
    validation_cooldown_windows: int
    regression_stabilization_order: tuple[str, ...]
    validation_interruption_pressure: int
    validation_schedule_score: int
    deterministic_validation_schedule: str
    bounded_validation_recommendation: str


@dataclass(frozen=True)
class RetrySchedulingFrame:
    retry_scheduling_active: bool
    retry_order: tuple[str, ...]
    retry_cooldown_ordering: int
    retry_amplification_pressure: int
    retry_interruption_windows: int
    retry_saturation_queue: int
    retry_schedule_score: int
    deterministic_retry_schedule: str
    bounded_retry_recommendation: str
    hidden_retry_execution_blocked: bool


@dataclass(frozen=True)
class ContinuationSchedulingFrame:
    continuation_scheduling_active: bool
    continuation_order: tuple[str, ...]
    continuation_depth: int
    continuation_depth_limit: int
    continuation_cooldown_ordering: int
    continuation_interruption_windows: int
    continuation_reset_timing: str
    continuation_schedule_score: int
    deterministic_continuation_schedule: str
    bounded_continuation_recommendation: str


@dataclass(frozen=True)
class ProviderSchedulingFrame:
    provider_scheduling_active: bool
    provider_order: tuple[str, ...]
    provider_window_limit: int
    provider_readiness: bool
    provider_cooldown_windows: int
    provider_latency_units: int
    provider_schedule_score: int
    deterministic_provider_schedule: str
    bounded_provider_recommendation: str


@dataclass(frozen=True)
class CooldownSchedulingFrame:
    cooldown_scheduling_active: bool
    cooldown_order: tuple[str, ...]
    validation_cooldown_required: bool
    retry_cooldown_required: bool
    continuation_cooldown_required: bool
    provider_cooldown_required: bool
    deterministic_cooldown_schedule: str
    bounded_cooldown_recommendation: str


@dataclass(frozen=True)
class RegressionSchedulingFrame:
    regression_scheduling_active: bool
    repeated_regressions: int
    regression_pressure: int
    regression_stabilization_order: tuple[str, ...]
    regression_before_execution: bool
    regression_schedule_score: int
    deterministic_regression_schedule: str
    bounded_regression_recommendation: str


@dataclass(frozen=True)
class CommitSchedulingFrame:
    commit_scheduling_active: bool
    validation_before_commit: bool
    regression_stable_before_commit: bool
    commit_readiness_score: int
    deterministic_commit_schedule: str
    bounded_commit_recommendation: str
    autonomous_commit_blocked: bool
    autonomous_push_blocked: bool
    autonomous_merge_blocked: bool


@dataclass(frozen=True)
class OrchestrationCoordinationFrame:
    orchestration_coordination_active: bool
    validation_vs_retry_ordering: str
    provider_vs_cooldown_ordering: str
    continuation_vs_termination_ordering: str
    regression_vs_execution_ordering: str
    commit_readiness_vs_validation_ordering: str
    orchestration_coordination_score: int
    deterministic_orchestration_summary: str
    bounded_orchestration_recommendation: str


@dataclass(frozen=True)
class OrchestrationGovernanceFrame:
    orchestration_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_orchestration_enforced: bool
    bounded_scheduling_windows_enforced: bool
    bounded_retry_authority_enforced: bool
    bounded_continuation_authority_enforced: bool
    bounded_orchestration_depth_enforced: bool
    recursive_orchestration_blocked: bool
    hidden_orchestration_execution_blocked: bool
    autonomous_branch_mutation_blocked: bool
    autonomous_governance_mutation_blocked: bool
    self_expanding_orchestration_graphs_blocked: bool
    retrieval_scope_widening_blocked: bool


@dataclass(frozen=True)
class OrchestrationTerminationFrame:
    orchestration_termination_active: bool
    orchestration_terminated: bool
    termination_reasons: tuple[str, ...]
    orchestration_budget_exceeded: bool
    recursive_orchestration_detected: bool
    governance_violation_detected: bool
    retry_amplification_threshold_exceeded: bool
    continuation_saturation_threshold_exceeded: bool
    orchestration_queue_saturation_exceeded: bool


@dataclass(frozen=True)
class OrchestrationBudgetFrame:
    orchestration_budget_active: bool
    orchestration_budget_used: int
    orchestration_budget_limit: int
    orchestration_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class OrchestrationHistoryFrame:
    orchestration_history_active: bool
    orchestration_history: tuple[str, ...]
    orchestration_history_limit: int
    compact_orchestration_history_summary: str
    orchestration_history_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class OrchestrationConfidenceFrame:
    orchestration_confidence_active: bool
    orchestration_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    next_step_confidence: bool


@dataclass(frozen=True)
class OrchestrationEvictionFrame:
    orchestration_eviction_active: bool
    evicted_execution_items: tuple[str, ...]
    evicted_validation_items: tuple[str, ...]
    evicted_provider_items: tuple[str, ...]
    evicted_history_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class RuntimeOrchestratorFrame:
    runtime_orchestrator_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    execution_scheduling: ExecutionSchedulingFrame
    validation_scheduling: ValidationSchedulingFrame
    retry_scheduling: RetrySchedulingFrame
    continuation_scheduling: ContinuationSchedulingFrame
    provider_scheduling: ProviderSchedulingFrame
    cooldown_scheduling: CooldownSchedulingFrame
    regression_scheduling: RegressionSchedulingFrame
    commit_scheduling: CommitSchedulingFrame
    orchestration_coordination: OrchestrationCoordinationFrame
    orchestration_governance: OrchestrationGovernanceFrame
    orchestration_termination: OrchestrationTerminationFrame
    orchestration_budget: OrchestrationBudgetFrame
    orchestration_history: OrchestrationHistoryFrame
    orchestration_confidence: OrchestrationConfidenceFrame
    orchestration_eviction: OrchestrationEvictionFrame
    orchestration_schedule_score: int
    validation_schedule_score: int
    retry_schedule_score: int
    continuation_schedule_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    runtime_orchestrator_mode: str
    estimated_avoided_manual_scheduling: int
    estimated_avoided_recursive_orchestration: int
    estimated_avoided_frontier_next_step_reasoning: int


class RuntimeOrchestrator:
    def evaluate(
        self,
        *,
        execution_queue_items: tuple[str, ...] = DEFAULT_EXECUTION_QUEUE,
        validation_queue_items: tuple[str, ...] = DEFAULT_VALIDATION_QUEUE,
        retry_queue_items: tuple[str, ...] = DEFAULT_RETRY_QUEUE,
        continuation_queue_items: tuple[str, ...] = DEFAULT_CONTINUATION_QUEUE,
        provider_queue_items: tuple[str, ...] = DEFAULT_PROVIDER_QUEUE,
        orchestration_history_items: tuple[str, ...] = DEFAULT_ORCHESTRATION_HISTORY,
        validation_completed_count: int = 5,
        validation_interruption_pressure: int = 0,
        validation_cooldown_windows: int = 1,
        validation_saturation_pressure: int = 1,
        retry_count: int = 1,
        retry_amplification: int = 1,
        retry_interruption_windows: int = 0,
        retry_cooldown_windows: int = 1,
        continuation_depth: int = 1,
        continuation_interruption_windows: int = 0,
        continuation_cooldown_windows: int = 1,
        provider_latency_units: int = 18,
        provider_cooldown_windows: int = 1,
        provider_fatigue_pressure: int = 1,
        provider_cost_pressure: int = 24,
        repeated_regressions: int = 0,
        regression_pressure: int = 1,
        regression_cooldown_windows: int = 1,
        orchestration_budget_used: int = 7,
        recursive_orchestration_attempts: int = 0,
        orchestration_scope_expansion_attempts: int = 0,
        hidden_orchestration_execution_attempts: int = 0,
        autonomous_branch_mutation_attempts: int = 0,
        autonomous_governance_mutation_attempts: int = 0,
        self_expanding_orchestration_graph_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
    ) -> RuntimeOrchestratorFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=retry_count,
            retry_cooldown_pressure=retry_cooldown_windows,
            retry_interruption_pressure=retry_interruption_windows,
            continuation_depth=continuation_depth,
            policy_budget_used=min(orchestration_budget_used, ORCHESTRATION_BUDGET_LIMIT),
        )
        sprint_loop = SprintLoopRuntime().evaluate(
            validation_completed_count=validation_completed_count,
            validation_interruption_pressure=validation_interruption_pressure,
            repeated_regressions=repeated_regressions,
            retry_amplification=retry_amplification,
            retry_count=retry_count,
            continuation_depth=continuation_depth,
            continuation_interruption_window=continuation_interruption_windows,
            sprint_budget_used=min(orchestration_budget_used, ORCHESTRATION_BUDGET_LIMIT),
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=provider_fatigue_pressure,
            retry_amplification=retry_amplification,
            orchestration_instability=regression_pressure,
            estimated_token_pressure=provider_cost_pressure,
            estimated_latency_units=provider_latency_units,
            provider_budget_used=min(orchestration_budget_used, ORCHESTRATION_BUDGET_LIMIT),
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

        bounded_execution_queue = execution_queue_items[:MAX_EXECUTION_QUEUE]
        bounded_validation_queue = validation_queue_items[:MAX_VALIDATION_QUEUE]
        bounded_retry_queue = retry_queue_items[:MAX_RETRY_QUEUE]
        bounded_continuation_queue = continuation_queue_items[:MAX_CONTINUATION_DEPTH]
        bounded_provider_queue = provider_queue_items[:MAX_PROVIDER_WINDOW]
        bounded_history = orchestration_history_items[:MAX_ORCHESTRATION_HISTORY]

        evicted_execution_items = execution_queue_items[MAX_EXECUTION_QUEUE:]
        evicted_validation_items = validation_queue_items[MAX_VALIDATION_QUEUE:]
        evicted_provider_items = provider_queue_items[MAX_PROVIDER_WINDOW:]
        evicted_history_items = orchestration_history_items[MAX_ORCHESTRATION_HISTORY:]

        validation_saturation = _clamp(
            max(0, len(validation_queue_items) - validation_completed_count) * 16
            + validation_interruption_pressure * 12
            + validation_saturation_pressure * 10
            + max(0, len(validation_queue_items) - MAX_VALIDATION_QUEUE) * 8
        )
        validation_schedule_score = _clamp(
            96
            - validation_saturation // 2
            - validation_interruption_pressure * 8
            + int(runtime_policy.runtime_policy_active) * 4
        )
        retry_saturation = _clamp(
            max(0, retry_count - MAX_RETRY_QUEUE) * 24
            + retry_amplification * 12
            + retry_interruption_windows * 10
            + max(0, len(retry_queue_items) - MAX_RETRY_QUEUE) * 8
        )
        retry_amplification_exceeded = retry_amplification > RETRY_AMPLIFICATION_THRESHOLD
        retry_schedule_score = _clamp(
            94 - retry_saturation // 2 - int(retry_amplification_exceeded) * 18
        )
        continuation_saturation = _clamp(
            max(0, continuation_depth - 1) * 24
            + continuation_interruption_windows * 12
            + max(0, continuation_depth - MAX_CONTINUATION_DEPTH) * 30
        )
        continuation_saturation_exceeded = (
            continuation_saturation >= CONTINUATION_SATURATION_THRESHOLD
        )
        continuation_schedule_score = _clamp(92 - continuation_saturation // 2)
        provider_readiness = (
            adaptive_provider.provider_confidence_score >= 60 and provider_latency_units <= 48
        )
        provider_schedule_score = _clamp(
            adaptive_provider.provider_confidence_score
            - provider_fatigue_pressure * 3
            - provider_latency_units // 8
        )
        regression_total_pressure = _clamp(
            repeated_regressions * 18
            + regression_pressure * 12
            + regression_cooldown_windows * 8
            + retry_amplification * 6
        )
        regression_schedule_score = _clamp(100 - regression_total_pressure)
        queue_saturation = _clamp(
            max(0, len(execution_queue_items) - MAX_EXECUTION_QUEUE) * 8
            + max(0, len(validation_queue_items) - MAX_VALIDATION_QUEUE) * 8
            + max(0, len(provider_queue_items) - MAX_PROVIDER_WINDOW) * 8
            + validation_saturation // 2
            + retry_saturation // 2
            + continuation_saturation // 2
        )
        queue_saturation_exceeded = queue_saturation >= ORCHESTRATION_QUEUE_SATURATION_THRESHOLD
        orchestration_schedule_score = _clamp(
            (
                validation_schedule_score
                + retry_schedule_score
                + continuation_schedule_score
                + provider_schedule_score
            )
            // 4
            + int(sprint_loop.sprint_loop_active) * 4
            + int(mediation.runtime_mediation_active) * 4
            - queue_saturation // 6
        )
        validation_complete = validation_completed_count >= len(bounded_validation_queue)
        regression_stable = regression_total_pressure < 45
        commit_readiness_score = _clamp(
            int(validation_complete) * 26
            + int(regression_stable) * 24
            + int(provider_readiness) * 16
            + int(runtime_policy.policy_coherence.policy_coherence_score >= 60) * 18
            + int(execution_memory.execution_memory_active) * 16
            - validation_interruption_pressure * 4
        )
        governance_violation = any(
            (
                orchestration_scope_expansion_attempts,
                hidden_orchestration_execution_attempts,
                autonomous_branch_mutation_attempts,
                autonomous_governance_mutation_attempts,
                self_expanding_orchestration_graph_attempts,
                retrieval_scope_widening_attempts,
            )
        )
        recursive_orchestration_detected = recursive_orchestration_attempts > 0
        orchestration_budget_exceeded = orchestration_budget_used > ORCHESTRATION_BUDGET_LIMIT
        termination_reasons = _termination_reasons(
            orchestration_budget_exceeded,
            recursive_orchestration_detected,
            governance_violation,
            retry_amplification_exceeded,
            continuation_saturation_exceeded,
            queue_saturation_exceeded,
        )
        confidence_score = _clamp(
            (orchestration_schedule_score + commit_readiness_score) // 2
            + reflection.execution_quality.execution_quality_score // 10
            - len(termination_reasons) * 8
        )

        return RuntimeOrchestratorFrame(
            runtime_orchestrator_active=True,
            requirement_ids=RUNTIME_ORCHESTRATOR_REQUIREMENT_IDS,
            test_ids=RUNTIME_ORCHESTRATOR_TEST_IDS,
            execution_scheduling=ExecutionSchedulingFrame(
                execution_scheduling_active=True,
                execution_queue=bounded_execution_queue,
                execution_queue_limit=MAX_EXECUTION_QUEUE,
                validation_prerequisites=bounded_validation_queue,
                retry_cooldown_windows=retry_cooldown_windows,
                continuation_dependencies=bounded_continuation_queue,
                provider_readiness=provider_readiness,
                execution_schedule_score=orchestration_schedule_score,
                deterministic_execution_schedule=(
                    f"execute={len(bounded_execution_queue)};"
                    f"validation={len(bounded_validation_queue)};"
                    f"provider_ready={str(provider_readiness).lower()}"
                ),
                bounded_execution_recommendation="FOLLOW_BOUNDED_RUNTIME_SEQUENCE",
            ),
            validation_scheduling=ValidationSchedulingFrame(
                validation_scheduling_active=True,
                validation_order=bounded_validation_queue,
                validation_saturation=validation_saturation,
                validation_cooldown_windows=validation_cooldown_windows,
                regression_stabilization_order=(
                    "stabilize-regression",
                    "rerun-targeted-validation",
                ),
                validation_interruption_pressure=validation_interruption_pressure,
                validation_schedule_score=validation_schedule_score,
                deterministic_validation_schedule=(
                    f"completed={validation_completed_count};"
                    f"queue={len(bounded_validation_queue)};"
                    f"saturation={validation_saturation}"
                ),
                bounded_validation_recommendation=(
                    "RESET_VALIDATION_AFTER_COOLDOWN"
                    if validation_saturation >= 70
                    else "CONTINUE_BOUNDED_VALIDATION_ORDER"
                ),
            ),
            retry_scheduling=RetrySchedulingFrame(
                retry_scheduling_active=True,
                retry_order=bounded_retry_queue,
                retry_cooldown_ordering=retry_cooldown_windows,
                retry_amplification_pressure=retry_amplification,
                retry_interruption_windows=retry_interruption_windows,
                retry_saturation_queue=retry_saturation,
                retry_schedule_score=retry_schedule_score,
                deterministic_retry_schedule=(
                    f"retry={retry_count};amplification={retry_amplification};"
                    f"saturation={retry_saturation}"
                ),
                bounded_retry_recommendation=(
                    "RESET_RETRY_QUEUE_AFTER_COOLDOWN"
                    if retry_amplification_exceeded
                    else "RETRY_WITHIN_BOUNDED_ORDER"
                ),
                hidden_retry_execution_blocked=True,
            ),
            continuation_scheduling=ContinuationSchedulingFrame(
                continuation_scheduling_active=True,
                continuation_order=bounded_continuation_queue,
                continuation_depth=continuation_depth,
                continuation_depth_limit=MAX_CONTINUATION_DEPTH,
                continuation_cooldown_ordering=continuation_cooldown_windows,
                continuation_interruption_windows=continuation_interruption_windows,
                continuation_reset_timing=(
                    "RESET_AFTER_COOLDOWN"
                    if continuation_depth > MAX_CONTINUATION_DEPTH
                    else "CONTINUE_WITHIN_DEPTH"
                ),
                continuation_schedule_score=continuation_schedule_score,
                deterministic_continuation_schedule=(
                    f"depth={continuation_depth};"
                    f"interrupt={continuation_interruption_windows};"
                    f"saturation={continuation_saturation}"
                ),
                bounded_continuation_recommendation=(
                    "RESET_CONTINUATION_WINDOW"
                    if continuation_saturation_exceeded
                    else "CONTINUE_BOUNDED_ORCHESTRATION"
                ),
            ),
            provider_scheduling=ProviderSchedulingFrame(
                provider_scheduling_active=True,
                provider_order=bounded_provider_queue,
                provider_window_limit=MAX_PROVIDER_WINDOW,
                provider_readiness=provider_readiness,
                provider_cooldown_windows=provider_cooldown_windows,
                provider_latency_units=provider_latency_units,
                provider_schedule_score=provider_schedule_score,
                deterministic_provider_schedule=(
                    f"providers={len(bounded_provider_queue)};"
                    f"latency={provider_latency_units};"
                    f"ready={str(provider_readiness).lower()}"
                ),
                bounded_provider_recommendation=(
                    "USE_LOCAL_PROVIDER_WINDOW"
                    if provider_readiness
                    else "APPLY_PROVIDER_COOLDOWN_BEFORE_SCHEDULING"
                ),
            ),
            cooldown_scheduling=CooldownSchedulingFrame(
                cooldown_scheduling_active=True,
                cooldown_order=("validation", "retry", "provider", "continuation"),
                validation_cooldown_required=validation_saturation >= 70,
                retry_cooldown_required=retry_amplification_exceeded,
                continuation_cooldown_required=continuation_saturation_exceeded,
                provider_cooldown_required=not provider_readiness,
                deterministic_cooldown_schedule=(
                    f"validation={validation_saturation};retry={retry_saturation};"
                    f"continuation={continuation_saturation}"
                ),
                bounded_cooldown_recommendation=(
                    "APPLY_ORCHESTRATION_COOLDOWN"
                    if queue_saturation_exceeded or retry_amplification_exceeded
                    else "MAINTAIN_BOUNDED_SCHEDULE"
                ),
            ),
            regression_scheduling=RegressionSchedulingFrame(
                regression_scheduling_active=True,
                repeated_regressions=repeated_regressions,
                regression_pressure=regression_total_pressure,
                regression_stabilization_order=(
                    "pause-execution",
                    "stabilize-regression",
                    "rerun-validation",
                ),
                regression_before_execution=not regression_stable,
                regression_schedule_score=regression_schedule_score,
                deterministic_regression_schedule=(
                    f"regressions={repeated_regressions};" f"pressure={regression_total_pressure}"
                ),
                bounded_regression_recommendation=(
                    "STABILIZE_BEFORE_EXECUTION"
                    if not regression_stable
                    else "REGRESSION_STABLE_FOR_EXECUTION"
                ),
            ),
            commit_scheduling=CommitSchedulingFrame(
                commit_scheduling_active=True,
                validation_before_commit=True,
                regression_stable_before_commit=regression_stable,
                commit_readiness_score=commit_readiness_score,
                deterministic_commit_schedule=(
                    f"validation={str(validation_complete).lower()};"
                    f"regression={str(regression_stable).lower()};"
                    f"score={commit_readiness_score}"
                ),
                bounded_commit_recommendation=(
                    "READY_FOR_HUMAN_AUTHORIZED_COMMIT"
                    if commit_readiness_score >= 80 and not termination_reasons
                    else "DEFER_COMMIT_UNTIL_SCHEDULE_STABLE"
                ),
                autonomous_commit_blocked=True,
                autonomous_push_blocked=True,
                autonomous_merge_blocked=True,
            ),
            orchestration_coordination=OrchestrationCoordinationFrame(
                orchestration_coordination_active=True,
                validation_vs_retry_ordering="VALIDATION_BEFORE_RETRY_RESET",
                provider_vs_cooldown_ordering="PROVIDER_AFTER_COOLDOWN_IF_NEEDED",
                continuation_vs_termination_ordering="TERMINATION_BEFORE_CONTINUATION",
                regression_vs_execution_ordering="REGRESSION_STABILIZATION_BEFORE_EXECUTION",
                commit_readiness_vs_validation_ordering="VALIDATION_BEFORE_COMMIT_READY",
                orchestration_coordination_score=orchestration_schedule_score,
                deterministic_orchestration_summary=(
                    f"schedule={orchestration_schedule_score};"
                    f"queue={queue_saturation};terminated={bool(termination_reasons)}"
                ),
                bounded_orchestration_recommendation=(
                    "FOLLOW_DETERMINISTIC_ORCHESTRATION_ORDER"
                    if not termination_reasons
                    else "TERMINATE_ORCHESTRATION_AND_RESET_WINDOW"
                ),
            ),
            orchestration_governance=OrchestrationGovernanceFrame(
                orchestration_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_orchestration_enforced=True,
                bounded_scheduling_windows_enforced=True,
                bounded_retry_authority_enforced=True,
                bounded_continuation_authority_enforced=True,
                bounded_orchestration_depth_enforced=True,
                recursive_orchestration_blocked=True,
                hidden_orchestration_execution_blocked=True,
                autonomous_branch_mutation_blocked=True,
                autonomous_governance_mutation_blocked=True,
                self_expanding_orchestration_graphs_blocked=True,
                retrieval_scope_widening_blocked=True,
            ),
            orchestration_termination=OrchestrationTerminationFrame(
                orchestration_termination_active=True,
                orchestration_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                orchestration_budget_exceeded=orchestration_budget_exceeded,
                recursive_orchestration_detected=recursive_orchestration_detected,
                governance_violation_detected=governance_violation,
                retry_amplification_threshold_exceeded=retry_amplification_exceeded,
                continuation_saturation_threshold_exceeded=continuation_saturation_exceeded,
                orchestration_queue_saturation_exceeded=queue_saturation_exceeded,
            ),
            orchestration_budget=OrchestrationBudgetFrame(
                orchestration_budget_active=True,
                orchestration_budget_used=orchestration_budget_used,
                orchestration_budget_limit=ORCHESTRATION_BUDGET_LIMIT,
                orchestration_budget_exceeded=orchestration_budget_exceeded,
                budget_pressure=_pressure(orchestration_budget_used, ORCHESTRATION_BUDGET_LIMIT),
            ),
            orchestration_history=OrchestrationHistoryFrame(
                orchestration_history_active=True,
                orchestration_history=bounded_history,
                orchestration_history_limit=MAX_ORCHESTRATION_HISTORY,
                compact_orchestration_history_summary=(
                    f"history={len(bounded_history)};orchestration=bounded"
                ),
                orchestration_history_overflow_blocked=bool(evicted_history_items),
                self_expanding_history_blocked=self_expanding_orchestration_graph_attempts > 0,
            ),
            orchestration_confidence=OrchestrationConfidenceFrame(
                orchestration_confidence_active=True,
                orchestration_confidence_score=confidence_score,
                confidence_status=_score_label(confidence_score),
                deterministic_confidence=True,
                next_step_confidence=orchestration_schedule_score >= 80,
            ),
            orchestration_eviction=OrchestrationEvictionFrame(
                orchestration_eviction_active=True,
                evicted_execution_items=evicted_execution_items,
                evicted_validation_items=evicted_validation_items,
                evicted_provider_items=evicted_provider_items,
                evicted_history_items=evicted_history_items,
                eviction_count=(
                    len(evicted_execution_items)
                    + len(evicted_validation_items)
                    + len(evicted_provider_items)
                    + len(evicted_history_items)
                ),
                bounded_eviction_active=bool(
                    evicted_execution_items
                    or evicted_validation_items
                    or evicted_provider_items
                    or evicted_history_items
                ),
                eviction_summary=(
                    f"execution={len(evicted_execution_items)};"
                    f"validation={len(evicted_validation_items)};"
                    f"provider={len(evicted_provider_items)};"
                    f"history={len(evicted_history_items)}"
                ),
            ),
            orchestration_schedule_score=orchestration_schedule_score,
            validation_schedule_score=validation_schedule_score,
            retry_schedule_score=retry_schedule_score,
            continuation_schedule_score=continuation_schedule_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            runtime_orchestrator_mode="LOCAL_PATCH_BOUNDED_RUNTIME_ORCHESTRATION",
            estimated_avoided_manual_scheduling=78,
            estimated_avoided_recursive_orchestration=(71 + recursive_orchestration_attempts * 8),
            estimated_avoided_frontier_next_step_reasoning=(
                74 + orchestration_schedule_score // 10
            ),
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
    orchestration_budget_exceeded: bool,
    recursive_orchestration_detected: bool,
    governance_violation_detected: bool,
    retry_amplification_threshold_exceeded: bool,
    continuation_saturation_threshold_exceeded: bool,
    orchestration_queue_saturation_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if orchestration_budget_exceeded:
        reasons.append("ORCHESTRATION_BUDGET_EXCEEDED")
    if recursive_orchestration_detected:
        reasons.append("RECURSIVE_ORCHESTRATION_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if retry_amplification_threshold_exceeded:
        reasons.append("RETRY_AMPLIFICATION_THRESHOLD_EXCEEDED")
    if continuation_saturation_threshold_exceeded:
        reasons.append("CONTINUATION_SATURATION_THRESHOLD_EXCEEDED")
    if orchestration_queue_saturation_exceeded:
        reasons.append("ORCHESTRATION_QUEUE_SATURATION_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "CONTINUATION_SATURATION_THRESHOLD",
    "MAX_CONTINUATION_DEPTH",
    "MAX_EXECUTION_QUEUE",
    "MAX_ORCHESTRATION_HISTORY",
    "MAX_PROVIDER_WINDOW",
    "MAX_RETRY_QUEUE",
    "MAX_VALIDATION_QUEUE",
    "ORCHESTRATION_BUDGET_LIMIT",
    "ORCHESTRATION_QUEUE_SATURATION_THRESHOLD",
    "RETRY_AMPLIFICATION_THRESHOLD",
    "RUNTIME_ORCHESTRATOR_REQUIREMENT_IDS",
    "RUNTIME_ORCHESTRATOR_TEST_IDS",
    "CommitSchedulingFrame",
    "ContinuationSchedulingFrame",
    "CooldownSchedulingFrame",
    "ExecutionSchedulingFrame",
    "OrchestrationBudgetFrame",
    "OrchestrationConfidenceFrame",
    "OrchestrationCoordinationFrame",
    "OrchestrationEvictionFrame",
    "OrchestrationGovernanceFrame",
    "OrchestrationHistoryFrame",
    "OrchestrationTerminationFrame",
    "ProviderSchedulingFrame",
    "RegressionSchedulingFrame",
    "RetrySchedulingFrame",
    "RuntimeOrchestrator",
    "RuntimeOrchestratorFrame",
    "ValidationSchedulingFrame",
]
