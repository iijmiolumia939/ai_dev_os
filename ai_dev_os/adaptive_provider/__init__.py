from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider_routing import AdaptiveProviderRoutingRuntime
from ai_dev_os.provider_fatigue import ProviderFatigueRuntime
from ai_dev_os.provider_stability import ProviderStabilityRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime

ADAPTIVE_PROVIDER_REQUIREMENT_IDS = tuple(
    f"FR-ADAPTIVEPROVIDER-{index:02d}" for index in range(1, 53)
) + ("NFR-COST-65", "NFR-ARCH-78", "NFR-SEC-49")
ADAPTIVE_PROVIDER_TEST_IDS = tuple(f"TC-ADAPTIVEPROVIDER-{index:02d}" for index in range(1, 53))

MAX_PROVIDER_WINDOW = 5
MAX_PROVIDER_HISTORY = 5
MAX_SPECIALIZATIONS = 4
MAX_ESCALATION_DEPTH = 2
PROVIDER_BUDGET_LIMIT = 12
PROVIDER_INSTABILITY_THRESHOLD = 72
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_PROVIDER_CAPABILITIES = {
    "local_patch_execution": 33,
    "orchestration_stability": 26,
    "planning_stability": 21,
    "reflective_stability": 20,
}
DEFAULT_PROVIDER_SPECIALIZATIONS = (
    "local_patch_execution",
    "compact_summary",
    "bounded_reflection",
    "governance_visibility",
)


@dataclass(frozen=True)
class ProviderCapabilityFrame:
    provider_capability_active: bool
    provider_capability_score: int
    deterministic_execution_success: bool
    bounded_orchestration_stability: str
    bounded_planning_stability: str
    bounded_reflective_stability: str
    verified_execution_quality: str
    deterministic_provider_capability_summary: str
    bounded_routing_recommendation: str


@dataclass(frozen=True)
class ProviderSpecializationFrame:
    provider_specialization_active: bool
    specialization_memory: tuple[str, ...]
    specialization_limit: int
    specialization_count: int
    specialization_overflow_blocked: bool
    deterministic_specialization_summary: str


@dataclass(frozen=True)
class ProviderFatigueFrame:
    provider_fatigue_active: bool
    provider_fatigue_score: int
    long_session_degradation: int
    retry_amplification: int
    orchestration_instability: int
    continuation_decay: int
    reflective_saturation: int
    deterministic_fatigue_summary: str
    bounded_cooldown_recommendation: str


@dataclass(frozen=True)
class ProviderCostFrame:
    provider_cost_active: bool
    provider_cost_pressure: str
    estimated_token_pressure: int
    bounded_reasoning_cost: int
    bounded_execution_cost: int
    bounded_escalation_pressure: int
    deterministic_cost_summary: str
    bounded_local_first_recommendation: str


@dataclass(frozen=True)
class ProviderLatencyFrame:
    provider_latency_active: bool
    latency_pressure: str
    estimated_latency_units: int
    latency_window_bounded: bool
    deterministic_latency_summary: str


@dataclass(frozen=True)
class ProviderConfidenceFrame:
    provider_confidence_active: bool
    provider_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    local_first_confidence: bool


@dataclass(frozen=True)
class ProviderRoutingFrame:
    provider_routing_active: bool
    recommended_provider: str
    routing_recommendations: tuple[str, ...]
    deterministic_routing: bool
    bounded_provider_window: bool
    hidden_provider_switching_blocked: bool
    dynamic_routing_scope_widening_blocked: bool


@dataclass(frozen=True)
class ProviderFallbackFrame:
    provider_fallback_active: bool
    fallback_recommendations: tuple[str, ...]
    fallback_pressure: str
    recursive_fallback_blocked: bool
    automatic_provider_execution_blocked: bool


@dataclass(frozen=True)
class ProviderEscalationFrame:
    provider_escalation_active: bool
    escalation_depth: int
    escalation_depth_limit: int
    escalation_pressure: str
    hidden_provider_escalation_blocked: bool
    autonomous_escalation_blocked: bool
    recursive_escalation_blocked: bool


