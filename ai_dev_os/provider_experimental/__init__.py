from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.provider_experimental.openmythos_conversion import (
    ExperimentalFallbackFrame,
    ExperimentalModelValidationFrame,
    ExperimentalQuantizationFrame,
    GGUFCompatibilityFrame,
    OpenMythosConversionFrame,
    OpenMythosConversionRuntime,
)

BENCHMARK_CATEGORIES = (
    "LOCAL_PATCH adherence",
    "compact continuity discipline",
    "governance adherence",
    "execution stability",
    "drift resistance",
)

BOUNDED_BENCHMARK_TASKS = (
    "compact dataclass generation",
    "runtime frame generation",
    "repetitive tests",
    "compact sprint summaries",
    "LOCAL_PATCH runtime integration",
    "bounded validation summaries",
)

FORBIDDEN_BENCHMARK_TASKS = (
    "repo-wide synthesis",
    "unrestricted architecture planning",
    "giant roadmap generation",
    "recursive benchmark loops",
    "giant continuity replay",
)

COMPARISON_PROVIDERS = (
    "openmythos:experimental",
    "qwen2.5-coder:7b",
    "qwen2.5-coder:14b",
    "gemma3:12b",
    "GPT-5.5 baseline",
)

COMPARISON_METRICS = (
    "token efficiency",
    "output stability",
    "governance adherence",
    "LOCAL_PATCH compliance",
    "compactness",
    "runtime drift",
    "hallucination rate",
    "repetitive reliability",
    "recursive reasoning tendency",
)


@dataclass(frozen=True)
class ExperimentalProviderFrame:
    experimental_provider_active: bool
    branch_isolated: bool
    production_adoption: bool
    governance_authority_delegated: bool
    architecture_authority_delegated: bool
    autonomous_execution_authority_delegated: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    rollback_safe: bool


@dataclass(frozen=True)
class OpenMythosProviderFrame:
    openmythos_provider_active: bool
    provider_name: str
    ollama_model: str
    load_result: str
    vram_runtime_stability: str
    reasoning_depth_profile: str
    no_architecture_authority: bool
    no_governance_authority: bool
    no_anti_explosion_authority: bool
    no_autonomous_execution_authority: bool


@dataclass(frozen=True)
class ProviderBenchmarkFrame:
    provider_benchmark_active: bool
    categories: tuple[str, ...]
    tasks: tuple[str, ...]
    forbidden_tasks: tuple[str, ...]
    compact_prompts_only: bool
    adjacent_runtime_only_retrieval: bool
    deterministic_benchmark_tasks: bool
    rollback_safe_evaluation_only: bool
    recursive_benchmark_loops_forbidden: bool
    unrestricted_prompts_forbidden: bool
    repo_wide_evaluation_forbidden: bool
    max_prompt_chars: int
    max_tasks_per_provider: int


@dataclass(frozen=True)
class ProviderComparisonFrame:
    provider_comparison_active: bool
    providers: tuple[str, ...]
    metrics: tuple[str, ...]
    compact_benchmark_summaries_only: bool
    no_real_provider_execution: bool
    no_hidden_provider_switching: bool
    no_provider_upload: bool
    deterministic_scoring_only: bool
    estimated_token_efficiency_delta: dict[str, int]


@dataclass(frozen=True)
class ProviderStabilityFrame:
    provider_stability_active: bool
    repetitive_runtime_generation: str
    test_generation_consistency: str
    structured_dataclass_generation: str
    compact_continuity_stability: str
    long_session_drift_resistance: str
    runtime_stability_notes: tuple[str, ...]


@dataclass(frozen=True)
class ProviderDriftFrame:
    provider_drift_active: bool
    recursive_reasoning_growth_blocked: bool
    giant_synthesis_attempts_blocked: bool
    hallucinated_architecture_expansion_blocked: bool
    estimated_reasoning_depth_gain: int
    estimated_governance_instability_risk: int
    estimated_architecture_drift_risk: int
    drift_risk: str


@dataclass(frozen=True)
class ProviderGovernanceFrame:
    provider_governance_active: bool
    local_patch_adherence_checked: bool
    compact_continuity_checked: bool
    bounded_retrieval_checked: bool
    anti_explosion_compliance: bool
    provider_escalation_compliance: bool
    bounded_cognition_discipline: bool
    governance_consistency: str


@dataclass(frozen=True)
class ProviderBenchmarkSummaryFrame:
    provider_benchmark_summary_active: bool
    compact_summary: str
    openmythos_load_result: str
    governance_adherence_observation: str
    architecture_drift_observation: str
    estimated_reasoning_depth_benefit: str
    estimated_instability_risk: str
    summary_only: bool


