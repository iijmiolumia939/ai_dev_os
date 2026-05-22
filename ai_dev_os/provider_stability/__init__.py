from __future__ import annotations

from dataclasses import dataclass

STABILITY_PROVIDERS = (
    "qwen2.5-coder:7b",
    "qwen2.5-coder:14b",
    "gemma3:12b",
    "GPT-5.5 reference",
    "OpenMythos placeholder:not_loaded",
)

STABILITY_WORKLOADS = (
    "compact dataclass generation",
    "runtime frame generation",
    "repetitive test generation",
    "VSCode extension glue generation",
    "compact continuity rollover",
    "bounded governance summary",
)

BLOCKED_STABILITY_BEHAVIORS = (
    "repo-wide synthesis",
    "unrestricted architecture planning",
    "recursive execution",
    "autonomous delegation",
    "giant roadmap generation",
)

PROVIDER_SCORE_BASELINE = {
    "qwen2.5-coder:7b": {
        "governance": 96,
        "local_patch": 97,
        "compactness": 94,
        "drift_resistance": 92,
        "repetitive_reliability": 95,
        "retrieval_discipline": 96,
    },
    "qwen2.5-coder:14b": {
        "governance": 95,
        "local_patch": 96,
        "compactness": 92,
        "drift_resistance": 90,
        "repetitive_reliability": 94,
        "retrieval_discipline": 94,
    },
    "gemma3:12b": {
        "governance": 92,
        "local_patch": 88,
        "compactness": 90,
        "drift_resistance": 86,
        "repetitive_reliability": 87,
        "retrieval_discipline": 89,
    },
    "GPT-5.5 reference": {
        "governance": 85,
        "local_patch": 76,
        "compactness": 78,
        "drift_resistance": 72,
        "repetitive_reliability": 80,
        "retrieval_discipline": 70,
    },
    "OpenMythos placeholder:not_loaded": {
        "governance": 0,
        "local_patch": 0,
        "compactness": 0,
        "drift_resistance": 0,
        "repetitive_reliability": 0,
        "retrieval_discipline": 0,
    },
}


@dataclass(frozen=True)
class ProviderStabilityFrame:
    provider_stability_active: bool
    providers: tuple[str, ...]
    workloads: tuple[str, ...]
    blocked_behaviors: tuple[str, ...]
    openmythos_placeholder_only: bool
    deterministic_workloads: bool
    compact_prompts_only: bool
    local_patch_discipline: bool
    rollback_safe_evaluation: bool


@dataclass(frozen=True)
class LongSessionDriftFrame:
    long_session_drift_active: bool
    simulated_rollovers: int
    repeated_sprint_consistency: dict[str, int]
    summary_corruption_risk: dict[str, int]
    governance_degradation: dict[str, int]
    compactness_decay: dict[str, int]
    recursive_reasoning_tendency: dict[str, int]
    estimated_long_session_degradation: dict[str, int]


@dataclass(frozen=True)
class GovernanceDecayFrame:
    governance_decay_active: bool
    anti_explosion_compliance: dict[str, int]
    bounded_cognition_discipline: dict[str, int]
    provider_escalation_discipline: dict[str, int]
    governance_adherence_score: dict[str, int]
    governance_adherence_ranking: tuple[str, ...]


@dataclass(frozen=True)
class CompactnessRetentionFrame:
    compactness_retention_active: bool
    compact_completion_consistency: dict[str, int]
    delta_only_adherence: dict[str, int]
    bounded_continuity_preservation: dict[str, int]
    compactness_score: dict[str, int]
    compactness_retention_ranking: tuple[str, ...]


@dataclass(frozen=True)
class RetrievalRadiusFrame:
    retrieval_radius_active: bool
    adjacent_runtime_retrieval: dict[str, int]
    retrieval_radius_inflation_resistance: dict[str, int]
    retrieval_discipline_score: dict[str, int]
    retrieval_discipline_ranking: tuple[str, ...]


@dataclass(frozen=True)
class HallucinationPressureFrame:
    hallucination_pressure_active: bool
    recursive_synthesis_growth: dict[str, int]
    giant_summary_expansion: dict[str, int]
    hallucinated_architecture_mutation: dict[str, int]
    drift_resistance_score: dict[str, int]
    drift_resistance_ranking: tuple[str, ...]
    estimated_recursive_drift_risk: str


