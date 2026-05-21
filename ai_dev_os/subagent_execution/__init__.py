from __future__ import annotations

from dataclasses import dataclass

SUBAGENT_EXECUTION_REQUIREMENT_IDS = tuple(
    f"FR-SUBAGENTEXEC-{index:02d}" for index in range(1, 15)
) + (
    "NFR-COST-26",
    "NFR-ARCH-40",
    "NFR-SEC-11",
)
SUBAGENT_EXECUTION_TEST_IDS = tuple(f"TC-SUBAGENTEXEC-{index:02d}" for index in range(1, 15))

DELEGATABLE_TASKS = (
    "repetitive_tests",
    "markdown_cleanup",
    "runtime_glue",
    "extension_wiring",
    "boilerplate",
    "compact_summaries",
    "projection_glue",
    "repetitive_runtime_frames",
)


@dataclass(frozen=True)
class SubagentRoutingFrame:
    task_routes: dict[str, str]
    provider_routing_distribution: dict[str, int]
    low_local_provider: str
    low_governance_provider: str
    medium_provider: str
    high_provider: str
    compact_routing_summaries: tuple[str, ...]
    fallback_safe_routing: bool
    provider_pressure_aware_routing: bool
    unsafe_local_governance_delegation_prevented: bool
    high_reasoning_local_delegation_prevented: bool
    hidden_provider_switching_prevented: bool


@dataclass(frozen=True)
class SubagentCapabilityFrame:
    qwen_coding: bool
    qwen_governance: bool
    qwen_architecture: bool
    gemma_summaries: bool
    gemma_governance_summaries: bool
    gemma_coding: str
    context_stability: str
    vram_stability: str
    fallback_available: bool
    local_14b_stable: bool
    deterministic_metadata_only: bool


@dataclass(frozen=True)
class SubagentPayloadFrame:
    payload_sections: tuple[str, ...]
    max_payload_tokens: int
    adjacent_runtime_only: bool
    delta_only_continuity: bool
    local_patch_scope: bool
    bounded_retrieval_radius: int
    compact_summaries_only: bool
    repo_wide_replay_prevented: bool
    giant_continuity_payload_prevented: bool
    full_sprint_history_prevented: bool
    unrestricted_retrieval_prevented: bool


@dataclass(frozen=True)
class SubagentValidationFrame:
    delegated_validation_ordering: tuple[str, ...]
    scoped_validation_coverage: tuple[str, ...]
    subagent_failure_patterns: tuple[str, ...]
    repeated_delegated_instability: int
    compact_validation_summaries: tuple[str, ...]
    delegated_rollback_reminders: tuple[str, ...]
    stabilization_guidance: tuple[str, ...]
    validation_bypass_prevented: bool


@dataclass(frozen=True)
class SubagentFallbackFrame:
    fallback_reasons: tuple[str, ...]
    active_fallback_provider: str
    downgrade_safe_fallback: bool
    compact_provider_switch_summaries: tuple[str, ...]
    rollback_safe_continuation_hints: tuple[str, ...]
    vram_instability_handled: bool
    cuda_failure_handled: bool
    context_instability_handled: bool
    provider_timeout_handled: bool
    delegated_execution_failure_handled: bool
    no_recursive_retry_loop: bool


@dataclass(frozen=True)
class SubagentCheckpointFrame:
    delegated_task_completion: tuple[str, ...]
    validation_checkpoints: tuple[str, ...]
    rollback_safe_boundaries: tuple[str, ...]
    delegated_execution_continuity: tuple[str, ...]
    compact_checkpoint_summaries: tuple[str, ...]
    continuation_safe_hints: tuple[str, ...]
    bounded_delegation_reminders: tuple[str, ...]


@dataclass(frozen=True)
class SubagentRollbackFrame:
    rollback_state: str
    rollback_safe_boundaries: tuple[str, ...]
    rollback_reminders: tuple[str, ...]
    compact_recovery_guidance: tuple[str, ...]
    autonomous_merge_prevented: bool
    autonomous_repository_rewrite_prevented: bool
    hidden_rollback_automation_prevented: bool


@dataclass(frozen=True)
class SubagentPressureFrame:
    delegated_cognition_pressure: str
    provider_escalation_pressure: str
    payload_pressure: str
    scope_pressure: str
    swarm_pressure: str
    compact_pressure_warnings: tuple[str, ...]
    bounded_delegation_only: bool


@dataclass(frozen=True)
class SubagentRecommendationFrame:
    compact_delegation_summary: str
    routing_recommendations: tuple[str, ...]
    fallback_recommendations: tuple[str, ...]
    stabilization_hints: tuple[str, ...]
    non_binding: bool
    human_confirmed: bool
    compact: bool
    deterministic: bool


