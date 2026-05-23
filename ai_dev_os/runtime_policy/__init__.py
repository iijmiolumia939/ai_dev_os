from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.execution_continuation import ExecutionContinuationRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.verified_execution import VerifiedExecutionRuntime

RUNTIME_POLICY_REQUIREMENT_IDS = tuple(
    f"FR-RUNTIMEPOLICY-{index:02d}" for index in range(1, 61)
) + ("NFR-COST-69", "NFR-ARCH-82", "NFR-SEC-53")
RUNTIME_POLICY_TEST_IDS = tuple(f"TC-RUNTIMEPOLICY-{index:02d}" for index in range(1, 61))

MAX_POLICY_WINDOW = 5
MAX_POLICY_HISTORY = 5
MAX_ESCALATION_DEPTH = 2
MAX_CONTINUATION_DEPTH = 2
POLICY_BUDGET_LIMIT = 12
RETRY_AMPLIFICATION_THRESHOLD = 3
CONTINUATION_SATURATION_THRESHOLD = 72
REFLECTIVE_SATURATION_THRESHOLD = 80
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_POLICY_HISTORY = (
    "execution_governance",
    "retry_governance",
    "provider_governance",
    "continuation_governance",
    "reflective_governance",
)


@dataclass(frozen=True)
class ExecutionPolicyFrame:
    execution_policy_active: bool
    bounded_subprocess_execution: bool
    bounded_filesystem_access: bool
    verified_execution_only_operations: bool
    deterministic_execution_windows: bool
    execution_policy_score: int
    deterministic_execution_policy_summary: str
    bounded_execution_recommendation: str


@dataclass(frozen=True)
class RetryPolicyFrame:
    retry_policy_active: bool
    bounded_retry_chains: bool
    retry_cooldown_enforced: bool
    retry_saturation_limited: bool
    retry_interruption_threshold_enforced: bool
    retry_policy_score: int
    deterministic_retry_policy_summary: str
    bounded_retry_reset_recommendation: str


@dataclass(frozen=True)
class ProviderPolicyFrame:
    provider_policy_active: bool
    local_first_routing: bool
    bounded_escalation_depth: bool
    provider_fatigue_cooldown: bool
    provider_cost_ceiling: bool
    bounded_provider_confidence_windows: bool
    provider_policy_score: int
    deterministic_provider_policy_summary: str
    bounded_provider_routing_recommendation: str


@dataclass(frozen=True)
class ContinuationPolicyFrame:
    continuation_policy_active: bool
    bounded_continuation_depth: bool
    bounded_continuation_windows: bool
    continuation_interruption_thresholds: bool
    continuation_reset_conditions: bool
    continuation_policy_score: int
    deterministic_continuation_policy_summary: str
    bounded_continuation_reset_recommendation: str


@dataclass(frozen=True)
class ReflectionPolicyFrame:
    reflection_policy_active: bool
    bounded_reflective_scoring: bool
    bounded_reflective_windows: bool
    bounded_evaluation_history: bool
    bounded_reflective_termination: bool
    reflective_policy_score: int
    deterministic_reflection_policy_summary: str
    bounded_reflective_reset_recommendation: str


@dataclass(frozen=True)
class EscalationPolicyFrame:
    escalation_policy_active: bool
    escalation_depth: int
    escalation_depth_limit: int
    escalation_depth_exceeded: bool
    autonomous_escalation_blocked: bool
    frontier_escalation_guarded: bool
    deterministic_escalation_summary: str


@dataclass(frozen=True)
class CostPolicyFrame:
    cost_policy_active: bool
    cost_pressure: str
    provider_cost_ceiling_enforced: bool
    local_first_cost_routing: bool
    frontier_cost_escalation_blocked: bool
    deterministic_cost_policy_summary: str


@dataclass(frozen=True)
class CooldownPolicyFrame:
    cooldown_policy_active: bool
    retry_cooldown_required: bool
    provider_cooldown_required: bool
    continuation_cooldown_required: bool
    deterministic_cooldown_summary: str
    bounded_cooldown_recommendation: str


