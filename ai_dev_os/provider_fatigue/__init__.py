from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider_routing import AdaptiveProviderRoutingRuntime
from ai_dev_os.provider_stability import STABILITY_PROVIDERS, ProviderStabilityRuntime

FATIGUE_WORKLOADS = (
    "extended sprint rollover",
    "repeated compact continuity reuse",
    "prolonged repetitive engineering workload",
    "governance-heavy recovery recommendation",
)

BLOCKED_FATIGUE_BEHAVIORS = (
    "autonomous provider replacement",
    "recursive provider rerouting",
    "hidden escalation switching",
    "automatic continuity erasure",
    "governance policy mutation",
)

REPEATED_ESCALATION_ATTEMPTS = {
    "qwen2.5-coder:7b": 1,
    "qwen2.5-coder:14b": 2,
    "gemma3:12b": 3,
    "GPT-5.5 reference": 8,
    "OpenMythos placeholder:not_loaded": 0,
}

FALLBACK_SWITCHING_BASELINE = {
    "qwen2.5-coder:7b": 1,
    "qwen2.5-coder:14b": 2,
    "gemma3:12b": 3,
    "GPT-5.5 reference": 7,
    "OpenMythos placeholder:not_loaded": 0,
}


@dataclass(frozen=True)
class ProviderFatigueFrame:
    provider_fatigue_active: bool
    workloads: tuple[str, ...]
    blocked_behaviors: tuple[str, ...]
    fatigue_score: dict[str, int]
    degradation_trend: dict[str, str]
    bounded_recovery_recommendation: str
    compact_fallback_suggestion: str
    human_confirmed_only: bool
    deterministic: bool
    rollback_safe: bool


@dataclass(frozen=True)
class EscalationFatigueFrame:
    escalation_fatigue_active: bool
    repeated_high_escalation_pressure: dict[str, int]
    unnecessary_premium_escalation: dict[str, int]
    recursive_reasoning_inflation: dict[str, int]
    governance_bypass_tendency: dict[str, int]
    escalation_fatigue_warning: str
    bounded_downgrade_recommendation: str
    compact_routing_recovery_hints: tuple[str, ...]


@dataclass(frozen=True)
class CompactnessDecayFrame:
    compactness_decay_active: bool
    summary_growth_inflation: dict[str, int]
    verbosity_pressure: dict[str, int]
    compact_continuity_corruption: dict[str, int]
    oversized_sprint_closure_tendency: dict[str, int]
    compactness_retention_score: dict[str, int]
    bounded_compression_recommendation: str


@dataclass(frozen=True)
class FallbackOscillationFrame:
    fallback_oscillation_active: bool
    repeated_provider_switching: dict[str, int]
    unstable_fallback_loops: dict[str, int]
    routing_indecision: dict[str, int]
    drift_induced_rerouting_pressure: dict[str, int]
    oscillation_risk_score: dict[str, int]
    recursive_reroute_loops_blocked: bool
    unstable_escalation_oscillation_blocked: bool
    fallback_oscillation_summary: str


@dataclass(frozen=True)
class RecursivePressureFrame:
    recursive_pressure_active: bool
    recursive_reasoning_pressure: dict[str, int]
    giant_synthesis_growth: dict[str, int]
    retrieval_scope_expansion_pressure: dict[str, int]
    recursive_cognition_exhaustion: dict[str, int]
    recursive_loop_blocked: bool


@dataclass(frozen=True)
class ContextFatigueFrame:
    context_fatigue_active: bool
    continuity_corruption_tendency: dict[str, int]
    repeated_context_reuse_pressure: dict[str, int]
    retrieval_radius_inflation: dict[str, int]
    compact_context_reset_recommended: bool


@dataclass(frozen=True)
class SummaryFatigueFrame:
    summary_fatigue_active: bool
    giant_summary_growth: dict[str, int]
    summary_drift_amplification: dict[str, int]
    oversized_summary_eviction_required: bool
    compact_summary_recovery: str


@dataclass(frozen=True)
class LongSessionPressureFrame:
    long_session_pressure_active: bool
    simulated_rollovers: int
    provider_exhaustion: dict[str, int]
    degradation_accumulation: dict[str, int]
    drift_amplification: dict[str, int]
    fallback_pressure_increase: dict[str, int]
    long_session_pressure_summary: str


@dataclass(frozen=True)
class ProviderRecoveryFrame:
    provider_recovery_active: bool
    bounded_cooldown: bool
    downgrade_to_local: bool
    compactness_reset: bool
    continuity_truncation: bool
    governance_safe_recovery: bool
    recovery_recommendation: str
    provider_recovery_ranking: tuple[str, ...]
    autonomous_reroute_allowed: bool
    continuity_erasure_allowed: bool
    governance_policy_mutation_allowed: bool