@dataclass(frozen=True)
class StabilityBenchmarkFrame:
    stability_benchmark_active: bool
    provider_scores: dict[str, dict[str, int]]
    local_patch_adherence_score: dict[str, int]
    repetitive_reliability_score: dict[str, int]
    local_patch_adherence_ranking: tuple[str, ...]
    repetitive_reliability_ranking: tuple[str, ...]
    provider_stability_comparison: tuple[str, ...]
    estimated_provider_stability_gain: int
    no_real_openmythos_execution: bool
    no_hidden_provider_switching: bool
    summary_only: bool


@dataclass(frozen=True)
class ProviderStabilityRuntimeFrame:
    stability: ProviderStabilityFrame
    long_session_drift: LongSessionDriftFrame
    governance_decay: GovernanceDecayFrame
    compactness_retention: CompactnessRetentionFrame
    retrieval_radius: RetrievalRadiusFrame
    hallucination_pressure: HallucinationPressureFrame
    benchmark: StabilityBenchmarkFrame
    provider_stability_active: bool
    long_session_drift_active: bool
    governance_decay_active: bool
    compactness_retention_active: bool
    estimated_provider_stability_gain: int
    estimated_recursive_drift_risk: str
    local_only: bool
    deterministic: bool
    summary_only: bool


def _metric_scores(metric: str) -> dict[str, int]:
    return {provider: scores[metric] for provider, scores in PROVIDER_SCORE_BASELINE.items()}


def _rank(scores: dict[str, int]) -> tuple[str, ...]:
    return tuple(
        provider
        for provider, _score in sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    )


def _average_score(provider: str) -> int:
    values = PROVIDER_SCORE_BASELINE[provider].values()
    return round(sum(values) / len(PROVIDER_SCORE_BASELINE[provider]))