@dataclass(frozen=True)
class GovernancePolicyFrame:
    governance_policy_active: bool
    local_patch_scope_enforced: bool
    deterministic_bounded_governance: bool
    bounded_escalation_authority: bool
    bounded_reflective_authority: bool
    bounded_execution_authority: bool
    bounded_policy_windows: bool
    hidden_governance_mutation_blocked: bool
    recursive_policy_optimization_blocked: bool
    autonomous_escalation_blocked: bool
    self_expanding_governance_graphs_blocked: bool
    policy_driven_autonomous_execution_blocked: bool
    policy_mutation_blocked: bool
    retrieval_scope_widening_blocked: bool


@dataclass(frozen=True)
class PolicyBudgetFrame:
    policy_budget_active: bool
    policy_budget_used: int
    policy_budget_limit: int
    policy_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class PolicyTerminationFrame:
    policy_termination_active: bool
    policy_terminated: bool
    termination_reasons: tuple[str, ...]
    policy_budget_exceeded: bool
    recursive_governance_detected: bool
    escalation_depth_exceeded: bool
    retry_amplification_threshold_exceeded: bool
    continuation_saturation_threshold_exceeded: bool
    reflective_saturation_threshold_exceeded: bool


@dataclass(frozen=True)
class PolicyConflictFrame:
    policy_conflict_active: bool
    retry_vs_cooldown_conflict: bool
    escalation_vs_cost_conflict: bool
    continuation_vs_termination_conflict: bool
    reflection_vs_execution_conflict: bool
    provider_vs_governance_conflict: bool
    deterministic_arbitration_summary: str
    bounded_arbitration_recommendation: str


@dataclass(frozen=True)
class PolicyCoherenceFrame:
    policy_coherence_active: bool
    policy_coherence_score: int
    execution_retry_coherence: bool
    provider_cost_coherence: bool
    continuation_reflection_coherence: bool
    governance_policy_coherence: bool
    deterministic_coherence_summary: str


@dataclass(frozen=True)
class PolicyHistoryFrame:
    policy_history_active: bool
    policy_history: tuple[str, ...]
    policy_history_limit: int
    compact_policy_history_summary: str
    policy_history_overflow_blocked: bool
    self_expanding_policy_history_blocked: bool


@dataclass(frozen=True)
class PolicyEvictionFrame:
    policy_eviction_active: bool
    evicted_policy_history_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class RuntimePolicyFrame:
    runtime_policy_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    execution_policy: ExecutionPolicyFrame
    retry_policy: RetryPolicyFrame
    provider_policy: ProviderPolicyFrame
    continuation_policy: ContinuationPolicyFrame
    reflection_policy: ReflectionPolicyFrame
    escalation_policy: EscalationPolicyFrame
    cost_policy: CostPolicyFrame
    cooldown_policy: CooldownPolicyFrame
    governance_policy: GovernancePolicyFrame
    policy_budget: PolicyBudgetFrame
    policy_termination: PolicyTerminationFrame
    policy_conflict: PolicyConflictFrame
    policy_coherence: PolicyCoherenceFrame
    policy_history: PolicyHistoryFrame
    policy_eviction: PolicyEvictionFrame
    execution_policy_score: int
    retry_policy_score: int
    provider_policy_score: int
    continuation_policy_score: int
    reflective_policy_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    runtime_policy_mode: str
    estimated_avoided_recursive_governance: int
    estimated_avoided_frontier_escalation: int
    estimated_avoided_policy_fragmentation: int


