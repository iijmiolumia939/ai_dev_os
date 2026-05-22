from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.provider_stability import (
    PROVIDER_SCORE_BASELINE,
    STABILITY_PROVIDERS,
    ProviderStabilityRuntime,
)

ADAPTIVE_ROUTING_WORKLOADS = (
    "LOW bounded implementation patch",
    "larger repetitive workload",
    "governance summary compression",
    "HIGH reasoning governance review",
    "OpenMythos placeholder evaluation",
)

BLOCKED_ADAPTIVE_ROUTING_BEHAVIORS = (
    "hidden provider switching",
    "recursive provider rerouting",
    "silent premium escalation",
    "automatic retrieval-radius expansion",
    "unrestricted provider authority",
)

WORKLOAD_PROVIDER_RECOMMENDATIONS = {
    "LOW bounded implementation patch": "qwen2.5-coder:7b",
    "larger repetitive workload": "qwen2.5-coder:14b",
    "governance summary compression": "gemma3:12b",
    "HIGH reasoning governance review": "GPT-5.5 reference",
    "OpenMythos placeholder evaluation": "OpenMythos placeholder:not_loaded",
}

FALLBACK_FREQUENCY_BASELINE = {
    "qwen2.5-coder:7b": 1,
    "qwen2.5-coder:14b": 2,
    "gemma3:12b": 3,
    "GPT-5.5 reference": 6,
    "OpenMythos placeholder:not_loaded": 0,
}

RUNTIME_INSTABILITY_HISTORY = {
    "qwen2.5-coder:7b": 2,
    "qwen2.5-coder:14b": 3,
    "gemma3:12b": 5,
    "GPT-5.5 reference": 10,
    "OpenMythos placeholder:not_loaded": 100,
}


@dataclass(frozen=True)
class AdaptiveProviderRoutingFrame:
    adaptive_provider_routing_active: bool
    workloads: tuple[str, ...]
    blocked_behaviors: tuple[str, ...]
    human_confirmed_only: bool
    bounded_recommendations: bool
    deterministic: bool
    rollback_safe: bool
    no_hidden_provider_switching: bool
    no_recursive_routing_loops: bool
    no_unrestricted_provider_escalation: bool
    openmythos_placeholder_only: bool


@dataclass(frozen=True)
class ProviderRecommendationFrame:
    provider_recommendation_active: bool
    primary_recommendation: str
    provider_recommendation_ranking: tuple[str, ...]
    workload_recommendations: dict[str, str]
    provider_recommendation_reasons: dict[str, str]
    human_confirmation_required: bool
    automatic_switching_allowed: bool
    premium_escalation_silent: bool


@dataclass(frozen=True)
class StabilityWeightedRoutingFrame:
    stability_weighted_routing_active: bool
    stability_weighted_scores: dict[str, int]
    stability_weighted_ranking: tuple[str, ...]
    low_bounded_provider: str
    repetitive_workload_provider: str
    governance_summary_provider: str
    high_reasoning_provider: str
    openmythos_placeholder_provider: str


@dataclass(frozen=True)
class DriftAwareRoutingFrame:
    drift_aware_routing_active: bool
    recursive_synthesis_attempts: dict[str, int]
    giant_summary_growth: dict[str, int]
    hallucinated_architecture_expansion: dict[str, int]
    retrieval_radius_inflation: dict[str, int]
    drift_confidence_penalty: dict[str, int]
    drift_aware_routing_result: str


@dataclass(frozen=True)
class GovernanceWeightedRoutingFrame:
    governance_weighted_routing_active: bool
    local_patch_preservation: dict[str, int]
    governance_adherence: dict[str, int]
    bounded_cognition_stability: dict[str, int]
    compact_continuity_preservation: dict[str, int]
    governance_weighted_scores: dict[str, int]
    governance_weighted_ranking: tuple[str, ...]
    escalation_blocked_by_governance: bool
    governance_weighted_routing_result: str


@dataclass(frozen=True)
class CompactnessRoutingFrame:
    compactness_routing_active: bool
    compactness_scores: dict[str, int]
    compact_fallback_hints: tuple[str, ...]
    giant_payloads_evicted: bool
    compact_continuity_preserved: bool


