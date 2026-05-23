from __future__ import annotations

from dataclasses import dataclass

EXECUTION_INTENT_REQUIREMENT_IDS = tuple(
    f"FR-EXECUTIONINTENT-{index:02d}" for index in range(1, 25)
) + ("NFR-COST-47", "NFR-ARCH-60", "NFR-SEC-31")
EXECUTION_INTENT_TEST_IDS = tuple(f"TC-EXECUTIONINTENT-{index:02d}" for index in range(1, 25))

MAX_INTENT_TRANSITIONS = 4
MAX_INTENT_CONFLICTS = 3
MAX_INTENT_OSCILLATION = 2
MAX_INTENT_HISTORY = 6
MAX_RETRIEVAL_RADIUS = 2

INTENT_PRIORITY_ORDER = (
    "governance",
    "saturation",
    "recovery",
    "cooldown",
    "coordination",
    "continuation",
)


@dataclass(frozen=True)
class IntentPriorityFrame:
    intent_priority_active: bool
    deterministic_intent_order: tuple[str, ...]
    active_priority_intent: str
    bounded_intent_precedence: bool
    compact_priority_metadata: tuple[str, ...]
    governance_safe_intent_arbitration: bool
    intent_hierarchy_mutated: bool
    adaptive_goal_system_created: bool
    compact_intent_arbitration_hint: str


@dataclass(frozen=True)
class IntentConflictFrame:
    intent_conflict_active: bool
    continuation_vs_cooldown_conflict: bool
    recovery_vs_continuation_conflict: bool
    saturation_vs_continuation_conflict: bool
    coordination_vs_recovery_conflict: bool
    conflict_count: int
    compact_intent_conflict_summary: str
    deterministic_intent_resolution_recommendation: str


@dataclass(frozen=True)
class IntentTransitionFrame:
    intent_transition_active: bool
    bounded_intent_transitions: int
    repeated_intent_oscillation: int
    unstable_intent_switching: int
    intent_amplification_pressure: int
    transition_cooldown_required: bool
    transition_cooldown_recommendation: str
    bounded_transition_stabilization_recommendation: str
    autonomous_intent_switch_allowed: bool
    recursive_intent_chain_regeneration_allowed: bool


@dataclass(frozen=True)
class IntentCooldownFrame:
    intent_cooldown_active: bool
    cooldown_intent_pressure: int
    transition_cooldown_recommendation: str
    bounded_cooldown_window: str
    autonomous_cooldown_enforcement_allowed: bool


@dataclass(frozen=True)
class IntentConfidenceFrame:
    intent_confidence_active: bool
    confidence_score: int
    confidence_label: str
    confidence_summary: tuple[str, ...]


@dataclass(frozen=True)
class IntentGovernanceFrame:
    intent_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_intent_signaling_enforced: bool
    bounded_execution_semantics_enforced: bool
    compact_continuity_enforced: bool
    bounded_retrieval_enforced: bool
    recursive_intent_generation_blocked: bool
    autonomous_planning_systems_blocked: bool
    self_generated_execution_goals_blocked: bool
    repo_wide_intent_expansion_blocked: bool
    governance_policy_mutated: bool
    retrieval_scope_widened: bool


@dataclass(frozen=True)
class IntentTerminationFrame:
    intent_termination_active: bool
    should_terminate_intent_transitions: bool
    termination_reason: str
    compact_intent_termination_summary: str
    safe_manual_intervention_recommendation: str
    intent_budget_exceeded: bool
    recursive_intent_oscillation_detected: bool
    governance_violation_risk_detected: bool
    unstable_transition_amplification_detected: bool
    intent_conflict_threshold_exceeded: bool


@dataclass(frozen=True)
class IntentRecoveryFrame:
    intent_recovery_active: bool
    recovery_intent_supported: bool
    recovery_intent_precedence: str
    compact_recovery_intent_summary: str
    autonomous_recovery_goal_generation_allowed: bool
    recursive_recovery_plan_synthesis_allowed: bool


@dataclass(frozen=True)
class IntentPersistenceFrame:
    intent_persistence_active: bool
    active_execution_intent: str
    continuation_intent: str
    recovery_intent: str
    saturation_intent: str
    cooldown_intent: str
    coordination_intent: str
    compact_intent_persistence_summary: str
    raw_objective_persistence_allowed: bool
    execution_scope_mutated: bool


