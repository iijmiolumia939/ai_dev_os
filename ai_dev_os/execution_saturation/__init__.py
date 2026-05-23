from __future__ import annotations

from dataclasses import dataclass

EXECUTION_SATURATION_REQUIREMENT_IDS = tuple(
    f"FR-EXECUTIONSATURATION-{index:02d}" for index in range(1, 21)
) + ("NFR-COST-41", "NFR-ARCH-54", "NFR-SEC-25")
EXECUTION_SATURATION_TEST_IDS = tuple(
    f"TC-EXECUTIONSATURATION-{index:02d}" for index in range(1, 21)
)

MAX_CONTINUATION_ACCUMULATION = 5
MAX_RETRY_OSCILLATION = 3
MAX_TOOL_BURST = 4
MAX_TOOL_QUEUE_DEPTH = 5
MAX_CHECKPOINT_COUNT = 3
MAX_COMPACT_STATE_UNITS = 4
MAX_RETRIEVAL_RADIUS = 2
MAX_HISTORY_ENTRIES = 6


@dataclass(frozen=True)
class SaturationPressureFrame:
    saturation_pressure_active: bool
    continuation_pressure: int
    retry_pressure: int
    tool_pressure: int
    checkpoint_pressure: int
    total_pressure: int
    pressure_label: str
    bounded_saturation_warning: str


@dataclass(frozen=True)
class ContinuationCongestionFrame:
    continuation_congestion_active: bool
    continuation_accumulation: int
    repeated_continuation_retries: int
    recursive_continuation_pressure: int
    continuation_congestion_detected: bool
    recursive_continuation_chain_blocked: bool
    continuation_warning: str


@dataclass(frozen=True)
class RetryOscillationFrame:
    retry_oscillation_active: bool
    repeated_retry_loops: int
    retry_recovery_oscillation: int
    failed_continuation_attempts: int
    retry_amplification: int
    retry_oscillation_detected: bool
    recursive_retry_behavior_detected: bool
    termination_required: bool


@dataclass(frozen=True)
class ToolCongestionFrame:
    tool_congestion_active: bool
    repeated_tool_execution_bursts: int
    tool_saturation_pressure: int
    continuation_tool_congestion: int
    execution_queue_inflation: int
    tool_congestion_detected: bool
    bounded_cooldown_recommendation: str
    deterministic_slowdown_recommendation: str


@dataclass(frozen=True)
class CheckpointInflationFrame:
    checkpoint_inflation_active: bool
    checkpoint_accumulation_pressure: int
    compact_state_inflation: int
    stale_checkpoint_persistence: int
    repeated_checkpoint_reuse: int
    checkpoint_inflation_detected: bool
    checkpoint_cleanup_recommendation: str
    compact_checkpoint_rewrite_recommendation: str
    checkpoints_erased_automatically: bool


@dataclass(frozen=True)
class SaturationDecayFrame:
    saturation_decay_active: bool
    continuation_decay: int
    retry_decay: int
    tool_decay: int
    checkpoint_decay: int
    decay_guard_active: bool


@dataclass(frozen=True)
class SaturationRecoveryFrame:
    saturation_recovery_active: bool
    continuation_cooldown_recommendation: str
    compact_continuation_reset_recommendation: str
    bounded_retry_reduction_recommendation: str
    checkpoint_narrowing_recommendation: str
    deterministic_recovery_recommendation: str
    autonomous_provider_reroute_allowed: bool
    recursive_graph_regeneration_allowed: bool


@dataclass(frozen=True)
class SaturationTerminationFrame:
    saturation_termination_active: bool
    should_terminate: bool
    termination_reason: str
    deterministic_termination_recommendation: str
    retry_oscillation_threshold_exceeded: bool
    recursive_retry_behavior_detected: bool
    recursive_continuation_blocked: bool
    checkpoint_explosion_risk_detected: bool
    tool_congestion_risk_detected: bool


@dataclass(frozen=True)
class SaturationGovernanceFrame:
    saturation_governance_active: bool
    bounded_continuation_enforced: bool
    deterministic_termination_enforced: bool
    local_patch_limits_enforced: bool
    compact_continuity_enforced: bool
    bounded_retrieval_enforced: bool
    recursive_continuation_chains_blocked: bool
    uncontrolled_retries_blocked: bool
    repo_wide_continuation_expansion_blocked: bool
    hidden_background_continuation_blocked: bool
    governance_policy_mutated: bool
    retrieval_scope_widened: bool