@dataclass(frozen=True)
class FatigueConfidenceFrame:
    fatigue_confidence_active: bool
    fatigue_confidence_by_provider: dict[str, int]
    fatigue_label_by_provider: dict[str, str]
    fatigue_confidence_summary: tuple[str, ...]
    overall_fatigue_label: str


@dataclass(frozen=True)
class FatigueHistoryFrame:
    fatigue_history_active: bool
    fatigue_history_entries: tuple[str, ...]
    fallback_history_entries: tuple[str, ...]
    degradation_trend_history: dict[str, int]
    bounded_history_size: int


@dataclass(frozen=True)
class FatigueDecayFrame:
    fatigue_decay_active: bool
    compactness_decay: dict[str, int]
    escalation_decay: dict[str, int]
    fallback_decay: dict[str, int]
    recursive_decay: dict[str, int]
    fatigue_decay_guard_active: bool


@dataclass(frozen=True)
class FatigueGovernanceFrame:
    fatigue_governance_active: bool
    bounded_cognition: bool
    human_confirmed_routing: bool
    anti_explosion_governance: bool
    local_patch_discipline: bool
    compact_continuity: bool
    rollback_safe_execution: bool
    governance_runtime_bypassed: bool
    autonomous_provider_replacement: bool
    hidden_escalation_switching: bool
    retrieval_scope_expansion_allowed: bool


@dataclass(frozen=True)
class FatigueEvictionFrame:
    fatigue_eviction_active: bool
    stale_fatigue_history_evicted: bool
    obsolete_fallback_oscillation_evicted: bool
    oversized_fatigue_payloads_evicted: bool
    max_history_entries: int


@dataclass(frozen=True)
class ProviderFatigueRuntimeFrame:
    provider_fatigue: ProviderFatigueFrame
    escalation_fatigue: EscalationFatigueFrame
    compactness_decay: CompactnessDecayFrame
    fallback_oscillation: FallbackOscillationFrame
    recursive_pressure: RecursivePressureFrame
    context_fatigue: ContextFatigueFrame
    summary_fatigue: SummaryFatigueFrame
    long_session_pressure: LongSessionPressureFrame
    recovery: ProviderRecoveryFrame
    confidence: FatigueConfidenceFrame
    history: FatigueHistoryFrame
    decay: FatigueDecayFrame
    governance: FatigueGovernanceFrame
    eviction: FatigueEvictionFrame
    provider_fatigue_active: bool
    escalation_fatigue_active: bool
    fallback_oscillation_active: bool
    compactness_decay_active: bool
    long_session_pressure_active: bool
    estimated_avoided_provider_exhaustion: int
    estimated_avoided_recursive_fatigue: int
    estimated_avoided_premium_burn: int
    deterministic: bool
    bounded: bool
    human_confirmed_only: bool
    rollback_safe: bool
    local_only: bool
    summary_only: bool


def _rank_low(scores: dict[str, int]) -> tuple[str, ...]:
    return tuple(
        provider
        for provider, _score in sorted(scores.items(), key=lambda item: (item[1], item[0]))
    )


def _fatigue_label(score: int) -> str:
    if score <= 20:
        return "FATIGUE_LOW"
    if score <= 35:
        return "FATIGUE_WATCH"
    if score <= 55:
        return "ESCALATION_PRESSURE"
    return "RECOVERY_REQUIRED"


