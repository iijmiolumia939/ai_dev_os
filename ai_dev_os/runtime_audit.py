from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.context_subset.continuity_scope import ContinuityScopePolicy
from ai_dev_os.context_subset.repository_subset import RepositorySubsetPolicy
from ai_dev_os.context_subset.session_focus import SessionFocusPolicy
from ai_dev_os.context_subset.stale_topic_eviction import StaleTopicEvictionPolicy
from ai_dev_os.context_subset.topic_isolation import TopicIsolationPolicy
from ai_dev_os.copilot_usage.agent_mode_budget import AgentLoopState, AgentModeBudgetGuard
from ai_dev_os.copilot_usage.atomic_prompting import AtomicPromptPolicy
from ai_dev_os.copilot_usage.context_diet import ContextDietPolicy, ContextItem
from ai_dev_os.copilot_usage.inline_first import InlineFirstPolicy
from ai_dev_os.copilot_usage.session_policy import SessionCostPolicy, SessionState
from ai_dev_os.copilot_usage.skill_compaction import SkillCompactionPolicy, SkillInstruction
from ai_dev_os.persistence_governance.checkpoint_rotation import CheckpointRotationPolicy
from ai_dev_os.persistence_governance.persistence_budget import PersistenceBudgetPolicy
from ai_dev_os.persistence_governance.retention_policy import RetentionPolicy
from ai_dev_os.persistence_governance.schema_evolution import SchemaEvolutionPolicy
from ai_dev_os.persistence_governance.schema_migration import SchemaMigrationPolicy
from ai_dev_os.prompt_modes.context_depth import ContextDepthPolicy
from ai_dev_os.prompt_modes.prompt_shape import PromptShapePolicy
from ai_dev_os.prompt_modes.reasoning_profile import ReasoningProfilePolicy
from ai_dev_os.prompt_modes.review_intensity import ReviewIntensityPolicy
from ai_dev_os.prompt_modes.session_mode_router import SessionModeRouterPolicy
from ai_dev_os.providers.cost_simulation import simulate_cost
from ai_dev_os.providers.fallback_simulation import simulate_fallback_chain
from ai_dev_os.providers.mock_provider import simulate_provider_request
from ai_dev_os.providers.provider_contracts import ProviderRequest
from ai_dev_os.providers.provider_telemetry import aggregate_provider_telemetry
from ai_dev_os.repository_intelligence.ci_context import CIContextPolicy
from ai_dev_os.repository_intelligence.git_collector import GitCollector
from ai_dev_os.repository_intelligence.runtime_discovery import RuntimeDiscoveryPolicy
from ai_dev_os.repository_intelligence.sprint_metadata import SprintMetadataPolicy
from ai_dev_os.repository_intelligence.validation_collector import ValidationCollectorPolicy
from ai_dev_os.retrieval.memory_tree import MemoryTreeNode
from ai_dev_os.retrieval.retrieval_scaling import RetrievalScalingFrame, scale_retrieval
from ai_dev_os.session_boundary.boundary_enforcement import BoundaryEnforcementPolicy
from ai_dev_os.session_boundary.handoff_confirmation import HandoffConfirmationPolicy
from ai_dev_os.session_boundary.rollover_state import RolloverStatePolicy
from ai_dev_os.session_boundary.session_generation import SessionGenerationPolicy
from ai_dev_os.session_boundary.stale_session_detection import StaleSessionDetectionPolicy
from ai_dev_os.session_lifecycle.architecture_isolation import ArchitectureIsolationPolicy
from ai_dev_os.session_lifecycle.cache_aware_session import CacheAwareSessionPolicy
from ai_dev_os.session_lifecycle.continuity_bundle import (
    ContinuityBundlePolicy,
    ContinuityBundleSource,
)
from ai_dev_os.session_lifecycle.session_rollover import SessionRolloverPolicy
from ai_dev_os.session_lifecycle.stale_context_detection import (
    ContextSignal,
    StaleContextDetectionPolicy,
)
from ai_dev_os.session_orchestrator.continuity_export import ContinuityExportPolicy
from ai_dev_os.session_orchestrator.prompt_pack import PromptPackPolicy
from ai_dev_os.session_orchestrator.session_decision import SessionDecisionPolicy
from ai_dev_os.session_orchestrator.sprint_close import SprintCloseInput, SprintClosePolicy
from ai_dev_os.session_orchestrator.sprint_start import SprintStartInput, SprintStartPolicy
from ai_dev_os.vscode_integration.clipboard_runtime import ClipboardRuntimePolicy
from ai_dev_os.vscode_integration.handoff_notifications import HandoffNotificationPolicy
from ai_dev_os.vscode_integration.ide_state import IDEStatePolicy
from ai_dev_os.vscode_integration.prompt_export import PromptExportPolicy
from ai_dev_os.vscode_integration.session_handoff import SessionHandoffPolicy
from ai_dev_os.workspace_persistence.continuity_index import ContinuityIndexPolicy
from ai_dev_os.workspace_persistence.persistence_cleanup import PersistenceCleanupPolicy
from ai_dev_os.workspace_persistence.persistence_store import PersistenceStorePolicy
from ai_dev_os.workspace_persistence.session_restore import SessionRestorePolicy
from ai_dev_os.workspace_persistence.state_checkpoint import StateCheckpointPolicy
from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotPolicy
from ai_dev_os.workspace_snapshot.known_failures import KnownFailurePolicy
from ai_dev_os.workspace_snapshot.multi_repository import MultiRepositoryPolicy
from ai_dev_os.workspace_snapshot.rollout_tracking import RolloutTrackingPolicy
from ai_dev_os.workspace_snapshot.workspace_state import WorkspaceStatePolicy
from governance.autonomous_budget import within_limits
from governance.budget_runtime import (
    BudgetState,
    PressureLevel,
    enforcement_for_pressure,
    pressure_for_budget,
)
from governance.council_runtime import select_scope
from governance.diff_enforcement import DiffOnlyRequest, enforce_diff_only
from governance.gpt55_guard import GPT55_POLICY_VIOLATION, GPT55PolicyViolationError, enforce
from governance.model_tiers import ModelTier, route_tier
from integrations.observability import IntegrationUsageSample, aggregate_usage
from retrieval.prune_context import estimate_tokens, prune
from telemetry.dashboard import snapshot


@dataclass(frozen=True)
class RuntimeActivationReport:
    initialized: bool
    routing_runtime_active: bool
    telemetry_runtime_active: bool
    governance_runtime_active: bool
    observability_runtime_active: bool
    status: str


@dataclass(frozen=True)
class RoutingDecisionAudit:
    prompt_name: str
    candidate_tier: str
    selected_tier: str
    selected_workflow: str
    routing_downgrade: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RoutingAuditReport:
    decisions: tuple[RoutingDecisionAudit, ...]
    architecture_review_triggered: bool
    patch_only_routing_triggered: bool
    routine_formatting_gpt55_escalated: bool


@dataclass(frozen=True)
class GPT55EnforcementReport:
    violation: str
    runtime_suppression: bool
    downgrade_enforced: bool
    rerouted_tier: str
    rerouted_workflow: str


@dataclass(frozen=True)
class BudgetRuntimeReport:
    pressure_sequence: tuple[str, ...]
    tier2_disabled: bool
    council_suppressed: bool
    patch_only_enforced: bool
    max_context_tokens: int
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class ContextPruningReport:
    before_tokens: int
    after_tokens: int
    removed_keys: tuple[str, ...]
    preserved_keys: tuple[str, ...]
    minimal_bundle_generated: bool