class RuntimePolicyEngine:
    def evaluate(
        self,
        *,
        policy_history_items: tuple[str, ...] = DEFAULT_POLICY_HISTORY,
        retry_count: int = 1,
        retry_cooldown_pressure: int = 1,
        retry_interruption_pressure: int = 0,
        escalation_depth: int = 1,
        provider_cost_pressure: int = 24,
        provider_fatigue_pressure: int = 1,
        continuation_depth: int = 1,
        continuation_saturation: int = 18,
        reflective_saturation: int = 18,
        policy_budget_used: int = 7,
        recursive_governance_attempts: int = 0,
        hidden_governance_mutation_attempts: int = 0,
        recursive_policy_optimization_attempts: int = 0,
        autonomous_escalation_attempts: int = 0,
        self_expanding_governance_graph_attempts: int = 0,
        policy_driven_autonomous_execution_attempts: int = 0,
        policy_mutation_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
    ) -> RuntimePolicyFrame:
        verified_execution = VerifiedExecutionRuntime().evaluate()
        mediation = ExecutionSequencer().mediate(retry_count=retry_count)
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            bounded_escalation_pressure=escalation_depth,
            estimated_token_pressure=provider_cost_pressure,
            long_session_degradation=provider_fatigue_pressure,
        )
        continuation = ExecutionContinuationRuntime().evaluate()
        reflection = ReflectiveEvaluationRuntime().evaluate(
            reflective_budget_used=min(policy_budget_used, POLICY_BUDGET_LIMIT),
            runtime_conflict_pressure=reflective_saturation // 10,
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=retry_count,
            continuation_reuse_depth=continuation_depth,
        )

        bounded_history = policy_history_items[:MAX_POLICY_HISTORY]
        evicted_history = policy_history_items[MAX_POLICY_HISTORY:]
        retry_amplification = retry_count > RETRY_AMPLIFICATION_THRESHOLD
        retry_vs_cooldown = retry_count > 0 and retry_cooldown_pressure > 0
        escalation_depth_exceeded = escalation_depth > MAX_ESCALATION_DEPTH
        escalation_vs_cost = escalation_depth > 0 and provider_cost_pressure >= 60
        continuation_depth_exceeded = continuation_depth > MAX_CONTINUATION_DEPTH
        continuation_saturated = continuation_saturation >= CONTINUATION_SATURATION_THRESHOLD
        reflective_saturated = reflective_saturation >= REFLECTIVE_SATURATION_THRESHOLD
        reflection_vs_execution = reflective_saturated and retry_amplification
        provider_vs_governance = bool(autonomous_escalation_attempts or policy_mutation_attempts)
        governance_violation = any(
            (
                hidden_governance_mutation_attempts,
                recursive_policy_optimization_attempts,
                autonomous_escalation_attempts,
                self_expanding_governance_graph_attempts,
                policy_driven_autonomous_execution_attempts,
                policy_mutation_attempts,
                retrieval_scope_widening_attempts,
            )
        )
        termination_reasons = _termination_reasons(
            policy_budget_used > POLICY_BUDGET_LIMIT,
            recursive_governance_attempts > 0,
            escalation_depth_exceeded,
            retry_amplification,
            continuation_saturated or continuation_depth_exceeded,
            reflective_saturated,
        )

        execution_policy_score = _clamp(
            45
            + int(verified_execution.governance.bounded_subprocess_execution) * 14
            + int(verified_execution.governance.bounded_filesystem_access) * 12
            + int(verified_execution.verification.fake_execution_rejected) * 12
            + int(mediation.window.window_active) * 10
        )
        retry_policy_score = _clamp(
            75
            - max(0, retry_count - 1) * 9
            - retry_interruption_pressure * 6
            - (18 if retry_amplification else 0)
            + int(mediation.retry.retry_governance_active) * 8
        )
        provider_policy_score = _clamp(
            62
            + adaptive_provider.provider_confidence_score // 5
            + adaptive_provider.provider_capability_score // 6
            - max(0, escalation_depth - 1) * 12
            - provider_cost_pressure // 8
            - provider_fatigue_pressure * 4
        )
        continuation_policy_score = _clamp(
            83
            - max(0, continuation_depth - 1) * 12
            - continuation_saturation // 6
            + int(continuation.continuation_governance_active) * 8
        )
        reflective_policy_score = _clamp(
            82
            - reflective_saturation // 6
            + reflection.reflective_confidence.confidence_score // 8
            - (20 if reflective_saturated else 0)
        )
        policy_coherence_score = _clamp(
            (
                execution_policy_score
                + retry_policy_score
                + provider_policy_score
                + continuation_policy_score
                + reflective_policy_score
            )
            // 5
            - len(termination_reasons) * 6
            - (10 if governance_violation else 0)
        )
        cost_pressure = _pressure(provider_cost_pressure, 60)

        return RuntimePolicyFrame(
            runtime_policy_active=True,
            requirement_ids=RUNTIME_POLICY_REQUIREMENT_IDS,
            test_ids=RUNTIME_POLICY_TEST_IDS,
            execution_policy=ExecutionPolicyFrame(
                execution_policy_active=True,
                bounded_subprocess_execution=True,
                bounded_filesystem_access=True,
                verified_execution_only_operations=True,
                deterministic_execution_windows=True,
                execution_policy_score=execution_policy_score,
                deterministic_execution_policy_summary=(
                    f"subprocess=bounded;filesystem=bounded;window={MAX_POLICY_WINDOW}"
                ),
                bounded_execution_recommendation=(
                    "FOLLOW_VERIFIED_EXECUTION_WINDOW"
                    if execution_policy_score >= 70
                    else "RESET_EXECUTION_POLICY_WINDOW"
                ),
            ),
            retry_policy=RetryPolicyFrame(
                retry_policy_active=True,
                bounded_retry_chains=not retry_amplification,
                retry_cooldown_enforced=True,
                retry_saturation_limited=True,
                retry_interruption_threshold_enforced=True,
                retry_policy_score=retry_policy_score,
                deterministic_retry_policy_summary=(
                    f"retry={retry_count};cooldown={retry_cooldown_pressure};interrupt={retry_interruption_pressure}"
                ),
                bounded_retry_reset_recommendation=_retry_recommendation(
                    retry_policy_score, retry_amplification
                ),
            ),
            provider_policy=ProviderPolicyFrame(
                provider_policy_active=True,
                local_first_routing=True,
                bounded_escalation_depth=not escalation_depth_exceeded,
                provider_fatigue_cooldown=provider_fatigue_pressure > 0,
                provider_cost_ceiling=True,
                bounded_provider_confidence_windows=True,
                provider_policy_score=provider_policy_score,
                deterministic_provider_policy_summary=(
                    f"depth={escalation_depth};cost={cost_pressure};provider={adaptive_provider.provider_routing.recommended_provider}"
                ),
                bounded_provider_routing_recommendation=_provider_recommendation(
                    provider_policy_score, cost_pressure
                ),
            ),
            continuation_policy=ContinuationPolicyFrame(
                continuation_policy_active=True,
                bounded_continuation_depth=not continuation_depth_exceeded,
                bounded_continuation_windows=True,
                continuation_interruption_thresholds=True,
                continuation_reset_conditions=True,
                continuation_policy_score=continuation_policy_score,
                deterministic_continuation_policy_summary=(
                    f"depth={continuation_depth};saturation={continuation_saturation}"
                ),
                bounded_continuation_reset_recommendation=(
                    "RESET_CONTINUATION_POLICY_WINDOW"
                    if continuation_saturated or continuation_depth_exceeded
                    else "CONTINUE_BOUNDED_CONTINUATION_POLICY"
                ),
            ),
            reflection_policy=ReflectionPolicyFrame(
                reflection_policy_active=True,
                bounded_reflective_scoring=True,
                bounded_reflective_windows=True,
                bounded_evaluation_history=True,
                bounded_reflective_termination=True,
                reflective_policy_score=reflective_policy_score,
                deterministic_reflection_policy_summary=(
                    f"reflective={reflective_saturation};confidence={reflection.reflective_confidence.confidence_score}"
                ),
                bounded_reflective_reset_recommendation=(
                    "RESET_REFLECTIVE_POLICY_WINDOW"
                    if reflective_saturated
                    else "CONTINUE_BOUNDED_REFLECTIVE_POLICY"
                ),
            ),
            escalation_policy=EscalationPolicyFrame(
                escalation_policy_active=True,
                escalation_depth=escalation_depth,
                escalation_depth_limit=MAX_ESCALATION_DEPTH,
                escalation_depth_exceeded=escalation_depth_exceeded,
                autonomous_escalation_blocked=True,
                frontier_escalation_guarded=True,
                deterministic_escalation_summary=(
                    f"depth={escalation_depth}/{MAX_ESCALATION_DEPTH};guarded=true"
                ),
            ),
            cost_policy=CostPolicyFrame(
                cost_policy_active=True,
                cost_pressure=cost_pressure,
                provider_cost_ceiling_enforced=True,
                local_first_cost_routing=True,
                frontier_cost_escalation_blocked=True,
                deterministic_cost_policy_summary=f"cost={provider_cost_pressure};pressure={cost_pressure}",
            ),
            cooldown_policy=CooldownPolicyFrame(
                cooldown_policy_active=True,
                retry_cooldown_required=retry_count > 0,
                provider_cooldown_required=provider_fatigue_pressure > 0,
                continuation_cooldown_required=continuation_saturated,
                deterministic_cooldown_summary=(
                    f"retry={retry_count};provider={provider_fatigue_pressure};continuation={continuation_saturation}"
                ),
                bounded_cooldown_recommendation=(
                    "APPLY_BOUNDED_POLICY_COOLDOWN"
                    if retry_vs_cooldown or continuation_saturated
                    else "MAINTAIN_POLICY_FLOW"
                ),
            ),
            governance_policy=GovernancePolicyFrame(
                governance_policy_active=True,
                local_patch_scope_enforced=True,
                deterministic_bounded_governance=True,
                bounded_escalation_authority=True,
                bounded_reflective_authority=True,
                bounded_execution_authority=True,
                bounded_policy_windows=True,
                hidden_governance_mutation_blocked=True,
                recursive_policy_optimization_blocked=True,
                autonomous_escalation_blocked=True,
                self_expanding_governance_graphs_blocked=True,
                policy_driven_autonomous_execution_blocked=True,
                policy_mutation_blocked=True,
                retrieval_scope_widening_blocked=True,
            ),
            policy_budget=PolicyBudgetFrame(
                policy_budget_active=True,
                policy_budget_used=policy_budget_used,
                policy_budget_limit=POLICY_BUDGET_LIMIT,
                policy_budget_exceeded=policy_budget_used > POLICY_BUDGET_LIMIT,
                budget_pressure=_pressure(policy_budget_used, POLICY_BUDGET_LIMIT),
            ),
            policy_termination=PolicyTerminationFrame(
                policy_termination_active=True,
                policy_terminated=bool(termination_reasons or governance_violation),
                termination_reasons=termination_reasons
                + (("GOVERNANCE_VIOLATION_DETECTED",) if governance_violation else ()),
                policy_budget_exceeded=policy_budget_used > POLICY_BUDGET_LIMIT,
                recursive_governance_detected=recursive_governance_attempts > 0,
                escalation_depth_exceeded=escalation_depth_exceeded,
                retry_amplification_threshold_exceeded=retry_amplification,
                continuation_saturation_threshold_exceeded=(
                    continuation_saturated or continuation_depth_exceeded
                ),
                reflective_saturation_threshold_exceeded=reflective_saturated,
            ),
            policy_conflict=PolicyConflictFrame(
                policy_conflict_active=True,
                retry_vs_cooldown_conflict=retry_vs_cooldown,
                escalation_vs_cost_conflict=escalation_vs_cost,
                continuation_vs_termination_conflict=(
                    continuation_saturated or continuation_depth_exceeded
                ),
                reflection_vs_execution_conflict=reflection_vs_execution,
                provider_vs_governance_conflict=provider_vs_governance,
                deterministic_arbitration_summary=(
                    f"retry_cooldown={str(retry_vs_cooldown).lower()};escalation_cost={str(escalation_vs_cost).lower()}"
                ),
                bounded_arbitration_recommendation=_arbitration_recommendation(
                    escalation_vs_cost,
                    retry_amplification,
                    continuation_saturated or continuation_depth_exceeded,
                    reflective_saturated,
                ),
            ),
            policy_coherence=PolicyCoherenceFrame(
                policy_coherence_active=True,
                policy_coherence_score=policy_coherence_score,
                execution_retry_coherence=execution_policy_score >= 55
                and retry_policy_score >= 55,
                provider_cost_coherence=not escalation_vs_cost,
                continuation_reflection_coherence=not (
                    continuation_saturated and reflective_saturated
                ),
                governance_policy_coherence=not governance_violation,
                deterministic_coherence_summary=(
                    f"coherence={policy_coherence_score};memory={execution_memory.execution_reuse_score}"
                ),
            ),
            policy_history=PolicyHistoryFrame(
                policy_history_active=True,
                policy_history=bounded_history,
                policy_history_limit=MAX_POLICY_HISTORY,
                compact_policy_history_summary=f"history={len(bounded_history)};policy=bounded",
                policy_history_overflow_blocked=bool(evicted_history),
                self_expanding_policy_history_blocked=(
                    self_expanding_governance_graph_attempts > 0
                ),
            ),
            policy_eviction=PolicyEvictionFrame(
                policy_eviction_active=True,
                evicted_policy_history_items=evicted_history,
                eviction_count=len(evicted_history),
                bounded_eviction_active=bool(evicted_history),
                eviction_summary=f"policy_history={len(evicted_history)}",
            ),
            execution_policy_score=execution_policy_score,
            retry_policy_score=retry_policy_score,
            provider_policy_score=provider_policy_score,
            continuation_policy_score=continuation_policy_score,
            reflective_policy_score=reflective_policy_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            runtime_policy_mode="LOCAL_PATCH_UNIFIED_RUNTIME_POLICY",
            estimated_avoided_recursive_governance=70 + recursive_governance_attempts * 7,
            estimated_avoided_frontier_escalation=68 + max(0, escalation_depth - 1) * 5,
            estimated_avoided_policy_fragmentation=72 + max(0, policy_coherence_score - 60) // 2,
        )