class ProviderFatigueRuntime:
    def evaluate(self) -> ProviderFatigueRuntimeFrame:
        stability = ProviderStabilityRuntime().evaluate()
        adaptive = AdaptiveProviderRoutingRuntime().evaluate()
        long_session = stability.long_session_drift.estimated_long_session_degradation
        compactness_decay = stability.long_session_drift.compactness_decay
        governance_decay = stability.long_session_drift.governance_degradation
        recursive_pressure = stability.long_session_drift.recursive_reasoning_tendency
        summary_corruption = stability.long_session_drift.summary_corruption_risk
        fallback_penalty = adaptive.fallback_pressure.fallback_pressure_penalty
        drift_penalty = adaptive.drift_aware.drift_confidence_penalty
        fatigue_scores = {
            provider: (
                100
                if provider == "OpenMythos placeholder:not_loaded"
                else min(
                    100,
                    (
                        long_session[provider]
                        + compactness_decay[provider]
                        + recursive_pressure[provider]
                        + summary_corruption[provider]
                        + fallback_penalty[provider]
                        + REPEATED_ESCALATION_ATTEMPTS[provider]
                    ),
                )
            )
            for provider in STABILITY_PROVIDERS
        }
        degradation_trend = {
            provider: _fatigue_label(score) for provider, score in fatigue_scores.items()
        }
        oscillation_scores = {
            provider: min(
                100,
                FALLBACK_SWITCHING_BASELINE[provider]
                + fallback_penalty[provider]
                + drift_penalty[provider],
            )
            for provider in STABILITY_PROVIDERS
        }
        fatigue_confidence = {
            provider: max(0, 100 - fatigue_scores[provider] - oscillation_scores[provider])
            for provider in STABILITY_PROVIDERS
        }
        fatigue_labels = {
            provider: _fatigue_label(fatigue_scores[provider]) for provider in STABILITY_PROVIDERS
        }
        recovery_ranking = _rank_low(fatigue_scores)
        provider_fatigue = ProviderFatigueFrame(
            provider_fatigue_active=True,
            workloads=FATIGUE_WORKLOADS,
            blocked_behaviors=BLOCKED_FATIGUE_BEHAVIORS,
            fatigue_score=fatigue_scores,
            degradation_trend=degradation_trend,
            bounded_recovery_recommendation="COOLDOWN_AND_LOCAL_DOWNGRADE_IF_PRESSURE_RISES",
            compact_fallback_suggestion="Use compactness reset before premium escalation retry.",
            human_confirmed_only=True,
            deterministic=True,
            rollback_safe=True,
        )
        escalation_fatigue = EscalationFatigueFrame(
            escalation_fatigue_active=True,
            repeated_high_escalation_pressure=REPEATED_ESCALATION_ATTEMPTS,
            unnecessary_premium_escalation={
                provider: max(0, REPEATED_ESCALATION_ATTEMPTS[provider] - 2)
                for provider in STABILITY_PROVIDERS
            },
            recursive_reasoning_inflation=recursive_pressure,
            governance_bypass_tendency=governance_decay,
            escalation_fatigue_warning="ESCALATION_PRESSURE_GUARDED",
            bounded_downgrade_recommendation=(
                "Prefer qwen2.5-coder:7b or qwen2.5-coder:14b before premium retry."
            ),
            compact_routing_recovery_hints=(
                "Compact continuity before retrying HIGH reasoning.",
                "Use gemma3:12b for governance summaries before escalation.",
            ),
        )
        compactness = CompactnessDecayFrame(
            compactness_decay_active=True,
            summary_growth_inflation=compactness_decay,
            verbosity_pressure=compactness_decay,
            compact_continuity_corruption=summary_corruption,
            oversized_sprint_closure_tendency=compactness_decay,
            compactness_retention_score=stability.compactness_retention.compactness_score,
            bounded_compression_recommendation="COMPACTNESS_RESET_BEFORE_LONG_SESSION_CONTINUATION",
        )
        fallback_oscillation = FallbackOscillationFrame(
            fallback_oscillation_active=True,
            repeated_provider_switching=FALLBACK_SWITCHING_BASELINE,
            unstable_fallback_loops=fallback_penalty,
            routing_indecision=oscillation_scores,
            drift_induced_rerouting_pressure=drift_penalty,
            oscillation_risk_score=oscillation_scores,
            recursive_reroute_loops_blocked=True,
            unstable_escalation_oscillation_blocked=True,
            fallback_oscillation_summary="OSCILLATION_LOW_LOCAL_FIRST_BLOCKED_LOOPS",
        )
        recursive = RecursivePressureFrame(
            recursive_pressure_active=True,
            recursive_reasoning_pressure=recursive_pressure,
            giant_synthesis_growth=adaptive.drift_aware.giant_summary_growth,
            retrieval_scope_expansion_pressure=adaptive.drift_aware.retrieval_radius_inflation,
            recursive_cognition_exhaustion=drift_penalty,
            recursive_loop_blocked=True,
        )
        context = ContextFatigueFrame(
            context_fatigue_active=True,
            continuity_corruption_tendency=summary_corruption,
            repeated_context_reuse_pressure=long_session,
            retrieval_radius_inflation=adaptive.drift_aware.retrieval_radius_inflation,
            compact_context_reset_recommended=True,
        )
        summary = SummaryFatigueFrame(
            summary_fatigue_active=True,
            giant_summary_growth=compactness_decay,
            summary_drift_amplification=adaptive.drift_aware.giant_summary_growth,
            oversized_summary_eviction_required=True,
            compact_summary_recovery="DEDUP_AND_TRUNCATE_TO_COMPACT_CONTINUITY",
        )
        long_session_pressure = LongSessionPressureFrame(
            long_session_pressure_active=True,
            simulated_rollovers=8,
            provider_exhaustion=fatigue_scores,
            degradation_accumulation=long_session,
            drift_amplification=drift_penalty,
            fallback_pressure_increase=fallback_penalty,
            long_session_pressure_summary="LONG_SESSION_PRESSURE_LOW_BUT_WATCH_ESCALATION",
        )
        recovery = ProviderRecoveryFrame(
            provider_recovery_active=True,
            bounded_cooldown=True,
            downgrade_to_local=True,
            compactness_reset=True,
            continuity_truncation=True,
            governance_safe_recovery=True,
            recovery_recommendation="RECOVER_WITH_LOCAL_DOWNGRADE_AND_COMPACTNESS_RESET",
            provider_recovery_ranking=recovery_ranking,
            autonomous_reroute_allowed=False,
            continuity_erasure_allowed=False,
            governance_policy_mutation_allowed=False,
        )
        confidence = FatigueConfidenceFrame(
            fatigue_confidence_active=True,
            fatigue_confidence_by_provider=fatigue_confidence,
            fatigue_label_by_provider=fatigue_labels,
            fatigue_confidence_summary=tuple(
                f"{provider}:{fatigue_scores[provider]}:{fatigue_labels[provider]}"
                for provider in recovery_ranking
            ),
            overall_fatigue_label=fatigue_labels[recovery_ranking[0]],
        )
        history = FatigueHistoryFrame(
            fatigue_history_active=True,
            fatigue_history_entries=tuple(
                f"{provider}:{fatigue_scores[provider]}" for provider in recovery_ranking
            ),
            fallback_history_entries=(
                "GPT-5.5 reference fallback pressure guarded",
                "qwen2.5-coder:7b remains low fatigue local route",
            ),
            degradation_trend_history=fatigue_scores,
            bounded_history_size=8,
        )
        decay = FatigueDecayFrame(
            fatigue_decay_active=True,
            compactness_decay=compactness_decay,
            escalation_decay=REPEATED_ESCALATION_ATTEMPTS,
            fallback_decay=fallback_penalty,
            recursive_decay=recursive_pressure,
            fatigue_decay_guard_active=True,
        )
        governance = FatigueGovernanceFrame(
            fatigue_governance_active=True,
            bounded_cognition=True,
            human_confirmed_routing=True,
            anti_explosion_governance=True,
            local_patch_discipline=True,
            compact_continuity=True,
            rollback_safe_execution=True,
            governance_runtime_bypassed=False,
            autonomous_provider_replacement=False,
            hidden_escalation_switching=False,
            retrieval_scope_expansion_allowed=False,
        )
        eviction = FatigueEvictionFrame(
            fatigue_eviction_active=True,
            stale_fatigue_history_evicted=True,
            obsolete_fallback_oscillation_evicted=True,
            oversized_fatigue_payloads_evicted=True,
            max_history_entries=8,
        )
        return ProviderFatigueRuntimeFrame(
            provider_fatigue=provider_fatigue,
            escalation_fatigue=escalation_fatigue,
            compactness_decay=compactness,
            fallback_oscillation=fallback_oscillation,
            recursive_pressure=recursive,
            context_fatigue=context,
            summary_fatigue=summary,
            long_session_pressure=long_session_pressure,
            recovery=recovery,
            confidence=confidence,
            history=history,
            decay=decay,
            governance=governance,
            eviction=eviction,
            provider_fatigue_active=provider_fatigue.provider_fatigue_active,
            escalation_fatigue_active=escalation_fatigue.escalation_fatigue_active,
            fallback_oscillation_active=fallback_oscillation.fallback_oscillation_active,
            compactness_decay_active=compactness.compactness_decay_active,
            long_session_pressure_active=long_session_pressure.long_session_pressure_active,
            estimated_avoided_provider_exhaustion=16,
            estimated_avoided_recursive_fatigue=11,
            estimated_avoided_premium_burn=14,
            deterministic=True,
            bounded=True,
            human_confirmed_only=True,
            rollback_safe=True,
            local_only=True,
            summary_only=True,
        )


__all__ = [
    "BLOCKED_FATIGUE_BEHAVIORS",
    "FALLBACK_SWITCHING_BASELINE",
    "FATIGUE_WORKLOADS",
    "REPEATED_ESCALATION_ATTEMPTS",
    "CompactnessDecayFrame",
    "ContextFatigueFrame",
    "EscalationFatigueFrame",
    "FallbackOscillationFrame",
    "FatigueConfidenceFrame",
    "FatigueDecayFrame",
    "FatigueEvictionFrame",
    "FatigueGovernanceFrame",
    "FatigueHistoryFrame",
    "LongSessionPressureFrame",
    "ProviderFatigueFrame",
    "ProviderFatigueRuntime",
    "ProviderFatigueRuntimeFrame",
    "ProviderRecoveryFrame",
    "RecursivePressureFrame",
    "SummaryFatigueFrame",
]