@dataclass(frozen=True)
class ProviderBenchmarkEvictionFrame:
    provider_benchmark_eviction_active: bool
    bounded_retention_limit: int
    retained_summary_count: int
    evicted_prompt_count: int
    evicts_raw_outputs: bool
    evicts_unbounded_context: bool
    compact_summary_retained: bool


@dataclass(frozen=True)
class ProviderExperimentalRuntimeFrame:
    experimental: ExperimentalProviderFrame
    openmythos: OpenMythosProviderFrame
    benchmark: ProviderBenchmarkFrame
    comparison: ProviderComparisonFrame
    stability: ProviderStabilityFrame
    drift: ProviderDriftFrame
    governance: ProviderGovernanceFrame
    summary: ProviderBenchmarkSummaryFrame
    eviction: ProviderBenchmarkEvictionFrame
    conversion: OpenMythosConversionFrame
    gguf: GGUFCompatibilityFrame
    model_validation: ExperimentalModelValidationFrame
    quantization: ExperimentalQuantizationFrame
    fallback: ExperimentalFallbackFrame
    experimental_provider_active: bool
    openmythos_provider_active: bool
    openmythos_loaded: bool
    openmythos_gguf_active: bool
    openmythos_conversion_active: bool
    openmythos_runtime_stability: str
    openmythos_drift_risk: str
    openmythos_reasoning_depth_signal: str
    openmythos_governance_adherence: str
    provider_benchmark_active: bool
    provider_comparison_active: bool
    provider_drift_active: bool
    estimated_reasoning_depth_gain: int
    estimated_governance_instability_risk: int
    estimated_architecture_drift_risk: int
    local_only: bool
    deterministic: bool
    summary_only: bool


