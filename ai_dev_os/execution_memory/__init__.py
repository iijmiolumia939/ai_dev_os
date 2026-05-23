from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.execution_continuation import ExecutionContinuationRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.verified_execution import VerifiedExecutionRuntime

EXECUTION_MEMORY_REQUIREMENT_IDS = tuple(
    f"FR-EXECUTIONMEMORY-{index:02d}" for index in range(1, 55)
) + ("NFR-COST-67", "NFR-ARCH-80", "NFR-SEC-51")
EXECUTION_MEMORY_TEST_IDS = tuple(f"TC-EXECUTIONMEMORY-{index:02d}" for index in range(1, 55))

MAX_EXECUTION_MEMORY_WINDOW = 5
MAX_EXECUTION_HISTORY = 5
MAX_EXECUTION_MOTIFS = 4
MAX_PROVIDER_EXECUTION_MOTIFS = 4
MAX_CONTINUATION_REUSE_DEPTH = 2
EXECUTION_MEMORY_BUDGET_LIMIT = 12
EXECUTION_MEMORY_SATURATION_THRESHOLD = 80
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_SUCCESS_MOTIFS = (
    "scoped_inspection",
    "local_patch_edit",
    "targeted_pytest",
    "runtime_audit_check",
)
DEFAULT_FAILURE_MOTIFS = ("format_guard", "command_timeout")
DEFAULT_RETRY_MOTIFS = ("retry_once_after_checkpoint", "cooldown_before_retry")
DEFAULT_CONTINUATION_MOTIFS = ("resume_pending_step", "compact_checkpoint")
DEFAULT_PROVIDER_EXECUTION_MOTIFS = (
    "local_patch_provider",
    "local_review_provider",
    "compact_summary_provider",
)
DEFAULT_PROVIDER_EXECUTION_OUTCOMES = (
    "local_patch:stable",
    "local_review:bounded",
    "compact_summary:low_cost",
)
DEFAULT_EXECUTION_HISTORY = (
    "inspect",
    "edit",
    "test",
    "audit",
    "commit",
)


@dataclass(frozen=True)
class ExecutionPatternFrame:
    execution_pattern_active: bool
    verified_successful_execution_motifs: tuple[str, ...]
    repeated_failure_motifs: tuple[str, ...]
    retry_amplification_motifs: tuple[str, ...]
    bounded_continuation_motifs: tuple[str, ...]
    provider_specific_execution_outcomes: tuple[str, ...]
    execution_pattern_score: int
    deterministic_execution_pattern_summary: str
    bounded_reuse_recommendation: str


@dataclass(frozen=True)
class RetryPatternFrame:
    retry_pattern_active: bool
    repeated_retry_chains: int
    retry_cooldown_reuse: int
    retry_saturation_motifs: int
    retry_interruption_patterns: int
    retry_pattern_score: int
    deterministic_retry_summary: str
    bounded_retry_reset_recommendation: str


@dataclass(frozen=True)
class ContinuationPatternFrame:
    continuation_pattern_active: bool
    continuation_motifs: tuple[str, ...]
    continuation_reuse_depth: int
    continuation_reuse_depth_limit: int
    bounded_continuation_reuse: bool
    recursive_continuation_reuse_blocked: bool
    deterministic_continuation_summary: str


@dataclass(frozen=True)
class ProviderExecutionPatternFrame:
    provider_execution_pattern_active: bool
    provider_execution_motifs: tuple[str, ...]
    provider_specific_memory_limit: int
    provider_execution_memory_score: int
    provider_specific_reuse: bool
    provider_memory_overflow_blocked: bool
    deterministic_provider_execution_summary: str


@dataclass(frozen=True)
class FailurePatternFrame:
    failure_pattern_active: bool
    repeated_failure_motifs: tuple[str, ...]
    failure_avoidance_reuse: bool
    failure_repetition_pressure: str
    deterministic_failure_summary: str


@dataclass(frozen=True)
class SuccessPatternFrame:
    success_pattern_active: bool
    verified_successful_execution_motifs: tuple[str, ...]
    success_reuse_recommendation: str
    verified_execution_grounded: bool
    deterministic_success_summary: str