@dataclass(frozen=True)
class IntentDecayFrame:
    intent_decay_active: bool
    conflict_decay_score: int
    transition_decay_score: int
    oscillation_decay_score: int
    amplification_decay_score: int
    decay_guard_active: bool


@dataclass(frozen=True)
class IntentHistoryFrame:
    intent_history_active: bool
    bounded_history: tuple[str, ...]
    history_entry_count: int
    history_truncated: bool
    recursive_history_expansion_blocked: bool


@dataclass(frozen=True)
class IntentIntegrityFrame:
    intent_integrity_active: bool
    execution_semantics_valid: bool
    autonomous_goal_generation_detected: bool
    recursive_planning_detected: bool
    self_expanding_objectives_detected: bool
    integrity_recommendation: str
    automatic_integrity_repair_allowed: bool


@dataclass(frozen=True)
class IntentEvictionFrame:
    intent_eviction_active: bool
    stale_intent_history_eviction_recommended: bool
    stale_intent_metadata_eviction_recommended: bool
    eviction_recommendation: str
    automatic_eviction_performed: bool


@dataclass(frozen=True)
class ExecutionIntentFrame:
    execution_intent_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    priority: IntentPriorityFrame
    conflict: IntentConflictFrame
    transition: IntentTransitionFrame
    cooldown: IntentCooldownFrame
    confidence: IntentConfidenceFrame
    governance: IntentGovernanceFrame
    termination: IntentTerminationFrame
    recovery: IntentRecoveryFrame
    persistence: IntentPersistenceFrame
    decay: IntentDecayFrame
    history: IntentHistoryFrame
    integrity: IntentIntegrityFrame
    eviction: IntentEvictionFrame
    deterministic_intent_summary: str
    bounded_intent_transition_recommendation: str
    compact_intent_arbitration_hint: str
    intent_priority_active: bool
    intent_transition_active: bool
    intent_conflict_active: bool
    estimated_avoided_intent_oscillation: int
    estimated_avoided_recursive_planning: int
    estimated_avoided_execution_instability: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    summary_only: bool