def _clamp(score: int) -> int:
    return max(MIN_SCORE, min(MAX_SCORE, score))


def _pressure(value: int, limit: int) -> str:
    if value > limit:
        return "HIGH"
    if value >= max(1, limit - 1):
        return "MEDIUM"
    return "LOW"


def _retry_recommendation(retry_policy_score: int, retry_amplification: bool) -> str:
    if retry_amplification or retry_policy_score < 55:
        return "RESET_RETRY_CHAIN_AND_APPLY_POLICY_COOLDOWN"
    if retry_policy_score < 75:
        return "RETRY_ONCE_WITH_POLICY_WINDOW"
    return "MAINTAIN_BOUNDED_RETRY_POLICY"


def _provider_recommendation(provider_policy_score: int, cost_pressure: str) -> str:
    if cost_pressure == "HIGH":
        return "LOCAL_FIRST_AND_BLOCK_FRONTIER_ESCALATION"
    if provider_policy_score < 55:
        return "HUMAN_CONFIRMED_PROVIDER_ESCALATION_ONLY"
    return "LOCAL_FIRST_BOUNDED_PROVIDER_ROUTING"


def _arbitration_recommendation(
    escalation_vs_cost: bool,
    retry_amplification: bool,
    continuation_pressure: bool,
    reflective_saturated: bool,
) -> str:
    if escalation_vs_cost:
        return "COST_POLICY_OVERRIDES_ESCALATION"
    if retry_amplification:
        return "COOLDOWN_POLICY_OVERRIDES_RETRY"
    if continuation_pressure:
        return "TERMINATION_POLICY_OVERRIDES_CONTINUATION"
    if reflective_saturated:
        return "EXECUTION_POLICY_OVERRIDES_REFLECTION"
    return "MAINTAIN_DETERMINISTIC_POLICY_ORDER"


