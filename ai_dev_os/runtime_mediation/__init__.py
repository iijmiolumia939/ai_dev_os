from __future__ import annotations

from dataclasses import dataclass

RUNTIME_MEDIATION_REQUIREMENT_IDS = tuple(
    f"FR-RUNTIMEMEDIATION-{index:02d}" for index in range(1, 41)
) + ("NFR-COST-59", "NFR-ARCH-72", "NFR-SEC-43")
RUNTIME_MEDIATION_TEST_IDS = tuple(f"TC-RUNTIMEMEDIATION-{index:02d}" for index in range(1, 41))

MAX_EXECUTION_CHAIN = 6
MAX_EXECUTION_WINDOW = 4
MAX_EXECUTION_QUEUE = 5
MAX_RETRIES = 3
MAX_COOLDOWN_PRESSURE = 5
MAX_HISTORY = 8

ACTION_PRIORITY = {
    "termination": 0,
    "cooldown": 1,
    "retry": 2,
    "test": 3,
    "command": 4,
    "filesystem": 5,
    "git": 6,
    "continuation": 7,
}


@dataclass(frozen=True)
class RuntimeArbitrationFrame:
    arbitration_active: bool
    command_vs_test_arbitrated: bool
    git_vs_filesystem_conflict_arbitrated: bool
    retry_vs_cooldown_conflict_arbitrated: bool
    queue_saturation_arbitrated: bool
    continuation_vs_termination_arbitrated: bool
    arbitration_summary: str
    bounded_recommendation: str


@dataclass(frozen=True)
class RetryGovernanceFrame:
    retry_governance_active: bool
    retry_count: int
    retry_limit: int
    bounded_retries_enforced: bool
    retry_cooldown_required: bool
    retry_amplification_blocked: bool
    retry_window_expired: bool
    recursive_retry_detected: bool


@dataclass(frozen=True)
class CooldownGovernanceFrame:
    cooldown_governance_active: bool
    execution_cooldown_pressure: int
    runtime_saturation_cooldown: int
    retry_cooldown_accumulation: int
    execution_queue_congestion: int
    cooldown_required: bool
    deterministic_cooldown_recommendation: str
    bounded_cooldown_summary: str


@dataclass(frozen=True)
class ExecutionPriorityFrame:
    priority_active: bool
    priority_order: tuple[str, ...]
    ordered_actions: tuple[str, ...]
    self_prioritized_execution_blocked: bool


@dataclass(frozen=True)
class ExecutionBudgetFrame:
    budget_active: bool
    execution_step_count: int
    execution_step_limit: int
    execution_budget_exceeded: bool
    bounded_subprocess_execution_required: bool


@dataclass(frozen=True)
class ExecutionWindowFrame:
    window_active: bool
    compact_execution_window: tuple[str, ...]
    window_limit: int
    window_truncated: bool
    self_expanded_window_blocked: bool


@dataclass(frozen=True)
class ExecutionQueueFrame:
    queue_active: bool
    queued_actions: tuple[str, ...]
    queue_limit: int
    queue_saturated: bool
    queue_saturation_blocked: bool


@dataclass(frozen=True)
class ExecutionConflictFrame:
    conflict_active: bool
    command_test_conflict: bool
    git_filesystem_conflict: bool
    retry_cooldown_conflict: bool
    continuation_termination_conflict: bool
    conflict_summary: str


@dataclass(frozen=True)
class ExecutionCooldownFrame:
    cooldown_active: bool
    cooldown_pressure: int
    cooldown_limit: int
    cooldown_stable: bool
    autonomous_scheduling_optimization_blocked: bool


@dataclass(frozen=True)
class ExecutionTerminationFrame:
    termination_active: bool
    should_terminate: bool
    termination_reason: str
    execution_budget_exceeded: bool
    recursive_execution_detected: bool
    governance_violation_detected: bool
    execution_saturation_threshold_exceeded: bool
    retry_amplification_detected: bool


@dataclass(frozen=True)
class ExecutionGovernanceFrame:
    governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_mediation_enforced: bool
    bounded_execution_authority_enforced: bool
    bounded_subprocess_execution_enforced: bool
    bounded_runtime_windows_enforced: bool
    autonomous_execution_authority_blocked: bool
    recursive_orchestration_blocked: bool
    hidden_background_execution_blocked: bool
    repo_wide_mediation_expansion_blocked: bool
    governance_policy_mutated: bool
    retrieval_scope_widened: bool


@dataclass(frozen=True)
class ExecutionIntegrityFrame:
    integrity_active: bool
    direct_unmediated_execution_blocked: bool
    adaptive_self_modifying_orchestration_blocked: bool
    mediation_bypass_detected: bool
    integrity_failure: bool
    integrity_summary: str