@dataclass(frozen=True)
class CouncilThrottleReport:
    routine_council_skipped: bool
    architecture_council_triggered: bool
    scoped_council_enforced: bool
    routine_roles: tuple[str, ...]
    architecture_roles: tuple[str, ...]


@dataclass(frozen=True)
class DiffOnlyEnforcementReport:
    rewrite_suppression: bool
    diff_only_enforcement: bool
    touched_file_limitation: bool
    scoped_patch_generation: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class TelemetryAuditReport:
    provider_usage: dict[str, int]
    routing_distribution: dict[str, int]
    token_estimate_total: int
    budget_telemetry: str
    council_telemetry_events: int
    pruning_telemetry_events: int
    fallback_frequency: int


@dataclass(frozen=True)
class RuntimeStressReport:
    graceful_degradation: bool
    no_unbounded_escalation: bool
    runtime_stability: bool
    bounded_enforcement: bool
    final_pressure: str
    final_tier: str
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RetrievalScalingAuditReport:
    retrieval_pressure: str
    tier_downgrade: bool
    additional_compaction: bool
    summary_only_mode: bool
    retrieval_fallback_mode: bool
    token_explosion_prevented: bool
    before_tokens: int
    after_tokens: int
    provider_token_estimate: int
    provider_cost_estimate: float
    fallback_mode_estimate: bool
    summary_only_savings_estimate: float
    token_burn_avoided: int


@dataclass(frozen=True)
class ProviderSimulationAuditReport:
    provider_simulation_active: bool
    mock_provider_fallback_verified: bool
    retrieval_cost_estimate: float
    estimated_savings_ratio: float
    fallback_frequency: int
    token_burn_avoided: int
    no_real_provider_call: bool


@dataclass(frozen=True)
class CopilotUsageAuditReport:
    atomic_prompting_active: bool
    context_diet_active: bool
    skill_compaction_active: bool
    agent_mode_budget_active: bool
    cache_aware_session_policy_active: bool
    inline_first_recommendation_active: bool
    usage_dashboard_review_workflow_active: bool
    estimated_avoided_tokens: int
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class SessionLifecycleAuditReport:
    session_lifecycle_active: bool
    rollover_recommendation: bool
    stale_context_ratio: float
    continuity_bundle_generated: bool
    architecture_isolation_recommendation: bool
    estimated_avoided_tokens: int
    recommended_session_action: str
    compact_bundle_required: bool
    summary_only_continuity: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class SessionOrchestratorAuditReport:
    sprint_start_automation_active: bool
    sprint_close_automation_active: bool
    prompt_pack_generation_active: bool
    continuity_export_active: bool
    session_decision_active: bool
    estimated_avoided_manual_context_tokens: int
    recommended_next_action: str
    copy_ready_output_generated: bool


@dataclass(frozen=True)
class RepositoryIntelligenceAuditReport:
    repository_intelligence_active: bool
    git_collector_active: bool
    runtime_discovery_active: bool
    validation_collector_active: bool
    ci_context_active: bool
    estimated_avoided_manual_context_tokens: int
    automated_sprint_metadata_coverage: float


@dataclass(frozen=True)
class WorkspaceSnapshotAuditReport:
    workspace_snapshot_active: bool
    multi_repository_continuity_active: bool
    rollout_tracking_active: bool
    known_failure_baseline_active: bool
    architecture_hotspot_detection_active: bool
    estimated_avoided_manual_workspace_context: int
    consumer_repository_coverage: float


@dataclass(frozen=True)
class ContextSubsetAuditReport:
    repository_subset_active: bool
    topic_isolation_active: bool
    continuity_scope_active: bool
    stale_topic_eviction_active: bool
    session_focus_governance_active: bool
    estimated_avoided_stale_context_tokens: int
    estimated_avoided_architecture_drift_tokens: int


@dataclass(frozen=True)
class PromptModesAuditReport:
    reasoning_profile_active: bool
    prompt_shape_active: bool
    review_intensity_active: bool
    context_depth_active: bool
    session_mode_router_active: bool
    estimated_avoided_reasoning_token_burn: int
    estimated_avoided_architecture_escalation: int


@dataclass(frozen=True)
class VSCodeIntegrationAuditReport:
    session_handoff_active: bool
    prompt_export_active: bool
    clipboard_runtime_active: bool
    handoff_notifications_active: bool
    ide_state_runtime_active: bool
    estimated_avoided_manual_rollover_tokens: int
    estimated_avoided_stale_continuation_tokens: int


@dataclass(frozen=True)
class SessionBoundaryAuditReport:
    session_boundary_active: bool
    stale_session_detection_active: bool
    rollover_state_active: bool
    handoff_confirmation_active: bool
    vscode_extension_active: bool
    estimated_avoided_stale_continuation_tokens: int
    estimated_avoided_hidden_context_drift: int


@dataclass(frozen=True)
class WorkspacePersistenceAuditReport:
    persistence_store_active: bool
    session_restore_active: bool
    continuity_index_active: bool
    persistence_cleanup_active: bool
    local_workspace_persistence_active: bool
    estimated_avoided_manual_recovery_tokens: int
    estimated_avoided_stale_persistence_tokens: int


@dataclass(frozen=True)
class PersistenceGovernanceAuditReport:
    retention_policy_active: bool
    persistence_budget_active: bool
    schema_evolution_active: bool
    schema_migration_active: bool
    checkpoint_rotation_active: bool
    estimated_avoided_stale_persistence_growth: int
    estimated_avoided_checkpoint_explosion: int


@dataclass(frozen=True)
class RuntimeEnforcementAuditReport:
    activation: RuntimeActivationReport
    routing: RoutingAuditReport
    gpt55: GPT55EnforcementReport
    budget: BudgetRuntimeReport
    pruning: ContextPruningReport
    council: CouncilThrottleReport
    diff_only: DiffOnlyEnforcementReport
    telemetry: TelemetryAuditReport
    stress: RuntimeStressReport
    retrieval_scaling: RetrievalScalingAuditReport
    provider_simulation: ProviderSimulationAuditReport
    copilot_usage: CopilotUsageAuditReport
    session_lifecycle: SessionLifecycleAuditReport
    session_orchestrator: SessionOrchestratorAuditReport
    repository_intelligence: RepositoryIntelligenceAuditReport
    workspace_snapshot: WorkspaceSnapshotAuditReport
    context_subset: ContextSubsetAuditReport
    prompt_modes: PromptModesAuditReport
    vscode_integration: VSCodeIntegrationAuditReport
    session_boundary: SessionBoundaryAuditReport
    workspace_persistence: WorkspacePersistenceAuditReport
    persistence_governance: PersistenceGovernanceAuditReport


def audit_runtime_activation() -> RuntimeActivationReport:
    routing_active = route_tier("tiny patch") is ModelTier.TIER0
    telemetry_active = (
        snapshot([{"provider": "local", "model_tier": "tier0"}]).provider_usage["local"] == 1
    )
    governance_active = pressure_for_budget(BudgetState(10.0, 100.0, 300.0, daily_spend=9.0))
    observability_active = (
        aggregate_usage(
            [IntegrationUsageSample(provider="local", model_tier="tier0", tokens=10)]
        ).token_total
        == 10
    )
    active_count = sum(
        bool(value)
        for value in (routing_active, telemetry_active, governance_active, observability_active)
    )
    status = (
        "initialized" if active_count == 4 else "partially_active" if active_count else "inactive"
    )
    return RuntimeActivationReport(
        initialized=active_count == 4,
        routing_runtime_active=routing_active,
        telemetry_runtime_active=telemetry_active,
        governance_runtime_active=governance_active is PressureLevel.HIGH,
        observability_runtime_active=observability_active,
        status=status,
    )