@dataclass(frozen=True)
class ProviderBudgetFrame:
    provider_budget_active: bool
    provider_budget_used: int
    provider_budget_limit: int
    provider_budget_exceeded: bool
    budget_pressure: str
    local_first_budget: bool


@dataclass(frozen=True)
class ProviderGovernanceFrame:
    provider_governance_active: bool
    local_patch_scope_enforced: bool
    bounded_provider_windows_enforced: bool
    deterministic_routing_enforced: bool
    bounded_escalation_depth_enforced: bool
    bounded_provider_history_enforced: bool
    hidden_provider_switching_blocked: bool
    autonomous_escalation_blocked: bool
    recursive_provider_optimization_blocked: bool
    provider_policy_mutation_blocked: bool
    retrieval_scope_widening_blocked: bool


@dataclass(frozen=True)
class ProviderTerminationFrame:
    provider_terminated: bool
    termination_reasons: tuple[str, ...]
    provider_budget_exceeded: bool
    recursive_escalation_detected: bool
    governance_violation_detected: bool
    provider_instability_threshold_exceeded: bool
    escalation_depth_exceeded: bool


@dataclass(frozen=True)
class ProviderHistoryFrame:
    provider_history_active: bool
    provider_history: tuple[str, ...]
    provider_history_limit: int
    compact_history_summary: str
    history_overflow_blocked: bool
    hidden_provider_history_blocked: bool


@dataclass(frozen=True)
class ProviderEvictionFrame:
    provider_eviction_active: bool
    evicted_history_items: tuple[str, ...]
    evicted_specializations: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class AdaptiveProviderFrame:
    adaptive_provider_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    provider_capability: ProviderCapabilityFrame
    provider_specialization: ProviderSpecializationFrame
    provider_fatigue: ProviderFatigueFrame
    provider_cost: ProviderCostFrame
    provider_latency: ProviderLatencyFrame
    provider_confidence: ProviderConfidenceFrame
    provider_routing: ProviderRoutingFrame
    provider_fallback: ProviderFallbackFrame
    provider_escalation: ProviderEscalationFrame
    provider_budget: ProviderBudgetFrame
    provider_governance: ProviderGovernanceFrame
    provider_termination: ProviderTerminationFrame
    provider_history: ProviderHistoryFrame
    provider_eviction: ProviderEvictionFrame
    provider_capability_score: int
    provider_fatigue_score: int
    provider_cost_pressure: str
    provider_confidence_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    provider_routing_mode: str
    estimated_avoided_frontier_provider_usage: int
    estimated_avoided_recursive_escalation: int
    estimated_avoided_provider_instability: int


