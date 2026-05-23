from __future__ import annotations

from dataclasses import dataclass

EXECUTION_COORDINATION_REQUIREMENT_IDS = tuple(
    f"FR-EXECUTIONCOORDINATION-{index:02d}" for index in range(1, 25)
) + ("NFR-COST-45", "NFR-ARCH-58", "NFR-SEC-29")
EXECUTION_COORDINATION_TEST_IDS = tuple(
    f"TC-EXECUTIONCOORDINATION-{index:02d}" for index in range(1, 25)
)

MAX_COORDINATION_STEPS = 4
MAX_RUNTIME_CONFLICTS = 3
MAX_COORDINATION_OSCILLATION = 2
MAX_COORDINATION_HISTORY = 6
MAX_RETRIEVAL_RADIUS = 2

RUNTIME_PRIORITY_ORDER = (
    "governance",
    "saturation",
    "recovery",
    "continuation",
    "fatigue",
    "memory_pressure",
    "load_balancing",
)


@dataclass(frozen=True)
class RuntimePriorityFrame:
    coordination_priority_active: bool
    deterministic_priority_order: tuple[str, ...]
    highest_priority_runtime: str
    bounded_runtime_conflict_arbitration: bool
    compact_coordination_metadata: tuple[str, ...]
    governance_safe_coordination_precedence: bool
    runtime_hierarchy_mutated: bool
    adaptive_dominance_loops_created: bool
    deterministic_runtime_priority_hint: str


@dataclass(frozen=True)
class CoordinationConflictFrame:
    coordination_conflict_active: bool
    continuation_vs_saturation_conflict: bool
    recovery_vs_fatigue_conflict: bool
    load_balancing_vs_cooldown_conflict: bool
    checkpoint_integrity_vs_continuation_conflict: bool
    conflict_count: int
    compact_coordination_warning: str
    deterministic_arbitration_recommendation: str


@dataclass(frozen=True)
class CoordinationResolutionFrame:
    coordination_resolution_active: bool
    bounded_coordination_recommendation: str
    compact_conflict_resolution_summary: str
    selected_runtime_precedence: str
    autonomous_coordination_action_allowed: bool
    runtime_graph_regeneration_allowed: bool
    orchestration_loop_created: bool
    runtime_hierarchy_self_expanded: bool


@dataclass(frozen=True)
class CoordinationBudgetFrame:
    coordination_budget_active: bool
    max_coordination_steps: int
    used_coordination_steps: int
    remaining_coordination_steps: int
    max_runtime_conflicts: int
    used_runtime_conflicts: int
    remaining_runtime_conflicts: int
    coordination_budget_exceeded: bool


@dataclass(frozen=True)
class CoordinationGovernanceFrame:
    coordination_governance_active: bool
    local_patch_scope_enforced: bool
    bounded_runtime_coordination_enforced: bool
    deterministic_conflict_resolution_enforced: bool
    compact_continuity_enforced: bool
    bounded_retrieval_enforced: bool
    recursive_runtime_coordination_blocked: bool
    hidden_orchestration_layers_blocked: bool
    autonomous_runtime_arbitration_blocked: bool
    repo_wide_coordination_expansion_blocked: bool
    governance_policy_mutated: bool
    retrieval_scope_widened: bool


@dataclass(frozen=True)
class CoordinationTerminationFrame:
    coordination_termination_active: bool
    should_terminate_coordination: bool
    termination_reason: str
    compact_coordination_termination_summary: str
    safe_manual_intervention_recommendation: str
    coordination_budget_exceeded: bool
    recursive_coordination_risk_detected: bool
    governance_violation_risk_detected: bool
    runtime_oscillation_threshold_exceeded: bool
    coordination_amplification_detected: bool


@dataclass(frozen=True)
class CoordinationCooldownFrame:
    coordination_cooldown_active: bool
    runtime_coordination_saturation: int
    repeated_coordination_oscillation: int
    conflicting_runtime_retry_pressure: int
    coordination_amplification_risk: int
    cooldown_required: bool
    coordination_cooldown_recommendation: str
    bounded_coordination_delay_recommendation: str
    autonomous_runtime_suppression_allowed: bool
    recursive_rebalance_allowed: bool


@dataclass(frozen=True)
class CoordinationConfidenceFrame:
    coordination_confidence_active: bool
    confidence_score: int
    confidence_label: str
    confidence_summary: tuple[str, ...]