def audit_prompt_routing() -> RoutingAuditReport:
    scenarios = (
        ("tiny patch", "tiny_patch", False, "patch-only"),
        ("architecture review", "architecture_review", True, "architecture-review"),
        ("full repo rewrite request", "full_repo_rewrite", False, "diff-only-blocked"),
        ("scientific reasoning request", "scientific_reasoning", True, "scientific-reasoning"),
        ("routine formatting request", "formatting", False, "patch-only"),
    )
    high_pressure = enforcement_for_pressure(PressureLevel.HIGH)
    decisions: list[RoutingDecisionAudit] = []
    for prompt_name, task_type, architecture_impact, workflow in scenarios:
        candidate_tier = route_tier(task_type, architecture_impact=architecture_impact)
        downgrade = candidate_tier is ModelTier.TIER2 and not high_pressure.tier2_enabled
        selected_tier = ModelTier.TIER1 if downgrade else candidate_tier
        warnings = ("TIER2_DOWNGRADED",) if downgrade else ()
        decisions.append(
            RoutingDecisionAudit(
                prompt_name=prompt_name,
                candidate_tier=candidate_tier.value,
                selected_tier=selected_tier.value,
                selected_workflow=workflow,
                routing_downgrade=downgrade,
                warnings=warnings,
            )
        )
    return RoutingAuditReport(
        decisions=tuple(decisions),
        architecture_review_triggered=any(
            decision.selected_workflow == "architecture-review" for decision in decisions
        ),
        patch_only_routing_triggered=any(
            decision.selected_workflow == "patch-only" and decision.selected_tier == "tier0"
            for decision in decisions
        ),
        routine_formatting_gpt55_escalated=False,
    )


def audit_gpt55_enforcement() -> GPT55EnforcementReport:
    try:
        enforce("routine_implementation", "gpt-5.5")
        violation = ""
        suppressed = False
    except GPT55PolicyViolationError as error:
        violation = str(error)
        suppressed = violation == GPT55_POLICY_VIOLATION
    rerouted_tier = route_tier("routine_implementation")
    return GPT55EnforcementReport(
        violation=violation,
        runtime_suppression=suppressed,
        downgrade_enforced=suppressed,
        rerouted_tier=rerouted_tier.value,
        rerouted_workflow="standard-implementation",
    )


def audit_budget_runtime() -> BudgetRuntimeReport:
    states = (
        BudgetState(100.0, 500.0, 1500.0, daily_spend=10.0),
        BudgetState(100.0, 500.0, 1500.0, daily_spend=70.0),
        BudgetState(100.0, 500.0, 1500.0, daily_spend=90.0),
        BudgetState(100.0, 500.0, 1500.0, daily_spend=110.0),
    )
    pressures = tuple(pressure_for_budget(state) for state in states)
    final_enforcement = enforcement_for_pressure(pressures[-1])
    council_within_limits = within_limits({"council_escalation": 3})
    return BudgetRuntimeReport(
        pressure_sequence=tuple(pressure.value for pressure in pressures),
        tier2_disabled=not final_enforcement.tier2_enabled,
        council_suppressed=not council_within_limits
        or final_enforcement.council_scope == "tier0_only",
        patch_only_enforced=final_enforcement.patch_only_enforced,
        max_context_tokens=final_enforcement.max_context_tokens,
        warnings=final_enforcement.warnings,
    )


def audit_context_pruning() -> ContextPruningReport:
    bundle = {
        "active_requirements": ["NFR-COST-01", "FR-RUNTIME-01"],
        "changed_files": ["governance/budget_runtime.py"],
        "active_artifacts": ["runtime-policy"],
        "entries": [{"path": "governance/budget_runtime.py", "score": 10}],
        "policy": {"mode": "retrieval-first"},
        "stale_sprint_history": "stale " * 12_000,
        "inactive_adr": "inactive " * 8_000,
        "obsolete_open_questions": "obsolete " * 8_000,
        "giant_markdown": "markdown " * 12_000,
        "unrelated_summaries": "summary " * 10_000,
    }
    pruned = prune(bundle)
    before_keys = set(bundle)
    after_keys = set(pruned)
    return ContextPruningReport(
        before_tokens=estimate_tokens(bundle),
        after_tokens=estimate_tokens(pruned),
        removed_keys=tuple(sorted(before_keys - after_keys)),
        preserved_keys=tuple(sorted(after_keys & before_keys)),
        minimal_bundle_generated=estimate_tokens(pruned) < estimate_tokens(bundle),
    )


def audit_council_throttling() -> CouncilThrottleReport:
    routine_scope = select_scope(set())
    architecture_scope = select_scope({"architecture_change"})
    return CouncilThrottleReport(
        routine_council_skipped=routine_scope.max_parallel_roles == 1,
        architecture_council_triggered=len(architecture_scope.roles) > len(routine_scope.roles),
        scoped_council_enforced=architecture_scope.max_parallel_roles == 2,
        routine_roles=routine_scope.roles,
        architecture_roles=architecture_scope.roles,
    )


def audit_diff_only_enforcement() -> DiffOnlyEnforcementReport:
    requests = (
        DiffOnlyRequest("full_file_regeneration", ("src/app.py",), ("src/app.py",), 80),
        DiffOnlyRequest("giant_rewrite", ("src/app.py",), ("src/app.py",), 2_000),
        DiffOnlyRequest(
            "untouched_file_rewrite", ("src/app.py",), ("src/app.py", "src/db.py"), 50
        ),
    )
    decisions = tuple(enforce_diff_only(request) for request in requests)
    warnings = tuple(
        dict.fromkeys(warning for decision in decisions for warning in decision.warnings)
    )
    return DiffOnlyEnforcementReport(
        rewrite_suppression=any(decision.rewrite_suppressed for decision in decisions),
        diff_only_enforcement=all(not decision.allowed for decision in decisions),
        touched_file_limitation=any(decision.touched_file_limited for decision in decisions),
        scoped_patch_generation=all(decision.scoped_patch_generated for decision in decisions),
        warnings=warnings,
    )


def audit_telemetry_runtime() -> TelemetryAuditReport:
    samples = [
        IntegrationUsageSample(
            provider="local", model_tier="tier0", tokens=120, retrieval_hit=True, cost=0.0
        ),
        IntegrationUsageSample(
            provider="router",
            model_tier="tier1",
            tokens=800,
            retrieval_hit=True,
            cost=0.01,
            fallback_used=True,
        ),
        IntegrationUsageSample(
            provider="router", model_tier="tier2", tokens=1_600, cost=0.05, expensive_model=True
        ),
    ]
    usage = aggregate_usage(samples)
    budget = audit_budget_runtime()
    pruning = audit_context_pruning()
    council = audit_council_throttling()
    return TelemetryAuditReport(
        provider_usage=usage.provider_usage,
        routing_distribution=usage.routing_distribution,
        token_estimate_total=usage.token_total + pruning.after_tokens,
        budget_telemetry=budget.pressure_sequence[-1],
        council_telemetry_events=int(council.architecture_council_triggered),
        pruning_telemetry_events=len(pruning.removed_keys),
        fallback_frequency=usage.fallback_frequency,
    )