class ProviderExperimentalRuntime:
    def evaluate(
        self,
        *,
        openmythos_load_result: str = "unavailable:hf_repository_not_gguf",
        openmythos_loaded: bool = False,
        openmythos_gguf_active: bool = False,
    ) -> ProviderExperimentalRuntimeFrame:
        conversion_runtime = OpenMythosConversionRuntime().evaluate()
        experimental = ExperimentalProviderFrame(
            experimental_provider_active=True,
            branch_isolated=True,
            production_adoption=False,
            governance_authority_delegated=False,
            architecture_authority_delegated=False,
            autonomous_execution_authority_delegated=False,
            local_only=True,
            deterministic=True,
            summary_only=True,
            rollback_safe=True,
        )
        openmythos = OpenMythosProviderFrame(
            openmythos_provider_active=openmythos_loaded and openmythos_gguf_active,
            provider_name="OpenMythos",
            ollama_model=conversion_runtime.conversion.ollama_model_name,
            load_result=openmythos_load_result,
            vram_runtime_stability="not_loaded" if not openmythos_loaded else "bounded",
            reasoning_depth_profile="experimental_recurrent_depth",
            no_architecture_authority=True,
            no_governance_authority=True,
            no_anti_explosion_authority=True,
            no_autonomous_execution_authority=True,
        )
        benchmark = ProviderBenchmarkFrame(
            provider_benchmark_active=True,
            categories=BENCHMARK_CATEGORIES,
            tasks=BOUNDED_BENCHMARK_TASKS,
            forbidden_tasks=FORBIDDEN_BENCHMARK_TASKS,
            compact_prompts_only=True,
            adjacent_runtime_only_retrieval=True,
            deterministic_benchmark_tasks=True,
            rollback_safe_evaluation_only=True,
            recursive_benchmark_loops_forbidden=True,
            unrestricted_prompts_forbidden=True,
            repo_wide_evaluation_forbidden=True,
            max_prompt_chars=2400,
            max_tasks_per_provider=len(BOUNDED_BENCHMARK_TASKS),
        )
        comparison = ProviderComparisonFrame(
            provider_comparison_active=True,
            providers=COMPARISON_PROVIDERS,
            metrics=COMPARISON_METRICS,
            compact_benchmark_summaries_only=True,
            no_real_provider_execution=True,
            no_hidden_provider_switching=True,
            no_provider_upload=True,
            deterministic_scoring_only=True,
            estimated_token_efficiency_delta={
                "openmythos:experimental": 0 if not openmythos_loaded else 8,
                "qwen2.5-coder:7b": 6,
                "qwen2.5-coder:14b": 4,
                "gemma3:12b": 3,
                "GPT-5.5 baseline": -6,
            },
        )
        stability = ProviderStabilityFrame(
            provider_stability_active=True,
            repetitive_runtime_generation="not_measured" if not openmythos_loaded else "bounded",
            test_generation_consistency="not_measured" if not openmythos_loaded else "bounded",
            structured_dataclass_generation="not_measured" if not openmythos_loaded else "bounded",
            compact_continuity_stability="stable_policy",
            long_session_drift_resistance="guarded",
            runtime_stability_notes=(
                (
                    "openmythos_model_unavailable",
                    "deterministic_comparison_harness_ready",
                )
                if not openmythos_loaded
                else ("bounded_runtime_probe_required",)
            ),
        )
        drift = ProviderDriftFrame(
            provider_drift_active=True,
            recursive_reasoning_growth_blocked=True,
            giant_synthesis_attempts_blocked=True,
            hallucinated_architecture_expansion_blocked=True,
            estimated_reasoning_depth_gain=0 if not openmythos_loaded else 8,
            estimated_governance_instability_risk=2 if not openmythos_loaded else 5,
            estimated_architecture_drift_risk=2 if not openmythos_loaded else 6,
            drift_risk="LOW_NOT_LOADED" if not openmythos_loaded else "MEDIUM_EXPERIMENTAL",
        )
        governance = ProviderGovernanceFrame(
            provider_governance_active=True,
            local_patch_adherence_checked=True,
            compact_continuity_checked=True,
            bounded_retrieval_checked=True,
            anti_explosion_compliance=True,
            provider_escalation_compliance=True,
            bounded_cognition_discipline=True,
            governance_consistency="stable_policy_harness",
        )
        summary = ProviderBenchmarkSummaryFrame(
            provider_benchmark_summary_active=True,
            compact_summary=(
                "OpenMythos HF GGUF unavailable; conversion fallback guarded; "
                "no production routing changed."
            ),
            openmythos_load_result=openmythos_load_result,
            governance_adherence_observation="guards_preserved",
            architecture_drift_observation="blocked_by_policy",
            estimated_reasoning_depth_benefit=(
                "unmeasured_model_unavailable"
                if not openmythos_loaded
                else "potential_for_bounded_local_patch_tasks"
            ),
            estimated_instability_risk=(
                "low_until_model_loaded" if not openmythos_loaded else "medium_experimental"
            ),
            summary_only=True,
        )
        eviction = ProviderBenchmarkEvictionFrame(
            provider_benchmark_eviction_active=True,
            bounded_retention_limit=5,
            retained_summary_count=1,
            evicted_prompt_count=0,
            evicts_raw_outputs=True,
            evicts_unbounded_context=True,
            compact_summary_retained=True,
        )
        return ProviderExperimentalRuntimeFrame(
            experimental=experimental,
            openmythos=openmythos,
            benchmark=benchmark,
            comparison=comparison,
            stability=stability,
            drift=drift,
            governance=governance,
            summary=summary,
            eviction=eviction,
            conversion=conversion_runtime.conversion,
            gguf=conversion_runtime.compatibility,
            model_validation=conversion_runtime.validation,
            quantization=conversion_runtime.quantization,
            fallback=conversion_runtime.fallback,
            experimental_provider_active=experimental.experimental_provider_active,
            openmythos_provider_active=openmythos.openmythos_provider_active,
            openmythos_loaded=openmythos_loaded,
            openmythos_gguf_active=openmythos_gguf_active,
            openmythos_conversion_active=conversion_runtime.conversion.conversion_active,
            openmythos_runtime_stability=openmythos.vram_runtime_stability,
            openmythos_drift_risk=drift.drift_risk,
            openmythos_reasoning_depth_signal=summary.estimated_reasoning_depth_benefit,
            openmythos_governance_adherence=summary.governance_adherence_observation,
            provider_benchmark_active=benchmark.provider_benchmark_active,
            provider_comparison_active=comparison.provider_comparison_active,
            provider_drift_active=drift.provider_drift_active,
            estimated_reasoning_depth_gain=drift.estimated_reasoning_depth_gain,
            estimated_governance_instability_risk=drift.estimated_governance_instability_risk,
            estimated_architecture_drift_risk=drift.estimated_architecture_drift_risk,
            local_only=True,
            deterministic=True,
            summary_only=True,
        )


__all__ = [
    "BENCHMARK_CATEGORIES",
    "BOUNDED_BENCHMARK_TASKS",
    "COMPARISON_METRICS",
    "COMPARISON_PROVIDERS",
    "FORBIDDEN_BENCHMARK_TASKS",
    "ExperimentalProviderFrame",
    "ExperimentalFallbackFrame",
    "ExperimentalModelValidationFrame",
    "ExperimentalQuantizationFrame",
    "GGUFCompatibilityFrame",
    "OpenMythosProviderFrame",
    "OpenMythosConversionFrame",
    "ProviderBenchmarkEvictionFrame",
    "ProviderBenchmarkFrame",
    "ProviderBenchmarkSummaryFrame",
    "ProviderComparisonFrame",
    "ProviderDriftFrame",
    "ProviderExperimentalRuntime",
    "ProviderExperimentalRuntimeFrame",
    "ProviderGovernanceFrame",
    "ProviderStabilityFrame",
]