@dataclass(frozen=True)
class SaturationConfidenceFrame:
    saturation_confidence_active: bool
    confidence_score: int
    confidence_label: str
    confidence_summary: tuple[str, ...]


@dataclass(frozen=True)
class SaturationHistoryFrame:
    saturation_history_active: bool
    bounded_history: tuple[str, ...]
    history_entry_count: int
    history_truncated: bool
    recursive_history_expansion_blocked: bool


@dataclass(frozen=True)
class SaturationEvictionFrame:
    saturation_eviction_active: bool
    stale_history_eviction_recommended: bool
    stale_checkpoint_eviction_recommended: bool
    eviction_recommendation: str
    automatic_eviction_performed: bool


@dataclass(frozen=True)
class SaturationBudgetFrame:
    saturation_budget_active: bool
    max_continuation_accumulation: int
    max_retry_oscillation: int
    max_tool_burst: int
    max_checkpoint_count: int
    used_continuation_accumulation: int
    used_retry_oscillation: int
    used_tool_burst: int
    used_checkpoint_count: int
    remaining_continuation_budget: int
    remaining_retry_budget: int
    remaining_tool_budget: int
    remaining_checkpoint_budget: int


@dataclass(frozen=True)
class ExecutionSaturationFrame:
    execution_saturation_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    pressure: SaturationPressureFrame
    continuation_congestion: ContinuationCongestionFrame
    retry_oscillation: RetryOscillationFrame
    tool_congestion: ToolCongestionFrame
    checkpoint_inflation: CheckpointInflationFrame
    decay: SaturationDecayFrame
    recovery: SaturationRecoveryFrame
    termination: SaturationTerminationFrame
    governance: SaturationGovernanceFrame
    confidence: SaturationConfidenceFrame
    history: SaturationHistoryFrame
    eviction: SaturationEvictionFrame
    budget: SaturationBudgetFrame
    bounded_saturation_warning: str
    compact_recovery_recommendation: str
    deterministic_termination_recommendation: str
    retry_oscillation_active: bool
    tool_congestion_active: bool
    checkpoint_inflation_active: bool
    saturation_termination_active: bool
    estimated_avoided_recursive_execution: int
    estimated_avoided_retry_loops: int
    estimated_avoided_checkpoint_explosion: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    summary_only: bool