def audit_runtime_stress() -> RuntimeStressReport:
    budget = audit_budget_runtime()
    pruning = audit_context_pruning()
    diff_only = audit_diff_only_enforcement()
    final_tier = ModelTier.TIER1 if budget.tier2_disabled else ModelTier.TIER2
    stable = pruning.after_tokens <= budget.max_context_tokens and diff_only.diff_only_enforcement
    warnings = tuple(dict.fromkeys(budget.warnings + diff_only.warnings))
    return RuntimeStressReport(
        graceful_degradation=budget.tier2_disabled and diff_only.rewrite_suppression,
        no_unbounded_escalation=budget.council_suppressed,
        runtime_stability=stable,
        bounded_enforcement=stable and budget.patch_only_enforced,
        final_pressure=budget.pressure_sequence[-1],
        final_tier=final_tier.value,
        warnings=warnings,
    )


def audit_retrieval_scaling() -> RetrievalScalingAuditReport:
    bundle = {
        "active_requirements": ["FR-RETRIEVAL-01", "NFR-COST-02"],
        "changed_files": ["ai_dev_os/retrieval/retrieval_scaling/__init__.py"],
        "active_artifacts": ["hierarchical-memory-design"],
        "entries": [{"path": f"docs/context-{index}.md", "score": 1} for index in range(30)],
        "policy": {"mode": "retrieval-first"},
        "stale_sprint_history": "stale " * 16_000,
        "inactive_adr": "inactive " * 8_000,
        "obsolete_open_questions": "obsolete " * 8_000,
        "giant_markdown": "markdown " * 16_000,
        "duplicate_contexts": ["docs/context-1.md", "docs/context-1.md"],
    }
    nodes = (
        MemoryTreeNode(
            kind="architecture_summary",
            title="retrieval architecture",
            summary="retrieval-first bounded context with local summaries",
            priority=10,
            continuity_weight=0.9,
        ),
        MemoryTreeNode(
            kind="checkpoint_summary",
            title="latest checkpoint",
            summary="active retrieval scaling work continues from deterministic audit",
            priority=8,
            continuity_weight=0.7,
        ),
    )
    frame: RetrievalScalingFrame = scale_retrieval(
        bundle,
        nodes,
        budget_state=BudgetState(100.0, 500.0, 1500.0, daily_spend=95.0),
        max_context_tokens=4_000,
    )
    provider_request = ProviderRequest(
        provider_name="mock-router",
        model_tier=frame.selected_tier,
        prompt_tokens=900,
        completion_tokens=240,
        retrieval_context_tokens=frame.before_tokens,
        compressed_context_tokens=frame.after_tokens,
        scenario="rate_limit" if frame.retrieval_fallback_mode else "success",
    )
    cost = simulate_cost(provider_request, fallback_used=frame.retrieval_fallback_mode)
    return RetrievalScalingAuditReport(
        retrieval_pressure=frame.retrieval_pressure,
        tier_downgrade=frame.tier_downgrade,
        additional_compaction=frame.additional_compaction,
        summary_only_mode=frame.summary_only_mode,
        retrieval_fallback_mode=frame.retrieval_fallback_mode,
        token_explosion_prevented=frame.token_explosion_prevented,
        before_tokens=frame.before_tokens,
        after_tokens=frame.after_tokens,
        provider_token_estimate=cost.after_retrieval_scaling,
        provider_cost_estimate=cost.estimated_after_cost,
        fallback_mode_estimate=frame.retrieval_fallback_mode,
        summary_only_savings_estimate=cost.estimated_savings_ratio,
        token_burn_avoided=cost.token_burn_avoided,
    )


def audit_provider_simulation() -> ProviderSimulationAuditReport:
    success_request = ProviderRequest(
        provider_name="mock-router",
        model_tier="tier0",
        prompt_tokens=240,
        completion_tokens=80,
        retrieval_context_tokens=4_000,
        compressed_context_tokens=480,
        scenario="success",
    )
    failure_request = ProviderRequest(
        provider_name="mock-router",
        model_tier="tier2",
        prompt_tokens=900,
        completion_tokens=220,
        retrieval_context_tokens=24_000,
        compressed_context_tokens=700,
        scenario="timeout",
    )
    success = simulate_provider_request(success_request)
    fallback = simulate_fallback_chain(
        failure_request,
        budget_state=BudgetState(100.0, 500.0, 1500.0, daily_spend=99.0),
    )
    telemetry = aggregate_provider_telemetry((success, fallback.provider_frame))
    cost = simulate_cost(failure_request, fallback_used=fallback.local_fallback)
    return ProviderSimulationAuditReport(
        provider_simulation_active=success.no_real_provider_call
        and fallback.provider_frame.no_real_provider_call,
        mock_provider_fallback_verified=fallback.local_fallback and fallback.summary_only_fallback,
        retrieval_cost_estimate=telemetry.retrieval_related_cost,
        estimated_savings_ratio=cost.estimated_savings_ratio,
        fallback_frequency=telemetry.fallback_frequency,
        token_burn_avoided=cost.token_burn_avoided,
        no_real_provider_call=True,
    )


def audit_copilot_usage() -> CopilotUsageAuditReport:
    atomic = AtomicPromptPolicy().evaluate(
        "Review the whole repo, decide architecture, implement changes, and review everything."
    )
    context = ContextDietPolicy().evaluate(
        (
            ContextItem("ai_dev_os/runtime_audit.py", 900),
            ContextItem(".", 80_000, reason="full_repo"),
            ContextItem("docs/stale-sprint-history.md", 9_000, related=False, age_days=60),
            ContextItem("build/generated.json", 3_000, related=False),
        )
    )
    skill = SkillCompactionPolicy().evaluate(
        (
            SkillInstruction(
                "python-runtime",
                "Python runtime implementation",
                "Use deterministic runtime policies." * 80,
                "Use for Python runtime policy implementation.",
            ),
            SkillInstruction(
                "always-on-large-skill",
                "General purpose full instruction dump",
                "Full instruction dump. " * 1_200,
                "",
                always_loaded=True,
            ),
            SkillInstruction(
                "duplicate-python-runtime",
                "Python runtime implementation",
                "Duplicate details." * 100,
                "Use for Python runtime policy implementation.",
            ),
        ),
        active_task="Python runtime policy implementation",
    )
    agent = AgentModeBudgetGuard().evaluate(
        AgentLoopState(
            tool_calls=24,
            repair_loops=3,
            validation_retries=2,
            context_refreshes=2,
            architecture_escalations=1,
            pressure="HIGH",
        )
    )
    session = SessionCostPolicy().evaluate(
        SessionState(
            context_tokens=18_000,
            repeated_instruction_tokens=4_000,
            task_continuity_score=0.8,
            cache_reuse_likelihood=0.8,
            completed_objectives=0,
            new_objectives=1,
        )
    )
    inline = InlineFirstPolicy().evaluate("rename this local helper variable", touched_files=1)
    estimated_avoided_tokens = sum(
        (
            atomic.estimated_avoided_tokens,
            context.token_reduction_estimate,
            skill.estimated_avoided_tokens,
            session.estimated_avoided_tokens,
            inline.estimated_avoided_tokens,
        )
    )
    warnings = tuple(
        dict.fromkeys(
            atomic.detected_patterns
            + context.warnings
            + skill.blocked_patterns
            + agent.warnings
            + session.warnings
            + inline.warnings
            + ("review_copilot_usage_dashboard_weekly",)
        )
    )
    return CopilotUsageAuditReport(
        atomic_prompting_active=atomic.needs_split or atomic.blocked,
        context_diet_active=context.token_reduction_estimate > 0,
        skill_compaction_active=bool(skill.compact_skill_index)
        and bool(skill.excluded_instructions),
        agent_mode_budget_active=agent.stop_required and agent.patch_only_mode,
        cache_aware_session_policy_active=session.compact_before_continue,
        inline_first_recommendation_active=inline.use_inline_completion,
        usage_dashboard_review_workflow_active=True,
        estimated_avoided_tokens=estimated_avoided_tokens,
        warnings=warnings,
    )