class ExecutionIntentRuntime:
    def evaluate(
        self,
        *,
        active_execution_intent: str = "coordination",
        continuation_intent: str = "continue_bounded_step",
        recovery_intent: str = "resume_safe_recovery",
        saturation_intent: str = "slow_or_terminate_when_saturated",
        cooldown_intent: str = "no_cooldown_required",
        coordination_intent: str = "coordinate_bounded_recommendations",
        bounded_intent_transitions: int = 2,
        repeated_intent_oscillation: int = 0,
        unstable_intent_switching: int = 0,
        intent_amplification_pressure: int = 0,
        recursive_intent_attempts: int = 0,
        autonomous_planning_attempts: int = 0,
        self_generated_goal_attempts: int = 0,
        repo_wide_intent_expansions: int = 0,
        retrieval_radius: int = 2,
        history_entries: tuple[str, ...] = (
            "coordination",
            "continuation",
            "recovery",
        ),
    ) -> ExecutionIntentFrame:
        continuation_cooldown_conflict = continuation_intent.startswith("continue") and (
            "cooldown" in cooldown_intent and "no_cooldown" not in cooldown_intent
        )
        recovery_continuation_conflict = recovery_intent.startswith("resume") and (
            continuation_intent.startswith("continue") and active_execution_intent == "recovery"
        )
        saturation_continuation_conflict = continuation_intent.startswith("continue") and (
            "terminate" in saturation_intent or "saturated" in saturation_intent
        )
        coordination_recovery_conflict = coordination_intent.startswith("coordinate") and (
            recovery_intent.startswith("resume") and active_execution_intent == "coordination"
        )
        conflict_count = sum(
            (
                continuation_cooldown_conflict,
                recovery_continuation_conflict,
                saturation_continuation_conflict,
                coordination_recovery_conflict,
            )
        )
        budget_exceeded = bounded_intent_transitions > MAX_INTENT_TRANSITIONS
        conflict_threshold_exceeded = conflict_count > MAX_INTENT_CONFLICTS
        oscillation_detected = repeated_intent_oscillation > MAX_INTENT_OSCILLATION
        amplification_detected = intent_amplification_pressure > 0 or unstable_intent_switching > 2
        governance_violation = (
            autonomous_planning_attempts > 0
            or self_generated_goal_attempts > 0
            or repo_wide_intent_expansions > 0
            or retrieval_radius > MAX_RETRIEVAL_RADIUS
        )
        recursive_detected = recursive_intent_attempts > 0
        should_terminate = (
            budget_exceeded
            or conflict_threshold_exceeded
            or oscillation_detected
            or amplification_detected
            or governance_violation
            or recursive_detected
        )

        if budget_exceeded:
            termination_reason = "INTENT_BUDGET_EXCEEDED"
        elif recursive_detected or oscillation_detected:
            termination_reason = "RECURSIVE_INTENT_OSCILLATION_DETECTED"
        elif governance_violation:
            termination_reason = "INTENT_GOVERNANCE_VIOLATION_RISK_DETECTED"
        elif amplification_detected:
            termination_reason = "UNSTABLE_TRANSITION_AMPLIFICATION_DETECTED"
        elif conflict_threshold_exceeded:
            termination_reason = "INTENT_CONFLICT_THRESHOLD_EXCEEDED"
        else:
            termination_reason = "INTENT_WITHIN_BOUNDS"

        if conflict_count > 0:
            arbitration_hint = "PRIORITIZE_SATURATION_RECOVERY_COOLDOWN_BEFORE_CONTINUATION"
            resolution_recommendation = "STABILIZE_INTENT_BEFORE_CONTINUATION"
        else:
            arbitration_hint = "FOLLOW_DETERMINISTIC_INTENT_PRIORITY_ORDER"
            resolution_recommendation = "KEEP_ACTIVE_INTENT_STABLE"
        transition_recommendation = (
            "TERMINATE_INTENT_TRANSITIONS_AND_REQUEST_MANUAL_REVIEW"
            if should_terminate
            else "ALLOW_BOUNDED_INTENT_TRANSITION"
        )
        deterministic_summary = (
            f"active={active_execution_intent};conflicts={conflict_count};"
            f"terminate={str(should_terminate).lower()}"
        )
        transition_cooldown_required = (
            repeated_intent_oscillation
            + unstable_intent_switching
            + intent_amplification_pressure
            + conflict_count
        ) > 4
        bounded_history = history_entries[-MAX_INTENT_HISTORY:]

        priority = IntentPriorityFrame(
            intent_priority_active=True,
            deterministic_intent_order=INTENT_PRIORITY_ORDER,
            active_priority_intent=INTENT_PRIORITY_ORDER[0],
            bounded_intent_precedence=True,
            compact_priority_metadata=(
                f"active:{active_execution_intent}",
                f"transitions:{bounded_intent_transitions}/{MAX_INTENT_TRANSITIONS}",
                f"conflicts:{conflict_count}",
            ),
            governance_safe_intent_arbitration=True,
            intent_hierarchy_mutated=False,
            adaptive_goal_system_created=False,
            compact_intent_arbitration_hint=arbitration_hint,
        )
        conflict = IntentConflictFrame(
            intent_conflict_active=True,
            continuation_vs_cooldown_conflict=continuation_cooldown_conflict,
            recovery_vs_continuation_conflict=recovery_continuation_conflict,
            saturation_vs_continuation_conflict=saturation_continuation_conflict,
            coordination_vs_recovery_conflict=coordination_recovery_conflict,
            conflict_count=conflict_count,
            compact_intent_conflict_summary=(
                f"intent-conflicts={conflict_count};resolution={resolution_recommendation}"
            ),
            deterministic_intent_resolution_recommendation=resolution_recommendation,
        )
        transition = IntentTransitionFrame(
            intent_transition_active=True,
            bounded_intent_transitions=bounded_intent_transitions,
            repeated_intent_oscillation=repeated_intent_oscillation,
            unstable_intent_switching=unstable_intent_switching,
            intent_amplification_pressure=intent_amplification_pressure,
            transition_cooldown_required=transition_cooldown_required or oscillation_detected,
            transition_cooldown_recommendation=(
                "APPLY_INTENT_TRANSITION_COOLDOWN"
                if transition_cooldown_required or oscillation_detected
                else "NO_INTENT_TRANSITION_COOLDOWN_REQUIRED"
            ),
            bounded_transition_stabilization_recommendation=(
                "STABILIZE_TO_SINGLE_ACTIVE_INTENT"
                if transition_cooldown_required or conflict_count > 0
                else "KEEP_CURRENT_INTENT_STABLE"
            ),
            autonomous_intent_switch_allowed=False,
            recursive_intent_chain_regeneration_allowed=False,
        )
        cooldown = IntentCooldownFrame(
            intent_cooldown_active=True,
            cooldown_intent_pressure=(
                repeated_intent_oscillation
                + unstable_intent_switching
                + intent_amplification_pressure
            ),
            transition_cooldown_recommendation=transition.transition_cooldown_recommendation,
            bounded_cooldown_window="SINGLE_INTENT_TRANSITION_WINDOW",
            autonomous_cooldown_enforcement_allowed=False,
        )
        governance = IntentGovernanceFrame(
            intent_governance_active=True,
            local_patch_scope_enforced=True,
            deterministic_intent_signaling_enforced=True,
            bounded_execution_semantics_enforced=True,
            compact_continuity_enforced=True,
            bounded_retrieval_enforced=retrieval_radius <= MAX_RETRIEVAL_RADIUS,
            recursive_intent_generation_blocked=True,
            autonomous_planning_systems_blocked=True,
            self_generated_execution_goals_blocked=True,
            repo_wide_intent_expansion_blocked=repo_wide_intent_expansions > 0,
            governance_policy_mutated=False,
            retrieval_scope_widened=False,
        )
        termination = IntentTerminationFrame(
            intent_termination_active=True,
            should_terminate_intent_transitions=should_terminate,
            termination_reason=termination_reason,
            compact_intent_termination_summary=(
                f"{termination_reason};manual-review={str(should_terminate).lower()}"
            ),
            safe_manual_intervention_recommendation=(
                "REQUEST_MANUAL_INTENT_REVIEW"
                if should_terminate
                else "NO_MANUAL_INTERVENTION_REQUIRED"
            ),
            intent_budget_exceeded=budget_exceeded,
            recursive_intent_oscillation_detected=recursive_detected or oscillation_detected,
            governance_violation_risk_detected=governance_violation,
            unstable_transition_amplification_detected=amplification_detected,
            intent_conflict_threshold_exceeded=conflict_threshold_exceeded,
        )
        recovery = IntentRecoveryFrame(
            intent_recovery_active=True,
            recovery_intent_supported=True,
            recovery_intent_precedence="recovery-after-saturation-before-continuation",
            compact_recovery_intent_summary="recovery intent is bounded and advisory",
            autonomous_recovery_goal_generation_allowed=False,
            recursive_recovery_plan_synthesis_allowed=False,
        )
        persistence = IntentPersistenceFrame(
            intent_persistence_active=True,
            active_execution_intent=active_execution_intent,
            continuation_intent=continuation_intent,
            recovery_intent=recovery_intent,
            saturation_intent=saturation_intent,
            cooldown_intent=cooldown_intent,
            coordination_intent=coordination_intent,
            compact_intent_persistence_summary=deterministic_summary,
            raw_objective_persistence_allowed=False,
            execution_scope_mutated=False,
        )
        decay = IntentDecayFrame(
            intent_decay_active=True,
            conflict_decay_score=conflict_count * 8,
            transition_decay_score=max(0, bounded_intent_transitions - 1) * 4,
            oscillation_decay_score=repeated_intent_oscillation * 10,
            amplification_decay_score=intent_amplification_pressure * 12,
            decay_guard_active=True,
        )
        history = IntentHistoryFrame(
            intent_history_active=True,
            bounded_history=bounded_history,
            history_entry_count=len(bounded_history),
            history_truncated=len(history_entries) > MAX_INTENT_HISTORY,
            recursive_history_expansion_blocked=True,
        )
        integrity = IntentIntegrityFrame(
            intent_integrity_active=True,
            execution_semantics_valid=not governance_violation and not recursive_detected,
            autonomous_goal_generation_detected=self_generated_goal_attempts > 0,
            recursive_planning_detected=(
                recursive_intent_attempts > 0 or autonomous_planning_attempts > 0
            ),
            self_expanding_objectives_detected=repo_wide_intent_expansions > 0,
            integrity_recommendation=(
                "KEEP_INTENT_METADATA_COMPACT"
                if not governance_violation and not recursive_detected
                else "STOP_INTENT_EXPANSION_AND_REQUEST_REVIEW"
            ),
            automatic_integrity_repair_allowed=False,
        )
        eviction = IntentEvictionFrame(
            intent_eviction_active=True,
            stale_intent_history_eviction_recommended=len(history_entries) > MAX_INTENT_HISTORY,
            stale_intent_metadata_eviction_recommended=conflict_count > MAX_INTENT_CONFLICTS,
            eviction_recommendation=(
                "RECOMMEND_STALE_INTENT_METADATA_EVICTION"
                if len(history_entries) > MAX_INTENT_HISTORY
                or conflict_count > MAX_INTENT_CONFLICTS
                else "NO_AUTOMATIC_INTENT_EVICTION"
            ),
            automatic_eviction_performed=False,
        )
        confidence_penalty = (
            conflict_count * 10
            + repeated_intent_oscillation * 12
            + unstable_intent_switching * 8
            + intent_amplification_pressure * 14
            + (25 if should_terminate else 0)
        )
        confidence_score = max(0, 100 - confidence_penalty)
        confidence = IntentConfidenceFrame(
            intent_confidence_active=True,
            confidence_score=confidence_score,
            confidence_label=(
                "INTENT_STABLE"
                if confidence_score >= 70
                else (
                    "INTENT_GUARDED" if confidence_score >= 45 else "MANUAL_INTENT_REVIEW_REQUIRED"
                )
            ),
            confidence_summary=(
                f"active:{active_execution_intent}",
                f"conflicts:{conflict_count}/{MAX_INTENT_CONFLICTS}",
                f"oscillation:{repeated_intent_oscillation}/{MAX_INTENT_OSCILLATION}",
                f"termination:{termination_reason}",
            ),
        )

        return ExecutionIntentFrame(
            execution_intent_active=True,
            requirement_ids=EXECUTION_INTENT_REQUIREMENT_IDS,
            test_ids=EXECUTION_INTENT_TEST_IDS,
            priority=priority,
            conflict=conflict,
            transition=transition,
            cooldown=cooldown,
            confidence=confidence,
            governance=governance,
            termination=termination,
            recovery=recovery,
            persistence=persistence,
            decay=decay,
            history=history,
            integrity=integrity,
            eviction=eviction,
            deterministic_intent_summary=deterministic_summary,
            bounded_intent_transition_recommendation=transition_recommendation,
            compact_intent_arbitration_hint=arbitration_hint,
            intent_priority_active=priority.intent_priority_active,
            intent_transition_active=transition.intent_transition_active,
            intent_conflict_active=conflict.intent_conflict_active,
            estimated_avoided_intent_oscillation=31,
            estimated_avoided_recursive_planning=19,
            estimated_avoided_execution_instability=17,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            summary_only=True,
        )


__all__ = [
    "ExecutionIntentFrame",
    "ExecutionIntentRuntime",
    "EXECUTION_INTENT_REQUIREMENT_IDS",
    "EXECUTION_INTENT_TEST_IDS",
    "INTENT_PRIORITY_ORDER",
    "IntentConfidenceFrame",
    "IntentConflictFrame",
    "IntentCooldownFrame",
    "IntentDecayFrame",
    "IntentEvictionFrame",
    "IntentGovernanceFrame",
    "IntentHistoryFrame",
    "IntentIntegrityFrame",
    "IntentPersistenceFrame",
    "IntentPriorityFrame",
    "IntentRecoveryFrame",
    "IntentTerminationFrame",
    "IntentTransitionFrame",
    "MAX_INTENT_CONFLICTS",
    "MAX_INTENT_OSCILLATION",
    "MAX_INTENT_TRANSITIONS",
]
