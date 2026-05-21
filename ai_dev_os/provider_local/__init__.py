from __future__ import annotations

from dataclasses import dataclass

LOW_LOCAL_TASKS = (
    "repetitive_tests",
    "markdown_cleanup",
    "formatting",
    "boilerplate",
    "runtime_glue",
    "extension_wiring",
    "compact_summaries",
    "projection_glue",
)
MEDIUM_ROUTING_TASKS = (
    "runtime_integration",
    "adapter_plumbing",
    "execution_sequencing",
)
HIGH_CLOUD_TASKS = (
    "architecture",
    "governance",
    "embodiment_realism",
    "anti_explosion_policy",
    "cognition_policy",
    "sprint_strategy",
)
LOCAL_EXECUTION_CONSTRAINTS = (
    "compact_prompts_only",
    "local_patch_only",
    "adjacent_runtime_retrieval_only",
    "bounded_context_windows",
    "repo_wide_local_reasoning_forbidden",
    "giant_continuity_replay_forbidden",
    "recursive_local_execution_forbidden",
    "hidden_autonomous_loops_forbidden",
    "unrestricted_repository_mutation_forbidden",
)


@dataclass(frozen=True)
class LocalProviderCapability:
    model: str
    coding: bool
    summaries: bool
    architecture: bool
    governance: bool
    compression: bool = False
    governance_summaries: bool = False
    coding_limited: bool = False


@dataclass(frozen=True)
class LocalProviderCapabilityFrame:
    capabilities: tuple[LocalProviderCapability, ...]
    primary_coding_model: str
    governance_compression_model: str
    fallback_coding_model: str
    qwen_coder_14b_coding: bool
    qwen_coder_14b_summaries: bool
    qwen_coder_14b_architecture: bool
    qwen_coder_14b_governance: bool
    gemma3_12b_compression: bool
    gemma3_12b_governance_summaries: bool
    gemma3_12b_coding: str
    deterministic_metadata_only: bool
    summary_only: bool


@dataclass(frozen=True)
class OllamaProviderFrame:
    provider_name: str
    runtime_installed: bool
    configured_models: tuple[str, ...]
    loaded_models: tuple[str, ...]
    primary_model_loaded: bool
    governance_model_loaded: bool
    fallback_model_loaded: bool
    no_remote_provider_call: bool
    no_hidden_execution: bool
    human_confirmed_execution_authority: bool


@dataclass(frozen=True)
class LocalExecutionBudgetFrame:
    max_prompt_tokens: int
    max_context_tokens: int
    max_patch_files: int
    max_adjacent_runtimes: int
    local_execution_ratio_target: float
    compact_prompts_required: bool
    local_patch_only: bool
    bounded_context_windows: bool
    recursive_local_execution_forbidden: bool
    unrestricted_repository_mutation_forbidden: bool
    human_confirmed_execution_authority: bool
    budget_state: str


@dataclass(frozen=True)
class LocalProviderHealthFrame:
    health_state: str
    vram_profile: str
    hardware_profile: str
    primary_model_practical: bool
    primary_model_gpu_operational: bool
    governance_model_stable: bool
    fallback_model_operational: bool
    windows_responsiveness_expected: str
    context_stability: str
    thermal_stability_observation_required: bool
    loaded_required_models: bool


@dataclass(frozen=True)
class LocalProviderRoutingFrame:
    low_local_tasks: tuple[str, ...]
    medium_routing_tasks: tuple[str, ...]
    high_cloud_tasks: tuple[str, ...]
    low_execution_provider: str
    governance_compression_provider: str
    high_provider: str
    routing_distribution: dict[str, int]
    local_provider_for_low: bool
    medium_requires_bounded_routing: bool
    high_requires_premium_cloud: bool
    local_has_no_architecture_authority: bool
    local_has_no_governance_authority: bool
    human_visible_routing: bool


@dataclass(frozen=True)
class LocalProviderFallbackFrame:
    fallback_model: str
    fallback_to_lightweight_model: bool
    premium_escalation_provider: str
    premium_escalation_requires_human_confirmation: bool
    no_hidden_premium_escalation: bool
    no_recursive_local_retry_loop: bool
    local_summary_before_escalation: bool
    fallback_state: str