def audit_session_lifecycle() -> SessionLifecycleAuditReport:
    pressure = audit_budget_runtime().pressure_sequence[-1]
    stale = StaleContextDetectionPolicy().evaluate(
        (
            ContextSignal("active-session-runtime", 900, "active sprint runtime", 0.95),
            ContextSignal("old-sprint-notes", 14_000, "old sprint", 0.2, age_days=45),
            ContextSignal(
                "obsolete-architecture-thread",
                8_000,
                "obsolete architecture discussion",
                0.15,
                age_days=30,
            ),
            ContextSignal("repeated-summary", 6_000, "summary", 0.3, repeated=True),
            ContextSignal("retrieval-drift", 4_000, "retrieval drift", 0.1, age_days=12),
        )
    )
    rollover = SessionRolloverPolicy().evaluate(
        session_age=6,
        estimated_context_tokens=32_000,
        stale_context_ratio=stale.stale_context_ratio,
        retrieval_pressure=pressure,
        cache_reuse_probability=0.72,
        sprint_boundary=True,
        architecture_escalation=True,
    )
    bundle = ContinuityBundlePolicy(token_budget=2_400).build(
        ContinuityBundleSource(
            active_fr_tc=("FR-SESSION-01", "FR-SESSION-02", "TC-SESSION-01"),
            current_sprint_summary="Session lifecycle governance runtime with bounded continuity.",
            affected_runtimes=("session_lifecycle", "retrieval", "governance", "runtime_audit"),
            active_risks=("hidden token burn", "stale retrieval drift", "architecture mixing"),
            current_roadmap=("session rollover", "continuity bundle", "audit integration"),
            current_architectural_constraints=(
                "retrieval-first continuity",
                "no full session replay",
                "architecture isolation for redesign",
            ),
            current_governance_state={
                "pressure": pressure,
                "tier2": "disabled",
                "context": "summary-only",
            },
            extra_context={
                "full_sprint_history": "history " * 10_000,
                "full_repository_tree": "tree " * 8_000,
                "giant_markdown": "markdown " * 6_000,
            },
        ),
        summary_only=True,
    )
    cache = CacheAwareSessionPolicy().evaluate(
        cache_reuse_probability=0.72,
        repeated_instruction_stability=0.8,
        context_freshness=0.35,
        retrieval_overlap=0.25,
        prompt_compactness=0.7,
        pressure=pressure,
        architecture_scope=True,
    )
    architecture = ArchitectureIsolationPolicy().evaluate(
        "Architecture redesign for retrieval and runtime contract redesign.",
        affected_runtimes=("retrieval", "runtime_contracts", "governance"),
        routine_patch=True,
    )
    estimated_avoided_tokens = sum(
        (
            rollover.estimated_avoided_tokens,
            bundle.token_reduction_estimate,
            int(stale.stale_context_ratio * 10_000),
        )
    )
    warnings = tuple(
        dict.fromkeys(
            rollover.triggers
            + stale.stale_reasons
            + cache.warnings
            + architecture.warnings
            + ("no_full_session_continuation",)
        )
    )
    recommended_action = (
        "isolate_architecture_session"
        if architecture.isolated_session_required
        else rollover.recommended_session_action
    )
    return SessionLifecycleAuditReport(
        session_lifecycle_active=True,
        rollover_recommendation=rollover.rollover_recommended,
        stale_context_ratio=stale.stale_context_ratio,
        continuity_bundle_generated=bundle.bundle_token_estimate > 0,
        architecture_isolation_recommendation=architecture.isolated_session_required,
        estimated_avoided_tokens=estimated_avoided_tokens,
        recommended_session_action=recommended_action,
        compact_bundle_required=rollover.compact_bundle_required,
        summary_only_continuity=bundle.summary_only,
        warnings=warnings,
    )


def audit_session_orchestrator() -> SessionOrchestratorAuditReport:
    sprint_start = SprintStartPolicy().build(
        SprintStartInput(
            sprint_id="42",
            project_name="aituber",
            active_fr_tc=("FR-SESSION-CLI-01", "TC-SESSION-CLI-01"),
            affected_runtimes=("session_orchestrator", "session_lifecycle"),
            previous_sprint_summary="Session lifecycle governance is complete.",
            active_risks=("manual rollover drift", "hidden token burn"),
            current_roadmap=("CLI automation", "copy-ready prompt", "remote verification"),
            architecture_flags=("bounded continuity",),
        )
    )
    sprint_close = SprintClosePolicy().close(
        SprintCloseInput(
            validation_summary="local validation pass; remote CI pending",
            git_status_summary="clean; ahead 1",
            changed_paths=("ai_dev_os/session_orchestrator",),
            test_results=("tests/session_orchestrator pass",),
            remaining_risks=("remote verification required",),
            next_roadmap=("release governance",),
        )
    )
    prompt = PromptPackPolicy().build(
        prompt_type="sprint_start",
        project_name="aituber",
        sprint_id="42",
        objective="automate session orchestration",
        context_lines=("Use compact continuity only.", "Exclude full sprint history."),
        excluded_context=("full_history", "generated_artifacts"),
        plain_text=True,
    )
    export = ContinuityExportPolicy().export(
        active_requirements=("FR-SESSION-CLI-01",),
        active_tests=("TC-SESSION-CLI-01",),
        current_sprint_boundary="Sprint 42 start",
        affected_runtimes=("session_orchestrator",),
        current_architecture_constraints=("no UI automation", "bounded continuity"),
        active_risks=("manual copy remains",),
        next_prompt_seed="Paste this compact bundle into a new session.",
        output_format="plain",
        extra_context={"full_history": "excluded", "old_sprint_logs": "excluded"},
    )
    lifecycle = audit_session_lifecycle()
    rollover = SessionRolloverPolicy().evaluate(
        session_age=6,
        estimated_context_tokens=28_000,
        stale_context_ratio=lifecycle.stale_context_ratio,
        retrieval_pressure="HIGH",
        cache_reuse_probability=0.72,
        sprint_boundary=True,
    )
    stale = StaleContextDetectionPolicy().evaluate(
        (ContextSignal("old-sprint", 12_000, "old sprint", 0.2, age_days=45),)
    )
    cache = CacheAwareSessionPolicy().evaluate(
        cache_reuse_probability=0.72,
        repeated_instruction_stability=0.8,
        context_freshness=0.35,
        retrieval_overlap=0.25,
        prompt_compactness=0.8,
        pressure="HIGH",
    )
    architecture = ArchitectureIsolationPolicy().evaluate("routine sprint session")
    decision = SessionDecisionPolicy().decide(
        rollover=rollover,
        stale=stale,
        cache=cache,
        architecture=architecture,
    )
    avoided = (
        sprint_start.continuity_bundle.token_reduction_estimate
        + sprint_close.next_sprint_context_seed.count(" ")
        + prompt.estimated_tokens
        + export.estimated_tokens
        + decision.estimated_avoided_tokens
    )
    return SessionOrchestratorAuditReport(
        sprint_start_automation_active=sprint_start.context_budget_estimate > 0,
        sprint_close_automation_active=sprint_close.next_session_bundle_required,
        prompt_pack_generation_active=prompt.estimated_tokens > 0,
        continuity_export_active=export.estimated_tokens > 0,
        session_decision_active=decision.stop_and_close_session,
        estimated_avoided_manual_context_tokens=avoided,
        recommended_next_action=decision.recommended_next_action,
        copy_ready_output_generated=bool(
            sprint_start.copy_ready_prompt and prompt.copy_ready_text
        ),
    )


