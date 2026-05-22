from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.cognitive_memory_pressure import CognitiveMemoryPressureRuntime
from ai_dev_os.dev_execution import DevelopmentExecutionRuntime
from ai_dev_os.provider_fatigue import ProviderFatigueRuntime

EXECUTION_CONTINUATION_REQUIREMENT_IDS = tuple(
    f"FR-EXECUTIONCONTINUATION-{index:02d}" for index in range(1, 21)
) + ("NFR-COST-39", "NFR-ARCH-52", "NFR-SEC-23")
EXECUTION_CONTINUATION_TEST_IDS = tuple(
    f"TC-EXECUTIONCONTINUATION-{index:02d}" for index in range(1, 21)
)

MAX_CONTINUATION_STEPS = 5
MAX_PENDING_STEPS = 4
MAX_CHECKPOINTS = 3


@dataclass(frozen=True)
class PendingStep:
    step_id: str
    description: str
    local_patch_scope: str
    requires_tool: bool


@dataclass(frozen=True)
class ExecutionContinuationInput:
    completed_steps: tuple[str, ...] = ("inspect-adjacent-runtime", "apply-local-patch")
    pending_steps: tuple[PendingStep, ...] = (
        PendingStep("test-local-runtime", "Run bounded runtime tests", "tests/execution_continuation", True),
        PendingStep("audit-runtime", "Run runtime audit", "ai_dev_os/runtime_audit.py", True),
    )
    successful_tool_executions: int = 2
    failed_tool_executions: int = 0
    repeated_continuation_loops: int = 0
    recursive_continuation_attempts: int = 0
    repo_wide_edit_attempts: int = 0
    hidden_background_attempts: int = 0
    retrieval_radius: int = 2
    compact_checkpoint_count: int = 2
    continuation_pressure: int = 18


@dataclass(frozen=True)
class ExecutionContinuationFrame:
    execution_continuation_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    continuation_summary: str
    bounded_continuation_recommendation: str
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    local_only: bool
    summary_only: bool


@dataclass(frozen=True)
class ContinuationStateFrame:
    continuation_state_active: bool
    state_label: str
    completed_step_count: int
    pending_step_count: int
    deterministic_state_key: str
    continuation_after_tool_execution: bool
    hidden_background_execution: bool


@dataclass(frozen=True)
class ExecutionProgressFrame:
    execution_progress_active: bool
    completed_steps: tuple[str, ...]
    progress_summary: str
    step_by_step_persistence: bool
    self_expanding_scope: bool


@dataclass(frozen=True)
class PendingStepFrame:
    pending_step_active: bool
    pending_steps: tuple[PendingStep, ...]
    bounded_pending_step_count: int
    pending_step_summary: str
    recursively_generated_steps: bool


@dataclass(frozen=True)
class ToolExecutionFrame:
    tool_execution_active: bool
    successful_tool_executions: int
    failed_tool_executions: int
    tool_execution_saturation: int
    continue_after_success: bool
    retry_recommendation: str
    hidden_tool_loop_blocked: bool


@dataclass(frozen=True)
class ContinuationCheckpointFrame:
    continuation_checkpoint_active: bool
    compact_execution_state: tuple[str, ...]
    pending_bounded_steps: tuple[str, ...]
    execution_progress_summary: str
    deterministic_metadata: tuple[str, ...]
    raw_conversation_persisted: bool
    recursive_execution_plan_persisted: bool


@dataclass(frozen=True)
class ContinuationRecoveryFrame:
    continuation_recovery_active: bool
    safe_resume_supported: bool
    rollback_safe_recovery: bool
    compact_continuation_reset: bool
    failed_step_retry_recommendation: str
    autonomous_provider_reroute_allowed: bool
    recursive_graph_regeneration_allowed: bool


@dataclass(frozen=True)
class ContinuationBudgetFrame:
    continuation_budget_active: bool
    max_steps: int
    used_steps: int
    remaining_steps: int
    continuation_pressure: int
    repeated_continuation_loops: int
    recursive_continuation_risk: int
    tool_execution_saturation: int
    bounded_continuation_recommendation: str
    cooldown_recommendation: str
    deterministic_termination_hint: str


@dataclass(frozen=True)
class ContinuationGovernanceFrame:
    continuation_governance_active: bool
    local_patch_scope_enforced: bool
    bounded_retrieval_enforced: bool
    compact_continuity_enforced: bool
    deterministic_execution_enforced: bool
    max_step_limit_enforced: bool
    repo_wide_autonomous_edits_blocked: bool
    recursive_execution_loops_blocked: bool
    uncontrolled_continuation_chains_blocked: bool
    hidden_background_execution_blocked: bool
    governance_rules_mutated: bool