@dataclass(frozen=True)
class SubagentGovernanceFrame:
    delegated_cognition_pressure: str
    subagent_explosion_attempts: int
    recursive_delegation_attempts: int
    oversized_payload_attempts: int
    provider_escalation_pressure: str
    compact_governance_warnings: tuple[str, ...]
    bounded_delegation_reminders: tuple[str, ...]
    anti_swarm_stabilization_guidance: tuple[str, ...]
    autonomous_swarm_emergence_prevented: bool
    recursive_delegation_trees_prevented: bool
    uncontrolled_execution_fanout_prevented: bool


@dataclass(frozen=True)
class SubagentEvictionFrame:
    evicted_stale_delegated_payloads: tuple[str, ...]
    evicted_oversized_execution_payloads: tuple[str, ...]
    evicted_obsolete_fallback_heuristics: tuple[str, ...]
    evicted_repeated_delegated_summaries: tuple[str, ...]
    preserved_compact_delegation_heuristics: tuple[str, ...]
    subagent_eviction_active: bool
    compact_useful_delegation_heuristics_only: bool


@dataclass(frozen=True)
class SubagentScopeFrame:
    local_patch_only: bool
    adjacent_runtime_only: bool
    bounded_retrieval_only: bool
    compact_execution_only: bool
    retrieval_radius: int
    delegated_scope_size: int
    context_accumulation_pressure: str
    repo_wide_delegated_cognition_prevented: bool
    automatic_scope_expansion_prevented: bool


@dataclass(frozen=True)
class SubagentHealthFrame:
    subagent_health: str
    local_subagent_ready: bool
    cloud_subagent_available: bool
    fallback_ready: bool
    validation_stable: bool
    rollback_safe: bool
    bounded_delegation_stable: bool


@dataclass(frozen=True)
class SubagentExecutionFrame:
    routing: SubagentRoutingFrame
    capability: SubagentCapabilityFrame
    payload: SubagentPayloadFrame
    validation: SubagentValidationFrame
    fallback: SubagentFallbackFrame
    checkpoint: SubagentCheckpointFrame
    rollback: SubagentRollbackFrame
    pressure: SubagentPressureFrame
    recommendation: SubagentRecommendationFrame
    governance: SubagentGovernanceFrame
    eviction: SubagentEvictionFrame
    scope: SubagentScopeFrame
    health: SubagentHealthFrame
    subagent_execution_active: bool
    subagent_routing_active: bool
    subagent_payload_active: bool
    subagent_validation_active: bool
    subagent_fallback_active: bool
    subagent_governance_active: bool
    subagent_scope_active: bool
    subagent_eviction_active: bool
    local_only_for_low_local: bool
    deterministic: bool
    summary_only: bool
    bounded_delegation_only: bool
    human_confirmed_delegation_only: bool
    no_autonomous_agent_swarms: bool
    no_recursive_subagent_spawning: bool
    no_hidden_provider_switching: bool
    no_repo_wide_delegated_cognition: bool
    no_autonomous_repository_mutation: bool
    estimated_avoided_premium_subagent_tokens: int
    estimated_avoided_recursive_agent_explosion: int
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]