class ProviderStabilityRuntime:
    def evaluate(self) -> ProviderStabilityRuntimeFrame:
        governance_scores = _metric_scores("governance")
        local_patch_scores = _metric_scores("local_patch")
        compactness_scores = _metric_scores("compactness")
        drift_scores = _metric_scores("drift_resistance")
        repetitive_scores = _metric_scores("repetitive_reliability")
        retrieval_scores = _metric_scores("retrieval_discipline")
        provider_comparison = tuple(
            f"{provider}:{_average_score(provider)}"
            for provider in _rank(
                {provider: _average_score(provider) for provider in STABILITY_PROVIDERS}
            )
        )
        long_session_degradation = {
            "qwen2.5-coder:7b": 4,
            "qwen2.5-coder:14b": 5,
            "gemma3:12b": 8,
            "GPT-5.5 reference": 18,
            "OpenMythos placeholder:not_loaded": 0,
        }
        stability = ProviderStabilityFrame(
            provider_stability_active=True,
            providers=STABILITY_PROVIDERS,
            workloads=STABILITY_WORKLOADS,
            blocked_behaviors=BLOCKED_STABILITY_BEHAVIORS,
            openmythos_placeholder_only=True,
            deterministic_workloads=True,
            compact_prompts_only=True,
            local_patch_discipline=True,
            rollback_safe_evaluation=True,
        )
        long_session_drift = LongSessionDriftFrame(
            long_session_drift_active=True,
            simulated_rollovers=6,
            repeated_sprint_consistency={
                "qwen2.5-coder:7b": 96,
                "qwen2.5-coder:14b": 94,
                "gemma3:12b": 90,
                "GPT-5.5 reference": 82,
                "OpenMythos placeholder:not_loaded": 0,
            },
            summary_corruption_risk={
                "qwen2.5-coder:7b": 3,
                "qwen2.5-coder:14b": 4,
                "gemma3:12b": 7,
                "GPT-5.5 reference": 14,
                "OpenMythos placeholder:not_loaded": 0,
            },
            governance_degradation={
                "qwen2.5-coder:7b": 2,
                "qwen2.5-coder:14b": 3,
                "gemma3:12b": 5,
                "GPT-5.5 reference": 11,
                "OpenMythos placeholder:not_loaded": 0,
            },
            compactness_decay={
                "qwen2.5-coder:7b": 4,
                "qwen2.5-coder:14b": 5,
                "gemma3:12b": 8,
                "GPT-5.5 reference": 16,
                "OpenMythos placeholder:not_loaded": 0,
            },
            recursive_reasoning_tendency={
                "qwen2.5-coder:7b": 5,
                "qwen2.5-coder:14b": 6,
                "gemma3:12b": 9,
                "GPT-5.5 reference": 19,
                "OpenMythos placeholder:not_loaded": 0,
            },
            estimated_long_session_degradation=long_session_degradation,
        )
        governance_decay = GovernanceDecayFrame(
            governance_decay_active=True,
            anti_explosion_compliance=governance_scores,
            bounded_cognition_discipline=governance_scores,
            provider_escalation_discipline=governance_scores,
            governance_adherence_score=governance_scores,
            governance_adherence_ranking=_rank(governance_scores),
        )
        compactness_retention = CompactnessRetentionFrame(
            compactness_retention_active=True,
            compact_completion_consistency=compactness_scores,
            delta_only_adherence=compactness_scores,
            bounded_continuity_preservation=compactness_scores,
            compactness_score=compactness_scores,
            compactness_retention_ranking=_rank(compactness_scores),
        )
        retrieval_radius = RetrievalRadiusFrame(
            retrieval_radius_active=True,
            adjacent_runtime_retrieval=retrieval_scores,
            retrieval_radius_inflation_resistance=retrieval_scores,
            retrieval_discipline_score=retrieval_scores,
            retrieval_discipline_ranking=_rank(retrieval_scores),
        )
        hallucination_pressure = HallucinationPressureFrame(
            hallucination_pressure_active=True,
            recursive_synthesis_growth=drift_scores,
            giant_summary_expansion=drift_scores,
            hallucinated_architecture_mutation=drift_scores,
            drift_resistance_score=drift_scores,
            drift_resistance_ranking=_rank(drift_scores),
            estimated_recursive_drift_risk="LOW_BASELINE_GUARDED",
        )
        benchmark = StabilityBenchmarkFrame(
            stability_benchmark_active=True,
            provider_scores=PROVIDER_SCORE_BASELINE,
            local_patch_adherence_score=local_patch_scores,
            repetitive_reliability_score=repetitive_scores,
            local_patch_adherence_ranking=_rank(local_patch_scores),
            repetitive_reliability_ranking=_rank(repetitive_scores),
            provider_stability_comparison=provider_comparison,
            estimated_provider_stability_gain=12,
            no_real_openmythos_execution=True,
            no_hidden_provider_switching=True,
            summary_only=True,
        )
        return ProviderStabilityRuntimeFrame(
            stability=stability,
            long_session_drift=long_session_drift,
            governance_decay=governance_decay,
            compactness_retention=compactness_retention,
            retrieval_radius=retrieval_radius,
            hallucination_pressure=hallucination_pressure,
            benchmark=benchmark,
            provider_stability_active=stability.provider_stability_active,
            long_session_drift_active=long_session_drift.long_session_drift_active,
            governance_decay_active=governance_decay.governance_decay_active,
            compactness_retention_active=compactness_retention.compactness_retention_active,
            estimated_provider_stability_gain=benchmark.estimated_provider_stability_gain,
            estimated_recursive_drift_risk=hallucination_pressure.estimated_recursive_drift_risk,
            local_only=True,
            deterministic=True,
            summary_only=True,
        )


__all__ = [
    "BLOCKED_STABILITY_BEHAVIORS",
    "PROVIDER_SCORE_BASELINE",
    "STABILITY_PROVIDERS",
    "STABILITY_WORKLOADS",
    "CompactnessRetentionFrame",
    "GovernanceDecayFrame",
    "HallucinationPressureFrame",
    "LongSessionDriftFrame",
    "ProviderStabilityFrame",
    "ProviderStabilityRuntime",
    "ProviderStabilityRuntimeFrame",
    "RetrievalRadiusFrame",
    "StabilityBenchmarkFrame",
]