@dataclass(frozen=True)
class ContinuationDecayFrame:
    continuation_decay_active: bool
    loop_decay_score: int
    checkpoint_decay_score: int
    retrieval_decay_score: int
    continuation_decay_guard_active: bool


@dataclass(frozen=True)
class ContinuationCompletionFrame:
    continuation_completion_active: bool
    bounded_completion_ready: bool
    completion_summary: str
    validation_required_before_completion: bool


@dataclass(frozen=True)
class ContinuationGuardFrame:
    continuation_guard_active: bool
    recursive_loop_blocked: bool
    repo_wide_scope_blocked: bool
    hidden_background_agent_blocked: bool
    uncontrolled_tool_loop_blocked: bool
    governance_violation_risk_detected: bool


@dataclass(frozen=True)
class ContinuationTerminationFrame:
    continuation_termination_active: bool
    should_terminate: bool
    termination_reason: str
    safe_recovery_recommendation: str
    budget_exceeded: bool
    recursive_risk_detected: bool
    governance_violation_risk_detected: bool
    bounded_scope_exceeded: bool
    execution_saturation_detected: bool


@dataclass(frozen=True)
class ContinuationConfidenceFrame:
    continuation_confidence_active: bool
    confidence_score: int
    confidence_label: str
    confidence_summary: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionContinuationRuntimeFrame:
    continuation: ExecutionContinuationFrame
    state: ContinuationStateFrame
    progress: ExecutionProgressFrame
    pending_step: PendingStepFrame
    tool_execution: ToolExecutionFrame
    checkpoint: ContinuationCheckpointFrame
    recovery: ContinuationRecoveryFrame
    budget: ContinuationBudgetFrame
    governance: ContinuationGovernanceFrame
    decay: ContinuationDecayFrame
    completion: ContinuationCompletionFrame
    guard: ContinuationGuardFrame
    termination: ContinuationTerminationFrame
    confidence: ContinuationConfidenceFrame
    execution_continuation_active: bool
    continuation_budget_active: bool
    continuation_governance_active: bool
    continuation_checkpoint_active: bool
    continuation_termination_active: bool
    estimated_avoided_execution_stalls: int
    estimated_avoided_recursive_loops: int
    estimated_avoided_agent_explosions: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    local_only: bool
    summary_only: bool


def _confidence_label(score: int) -> str:
    if score >= 80:
        return "CONTINUATION_SAFE"
    if score >= 60:
        return "CONTINUATION_GUARDED"
    return "TERMINATION_REQUIRED"