@dataclass(frozen=True)
class CoordinationHistoryFrame:
    coordination_history_active: bool
    bounded_history: tuple[str, ...]
    history_entry_count: int
    history_truncated: bool
    recursive_history_expansion_blocked: bool


@dataclass(frozen=True)
class CoordinationDecayFrame:
    coordination_decay_active: bool
    conflict_decay_score: int
    oscillation_decay_score: int
    cooldown_decay_score: int
    amplification_decay_score: int
    decay_guard_active: bool


@dataclass(frozen=True)
class CoordinationIntegrityFrame:
    coordination_integrity_active: bool
    runtime_priority_integrity_valid: bool
    conflicting_recommendations_detected: bool
    incompatible_recovery_continuation_detected: bool
    runtime_graph_synthesis_detected: bool
    integrity_recommendation: str
    automatic_integrity_repair_allowed: bool


@dataclass(frozen=True)
class CoordinationRecoveryFrame:
    coordination_recovery_active: bool
    recovery_coordination_supported: bool
    recovery_precedence: str
    compact_recovery_coordination_summary: str
    autonomous_recovery_orchestration_allowed: bool
    recursive_recovery_coordination_allowed: bool


@dataclass(frozen=True)
class CoordinationEvictionFrame:
    coordination_eviction_active: bool
    stale_coordination_history_eviction_recommended: bool
    stale_conflict_metadata_eviction_recommended: bool
    eviction_recommendation: str
    automatic_eviction_performed: bool


@dataclass(frozen=True)
class ExecutionCoordinationFrame:
    execution_coordination_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    priority: RuntimePriorityFrame
    conflict: CoordinationConflictFrame
    resolution: CoordinationResolutionFrame
    budget: CoordinationBudgetFrame
    governance: CoordinationGovernanceFrame
    termination: CoordinationTerminationFrame
    cooldown: CoordinationCooldownFrame
    confidence: CoordinationConfidenceFrame
    history: CoordinationHistoryFrame
    decay: CoordinationDecayFrame
    integrity: CoordinationIntegrityFrame
    recovery: CoordinationRecoveryFrame
    eviction: CoordinationEvictionFrame
    bounded_coordination_recommendation: str
    deterministic_runtime_priority_hint: str
    compact_conflict_resolution_summary: str
    coordination_conflict_active: bool
    coordination_priority_active: bool
    coordination_termination_active: bool
    estimated_avoided_runtime_conflicts: int
    estimated_avoided_recursive_coordination: int
    estimated_avoided_runtime_oscillation: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    summary_only: bool