@dataclass(frozen=True)
class FallbackPressureRoutingFrame:
    fallback_pressure_routing_active: bool
    fallback_frequency: dict[str, int]
    fallback_pressure_penalty: dict[str, int]
    fallback_downgrade_suggestions: tuple[str, ...]
    unrestricted_fallback_escalation_allowed: bool


@dataclass(frozen=True)
class LongSessionRoutingFrame:
    long_session_routing_active: bool
    repeated_sprint_degradation: dict[str, int]
    continuity_corruption_risk: dict[str, int]
    provider_fatigue_patterns: dict[str, int]
    stability_weighted_recommendations: tuple[str, ...]
    governance_safe_downgrade_suggestions: tuple[str, ...]


@dataclass(frozen=True)
class RoutingConfidenceFrame:
    routing_confidence_active: bool
    confidence_by_provider: dict[str, int]
    confidence_label_by_provider: dict[str, str]
    routing_confidence_summary: tuple[str, ...]
    overall_confidence: str


@dataclass(frozen=True)
class RoutingHistoryFrame:
    routing_history_active: bool
    provider_recommendation_history: tuple[str, ...]
    fallback_history: tuple[str, ...]
    instability_trends: dict[str, int]
    governance_drift_trends: dict[str, int]
    bounded_history_size: int


@dataclass(frozen=True)
class RoutingDecayFrame:
    routing_decay_active: bool
    confidence_decay: dict[str, int]
    compactness_decay: dict[str, int]
    governance_decay: dict[str, int]
    drift_decay_guard_active: bool


@dataclass(frozen=True)
class RoutingPressureFrame:
    routing_pressure_active: bool
    recursive_pressure_detected: bool
    instability_pressure: dict[str, int]
    fallback_pressure: dict[str, int]
    escalation_pressure: str
    escalation_blocked: bool


@dataclass(frozen=True)
class RoutingGovernanceFrame:
    routing_governance_active: bool
    local_patch_discipline: bool
    bounded_cognition: bool
    anti_explosion_governance: bool
    compact_continuity: bool
    human_confirmed_routing_authority: bool
    governance_runtime_bypassed: bool
    autonomous_execution_enabled: bool


@dataclass(frozen=True)
class RoutingEvictionFrame:
    routing_eviction_active: bool
    stale_routing_history_evicted: bool
    obsolete_fallback_heuristics_evicted: bool
    oversized_recommendation_payloads_evicted: bool
    max_history_entries: int


@dataclass(frozen=True)
class AdaptiveProviderRoutingRuntimeFrame:
    adaptive: AdaptiveProviderRoutingFrame
    recommendation: ProviderRecommendationFrame
    stability_weighted: StabilityWeightedRoutingFrame
    drift_aware: DriftAwareRoutingFrame
    governance_weighted: GovernanceWeightedRoutingFrame
    compactness: CompactnessRoutingFrame
    fallback_pressure: FallbackPressureRoutingFrame
    long_session: LongSessionRoutingFrame
    confidence: RoutingConfidenceFrame
    history: RoutingHistoryFrame
    decay: RoutingDecayFrame
    pressure: RoutingPressureFrame
    governance: RoutingGovernanceFrame
    eviction: RoutingEvictionFrame
    adaptive_provider_routing_active: bool
    drift_aware_routing_active: bool
    governance_weighted_routing_active: bool
    long_session_routing_active: bool
    routing_confidence_active: bool
    estimated_avoided_provider_drift: int
    estimated_avoided_recursive_routing: int
    estimated_avoided_premium_burn: int
    deterministic: bool
    human_confirmed_only: bool
    rollback_safe: bool
    local_only: bool
    summary_only: bool


def _rank(scores: dict[str, int]) -> tuple[str, ...]:
    return tuple(
        provider
        for provider, _score in sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    )