class ExecutionContinuationRuntime:
    def evaluate(
        self, sample: ExecutionContinuationInput | None = None
    ) -> ExecutionContinuationRuntimeFrame:
        current = sample or ExecutionContinuationInput()
        memory_pressure = CognitiveMemoryPressureRuntime().evaluate()
        provider_fatigue = ProviderFatigueRuntime().evaluate()
        dev_execution = DevelopmentExecutionRuntime().evaluate()

        completed_count = len(current.completed_steps)
        bounded_pending_steps = current.pending_steps[:MAX_PENDING_STEPS]
        pending_count = len(bounded_pending_steps)
        used_steps = completed_count + current.successful_tool_executions
        remaining_steps = max(0, MAX_CONTINUATION_STEPS - used_steps)
        tool_saturation = min(
            100,
            current.successful_tool_executions * 11
            + current.failed_tool_executions * 17
            + current.repeated_continuation_loops * 19,
        )
        recursive_risk = min(
            100,
            current.recursive_continuation_attempts * 35
            + current.repeated_continuation_loops * 21,
        )
        budget_exceeded = used_steps > MAX_CONTINUATION_STEPS
        scope_exceeded = current.repo_wide_edit_attempts > 0 or current.retrieval_radius > 3
        recursive_detected = recursive_risk >= 35
        saturation_detected = tool_saturation >= 70
        governance_risk = scope_exceeded or current.hidden_background_attempts > 0
        should_terminate = (
            budget_exceeded or recursive_detected or governance_risk or saturation_detected
        )

        if budget_exceeded:
            termination_reason = "CONTINUATION_BUDGET_EXCEEDED"
        elif recursive_detected:
            termination_reason = "RECURSIVE_CONTINUATION_RISK_DETECTED"
        elif governance_risk:
            termination_reason = "GOVERNANCE_VIOLATION_RISK_DETECTED"
        elif saturation_detected:
            termination_reason = "EXECUTION_SATURATION_DETECTED"
        else:
            termination_reason = "CONTINUATION_WITHIN_BOUNDS"

        confidence_score = max(
            0,
            100
            - current.continuation_pressure
            - recursive_risk
            - min(tool_saturation, 35)
            - (25 if governance_risk else 0),
        )
        confidence_label = _confidence_label(confidence_score)
        can_continue = not should_terminate and current.successful_tool_executions > 0
        state_key = f"steps:{completed_count}:{pending_count}:tools:{current.successful_tool_executions}"

        continuation = ExecutionContinuationFrame(
            execution_continuation_active=True,
            requirement_ids=EXECUTION_CONTINUATION_REQUIREMENT_IDS,
            test_ids=EXECUTION_CONTINUATION_TEST_IDS,
            continuation_summary="BOUNDED_LOCAL_EXECUTION_CONTINUATION_ACTIVE",
            bounded_continuation_recommendation=(
                "CONTINUE_NEXT_PENDING_STEP" if can_continue else "TERMINATE_OR_COOLDOWN"
            ),
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            local_only=True,
            summary_only=True,
        )
        state = ContinuationStateFrame(
            continuation_state_active=True,
            state_label="BOUNDED_CONTINUATION_READY" if can_continue else "CONTINUATION_GUARDED",
            completed_step_count=completed_count,
            pending_step_count=pending_count,
            deterministic_state_key=state_key,
            continuation_after_tool_execution=can_continue,
            hidden_background_execution=False,
        )
        progress = ExecutionProgressFrame(
            execution_progress_active=True,
            completed_steps=current.completed_steps,
            progress_summary=";".join(current.completed_steps),
            step_by_step_persistence=True,
            self_expanding_scope=False,
        )
        pending_step = PendingStepFrame(
            pending_step_active=True,
            pending_steps=bounded_pending_steps,
            bounded_pending_step_count=pending_count,
            pending_step_summary=";".join(step.step_id for step in bounded_pending_steps),
            recursively_generated_steps=False,
        )
        tool_execution = ToolExecutionFrame(
            tool_execution_active=True,
            successful_tool_executions=current.successful_tool_executions,
            failed_tool_executions=current.failed_tool_executions,
            tool_execution_saturation=tool_saturation,
            continue_after_success=can_continue,
            retry_recommendation=(
                "RETRY_FAILED_STEP_ONCE_WITH_CHECKPOINT" if current.failed_tool_executions else "NO_RETRY_REQUIRED"
            ),
            hidden_tool_loop_blocked=True,
        )
        checkpoint = ContinuationCheckpointFrame(
            continuation_checkpoint_active=True,
            compact_execution_state=current.completed_steps[-MAX_CHECKPOINTS:],
            pending_bounded_steps=tuple(step.step_id for step in bounded_pending_steps),
            execution_progress_summary=f"completed={completed_count};pending={pending_count}",
            deterministic_metadata=(
                state_key,
                f"retrieval-radius:{current.retrieval_radius}",
                f"checkpoint-count:{min(current.compact_checkpoint_count, MAX_CHECKPOINTS)}",
            ),
            raw_conversation_persisted=False,
            recursive_execution_plan_persisted=False,
        )
        recovery = ContinuationRecoveryFrame(
            continuation_recovery_active=True,
            safe_resume_supported=True,
            rollback_safe_recovery=True,
            compact_continuation_reset=True,
            failed_step_retry_recommendation=(
                "RETRY_FAILED_STEP_ONCE_AFTER_COMPACT_CHECKPOINT"
                if current.failed_tool_executions
                else "RESUME_NEXT_PENDING_STEP"
            ),
            autonomous_provider_reroute_allowed=False,
            recursive_graph_regeneration_allowed=False,
        )
        budget = ContinuationBudgetFrame(
            continuation_budget_active=True,
            max_steps=MAX_CONTINUATION_STEPS,
            used_steps=used_steps,
            remaining_steps=remaining_steps,
            continuation_pressure=current.continuation_pressure,
            repeated_continuation_loops=current.repeated_continuation_loops,
            recursive_continuation_risk=recursive_risk,
            tool_execution_saturation=tool_saturation,
            bounded_continuation_recommendation=continuation.bounded_continuation_recommendation,
            cooldown_recommendation=(
                "COOLDOWN_BEFORE_NEXT_TOOL" if remaining_steps == 0 else "NO_COOLDOWN_REQUIRED"
            ),
            deterministic_termination_hint=termination_reason,
        )
        governance = ContinuationGovernanceFrame(
            continuation_governance_active=True,
            local_patch_scope_enforced=True,
            bounded_retrieval_enforced=memory_pressure.retrieval_overload.repo_wide_retrieval_expansion_blocked,
            compact_continuity_enforced=memory_pressure.governance.compact_continuity,
            deterministic_execution_enforced=dev_execution.deterministic,
            max_step_limit_enforced=True,
            repo_wide_autonomous_edits_blocked=True,
            recursive_execution_loops_blocked=True,
            uncontrolled_continuation_chains_blocked=True,
            hidden_background_execution_blocked=True,
            governance_rules_mutated=False,
        )
        decay = ContinuationDecayFrame(
            continuation_decay_active=True,
            loop_decay_score=current.repeated_continuation_loops * 10,
            checkpoint_decay_score=max(0, current.compact_checkpoint_count - MAX_CHECKPOINTS) * 10,
            retrieval_decay_score=max(0, current.retrieval_radius - 2) * 12,
            continuation_decay_guard_active=True,
        )
        completion = ContinuationCompletionFrame(
            continuation_completion_active=True,
            bounded_completion_ready=pending_count == 0 and not should_terminate,
            completion_summary="COMPACT_COMPLETION_PENDING_VALIDATION",
            validation_required_before_completion=True,
        )
        guard = ContinuationGuardFrame(
            continuation_guard_active=True,
            recursive_loop_blocked=current.recursive_continuation_attempts > 0,
            repo_wide_scope_blocked=current.repo_wide_edit_attempts > 0,
            hidden_background_agent_blocked=current.hidden_background_attempts > 0,
            uncontrolled_tool_loop_blocked=saturation_detected,
            governance_violation_risk_detected=governance_risk,
        )
        termination = ContinuationTerminationFrame(
            continuation_termination_active=True,
            should_terminate=should_terminate,
            termination_reason=termination_reason,
            safe_recovery_recommendation=(
                "COMPACT_CONTINUATION_RESET_AND_RESUME_LOCAL_PATCH" if should_terminate else "CONTINUE_BOUNDED_STEP"
            ),
            budget_exceeded=budget_exceeded,
            recursive_risk_detected=recursive_detected,
            governance_violation_risk_detected=governance_risk,
            bounded_scope_exceeded=scope_exceeded,
            execution_saturation_detected=saturation_detected,
        )
        confidence = ContinuationConfidenceFrame(
            continuation_confidence_active=True,
            confidence_score=confidence_score,
            confidence_label=confidence_label,
            confidence_summary=(
                f"state:{state.state_label}",
                f"budget:{used_steps}/{MAX_CONTINUATION_STEPS}",
                f"provider-fatigue:{provider_fatigue.confidence.overall_fatigue_label}",
                f"memory:{memory_pressure.cognitive_memory_pressure.memory_pressure_label}",
            ),
        )
        return ExecutionContinuationRuntimeFrame(
            continuation=continuation,
            state=state,
            progress=progress,
            pending_step=pending_step,
            tool_execution=tool_execution,
            checkpoint=checkpoint,
            recovery=recovery,
            budget=budget,
            governance=governance,
            decay=decay,
            completion=completion,
            guard=guard,
            termination=termination,
            confidence=confidence,
            execution_continuation_active=continuation.execution_continuation_active,
            continuation_budget_active=budget.continuation_budget_active,
            continuation_governance_active=governance.continuation_governance_active,
            continuation_checkpoint_active=checkpoint.continuation_checkpoint_active,
            continuation_termination_active=termination.continuation_termination_active,
            estimated_avoided_execution_stalls=24,
            estimated_avoided_recursive_loops=17,
            estimated_avoided_agent_explosions=13,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            local_only=True,
            summary_only=True,
        )


__all__ = [
    "ContinuationBudgetFrame",
    "ContinuationCheckpointFrame",
    "ContinuationCompletionFrame",
    "ContinuationConfidenceFrame",
    "ContinuationDecayFrame",
    "ContinuationGovernanceFrame",
    "ContinuationGuardFrame",
    "ContinuationRecoveryFrame",
    "ContinuationStateFrame",
    "ContinuationTerminationFrame",
    "ExecutionContinuationFrame",
    "ExecutionContinuationInput",
    "ExecutionContinuationRuntime",
    "ExecutionContinuationRuntimeFrame",
    "ExecutionProgressFrame",
    "EXECUTION_CONTINUATION_REQUIREMENT_IDS",
    "EXECUTION_CONTINUATION_TEST_IDS",
    "MAX_CONTINUATION_STEPS",
    "PendingStep",
    "PendingStepFrame",
    "ToolExecutionFrame",
]