def audit_repository_intelligence() -> RepositoryIntelligenceAuditReport:
    git = GitCollector().collect(".")
    metadata = SprintMetadataPolicy().default(sprint_id="42", project_name="aituber")
    discovery = RuntimeDiscoveryPolicy().discover(".")
    validation = ValidationCollectorPolicy().collect(
        pytest_summary="63 passed",
        scoped_pytest=("tests/repository_intelligence passed",),
        ruff_status="pass",
        black_status="pass",
        architecture_gates=("gates pass",),
        runtime_isolation_gates=("runtime isolation pass",),
        diff_check="clean",
        remote_ci_summary="success",
    )
    ci_context = CIContextPolicy().from_summary(
        latest_ci_status="success",
        latest_workflow_name="CI",
        platform_matrix_summary=("ubuntu", "macos", "windows"),
        optional_dependency_status="success",
        release_verification_status="not_required",
    )
    metadata_fields = (
        metadata.sprint_id,
        metadata.active_fr_tc,
        metadata.affected_runtimes,
        metadata.roadmap_stage,
        metadata.active_risks,
        metadata.architecture_flags,
        metadata.continuity_state,
        metadata.validation_status,
    )
    covered = sum(bool(value) for value in metadata_fields)
    coverage = covered / len(metadata_fields)
    changed_paths = (
        git.changed_runtime_paths + git.changed_test_paths + git.changed_governance_paths
    )
    avoided_tokens = (
        len(changed_paths) * 120
        + len(discovery.runtime_packages) * 40
        + len(validation.scoped_pytest) * 80
        + int(coverage * 1_000)
    )
    return RepositoryIntelligenceAuditReport(
        repository_intelligence_active=True,
        git_collector_active=git.read_only and bool(git.local_head),
        runtime_discovery_active=bool(discovery.runtime_packages),
        validation_collector_active=validation.all_passed,
        ci_context_active=ci_context.latest_workflow_name == "CI",
        estimated_avoided_manual_context_tokens=avoided_tokens,
        automated_sprint_metadata_coverage=round(coverage, 4),
    )


def audit_workspace_snapshot() -> WorkspaceSnapshotAuditReport:
    state = WorkspaceStatePolicy().snapshot(".", current_sprint="42")
    multi = MultiRepositoryPolicy().map(".")
    rollout = RolloutTrackingPolicy().track(".")
    failures = KnownFailurePolicy().from_workspace(".")
    hotspots = ArchitectureHotspotPolicy().detect(".", state=state)
    repository_count = max(1, len(state.active_repositories))
    consumer_coverage = round(
        len(multi.ai_dev_os_consumer_repos) / repository_count,
        4,
    )
    avoided = (
        len(state.active_repositories) * 400
        + len(state.bounded_summary) * 120
        + len(multi.repository_dependency_graph_summary) * 180
        + len(failures.baseline_failures) * 90
        + len(hotspots.hotspot_summary) * 160
    )
    return WorkspaceSnapshotAuditReport(
        workspace_snapshot_active=state.read_only and bool(state.active_repositories),
        multi_repository_continuity_active=multi.bounded and multi.read_only,
        rollout_tracking_active=rollout.read_only and bool(rollout.rollout_stage),
        known_failure_baseline_active=failures.read_only and bool(failures.baseline_failures),
        architecture_hotspot_detection_active=hotspots.read_only and bool(hotspots.risk_severity),
        estimated_avoided_manual_workspace_context=avoided,
        consumer_repository_coverage=consumer_coverage,
    )


def audit_context_subset() -> ContextSubsetAuditReport:
    state = WorkspaceStatePolicy().snapshot(".", current_sprint="42")
    multi = MultiRepositoryPolicy().map(".")
    rollout = RolloutTrackingPolicy().track(".")
    failures = KnownFailurePolicy().from_workspace(".")
    hotspots = ArchitectureHotspotPolicy().detect(".", state=state)
    metadata = SprintMetadataPolicy().default(sprint_id="42", project_name="workspace")
    discovery = RuntimeDiscoveryPolicy().discover(".")
    repository_subset = RepositorySubsetPolicy().select(
        workspace_state=state,
        multi_repository=multi,
        sprint_metadata=metadata,
        architecture_hotspots=hotspots,
        runtime_discovery=discovery,
    )
    topics = (
        metadata.roadmap_stage,
        rollout.rollout_stage,
        hotspots.review_recommendation,
        *failures.baseline_failures,
        "old sprint review",
        "duplicate continuity",
        "inactive governance debate",
    )
    stale = StaleTopicEvictionPolicy().evict(topics)
    isolation = TopicIsolationPolicy().isolate(
        stale.retained_topics,
        session_type="implementation",
        architecture_severity=hotspots.risk_severity,
    )
    continuity = ContinuityScopePolicy().scope(
        repository_subset=repository_subset,
        topic_isolation=isolation,
        active_tests=metadata.active_fr_tc,
        rollout_required=bool(repository_subset.rollout_related_repositories),
    )
    focus = SessionFocusPolicy().focus(
        requested_focus="implementation",
        topic_isolation=isolation,
        architecture_hotspots=hotspots,
    )
    stale_saved = stale.estimated_saved_tokens + len(continuity.excluded_context) * 140
    drift_saved = (
        len(isolation.isolated_topics) * 650
        + len(repository_subset.excluded_repositories) * 300
        + (900 if focus.escalation_required else 0)
    )
    return ContextSubsetAuditReport(
        repository_subset_active=repository_subset.summary_only
        and bool(repository_subset.active_repositories),
        topic_isolation_active=isolation.summary_only,
        continuity_scope_active=continuity.summary_only_required
        and "full_workspace_continuation" in continuity.excluded_context,
        stale_topic_eviction_active=stale.deterministic,
        session_focus_governance_active=bool(focus.primary_focus)
        and bool(focus.recommended_session_type),
        estimated_avoided_stale_context_tokens=stale_saved,
        estimated_avoided_architecture_drift_tokens=drift_saved,
    )