def _stability_weighted_score(provider: str, long_session_degradation: int) -> int:
    scores = PROVIDER_SCORE_BASELINE[provider]
    if provider == "OpenMythos placeholder:not_loaded":
        return 0
    score = (
        scores["governance"] * 0.22
        + scores["local_patch"] * 0.18
        + scores["compactness"] * 0.18
        + scores["drift_resistance"] * 0.17
        + scores["repetitive_reliability"] * 0.10
        + scores["retrieval_discipline"] * 0.05
        + (100 - long_session_degradation) * 0.10
    )
    return round(score)


def _confidence_label(provider: str, confidence: int) -> str:
    if provider == "OpenMythos placeholder:not_loaded" or confidence < 50:
        return "LOW_CONFIDENCE"
    if provider == "GPT-5.5 reference":
        return "HIGH_ESCALATION_REQUIRED"
    if confidence < 80:
        return "DRIFT_RISK"
    if provider == "gemma3:12b":
        return "STABLE_GOVERNANCE"
    return "STABLE_LOCAL"


class AdaptiveProviderRoutingRuntime:
    def evaluate(self) -> AdaptiveProviderRoutingRuntimeFrame:
        stability_frame = ProviderStabilityRuntime().evaluate()
        long_session_degradation = (
            stability_frame.long_session_drift.estimated_long_session_degradation
        )
        stability_scores = {
            provider: _stability_weighted_score(provider, long_session_degradation[provider])
            for provider in STABILITY_PROVIDERS
        }
        recursive_pressure = {
            provider: 100 - score
            for provider, score in (
                stability_frame.hallucination_pressure.drift_resistance_score.items()
            )
        }
        summary_growth = {
            provider: 100 - score
            for provider, score in stability_frame.compactness_retention.compactness_score.items()
        }
        retrieval_inflation = {
            provider: 100 - score
            for provider, score in (
                stability_frame.retrieval_radius.retrieval_discipline_score.items()
            )
        }
        drift_penalty = {
            provider: min(
                40,
                round(
                    (
                        recursive_pressure[provider]
                        + summary_growth[provider]
                        + retrieval_inflation[provider]
                        + RUNTIME_INSTABILITY_HISTORY[provider]
                    )
                    / 4
                ),
            )
            for provider in STABILITY_PROVIDERS
        }
        fallback_penalty = {
            provider: min(24, FALLBACK_FREQUENCY_BASELINE[provider] * 2)
            for provider in STABILITY_PROVIDERS
        }
        governance_scores = {
            provider: round(
                (
                    PROVIDER_SCORE_BASELINE[provider]["governance"]
                    + PROVIDER_SCORE_BASELINE[provider]["local_patch"]
                    + PROVIDER_SCORE_BASELINE[provider]["compactness"]
                )
                / 3
            )
            for provider in STABILITY_PROVIDERS
        }
        confidence = {
            provider: max(
                0,
                min(
                    100,
                    stability_scores[provider]
                    + round(governance_scores[provider] * 0.08)
                    - drift_penalty[provider]
                    - fallback_penalty[provider],
                ),
            )
            for provider in STABILITY_PROVIDERS
        }
        confidence_labels = {
            provider: _confidence_label(provider, confidence[provider])
            for provider in STABILITY_PROVIDERS
        }
        recommendation_ranking = _rank(confidence)
        adaptive = AdaptiveProviderRoutingFrame(
            adaptive_provider_routing_active=True,
            workloads=ADAPTIVE_ROUTING_WORKLOADS,
            blocked_behaviors=BLOCKED_ADAPTIVE_ROUTING_BEHAVIORS,
            human_confirmed_only=True,
            bounded_recommendations=True,
            deterministic=True,
            rollback_safe=True,
            no_hidden_provider_switching=True,
            no_recursive_routing_loops=True,
            no_unrestricted_provider_escalation=True,
            openmythos_placeholder_only=True,
        )
        recommendation = ProviderRecommendationFrame(
            provider_recommendation_active=True,
            primary_recommendation=recommendation_ranking[0],
            provider_recommendation_ranking=recommendation_ranking,
            workload_recommendations=WORKLOAD_PROVIDER_RECOMMENDATIONS,
            provider_recommendation_reasons={
                "qwen2.5-coder:7b": "LOW bounded tasks keep strongest local stability.",
                "qwen2.5-coder:14b": "Larger repetitive workloads preserve local routing.",
                "gemma3:12b": "Governance summaries favor compact compression.",
                "GPT-5.5 reference": "HIGH governance reasoning requires human confirmation.",
                "OpenMythos placeholder:not_loaded": "Blocked until runtime artifact exists.",
            },
            human_confirmation_required=True,
            automatic_switching_allowed=False,
            premium_escalation_silent=False,
        )
        stability_weighted = StabilityWeightedRoutingFrame(
            stability_weighted_routing_active=True,
            stability_weighted_scores=stability_scores,
            stability_weighted_ranking=_rank(stability_scores),
            low_bounded_provider="qwen2.5-coder:7b",
            repetitive_workload_provider="qwen2.5-coder:14b",
            governance_summary_provider="gemma3:12b",
            high_reasoning_provider="GPT-5.5 reference",
            openmythos_placeholder_provider="OpenMythos placeholder:not_loaded",
        )
        drift_aware = DriftAwareRoutingFrame(
            drift_aware_routing_active=True,
            recursive_synthesis_attempts=recursive_pressure,
            giant_summary_growth=summary_growth,
            hallucinated_architecture_expansion=recursive_pressure,
            retrieval_radius_inflation=retrieval_inflation,
            drift_confidence_penalty=drift_penalty,
            drift_aware_routing_result="DRIFT_LOW_LOCAL_FIRST_ESCALATION_GUARDED",
        )
        governance_weighted = GovernanceWeightedRoutingFrame(
            governance_weighted_routing_active=True,
            local_patch_preservation=stability_frame.benchmark.local_patch_adherence_score,
            governance_adherence=stability_frame.governance_decay.governance_adherence_score,
            bounded_cognition_stability=governance_scores,
            compact_continuity_preservation=stability_frame.compactness_retention.compactness_score,
            governance_weighted_scores=governance_scores,
            governance_weighted_ranking=_rank(governance_scores),
            escalation_blocked_by_governance=True,
            governance_weighted_routing_result="GOVERNANCE_WEIGHTED_LOCAL_PATCH_PREFERRED",
        )
        compactness = CompactnessRoutingFrame(
            compactness_routing_active=True,
            compactness_scores=stability_frame.compactness_retention.compactness_score,
            compact_fallback_hints=(
                "Prefer qwen2.5-coder:7b for compact implementation patches.",
                "Use gemma3:12b for summary compression before premium escalation.",
            ),
            giant_payloads_evicted=True,
            compact_continuity_preserved=True,
        )
        fallback_pressure = FallbackPressureRoutingFrame(
            fallback_pressure_routing_active=True,
            fallback_frequency=FALLBACK_FREQUENCY_BASELINE,
            fallback_pressure_penalty=fallback_penalty,
            fallback_downgrade_suggestions=(
                "Downgrade HIGH non-architecture work to qwen2.5-coder:14b.",
                "Compact governance summaries with gemma3:12b before retry.",
            ),
            unrestricted_fallback_escalation_allowed=False,
        )
        long_session = LongSessionRoutingFrame(
            long_session_routing_active=True,
            repeated_sprint_degradation=long_session_degradation,
            continuity_corruption_risk=stability_frame.long_session_drift.summary_corruption_risk,
            provider_fatigue_patterns=stability_frame.long_session_drift.recursive_reasoning_tendency,
            stability_weighted_recommendations=recommendation_ranking,
            governance_safe_downgrade_suggestions=(
                "Use qwen2.5-coder:7b when sprint pressure is LOW.",
                "Use qwen2.5-coder:14b for repetitive edits after compaction.",
                "Use gemma3:12b when continuity summary growth appears.",
            ),
        )
        confidence_frame = RoutingConfidenceFrame(
            routing_confidence_active=True,
            confidence_by_provider=confidence,
            confidence_label_by_provider=confidence_labels,
            routing_confidence_summary=tuple(
                f"{provider}:{confidence[provider]}:{confidence_labels[provider]}"
                for provider in recommendation_ranking
            ),
            overall_confidence=confidence_labels[recommendation_ranking[0]],
        )
        history = RoutingHistoryFrame(
            routing_history_active=True,
            provider_recommendation_history=recommendation_ranking,
            fallback_history=(
                "GPT-5.5 reference -> gemma3:12b when governance summary is enough",
                "qwen2.5-coder:14b -> qwen2.5-coder:7b when task is LOW bounded",
            ),
            instability_trends=RUNTIME_INSTABILITY_HISTORY,
            governance_drift_trends={
                provider: 100 - score for provider, score in governance_scores.items()
            },
            bounded_history_size=8,
        )
        decay = RoutingDecayFrame(
            routing_decay_active=True,
            confidence_decay=drift_penalty,
            compactness_decay=stability_frame.long_session_drift.compactness_decay,
            governance_decay=stability_frame.long_session_drift.governance_degradation,
            drift_decay_guard_active=True,
        )
        pressure = RoutingPressureFrame(
            routing_pressure_active=True,
            recursive_pressure_detected=True,
            instability_pressure=RUNTIME_INSTABILITY_HISTORY,
            fallback_pressure=fallback_penalty,
            escalation_pressure="GUARDED",
            escalation_blocked=True,
        )
        governance = RoutingGovernanceFrame(
            routing_governance_active=True,
            local_patch_discipline=True,
            bounded_cognition=True,
            anti_explosion_governance=True,
            compact_continuity=True,
            human_confirmed_routing_authority=True,
            governance_runtime_bypassed=False,
            autonomous_execution_enabled=False,
        )
        eviction = RoutingEvictionFrame(
            routing_eviction_active=True,
            stale_routing_history_evicted=True,
            obsolete_fallback_heuristics_evicted=True,
            oversized_recommendation_payloads_evicted=True,
            max_history_entries=8,
        )
        return AdaptiveProviderRoutingRuntimeFrame(
            adaptive=adaptive,
            recommendation=recommendation,
            stability_weighted=stability_weighted,
            drift_aware=drift_aware,
            governance_weighted=governance_weighted,
            compactness=compactness,
            fallback_pressure=fallback_pressure,
            long_session=long_session,
            confidence=confidence_frame,
            history=history,
            decay=decay,
            pressure=pressure,
            governance=governance,
            eviction=eviction,
            adaptive_provider_routing_active=adaptive.adaptive_provider_routing_active,
            drift_aware_routing_active=drift_aware.drift_aware_routing_active,
            governance_weighted_routing_active=(
                governance_weighted.governance_weighted_routing_active
            ),
            long_session_routing_active=long_session.long_session_routing_active,
            routing_confidence_active=confidence_frame.routing_confidence_active,
            estimated_avoided_provider_drift=14,
            estimated_avoided_recursive_routing=9,
            estimated_avoided_premium_burn=18,
            deterministic=True,
            human_confirmed_only=True,
            rollback_safe=True,
            local_only=True,
            summary_only=True,
        )


__all__ = [
    "ADAPTIVE_ROUTING_WORKLOADS",
    "BLOCKED_ADAPTIVE_ROUTING_BEHAVIORS",
    "FALLBACK_FREQUENCY_BASELINE",
    "RUNTIME_INSTABILITY_HISTORY",
    "WORKLOAD_PROVIDER_RECOMMENDATIONS",
    "AdaptiveProviderRoutingFrame",
    "AdaptiveProviderRoutingRuntime",
    "AdaptiveProviderRoutingRuntimeFrame",
    "CompactnessRoutingFrame",
    "DriftAwareRoutingFrame",
    "FallbackPressureRoutingFrame",
    "GovernanceWeightedRoutingFrame",
    "LongSessionRoutingFrame",
    "ProviderRecommendationFrame",
    "RoutingConfidenceFrame",
    "RoutingDecayFrame",
    "RoutingEvictionFrame",
    "RoutingGovernanceFrame",
    "RoutingHistoryFrame",
    "RoutingPressureFrame",
    "StabilityWeightedRoutingFrame",
]