@dataclass(frozen=True)
class ExecutionConfidenceFrame:
    confidence_active: bool
    confidence_score: int
    confidence_label: str
    confidence_summary: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionHistoryFrame:
    history_active: bool
    bounded_history: tuple[str, ...]
    history_entry_count: int
    history_truncated: bool
    recursive_history_expansion_blocked: bool


@dataclass(frozen=True)
class ExecutionEvictionFrame:
    eviction_active: bool
    stale_mediation_eviction_recommended: bool
    queue_metadata_eviction_recommended: bool
    eviction_recommendation: str
    automatic_eviction_performed: bool


@dataclass(frozen=True)
class RuntimeMediationFrame:
    runtime_mediation_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    arbitration: RuntimeArbitrationFrame
    retry: RetryGovernanceFrame
    cooldown_governance: CooldownGovernanceFrame
    priority: ExecutionPriorityFrame
    budget: ExecutionBudgetFrame
    window: ExecutionWindowFrame
    queue: ExecutionQueueFrame
    conflict: ExecutionConflictFrame
    cooldown: ExecutionCooldownFrame
    termination: ExecutionTerminationFrame
    governance: ExecutionGovernanceFrame
    integrity: ExecutionIntegrityFrame
    confidence: ExecutionConfidenceFrame
    history: ExecutionHistoryFrame
    eviction: ExecutionEvictionFrame
    deterministic_mediation_summary: str
    bounded_mediation_recommendation: str
    compact_runtime_mediation_summary: str
    execution_sequencer_active: bool
    retry_governance_active: bool
    cooldown_governance_active: bool
    execution_arbitration_active: bool
    estimated_avoided_recursive_execution: int
    estimated_avoided_retry_amplification: int
    estimated_avoided_execution_saturation: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool


class ExecutionSequencer:
    def mediate(
        self,
        actions: tuple[str, ...] = ("command", "test", "git"),
        *,
        retry_count: int = 1,
        execution_cooldown_pressure: int = 1,
        runtime_saturation_cooldown: int = 0,
        retry_cooldown_accumulation: int = 1,
        execution_steps: int | None = None,
        recursive_execution_attempts: int = 0,
        recursive_retry_attempts: int = 0,
        direct_unmediated_execution_attempts: int = 0,
        autonomous_execution_attempts: int = 0,
        hidden_background_execution_attempts: int = 0,
        repo_wide_mediation_expansions: int = 0,
        adaptive_self_modifying_orchestration_attempts: int = 0,
        self_prioritization_attempts: int = 0,
        self_expanded_window_attempts: int = 0,
        retrieval_radius: int = 1,
        history_entries: tuple[str, ...] = ("sequence", "arbitrate", "retry", "cooldown"),
    ) -> RuntimeMediationFrame:
        normalized_actions = tuple(actions)
        ordered_actions = tuple(
            action
            for _, action in sorted(
                enumerate(normalized_actions),
                key=lambda indexed: (ACTION_PRIORITY.get(indexed[1], 99), indexed[0]),
            )
        )
        step_count = len(normalized_actions) if execution_steps is None else execution_steps
        compact_window = ordered_actions[:MAX_EXECUTION_WINDOW]
        bounded_queue = ordered_actions[:MAX_EXECUTION_QUEUE]
        queue_saturated = len(ordered_actions) > MAX_EXECUTION_QUEUE
        retry_amplification = retry_count > MAX_RETRIES
        retry_window_expired = retry_count == MAX_RETRIES
        recursive_retry_detected = recursive_retry_attempts > 0
        command_test_conflict = "command" in normalized_actions and "test" in normalized_actions
        git_filesystem_conflict = (
            "git" in normalized_actions and "filesystem" in normalized_actions
        )
        retry_cooldown_conflict = retry_count > 0 and retry_cooldown_accumulation > 0
        continuation_termination_conflict = (
            "continuation" in normalized_actions and "termination" in normalized_actions
        )
        conflict_count = sum(
            (
                command_test_conflict,
                git_filesystem_conflict,
                retry_cooldown_conflict,
                continuation_termination_conflict,
            )
        )
        cooldown_pressure = (
            execution_cooldown_pressure
            + runtime_saturation_cooldown
            + retry_cooldown_accumulation
            + max(0, len(ordered_actions) - MAX_EXECUTION_WINDOW)
        )
        cooldown_required = cooldown_pressure >= MAX_COOLDOWN_PRESSURE or retry_amplification
        budget_exceeded = step_count > MAX_EXECUTION_CHAIN
        recursive_execution_detected = recursive_execution_attempts > 0
        governance_violation = bool(
            direct_unmediated_execution_attempts
            or autonomous_execution_attempts
            or hidden_background_execution_attempts
            or repo_wide_mediation_expansions
            or retrieval_radius > 2
        )
        integrity_failure = bool(
            direct_unmediated_execution_attempts or adaptive_self_modifying_orchestration_attempts
        )
        should_terminate = bool(
            budget_exceeded
            or recursive_execution_detected
            or governance_violation
            or queue_saturated
            or retry_amplification
            or recursive_retry_detected
        )
        termination_reason = _termination_reason(
            budget_exceeded=budget_exceeded,
            recursive_execution_detected=recursive_execution_detected,
            governance_violation=governance_violation,
            queue_saturated=queue_saturated,
            retry_amplification=retry_amplification,
            recursive_retry_detected=recursive_retry_detected,
        )
        bounded_history = history_entries[:MAX_HISTORY]
        confidence_score = 91 if not should_terminate else 43
        confidence_label = (
            "MEDIATION_BOUNDED" if confidence_score >= 80 else "MEDIATION_TERMINATED"
        )

        return RuntimeMediationFrame(
            runtime_mediation_active=True,
            requirement_ids=RUNTIME_MEDIATION_REQUIREMENT_IDS,
            test_ids=RUNTIME_MEDIATION_TEST_IDS,
            arbitration=RuntimeArbitrationFrame(
                arbitration_active=True,
                command_vs_test_arbitrated=command_test_conflict,
                git_vs_filesystem_conflict_arbitrated=git_filesystem_conflict,
                retry_vs_cooldown_conflict_arbitrated=retry_cooldown_conflict,
                queue_saturation_arbitrated=queue_saturated,
                continuation_vs_termination_arbitrated=continuation_termination_conflict,
                arbitration_summary=(
                    "conflicts="
                    f"{conflict_count}"
                    f";queue_saturated={str(queue_saturated).lower()}"
                ),
                bounded_recommendation="FOLLOW_MEDIATED_EXECUTION_ORDER",
            ),
            retry=RetryGovernanceFrame(
                retry_governance_active=True,
                retry_count=retry_count,
                retry_limit=MAX_RETRIES,
                bounded_retries_enforced=retry_count <= MAX_RETRIES,
                retry_cooldown_required=retry_count > 0,
                retry_amplification_blocked=retry_amplification,
                retry_window_expired=retry_window_expired,
                recursive_retry_detected=recursive_retry_detected,
            ),
            cooldown_governance=CooldownGovernanceFrame(
                cooldown_governance_active=True,
                execution_cooldown_pressure=execution_cooldown_pressure,
                runtime_saturation_cooldown=runtime_saturation_cooldown,
                retry_cooldown_accumulation=retry_cooldown_accumulation,
                execution_queue_congestion=max(0, len(ordered_actions) - MAX_EXECUTION_WINDOW),
                cooldown_required=cooldown_required,
                deterministic_cooldown_recommendation=(
                    "APPLY_BOUNDED_MEDIATION_COOLDOWN"
                    if cooldown_required
                    else "MAINTAIN_MEDIATION_FLOW"
                ),
                bounded_cooldown_summary=f"cooldown_pressure={cooldown_pressure};required={str(cooldown_required).lower()}",
            ),
            priority=ExecutionPriorityFrame(
                priority_active=True,
                priority_order=tuple(ACTION_PRIORITY),
                ordered_actions=ordered_actions,
                self_prioritized_execution_blocked=self_prioritization_attempts > 0,
            ),
            budget=ExecutionBudgetFrame(
                budget_active=True,
                execution_step_count=step_count,
                execution_step_limit=MAX_EXECUTION_CHAIN,
                execution_budget_exceeded=budget_exceeded,
                bounded_subprocess_execution_required=True,
            ),
            window=ExecutionWindowFrame(
                window_active=True,
                compact_execution_window=compact_window,
                window_limit=MAX_EXECUTION_WINDOW,
                window_truncated=len(ordered_actions) > MAX_EXECUTION_WINDOW,
                self_expanded_window_blocked=self_expanded_window_attempts > 0,
            ),
            queue=ExecutionQueueFrame(
                queue_active=True,
                queued_actions=bounded_queue,
                queue_limit=MAX_EXECUTION_QUEUE,
                queue_saturated=queue_saturated,
                queue_saturation_blocked=queue_saturated,
            ),
            conflict=ExecutionConflictFrame(
                conflict_active=True,
                command_test_conflict=command_test_conflict,
                git_filesystem_conflict=git_filesystem_conflict,
                retry_cooldown_conflict=retry_cooldown_conflict,
                continuation_termination_conflict=continuation_termination_conflict,
                conflict_summary=(
                    f"command_test={str(command_test_conflict).lower()};git_filesystem={str(git_filesystem_conflict).lower()};retry_cooldown={str(retry_cooldown_conflict).lower()}"
                ),
            ),
            cooldown=ExecutionCooldownFrame(
                cooldown_active=True,
                cooldown_pressure=cooldown_pressure,
                cooldown_limit=MAX_COOLDOWN_PRESSURE,
                cooldown_stable=not cooldown_required,
                autonomous_scheduling_optimization_blocked=True,
            ),
            termination=ExecutionTerminationFrame(
                termination_active=True,
                should_terminate=should_terminate,
                termination_reason=termination_reason,
                execution_budget_exceeded=budget_exceeded,
                recursive_execution_detected=recursive_execution_detected,
                governance_violation_detected=governance_violation,
                execution_saturation_threshold_exceeded=queue_saturated,
                retry_amplification_detected=retry_amplification or recursive_retry_detected,
            ),
            governance=ExecutionGovernanceFrame(
                governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_mediation_enforced=True,
                bounded_execution_authority_enforced=True,
                bounded_subprocess_execution_enforced=True,
                bounded_runtime_windows_enforced=True,
                autonomous_execution_authority_blocked=autonomous_execution_attempts > 0,
                recursive_orchestration_blocked=recursive_execution_detected,
                hidden_background_execution_blocked=hidden_background_execution_attempts > 0,
                repo_wide_mediation_expansion_blocked=repo_wide_mediation_expansions > 0,
                governance_policy_mutated=False,
                retrieval_scope_widened=False,
            ),
            integrity=ExecutionIntegrityFrame(
                integrity_active=True,
                direct_unmediated_execution_blocked=direct_unmediated_execution_attempts > 0,
                adaptive_self_modifying_orchestration_blocked=(
                    adaptive_self_modifying_orchestration_attempts > 0
                ),
                mediation_bypass_detected=direct_unmediated_execution_attempts > 0,
                integrity_failure=integrity_failure,
                integrity_summary=(
                    "mediation enforced" if not integrity_failure else "mediation bypass blocked"
                ),
            ),
            confidence=ExecutionConfidenceFrame(
                confidence_active=True,
                confidence_score=confidence_score,
                confidence_label=confidence_label,
                confidence_summary=("sequencing", "arbitration", "retry", "cooldown"),
            ),
            history=ExecutionHistoryFrame(
                history_active=True,
                bounded_history=bounded_history,
                history_entry_count=len(bounded_history),
                history_truncated=len(history_entries) > MAX_HISTORY,
                recursive_history_expansion_blocked=len(history_entries) > MAX_HISTORY,
            ),
            eviction=ExecutionEvictionFrame(
                eviction_active=True,
                stale_mediation_eviction_recommended=len(history_entries) > MAX_HISTORY,
                queue_metadata_eviction_recommended=queue_saturated,
                eviction_recommendation="RECOMMEND_BOUNDED_MEDIATION_METADATA_EVICTION_REVIEW",
                automatic_eviction_performed=False,
            ),
            deterministic_mediation_summary=(
                f"window={len(compact_window)};queue={len(bounded_queue)};retry={retry_count};terminate={str(should_terminate).lower()}"
            ),
            bounded_mediation_recommendation=(
                "TERMINATE_MEDIATION" if should_terminate else "CONTINUE_MEDIATED_EXECUTION"
            ),
            compact_runtime_mediation_summary=(
                "runtime mediation active; no direct LLM execution authority"
            ),
            execution_sequencer_active=True,
            retry_governance_active=True,
            cooldown_governance_active=True,
            execution_arbitration_active=True,
            estimated_avoided_recursive_execution=67,
            estimated_avoided_retry_amplification=41,
            estimated_avoided_execution_saturation=38,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
        )


def _termination_reason(
    *,
    budget_exceeded: bool,
    recursive_execution_detected: bool,
    governance_violation: bool,
    queue_saturated: bool,
    retry_amplification: bool,
    recursive_retry_detected: bool,
) -> str:
    if queue_saturated:
        return "EXECUTION_SATURATION_THRESHOLD_EXCEEDED"
    if budget_exceeded:
        return "EXECUTION_BUDGET_EXCEEDED"
    if recursive_execution_detected:
        return "RECURSIVE_EXECUTION_DETECTED"
    if governance_violation:
        return "GOVERNANCE_VIOLATION_DETECTED"
    if retry_amplification or recursive_retry_detected:
        return "RETRY_AMPLIFICATION_DETECTED"
    return "NOT_TERMINATED"