@dataclass(frozen=True)
class LocalProviderFrame:
    capability: LocalProviderCapabilityFrame
    ollama: OllamaProviderFrame
    routing: LocalProviderRoutingFrame
    budget: LocalExecutionBudgetFrame
    health: LocalProviderHealthFrame
    fallback: LocalProviderFallbackFrame
    local_provider_active: bool
    ollama_provider_active: bool
    local_provider_health: str
    local_provider_budget: str
    local_provider_fallback: str
    estimated_avoided_premium_tokens: int
    estimated_local_execution_ratio: float
    constraints: tuple[str, ...]
    local_only: bool
    deterministic: bool
    summary_only: bool
    no_repo_wide_local_reasoning: bool
    no_giant_continuity_replay: bool
    no_recursive_local_execution: bool
    no_hidden_autonomous_loops: bool
    no_unrestricted_repository_mutation: bool


class LocalProviderRuntime:
    def evaluate(
        self,
        *,
        installed_models: tuple[str, ...] = (
            "qwen2.5-coder:14b",
            "gemma3:12b",
            "qwen2.5-coder:7b",
        ),
        ollama_installed: bool = True,
        primary_model_gpu_operational: bool = False,
        low_task_count: int = 8,
        medium_task_count: int = 3,
        high_task_count: int = 3,
    ) -> LocalProviderFrame:
        configured_models = (
            "qwen2.5-coder:14b",
            "gemma3:12b",
            "qwen2.5-coder:7b",
        )
        loaded = tuple(model for model in configured_models if model in set(installed_models))
        capability = LocalProviderCapabilityFrame(
            capabilities=(
                LocalProviderCapability(
                    "qwen2.5-coder:14b",
                    coding=True,
                    summaries=True,
                    architecture=False,
                    governance=False,
                ),
                LocalProviderCapability(
                    "gemma3:12b",
                    coding=False,
                    summaries=True,
                    architecture=False,
                    governance=False,
                    compression=True,
                    governance_summaries=True,
                    coding_limited=True,
                ),
                LocalProviderCapability(
                    "qwen2.5-coder:7b",
                    coding=True,
                    summaries=True,
                    architecture=False,
                    governance=False,
                    coding_limited=True,
                ),
            ),
            primary_coding_model="qwen2.5-coder:14b",
            governance_compression_model="gemma3:12b",
            fallback_coding_model="qwen2.5-coder:7b",
            qwen_coder_14b_coding=True,
            qwen_coder_14b_summaries=True,
            qwen_coder_14b_architecture=False,
            qwen_coder_14b_governance=False,
            gemma3_12b_compression=True,
            gemma3_12b_governance_summaries=True,
            gemma3_12b_coding="limited",
            deterministic_metadata_only=True,
            summary_only=True,
        )
        ollama = OllamaProviderFrame(
            provider_name="ollama",
            runtime_installed=ollama_installed,
            configured_models=configured_models,
            loaded_models=loaded,
            primary_model_loaded="qwen2.5-coder:14b" in loaded,
            governance_model_loaded="gemma3:12b" in loaded,
            fallback_model_loaded="qwen2.5-coder:7b" in loaded,
            no_remote_provider_call=True,
            no_hidden_execution=True,
            human_confirmed_execution_authority=True,
        )
        budget = LocalExecutionBudgetFrame(
            max_prompt_tokens=1_800,
            max_context_tokens=6_000,
            max_patch_files=4,
            max_adjacent_runtimes=2,
            local_execution_ratio_target=0.62,
            compact_prompts_required=True,
            local_patch_only=True,
            bounded_context_windows=True,
            recursive_local_execution_forbidden=True,
            unrestricted_repository_mutation_forbidden=True,
            human_confirmed_execution_authority=True,
            budget_state="LOCAL_BUDGET_OK",
        )
        fallback_ready = ollama.fallback_model_loaded and ollama.governance_model_loaded
        required_loaded = ollama.primary_model_loaded and ollama.governance_model_loaded
        local_ready = required_loaded and (primary_model_gpu_operational or fallback_ready)
        health = LocalProviderHealthFrame(
            health_state=(
                "READY"
                if ollama.runtime_installed and required_loaded and primary_model_gpu_operational
                else (
                    "DEGRADED_FALLBACK_READY"
                    if ollama.runtime_installed and fallback_ready
                    else "DEGRADED"
                )
            ),
            vram_profile="RTX3080_10GB_12GB_BOUNDED_CONTEXT",
            hardware_profile="RTX3080",
            primary_model_practical=primary_model_gpu_operational,
            primary_model_gpu_operational=primary_model_gpu_operational,
            governance_model_stable=True,
            fallback_model_operational=fallback_ready,
            windows_responsiveness_expected="stable_under_bounded_prompts",
            context_stability="bounded_context_required",
            thermal_stability_observation_required=True,
            loaded_required_models=required_loaded,
        )
        distribution = {
            "LOW_LOCAL": low_task_count,
            "MEDIUM_ROUTED": medium_task_count,
            "HIGH_CLOUD": high_task_count,
        }
        routing = LocalProviderRoutingFrame(
            low_local_tasks=LOW_LOCAL_TASKS,
            medium_routing_tasks=MEDIUM_ROUTING_TASKS,
            high_cloud_tasks=HIGH_CLOUD_TASKS,
            low_execution_provider=(
                "ollama:qwen2.5-coder:14b"
                if primary_model_gpu_operational
                else "ollama:qwen2.5-coder:7b"
            ),
            governance_compression_provider="ollama:gemma3:12b",
            high_provider="GPT-5.5 premium provider",
            routing_distribution=distribution,
            local_provider_for_low=True,
            medium_requires_bounded_routing=True,
            high_requires_premium_cloud=True,
            local_has_no_architecture_authority=True,
            local_has_no_governance_authority=True,
            human_visible_routing=True,
        )
        fallback = LocalProviderFallbackFrame(
            fallback_model="qwen2.5-coder:7b",
            fallback_to_lightweight_model=True,
            premium_escalation_provider="GPT-5.5 premium provider",
            premium_escalation_requires_human_confirmation=True,
            no_hidden_premium_escalation=True,
            no_recursive_local_retry_loop=True,
            local_summary_before_escalation=True,
            fallback_state=(
                "PRIMARY_READY_WITH_LIGHTWEIGHT_FALLBACK"
                if primary_model_gpu_operational
                else "LIGHTWEIGHT_ACTIVE_PRIMARY_GPU_DEGRADED"
            ),
        )
        local_units = low_task_count + max(0, medium_task_count - 1)
        total_units = max(1, low_task_count + medium_task_count + high_task_count)
        ratio = round(local_units / total_units, 4)
        avoided_tokens = low_task_count * 900 + medium_task_count * 350
        active = all(
            (
                ollama.runtime_installed,
                local_ready,
                budget.compact_prompts_required,
                budget.local_patch_only,
                routing.local_provider_for_low,
                routing.local_has_no_architecture_authority,
                routing.local_has_no_governance_authority,
                fallback.no_hidden_premium_escalation,
                fallback.no_recursive_local_retry_loop,
            )
        )
        return LocalProviderFrame(
            capability=capability,
            ollama=ollama,
            routing=routing,
            budget=budget,
            health=health,
            fallback=fallback,
            local_provider_active=active,
            ollama_provider_active=ollama.runtime_installed and required_loaded,
            local_provider_health=health.health_state,
            local_provider_budget=budget.budget_state,
            local_provider_fallback=fallback.fallback_state,
            estimated_avoided_premium_tokens=avoided_tokens,
            estimated_local_execution_ratio=ratio,
            constraints=LOCAL_EXECUTION_CONSTRAINTS,
            local_only=True,
            deterministic=True,
            summary_only=True,
            no_repo_wide_local_reasoning=True,
            no_giant_continuity_replay=True,
            no_recursive_local_execution=True,
            no_hidden_autonomous_loops=True,
            no_unrestricted_repository_mutation=True,
        )


__all__ = [
    "LocalExecutionBudgetFrame",
    "LocalProviderCapability",
    "LocalProviderCapabilityFrame",
    "LocalProviderFallbackFrame",
    "LocalProviderFrame",
    "LocalProviderHealthFrame",
    "LocalProviderRoutingFrame",
    "LocalProviderRuntime",
    "OllamaProviderFrame",
]