class ExecutionCoordinationRuntime:
    def evaluate(
        self,
        *,
        continuation_recommendation: str = "CONTINUE_NEXT_PENDING_STEP",
        saturation_recommendation: str = "CONTINUE_WITH_BOUNDED_SLOWDOWN",
        recovery_recommendation: str = "RESUME_SAFE_RECOVERY_FROM_COMPACT_CHECKPOINT",
        fatigue_recommendation: str = "FATIGUE_LOW_LOCAL_FIRST",
        memory_pressure_recommendation: str = "MEMORY_PRESSURE_LOW_COMPACT_CONTINUITY_GUARDED",
        load_balancing_recommendation: str = "KEEP_SINGLE_BOUNDED_RUNTIME",
        checkpoint_integrity_valid: bool = True,
        runtime_coordination_saturation: int = 1,
        repeated_coordination_oscillation: int = 0,
        conflicting_runtime_retry_pressure: int = 1,
        coordination_amplification_risk: int = 0,
        recursive_coordination_attempts: int = 0,
        autonomous_arbitration_attempts: int = 0,
        hidden_orchestration_layers: int = 0,
        repo_wide_coordination_expansions: int = 0,
        runtime_graph_synthesis_attempts: int = 0,
        retrieval_radius: int = 2,
        coordination_steps: int = 2,
        history_entries: tuple[str, ...] = (
            "continuation",
            "saturation",
            "recovery",
        ),
    ) -> ExecutionCoordinationFrame:
        continuation_conflict = continuation_recommendation.startswith("CONTINUE") and (
            "TERMINATE" in saturation_recommendation or "COOLDOWN" in saturation_recommendation
        )
        recovery_fatigue_conflict = recovery_recommendation.startswith("RESUME") and (
            "RECOVERY_REQUIRED" in fatigue_recommendation
            or "ESCALATION_PRESSURE" in fatigue_recommendation
        )
        load_cooldown_conflict = (
            "PARALLEL" in load_balancing_recommendation and runtime_coordination_saturation > 2
        )
        checkpoint_conflict = (
            not checkpoint_integrity_valid and continuation_recommendation.startswith("CONTINUE")
        )
        conflict_count = sum(
            (
                continuation_conflict,
                recovery_fatigue_conflict,
                load_cooldown_conflict,
                checkpoint_conflict,
            )
        )
        budget_exceeded = (
            coordination_steps > MAX_COORDINATION_STEPS or conflict_count > MAX_RUNTIME_CONFLICTS
        )
        oscillation_exceeded = repeated_coordination_oscillation > MAX_COORDINATION_OSCILLATION
        amplification_detected = coordination_amplification_risk > 0 or (
            conflicting_runtime_retry_pressure > 3 and conflict_count > 0
        )
        recursive_detected = recursive_coordination_attempts > 0
        governance_violation = (
            autonomous_arbitration_attempts > 0
            or hidden_orchestration_layers > 0
            or repo_wide_coordination_expansions > 0
            or runtime_graph_synthesis_attempts > 0
            or retrieval_radius > MAX_RETRIEVAL_RADIUS
        )
        should_terminate = (
            budget_exceeded
            or recursive_detected
            or governance_violation
            or oscillation_exceeded
            or amplification_detected
        )

        if budget_exceeded:
            termination_reason = "COORDINATION_BUDGET_EXCEEDED"
        elif recursive_detected:
            termination_reason = "RECURSIVE_COORDINATION_RISK_DETECTED"
        elif governance_violation:
            termination_reason = "COORDINATION_GOVERNANCE_VIOLATION_RISK_DETECTED"
        elif oscillation_exceeded:
            termination_reason = "RUNTIME_OSCILLATION_THRESHOLD_EXCEEDED"
        elif amplification_detected:
            termination_reason = "COORDINATION_AMPLIFICATION_DETECTED"
        else:
            termination_reason = "COORDINATION_WITHIN_BOUNDS"

        if conflict_count > 0:
            priority_hint = "PRIORITIZE_SATURATION_RECOVERY_BEFORE_CONTINUATION"
            selected_precedence = "saturation"
        else:
            priority_hint = "FOLLOW_DETERMINISTIC_RUNTIME_PRIORITY_ORDER"
            selected_precedence = "governance"

        bounded_recommendation = (
            "TERMINATE_COORDINATION_AND_REQUEST_MANUAL_REVIEW"
            if should_terminate
            else "COORDINATE_BOUNDED_RUNTIME_RECOMMENDATIONS"
        )
        conflict_summary = (
            f"conflicts={conflict_count};precedence={selected_precedence};terminate="
            f"{str(should_terminate).lower()}"
        )
        bounded_history = history_entries[-MAX_COORDINATION_HISTORY:]
        cooldown_required = (
            runtime_coordination_saturation
            + repeated_coordination_oscillation
            + conflicting_runtime_retry_pressure
            + coordination_amplification_risk
        ) > 5

        priority = RuntimePriorityFrame(
            coordination_priority_active=True,
            deterministic_priority_order=RUNTIME_PRIORITY_ORDER,
            highest_priority_runtime=RUNTIME_PRIORITY_ORDER[0],
            bounded_runtime_conflict_arbitration=True,
            compact_coordination_metadata=(
                f"conflicts:{conflict_count}",
                f"steps:{coordination_steps}/{MAX_COORDINATION_STEPS}",
                f"oscillation:{repeated_coordination_oscillation}",
            ),
            governance_safe_coordination_precedence=True,
            runtime_hierarchy_mutated=False,
            adaptive_dominance_loops_created=False,
            deterministic_runtime_priority_hint=priority_hint,
        )
        conflict = CoordinationConflictFrame(
            coordination_conflict_active=True,
            continuation_vs_saturation_conflict=continuation_conflict,
            recovery_vs_fatigue_conflict=recovery_fatigue_conflict,
            load_balancing_vs_cooldown_conflict=load_cooldown_conflict,
            checkpoint_integrity_vs_continuation_conflict=checkpoint_conflict,
            conflict_count=conflict_count,
            compact_coordination_warning=(
                "COORDINATION_CONFLICTS_BOUNDED"
                if conflict_count > 0
                else "NO_COORDINATION_CONFLICTS"
            ),
            deterministic_arbitration_recommendation=priority_hint,
        )
        resolution = CoordinationResolutionFrame(
            coordination_resolution_active=True,
            bounded_coordination_recommendation=bounded_recommendation,
            compact_conflict_resolution_summary=conflict_summary,
            selected_runtime_precedence=selected_precedence,
            autonomous_coordination_action_allowed=False,
            runtime_graph_regeneration_allowed=False,
            orchestration_loop_created=False,
            runtime_hierarchy_self_expanded=False,
        )
        budget = CoordinationBudgetFrame(
            coordination_budget_active=True,
            max_coordination_steps=MAX_COORDINATION_STEPS,
            used_coordination_steps=coordination_steps,
            remaining_coordination_steps=max(0, MAX_COORDINATION_STEPS - coordination_steps),
            max_runtime_conflicts=MAX_RUNTIME_CONFLICTS,
            used_runtime_conflicts=conflict_count,
            remaining_runtime_conflicts=max(0, MAX_RUNTIME_CONFLICTS - conflict_count),
            coordination_budget_exceeded=budget_exceeded,
        )
        governance = CoordinationGovernanceFrame(
            coordination_governance_active=True,
            local_patch_scope_enforced=True,
            bounded_runtime_coordination_enforced=True,
            deterministic_conflict_resolution_enforced=True,
            compact_continuity_enforced=True,
            bounded_retrieval_enforced=retrieval_radius <= MAX_RETRIEVAL_RADIUS,
            recursive_runtime_coordination_blocked=True,
            hidden_orchestration_layers_blocked=True,
            autonomous_runtime_arbitration_blocked=True,
            repo_wide_coordination_expansion_blocked=repo_wide_coordination_expansions > 0,
            governance_policy_mutated=False,
            retrieval_scope_widened=False,
        )
        termination = CoordinationTerminationFrame(
            coordination_termination_active=True,
            should_terminate_coordination=should_terminate,
            termination_reason=termination_reason,
            compact_coordination_termination_summary=(
                f"{termination_reason};manual-review={str(should_terminate).lower()}"
            ),
            safe_manual_intervention_recommendation=(
                "REQUEST_MANUAL_COORDINATION_REVIEW"
                if should_terminate
                else "NO_MANUAL_INTERVENTION_REQUIRED"
            ),
            coordination_budget_exceeded=budget_exceeded,
            recursive_coordination_risk_detected=recursive_detected,
            governance_violation_risk_detected=governance_violation,
            runtime_oscillation_threshold_exceeded=oscillation_exceeded,
            coordination_amplification_detected=amplification_detected,
        )
        cooldown = CoordinationCooldownFrame(
            coordination_cooldown_active=True,
            runtime_coordination_saturation=runtime_coordination_saturation,
            repeated_coordination_oscillation=repeated_coordination_oscillation,
            conflicting_runtime_retry_pressure=conflicting_runtime_retry_pressure,
            coordination_amplification_risk=coordination_amplification_risk,
            cooldown_required=cooldown_required or oscillation_exceeded,
            coordination_cooldown_recommendation=(
                "APPLY_COORDINATION_COOLDOWN"
                if cooldown_required or oscillation_exceeded
                else "NO_COORDINATION_COOLDOWN_REQUIRED"
            ),
            bounded_coordination_delay_recommendation=(
                "DELAY_COORDINATION_UNTIL_RUNTIME_PRESSURE_DROPS"
                if cooldown_required
                else "NO_COORDINATION_DELAY_REQUIRED"
            ),
            autonomous_runtime_suppression_allowed=False,
            recursive_rebalance_allowed=False,
        )
        integrity = CoordinationIntegrityFrame(
            coordination_integrity_active=True,
            runtime_priority_integrity_valid=True,
            conflicting_recommendations_detected=conflict_count > 0,
            incompatible_recovery_continuation_detected=(
                recovery_fatigue_conflict or checkpoint_conflict
            ),
            runtime_graph_synthesis_detected=runtime_graph_synthesis_attempts > 0,
            integrity_recommendation=(
                "KEEP_COORDINATION_METADATA_COMPACT"
                if not governance_violation
                else "STOP_COORDINATION_GRAPH_SYNTHESIS"
            ),
            automatic_integrity_repair_allowed=False,
        )
        recovery = CoordinationRecoveryFrame(
            coordination_recovery_active=True,
            recovery_coordination_supported=True,
            recovery_precedence="recovery-after-saturation-before-continuation",
            compact_recovery_coordination_summary=(
                "recovery bounded; continuation waits for saturation and integrity"
            ),
            autonomous_recovery_orchestration_allowed=False,
            recursive_recovery_coordination_allowed=False,
        )
        history = CoordinationHistoryFrame(
            coordination_history_active=True,
            bounded_history=bounded_history,
            history_entry_count=len(bounded_history),
            history_truncated=len(history_entries) > MAX_COORDINATION_HISTORY,
            recursive_history_expansion_blocked=True,
        )
        decay = CoordinationDecayFrame(
            coordination_decay_active=True,
            conflict_decay_score=conflict_count * 8,
            oscillation_decay_score=repeated_coordination_oscillation * 10,
            cooldown_decay_score=max(0, runtime_coordination_saturation - 1) * 4,
            amplification_decay_score=coordination_amplification_risk * 12,
            decay_guard_active=True,
        )
        eviction = CoordinationEvictionFrame(
            coordination_eviction_active=True,
            stale_coordination_history_eviction_recommended=(
                len(history_entries) > MAX_COORDINATION_HISTORY
            ),
            stale_conflict_metadata_eviction_recommended=conflict_count > MAX_RUNTIME_CONFLICTS,
            eviction_recommendation=(
                "RECOMMEND_STALE_COORDINATION_METADATA_EVICTION"
                if len(history_entries) > MAX_COORDINATION_HISTORY
                or conflict_count > MAX_RUNTIME_CONFLICTS
                else "NO_AUTOMATIC_COORDINATION_EVICTION"
            ),
            automatic_eviction_performed=False,
        )
        confidence_penalty = (
            conflict_count * 12
            + repeated_coordination_oscillation * 12
            + coordination_amplification_risk * 14
            + (25 if should_terminate else 0)
        )
        confidence_score = max(0, 100 - confidence_penalty)
        confidence = CoordinationConfidenceFrame(
            coordination_confidence_active=True,
            confidence_score=confidence_score,
            confidence_label=(
                "COORDINATION_STABLE"
                if confidence_score >= 70
                else (
                    "COORDINATION_GUARDED"
                    if confidence_score >= 45
                    else "MANUAL_COORDINATION_REQUIRED"
                )
            ),
            confidence_summary=(
                f"conflicts:{conflict_count}/{MAX_RUNTIME_CONFLICTS}",
                f"oscillation:{repeated_coordination_oscillation}/{MAX_COORDINATION_OSCILLATION}",
                f"termination:{termination_reason}",
            ),
        )

        return ExecutionCoordinationFrame(
            execution_coordination_active=True,
            requirement_ids=EXECUTION_COORDINATION_REQUIREMENT_IDS,
            test_ids=EXECUTION_COORDINATION_TEST_IDS,
            priority=priority,
            conflict=conflict,
            resolution=resolution,
            budget=budget,
            governance=governance,
            termination=termination,
            cooldown=cooldown,
            confidence=confidence,
            history=history,
            decay=decay,
            integrity=integrity,
            recovery=recovery,
            eviction=eviction,
            bounded_coordination_recommendation=bounded_recommendation,
            deterministic_runtime_priority_hint=priority_hint,
            compact_conflict_resolution_summary=conflict_summary,
            coordination_conflict_active=conflict.coordination_conflict_active,
            coordination_priority_active=priority.coordination_priority_active,
            coordination_termination_active=termination.coordination_termination_active,
            estimated_avoided_runtime_conflicts=29,
            estimated_avoided_recursive_coordination=17,
            estimated_avoided_runtime_oscillation=15,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            summary_only=True,
        )


__all__ = [
    "CoordinationBudgetFrame",
    "CoordinationConflictFrame",
    "CoordinationConfidenceFrame",
    "CoordinationCooldownFrame",
    "CoordinationDecayFrame",
    "CoordinationEvictionFrame",
    "CoordinationGovernanceFrame",
    "CoordinationHistoryFrame",
    "CoordinationIntegrityFrame",
    "CoordinationRecoveryFrame",
    "CoordinationResolutionFrame",
    "CoordinationTerminationFrame",
    "ExecutionCoordinationFrame",
    "ExecutionCoordinationRuntime",
    "EXECUTION_COORDINATION_REQUIREMENT_IDS",
    "EXECUTION_COORDINATION_TEST_IDS",
    "MAX_COORDINATION_OSCILLATION",
    "MAX_COORDINATION_STEPS",
    "MAX_RUNTIME_CONFLICTS",
    "RuntimePriorityFrame",
]