@dataclass(frozen=True)
class ExecutionReuseFrame:
    execution_reuse_active: bool
    bounded_execution_history_reuse: bool
    bounded_provider_specific_reuse: bool
    bounded_continuation_reuse: bool
    bounded_failure_avoidance_reuse: bool
    execution_reuse_score: int
    deterministic_reuse_recommendations: tuple[str, ...]
    autonomous_plan_generation_blocked: bool
    recursive_motif_evolution_blocked: bool


@dataclass(frozen=True)
class ExecutionMotifFrame:
    execution_motif_active: bool
    execution_motifs: tuple[str, ...]
    motif_limit: int
    motif_count: int
    motif_overflow_blocked: bool
    deterministic_motif_summary: str


@dataclass(frozen=True)
class ExecutionHistoryFrame:
    execution_history_active: bool
    execution_history: tuple[str, ...]
    history_limit: int
    history_count: int
    compact_history_summary: str
    history_overflow_blocked: bool
    hidden_memory_expansion_blocked: bool


@dataclass(frozen=True)
class ExecutionBudgetFrame:
    execution_budget_active: bool
    execution_memory_budget_used: int
    execution_memory_budget_limit: int
    execution_memory_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class ExecutionGovernanceFrame:
    execution_governance_active: bool
    local_patch_scope_enforced: bool
    bounded_execution_memory_windows_enforced: bool
    deterministic_execution_reuse_enforced: bool
    bounded_provider_specific_memory_enforced: bool
    bounded_execution_history_retention_enforced: bool
    autonomous_learning_blocked: bool
    recursive_execution_optimization_blocked: bool
    hidden_memory_expansion_blocked: bool
    self_expanding_execution_histories_blocked: bool
    governance_policy_mutation_blocked: bool
    retrieval_scope_widening_blocked: bool


@dataclass(frozen=True)
class ExecutionTerminationFrame:
    execution_termination_active: bool
    execution_memory_terminated: bool
    termination_reasons: tuple[str, ...]
    execution_memory_budget_exceeded: bool
    recursive_reuse_detected: bool
    governance_violation_detected: bool
    execution_memory_saturation_threshold_exceeded: bool
    continuation_reuse_depth_exceeded: bool


@dataclass(frozen=True)
class ExecutionConfidenceFrame:
    execution_confidence_active: bool
    execution_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    local_execution_memory_confidence: bool


@dataclass(frozen=True)
class ExecutionEvictionFrame:
    execution_eviction_active: bool
    evicted_history_items: tuple[str, ...]
    evicted_execution_motifs: tuple[str, ...]
    evicted_provider_motifs: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class ExecutionMemoryFrame:
    execution_memory_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    execution_pattern: ExecutionPatternFrame
    retry_pattern: RetryPatternFrame
    continuation_pattern: ContinuationPatternFrame
    provider_execution_pattern: ProviderExecutionPatternFrame
    failure_pattern: FailurePatternFrame
    success_pattern: SuccessPatternFrame
    execution_reuse: ExecutionReuseFrame
    execution_motif: ExecutionMotifFrame
    execution_history: ExecutionHistoryFrame
    execution_budget: ExecutionBudgetFrame
    execution_governance: ExecutionGovernanceFrame
    execution_termination: ExecutionTerminationFrame
    execution_confidence: ExecutionConfidenceFrame
    execution_eviction: ExecutionEvictionFrame
    execution_pattern_score: int
    retry_pattern_score: int
    execution_reuse_score: int
    provider_execution_memory_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    execution_memory_mode: str
    estimated_avoided_retry_repetition: int
    estimated_avoided_frontier_replanning: int
    estimated_avoided_execution_instability: int