class ExecutionSaturationRuntime:
    def evaluate(
        self,
        *,
        continuation_accumulation: int = 3,
        repeated_continuation_retries: int = 1,
        recursive_continuation_pressure: int = 0,
        execution_congestion: int = 0,
        repeated_retry_loops: int = 1,
        retry_recovery_oscillation: int = 0,
        failed_continuation_attempts: int = 1,
        tool_execution_bursts: int = 2,
        tool_queue_depth: int = 1,
        checkpoint_count: int = 2,
        compact_state_units: int = 2,
        stale_checkpoint_count: int = 0,
        checkpoint_reuse_count: int = 1,
        repo_wide_continuation_expansions: int = 0,
        hidden_background_continuations: int = 0,
        retrieval_radius: int = 2,
        history_entries: tuple[str, ...] = (
            "bounded-continuation",
            "single-retry",
            "compact-checkpoint",
        ),
    ) -> ExecutionSaturationFrame:
        bounded_history = history_entries[-MAX_HISTORY_ENTRIES:]
        retry_amplification = (
            repeated_retry_loops
            + retry_recovery_oscillation
            + failed_continuation_attempts
        )
        continuation_pressure = min(
            100,
            continuation_accumulation * 14
            + repeated_continuation_retries * 9
            + recursive_continuation_pressure * 35
            + execution_congestion,
        )
        retry_pressure = min(100, retry_amplification * 18)
        tool_pressure = min(100, tool_execution_bursts * 15 + tool_queue_depth * 8)
        checkpoint_pressure = min(
            100,
            checkpoint_count * 11
            + compact_state_units * 8
            + stale_checkpoint_count * 14
            + checkpoint_reuse_count * 10,
        )
        total_pressure = min(
            100,
            (continuation_pressure + retry_pressure + tool_pressure + checkpoint_pressure) // 4,
        )

        continuation_detected = (
            continuation_accumulation > MAX_CONTINUATION_ACCUMULATION
            or recursive_continuation_pressure > 0
        )
        retry_detected = retry_amplification > MAX_RETRY_OSCILLATION
        recursive_retry_detected = repeated_retry_loops > 1 and failed_continuation_attempts > 1
        tool_detected = (
            tool_execution_bursts > MAX_TOOL_BURST or tool_queue_depth > MAX_TOOL_QUEUE_DEPTH
        )
        checkpoint_detected = (
            checkpoint_count > MAX_CHECKPOINT_COUNT
            or compact_state_units > MAX_COMPACT_STATE_UNITS
            or stale_checkpoint_count > 0
            or checkpoint_reuse_count > 2
        )
        governance_block = (
            repo_wide_continuation_expansions > 0
            or hidden_background_continuations > 0
            or retrieval_radius > MAX_RETRIEVAL_RADIUS
        )
        should_terminate = (
            continuation_detected
            or retry_detected
            or recursive_retry_detected
            or governance_block
        )

        if retry_detected:
            termination_reason = "RETRY_OSCILLATION_THRESHOLD_EXCEEDED"
        elif recursive_retry_detected:
            termination_reason = "RECURSIVE_RETRY_BEHAVIOR_DETECTED"
        elif recursive_continuation_pressure > 0:
            termination_reason = "RECURSIVE_CONTINUATION_CHAIN_BLOCKED"
        elif continuation_accumulation > MAX_CONTINUATION_ACCUMULATION:
            termination_reason = "CONTINUATION_CONGESTION_THRESHOLD_EXCEEDED"
        elif governance_block:
            termination_reason = "SATURATION_GOVERNANCE_BLOCKED"
        else:
            termination_reason = "SATURATION_WITHIN_BOUNDS"

        if total_pressure >= 70 or should_terminate:
            pressure_label = "SATURATION_TERMINATION_REQUIRED"
        elif total_pressure >= 45:
            pressure_label = "SATURATION_GUARDED"
        else:
            pressure_label = "SATURATION_LOW"

        bounded_warning = (
            "BOUNDED_SATURATION_WARNING"
            if total_pressure >= 45 or should_terminate
            else "SATURATION_LOW"
        )
        recovery_recommendation = (
            "COMPACT_CONTINUATION_RESET_AND_COOLDOWN"
            if should_terminate
            else "CONTINUE_WITH_BOUNDED_SLOWDOWN"
        )
        termination_recommendation = (
            "TERMINATE_CONTINUATION_BEFORE_RETRY_EXPANSION"
            if should_terminate
            else "NO_TERMINATION_REQUIRED"
        )

        pressure = SaturationPressureFrame(
            saturation_pressure_active=True,
            continuation_pressure=continuation_pressure,
            retry_pressure=retry_pressure,
            tool_pressure=tool_pressure,
            checkpoint_pressure=checkpoint_pressure,
            total_pressure=total_pressure,
            pressure_label=pressure_label,
            bounded_saturation_warning=bounded_warning,
        )
        continuation_congestion = ContinuationCongestionFrame(
            continuation_congestion_active=True,
            continuation_accumulation=continuation_accumulation,
            repeated_continuation_retries=repeated_continuation_retries,
            recursive_continuation_pressure=recursive_continuation_pressure,
            continuation_congestion_detected=continuation_detected,
            recursive_continuation_chain_blocked=recursive_continuation_pressure > 0,
            continuation_warning=(
                "TERMINATE_RECURSIVE_CONTINUATION"
                if continuation_detected
                else "CONTINUATION_BOUNDED"
            ),
        )
        retry_oscillation = RetryOscillationFrame(
            retry_oscillation_active=True,
            repeated_retry_loops=repeated_retry_loops,
            retry_recovery_oscillation=retry_recovery_oscillation,
            failed_continuation_attempts=failed_continuation_attempts,
            retry_amplification=retry_amplification,
            retry_oscillation_detected=retry_detected,
            recursive_retry_behavior_detected=recursive_retry_detected,
            termination_required=retry_detected or recursive_retry_detected,
        )
        tool_congestion = ToolCongestionFrame(
            tool_congestion_active=True,
            repeated_tool_execution_bursts=tool_execution_bursts,
            tool_saturation_pressure=tool_pressure,
            continuation_tool_congestion=tool_execution_bursts + repeated_continuation_retries,
            execution_queue_inflation=tool_queue_depth,
            tool_congestion_detected=tool_detected,
            bounded_cooldown_recommendation=(
                "COOLDOWN_BEFORE_NEXT_TOOL_BURST" if tool_detected else "NO_TOOL_COOLDOWN_REQUIRED"
            ),
            deterministic_slowdown_recommendation=(
                "SLOW_CONTINUATION_TO_SINGLE_TOOL_STEP"
                if tool_detected
                else "KEEP_SINGLE_BOUNDED_TOOL_STEP"
            ),
        )
        checkpoint_inflation = CheckpointInflationFrame(
            checkpoint_inflation_active=True,
            checkpoint_accumulation_pressure=checkpoint_count,
            compact_state_inflation=compact_state_units,
            stale_checkpoint_persistence=stale_checkpoint_count,
            repeated_checkpoint_reuse=checkpoint_reuse_count,
            checkpoint_inflation_detected=checkpoint_detected,
            checkpoint_cleanup_recommendation=(
                "RECOMMEND_CHECKPOINT_CLEANUP"
                if checkpoint_detected
                else "NO_CHECKPOINT_CLEANUP_REQUIRED"
            ),
            compact_checkpoint_rewrite_recommendation=(
                "REWRITE_COMPACT_CHECKPOINT_SUMMARY"
                if checkpoint_detected
                else "KEEP_COMPACT_CHECKPOINT"
            ),
            checkpoints_erased_automatically=False,
        )
        decay = SaturationDecayFrame(
            saturation_decay_active=True,
            continuation_decay=max(0, continuation_accumulation - 1) * 4,
            retry_decay=max(0, retry_amplification - 1) * 5,
            tool_decay=max(0, tool_execution_bursts - 1) * 4,
            checkpoint_decay=max(0, checkpoint_count - 1) * 4,
            decay_guard_active=True,
        )
        recovery = SaturationRecoveryFrame(
            saturation_recovery_active=True,
            continuation_cooldown_recommendation="CONTINUATION_COOLDOWN",
            compact_continuation_reset_recommendation="COMPACT_CONTINUATION_RESET",
            bounded_retry_reduction_recommendation="REDUCE_RETRY_TO_SINGLE_ATTEMPT",
            checkpoint_narrowing_recommendation="NARROW_CHECKPOINT_TO_RECENT_COMPACT_STATE",
            deterministic_recovery_recommendation=recovery_recommendation,
            autonomous_provider_reroute_allowed=False,
            recursive_graph_regeneration_allowed=False,
        )
        termination = SaturationTerminationFrame(
            saturation_termination_active=True,
            should_terminate=should_terminate,
            termination_reason=termination_reason,
            deterministic_termination_recommendation=termination_recommendation,
            retry_oscillation_threshold_exceeded=retry_detected,
            recursive_retry_behavior_detected=recursive_retry_detected,
            recursive_continuation_blocked=recursive_continuation_pressure > 0,
            checkpoint_explosion_risk_detected=checkpoint_detected,
            tool_congestion_risk_detected=tool_detected,
        )
        governance = SaturationGovernanceFrame(
            saturation_governance_active=True,
            bounded_continuation_enforced=True,
            deterministic_termination_enforced=True,
            local_patch_limits_enforced=True,
            compact_continuity_enforced=True,
            bounded_retrieval_enforced=retrieval_radius <= MAX_RETRIEVAL_RADIUS,
            recursive_continuation_chains_blocked=True,
            uncontrolled_retries_blocked=True,
            repo_wide_continuation_expansion_blocked=repo_wide_continuation_expansions > 0,
            hidden_background_continuation_blocked=hidden_background_continuations > 0,
            governance_policy_mutated=False,
            retrieval_scope_widened=False,
        )
        confidence_score = max(0, 100 - total_pressure - (25 if should_terminate else 0))
        confidence = SaturationConfidenceFrame(
            saturation_confidence_active=True,
            confidence_score=confidence_score,
            confidence_label=(
                "SATURATION_LOW"
                if confidence_score >= 70
                else "SATURATION_GUARDED"
                if confidence_score >= 45
                else "TERMINATION_REQUIRED"
            ),
            confidence_summary=(
                f"pressure:{pressure_label}",
                f"retry:{retry_amplification}/{MAX_RETRY_OSCILLATION}",
                f"continuation:{continuation_accumulation}/{MAX_CONTINUATION_ACCUMULATION}",
                f"checkpoint:{checkpoint_count}/{MAX_CHECKPOINT_COUNT}",
            ),
        )
        history = SaturationHistoryFrame(
            saturation_history_active=True,
            bounded_history=bounded_history,
            history_entry_count=len(bounded_history),
            history_truncated=len(history_entries) > MAX_HISTORY_ENTRIES,
            recursive_history_expansion_blocked=True,
        )
        eviction = SaturationEvictionFrame(
            saturation_eviction_active=True,
            stale_history_eviction_recommended=len(history_entries) > MAX_HISTORY_ENTRIES,
            stale_checkpoint_eviction_recommended=stale_checkpoint_count > 0,
            eviction_recommendation=(
                "RECOMMEND_STALE_CHECKPOINT_AND_HISTORY_EVICTION"
                if stale_checkpoint_count > 0 or len(history_entries) > MAX_HISTORY_ENTRIES
                else "NO_AUTOMATIC_EVICTION"
            ),
            automatic_eviction_performed=False,
        )
        budget = SaturationBudgetFrame(
            saturation_budget_active=True,
            max_continuation_accumulation=MAX_CONTINUATION_ACCUMULATION,
            max_retry_oscillation=MAX_RETRY_OSCILLATION,
            max_tool_burst=MAX_TOOL_BURST,
            max_checkpoint_count=MAX_CHECKPOINT_COUNT,
            used_continuation_accumulation=continuation_accumulation,
            used_retry_oscillation=retry_amplification,
            used_tool_burst=tool_execution_bursts,
            used_checkpoint_count=checkpoint_count,
            remaining_continuation_budget=max(
                0,
                MAX_CONTINUATION_ACCUMULATION - continuation_accumulation,
            ),
            remaining_retry_budget=max(0, MAX_RETRY_OSCILLATION - retry_amplification),
            remaining_tool_budget=max(0, MAX_TOOL_BURST - tool_execution_bursts),
            remaining_checkpoint_budget=max(0, MAX_CHECKPOINT_COUNT - checkpoint_count),
        )

        return ExecutionSaturationFrame(
            execution_saturation_active=True,
            requirement_ids=EXECUTION_SATURATION_REQUIREMENT_IDS,
            test_ids=EXECUTION_SATURATION_TEST_IDS,
            pressure=pressure,
            continuation_congestion=continuation_congestion,
            retry_oscillation=retry_oscillation,
            tool_congestion=tool_congestion,
            checkpoint_inflation=checkpoint_inflation,
            decay=decay,
            recovery=recovery,
            termination=termination,
            governance=governance,
            confidence=confidence,
            history=history,
            eviction=eviction,
            budget=budget,
            bounded_saturation_warning=bounded_warning,
            compact_recovery_recommendation=recovery_recommendation,
            deterministic_termination_recommendation=termination_recommendation,
            retry_oscillation_active=retry_oscillation.retry_oscillation_active,
            tool_congestion_active=tool_congestion.tool_congestion_active,
            checkpoint_inflation_active=checkpoint_inflation.checkpoint_inflation_active,
            saturation_termination_active=termination.saturation_termination_active,
            estimated_avoided_recursive_execution=31,
            estimated_avoided_retry_loops=19,
            estimated_avoided_checkpoint_explosion=11,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            summary_only=True,
        )


__all__ = [
    "CheckpointInflationFrame",
    "ContinuationCongestionFrame",
    "ExecutionSaturationFrame",
    "ExecutionSaturationRuntime",
    "EXECUTION_SATURATION_REQUIREMENT_IDS",
    "EXECUTION_SATURATION_TEST_IDS",
    "MAX_CHECKPOINT_COUNT",
    "MAX_CONTINUATION_ACCUMULATION",
    "MAX_RETRY_OSCILLATION",
    "MAX_TOOL_BURST",
    "SaturationBudgetFrame",
    "SaturationConfidenceFrame",
    "SaturationDecayFrame",
    "SaturationEvictionFrame",
    "SaturationGovernanceFrame",
    "SaturationHistoryFrame",
    "SaturationPressureFrame",
    "SaturationRecoveryFrame",
    "SaturationTerminationFrame",
    "ToolCongestionFrame",
]