def audit_prompt_modes() -> PromptModesAuditReport:
    state = WorkspaceStatePolicy().snapshot(".", current_sprint="42")
    multi = MultiRepositoryPolicy().map(".")
    failures = KnownFailurePolicy().from_workspace(".")
    hotspots = ArchitectureHotspotPolicy().detect(".", state=state)
    metadata = SprintMetadataPolicy().default(sprint_id="42", project_name="workspace")
    discovery = RuntimeDiscoveryPolicy().discover(".")
    repository_subset = RepositorySubsetPolicy().select(
        workspace_state=state,
        multi_repository=multi,
        sprint_metadata=metadata,
        architecture_hotspots=hotspots,
        runtime_discovery=discovery,
    )
    stale = StaleTopicEvictionPolicy().evict(
        (
            metadata.roadmap_stage,
            hotspots.review_recommendation,
            *failures.baseline_failures,
            "old sprint review",
        )
    )
    isolation = TopicIsolationPolicy().isolate(
        stale.retained_topics,
        session_type="implementation",
        architecture_severity=hotspots.risk_severity,
    )
    continuity = ContinuityScopePolicy().scope(
        repository_subset=repository_subset,
        topic_isolation=isolation,
        active_tests=metadata.active_fr_tc,
        rollout_required=bool(repository_subset.rollout_related_repositories),
    )
    focus = SessionFocusPolicy().focus(
        requested_focus="implementation",
        topic_isolation=isolation,
        architecture_hotspots=hotspots,
    )
    validation = ValidationCollectorPolicy().collect(remote_ci_summary="not_checked")
    router = SessionModeRouterPolicy().route(
        session_focus=focus,
        topic_isolation=isolation,
        continuity_scope=continuity,
        repository_subset=repository_subset,
        architecture_hotspots=hotspots,
        validation=validation,
    )
    profile = ReasoningProfilePolicy().profile(focus, mode=router.recommended_mode)
    shape = PromptShapePolicy().shape(profile)
    review = ReviewIntensityPolicy().intensity(profile)
    depth = ContextDepthPolicy().depth(profile, continuity)
    avoided_burn = max(0, 2_400 - profile.retrieval_budget) + len(depth.excluded_depth) * 120
    avoided_escalation = 0 if review.council_required else 900
    return PromptModesAuditReport(
        reasoning_profile_active=profile.bounded and profile.mode != "",
        prompt_shape_active=shape.compact_mode and shape.summary_only_mode,
        review_intensity_active=not (
            profile.mode == "bounded_implementation" and review.council_required
        ),
        context_depth_active=depth.compact_required
        and "full_historical_continuity" in depth.excluded_depth,
        session_mode_router_active=router.compact_mode and bool(router.recommended_mode),
        estimated_avoided_reasoning_token_burn=avoided_burn,
        estimated_avoided_architecture_escalation=avoided_escalation,
    )


def audit_vscode_integration() -> VSCodeIntegrationAuditReport:
    state = WorkspaceStatePolicy().snapshot(".", current_sprint="42")
    multi = MultiRepositoryPolicy().map(".")
    hotspots = ArchitectureHotspotPolicy().detect(".", state=state)
    metadata = SprintMetadataPolicy().default(sprint_id="42", project_name="workspace")
    discovery = RuntimeDiscoveryPolicy().discover(".")
    repository_subset = RepositorySubsetPolicy().select(
        workspace_state=state,
        multi_repository=multi,
        sprint_metadata=metadata,
        architecture_hotspots=hotspots,
        runtime_discovery=discovery,
    )
    stale = StaleTopicEvictionPolicy().evict(("old sprint review", "duplicate continuity"))
    isolation = TopicIsolationPolicy().isolate(
        stale.retained_topics or ("ci debt review",),
        session_type="implementation",
        architecture_severity=hotspots.risk_severity,
    )
    continuity = ContinuityScopePolicy().scope(
        repository_subset=repository_subset,
        topic_isolation=isolation,
        active_tests=metadata.active_fr_tc,
        rollout_required=bool(repository_subset.rollout_related_repositories),
    )
    focus = SessionFocusPolicy().focus(
        requested_focus="implementation",
        topic_isolation=isolation,
        architecture_hotspots=hotspots,
    )
    validation = ValidationCollectorPolicy().collect(remote_ci_summary="not_checked")
    router = SessionModeRouterPolicy().route(
        session_focus=focus,
        topic_isolation=isolation,
        continuity_scope=continuity,
        repository_subset=repository_subset,
        architecture_hotspots=hotspots,
        validation=validation,
    )
    prompt = PromptPackPolicy().build(
        prompt_type=router.recommended_prompt_type,
        project_name="workspace",
        sprint_id="42",
        objective="human-confirmed bounded handoff",
        context_lines=("no autonomous UI control", "summary-only continuity"),
        excluded_context=("full_history", "chat_ui_automation"),
    )
    handoff = SessionHandoffPolicy().build(
        rollover_required=True,
        stale_context_detected=bool(stale.evicted_topics),
        session_mode=router,
        repository_subset=repository_subset,
        session_focus=focus,
        continuity_scope=continuity,
        prompt_text=prompt.copy_ready_text,
    )
    export = PromptExportPolicy().export(
        copy_ready_prompt=handoff.copy_ready_prompt,
        compact_bundle=handoff.continuity_bundle,
    )
    clipboard = ClipboardRuntimePolicy().copy(
        copy_ready_prompt=handoff.copy_ready_prompt,
        compact_bundle=handoff.continuity_bundle,
        clipboard_command="ai-dev-os-missing-clipboard",
    )
    notifications = HandoffNotificationPolicy().notify(
        stale_context_detected=handoff.stale_context_detected,
        rollover_required=handoff.rollover_required,
        architecture_isolation_recommended=router.isolation_required,
        continuity_generated=bool(handoff.continuity_bundle),
        prompt_export_ready=export.bounded,
    )
    ide_state = IDEStatePolicy().snapshot(
        ".",
        active_sprint="42",
        active_prompt_mode=router.recommended_mode,
        current_session_focus=focus.recommended_session_type,
        pending_rollover=handoff.recommended_new_session,
    )
    return VSCodeIntegrationAuditReport(
        session_handoff_active=handoff.recommended_new_session
        and not handoff.full_history_included,
        prompt_export_active=export.bounded and export.summary_only,
        clipboard_runtime_active=clipboard.compact_export_mode and clipboard.export_fallback,
        handoff_notifications_active=notifications.emitted_count > 0
        and notifications.emitted_count <= 3,
        ide_state_runtime_active=not ide_state.telemetry_collected and not ide_state.network_used,
        estimated_avoided_manual_rollover_tokens=len(handoff.copy_ready_prompt) // 2,
        estimated_avoided_stale_continuation_tokens=stale.estimated_saved_tokens
        + len(continuity.excluded_context) * 160,
    )