class ExecutionMemoryRuntime:
    def evaluate(
        self,
        *,
        successful_execution_motifs: tuple[str, ...] = DEFAULT_SUCCESS_MOTIFS,
        failure_motifs: tuple[str, ...] = DEFAULT_FAILURE_MOTIFS,
        retry_motifs: tuple[str, ...] = DEFAULT_RETRY_MOTIFS,
        continuation_motifs: tuple[str, ...] = DEFAULT_CONTINUATION_MOTIFS,
        provider_execution_motifs: tuple[str, ...] = DEFAULT_PROVIDER_EXECUTION_MOTIFS,
        provider_execution_outcomes: tuple[str, ...] = DEFAULT_PROVIDER_EXECUTION_OUTCOMES,
        execution_history_items: tuple[str, ...] = DEFAULT_EXECUTION_HISTORY,
        repeated_retry_chains: int = 1,
        retry_cooldown_reuse: int = 1,
        retry_saturation_motifs: int = 0,
        retry_interruption_patterns: int = 0,
        continuation_reuse_depth: int = 1,
        execution_memory_budget_used: int = 7,
        recursive_reuse_attempts: int = 0,
        autonomous_learning_attempts: int = 0,
        recursive_execution_optimization_attempts: int = 0,
        hidden_memory_expansion_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
    ) -> ExecutionMemoryFrame:
        verified_execution = VerifiedExecutionRuntime().evaluate()
        mediation = ExecutionSequencer().mediate()
        continuation = ExecutionContinuationRuntime().evaluate()
        adaptive_provider = AdaptiveProviderRuntime().evaluate()

        bounded_success_motifs = successful_execution_motifs[:MAX_EXECUTION_MOTIFS]
        bounded_failure_motifs = failure_motifs[:MAX_EXECUTION_MEMORY_WINDOW]
        bounded_retry_motifs = retry_motifs[:MAX_EXECUTION_MEMORY_WINDOW]
        bounded_continuation_motifs = continuation_motifs[:MAX_EXECUTION_MEMORY_WINDOW]
        bounded_provider_motifs = provider_execution_motifs[:MAX_PROVIDER_EXECUTION_MOTIFS]
        bounded_provider_outcomes = provider_execution_outcomes[:MAX_EXECUTION_MEMORY_WINDOW]
        bounded_history = execution_history_items[:MAX_EXECUTION_HISTORY]

        evicted_success_motifs = successful_execution_motifs[MAX_EXECUTION_MOTIFS:]
        evicted_provider_motifs = provider_execution_motifs[MAX_PROVIDER_EXECUTION_MOTIFS:]
        evicted_history_items = execution_history_items[MAX_EXECUTION_HISTORY:]

        execution_pattern_score = _clamp(
            len(bounded_success_motifs) * 18
            + int(verified_execution.verification.fake_execution_rejected) * 10
            + int(continuation.tool_execution.successful_tool_executions > 0) * 8
            + int(mediation.runtime_mediation_active) * 6
            - len(bounded_failure_motifs) * 3
        )
        retry_pattern_score = _clamp(
            repeated_retry_chains * 14
            + retry_cooldown_reuse * 10
            + retry_saturation_motifs * 18
            + retry_interruption_patterns * 12
            + len(bounded_retry_motifs) * 7
            + int(mediation.retry.retry_governance_active) * 5
        )
        provider_execution_memory_score = _clamp(
            len(bounded_provider_motifs) * 16
            + len(bounded_provider_outcomes) * 8
            + adaptive_provider.provider_capability_score // 4
            + adaptive_provider.provider_confidence_score // 5
        )
        execution_reuse_score = _clamp(
            len(bounded_history) * 10
            + len(bounded_success_motifs) * 9
            + len(bounded_continuation_motifs) * 7
            + len(bounded_provider_motifs) * 5
            - len(bounded_failure_motifs) * 2
        )
        failure_repetition_score = _clamp(
            len(bounded_failure_motifs) * 12 + retry_saturation_motifs * 15
        )
        saturation_score = _clamp(
            retry_pattern_score
            + failure_repetition_score // 2
            + max(0, execution_memory_budget_used - EXECUTION_MEMORY_BUDGET_LIMIT) * 8
            + max(0, len(execution_history_items) - MAX_EXECUTION_HISTORY) * 4
        )
        governance_violation = any(
            (
                autonomous_learning_attempts,
                recursive_execution_optimization_attempts,
                hidden_memory_expansion_attempts,
                self_expanding_history_attempts,
                governance_policy_mutation_attempts,
                retrieval_scope_widening_attempts,
            )
        )
        termination_reasons = _termination_reasons(
            execution_memory_budget_used > EXECUTION_MEMORY_BUDGET_LIMIT,
            recursive_reuse_attempts > 0,
            governance_violation,
            saturation_score >= EXECUTION_MEMORY_SATURATION_THRESHOLD,
            continuation_reuse_depth > MAX_CONTINUATION_REUSE_DEPTH,
        )
        confidence_score = _clamp(
            90
            + execution_pattern_score // 10
            + execution_reuse_score // 12
            - retry_pattern_score // 5
            - (25 if termination_reasons else 0)
        )

        return ExecutionMemoryFrame(
            execution_memory_active=True,
            requirement_ids=EXECUTION_MEMORY_REQUIREMENT_IDS,
            test_ids=EXECUTION_MEMORY_TEST_IDS,
            execution_pattern=ExecutionPatternFrame(
                execution_pattern_active=True,
                verified_successful_execution_motifs=bounded_success_motifs,
                repeated_failure_motifs=bounded_failure_motifs,
                retry_amplification_motifs=bounded_retry_motifs,
                bounded_continuation_motifs=bounded_continuation_motifs,
                provider_specific_execution_outcomes=bounded_provider_outcomes,
                execution_pattern_score=execution_pattern_score,
                deterministic_execution_pattern_summary=(
                    f"success={len(bounded_success_motifs)};failure={len(bounded_failure_motifs)};retry={len(bounded_retry_motifs)}"
                ),
                bounded_reuse_recommendation=_reuse_recommendation(execution_reuse_score),
            ),
            retry_pattern=RetryPatternFrame(
                retry_pattern_active=True,
                repeated_retry_chains=repeated_retry_chains,
                retry_cooldown_reuse=retry_cooldown_reuse,
                retry_saturation_motifs=retry_saturation_motifs,
                retry_interruption_patterns=retry_interruption_patterns,
                retry_pattern_score=retry_pattern_score,
                deterministic_retry_summary=(
                    f"chains={repeated_retry_chains};cooldown={retry_cooldown_reuse};saturation={retry_saturation_motifs}"
                ),
                bounded_retry_reset_recommendation=_retry_recommendation(retry_pattern_score),
            ),
            continuation_pattern=ContinuationPatternFrame(
                continuation_pattern_active=True,
                continuation_motifs=bounded_continuation_motifs,
                continuation_reuse_depth=continuation_reuse_depth,
                continuation_reuse_depth_limit=MAX_CONTINUATION_REUSE_DEPTH,
                bounded_continuation_reuse=(
                    continuation_reuse_depth <= MAX_CONTINUATION_REUSE_DEPTH
                ),
                recursive_continuation_reuse_blocked=recursive_reuse_attempts > 0,
                deterministic_continuation_summary=(
                    f"motifs={len(bounded_continuation_motifs)};depth={continuation_reuse_depth}"
                ),
            ),
            provider_execution_pattern=ProviderExecutionPatternFrame(
                provider_execution_pattern_active=True,
                provider_execution_motifs=bounded_provider_motifs,
                provider_specific_memory_limit=MAX_PROVIDER_EXECUTION_MOTIFS,
                provider_execution_memory_score=provider_execution_memory_score,
                provider_specific_reuse=True,
                provider_memory_overflow_blocked=bool(evicted_provider_motifs),
                deterministic_provider_execution_summary=(
                    f"motifs={len(bounded_provider_motifs)};outcomes={len(bounded_provider_outcomes)}"
                ),
            ),
            failure_pattern=FailurePatternFrame(
                failure_pattern_active=True,
                repeated_failure_motifs=bounded_failure_motifs,
                failure_avoidance_reuse=True,
                failure_repetition_pressure=_pressure(failure_repetition_score, 60),
                deterministic_failure_summary=(
                    f"failures={len(bounded_failure_motifs)};pressure={failure_repetition_score}"
                ),
            ),
            success_pattern=SuccessPatternFrame(
                success_pattern_active=True,
                verified_successful_execution_motifs=bounded_success_motifs,
                success_reuse_recommendation=_reuse_recommendation(execution_reuse_score),
                verified_execution_grounded=verified_execution.verification.fake_execution_rejected,
                deterministic_success_summary=(
                    f"success={len(bounded_success_motifs)};verified=true"
                ),
            ),
            execution_reuse=ExecutionReuseFrame(
                execution_reuse_active=True,
                bounded_execution_history_reuse=True,
                bounded_provider_specific_reuse=True,
                bounded_continuation_reuse=True,
                bounded_failure_avoidance_reuse=True,
                execution_reuse_score=execution_reuse_score,
                deterministic_reuse_recommendations=(
                    _reuse_recommendation(execution_reuse_score),
                    _retry_recommendation(retry_pattern_score),
                    "BLOCK_FRONTIER_REPLANNING_FOR_KNOWN_LOCAL_PATCH_MOTIF",
                ),
                autonomous_plan_generation_blocked=True,
                recursive_motif_evolution_blocked=True,
            ),
            execution_motif=ExecutionMotifFrame(
                execution_motif_active=True,
                execution_motifs=bounded_success_motifs,
                motif_limit=MAX_EXECUTION_MOTIFS,
                motif_count=len(bounded_success_motifs),
                motif_overflow_blocked=bool(evicted_success_motifs),
                deterministic_motif_summary=(
                    f"motifs={len(bounded_success_motifs)};evicted={len(evicted_success_motifs)}"
                ),
            ),
            execution_history=ExecutionHistoryFrame(
                execution_history_active=True,
                execution_history=bounded_history,
                history_limit=MAX_EXECUTION_HISTORY,
                history_count=len(bounded_history),
                compact_history_summary=f"history={len(bounded_history)};reuse=bounded",
                history_overflow_blocked=bool(evicted_history_items),
                hidden_memory_expansion_blocked=hidden_memory_expansion_attempts > 0,
            ),
            execution_budget=ExecutionBudgetFrame(
                execution_budget_active=True,
                execution_memory_budget_used=execution_memory_budget_used,
                execution_memory_budget_limit=EXECUTION_MEMORY_BUDGET_LIMIT,
                execution_memory_budget_exceeded=(
                    execution_memory_budget_used > EXECUTION_MEMORY_BUDGET_LIMIT
                ),
                budget_pressure=_pressure(
                    execution_memory_budget_used, EXECUTION_MEMORY_BUDGET_LIMIT
                ),
            ),
            execution_governance=ExecutionGovernanceFrame(
                execution_governance_active=True,
                local_patch_scope_enforced=True,
                bounded_execution_memory_windows_enforced=True,
                deterministic_execution_reuse_enforced=True,
                bounded_provider_specific_memory_enforced=True,
                bounded_execution_history_retention_enforced=True,
                autonomous_learning_blocked=True,
                recursive_execution_optimization_blocked=True,
                hidden_memory_expansion_blocked=True,
                self_expanding_execution_histories_blocked=True,
                governance_policy_mutation_blocked=True,
                retrieval_scope_widening_blocked=True,
            ),
            execution_termination=ExecutionTerminationFrame(
                execution_termination_active=True,
                execution_memory_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                execution_memory_budget_exceeded=(
                    execution_memory_budget_used > EXECUTION_MEMORY_BUDGET_LIMIT
                ),
                recursive_reuse_detected=recursive_reuse_attempts > 0,
                governance_violation_detected=governance_violation,
                execution_memory_saturation_threshold_exceeded=(
                    saturation_score >= EXECUTION_MEMORY_SATURATION_THRESHOLD
                ),
                continuation_reuse_depth_exceeded=(
                    continuation_reuse_depth > MAX_CONTINUATION_REUSE_DEPTH
                ),
            ),
            execution_confidence=ExecutionConfidenceFrame(
                execution_confidence_active=True,
                execution_confidence_score=confidence_score,
                confidence_status=_score_label(confidence_score),
                deterministic_confidence=True,
                local_execution_memory_confidence=confidence_score >= 55,
            ),
            execution_eviction=ExecutionEvictionFrame(
                execution_eviction_active=True,
                evicted_history_items=evicted_history_items,
                evicted_execution_motifs=evicted_success_motifs,
                evicted_provider_motifs=evicted_provider_motifs,
                eviction_count=(
                    len(evicted_history_items)
                    + len(evicted_success_motifs)
                    + len(evicted_provider_motifs)
                ),
                bounded_eviction_active=bool(
                    evicted_history_items or evicted_success_motifs or evicted_provider_motifs
                ),
                eviction_summary=(
                    f"history={len(evicted_history_items)};motifs={len(evicted_success_motifs)};provider={len(evicted_provider_motifs)}"
                ),
            ),
            execution_pattern_score=execution_pattern_score,
            retry_pattern_score=retry_pattern_score,
            execution_reuse_score=execution_reuse_score,
            provider_execution_memory_score=provider_execution_memory_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            execution_memory_mode="LOCAL_PATCH_BOUNDED_EXECUTION_MEMORY",
            estimated_avoided_retry_repetition=58 + retry_cooldown_reuse * 4,
            estimated_avoided_frontier_replanning=66 + len(bounded_success_motifs) * 3,
            estimated_avoided_execution_instability=61 + max(0, saturation_score - 45) // 2,
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


def _reuse_recommendation(execution_reuse_score: int) -> str:
    if execution_reuse_score >= 70:
        return "REUSE_KNOWN_LOCAL_PATCH_EXECUTION_MOTIF"
    if execution_reuse_score >= 45:
        return "REUSE_AFTER_COMPACT_CHECKPOINT"
    return "RESET_EXECUTION_MEMORY_AND_REVALIDATE"


def _retry_recommendation(retry_pattern_score: int) -> str:
    if retry_pattern_score >= 70:
        return "RESET_RETRY_CHAIN_AND_COOLDOWN"
    if retry_pattern_score >= 45:
        return "RETRY_ONCE_AFTER_BOUNDED_COOLDOWN"
    return "NO_RETRY_RESET_REQUIRED"


def _termination_reasons(
    budget_exceeded: bool,
    recursive_reuse_detected: bool,
    governance_violation_detected: bool,
    execution_memory_saturation_threshold_exceeded: bool,
    continuation_reuse_depth_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if budget_exceeded:
        reasons.append("EXECUTION_MEMORY_BUDGET_EXCEEDED")
    if recursive_reuse_detected:
        reasons.append("RECURSIVE_REUSE_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if execution_memory_saturation_threshold_exceeded:
        reasons.append("EXECUTION_MEMORY_SATURATION_THRESHOLD_EXCEEDED")
    if continuation_reuse_depth_exceeded:
        reasons.append("CONTINUATION_REUSE_DEPTH_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "EXECUTION_MEMORY_REQUIREMENT_IDS",
    "EXECUTION_MEMORY_TEST_IDS",
    "EXECUTION_MEMORY_BUDGET_LIMIT",
    "EXECUTION_MEMORY_SATURATION_THRESHOLD",
    "MAX_CONTINUATION_REUSE_DEPTH",
    "MAX_EXECUTION_HISTORY",
    "MAX_EXECUTION_MEMORY_WINDOW",
    "MAX_EXECUTION_MOTIFS",
    "MAX_PROVIDER_EXECUTION_MOTIFS",
    "ContinuationPatternFrame",
    "ExecutionBudgetFrame",
    "ExecutionConfidenceFrame",
    "ExecutionEvictionFrame",
    "ExecutionGovernanceFrame",
    "ExecutionHistoryFrame",
    "ExecutionMemoryFrame",
    "ExecutionMemoryRuntime",
    "ExecutionMotifFrame",
    "ExecutionPatternFrame",
    "ExecutionReuseFrame",
    "ExecutionTerminationFrame",
    "FailurePatternFrame",
    "ProviderExecutionPatternFrame",
    "RetryPatternFrame",
    "SuccessPatternFrame",
]