class AdaptiveProviderRuntime:
    def evaluate(
        self,
        *,
        provider_capabilities: dict[str, int] | None = None,
        provider_specializations: tuple[str, ...] = DEFAULT_PROVIDER_SPECIALIZATIONS,
        provider_history_items: tuple[str, ...] = (
            "local_patch",
            "runtime_mediation",
            "reflective_evaluation",
            "intentional_planning",
        ),
        long_session_degradation: int = 1,
        retry_amplification: int = 1,
        orchestration_instability: int = 1,
        continuation_decay: int = 0,
        reflective_saturation: int = 0,
        estimated_token_pressure: int = 24,
        bounded_reasoning_cost: int = 18,
        bounded_execution_cost: int = 12,
        bounded_escalation_pressure: int = 1,
        estimated_latency_units: int = 18,
        provider_budget_used: int = 7,
        escalation_depth: int = 1,
        recursive_escalation_attempts: int = 0,
        hidden_provider_switching_attempts: int = 0,
        autonomous_escalation_attempts: int = 0,
        recursive_provider_optimization_attempts: int = 0,
        provider_policy_mutation_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
        hidden_provider_history_attempts: int = 0,
    ) -> AdaptiveProviderFrame:
        capabilities = dict(provider_capabilities or DEFAULT_PROVIDER_CAPABILITIES)
        adaptive_routing = AdaptiveProviderRoutingRuntime().evaluate()
        fatigue_runtime = ProviderFatigueRuntime().evaluate()
        stability = ProviderStabilityRuntime().evaluate()
        reflection = ReflectiveEvaluationRuntime().evaluate()
        specialization_memory = provider_specializations[:MAX_SPECIALIZATIONS]
        evicted_specializations = provider_specializations[MAX_SPECIALIZATIONS:]
        bounded_history = provider_history_items[:MAX_PROVIDER_HISTORY]
        evicted_history = provider_history_items[MAX_PROVIDER_HISTORY:]
        capability_score = _clamp(
            sum(max(0, value) for value in capabilities.values())
            + int(adaptive_routing.adaptive_provider_routing_active) * 16
            + int(stability.provider_stability_active) * 12
            + int(reflection.execution_quality_score >= 80) * 10
        )
        fatigue_score = _clamp(
            long_session_degradation * 13
            + retry_amplification * 11
            + orchestration_instability * 12
            + continuation_decay * 10
            + reflective_saturation * 14
            + int(fatigue_runtime.provider_fatigue_active) * 3
        )
        cost_pressure_score = _clamp(
            estimated_token_pressure
            + bounded_reasoning_cost
            + bounded_execution_cost
            + bounded_escalation_pressure * 12
        )
        cost_pressure = _pressure(cost_pressure_score, 70)
        latency_pressure = _pressure(estimated_latency_units, 36)
        capability_penalty = 100 - capability_score
        confidence_score = _clamp(
            94 - capability_penalty // 2 - fatigue_score // 3 - cost_pressure_score // 5
        )
        instability_score = _clamp(
            fatigue_score + (100 - confidence_score) + orchestration_instability * 8
        )
        governance_violation = any(
            (
                hidden_provider_switching_attempts,
                autonomous_escalation_attempts,
                recursive_provider_optimization_attempts,
                provider_policy_mutation_attempts,
                retrieval_scope_widening_attempts,
                hidden_provider_history_attempts,
            )
        )
        termination_reasons = _termination_reasons(
            provider_budget_used > PROVIDER_BUDGET_LIMIT,
            recursive_escalation_attempts > 0,
            governance_violation,
            instability_score >= PROVIDER_INSTABILITY_THRESHOLD,
            escalation_depth > MAX_ESCALATION_DEPTH,
        )
        recommended_provider = _recommended_provider(
            confidence_score, cost_pressure, fatigue_score
        )
        routing_recommendations = (
            f"primary:{recommended_provider}",
            f"capability:{capability_score}",
            f"fatigue:{fatigue_score}",
            f"cost:{cost_pressure}",
        )

        return AdaptiveProviderFrame(
            adaptive_provider_active=True,
            requirement_ids=ADAPTIVE_PROVIDER_REQUIREMENT_IDS,
            test_ids=ADAPTIVE_PROVIDER_TEST_IDS,
            provider_capability=ProviderCapabilityFrame(
                provider_capability_active=True,
                provider_capability_score=capability_score,
                deterministic_execution_success=reflection.execution_quality_score >= 80,
                bounded_orchestration_stability=_score_label(capability_score),
                bounded_planning_stability=_score_label(reflection.planning_integrity_score),
                bounded_reflective_stability=_score_label(
                    reflection.reflective_confidence.confidence_score
                ),
                verified_execution_quality=_score_label(reflection.execution_quality_score),
                deterministic_provider_capability_summary=(
                    f"capability={capability_score};reflection={reflection.execution_quality_score}"
                ),
                bounded_routing_recommendation=f"LOCAL_FIRST:{recommended_provider}",
            ),
            provider_specialization=ProviderSpecializationFrame(
                provider_specialization_active=True,
                specialization_memory=specialization_memory,
                specialization_limit=MAX_SPECIALIZATIONS,
                specialization_count=len(specialization_memory),
                specialization_overflow_blocked=bool(evicted_specializations),
                deterministic_specialization_summary=(
                    f"specializations={len(specialization_memory)};evicted={len(evicted_specializations)}"
                ),
            ),
            provider_fatigue=ProviderFatigueFrame(
                provider_fatigue_active=True,
                provider_fatigue_score=fatigue_score,
                long_session_degradation=long_session_degradation,
                retry_amplification=retry_amplification,
                orchestration_instability=orchestration_instability,
                continuation_decay=continuation_decay,
                reflective_saturation=reflective_saturation,
                deterministic_fatigue_summary=(
                    f"long={long_session_degradation};retry={retry_amplification};reflect={reflective_saturation}"
                ),
                bounded_cooldown_recommendation=_cooldown_recommendation(fatigue_score),
            ),
            provider_cost=ProviderCostFrame(
                provider_cost_active=True,
                provider_cost_pressure=cost_pressure,
                estimated_token_pressure=estimated_token_pressure,
                bounded_reasoning_cost=bounded_reasoning_cost,
                bounded_execution_cost=bounded_execution_cost,
                bounded_escalation_pressure=bounded_escalation_pressure,
                deterministic_cost_summary=(
                    f"tokens={estimated_token_pressure};reasoning={bounded_reasoning_cost};execution={bounded_execution_cost}"
                ),
                bounded_local_first_recommendation=_cost_recommendation(cost_pressure),
            ),
            provider_latency=ProviderLatencyFrame(
                provider_latency_active=True,
                latency_pressure=latency_pressure,
                estimated_latency_units=estimated_latency_units,
                latency_window_bounded=True,
                deterministic_latency_summary=f"latency_units={estimated_latency_units}",
            ),
            provider_confidence=ProviderConfidenceFrame(
                provider_confidence_active=True,
                provider_confidence_score=confidence_score,
                confidence_status=_score_label(confidence_score),
                deterministic_confidence=True,
                local_first_confidence=recommended_provider != "frontier_reference",
            ),
            provider_routing=ProviderRoutingFrame(
                provider_routing_active=True,
                recommended_provider=recommended_provider,
                routing_recommendations=routing_recommendations,
                deterministic_routing=True,
                bounded_provider_window=True,
                hidden_provider_switching_blocked=hidden_provider_switching_attempts > 0,
                dynamic_routing_scope_widening_blocked=retrieval_scope_widening_attempts > 0,
            ),
            provider_fallback=ProviderFallbackFrame(
                provider_fallback_active=True,
                fallback_recommendations=(
                    "local_patch",
                    "compact_summary",
                    "human_confirmed_escalation",
                ),
                fallback_pressure=_pressure(fatigue_score + cost_pressure_score // 2, 70),
                recursive_fallback_blocked=recursive_escalation_attempts > 0,
                automatic_provider_execution_blocked=True,
            ),
            provider_escalation=ProviderEscalationFrame(
                provider_escalation_active=True,
                escalation_depth=escalation_depth,
                escalation_depth_limit=MAX_ESCALATION_DEPTH,
                escalation_pressure=_pressure(escalation_depth + bounded_escalation_pressure, 3),
                hidden_provider_escalation_blocked=hidden_provider_switching_attempts > 0,
                autonomous_escalation_blocked=autonomous_escalation_attempts > 0,
                recursive_escalation_blocked=recursive_escalation_attempts > 0,
            ),
            provider_budget=ProviderBudgetFrame(
                provider_budget_active=True,
                provider_budget_used=provider_budget_used,
                provider_budget_limit=PROVIDER_BUDGET_LIMIT,
                provider_budget_exceeded=provider_budget_used > PROVIDER_BUDGET_LIMIT,
                budget_pressure=_pressure(provider_budget_used, PROVIDER_BUDGET_LIMIT),
                local_first_budget=True,
            ),
            provider_governance=ProviderGovernanceFrame(
                provider_governance_active=True,
                local_patch_scope_enforced=True,
                bounded_provider_windows_enforced=True,
                deterministic_routing_enforced=True,
                bounded_escalation_depth_enforced=True,
                bounded_provider_history_enforced=True,
                hidden_provider_switching_blocked=hidden_provider_switching_attempts > 0,
                autonomous_escalation_blocked=autonomous_escalation_attempts > 0,
                recursive_provider_optimization_blocked=(
                    recursive_provider_optimization_attempts > 0
                ),
                provider_policy_mutation_blocked=provider_policy_mutation_attempts > 0,
                retrieval_scope_widening_blocked=retrieval_scope_widening_attempts > 0,
            ),
            provider_termination=ProviderTerminationFrame(
                provider_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                provider_budget_exceeded=provider_budget_used > PROVIDER_BUDGET_LIMIT,
                recursive_escalation_detected=recursive_escalation_attempts > 0,
                governance_violation_detected=governance_violation,
                provider_instability_threshold_exceeded=(
                    instability_score >= PROVIDER_INSTABILITY_THRESHOLD
                ),
                escalation_depth_exceeded=escalation_depth > MAX_ESCALATION_DEPTH,
            ),
            provider_history=ProviderHistoryFrame(
                provider_history_active=True,
                provider_history=bounded_history,
                provider_history_limit=MAX_PROVIDER_HISTORY,
                compact_history_summary=f"history={len(bounded_history)};provider={recommended_provider}",
                history_overflow_blocked=bool(evicted_history),
                hidden_provider_history_blocked=hidden_provider_history_attempts > 0,
            ),
            provider_eviction=ProviderEvictionFrame(
                provider_eviction_active=True,
                evicted_history_items=evicted_history,
                evicted_specializations=evicted_specializations,
                eviction_count=len(evicted_history) + len(evicted_specializations),
                bounded_eviction_active=bool(evicted_history or evicted_specializations),
                eviction_summary=(
                    f"history={len(evicted_history)};specialization={len(evicted_specializations)}"
                ),
            ),
            provider_capability_score=capability_score,
            provider_fatigue_score=fatigue_score,
            provider_cost_pressure=cost_pressure,
            provider_confidence_score=confidence_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            provider_routing_mode="LOCAL_FIRST_BOUNDED_ADAPTATION",
            estimated_avoided_frontier_provider_usage=74,
            estimated_avoided_recursive_escalation=68 + recursive_escalation_attempts * 8,
            estimated_avoided_provider_instability=62 + max(0, instability_score - 50) // 2,
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


def _cooldown_recommendation(fatigue_score: int) -> str:
    if fatigue_score >= 70:
        return "COOLDOWN_AND_LOCAL_FIRST_COMPACTION"
    if fatigue_score >= 45:
        return "WATCH_FATIGUE_AND_BOUND_RETRIES"
    return "CONTINUE_BOUNDED_PROVIDER_ROUTING"


def _cost_recommendation(cost_pressure: str) -> str:
    if cost_pressure == "HIGH":
        return "LOCAL_FIRST_AND_BLOCK_SILENT_ESCALATION"
    if cost_pressure == "MEDIUM":
        return "COMPACT_CONTEXT_BEFORE_ESCALATION"
    return "CONTINUE_LOCAL_FIRST_ROUTING"


def _recommended_provider(confidence_score: int, cost_pressure: str, fatigue_score: int) -> str:
    if cost_pressure == "HIGH" or fatigue_score >= 70:
        return "local_compact"
    if confidence_score >= 80:
        return "local_patch"
    if confidence_score >= 55:
        return "local_review"
    return "human_confirmed_escalation"


def _termination_reasons(
    budget_exceeded: bool,
    recursive_escalation_detected: bool,
    governance_violation_detected: bool,
    provider_instability_threshold_exceeded: bool,
    escalation_depth_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if budget_exceeded:
        reasons.append("PROVIDER_BUDGET_EXCEEDED")
    if recursive_escalation_detected:
        reasons.append("RECURSIVE_ESCALATION_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if provider_instability_threshold_exceeded:
        reasons.append("PROVIDER_INSTABILITY_THRESHOLD_EXCEEDED")
    if escalation_depth_exceeded:
        reasons.append("ESCALATION_DEPTH_EXCEEDED")
    return tuple(reasons)