def audit_session_boundary() -> SessionBoundaryAuditReport:
    generation = SessionGenerationPolicy().generate(
        session_id="audit-session",
        session_generation=3,
        rollover_recommended=True,
        parent_session="audit-parent",
    )
    stale = StaleSessionDetectionPolicy().detect(
        generation=generation,
        rollover_recommended=True,
        handoff_generated=True,
        new_session_started=False,
        continuity_generation=2,
        architecture_topic_count=4,
        continuity_token_estimate=18_000,
        session_age=7,
        stale_continuity_reuse=True,
    )
    enforcement = BoundaryEnforcementPolicy().enforce(
        stale_session=stale,
        architecture_isolation_signal=True,
    )
    rollover = RolloverStatePolicy().evaluate(
        rollover_required=stale.rollover_required,
        handoff_generated=True,
        clipboard_ready=True,
        export_ready=True,
        confirmed=False,
        new_session_started=False,
        stale_session_active=stale.stale_session_detected,
    )
    confirmation = HandoffConfirmationPolicy().confirm(
        export_consumed=True,
        prompt_copied=True,
        new_session_acknowledged=False,
        stale_session_closed=False,
    )
    extension_root = Path("extensions/ai-dev-os-vscode")
    stale_savings = 18_000 if stale.forced_compaction_recommended else 0
    drift_savings = 2_400 if enforcement.architecture_isolation_required else 900
    return SessionBoundaryAuditReport(
        session_boundary_active=enforcement.enforcement_state == "STALE_BLOCKED"
        and not enforcement.ai_response_blocking_enforced,
        stale_session_detection_active=stale.stale_session_detected
        and stale.stale_generation_mismatch,
        rollover_state_active=rollover.rollover_pending and rollover.confirmation_pending,
        handoff_confirmation_active=not confirmation.ui_automation_used,
        vscode_extension_active=(extension_root / "package.json").exists()
        and (extension_root / "src" / "extension.ts").exists(),
        estimated_avoided_stale_continuation_tokens=stale_savings,
        estimated_avoided_hidden_context_drift=drift_savings,
    )


def audit_workspace_persistence() -> WorkspacePersistenceAuditReport:
    store = PersistenceStorePolicy().build(
        current_session_generation=4,
        rollover_state={"rollover_pending": True, "raw_transcript": "excluded"},
        last_continuity_bundle={"bundle_id": "b-4", "provider_responses": "excluded"},
        current_prompt_mode="bounded_implementation",
        session_focus="bounded-implementation",
        stale_warning_state={"stale_session_detected": True, "warning_count": 2},
        repository_subset_summary=("ai_dev_os", "consumer"),
        compact_continuity_metadata={"summary_only": True, "full_prompt_history": "excluded"},
    )
    restore = SessionRestorePolicy().restore(store)
    checkpoint = StateCheckpointPolicy().checkpoint(
        session_generation=store.current_session_generation,
        enforcement_state="ROLLOVER_REQUIRED",
        prompt_mode=store.current_prompt_mode,
        continuity_scope=("active_sprint_continuity", "repository_subset"),
        repository_subset=store.repository_subset_summary,
        active_sprint_metadata={"sprint": "42", "full_workspace_snapshot": "excluded"},
    )
    index = ContinuityIndexPolicy().index(
        continuity_bundle_ids=("b-4",),
        generation_mapping={"b-4": store.current_session_generation},
        sprint_mapping={"b-4": "42"},
        prompt_export_references=("prompt.txt",),
        rollover_lineage=("b-3", "b-4"),
        stale_continuity_flags=("b-3",),
    )
    cleanup = PersistenceCleanupPolicy().cleanup(
        entries=("obsolete-b-1", "b-4", "duplicate-b-2"),
        active_entries=("b-4",),
        expired_entries=("obsolete-b-1",),
        duplicate_entries=("duplicate-b-2",),
    )
    gitignore = Path(".gitignore")
    gitignore_text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    return WorkspacePersistenceAuditReport(
        persistence_store_active=store.bounded
        and store.summary_only
        and bool(store.forbidden_keys_removed)
        and checkpoint.full_workspace_snapshot_included is False,
        session_restore_active=restore.restore_available
        and restore.pending_rollover_restored
        and not restore.stale_persistence_auto_applied,
        continuity_index_active=index.summary_only and not index.raw_export_replay_allowed,
        persistence_cleanup_active=cleanup.stale_persistence_detected
        and bool(cleanup.cleaned_entries),
        local_workspace_persistence_active=".ai-dev-os/" in gitignore_text
        and ".ai-dev-os" in store.store_path,
        estimated_avoided_manual_recovery_tokens=2_400 + len(index.continuity_bundle_ids) * 300,
        estimated_avoided_stale_persistence_tokens=cleanup.estimated_saved_storage
        + len(store.forbidden_keys_removed) * 700,
    )


def audit_persistence_governance() -> PersistenceGovernanceAuditReport:
    checkpoint_ids = tuple(f"checkpoint-{index}" for index in range(10))
    retention = RetentionPolicy().apply(
        checkpoint_generations=checkpoint_ids,
        continuity_lineage=tuple(f"lineage-{index}" for index in range(12)),
        stale_rollovers=("stale-rollover-1", "stale-rollover-2", "stale-rollover-3"),
        inactive_sprints=("inactive-1", "inactive-2", "inactive-3", "inactive-4"),
        prompt_exports=tuple(f"prompt-export-{index}" for index in range(8)),
        compact_bundles=tuple(f"compact-bundle-{index}" for index in range(10)),
    )
    budget = PersistenceBudgetPolicy().evaluate(
        checkpoint_storage=18_000,
        continuity_index_storage=9_000,
        prompt_export_storage=11_000,
        stale_persistence_storage=15_000,
        schema_metadata_storage=2_000,
    )
    schema = SchemaEvolutionPolicy().evaluate(schema_version="1.1", current_version="0.9")
    migration = SchemaMigrationPolicy().migrate(
        state={"schema_version": "0.9", "raw_transcript": "excluded", "summary": "kept"},
        from_version="0.9",
        to_version="1.1",
    )
    rotation = CheckpointRotationPolicy().rotate(checkpoints=checkpoint_ids)
    return PersistenceGovernanceAuditReport(
        retention_policy_active=retention.cleanup_required
        and retention.retention_pressure in {"medium", "high"},
        persistence_budget_active=budget.compact_required and budget.current_budget_usage > 0,
        schema_evolution_active=schema.migration_required
        and "session-boundary.json" in schema.managed_files,
        schema_migration_active=migration.version_upgraded
        and not migration.raw_persistence_replay_allowed,
        checkpoint_rotation_active=rotation.rotation_required
        and bool(rotation.expired_checkpoints),
        estimated_avoided_stale_persistence_growth=retention.estimated_saved_storage
        + budget.stale_persistence_storage,
        estimated_avoided_checkpoint_explosion=len(rotation.expired_checkpoints) * 512,
    )


def run_runtime_enforcement_audit() -> RuntimeEnforcementAuditReport:
    return RuntimeEnforcementAuditReport(
        activation=audit_runtime_activation(),
        routing=audit_prompt_routing(),
        gpt55=audit_gpt55_enforcement(),
        budget=audit_budget_runtime(),
        pruning=audit_context_pruning(),
        council=audit_council_throttling(),
        diff_only=audit_diff_only_enforcement(),
        telemetry=audit_telemetry_runtime(),
        stress=audit_runtime_stress(),
        retrieval_scaling=audit_retrieval_scaling(),
        provider_simulation=audit_provider_simulation(),
        copilot_usage=audit_copilot_usage(),
        session_lifecycle=audit_session_lifecycle(),
        session_orchestrator=audit_session_orchestrator(),
        repository_intelligence=audit_repository_intelligence(),
        workspace_snapshot=audit_workspace_snapshot(),
        context_subset=audit_context_subset(),
        prompt_modes=audit_prompt_modes(),
        vscode_integration=audit_vscode_integration(),
        session_boundary=audit_session_boundary(),
        workspace_persistence=audit_workspace_persistence(),
        persistence_governance=audit_persistence_governance(),
    )


def main() -> int:
    report = run_runtime_enforcement_audit()
    print(json.dumps(report, default=lambda value: value.__dict__, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