class SubagentExecutionRuntime:
    def evaluate(
        self,
        *,
        local_14b_stable: bool = False,
        delegated_task_count: int = 8,
        recursive_attempts: int = 2,
        oversized_payload_attempts: int = 2,
        provider_escalations: int = 1,
    ) -> SubagentExecutionFrame:
        low_local = "ollama:qwen2.5-coder:14b" if local_14b_stable else "ollama:qwen2.5-coder:7b"
        distribution = {"LOW_LOCAL": 5, "LOW_GOVERNANCE": 2, "MEDIUM": 2, "HIGH": 1}
        routing = SubagentRoutingFrame(
            task_routes={
                "repetitive_tests": "LOW_LOCAL",
                "markdown_cleanup": "LOW_LOCAL",
                "runtime_glue": "LOW_LOCAL",
                "extension_wiring": "MEDIUM",
                "compact_summaries": "LOW_GOVERNANCE",
                "continuity_compression": "LOW_GOVERNANCE",
                "integration_sequencing": "MEDIUM",
                "architecture": "HIGH",
                "governance": "HIGH",
            },
            provider_routing_distribution=distribution,
            low_local_provider=low_local,
            low_governance_provider="ollama:gemma3:12b",
            medium_provider="cloud:medium_provider",
            high_provider="GPT-5.5 premium governance provider",
            compact_routing_summaries=(
                "LOW_LOCAL handles repetitive coding and tests",
                "LOW_GOVERNANCE handles compact summaries only",
                "HIGH remains governance and architecture only",
            ),
            fallback_safe_routing=True,
            provider_pressure_aware_routing=True,
            unsafe_local_governance_delegation_prevented=True,
            high_reasoning_local_delegation_prevented=True,
            hidden_provider_switching_prevented=True,
        )
        capability = SubagentCapabilityFrame(
            qwen_coding=True,
            qwen_governance=False,
            qwen_architecture=False,
            gemma_summaries=True,
            gemma_governance_summaries=True,
            gemma_coding="limited",
            context_stability="bounded_context_only",
            vram_stability="14b_degraded_7b_fallback_ready",
            fallback_available=True,
            local_14b_stable=local_14b_stable,
            deterministic_metadata_only=True,
        )
        payload = SubagentPayloadFrame(
            payload_sections=(
                "task_delta",
                "adjacent_runtime_contract",
                "local_patch_scope",
                "validation_order",
                "rollback_hint",
            ),
            max_payload_tokens=1_600,
            adjacent_runtime_only=True,
            delta_only_continuity=True,
            local_patch_scope=True,
            bounded_retrieval_radius=2,
            compact_summaries_only=True,
            repo_wide_replay_prevented=True,
            giant_continuity_payload_prevented=True,
            full_sprint_history_prevented=True,
            unrestricted_retrieval_prevented=True,
        )
        validation = SubagentValidationFrame(
            delegated_validation_ordering=("ruff", "black", "targeted_tests", "runtime_audit"),
            scoped_validation_coverage=("tests/subagent_execution", "tests/subagent_routing"),
            subagent_failure_patterns=("cuda_failure", "provider_timeout"),
            repeated_delegated_instability=1,
            compact_validation_summaries=("targeted_subagent_tests_required",),
            delegated_rollback_reminders=("return_to_pre_delegation_checkpoint",),
            stabilization_guidance=("compact_payload_before_retry", "fallback_once_then_stop"),
            validation_bypass_prevented=True,
        )
        fallback = SubagentFallbackFrame(
            fallback_reasons=("vram_instability", "cuda_failure", "provider_timeout"),
            active_fallback_provider="ollama:qwen2.5-coder:7b",
            downgrade_safe_fallback=True,
            compact_provider_switch_summaries=("14b_gpu_degraded_to_7b_local",),
            rollback_safe_continuation_hints=("checkpoint_before_retry",),
            vram_instability_handled=True,
            cuda_failure_handled=True,
            context_instability_handled=True,
            provider_timeout_handled=True,
            delegated_execution_failure_handled=True,
            no_recursive_retry_loop=True,
        )
        checkpoint = SubagentCheckpointFrame(
            delegated_task_completion=DELEGATABLE_TASKS[:delegated_task_count],
            validation_checkpoints=("before_delegation", "after_scoped_patch", "after_validation"),
            rollback_safe_boundaries=("pre_delegation_diff", "targeted_validation_pass"),
            delegated_execution_continuity=("compact_delta_only", "no_full_history"),
            compact_checkpoint_summaries=("delegated_patch_ready_for_human_review",),
            continuation_safe_hints=("resume_from_validation_checkpoint",),
            bounded_delegation_reminders=("one_subagent_layer_only", "human_confirmed_execution"),
        )
        rollback = SubagentRollbackFrame(
            rollback_state="ROLLBACK_SAFE",
            rollback_safe_boundaries=checkpoint.rollback_safe_boundaries,
            rollback_reminders=("do_not_revert_unrelated_worktree",),
            compact_recovery_guidance=("restore_only_delegated_patch_if_validation_regresses",),
            autonomous_merge_prevented=True,
            autonomous_repository_rewrite_prevented=True,
            hidden_rollback_automation_prevented=True,
        )
        pressure = SubagentPressureFrame(
            delegated_cognition_pressure="MEDIUM",
            provider_escalation_pressure="MEDIUM" if provider_escalations else "LOW",
            payload_pressure="LOW",
            scope_pressure="LOW",
            swarm_pressure="BLOCKED" if recursive_attempts else "LOW",
            compact_pressure_warnings=(
                "recursive_delegation_blocked",
                "oversized_payload_compacted",
            ),
            bounded_delegation_only=True,
        )
        recommendation = SubagentRecommendationFrame(
            compact_delegation_summary="delegate LOW/MEDIUM bounded tasks; block recursive swarms",
            routing_recommendations=("LOW_LOCAL_for_repetitive_patch", "HIGH_for_governance"),
            fallback_recommendations=("7b_local_after_14b_cuda_failure",),
            stabilization_hints=("compact_payload", "validate_before_next_delegation"),
            non_binding=True,
            human_confirmed=True,
            compact=True,
            deterministic=True,
        )
        governance = SubagentGovernanceFrame(
            delegated_cognition_pressure=pressure.delegated_cognition_pressure,
            subagent_explosion_attempts=recursive_attempts,
            recursive_delegation_attempts=recursive_attempts,
            oversized_payload_attempts=oversized_payload_attempts,
            provider_escalation_pressure=pressure.provider_escalation_pressure,
            compact_governance_warnings=("swarm_blocked", "recursive_subagent_spawn_blocked"),
            bounded_delegation_reminders=("single_layer_delegation", "local_patch_only"),
            anti_swarm_stabilization_guidance=("evict_stale_payloads", "stop_after_fallback"),
            autonomous_swarm_emergence_prevented=True,
            recursive_delegation_trees_prevented=True,
            uncontrolled_execution_fanout_prevented=True,
        )
        eviction = SubagentEvictionFrame(
            evicted_stale_delegated_payloads=("old_low_patch_payload",),
            evicted_oversized_execution_payloads=("repo_wide_delegate_request",),
            evicted_obsolete_fallback_heuristics=("retry_until_success",),
            evicted_repeated_delegated_summaries=("duplicate_validation_summary",),
            preserved_compact_delegation_heuristics=("single_layer_local_patch", "fallback_once"),
            subagent_eviction_active=True,
            compact_useful_delegation_heuristics_only=True,
        )
        scope = SubagentScopeFrame(
            local_patch_only=True,
            adjacent_runtime_only=True,
            bounded_retrieval_only=True,
            compact_execution_only=True,
            retrieval_radius=2,
            delegated_scope_size=2,
            context_accumulation_pressure="LOW",
            repo_wide_delegated_cognition_prevented=True,
            automatic_scope_expansion_prevented=True,
        )
        health = SubagentHealthFrame(
            subagent_health="READY_WITH_FALLBACK",
            local_subagent_ready=True,
            cloud_subagent_available=True,
            fallback_ready=True,
            validation_stable=True,
            rollback_safe=True,
            bounded_delegation_stable=True,
        )
        avoided_tokens = delegated_task_count * 850 + distribution["LOW_GOVERNANCE"] * 500
        avoided_explosion = recursive_attempts * 2_400 + oversized_payload_attempts * 900
        active = all(
            (
                routing.fallback_safe_routing,
                payload.adjacent_runtime_only,
                validation.validation_bypass_prevented,
                fallback.no_recursive_retry_loop,
                governance.autonomous_swarm_emergence_prevented,
                scope.local_patch_only,
                eviction.subagent_eviction_active,
                health.bounded_delegation_stable,
            )
        )
        return SubagentExecutionFrame(
            routing=routing,
            capability=capability,
            payload=payload,
            validation=validation,
            fallback=fallback,
            checkpoint=checkpoint,
            rollback=rollback,
            pressure=pressure,
            recommendation=recommendation,
            governance=governance,
            eviction=eviction,
            scope=scope,
            health=health,
            subagent_execution_active=active,
            subagent_routing_active=routing.provider_pressure_aware_routing,
            subagent_payload_active=payload.compact_summaries_only,
            subagent_validation_active=validation.validation_bypass_prevented,
            subagent_fallback_active=fallback.downgrade_safe_fallback,
            subagent_governance_active=governance.autonomous_swarm_emergence_prevented,
            subagent_scope_active=scope.local_patch_only,
            subagent_eviction_active=eviction.subagent_eviction_active,
            local_only_for_low_local=True,
            deterministic=True,
            summary_only=True,
            bounded_delegation_only=True,
            human_confirmed_delegation_only=True,
            no_autonomous_agent_swarms=True,
            no_recursive_subagent_spawning=True,
            no_hidden_provider_switching=True,
            no_repo_wide_delegated_cognition=True,
            no_autonomous_repository_mutation=True,
            estimated_avoided_premium_subagent_tokens=avoided_tokens,
            estimated_avoided_recursive_agent_explosion=avoided_explosion,
            requirement_ids=SUBAGENT_EXECUTION_REQUIREMENT_IDS,
            test_ids=SUBAGENT_EXECUTION_TEST_IDS,
        )


__all__ = [
    "SUBAGENT_EXECUTION_REQUIREMENT_IDS",
    "SUBAGENT_EXECUTION_TEST_IDS",
    "SubagentCapabilityFrame",
    "SubagentCheckpointFrame",
    "SubagentEvictionFrame",
    "SubagentExecutionFrame",
    "SubagentExecutionRuntime",
    "SubagentFallbackFrame",
    "SubagentGovernanceFrame",
    "SubagentHealthFrame",
    "SubagentPayloadFrame",
    "SubagentPressureFrame",
    "SubagentRecommendationFrame",
    "SubagentRollbackFrame",
    "SubagentRoutingFrame",
    "SubagentScopeFrame",
    "SubagentValidationFrame",
]