def _termination_reasons(
    policy_budget_exceeded: bool,
    recursive_governance_detected: bool,
    escalation_depth_exceeded: bool,
    retry_amplification_threshold_exceeded: bool,
    continuation_saturation_threshold_exceeded: bool,
    reflective_saturation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if policy_budget_exceeded:
        reasons.append("POLICY_BUDGET_EXCEEDED")
    if recursive_governance_detected:
        reasons.append("RECURSIVE_GOVERNANCE_DETECTED")
    if escalation_depth_exceeded:
        reasons.append("ESCALATION_DEPTH_EXCEEDED")
    if retry_amplification_threshold_exceeded:
        reasons.append("RETRY_AMPLIFICATION_THRESHOLD_EXCEEDED")
    if continuation_saturation_threshold_exceeded:
        reasons.append("CONTINUATION_SATURATION_THRESHOLD_EXCEEDED")
    if reflective_saturation_threshold_exceeded:
        reasons.append("REFLECTIVE_SATURATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "RUNTIME_POLICY_REQUIREMENT_IDS",
    "RUNTIME_POLICY_TEST_IDS",
    "MAX_ESCALATION_DEPTH",
    "MAX_POLICY_HISTORY",
    "POLICY_BUDGET_LIMIT",
    "CONTINUATION_SATURATION_THRESHOLD",
    "REFLECTIVE_SATURATION_THRESHOLD",
    "RETRY_AMPLIFICATION_THRESHOLD",
    "ContinuationPolicyFrame",
    "CooldownPolicyFrame",
    "CostPolicyFrame",
    "EscalationPolicyFrame",
    "ExecutionPolicyFrame",
    "GovernancePolicyFrame",
    "PolicyBudgetFrame",
    "PolicyCoherenceFrame",
    "PolicyConflictFrame",
    "PolicyEvictionFrame",
    "PolicyHistoryFrame",
    "PolicyTerminationFrame",
    "ProviderPolicyFrame",
    "ReflectionPolicyFrame",
    "RetryPolicyFrame",
    "RuntimePolicyEngine",
    "RuntimePolicyFrame",
]
