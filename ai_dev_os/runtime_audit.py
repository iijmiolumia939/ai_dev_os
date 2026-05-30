from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.adaptive_provider_routing import AdaptiveProviderRoutingRuntime
from ai_dev_os.cognitive_memory_pressure import CognitiveMemoryPressureRuntime
from ai_dev_os.cognitive_state import CognitiveStateRuntime
from ai_dev_os.consumer_rollout import (
    CompatibilityProjectionPolicy,
    ConsumerRolloutAuditPolicy,
    GovernanceReadinessPolicy,
    MigrationFrictionPolicy,
    RollbackRehearsalPolicy,
)
from ai_dev_os.context_subset.continuity_scope import ContinuityScopePolicy
from ai_dev_os.context_subset.repository_subset import RepositorySubsetPolicy
from ai_dev_os.context_subset.session_focus import SessionFocusPolicy
from ai_dev_os.context_subset.stale_topic_eviction import StaleTopicEvictionPolicy
from ai_dev_os.context_subset.topic_isolation import TopicIsolationPolicy
from ai_dev_os.continuous_runtime_audit import ContinuousRuntimeAuditRuntime
from ai_dev_os.copilot_usage.agent_mode_budget import AgentLoopState, AgentModeBudgetGuard
from ai_dev_os.copilot_usage.atomic_prompting import AtomicPromptPolicy
from ai_dev_os.copilot_usage.context_diet import ContextDietPolicy, ContextItem
from ai_dev_os.copilot_usage.inline_first import InlineFirstPolicy
from ai_dev_os.copilot_usage.session_policy import SessionCostPolicy, SessionState
from ai_dev_os.copilot_usage.skill_compaction import SkillCompactionPolicy, SkillInstruction
from ai_dev_os.dev_execution import DevelopmentExecutionRuntime
from ai_dev_os.dev_loop import SprintDevLoopRuntime
from ai_dev_os.dev_policy import DevelopmentPolicyRuntime
from ai_dev_os.dev_strategy import DevelopmentStrategyRuntime
from ai_dev_os.execution_continuation import ExecutionContinuationRuntime
from ai_dev_os.execution_coordination import ExecutionCoordinationRuntime
from ai_dev_os.execution_intent import ExecutionIntentRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.execution_quality import ExecutionQualityRuntime
from ai_dev_os.execution_recovery import ExecutionRecoveryRuntime
from ai_dev_os.execution_saturation import ExecutionSaturationRuntime
from ai_dev_os.execution_session import ExecutionSessionRuntime
from ai_dev_os.execution_stability import ExecutionStabilityRuntime
from ai_dev_os.failure_injection import FailureInjectionRuntime
from ai_dev_os.governance_core import GovernanceCorePolicy
from ai_dev_os.governance_health.governance_dashboard import GovernanceDashboardPolicy
from ai_dev_os.governance_health.health_score import GovernanceHealthPolicy
from ai_dev_os.governance_health.pressure_aggregation import GovernancePressurePolicy
from ai_dev_os.governance_health.risk_aggregation import GovernanceRiskPolicy
from ai_dev_os.governance_health.stability_assessment import GovernanceStabilityPolicy
from ai_dev_os.governance_trends.dashboard_delta import GovernanceDashboardDeltaPolicy
from ai_dev_os.governance_trends.drift_detection import GovernanceDriftPolicy
from ai_dev_os.governance_trends.regression_detection import GovernanceRegressionPolicy
from ai_dev_os.governance_trends.stability_trends import GovernanceStabilityTrendPolicy
from ai_dev_os.governance_trends.trend_window import (
    GovernanceTrendSnapshot,
    GovernanceTrendWindowPolicy,
)
from ai_dev_os.incremental_context import IncrementalContextRuntime
from ai_dev_os.intentional_planning import IntentionalPlanningRuntime
from ai_dev_os.main_merge_qualification import MainMergeQualificationRuntime
from ai_dev_os.main_merge_rehearsal import MainMergeRehearsalRuntime
from ai_dev_os.observation_review import ObservationReviewRuntime, RuntimeReadinessFrame
from ai_dev_os.output_compression import (
    CompactCompletionInput,
    CompactCompletionPolicy,
    ReportDensityPolicy,
    SummaryDeduplicationPolicy,
    SummarySection,
    ValidationCompactionPolicy,
    ValidationResult,
)
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
from ai_dev_os.provider_cost_stabilization import ProviderCostStabilizationRuntime
from ai_dev_os.provider_experimental import ProviderExperimentalRuntime
from ai_dev_os.provider_fatigue import ProviderFatigueRuntime
from ai_dev_os.provider_local import LocalProviderRuntime
from ai_dev_os.provider_routing import ProviderRoutingRuntime
from ai_dev_os.provider_stability import ProviderStabilityRuntime
from ai_dev_os.providers.cost_simulation import simulate_cost
from ai_dev_os.providers.fallback_simulation import simulate_fallback_chain
from ai_dev_os.providers.mock_provider import simulate_provider_request
from ai_dev_os.providers.provider_contracts import ProviderRequest
from ai_dev_os.providers.provider_telemetry import aggregate_provider_telemetry
from ai_dev_os.reasoning_routing import (
    CostBudgetPolicy,
    EscalationPolicy,
    EscalationPolicyInput,
    QualityFloorPolicy,
    ReasoningTask,
    ReasoningTierPolicy,
    ReasoningUsageSample,
    SprintReasoningRouter,
    SprintReasoningTask,
    TaskComplexityInput,
    TaskComplexityPolicy,
)
from ai_dev_os.reasoning_scope import ReasoningScopeRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.release_readiness import (
    ConsumerRolloutPolicy,
    ExtensionReadinessPolicy,
    GovernanceFreezeStatusPolicy,
)
from ai_dev_os.repository_intelligence.ci_context import CIContextPolicy
from ai_dev_os.repository_intelligence.git_collector import GitCollector
from ai_dev_os.repository_intelligence.runtime_discovery import RuntimeDiscoveryPolicy
from ai_dev_os.repository_intelligence.sprint_metadata import SprintMetadataPolicy
from ai_dev_os.repository_intelligence.validation_collector import ValidationCollectorPolicy
from ai_dev_os.retrieval.memory_tree import MemoryTreeNode
from ai_dev_os.retrieval.retrieval_scaling import RetrievalScalingFrame, scale_retrieval
from ai_dev_os.retrieval_budget import RetrievalBudgetRuntime, RuntimeDependency
from ai_dev_os.runtime_graph import RuntimeGraphPolicy
from ai_dev_os.runtime_hardening import RuntimeHardeningRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_orchestrator import RuntimeOrchestrator
from ai_dev_os.runtime_policy import RuntimePolicyEngine
from ai_dev_os.runtime_simplification import RuntimeSimplificationPolicy
from ai_dev_os.session_bootstrap.draft_injection import DraftInjectionPolicy
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
from ai_dev_os.soak_stability import SoakStabilityRuntime
from ai_dev_os.sprint_continuation import SprintContinuationRuntime
from ai_dev_os.sprint_loop import SprintLoopRuntime
from ai_dev_os.sprint_memory import SprintMemoryRuntime
from ai_dev_os.streaming_cognition import StreamingCognitionRuntime
from ai_dev_os.subagent_execution import SubagentExecutionRuntime
from ai_dev_os.verified_execution import VerifiedExecutionRuntime
from ai_dev_os.vscode_integration.clipboard_runtime import ClipboardRuntimePolicy
from ai_dev_os.vscode_integration.handoff_notifications import HandoffNotificationPolicy
from ai_dev_os.vscode_integration.ide_state import IDEStatePolicy
from ai_dev_os.vscode_integration.prompt_export import PromptExportPolicy
from ai_dev_os.vscode_integration.session_handoff import SessionHandoffPolicy
from ai_dev_os.vscode_presence import (
    build_heartbeat_frame,
    build_presence_frame,
    detect_extension_version,
    detect_stale_extension,
    project_governance_status,
)
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
    incremental_context_active: bool
    raw_transcript_persistence_forbidden: bool


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
class GovernanceHealthAuditReport:
    governance_health_active: bool
    governance_pressure_active: bool
    governance_risk_active: bool
    governance_dashboard_active: bool
    governance_stability_active: bool
    estimated_avoided_governance_drift: int
    estimated_avoided_stale_governance_accumulation: int
    estimated_avoided_hidden_context_pressure: int
    incremental_context_active: bool
    replay_pressure: str
    reasoning_scope_active: bool
    premium_pressure: str


@dataclass(frozen=True)
class GovernanceTrendsAuditReport:
    governance_trend_window_active: bool
    governance_drift_detection_active: bool
    governance_regression_active: bool
    governance_stability_trends_active: bool
    dashboard_delta_active: bool
    estimated_avoided_governance_regression: int
    estimated_avoided_hidden_trend_accumulation: int
    estimated_avoided_governance_oscillation: int
    incremental_context_active: bool
    unchanged_trend_replay_suppressed: bool
    reasoning_scope_active: bool
    unnecessary_escalation_suppressed: bool


@dataclass(frozen=True)
class RuntimeGraphAuditReport:
    runtime_graph_active: bool
    runtime_discovery_active: bool
    dependency_graph_active: bool
    contract_surface_active: bool
    runtime_clustering_active: bool
    architecture_pressure_active: bool
    estimated_avoided_architecture_cognition_tokens: int
    estimated_avoided_runtime_explosion_drift: int
    bounded_dependency_graph: bool
    summary_only_dependency_metadata: bool
    local_only_architecture_cognition: bool
    hidden_telemetry_used: bool
    incremental_context_active: bool
    repo_wide_replay_forbidden: bool
    reasoning_scope_active: bool
    automatic_architecture_escalation_forbidden: bool


@dataclass(frozen=True)
class RuntimeSimplificationAuditReport:
    runtime_overlap_active: bool
    contract_overlap_active: bool
    runtime_merge_candidates_active: bool
    governance_duplication_active: bool
    simplification_recommendations_active: bool
    estimated_avoided_runtime_fragmentation: int
    estimated_avoided_governance_duplication: int
    estimated_avoided_contract_explosion: int
    bounded_simplification_analysis: bool
    human_confirmed_simplification: bool
    autonomous_mutation_used: bool
    incremental_context_active: bool
    repo_wide_replay_forbidden: bool
    reasoning_scope_active: bool
    automatic_architecture_escalation_forbidden: bool


@dataclass(frozen=True)
class GovernanceCoreAuditReport:
    governance_core_active: bool
    pressure_primitives_active: bool
    stale_detection_primitives_active: bool
    bounded_retention_active: bool
    continuity_primitives_active: bool
    compact_export_primitives_active: bool
    estimated_avoided_governance_duplication: int
    estimated_avoided_runtime_fragmentation: int
    estimated_avoided_bounded_retention_drift: int
    bounded_governance_reuse: bool
    human_confirmed_migration: bool
    automatic_rewrite_used: bool


@dataclass(frozen=True)
class ReleaseReadinessAuditReport:
    release_readiness_active: bool
    consumer_rollout_active: bool
    extension_release_ready: bool
    governance_freeze_active: bool
    bounded_release_confirmed: bool
    estimated_avoided_rollout_confusion: int
    estimated_avoided_stale_migration_context: int
    rollback_safe_release_prep: bool
    local_first_governance: bool
    no_hidden_automation: bool


@dataclass(frozen=True)
class VSCodePresenceAuditReport:
    governance_presence_active: bool
    version_detection_active: bool
    runtime_heartbeat_active: bool
    status_projection_active: bool
    stale_extension_detection_active: bool
    estimated_avoided_invisible_governance_drift: int
    estimated_avoided_stale_extension_confusion: int
    compact_status: str
    stale_extension_detected: bool
    bounded_visibility: bool


@dataclass(frozen=True)
class DraftInjectionAuditReport:
    provider_prefill_active: bool
    copilot_prefill_active: bool
    vscode_chat_prefill_active: bool
    prefill_observability_active: bool
    enter_only_confidence: str
    draft_injection_active: bool
    chat_prefill_active: bool
    chat_launch_active: bool
    chat_target_detection_active: bool
    enter_only_rollover_active: bool
    clipboard_fallback_active: bool
    no_auto_send: bool
    no_hidden_continuation: bool
    no_background_message_dispatch: bool
    no_silent_prompt_mutation: bool
    estimated_avoided_handoff_friction: int
    estimated_avoided_stale_continuity_replay: int
    status_bar_states: tuple[str, ...]


@dataclass(frozen=True)
class ConsumerRolloutAuditReport:
    consumer_rollout_active: bool
    rollout_audit_active: bool
    migration_friction_active: bool
    compatibility_projection_active: bool
    governance_readiness_active: bool
    rollback_rehearsal_active: bool
    estimated_avoided_rollout_failure: int
    estimated_avoided_stale_migration_state: int
    rollout_ready: bool
    migration_friction: str
    governance_readiness: str
    rollback_ready: bool
    bounded_rollout_confirmed: bool
    consumer_name: str


@dataclass(frozen=True)
class ReasoningRoutingAuditReport:
    reasoning_routing_active: bool
    task_complexity_active: bool
    escalation_policy_active: bool
    cost_budget_policy_active: bool
    quality_floor_active: bool
    sprint_reasoning_map_active: bool
    tier_distribution: dict[str, int]
    budget_pressure: str
    escalation_reason: str
    downgrade_recommendation: bool
    compaction_recommendation: bool
    estimated_avoided_premium_burn: int
    estimated_avoided_unnecessary_escalation: int
    human_visible_routing: bool
    deterministic_reasoning_policy: bool
    rollback_safe_routing: bool
    provider_neutral_contracts: bool
    hidden_escalation_used: bool
    reasoning_scope_active: bool
    local_patch_recommendation_active: bool


@dataclass(frozen=True)
class OutputCompressionAuditReport:
    output_compression_active: bool
    summary_deduplication_active: bool
    validation_compaction_active: bool
    report_density_active: bool
    compact_completion_active: bool
    verbosity_pressure: str
    compact_summary_lines: int
    expandable_reporting: bool
    human_readable: bool
    rollback_safe: bool
    deterministic_compact_mode: bool
    estimated_avoided_completion_tokens: int
    estimated_avoided_repeated_summaries: int
    hidden_reporting_used: bool
    validation_skipped: bool


@dataclass(frozen=True)
class RetrievalBudgetAuditReport:
    retrieval_budget_active: bool
    retrieval_scope_active: bool
    retrieval_radius_active: bool
    retrieval_pressure_active: bool
    retrieval_compaction_active: bool
    bounded_retrieval_neighborhood: tuple[str, ...]
    repo_wide_retrieval_forbidden: bool
    retrieval_pressure: str
    compact_retrieval_recommendation: bool
    estimated_avoided_hidden_input_tokens: int
    estimated_avoided_repo_wide_reasoning: int
    local_only: bool
    deterministic: bool
    summary_only: bool
    no_ast_replay: bool
    no_dynamic_tracing: bool
    no_hidden_provider_routing: bool
    no_automatic_retrieval_escalation: bool


@dataclass(frozen=True)
class IncrementalContextAuditReport:
    incremental_context_active: bool
    context_delta_active: bool
    delta_retrieval_active: bool
    continuity_delta_active: bool
    audit_delta_active: bool
    cognition_cache_active: bool
    incremental_pressure_active: bool
    incremental_recommendation_active: bool
    estimated_avoided_repeated_input_tokens: int
    estimated_avoided_duplicate_runtime_cognition: int
    replay_pressure: str
    compact_changed_neighborhood: tuple[str, ...]
    unchanged_context_excluded: tuple[str, ...]
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_retention: bool
    no_raw_transcript_persistence: bool
    no_hidden_provider_memory: bool
    no_ast_replay: bool
    no_repo_wide_replay: bool
    no_dynamic_tracing: bool
    no_automatic_context_expansion: bool


@dataclass(frozen=True)
class ReasoningScopeAuditReport:
    reasoning_scope_active: bool
    reasoning_depth_active: bool
    architecture_reasoning_guard_active: bool
    local_patch_mode_active: bool
    reasoning_pressure_active: bool
    reasoning_compaction_active: bool
    reasoning_recommendation_active: bool
    estimated_avoided_premium_reasoning_burn: int
    estimated_avoided_unnecessary_architecture_reasoning: int
    pressure_level: str
    depth_cap: int
    task_local_cognition_scope: tuple[str, ...]
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_cognition_only: bool
    no_hidden_chain_of_thought_persistence: bool
    no_ast_replay: bool
    no_hidden_provider_routing: bool
    no_automatic_architecture_escalation: bool
    no_automatic_roadmap_synthesis: bool


@dataclass(frozen=True)
class ProviderRoutingAuditReport:
    provider_routing_active: bool
    provider_capability_matrix_active: bool
    provider_budget_policy_active: bool
    provider_pressure_active: bool
    provider_downgrade_active: bool
    provider_observability_active: bool
    estimated_avoided_premium_provider_burn: int
    estimated_avoided_unnecessary_high_tier_usage: int
    recommended_provider_class: str
    provider_burn_pressure: str
    premium_vs_cheap_ratio: float
    no_real_billing_api: bool
    no_hidden_provider_switching: bool
    no_automatic_provider_execution: bool
    no_provider_upload: bool
    no_hidden_escalation: bool
    provider_neutral: bool
    local_only: bool
    deterministic: bool
    summary_only: bool


@dataclass(frozen=True)
class LocalProviderAuditReport:
    local_provider_active: bool
    ollama_provider_active: bool
    local_provider_health: str
    local_provider_budget: str
    local_provider_fallback: str
    estimated_avoided_premium_tokens: int
    estimated_local_execution_ratio: float
    routing_distribution: dict[str, int]
    primary_coding_model: str
    governance_compression_model: str
    fallback_coding_model: str
    primary_model_gpu_operational: bool
    fallback_model_operational: bool
    qwen_coder_14b_coding: bool
    qwen_coder_14b_summaries: bool
    qwen_coder_14b_architecture: bool
    qwen_coder_14b_governance: bool
    gemma3_12b_compression: bool
    gemma3_12b_governance_summaries: bool
    gemma3_12b_coding: str
    low_execution_provider: str
    governance_compression_provider: str
    high_provider: str
    compact_prompts_required: bool
    local_patch_only: bool
    adjacent_runtime_retrieval_only: bool
    bounded_context_windows: bool
    no_repo_wide_local_reasoning: bool
    no_giant_continuity_replay: bool
    no_recursive_local_execution: bool
    no_hidden_autonomous_loops: bool
    no_unrestricted_repository_mutation: bool
    human_confirmed_execution_authority: bool


@dataclass(frozen=True)
class SubagentExecutionAuditReport:
    subagent_execution_active: bool
    subagent_routing_active: bool
    subagent_payload_active: bool
    subagent_validation_active: bool
    subagent_fallback_active: bool
    subagent_governance_active: bool
    subagent_scope_active: bool
    subagent_eviction_active: bool
    estimated_avoided_premium_subagent_tokens: int
    estimated_avoided_recursive_agent_explosion: int
    provider_routing_distribution: dict[str, int]
    local_subagent_routing_result: str
    low_governance_routing_result: str
    medium_routing_result: str
    high_routing_result: str
    fallback_activation_summary: str
    delegated_cognition_pressure: str
    swarm_pressure: str
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


@dataclass(frozen=True)
class DevExecutionAuditReport:
    dev_execution_active: bool
    execution_plan_active: bool
    execution_checkpoint_active: bool
    execution_validation_active: bool
    execution_rollback_active: bool
    execution_pacing_active: bool
    execution_scope_active: bool
    execution_failure_active: bool
    execution_eviction_active: bool
    estimated_avoided_execution_overhead: int
    estimated_avoided_execution_explosion: int
    provider_routing_distribution: dict[str, int]
    execution_pressure: str
    validation_pressure: str
    rollback_pressure: str
    pacing_pressure: str
    scope_pressure: str
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_execution_only: bool
    human_confirmed_execution_only: bool
    no_autonomous_coding_authority: bool
    no_hidden_repository_mutation: bool
    no_recursive_execution_expansion: bool
    no_giant_execution_replay: bool
    no_validation_bypass: bool
    compact_pressure_warnings: tuple[str, ...]


@dataclass(frozen=True)
class DevLoopAuditReport:
    dev_loop_active: bool
    sprint_planning_active: bool
    sprint_lifecycle_active: bool
    sprint_rollover_active: bool
    sprint_bootstrap_active: bool
    sprint_governance_active: bool
    estimated_avoided_manual_orchestration_tokens: int
    estimated_avoided_sprint_explosion: int
    provider_routing_distribution: dict[str, int]
    local_patch_required: bool
    bounded_cognition_only: bool
    human_confirmed_orchestration_only: bool
    no_autonomous_roadmap_expansion: bool
    no_hidden_provider_switching: bool
    no_giant_continuity_replay: bool
    compact_bootstrap_payload: bool
    lifecycle_state: str
    compact_governance_warnings: tuple[str, ...]


@dataclass(frozen=True)
class SprintMemoryAuditReport:
    sprint_memory_active: bool
    sprint_pattern_active: bool
    sprint_outcome_active: bool
    sprint_provider_pattern_active: bool
    sprint_retrieval_pattern_active: bool
    sprint_governance_pattern_active: bool
    sprint_compression_active: bool
    sprint_eviction_active: bool
    estimated_avoided_manual_sprint_analysis: int
    estimated_avoided_repeated_sprint_failures: int
    provider_routing_distribution: dict[str, int]
    memory_pressure: str
    pattern_stable: bool
    memory_eviction_required: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_memory_only: bool
    no_hidden_long_term_cognition: bool
    no_autonomous_roadmap_learning: bool
    no_hidden_provider_switching: bool
    compact_governance_warnings: tuple[str, ...]


@dataclass(frozen=True)
class DevStrategyAuditReport:
    dev_strategy_active: bool
    strategy_priority_active: bool
    cost_reduction_strategy_active: bool
    governance_stability_strategy_active: bool
    provider_efficiency_strategy_active: bool
    sprint_density_strategy_active: bool
    embodiment_focus_strategy_active: bool
    strategy_eviction_active: bool
    estimated_avoided_strategy_overhead: int
    estimated_avoided_roadmap_explosion: int
    provider_routing_distribution: dict[str, int]
    strategy_pressure: str
    cost_pressure: str
    roadmap_pressure: str
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_strategy_only: bool
    human_confirmed_strategy_only: bool
    no_autonomous_roadmap_generation: bool
    no_recursive_future_sprint_synthesis: bool
    no_hidden_provider_switching: bool
    no_giant_strategic_replay: bool
    compact_pressure_warnings: tuple[str, ...]


@dataclass(frozen=True)
class DevPolicyAuditReport:
    dev_policy_active: bool
    architecture_policy_active: bool
    embodiment_realism_policy_active: bool
    provider_escalation_policy_active: bool
    bounded_cognition_policy_active: bool
    anti_explosion_policy_active: bool
    rollout_safety_policy_active: bool
    policy_eviction_active: bool
    estimated_avoided_policy_overhead: int
    estimated_avoided_governance_explosion: int
    provider_routing_distribution: dict[str, int]
    policy_pressure: str
    governance_pressure: str
    escalation_pressure: str
    realism_pressure: str
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_policy_only: bool
    human_confirmed_governance_only: bool
    no_autonomous_enforcement: bool
    no_repository_mutation_authority: bool
    no_hidden_provider_switching: bool
    no_recursive_governance_expansion: bool
    no_giant_policy_replay: bool
    compact_pressure_warnings: tuple[str, ...]


@dataclass(frozen=True)
class ProviderExperimentalAuditReport:
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
    provider_governance_active: bool
    provider_benchmark_summary_active: bool
    provider_benchmark_eviction_active: bool
    openmythos_load_result: str
    openmythos_direct_hf_result: str
    openmythos_weighted_hf_result: str
    openmythos_gguf_conversion_result: str
    openmythos_quantization: str
    openmythos_ollama_model: str
    openmythos_fallback_route: str
    vram_runtime_stability: str
    provider_comparison_summary: str
    governance_adherence_observation: str
    architecture_drift_observation: str
    estimated_reasoning_depth_gain: int
    estimated_governance_instability_risk: int
    estimated_architecture_drift_risk: int
    local_only: bool
    deterministic: bool
    summary_only: bool
    rollback_safe: bool
    no_architecture_authority: bool
    no_governance_authority: bool
    no_anti_explosion_authority: bool
    no_autonomous_execution_authority: bool


@dataclass(frozen=True)
class ProviderStabilityAuditReport:
    provider_stability_active: bool
    long_session_drift_active: bool
    governance_decay_active: bool
    compactness_retention_active: bool
    retrieval_radius_active: bool
    hallucination_pressure_active: bool
    stability_benchmark_active: bool
    provider_stability_comparison: tuple[str, ...]
    governance_adherence_ranking: tuple[str, ...]
    compactness_retention_ranking: tuple[str, ...]
    drift_resistance_ranking: tuple[str, ...]
    local_patch_adherence_ranking: tuple[str, ...]
    repetitive_reliability_ranking: tuple[str, ...]
    retrieval_discipline_ranking: tuple[str, ...]
    estimated_long_session_degradation: dict[str, int]
    estimated_provider_stability_gain: int
    estimated_recursive_drift_risk: str
    openmythos_placeholder_only: bool
    no_real_openmythos_execution: bool
    no_hidden_provider_switching: bool
    local_only: bool
    deterministic: bool
    summary_only: bool


@dataclass(frozen=True)
class AdaptiveProviderRoutingAuditReport:
    adaptive_provider_routing_active: bool
    drift_aware_routing_active: bool
    governance_weighted_routing_active: bool
    long_session_routing_active: bool
    routing_confidence_active: bool
    provider_recommendation_ranking: tuple[str, ...]
    stability_weighted_ranking: tuple[str, ...]
    governance_weighted_ranking: tuple[str, ...]
    routing_confidence_summary: tuple[str, ...]
    drift_aware_routing_result: str
    governance_weighted_routing_result: str
    estimated_avoided_provider_drift: int
    estimated_avoided_recursive_routing: int
    estimated_avoided_premium_burn: int
    human_confirmed_only: bool
    deterministic: bool
    rollback_safe: bool
    no_hidden_provider_switching: bool
    no_recursive_routing_loops: bool
    no_unrestricted_provider_escalation: bool
    automatic_switching_allowed: bool
    governance_runtime_bypassed: bool


@dataclass(frozen=True)
class ProviderFatigueAuditReport:
    provider_fatigue_active: bool
    escalation_fatigue_active: bool
    fallback_oscillation_active: bool
    compactness_decay_active: bool
    long_session_pressure_active: bool
    fatigue_confidence_active: bool
    provider_recovery_active: bool
    provider_fatigue_summary: tuple[str, ...]
    escalation_fatigue_warning: str
    fallback_oscillation_summary: str
    compactness_decay_recommendation: str
    recovery_recommendation: str
    estimated_avoided_provider_exhaustion: int
    estimated_avoided_recursive_fatigue: int
    estimated_avoided_premium_burn: int
    human_confirmed_only: bool
    deterministic: bool
    rollback_safe: bool
    autonomous_provider_replacement: bool
    recursive_reroute_loops_blocked: bool
    governance_runtime_bypassed: bool
    hidden_escalation_switching: bool


@dataclass(frozen=True)
class CognitiveMemoryPressureAuditReport:
    cognitive_memory_pressure_active: bool
    continuity_inflation_active: bool
    retrieval_overload_active: bool
    summary_entropy_active: bool
    context_fragmentation_active: bool
    memory_pressure_summary: str
    continuity_inflation_summary: str
    retrieval_overload_summary: str
    summary_entropy_summary: str
    continuity_recovery_recommendation: str
    estimated_avoided_context_explosion: int
    estimated_avoided_summary_entropy: int
    estimated_avoided_retrieval_overload: int
    human_confirmed_only: bool
    deterministic: bool
    rollback_safe: bool
    autonomous_cognition_erasure: bool
    recursive_continuity_mutation: bool
    governance_runtime_bypassed: bool
    hidden_context_mutation: bool
    retrieval_scope_expansion_allowed: bool
    automatic_context_expansion: bool


@dataclass(frozen=True)
class ExecutionContinuationAuditReport:
    execution_continuation_active: bool
    continuation_budget_active: bool
    continuation_governance_active: bool
    continuation_checkpoint_active: bool
    continuation_termination_active: bool
    continuation_summary: str
    governance_summary: str
    checkpoint_summary: str
    termination_summary: str
    estimated_avoided_execution_stalls: int
    estimated_avoided_recursive_loops: int
    estimated_avoided_agent_explosions: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    local_only: bool
    summary_only: bool
    governance_rules_mutated: bool
    hidden_background_execution_blocked: bool
    recursive_execution_loops_blocked: bool


@dataclass(frozen=True)
class ExecutionSaturationAuditReport:
    execution_saturation_active: bool
    retry_oscillation_active: bool
    tool_congestion_active: bool
    checkpoint_inflation_active: bool
    saturation_termination_active: bool
    estimated_avoided_recursive_execution: int
    estimated_avoided_retry_loops: int
    estimated_avoided_checkpoint_explosion: int


@dataclass(frozen=True)
class ExecutionRecoveryAuditReport:
    execution_recovery_active: bool
    recovery_cooldown_active: bool
    recovery_checkpoint_integrity_active: bool
    recovery_termination_active: bool
    estimated_avoided_recovery_loops: int
    estimated_avoided_checkpoint_corruption: int
    estimated_avoided_recursive_repair: int


@dataclass(frozen=True)
class ExecutionCoordinationAuditReport:
    execution_coordination_active: bool
    coordination_conflict_active: bool
    coordination_priority_active: bool
    coordination_termination_active: bool
    estimated_avoided_runtime_conflicts: int
    estimated_avoided_recursive_coordination: int
    estimated_avoided_runtime_oscillation: int


@dataclass(frozen=True)
class ExecutionIntentAuditReport:
    execution_intent_active: bool
    intent_priority_active: bool
    intent_transition_active: bool
    intent_conflict_active: bool
    estimated_avoided_intent_oscillation: int
    estimated_avoided_recursive_planning: int
    estimated_avoided_execution_instability: int


@dataclass(frozen=True)
class ExecutionSessionAuditReport:
    execution_session_active: bool
    session_lifecycle_active: bool
    session_integrity_active: bool
    session_termination_active: bool
    estimated_avoided_orphaned_sessions: int
    estimated_avoided_recursive_persistence: int
    estimated_avoided_session_fragmentation: int


@dataclass(frozen=True)
class ExecutionStabilityAuditReport:
    execution_stability_active: bool
    stability_drift_active: bool
    stability_oscillation_active: bool
    stability_persistence_active: bool
    estimated_avoided_long_session_drift: int
    estimated_avoided_recursive_stabilization: int
    estimated_avoided_persistence_entropy: int


@dataclass(frozen=True)
class ExecutionQualityAuditReport:
    execution_quality_active: bool
    quality_drift_active: bool
    quality_redundancy_active: bool
    quality_persistence_active: bool
    estimated_avoided_low_value_execution: int
    estimated_avoided_recursive_optimization: int
    estimated_avoided_execution_redundancy: int


@dataclass(frozen=True)
class VerifiedExecutionAuditReport:
    verified_execution_active: bool
    command_runtime_active: bool
    filesystem_runtime_active: bool
    pytest_runtime_active: bool
    git_runtime_active: bool
    evidence_runtime_active: bool
    estimated_avoided_fake_execution: int
    estimated_avoided_hallucinated_pytest: int
    estimated_avoided_synthetic_git_state: int


@dataclass(frozen=True)
class CognitiveStateAuditReport:
    cognitive_state_active: bool
    attention_distribution: tuple[str, ...]
    memory_pressure: str
    decay_status: str


@dataclass(frozen=True)
class IntentionalPlanningAuditReport:
    intentional_planning_active: bool
    active_goal_count: int
    planning_window_pressure: str
    planning_decay_status: str
    planning_interruption_pressure: str
    estimated_avoided_recursive_planning: int
    estimated_avoided_goal_explosion: int
    estimated_avoided_frontier_reasoning: int


@dataclass(frozen=True)
class SprintLoopAuditReport:
    sprint_loop_active: bool
    sprint_validation_score: int
    sprint_regression_score: int
    sprint_commit_readiness_score: int
    sprint_continuation_score: int
    estimated_avoided_manual_orchestration: int
    estimated_avoided_recursive_sprints: int
    estimated_avoided_frontier_supervision: int


@dataclass(frozen=True)
class RuntimeHardeningAuditReport:
    runtime_hardening_active: bool
    retry_storm_score: int
    escalation_oscillation_score: int
    continuation_stability_score: int
    provider_starvation_score: int
    orchestration_deadlock_score: int
    estimated_avoided_retry_storms: int
    estimated_avoided_orchestration_collapse: int
    estimated_avoided_frontier_stabilization: int


@dataclass(frozen=True)
class ContinuousRuntimeAuditReport:
    continuous_runtime_audit_active: bool
    runtime_health_score: int
    retry_pressure_score: int
    provider_fatigue_score: int
    continuation_instability_score: int
    orchestration_pressure_score: int
    estimated_avoided_runtime_blindness: int
    estimated_avoided_orchestration_collapse: int
    estimated_avoided_frontier_observability: int


@dataclass(frozen=True)
class FailureInjectionAuditReport:
    failure_injection_active: bool
    retry_injection_score: int
    provider_injection_score: int
    continuation_injection_score: int
    orchestration_injection_score: int
    recovery_resilience_score: int
    estimated_avoided_runtime_collapse: int
    estimated_avoided_frontier_recovery: int
    estimated_avoided_hidden_instability: int


@dataclass(frozen=True)
class SoakStabilityAuditReport:
    soak_stability_active: bool
    long_session_stability_score: int
    retry_accumulation_score: int
    provider_fatigue_accumulation_score: int
    continuation_entropy_score: int
    orchestration_queue_drift_score: int
    estimated_avoided_slow_degradation: int
    estimated_avoided_runtime_entropy: int
    estimated_avoided_frontier_stabilization: int


@dataclass(frozen=True)
class ProviderCostStabilizationAuditReport:
    provider_cost_stabilization_active: bool
    frontier_dependency_score: int
    retry_cost_score: int
    continuation_reuse_score: int
    orchestration_cost_score: int
    local_first_efficiency_score: int
    estimated_avoided_frontier_escalation: int
    estimated_avoided_cost_drift: int
    estimated_avoided_runtime_overhead: int


@dataclass(frozen=True)
class MainMergeQualificationAuditReport:
    main_merge_qualification_active: bool
    merge_readiness_score: int
    governance_completeness_score: int
    validation_completeness_score: int
    runtime_coherence_score: int
    operational_risk_score: int
    estimated_avoided_merge_regression: int
    estimated_avoided_runtime_instability: int
    estimated_avoided_frontier_dependency: int


@dataclass(frozen=True)
class MainMergeRehearsalAuditReport:
    main_merge_rehearsal_active: bool
    protected_branch_readiness_score: int
    merge_conflict_visibility_score: int
    rollback_survivability_score: int
    post_merge_runtime_score: int
    ci_readiness_score: int
    estimated_avoided_merge_instability: int
    estimated_avoided_post_merge_regression: int
    estimated_avoided_frontier_recovery: int


@dataclass(frozen=True)
class RuntimeOrchestratorAuditReport:
    runtime_orchestrator_active: bool
    orchestration_schedule_score: int
    validation_schedule_score: int
    retry_schedule_score: int
    continuation_schedule_score: int
    estimated_avoided_manual_scheduling: int
    estimated_avoided_recursive_orchestration: int
    estimated_avoided_frontier_next_step_reasoning: int


@dataclass(frozen=True)
class RuntimePolicyAuditReport:
    runtime_policy_active: bool
    execution_policy_score: int
    retry_policy_score: int
    provider_policy_score: int
    continuation_policy_score: int
    reflective_policy_score: int
    estimated_avoided_recursive_governance: int
    estimated_avoided_frontier_escalation: int
    estimated_avoided_policy_fragmentation: int


@dataclass(frozen=True)
class ExecutionMemoryAuditReport:
    execution_memory_active: bool
    execution_pattern_score: int
    retry_pattern_score: int
    execution_reuse_score: int
    provider_execution_memory_score: int
    estimated_avoided_retry_repetition: int
    estimated_avoided_frontier_replanning: int
    estimated_avoided_execution_instability: int


@dataclass(frozen=True)
class AdaptiveProviderAuditReport:
    adaptive_provider_active: bool
    provider_capability_score: int
    provider_fatigue_score: int
    provider_cost_pressure: str
    provider_confidence_score: int
    estimated_avoided_frontier_provider_usage: int
    estimated_avoided_recursive_escalation: int
    estimated_avoided_provider_instability: int


@dataclass(frozen=True)
class ReflectiveEvaluationAuditReport:
    reflective_evaluation_active: bool
    execution_quality_score: int
    cognitive_coherence_score: int
    continuation_validity_score: int
    planning_integrity_score: int
    estimated_avoided_recursive_reflection: int
    estimated_avoided_self_optimization: int
    estimated_avoided_frontier_evaluation: int


@dataclass(frozen=True)
class RuntimeMediationAuditReport:
    runtime_mediation_active: bool
    execution_sequencer_active: bool
    retry_governance_active: bool
    cooldown_governance_active: bool
    execution_arbitration_active: bool
    estimated_avoided_recursive_execution: int
    estimated_avoided_retry_amplification: int
    estimated_avoided_execution_saturation: int


@dataclass(frozen=True)
class StreamingCognitionAuditReport:
    streaming_cognition_active: bool
    streaming_latency_score: int
    interruption_recovery_score: int
    provider_streaming_score: int
    continuation_streaming_score: int
    bounded_cognition_score: int
    estimated_avoided_streaming_instability: int
    estimated_avoided_provider_interruptions: int
    estimated_avoided_frontier_streaming: int


@dataclass(frozen=True)
class SprintContinuationAuditReport:
    sprint_continuation_active: bool
    continuation_selection_score: int
    backlog_continuation_score: int
    dependency_continuation_score: int
    regression_continuation_score: int
    operational_carryover_score: int
    estimated_avoided_continuation_drift: int
    estimated_avoided_recursive_sprinting: int
    estimated_avoided_frontier_planning: int


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
    governance_health: GovernanceHealthAuditReport
    governance_trends: GovernanceTrendsAuditReport
    runtime_graph: RuntimeGraphAuditReport
    runtime_simplification: RuntimeSimplificationAuditReport
    governance_core: GovernanceCoreAuditReport
    release_readiness: ReleaseReadinessAuditReport
    vscode_presence: VSCodePresenceAuditReport
    draft_injection: DraftInjectionAuditReport
    consumer_rollout: ConsumerRolloutAuditReport
    reasoning_routing: ReasoningRoutingAuditReport
    output_compression: OutputCompressionAuditReport
    retrieval_budget: RetrievalBudgetAuditReport
    incremental_context: IncrementalContextAuditReport
    reasoning_scope: ReasoningScopeAuditReport
    local_provider: LocalProviderAuditReport
    subagent_execution: SubagentExecutionAuditReport
    provider_routing: ProviderRoutingAuditReport
    dev_execution: DevExecutionAuditReport
    dev_loop: DevLoopAuditReport
    sprint_memory: SprintMemoryAuditReport
    dev_strategy: DevStrategyAuditReport
    dev_policy: DevPolicyAuditReport
    provider_experimental: ProviderExperimentalAuditReport
    provider_stability: ProviderStabilityAuditReport
    adaptive_provider_routing: AdaptiveProviderRoutingAuditReport
    provider_fatigue: ProviderFatigueAuditReport
    cognitive_memory_pressure: CognitiveMemoryPressureAuditReport
    execution_continuation: ExecutionContinuationAuditReport
    execution_saturation: ExecutionSaturationAuditReport
    execution_recovery: ExecutionRecoveryAuditReport
    execution_coordination: ExecutionCoordinationAuditReport
    execution_intent: ExecutionIntentAuditReport
    execution_session: ExecutionSessionAuditReport
    execution_stability: ExecutionStabilityAuditReport
    execution_quality: ExecutionQualityAuditReport
    verified_execution: VerifiedExecutionAuditReport
    runtime_mediation: RuntimeMediationAuditReport
    cognitive_state: CognitiveStateAuditReport
    intentional_planning: IntentionalPlanningAuditReport
    reflective_evaluation: ReflectiveEvaluationAuditReport
    streaming_cognition: StreamingCognitionAuditReport
    adaptive_provider: AdaptiveProviderAuditReport
    execution_memory: ExecutionMemoryAuditReport
    runtime_policy: RuntimePolicyAuditReport
    sprint_loop: SprintLoopAuditReport
    runtime_orchestrator: RuntimeOrchestratorAuditReport
    runtime_hardening: RuntimeHardeningAuditReport
    continuous_runtime_audit: ContinuousRuntimeAuditReport
    failure_injection: FailureInjectionAuditReport
    soak_stability: SoakStabilityAuditReport
    provider_cost_stabilization: ProviderCostStabilizationAuditReport
    observation_review: RuntimeReadinessFrame
    main_merge_qualification: MainMergeQualificationAuditReport
    main_merge_rehearsal: MainMergeRehearsalAuditReport
    sprint_continuation: SprintContinuationAuditReport


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
        incremental_context_active=True,
        raw_transcript_persistence_forbidden="raw_transcript" in store.forbidden_keys_removed,
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


def audit_governance_health() -> GovernanceHealthAuditReport:
    pressure = GovernancePressurePolicy().aggregate(
        retrieval_pressure="medium",
        persistence_pressure="high",
        session_pressure="high",
        architecture_pressure="medium",
        provider_pressure="low",
        continuity_pressure="high",
        checkpoint_pressure="high",
        stale_context_pressure="high",
    )
    risk = GovernanceRiskPolicy().aggregate(
        stale_continuity_risk=True,
        hidden_context_drift=True,
        architecture_contamination=False,
        retrieval_explosion=False,
        persistence_explosion=True,
        checkpoint_explosion=True,
        provider_lock_in_risk=False,
        governance_runtime_drift=True,
        prompt_mode_drift=False,
    )
    health = GovernanceHealthPolicy().score(
        session_lifecycle="high",
        stale_context_pressure="high",
        persistence_pressure="high",
        retrieval_scaling_pressure="medium",
        provider_simulation_pressure="low",
        architecture_isolation_pressure="medium",
        schema_migration_pressure="medium",
        checkpoint_rotation_pressure="high",
        workspace_contamination_risk=False,
    )
    dashboard = GovernanceDashboardPolicy().build(
        health=health,
        pressure=pressure,
        risk=risk,
        stale_session_active=True,
        persistence_budget_state="high",
        checkpoint_pressure="high",
        architecture_isolation_required=False,
        workspace_dirty=False,
        rollout_stability="stable rollout",
    )
    stability = GovernanceStabilityPolicy().assess(
        bounded_governance_maintained=True,
        uncontrolled_expansion_detected=False,
        stale_governance_accumulation=True,
        governance_oscillation=False,
        repeated_rollover_instability=True,
        persistence_instability=True,
        retrieval_instability=False,
    )
    return GovernanceHealthAuditReport(
        governance_health_active=health.governance_health_state
        in {
            "HEALTHY",
            "STABLE_WARNING",
            "HIGH_PRESSURE",
            "CRITICAL_GOVERNANCE",
        },
        governance_pressure_active=pressure.aggregate_pressure
        in {
            "low",
            "medium",
            "high",
            "critical",
        },
        governance_risk_active=bool(risk.active_risks),
        governance_dashboard_active=dashboard.summary_only
        and not dashboard.raw_runtime_replay_allowed,
        governance_stability_active=stability.bounded_governance_maintained,
        estimated_avoided_governance_drift=len(risk.active_risks) * 700,
        estimated_avoided_stale_governance_accumulation=len(dashboard.active_warnings) * 500,
        estimated_avoided_hidden_context_pressure=health.pressure_average * 20,
        incremental_context_active=True,
        replay_pressure="HIGH",
        reasoning_scope_active=True,
        premium_pressure="MEDIUM",
    )


def audit_governance_trends() -> GovernanceTrendsAuditReport:
    snapshots = (
        GovernanceTrendSnapshot("g-1", "low", "low", "HEALTHY", "stable", 90),
        GovernanceTrendSnapshot("g-2", "medium", "medium", "STABLE_WARNING", "warning", 72),
        GovernanceTrendSnapshot("g-3", "high", "medium", "HIGH_PRESSURE", "unstable", 55),
        GovernanceTrendSnapshot(
            "g-4",
            "medium",
            "high",
            "STABLE_WARNING",
            "warning",
            68,
            checkpoint_pressure="high",
            persistence_pressure="high",
        ),
        GovernanceTrendSnapshot(
            "g-5",
            "high",
            "high",
            "HIGH_PRESSURE",
            "unstable",
            50,
            checkpoint_pressure="high",
            persistence_pressure="high",
        ),
        GovernanceTrendSnapshot(
            "g-6",
            "critical",
            "high",
            "CRITICAL_GOVERNANCE",
            "degraded",
            30,
            checkpoint_pressure="high",
            persistence_pressure="critical",
            architecture_isolation="recommended",
        ),
    )
    window = GovernanceTrendWindowPolicy().apply(snapshots, max_window_size=5)
    drift = GovernanceDriftPolicy().detect(window)
    regression = GovernanceRegressionPolicy().detect(window)
    stability = GovernanceStabilityTrendPolicy().evaluate(window)
    delta = GovernanceDashboardDeltaPolicy().summarize(
        previous=window.snapshots[-2],
        current=window.snapshots[-1],
    )
    return GovernanceTrendsAuditReport(
        governance_trend_window_active=window.bounded_window_maintained
        and not window.full_historical_replay_allowed,
        governance_drift_detection_active=drift.drift_detected,
        governance_regression_active=regression.regression_detected,
        governance_stability_trends_active=stability.stability_direction
        in {"improving", "stable", "degrading", "oscillating"},
        dashboard_delta_active=delta.delta_only_summary and not delta.raw_runtime_replay_allowed,
        estimated_avoided_governance_regression=regression.repeated_instability_count * 600,
        estimated_avoided_hidden_trend_accumulation=len(window.evicted_snapshots) * 450,
        estimated_avoided_governance_oscillation=800 if regression.oscillation_detected else 200,
        incremental_context_active=True,
        unchanged_trend_replay_suppressed=window.bounded_window_maintained,
        reasoning_scope_active=True,
        unnecessary_escalation_suppressed=True,
    )


def audit_runtime_graph() -> RuntimeGraphAuditReport:
    frame = RuntimeGraphPolicy().evaluate(".", max_edges=24)
    discovery = frame.discovery
    graph = frame.dependency_graph
    contract = frame.contract_surface
    clusters = frame.runtime_clusters
    pressure = frame.architecture_pressure
    avoided_cognition = (
        discovery.runtime_count * 140
        + graph.edge_count * 90
        + min(contract.contract_surface_size, 80) * 24
    )
    avoided_drift = (
        len(graph.cross_boundary_edges) * 160
        + len(clusters.oversized_clusters) * 500
        + (700 if pressure.simplification_recommended else 250)
    )
    return RuntimeGraphAuditReport(
        runtime_graph_active=frame.runtime_graph_active,
        runtime_discovery_active=discovery.deterministic_discovery
        and not discovery.full_source_indexing_used,
        dependency_graph_active=graph.bounded_graph_size and not graph.full_repository_graph_used,
        contract_surface_active=not contract.full_signature_replay_used
        and not contract.raw_ast_export_used,
        runtime_clustering_active=clusters.summary_only
        and (clusters.bounded_clusters or max(clusters.cluster_sizes.values(), default=0) <= 9),
        architecture_pressure_active=pressure.bounded_architecture_maintained,
        estimated_avoided_architecture_cognition_tokens=avoided_cognition,
        estimated_avoided_runtime_explosion_drift=avoided_drift,
        bounded_dependency_graph=graph.edge_count <= graph.max_edge_limit,
        summary_only_dependency_metadata=frame.summary_only_dependency_cognition,
        local_only_architecture_cognition=True,
        hidden_telemetry_used=frame.hidden_telemetry_used,
        incremental_context_active=frame.incremental_context_active,
        repo_wide_replay_forbidden=frame.repo_wide_replay_forbidden,
        reasoning_scope_active=frame.reasoning_scope_active,
        automatic_architecture_escalation_forbidden=(
            frame.automatic_architecture_escalation_forbidden
        ),
    )


def audit_runtime_simplification() -> RuntimeSimplificationAuditReport:
    frame = RuntimeSimplificationPolicy().evaluate(".")
    overlap = frame.runtime_overlap
    contract = frame.contract_overlap
    merge = frame.merge_candidates
    governance = frame.governance_duplication
    recommendations = frame.recommendations
    avoided_fragmentation = (
        len(merge.merge_candidates) * 480 + len(overlap.overlap_categories) * 180
    )
    avoided_governance = len(governance.duplicated_governance_groups) * 520
    avoided_contract = len(contract.duplicated_contract_groups) * 260 + (
        700 if contract.oversized_contract_surface else 0
    )
    return RuntimeSimplificationAuditReport(
        runtime_overlap_active=overlap.overlap_detected and overlap.summary_only,
        contract_overlap_active=contract.contract_overlap_detected and contract.summary_only,
        runtime_merge_candidates_active=merge.human_review_required and merge.recommendation_only,
        governance_duplication_active=governance.governance_duplication_detected,
        simplification_recommendations_active=recommendations.summary_only
        and recommendations.human_confirmed_only,
        estimated_avoided_runtime_fragmentation=avoided_fragmentation,
        estimated_avoided_governance_duplication=avoided_governance,
        estimated_avoided_contract_explosion=avoided_contract,
        bounded_simplification_analysis=frame.bounded_simplification_analysis,
        human_confirmed_simplification=recommendations.human_confirmed_only,
        autonomous_mutation_used=frame.autonomous_mutation_used
        or merge.automatic_merge_used
        or recommendations.automatic_rewrite_used,
        incremental_context_active=frame.incremental_context_active,
        repo_wide_replay_forbidden=frame.repo_wide_replay_forbidden,
        reasoning_scope_active=frame.reasoning_scope_active,
        automatic_architecture_escalation_forbidden=(
            frame.automatic_architecture_escalation_forbidden
        ),
    )


def audit_governance_core() -> GovernanceCoreAuditReport:
    frame = GovernanceCorePolicy().evaluate()
    avoided_duplication = (
        frame.pressure.pressure_severity * 80 + len(frame.stale.stale_categories) * 220
    )
    avoided_fragmentation = (
        len(frame.continuity.continuity_scope) * 180 + frame.compact_export.compact_export_size * 4
    )
    avoided_retention_drift = frame.retention.eviction_count * 360
    return GovernanceCoreAuditReport(
        governance_core_active=frame.governance_core_active,
        pressure_primitives_active=frame.pressure.bounded_pressure_state,
        stale_detection_primitives_active=frame.stale.summary_only,
        bounded_retention_active=frame.retention.bounded_retention_active
        and frame.retention.bounded_growth_maintained,
        continuity_primitives_active=frame.continuity.bounded_continuity_maintained,
        compact_export_primitives_active=frame.compact_export.summary_only
        and frame.compact_export.bounded_export_maintained,
        estimated_avoided_governance_duplication=avoided_duplication,
        estimated_avoided_runtime_fragmentation=avoided_fragmentation,
        estimated_avoided_bounded_retention_drift=avoided_retention_drift,
        bounded_governance_reuse=frame.bounded_governance_reuse,
        human_confirmed_migration=True,
        automatic_rewrite_used=frame.automatic_rewrite_used,
    )


def audit_release_readiness() -> ReleaseReadinessAuditReport:
    activation = audit_runtime_activation()
    session = audit_session_lifecycle()
    workspace = audit_workspace_persistence()
    provider = audit_provider_simulation()
    runtime_graph = audit_runtime_graph()
    simplification = audit_runtime_simplification()
    governance_core = audit_governance_core()
    extension = ExtensionReadinessPolicy().evaluate(".")
    rollout = ConsumerRolloutPolicy().evaluate(".")
    freeze = GovernanceFreezeStatusPolicy().evaluate(".")
    no_hidden_automation = (
        provider.no_real_provider_call
        and not runtime_graph.hidden_telemetry_used
        and not simplification.autonomous_mutation_used
        and governance_core.automatic_rewrite_used is False
    )
    bounded = (
        activation.initialized
        and governance_core.bounded_governance_reuse
        and governance_core.bounded_retention_active
        and session.summary_only_continuity
        and extension.extension_release_ready
        and rollout.human_confirmed_rollout
        and freeze.alpha_boundary_declared
    )
    return ReleaseReadinessAuditReport(
        release_readiness_active=bounded,
        consumer_rollout_active=rollout.consumer_rollout_active,
        extension_release_ready=extension.extension_release_ready,
        governance_freeze_active=freeze.governance_freeze_active,
        bounded_release_confirmed=bounded,
        estimated_avoided_rollout_confusion=len(rollout.supported_consumers) * 420,
        estimated_avoided_stale_migration_context=session.estimated_avoided_tokens
        + workspace.estimated_avoided_stale_persistence_tokens,
        rollback_safe_release_prep=rollout.rollback_procedure_documented,
        local_first_governance=workspace.local_workspace_persistence_active,
        no_hidden_automation=no_hidden_automation,
    )


def audit_vscode_presence() -> VSCodePresenceAuditReport:
    governance_core = audit_governance_core()
    runtime_graph = audit_runtime_graph()
    presence = build_presence_frame(
        ".",
        runtime_audit_active=True,
        governance_core_active=governance_core.governance_core_active,
        runtime_graph_active=runtime_graph.runtime_graph_active,
    )
    version = detect_extension_version(".")
    stale = detect_stale_extension(".")
    heartbeat = build_heartbeat_frame(".")
    projection = project_governance_status(
        presence,
        pressure="HIGH" if presence.stale_session_detected else "LOW",
        stale_extension_detected=stale.stale_extension_detected,
    )
    invisible_drift_saved = (
        1_200 + int(presence.rollover_pending) * 500 + len(projection.compact_status)
    )
    stale_confusion_saved = 1_000 + len(stale.missing_capabilities) * 180
    return VSCodePresenceAuditReport(
        governance_presence_active=presence.summary_only
        and presence.extension_active
        and presence.runtime_audit_active
        and presence.governance_core_active,
        version_detection_active=bool(version.repo_version) or bool(version.installed_version),
        runtime_heartbeat_active=heartbeat.heartbeat_active or heartbeat.stale_heartbeat,
        status_projection_active=projection.summary_only
        and not projection.automatic_action_allowed,
        stale_extension_detection_active=stale.summary_only,
        estimated_avoided_invisible_governance_drift=invisible_drift_saved,
        estimated_avoided_stale_extension_confusion=stale_confusion_saved,
        compact_status=projection.compact_status,
        stale_extension_detected=stale.stale_extension_detected,
        bounded_visibility=presence.summary_only
        and heartbeat.summary_only
        and projection.summary_only
        and stale.summary_only,
    )


def audit_draft_injection() -> DraftInjectionAuditReport:
    vscode_frame = DraftInjectionPolicy().build(
        project_name="workspace",
        sprint_id="next",
        requested_target="vscode_chat",
    )
    copilot_frame = DraftInjectionPolicy().build(
        project_name="workspace",
        sprint_id="next",
        requested_target="copilot_chat",
    )
    frame = vscode_frame
    avoided_friction = (
        frame.observability.estimated_avoided_handoff_friction if frame.observability else 300
    )
    avoided_stale = len(frame.preview.excluded_stale_context) * 420
    return DraftInjectionAuditReport(
        provider_prefill_active=bool(frame.provider_prefill)
        and frame.provider_prefill.awaiting_human_send,
        copilot_prefill_active=copilot_frame.prefill_success and copilot_frame.awaiting_human_send,
        vscode_chat_prefill_active=frame.prefill_success and frame.awaiting_human_send,
        prefill_observability_active=bool(frame.observability)
        and frame.observability.summary_only,
        enter_only_confidence=frame.enter_only_confidence,
        draft_injection_active=frame.draft_prefilled and frame.continuity_injected,
        chat_prefill_active=frame.draft_prefilled,
        chat_launch_active=frame.chat_opened,
        chat_target_detection_active=frame.target == "vscode_chat",
        enter_only_rollover_active=frame.awaiting_human_send and not frame.auto_send,
        clipboard_fallback_active=frame.clipboard_fallback_active,
        no_auto_send=not frame.auto_send,
        no_hidden_continuation=not frame.hidden_continuation,
        no_background_message_dispatch=not frame.background_message_dispatch,
        no_silent_prompt_mutation=not frame.silent_prompt_mutation,
        estimated_avoided_handoff_friction=avoided_friction,
        estimated_avoided_stale_continuity_replay=avoided_stale,
        status_bar_states=frame.status_bar_states,
    )


def audit_consumer_rollout() -> ConsumerRolloutAuditReport:
    consumer_repo = _default_consumer_repo()
    audit = ConsumerRolloutAuditPolicy().evaluate(consumer_repo, platform_repo=".")
    friction = MigrationFrictionPolicy().evaluate(consumer_repo, platform_repo=".")
    compatibility = CompatibilityProjectionPolicy().evaluate(consumer_repo, platform_repo=".")
    governance = GovernanceReadinessPolicy().evaluate(consumer_repo, platform_repo=".")
    rollback = RollbackRehearsalPolicy().evaluate(consumer_repo, platform_repo=".")
    avoided_failure = (
        2_000 + len(friction.friction_categories) * 400 + int(rollback.rollback_ready) * 600
    )
    avoided_stale = 1_200 + len(friction.recommended_human_actions) * 300
    return ConsumerRolloutAuditReport(
        consumer_rollout_active=audit.summary_only and audit.install_state_active,
        rollout_audit_active=audit.summary_only,
        migration_friction_active=friction.summary_only,
        compatibility_projection_active=compatibility.summary_only,
        governance_readiness_active=governance.summary_only,
        rollback_rehearsal_active=rollback.summary_only and rollback.dry_run_only,
        estimated_avoided_rollout_failure=avoided_failure,
        estimated_avoided_stale_migration_state=avoided_stale,
        rollout_ready=audit.rollout_ready,
        migration_friction=audit.migration_friction,
        governance_readiness=audit.governance_readiness,
        rollback_ready=audit.rollback_ready,
        bounded_rollout_confirmed=audit.bounded_rollout_confirmed,
        consumer_name=audit.consumer_name,
    )


def audit_reasoning_routing() -> ReasoningRoutingAuditReport:
    architecture = ReasoningTierPolicy().classify(
        ReasoningTask(
            name="Sprint 42 architecture",
            description="architecture rollout strategy runtime boundary design",
            affected_runtimes=("runtime_graph", "governance_core", "session_orchestrator"),
            architecture_sensitive=True,
            governance_sensitive=True,
        )
    )
    tests = ReasoningTierPolicy().classify(
        ReasoningTask(
            name="runtime tests",
            description="repetitive tests deterministic snapshots",
            affected_runtimes=("tests",),
        )
    )
    docs = ReasoningTierPolicy().classify(
        ReasoningTask(name="docs", description="markdown checklist generation")
    )
    adapter = ReasoningTierPolicy().classify(
        ReasoningTask(
            name="adapter wiring",
            description="runtime integration adapters orchestration wiring",
            affected_runtimes=("providers", "session_orchestrator"),
        )
    )
    complexity = TaskComplexityPolicy().evaluate(
        TaskComplexityInput(
            architecture_density=3,
            cross_runtime_scope=2,
            continuity_size=2,
            reasoning_depth=3,
            dependency_breadth=2,
            governance_sensitivity=3,
            runtime_authority_risk=1,
        )
    )
    floor = QualityFloorPolicy().enforce(
        tests.recommended_tier,
        architecture_protection=True,
        governance_protection=True,
    )
    escalation = EscalationPolicy().evaluate(
        EscalationPolicyInput(
            recommended_tier=architecture.recommended_tier,
            complexity_level=complexity.complexity_level,
            escalation_required=complexity.escalation_required,
            quality_floor_tier=floor.minimum_reasoning_floor,
            previous_escalations=1,
            cooldown_remaining=0,
        )
    )
    budget = CostBudgetPolicy().evaluate(
        (
            ReasoningUsageSample(architecture.task_name, architecture.recommended_tier),
            ReasoningUsageSample(tests.task_name, tests.recommended_tier),
            ReasoningUsageSample(docs.task_name, docs.recommended_tier),
            ReasoningUsageSample(adapter.task_name, adapter.recommended_tier),
        ),
        daily_budget_units=20,
        monthly_budget_units=500,
    )
    sprint_map = SprintReasoningRouter().map(
        "42",
        (
            SprintReasoningTask(
                "architecture",
                "architecture rollout strategy runtime boundary design",
                ("runtime_graph", "governance_core"),
                architecture_sensitive=True,
                governance_sensitive=True,
            ),
            SprintReasoningTask("runtime tests", "repetitive tests deterministic snapshots"),
            SprintReasoningTask("docs", "markdown checklist generation"),
            SprintReasoningTask(
                "adapter wiring",
                "runtime integration adapters orchestration wiring",
                ("providers", "session_orchestrator"),
            ),
        ),
    )
    scope = ReasoningScopeRuntime().evaluate(
        task_name="routine adapter patch",
        complexity="LOW",
        affected_runtimes=("reasoning_routing",),
        touched_files=("ai_dev_os/reasoning_routing/__init__.py",),
        adjacent_contracts=("ReasoningTierFrame",),
        requested_depth=3,
        requested_runtime_count=4,
        repeated_architecture_sections=1,
        governance_sensitive=True,
        continuity_size=3_200,
        escalation_requested=True,
    )
    return ReasoningRoutingAuditReport(
        reasoning_routing_active=architecture.recommended_tier == "HIGH"
        and adapter.recommended_tier == "MEDIUM"
        and tests.recommended_tier == "LOW",
        task_complexity_active=complexity.bounded_metadata
        and complexity.reasoning_recommendation == "HIGH",
        escalation_policy_active=escalation.bounded_escalation
        and escalation.human_visible_escalation
        and not escalation.hidden_provider_switching,
        cost_budget_policy_active=budget.deterministic_estimate and not budget.billing_api_used,
        quality_floor_active=floor.unsafe_downgrade_blocked
        and floor.minimum_reasoning_floor == "HIGH",
        sprint_reasoning_map_active=sprint_map.task_tiers["architecture"] == "HIGH"
        and sprint_map.task_tiers["docs"] == "LOW",
        tier_distribution=budget.reasoning_tier_distribution,
        budget_pressure=budget.budget_pressure,
        escalation_reason=escalation.escalation_reason,
        downgrade_recommendation=budget.downgrade_recommendation,
        compaction_recommendation=budget.compaction_recommendation,
        estimated_avoided_premium_burn=budget.estimated_avoided_premium_burn,
        estimated_avoided_unnecessary_escalation=budget.estimated_avoided_unnecessary_escalation,
        human_visible_routing=architecture.human_visible
        and escalation.human_visible_escalation
        and sprint_map.human_visible_routing,
        deterministic_reasoning_policy=architecture.deterministic_policy
        and budget.deterministic_estimate,
        rollback_safe_routing=architecture.rollback_safe
        and escalation.rollback_safe_escalation
        and sprint_map.rollback_safe_routing,
        provider_neutral_contracts=architecture.provider_neutral,
        hidden_escalation_used=escalation.hidden_provider_switching,
        reasoning_scope_active=scope.reasoning_scope_active,
        local_patch_recommendation_active=(
            scope.reasoning_recommendation.downgrade_to_local_recommendation
        ),
    )


def audit_output_compression() -> OutputCompressionAuditReport:
    validation_results = (
        ValidationResult("pytest", "pass", 289, "full test suite"),
        ValidationResult("runtime audit", "pass", 1, "output compression active"),
        ValidationResult("build", "success", 1, "wheel and sdist verified"),
        ValidationResult("twine", "success", 1, "metadata check"),
        ValidationResult("compile", "success", 1, "VSCode extension"),
    )
    validation = ValidationCompactionPolicy().compact(validation_results)
    sections = (
        SummarySection("validation pass", "pytest passed and build passed"),
        SummarySection("clean worktree", "clean worktree", unchanged=True),
        SummarySection("CI success", "remote CI success", unchanged=True),
        SummarySection("artifact cleanup", "generated artifacts removed", unchanged=True),
        SummarySection("rollout summary", "rollout summary unchanged", unchanged=True),
    )
    dedup = SummaryDeduplicationPolicy().deduplicate(sections)
    density = ReportDensityPolicy().audit(
        tuple(section.title for section in sections),
        unchanged_sections=4,
        repeated_token_estimate=dedup.estimated_avoided_repeated_tokens,
    )
    completion = CompactCompletionPolicy().compact(
        CompactCompletionInput(
            commit="06d38e7",
            ci_status="success",
            validation_results=validation_results,
            runtime_audit_status="active",
            risks=("verbose completion drift", "repeated validation output"),
            next_step="output compression rollout",
            rollout_summary="unchanged rollout summary",
            unchanged_sections=("rollout",),
        )
    )
    return OutputCompressionAuditReport(
        output_compression_active=completion.compact and completion.bounded,
        summary_deduplication_active=dedup.repeated_summary_detected
        and dedup.unchanged_section_suppression,
        validation_compaction_active=validation.validation_aggregation
        and validation.compact_validation_projection.startswith("Validation: pass"),
        report_density_active=density.compaction_recommendation,
        compact_completion_active=completion.compact and completion.deduplicated,
        verbosity_pressure=density.verbosity_pressure,
        compact_summary_lines=len(completion.compact_summary.splitlines()),
        expandable_reporting=completion.expandable and bool(completion.expandable_details),
        human_readable=completion.human_readable,
        rollback_safe=completion.rollback_safe,
        deterministic_compact_mode=completion.deterministic_compact_mode,
        estimated_avoided_completion_tokens=completion.estimated_avoided_completion_tokens,
        estimated_avoided_repeated_summaries=completion.estimated_avoided_repeated_summaries,
        hidden_reporting_used=False,
        validation_skipped=False,
    )


def audit_retrieval_budget() -> RetrievalBudgetAuditReport:
    all_runtimes = (
        "session_orchestrator",
        "context_subset",
        "retrieval",
        "runtime_graph",
        "governance_health",
        "providers",
        "workspace_snapshot",
        "vscode_integration",
    )
    frame = RetrievalBudgetRuntime().evaluate(
        affected_runtimes=("session_orchestrator", "retrieval"),
        all_runtimes=all_runtimes,
        dependencies=(
            RuntimeDependency("session_orchestrator", "retrieval", 1, "continuity"),
            RuntimeDependency("retrieval", "context_subset", 1, "scope"),
            RuntimeDependency("runtime_graph", "governance_health", 3, "pressure"),
            RuntimeDependency("workspace_snapshot", "providers", 4, "optional"),
        ),
        continuity_size=3_200,
        contract_surfaces=("RetrievalScopeFrame", "RetrievalBudgetFrame", "RuntimeDependency"),
        architecture_isolation=True,
        max_dependency_distance=2,
    )
    return RetrievalBudgetAuditReport(
        retrieval_budget_active=frame.retrieval_budget_active,
        retrieval_scope_active=frame.scope.affected_runtime_only_retrieval
        and frame.scope.repo_wide_retrieval_forbidden,
        retrieval_radius_active=frame.radius.dependency_depth_cap_applied
        and frame.radius.max_dependency_distance == 2,
        retrieval_pressure_active=frame.pressure.pressure_level in {"LOW", "MEDIUM", "HIGH"},
        retrieval_compaction_active=frame.compaction.summary_only
        and bool(frame.compaction.expandable_retrieval_details),
        bounded_retrieval_neighborhood=frame.scope.bounded_retrieval_neighborhood,
        repo_wide_retrieval_forbidden=frame.repo_wide_retrieval_forbidden,
        retrieval_pressure=frame.pressure.pressure_level,
        compact_retrieval_recommendation=frame.budget.compact_retrieval_recommendation,
        estimated_avoided_hidden_input_tokens=frame.estimated_avoided_hidden_input_tokens,
        estimated_avoided_repo_wide_reasoning=frame.estimated_avoided_repo_wide_reasoning,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        no_ast_replay=frame.scope.no_ast_replay,
        no_dynamic_tracing=frame.scope.no_dynamic_tracing,
        no_hidden_provider_routing=frame.pressure.no_hidden_provider_routing,
        no_automatic_retrieval_escalation=frame.pressure.no_automatic_retrieval_escalation
        and not frame.budget.automatic_retrieval_escalation,
    )


def audit_incremental_context() -> IncrementalContextAuditReport:
    all_runtimes = (
        "session_orchestrator",
        "continuity_export",
        "retrieval_budget",
        "runtime_graph",
        "runtime_simplification",
        "governance_health",
        "governance_trends",
        "workspace_persistence",
        "output_compression",
        "runtime_audit",
    )
    frame = IncrementalContextRuntime().evaluate(
        changed_runtimes=("incremental_context", "runtime_audit", "retrieval_budget"),
        all_runtimes=all_runtimes,
        dependencies=(
            RuntimeDependency("incremental_context", "retrieval_budget", 1, "delta_retrieval"),
            RuntimeDependency("incremental_context", "runtime_graph", 1, "runtime_delta"),
            RuntimeDependency("runtime_audit", "governance_health", 2, "audit_delta"),
            RuntimeDependency("workspace_persistence", "governance_trends", 4, "stale"),
        ),
        changed_contracts=("IncrementalContextFrame", "IncrementalContextAuditReport"),
        changed_governance=("NFR-COST-18", "NFR-ARCH-32", "NFR-RETRIEVAL-02"),
        changed_session=("FR-INCREMENTALCONTEXT-01..07",),
        previous_continuity=("prior retrieval budget summary", "prior CI summary"),
        current_continuity=("incremental context runtime active", "delta audit active"),
        stale_continuity=("old sprint completion replay",),
        changed_audit_sections=("incremental_context", "runtime_audit", "retrieval_budget"),
        unchanged_audit_sections=("activation", "routing", "provider_simulation"),
        repeated_validations=("ruff", "pytest", "runtime_audit"),
        continuity_size=2_800,
        architecture_isolation=True,
    )
    return IncrementalContextAuditReport(
        incremental_context_active=frame.incremental_context_active,
        context_delta_active=frame.context_delta.unchanged_context_exclusion,
        delta_retrieval_active=frame.delta_retrieval.delta_only_retrieval,
        continuity_delta_active=frame.continuity_delta.continuity_replay_reduction,
        audit_delta_active=frame.audit_delta.runtime_audit_delta_mode,
        cognition_cache_active=frame.cognition_cache.bounded_retention,
        incremental_pressure_active=frame.incremental_pressure.repeated_replay_detection,
        incremental_recommendation_active=(
            frame.incremental_recommendation.delta_only_session_recommendation
        ),
        estimated_avoided_repeated_input_tokens=(frame.estimated_avoided_repeated_input_tokens),
        estimated_avoided_duplicate_runtime_cognition=(
            frame.estimated_avoided_duplicate_runtime_cognition
        ),
        replay_pressure=frame.incremental_pressure.pressure_level,
        compact_changed_neighborhood=frame.delta_retrieval.compact_changed_neighborhood,
        unchanged_context_excluded=frame.context_delta.excluded_unchanged_context,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        bounded_retention=frame.bounded_retention,
        no_raw_transcript_persistence=frame.no_raw_transcript_persistence,
        no_hidden_provider_memory=frame.no_hidden_provider_memory,
        no_ast_replay=frame.no_ast_replay,
        no_repo_wide_replay=frame.no_repo_wide_replay,
        no_dynamic_tracing=frame.no_dynamic_tracing,
        no_automatic_context_expansion=frame.no_automatic_context_expansion,
    )


def audit_reasoning_scope() -> ReasoningScopeAuditReport:
    frame = ReasoningScopeRuntime().evaluate(
        task_name="low complexity local patch",
        complexity="LOW",
        affected_runtimes=("reasoning_scope", "reasoning_routing"),
        touched_files=(
            "ai_dev_os/reasoning_scope/__init__.py",
            "ai_dev_os/runtime_audit.py",
        ),
        adjacent_contracts=("ReasoningScopeRuntimeFrame", "ReasoningRoutingAuditReport"),
        requested_depth=4,
        requested_runtime_count=7,
        repeated_architecture_sections=2,
        governance_sensitive=True,
        architecture_sensitive=False,
        continuity_size=4_200,
        escalation_requested=True,
    )
    return ReasoningScopeAuditReport(
        reasoning_scope_active=frame.reasoning_scope_active,
        reasoning_depth_active=frame.reasoning_depth.reasoning_depth_cap > 0,
        architecture_reasoning_guard_active=(
            frame.architecture_guard.architecture_wide_reasoning_forbidden
            and frame.architecture_guard.no_automatic_architecture_escalation
        ),
        local_patch_mode_active=frame.local_patch_mode.local_runtime_only_reasoning,
        reasoning_pressure_active=frame.reasoning_pressure.pressure_level
        in {"LOW", "MEDIUM", "HIGH"},
        reasoning_compaction_active=frame.reasoning_compaction.summary_only
        and bool(frame.reasoning_compaction.compact_reasoning_summaries),
        reasoning_recommendation_active=(
            frame.reasoning_recommendation.premium_reasoning_avoidance_recommendation
        ),
        estimated_avoided_premium_reasoning_burn=(frame.estimated_avoided_premium_reasoning_burn),
        estimated_avoided_unnecessary_architecture_reasoning=(
            frame.estimated_avoided_unnecessary_architecture_reasoning
        ),
        pressure_level=frame.reasoning_pressure.pressure_level,
        depth_cap=frame.reasoning_depth.reasoning_depth_cap,
        task_local_cognition_scope=frame.reasoning_scope.task_local_cognition_scope,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        bounded_cognition_only=frame.bounded_cognition_only,
        no_hidden_chain_of_thought_persistence=(frame.no_hidden_chain_of_thought_persistence),
        no_ast_replay=frame.no_ast_replay,
        no_hidden_provider_routing=frame.no_hidden_provider_routing,
        no_automatic_architecture_escalation=frame.no_automatic_architecture_escalation,
        no_automatic_roadmap_synthesis=frame.no_automatic_roadmap_synthesis,
    )


def audit_provider_routing() -> ProviderRoutingAuditReport:
    frame = ProviderRoutingRuntime().evaluate(
        cognition_tier="MEDIUM",
        implementation_patch=True,
        compact_summary=True,
        premium_units_used=9,
        premium_reasoning_requests=2,
        premium_escalations=1,
        previous_distribution=("LOW:2", "MEDIUM:1"),
    )
    return ProviderRoutingAuditReport(
        provider_routing_active=frame.provider_routing_active,
        provider_capability_matrix_active=(
            frame.capability_matrix.deterministic_provider_metadata_only
        ),
        provider_budget_policy_active=frame.budget_policy.deterministic_estimate
        and not frame.budget_policy.billing_api_used,
        provider_pressure_active=frame.pressure.provider_pressure in {"LOW", "MEDIUM", "HIGH"},
        provider_downgrade_active=frame.downgrade.quality_floor_aware_downgrade,
        provider_observability_active=frame.observability.no_real_billing_integration
        and frame.observability.deterministic_estimated_burn_only,
        estimated_avoided_premium_provider_burn=(frame.estimated_avoided_premium_provider_burn),
        estimated_avoided_unnecessary_high_tier_usage=(
            frame.estimated_avoided_unnecessary_high_tier_usage
        ),
        recommended_provider_class=frame.recommendation.recommended_provider_class,
        provider_burn_pressure=frame.budget_policy.provider_burn_pressure,
        premium_vs_cheap_ratio=frame.observability.premium_vs_cheap_ratio,
        no_real_billing_api=frame.no_real_billing_api,
        no_hidden_provider_switching=frame.no_hidden_provider_switching,
        no_automatic_provider_execution=frame.no_automatic_provider_execution,
        no_provider_upload=frame.no_provider_upload,
        no_hidden_escalation=frame.no_hidden_escalation,
        provider_neutral=frame.provider_neutral,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
    )


def audit_provider_experimental() -> ProviderExperimentalAuditReport:
    frame = ProviderExperimentalRuntime().evaluate()
    return ProviderExperimentalAuditReport(
        experimental_provider_active=frame.experimental_provider_active,
        openmythos_provider_active=frame.openmythos_provider_active,
        openmythos_loaded=frame.openmythos_loaded,
        openmythos_gguf_active=frame.openmythos_gguf_active,
        openmythos_conversion_active=frame.openmythos_conversion_active,
        openmythos_runtime_stability=frame.openmythos_runtime_stability,
        openmythos_drift_risk=frame.openmythos_drift_risk,
        openmythos_reasoning_depth_signal=frame.openmythos_reasoning_depth_signal,
        openmythos_governance_adherence=frame.openmythos_governance_adherence,
        provider_benchmark_active=frame.provider_benchmark_active,
        provider_comparison_active=frame.provider_comparison_active,
        provider_drift_active=frame.provider_drift_active,
        provider_governance_active=frame.governance.provider_governance_active,
        provider_benchmark_summary_active=frame.summary.provider_benchmark_summary_active,
        provider_benchmark_eviction_active=frame.eviction.provider_benchmark_eviction_active,
        openmythos_load_result=frame.openmythos.load_result,
        openmythos_direct_hf_result=frame.gguf.direct_ollama_result,
        openmythos_weighted_hf_result=frame.gguf.weighted_ollama_result,
        openmythos_gguf_conversion_result=frame.conversion.conversion_result,
        openmythos_quantization=frame.quantization.preferred_quantization,
        openmythos_ollama_model=frame.conversion.ollama_model_name,
        openmythos_fallback_route=frame.fallback.fallback_route,
        vram_runtime_stability=frame.openmythos.vram_runtime_stability,
        provider_comparison_summary="; ".join(frame.comparison.providers),
        governance_adherence_observation=frame.summary.governance_adherence_observation,
        architecture_drift_observation=frame.summary.architecture_drift_observation,
        estimated_reasoning_depth_gain=frame.estimated_reasoning_depth_gain,
        estimated_governance_instability_risk=frame.estimated_governance_instability_risk,
        estimated_architecture_drift_risk=frame.estimated_architecture_drift_risk,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        rollback_safe=frame.experimental.rollback_safe,
        no_architecture_authority=frame.openmythos.no_architecture_authority,
        no_governance_authority=frame.openmythos.no_governance_authority,
        no_anti_explosion_authority=frame.openmythos.no_anti_explosion_authority,
        no_autonomous_execution_authority=frame.openmythos.no_autonomous_execution_authority,
    )


def audit_provider_stability() -> ProviderStabilityAuditReport:
    frame = ProviderStabilityRuntime().evaluate()
    return ProviderStabilityAuditReport(
        provider_stability_active=frame.provider_stability_active,
        long_session_drift_active=frame.long_session_drift_active,
        governance_decay_active=frame.governance_decay_active,
        compactness_retention_active=frame.compactness_retention_active,
        retrieval_radius_active=frame.retrieval_radius.retrieval_radius_active,
        hallucination_pressure_active=frame.hallucination_pressure.hallucination_pressure_active,
        stability_benchmark_active=frame.benchmark.stability_benchmark_active,
        provider_stability_comparison=frame.benchmark.provider_stability_comparison,
        governance_adherence_ranking=frame.governance_decay.governance_adherence_ranking,
        compactness_retention_ranking=frame.compactness_retention.compactness_retention_ranking,
        drift_resistance_ranking=frame.hallucination_pressure.drift_resistance_ranking,
        local_patch_adherence_ranking=frame.benchmark.local_patch_adherence_ranking,
        repetitive_reliability_ranking=frame.benchmark.repetitive_reliability_ranking,
        retrieval_discipline_ranking=frame.retrieval_radius.retrieval_discipline_ranking,
        estimated_long_session_degradation=(
            frame.long_session_drift.estimated_long_session_degradation
        ),
        estimated_provider_stability_gain=frame.estimated_provider_stability_gain,
        estimated_recursive_drift_risk=frame.estimated_recursive_drift_risk,
        openmythos_placeholder_only=frame.stability.openmythos_placeholder_only,
        no_real_openmythos_execution=frame.benchmark.no_real_openmythos_execution,
        no_hidden_provider_switching=frame.benchmark.no_hidden_provider_switching,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
    )


def audit_adaptive_provider_routing() -> AdaptiveProviderRoutingAuditReport:
    frame = AdaptiveProviderRoutingRuntime().evaluate()
    return AdaptiveProviderRoutingAuditReport(
        adaptive_provider_routing_active=frame.adaptive_provider_routing_active,
        drift_aware_routing_active=frame.drift_aware_routing_active,
        governance_weighted_routing_active=frame.governance_weighted_routing_active,
        long_session_routing_active=frame.long_session_routing_active,
        routing_confidence_active=frame.routing_confidence_active,
        provider_recommendation_ranking=frame.recommendation.provider_recommendation_ranking,
        stability_weighted_ranking=frame.stability_weighted.stability_weighted_ranking,
        governance_weighted_ranking=frame.governance_weighted.governance_weighted_ranking,
        routing_confidence_summary=frame.confidence.routing_confidence_summary,
        drift_aware_routing_result=frame.drift_aware.drift_aware_routing_result,
        governance_weighted_routing_result=(
            frame.governance_weighted.governance_weighted_routing_result
        ),
        estimated_avoided_provider_drift=frame.estimated_avoided_provider_drift,
        estimated_avoided_recursive_routing=frame.estimated_avoided_recursive_routing,
        estimated_avoided_premium_burn=frame.estimated_avoided_premium_burn,
        human_confirmed_only=frame.human_confirmed_only,
        deterministic=frame.deterministic,
        rollback_safe=frame.rollback_safe,
        no_hidden_provider_switching=frame.adaptive.no_hidden_provider_switching,
        no_recursive_routing_loops=frame.adaptive.no_recursive_routing_loops,
        no_unrestricted_provider_escalation=frame.adaptive.no_unrestricted_provider_escalation,
        automatic_switching_allowed=frame.recommendation.automatic_switching_allowed,
        governance_runtime_bypassed=frame.governance.governance_runtime_bypassed,
    )


def audit_provider_fatigue() -> ProviderFatigueAuditReport:
    frame = ProviderFatigueRuntime().evaluate()
    return ProviderFatigueAuditReport(
        provider_fatigue_active=frame.provider_fatigue_active,
        escalation_fatigue_active=frame.escalation_fatigue_active,
        fallback_oscillation_active=frame.fallback_oscillation_active,
        compactness_decay_active=frame.compactness_decay_active,
        long_session_pressure_active=frame.long_session_pressure_active,
        fatigue_confidence_active=frame.confidence.fatigue_confidence_active,
        provider_recovery_active=frame.recovery.provider_recovery_active,
        provider_fatigue_summary=frame.confidence.fatigue_confidence_summary,
        escalation_fatigue_warning=frame.escalation_fatigue.escalation_fatigue_warning,
        fallback_oscillation_summary=(frame.fallback_oscillation.fallback_oscillation_summary),
        compactness_decay_recommendation=(
            frame.compactness_decay.bounded_compression_recommendation
        ),
        recovery_recommendation=frame.recovery.recovery_recommendation,
        estimated_avoided_provider_exhaustion=(frame.estimated_avoided_provider_exhaustion),
        estimated_avoided_recursive_fatigue=frame.estimated_avoided_recursive_fatigue,
        estimated_avoided_premium_burn=frame.estimated_avoided_premium_burn,
        human_confirmed_only=frame.human_confirmed_only,
        deterministic=frame.deterministic,
        rollback_safe=frame.rollback_safe,
        autonomous_provider_replacement=(frame.governance.autonomous_provider_replacement),
        recursive_reroute_loops_blocked=(
            frame.fallback_oscillation.recursive_reroute_loops_blocked
        ),
        governance_runtime_bypassed=frame.governance.governance_runtime_bypassed,
        hidden_escalation_switching=frame.governance.hidden_escalation_switching,
    )


def audit_cognitive_memory_pressure() -> CognitiveMemoryPressureAuditReport:
    frame = CognitiveMemoryPressureRuntime().evaluate()
    return CognitiveMemoryPressureAuditReport(
        cognitive_memory_pressure_active=frame.cognitive_memory_pressure_active,
        continuity_inflation_active=frame.continuity_inflation_active,
        retrieval_overload_active=frame.retrieval_overload_active,
        summary_entropy_active=frame.summary_entropy_active,
        context_fragmentation_active=frame.context_fragmentation_active,
        memory_pressure_summary=frame.cognitive_memory_pressure.memory_pressure_summary,
        continuity_inflation_summary=frame.continuity_inflation.inflation_warning,
        retrieval_overload_summary=frame.retrieval_overload.retrieval_overload_summary,
        summary_entropy_summary=frame.summary_entropy.summary_entropy_summary,
        continuity_recovery_recommendation=(
            frame.continuity_recovery.continuity_recovery_recommendation
        ),
        estimated_avoided_context_explosion=frame.estimated_avoided_context_explosion,
        estimated_avoided_summary_entropy=frame.estimated_avoided_summary_entropy,
        estimated_avoided_retrieval_overload=frame.estimated_avoided_retrieval_overload,
        human_confirmed_only=frame.human_confirmed_only,
        deterministic=frame.deterministic,
        rollback_safe=frame.rollback_safe,
        autonomous_cognition_erasure=frame.governance.autonomous_cognition_erasure,
        recursive_continuity_mutation=frame.governance.recursive_continuity_mutation,
        governance_runtime_bypassed=frame.governance.governance_runtime_bypassed,
        hidden_context_mutation=frame.governance.hidden_context_mutation,
        retrieval_scope_expansion_allowed=frame.governance.retrieval_scope_expansion_allowed,
        automatic_context_expansion=frame.governance.automatic_context_expansion,
    )


def audit_execution_continuation() -> ExecutionContinuationAuditReport:
    frame = ExecutionContinuationRuntime().evaluate()
    return ExecutionContinuationAuditReport(
        execution_continuation_active=frame.execution_continuation_active,
        continuation_budget_active=frame.continuation_budget_active,
        continuation_governance_active=frame.continuation_governance_active,
        continuation_checkpoint_active=frame.continuation_checkpoint_active,
        continuation_termination_active=frame.continuation_termination_active,
        continuation_summary=frame.continuation.continuation_summary,
        governance_summary="LOCAL_PATCH_BOUNDED_RETRIEVAL_COMPACT_CONTINUITY",
        checkpoint_summary=frame.checkpoint.execution_progress_summary,
        termination_summary=frame.termination.termination_reason,
        estimated_avoided_execution_stalls=frame.estimated_avoided_execution_stalls,
        estimated_avoided_recursive_loops=frame.estimated_avoided_recursive_loops,
        estimated_avoided_agent_explosions=frame.estimated_avoided_agent_explosions,
        deterministic=frame.deterministic,
        bounded=frame.bounded,
        rollback_safe=frame.rollback_safe,
        local_only=frame.local_only,
        summary_only=frame.summary_only,
        governance_rules_mutated=frame.governance.governance_rules_mutated,
        hidden_background_execution_blocked=(frame.governance.hidden_background_execution_blocked),
        recursive_execution_loops_blocked=frame.governance.recursive_execution_loops_blocked,
    )


def audit_execution_saturation() -> ExecutionSaturationAuditReport:
    frame = ExecutionSaturationRuntime().evaluate()
    return ExecutionSaturationAuditReport(
        execution_saturation_active=frame.execution_saturation_active,
        retry_oscillation_active=frame.retry_oscillation_active,
        tool_congestion_active=frame.tool_congestion_active,
        checkpoint_inflation_active=frame.checkpoint_inflation_active,
        saturation_termination_active=frame.saturation_termination_active,
        estimated_avoided_recursive_execution=(frame.estimated_avoided_recursive_execution),
        estimated_avoided_retry_loops=frame.estimated_avoided_retry_loops,
        estimated_avoided_checkpoint_explosion=(frame.estimated_avoided_checkpoint_explosion),
    )


def audit_execution_recovery() -> ExecutionRecoveryAuditReport:
    frame = ExecutionRecoveryRuntime().evaluate()
    return ExecutionRecoveryAuditReport(
        execution_recovery_active=frame.execution_recovery_active,
        recovery_cooldown_active=frame.recovery_cooldown_active,
        recovery_checkpoint_integrity_active=(frame.recovery_checkpoint_integrity_active),
        recovery_termination_active=frame.recovery_termination_active,
        estimated_avoided_recovery_loops=frame.estimated_avoided_recovery_loops,
        estimated_avoided_checkpoint_corruption=(frame.estimated_avoided_checkpoint_corruption),
        estimated_avoided_recursive_repair=frame.estimated_avoided_recursive_repair,
    )


def audit_execution_coordination() -> ExecutionCoordinationAuditReport:
    frame = ExecutionCoordinationRuntime().evaluate()
    return ExecutionCoordinationAuditReport(
        execution_coordination_active=frame.execution_coordination_active,
        coordination_conflict_active=frame.coordination_conflict_active,
        coordination_priority_active=frame.coordination_priority_active,
        coordination_termination_active=frame.coordination_termination_active,
        estimated_avoided_runtime_conflicts=frame.estimated_avoided_runtime_conflicts,
        estimated_avoided_recursive_coordination=(frame.estimated_avoided_recursive_coordination),
        estimated_avoided_runtime_oscillation=(frame.estimated_avoided_runtime_oscillation),
    )


def audit_execution_intent() -> ExecutionIntentAuditReport:
    frame = ExecutionIntentRuntime().evaluate()
    return ExecutionIntentAuditReport(
        execution_intent_active=frame.execution_intent_active,
        intent_priority_active=frame.intent_priority_active,
        intent_transition_active=frame.intent_transition_active,
        intent_conflict_active=frame.intent_conflict_active,
        estimated_avoided_intent_oscillation=frame.estimated_avoided_intent_oscillation,
        estimated_avoided_recursive_planning=frame.estimated_avoided_recursive_planning,
        estimated_avoided_execution_instability=(frame.estimated_avoided_execution_instability),
    )


def audit_execution_session() -> ExecutionSessionAuditReport:
    frame = ExecutionSessionRuntime().evaluate()
    return ExecutionSessionAuditReport(
        execution_session_active=frame.execution_session_active,
        session_lifecycle_active=frame.session_lifecycle_active,
        session_integrity_active=frame.session_integrity_active,
        session_termination_active=frame.session_termination_active,
        estimated_avoided_orphaned_sessions=frame.estimated_avoided_orphaned_sessions,
        estimated_avoided_recursive_persistence=(frame.estimated_avoided_recursive_persistence),
        estimated_avoided_session_fragmentation=(frame.estimated_avoided_session_fragmentation),
    )


def audit_execution_stability() -> ExecutionStabilityAuditReport:
    frame = ExecutionStabilityRuntime().evaluate()
    return ExecutionStabilityAuditReport(
        execution_stability_active=frame.execution_stability_active,
        stability_drift_active=frame.stability_drift_active,
        stability_oscillation_active=frame.stability_oscillation_active,
        stability_persistence_active=frame.stability_persistence_active,
        estimated_avoided_long_session_drift=frame.estimated_avoided_long_session_drift,
        estimated_avoided_recursive_stabilization=(
            frame.estimated_avoided_recursive_stabilization
        ),
        estimated_avoided_persistence_entropy=frame.estimated_avoided_persistence_entropy,
    )


def audit_execution_quality() -> ExecutionQualityAuditReport:
    frame = ExecutionQualityRuntime().evaluate()
    return ExecutionQualityAuditReport(
        execution_quality_active=frame.execution_quality_active,
        quality_drift_active=frame.quality_drift_active,
        quality_redundancy_active=frame.quality_redundancy_active,
        quality_persistence_active=frame.quality_persistence_active,
        estimated_avoided_low_value_execution=(frame.estimated_avoided_low_value_execution),
        estimated_avoided_recursive_optimization=(frame.estimated_avoided_recursive_optimization),
        estimated_avoided_execution_redundancy=(frame.estimated_avoided_execution_redundancy),
    )


def audit_verified_execution() -> VerifiedExecutionAuditReport:
    frame = VerifiedExecutionRuntime().evaluate()
    return VerifiedExecutionAuditReport(
        verified_execution_active=frame.envelope_active,
        command_runtime_active=frame.verification.command_verified,
        filesystem_runtime_active=frame.verification.filesystem_verified,
        pytest_runtime_active=frame.verification.pytest_verified,
        git_runtime_active=frame.verification.git_verified,
        evidence_runtime_active=frame.integrity.integrity_active,
        estimated_avoided_fake_execution=frame.estimated_avoided_fake_execution,
        estimated_avoided_hallucinated_pytest=frame.estimated_avoided_hallucinated_pytest,
        estimated_avoided_synthetic_git_state=frame.estimated_avoided_synthetic_git_state,
    )


def audit_cognitive_state() -> CognitiveStateAuditReport:
    frame = CognitiveStateRuntime().evaluate()
    return CognitiveStateAuditReport(
        cognitive_state_active=frame.cognitive_state_active,
        attention_distribution=frame.attention_distribution,
        memory_pressure=frame.memory_pressure,
        decay_status=frame.decay_status,
    )


def audit_intentional_planning() -> IntentionalPlanningAuditReport:
    frame = IntentionalPlanningRuntime().evaluate()
    return IntentionalPlanningAuditReport(
        intentional_planning_active=frame.intentional_planning_active,
        active_goal_count=frame.active_goal_count,
        planning_window_pressure=frame.planning_window_pressure,
        planning_decay_status=frame.planning_decay_status,
        planning_interruption_pressure=frame.planning_interruption_pressure,
        estimated_avoided_recursive_planning=(frame.estimated_avoided_recursive_planning),
        estimated_avoided_goal_explosion=frame.estimated_avoided_goal_explosion,
        estimated_avoided_frontier_reasoning=(frame.estimated_avoided_frontier_reasoning),
    )


def audit_sprint_loop() -> SprintLoopAuditReport:
    frame = SprintLoopRuntime().evaluate()
    return SprintLoopAuditReport(
        sprint_loop_active=frame.sprint_loop_active,
        sprint_validation_score=frame.sprint_validation_score,
        sprint_regression_score=frame.sprint_regression_score,
        sprint_commit_readiness_score=frame.sprint_commit_readiness_score,
        sprint_continuation_score=frame.sprint_continuation_score,
        estimated_avoided_manual_orchestration=(frame.estimated_avoided_manual_orchestration),
        estimated_avoided_recursive_sprints=(frame.estimated_avoided_recursive_sprints),
        estimated_avoided_frontier_supervision=(frame.estimated_avoided_frontier_supervision),
    )


def audit_runtime_hardening() -> RuntimeHardeningAuditReport:
    frame = RuntimeHardeningRuntime().evaluate()
    return RuntimeHardeningAuditReport(
        runtime_hardening_active=frame.runtime_hardening_active,
        retry_storm_score=frame.retry_storm_score,
        escalation_oscillation_score=frame.escalation_oscillation_score,
        continuation_stability_score=frame.continuation_stability_score,
        provider_starvation_score=frame.provider_starvation_score,
        orchestration_deadlock_score=frame.orchestration_deadlock_score,
        estimated_avoided_retry_storms=frame.estimated_avoided_retry_storms,
        estimated_avoided_orchestration_collapse=(frame.estimated_avoided_orchestration_collapse),
        estimated_avoided_frontier_stabilization=(frame.estimated_avoided_frontier_stabilization),
    )


def audit_continuous_runtime_audit() -> ContinuousRuntimeAuditReport:
    frame = ContinuousRuntimeAuditRuntime().evaluate()
    return ContinuousRuntimeAuditReport(
        continuous_runtime_audit_active=frame.continuous_runtime_audit_active,
        runtime_health_score=frame.runtime_health_score,
        retry_pressure_score=frame.retry_pressure_score,
        provider_fatigue_score=frame.provider_fatigue_score,
        continuation_instability_score=frame.continuation_instability_score,
        orchestration_pressure_score=frame.orchestration_pressure_score,
        estimated_avoided_runtime_blindness=frame.estimated_avoided_runtime_blindness,
        estimated_avoided_orchestration_collapse=(frame.estimated_avoided_orchestration_collapse),
        estimated_avoided_frontier_observability=(frame.estimated_avoided_frontier_observability),
    )


def audit_failure_injection() -> FailureInjectionAuditReport:
    frame = FailureInjectionRuntime().evaluate()
    return FailureInjectionAuditReport(
        failure_injection_active=frame.failure_injection_active,
        retry_injection_score=frame.retry_injection_score,
        provider_injection_score=frame.provider_injection_score,
        continuation_injection_score=frame.continuation_injection_score,
        orchestration_injection_score=frame.orchestration_injection_score,
        recovery_resilience_score=frame.recovery_resilience_score,
        estimated_avoided_runtime_collapse=frame.estimated_avoided_runtime_collapse,
        estimated_avoided_frontier_recovery=frame.estimated_avoided_frontier_recovery,
        estimated_avoided_hidden_instability=frame.estimated_avoided_hidden_instability,
    )


def audit_soak_stability() -> SoakStabilityAuditReport:
    frame = SoakStabilityRuntime().evaluate()
    return SoakStabilityAuditReport(
        soak_stability_active=frame.soak_stability_active,
        long_session_stability_score=frame.long_session_stability_score,
        retry_accumulation_score=frame.retry_accumulation_score,
        provider_fatigue_accumulation_score=frame.provider_fatigue_accumulation_score,
        continuation_entropy_score=frame.continuation_entropy_score,
        orchestration_queue_drift_score=frame.orchestration_queue_drift_score,
        estimated_avoided_slow_degradation=frame.estimated_avoided_slow_degradation,
        estimated_avoided_runtime_entropy=frame.estimated_avoided_runtime_entropy,
        estimated_avoided_frontier_stabilization=frame.estimated_avoided_frontier_stabilization,
    )


def audit_provider_cost_stabilization() -> ProviderCostStabilizationAuditReport:
    frame = ProviderCostStabilizationRuntime().evaluate()
    return ProviderCostStabilizationAuditReport(
        provider_cost_stabilization_active=frame.provider_cost_stabilization_active,
        frontier_dependency_score=frame.frontier_dependency_score,
        retry_cost_score=frame.retry_cost_score,
        continuation_reuse_score=frame.continuation_reuse_score,
        orchestration_cost_score=frame.orchestration_cost_score,
        local_first_efficiency_score=frame.local_first_efficiency_score,
        estimated_avoided_frontier_escalation=frame.estimated_avoided_frontier_escalation,
        estimated_avoided_cost_drift=frame.estimated_avoided_cost_drift,
        estimated_avoided_runtime_overhead=frame.estimated_avoided_runtime_overhead,
    )


def audit_main_merge_qualification() -> MainMergeQualificationAuditReport:
    frame = MainMergeQualificationRuntime().evaluate()
    return MainMergeQualificationAuditReport(
        main_merge_qualification_active=frame.main_merge_qualification_active,
        merge_readiness_score=frame.merge_readiness_score,
        governance_completeness_score=frame.governance_completeness_score,
        validation_completeness_score=frame.validation_completeness_score,
        runtime_coherence_score=frame.runtime_coherence_score,
        operational_risk_score=frame.operational_risk_score,
        estimated_avoided_merge_regression=frame.estimated_avoided_merge_regression,
        estimated_avoided_runtime_instability=frame.estimated_avoided_runtime_instability,
        estimated_avoided_frontier_dependency=frame.estimated_avoided_frontier_dependency,
    )


def audit_observation_review() -> RuntimeReadinessFrame:
    return ObservationReviewRuntime().evaluate()


def audit_main_merge_rehearsal() -> MainMergeRehearsalAuditReport:
    frame = MainMergeRehearsalRuntime().evaluate()
    return MainMergeRehearsalAuditReport(
        main_merge_rehearsal_active=frame.main_merge_rehearsal_active,
        protected_branch_readiness_score=frame.protected_branch_readiness_score,
        merge_conflict_visibility_score=frame.merge_conflict_visibility_score,
        rollback_survivability_score=frame.rollback_survivability_score,
        post_merge_runtime_score=frame.post_merge_runtime_score,
        ci_readiness_score=frame.ci_readiness_score,
        estimated_avoided_merge_instability=frame.estimated_avoided_merge_instability,
        estimated_avoided_post_merge_regression=frame.estimated_avoided_post_merge_regression,
        estimated_avoided_frontier_recovery=frame.estimated_avoided_frontier_recovery,
    )


def audit_runtime_orchestrator() -> RuntimeOrchestratorAuditReport:
    frame = RuntimeOrchestrator().evaluate()
    return RuntimeOrchestratorAuditReport(
        runtime_orchestrator_active=frame.runtime_orchestrator_active,
        orchestration_schedule_score=frame.orchestration_schedule_score,
        validation_schedule_score=frame.validation_schedule_score,
        retry_schedule_score=frame.retry_schedule_score,
        continuation_schedule_score=frame.continuation_schedule_score,
        estimated_avoided_manual_scheduling=frame.estimated_avoided_manual_scheduling,
        estimated_avoided_recursive_orchestration=(
            frame.estimated_avoided_recursive_orchestration
        ),
        estimated_avoided_frontier_next_step_reasoning=(
            frame.estimated_avoided_frontier_next_step_reasoning
        ),
    )


def audit_streaming_cognition() -> StreamingCognitionAuditReport:
    frame = StreamingCognitionRuntime().evaluate()
    return StreamingCognitionAuditReport(
        streaming_cognition_active=frame.streaming_cognition_active,
        streaming_latency_score=frame.streaming_latency_score,
        interruption_recovery_score=frame.interruption_recovery_score,
        provider_streaming_score=frame.provider_streaming_score,
        continuation_streaming_score=frame.continuation_streaming_score,
        bounded_cognition_score=frame.bounded_cognition_score,
        estimated_avoided_streaming_instability=frame.estimated_avoided_streaming_instability,
        estimated_avoided_provider_interruptions=frame.estimated_avoided_provider_interruptions,
        estimated_avoided_frontier_streaming=frame.estimated_avoided_frontier_streaming,
    )


def audit_sprint_continuation() -> SprintContinuationAuditReport:
    frame = SprintContinuationRuntime().evaluate()
    return SprintContinuationAuditReport(
        sprint_continuation_active=frame.sprint_continuation_active,
        continuation_selection_score=frame.continuation_selection_score,
        backlog_continuation_score=frame.backlog_continuation_score,
        dependency_continuation_score=frame.dependency_continuation_score,
        regression_continuation_score=frame.regression_continuation_score,
        operational_carryover_score=frame.operational_carryover_score,
        estimated_avoided_continuation_drift=frame.estimated_avoided_continuation_drift,
        estimated_avoided_recursive_sprinting=frame.estimated_avoided_recursive_sprinting,
        estimated_avoided_frontier_planning=frame.estimated_avoided_frontier_planning,
    )


def audit_runtime_policy() -> RuntimePolicyAuditReport:
    frame = RuntimePolicyEngine().evaluate()
    return RuntimePolicyAuditReport(
        runtime_policy_active=frame.runtime_policy_active,
        execution_policy_score=frame.execution_policy_score,
        retry_policy_score=frame.retry_policy_score,
        provider_policy_score=frame.provider_policy_score,
        continuation_policy_score=frame.continuation_policy_score,
        reflective_policy_score=frame.reflective_policy_score,
        estimated_avoided_recursive_governance=(frame.estimated_avoided_recursive_governance),
        estimated_avoided_frontier_escalation=(frame.estimated_avoided_frontier_escalation),
        estimated_avoided_policy_fragmentation=(frame.estimated_avoided_policy_fragmentation),
    )


def audit_execution_memory() -> ExecutionMemoryAuditReport:
    frame = ExecutionMemoryRuntime().evaluate()
    return ExecutionMemoryAuditReport(
        execution_memory_active=frame.execution_memory_active,
        execution_pattern_score=frame.execution_pattern_score,
        retry_pattern_score=frame.retry_pattern_score,
        execution_reuse_score=frame.execution_reuse_score,
        provider_execution_memory_score=frame.provider_execution_memory_score,
        estimated_avoided_retry_repetition=frame.estimated_avoided_retry_repetition,
        estimated_avoided_frontier_replanning=frame.estimated_avoided_frontier_replanning,
        estimated_avoided_execution_instability=(frame.estimated_avoided_execution_instability),
    )


def audit_adaptive_provider() -> AdaptiveProviderAuditReport:
    frame = AdaptiveProviderRuntime().evaluate()
    return AdaptiveProviderAuditReport(
        adaptive_provider_active=frame.adaptive_provider_active,
        provider_capability_score=frame.provider_capability_score,
        provider_fatigue_score=frame.provider_fatigue_score,
        provider_cost_pressure=frame.provider_cost_pressure,
        provider_confidence_score=frame.provider_confidence_score,
        estimated_avoided_frontier_provider_usage=(
            frame.estimated_avoided_frontier_provider_usage
        ),
        estimated_avoided_recursive_escalation=(frame.estimated_avoided_recursive_escalation),
        estimated_avoided_provider_instability=(frame.estimated_avoided_provider_instability),
    )


def audit_reflective_evaluation() -> ReflectiveEvaluationAuditReport:
    frame = ReflectiveEvaluationRuntime().evaluate()
    return ReflectiveEvaluationAuditReport(
        reflective_evaluation_active=frame.reflective_evaluation_active,
        execution_quality_score=frame.execution_quality_score,
        cognitive_coherence_score=frame.cognitive_coherence_score,
        continuation_validity_score=frame.continuation_validity_score,
        planning_integrity_score=frame.planning_integrity_score,
        estimated_avoided_recursive_reflection=(frame.estimated_avoided_recursive_reflection),
        estimated_avoided_self_optimization=frame.estimated_avoided_self_optimization,
        estimated_avoided_frontier_evaluation=(frame.estimated_avoided_frontier_evaluation),
    )


def audit_runtime_mediation() -> RuntimeMediationAuditReport:
    frame = ExecutionSequencer().mediate()
    return RuntimeMediationAuditReport(
        runtime_mediation_active=frame.runtime_mediation_active,
        execution_sequencer_active=frame.execution_sequencer_active,
        retry_governance_active=frame.retry_governance_active,
        cooldown_governance_active=frame.cooldown_governance_active,
        execution_arbitration_active=frame.execution_arbitration_active,
        estimated_avoided_recursive_execution=frame.estimated_avoided_recursive_execution,
        estimated_avoided_retry_amplification=frame.estimated_avoided_retry_amplification,
        estimated_avoided_execution_saturation=frame.estimated_avoided_execution_saturation,
    )


def audit_local_provider() -> LocalProviderAuditReport:
    frame = LocalProviderRuntime().evaluate()
    return LocalProviderAuditReport(
        local_provider_active=frame.local_provider_active,
        ollama_provider_active=frame.ollama_provider_active,
        local_provider_health=frame.local_provider_health,
        local_provider_budget=frame.local_provider_budget,
        local_provider_fallback=frame.local_provider_fallback,
        estimated_avoided_premium_tokens=frame.estimated_avoided_premium_tokens,
        estimated_local_execution_ratio=frame.estimated_local_execution_ratio,
        routing_distribution=frame.routing.routing_distribution,
        primary_coding_model=frame.capability.primary_coding_model,
        governance_compression_model=frame.capability.governance_compression_model,
        fallback_coding_model=frame.capability.fallback_coding_model,
        primary_model_gpu_operational=frame.health.primary_model_gpu_operational,
        fallback_model_operational=frame.health.fallback_model_operational,
        qwen_coder_14b_coding=frame.capability.qwen_coder_14b_coding,
        qwen_coder_14b_summaries=frame.capability.qwen_coder_14b_summaries,
        qwen_coder_14b_architecture=frame.capability.qwen_coder_14b_architecture,
        qwen_coder_14b_governance=frame.capability.qwen_coder_14b_governance,
        gemma3_12b_compression=frame.capability.gemma3_12b_compression,
        gemma3_12b_governance_summaries=frame.capability.gemma3_12b_governance_summaries,
        gemma3_12b_coding=frame.capability.gemma3_12b_coding,
        low_execution_provider=frame.routing.low_execution_provider,
        governance_compression_provider=frame.routing.governance_compression_provider,
        high_provider=frame.routing.high_provider,
        compact_prompts_required=frame.budget.compact_prompts_required,
        local_patch_only=frame.budget.local_patch_only,
        adjacent_runtime_retrieval_only="adjacent_runtime_retrieval_only" in frame.constraints,
        bounded_context_windows=frame.budget.bounded_context_windows,
        no_repo_wide_local_reasoning=frame.no_repo_wide_local_reasoning,
        no_giant_continuity_replay=frame.no_giant_continuity_replay,
        no_recursive_local_execution=frame.no_recursive_local_execution,
        no_hidden_autonomous_loops=frame.no_hidden_autonomous_loops,
        no_unrestricted_repository_mutation=frame.no_unrestricted_repository_mutation,
        human_confirmed_execution_authority=frame.budget.human_confirmed_execution_authority,
    )


def audit_subagent_execution() -> SubagentExecutionAuditReport:
    frame = SubagentExecutionRuntime().evaluate()
    return SubagentExecutionAuditReport(
        subagent_execution_active=frame.subagent_execution_active,
        subagent_routing_active=frame.subagent_routing_active,
        subagent_payload_active=frame.subagent_payload_active,
        subagent_validation_active=frame.subagent_validation_active,
        subagent_fallback_active=frame.subagent_fallback_active,
        subagent_governance_active=frame.subagent_governance_active,
        subagent_scope_active=frame.subagent_scope_active,
        subagent_eviction_active=frame.subagent_eviction_active,
        estimated_avoided_premium_subagent_tokens=(
            frame.estimated_avoided_premium_subagent_tokens
        ),
        estimated_avoided_recursive_agent_explosion=(
            frame.estimated_avoided_recursive_agent_explosion
        ),
        provider_routing_distribution=frame.routing.provider_routing_distribution,
        local_subagent_routing_result=frame.routing.low_local_provider,
        low_governance_routing_result=frame.routing.low_governance_provider,
        medium_routing_result=frame.routing.medium_provider,
        high_routing_result=frame.routing.high_provider,
        fallback_activation_summary=frame.fallback.active_fallback_provider,
        delegated_cognition_pressure=frame.pressure.delegated_cognition_pressure,
        swarm_pressure=frame.pressure.swarm_pressure,
        local_only_for_low_local=frame.local_only_for_low_local,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        bounded_delegation_only=frame.bounded_delegation_only,
        human_confirmed_delegation_only=frame.human_confirmed_delegation_only,
        no_autonomous_agent_swarms=frame.no_autonomous_agent_swarms,
        no_recursive_subagent_spawning=frame.no_recursive_subagent_spawning,
        no_hidden_provider_switching=frame.no_hidden_provider_switching,
        no_repo_wide_delegated_cognition=frame.no_repo_wide_delegated_cognition,
        no_autonomous_repository_mutation=frame.no_autonomous_repository_mutation,
    )


def audit_dev_execution() -> DevExecutionAuditReport:
    frame = DevelopmentExecutionRuntime().evaluate()
    return DevExecutionAuditReport(
        dev_execution_active=frame.dev_execution_active,
        execution_plan_active=frame.execution_plan_active,
        execution_checkpoint_active=frame.execution_checkpoint_active,
        execution_validation_active=frame.execution_validation_active,
        execution_rollback_active=frame.execution_rollback_active,
        execution_pacing_active=frame.execution_pacing_active,
        execution_scope_active=frame.execution_scope_active,
        execution_failure_active=frame.execution_failure_active,
        execution_eviction_active=frame.execution_eviction_active,
        estimated_avoided_execution_overhead=frame.estimated_avoided_execution_overhead,
        estimated_avoided_execution_explosion=frame.estimated_avoided_execution_explosion,
        provider_routing_distribution=frame.provider_routing_distribution,
        execution_pressure=frame.pressure.execution_pressure,
        validation_pressure=frame.pressure.validation_pressure,
        rollback_pressure=frame.pressure.rollback_pressure,
        pacing_pressure=frame.pressure.pacing_pressure,
        scope_pressure=frame.pressure.scope_pressure,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        bounded_execution_only=frame.bounded_execution_only,
        human_confirmed_execution_only=frame.human_confirmed_execution_only,
        no_autonomous_coding_authority=frame.no_autonomous_coding_authority,
        no_hidden_repository_mutation=frame.no_hidden_repository_mutation,
        no_recursive_execution_expansion=frame.no_recursive_execution_expansion,
        no_giant_execution_replay=frame.no_giant_execution_replay,
        no_validation_bypass=frame.no_validation_bypass,
        compact_pressure_warnings=frame.pressure.compact_pressure_warnings,
    )


def audit_dev_loop() -> DevLoopAuditReport:
    frame = SprintDevLoopRuntime().evaluate(
        objective_seed="AI Development Loop Runtime",
        lifecycle_state="VALIDATING",
        validation_passed=True,
        sprint_age_days=16,
        continuity_tokens=4_200,
        stale_sprints=("sprint-39", "sprint-40"),
    )
    return DevLoopAuditReport(
        dev_loop_active=frame.dev_loop_active,
        sprint_planning_active=frame.planning.no_repo_wide_sprint_synthesis
        and frame.planning.local_patch_recommendation,
        sprint_lifecycle_active=frame.lifecycle.bounded_transition,
        sprint_rollover_active=frame.rollover.rollover_ready
        and frame.rollover.infinite_sprint_chaining_prevented,
        sprint_bootstrap_active=frame.bootstrap.enter_only_continuation_workflow
        and frame.bootstrap.bounded_bootstrap_payload,
        sprint_governance_active=frame.governance.human_confirmed_orchestration_only,
        estimated_avoided_manual_orchestration_tokens=(
            frame.estimated_avoided_manual_orchestration_tokens
        ),
        estimated_avoided_sprint_explosion=frame.estimated_avoided_sprint_explosion,
        provider_routing_distribution=frame.provider_routing_distribution,
        local_patch_required=frame.scope.local_patch_required,
        bounded_cognition_only=frame.bounded_cognition_only,
        human_confirmed_orchestration_only=frame.human_confirmed_orchestration_only,
        no_autonomous_roadmap_expansion=frame.no_autonomous_roadmap_expansion,
        no_hidden_provider_switching=frame.no_hidden_provider_switching,
        no_giant_continuity_replay=frame.no_giant_continuity_replay,
        compact_bootstrap_payload=frame.bootstrap.bounded_bootstrap_payload,
        lifecycle_state=frame.lifecycle.lifecycle_state,
        compact_governance_warnings=frame.governance.compact_governance_warnings,
    )


def audit_sprint_memory() -> SprintMemoryAuditReport:
    frame = SprintMemoryRuntime().evaluate()
    memory_pressure = frame.governance_patterns.sprint_pressure_trend
    return SprintMemoryAuditReport(
        sprint_memory_active=frame.sprint_memory_active,
        sprint_pattern_active=frame.sprint_pattern_active,
        sprint_outcome_active=frame.sprint_outcome_active,
        sprint_provider_pattern_active=frame.sprint_provider_pattern_active,
        sprint_retrieval_pattern_active=frame.sprint_retrieval_pattern_active,
        sprint_governance_pattern_active=frame.sprint_governance_pattern_active,
        sprint_compression_active=frame.sprint_compression_active,
        sprint_eviction_active=frame.sprint_eviction_active,
        estimated_avoided_manual_sprint_analysis=(frame.estimated_avoided_manual_sprint_analysis),
        estimated_avoided_repeated_sprint_failures=(
            frame.estimated_avoided_repeated_sprint_failures
        ),
        provider_routing_distribution=frame.provider_routing_distribution,
        memory_pressure=memory_pressure,
        pattern_stable=frame.governance_patterns.sprint_stability == "STABLE",
        memory_eviction_required=bool(
            frame.eviction.evicted_stale_sprint_memory
            or frame.eviction.evicted_oversized_sprint_memory
            or frame.eviction.evicted_redundant_sprint_patterns
        ),
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        bounded_memory_only=frame.bounded_memory_only,
        no_hidden_long_term_cognition=frame.no_hidden_long_term_cognition,
        no_autonomous_roadmap_learning=frame.no_autonomous_roadmap_learning,
        no_hidden_provider_switching=frame.no_hidden_provider_switching,
        compact_governance_warnings=frame.governance_patterns.compact_governance_warnings,
    )


def audit_dev_strategy() -> DevStrategyAuditReport:
    frame = DevelopmentStrategyRuntime().evaluate()
    return DevStrategyAuditReport(
        dev_strategy_active=frame.dev_strategy_active,
        strategy_priority_active=frame.strategy_priority_active,
        cost_reduction_strategy_active=frame.cost_reduction_strategy_active,
        governance_stability_strategy_active=frame.governance_stability_strategy_active,
        provider_efficiency_strategy_active=frame.provider_efficiency_strategy_active,
        sprint_density_strategy_active=frame.sprint_density_strategy_active,
        embodiment_focus_strategy_active=frame.embodiment_focus_strategy_active,
        strategy_eviction_active=frame.strategy_eviction_active,
        estimated_avoided_strategy_overhead=frame.estimated_avoided_strategy_overhead,
        estimated_avoided_roadmap_explosion=frame.estimated_avoided_roadmap_explosion,
        provider_routing_distribution=frame.provider_routing_distribution,
        strategy_pressure=frame.pressure.strategy_pressure,
        cost_pressure=frame.pressure.cost_pressure,
        roadmap_pressure=frame.pressure.roadmap_pressure,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        bounded_strategy_only=frame.bounded_strategy_only,
        human_confirmed_strategy_only=frame.human_confirmed_strategy_only,
        no_autonomous_roadmap_generation=frame.no_autonomous_roadmap_generation,
        no_recursive_future_sprint_synthesis=frame.no_recursive_future_sprint_synthesis,
        no_hidden_provider_switching=frame.no_hidden_provider_switching,
        no_giant_strategic_replay=frame.no_giant_strategic_replay,
        compact_pressure_warnings=frame.pressure.compact_pressure_warnings,
    )


def audit_dev_policy() -> DevPolicyAuditReport:
    frame = DevelopmentPolicyRuntime().evaluate()
    return DevPolicyAuditReport(
        dev_policy_active=frame.dev_policy_active,
        architecture_policy_active=frame.architecture_policy_active,
        embodiment_realism_policy_active=frame.embodiment_realism_policy_active,
        provider_escalation_policy_active=frame.provider_escalation_policy_active,
        bounded_cognition_policy_active=frame.bounded_cognition_policy_active,
        anti_explosion_policy_active=frame.anti_explosion_policy_active,
        rollout_safety_policy_active=frame.rollout_safety_policy_active,
        policy_eviction_active=frame.policy_eviction_active,
        estimated_avoided_policy_overhead=frame.estimated_avoided_policy_overhead,
        estimated_avoided_governance_explosion=frame.estimated_avoided_governance_explosion,
        provider_routing_distribution=frame.provider_routing_distribution,
        policy_pressure=frame.pressure.policy_pressure,
        governance_pressure=frame.pressure.governance_pressure,
        escalation_pressure=frame.pressure.escalation_pressure,
        realism_pressure=frame.pressure.realism_pressure,
        local_only=frame.local_only,
        deterministic=frame.deterministic,
        summary_only=frame.summary_only,
        bounded_policy_only=frame.bounded_policy_only,
        human_confirmed_governance_only=frame.human_confirmed_governance_only,
        no_autonomous_enforcement=frame.no_autonomous_enforcement,
        no_repository_mutation_authority=frame.no_repository_mutation_authority,
        no_hidden_provider_switching=frame.no_hidden_provider_switching,
        no_recursive_governance_expansion=frame.no_recursive_governance_expansion,
        no_giant_policy_replay=frame.no_giant_policy_replay,
        compact_pressure_warnings=frame.pressure.compact_pressure_warnings,
    )


def _default_consumer_repo() -> Path:
    sibling = Path("..") / "AITuber"
    return sibling if sibling.exists() else Path(".")


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
        governance_health=audit_governance_health(),
        governance_trends=audit_governance_trends(),
        runtime_graph=audit_runtime_graph(),
        runtime_simplification=audit_runtime_simplification(),
        governance_core=audit_governance_core(),
        release_readiness=audit_release_readiness(),
        vscode_presence=audit_vscode_presence(),
        draft_injection=audit_draft_injection(),
        consumer_rollout=audit_consumer_rollout(),
        reasoning_routing=audit_reasoning_routing(),
        output_compression=audit_output_compression(),
        retrieval_budget=audit_retrieval_budget(),
        incremental_context=audit_incremental_context(),
        reasoning_scope=audit_reasoning_scope(),
        local_provider=audit_local_provider(),
        subagent_execution=audit_subagent_execution(),
        provider_routing=audit_provider_routing(),
        dev_execution=audit_dev_execution(),
        dev_loop=audit_dev_loop(),
        sprint_memory=audit_sprint_memory(),
        dev_strategy=audit_dev_strategy(),
        dev_policy=audit_dev_policy(),
        provider_experimental=audit_provider_experimental(),
        provider_stability=audit_provider_stability(),
        adaptive_provider_routing=audit_adaptive_provider_routing(),
        provider_fatigue=audit_provider_fatigue(),
        cognitive_memory_pressure=audit_cognitive_memory_pressure(),
        execution_continuation=audit_execution_continuation(),
        execution_saturation=audit_execution_saturation(),
        execution_recovery=audit_execution_recovery(),
        execution_coordination=audit_execution_coordination(),
        execution_intent=audit_execution_intent(),
        execution_session=audit_execution_session(),
        execution_stability=audit_execution_stability(),
        execution_quality=audit_execution_quality(),
        verified_execution=audit_verified_execution(),
        runtime_mediation=audit_runtime_mediation(),
        cognitive_state=audit_cognitive_state(),
        intentional_planning=audit_intentional_planning(),
        reflective_evaluation=audit_reflective_evaluation(),
        streaming_cognition=audit_streaming_cognition(),
        adaptive_provider=audit_adaptive_provider(),
        execution_memory=audit_execution_memory(),
        runtime_policy=audit_runtime_policy(),
        sprint_loop=audit_sprint_loop(),
        runtime_orchestrator=audit_runtime_orchestrator(),
        runtime_hardening=audit_runtime_hardening(),
        continuous_runtime_audit=audit_continuous_runtime_audit(),
        failure_injection=audit_failure_injection(),
        soak_stability=audit_soak_stability(),
        provider_cost_stabilization=audit_provider_cost_stabilization(),
        observation_review=audit_observation_review(),
        main_merge_qualification=audit_main_merge_qualification(),
        main_merge_rehearsal=audit_main_merge_rehearsal(),
        sprint_continuation=audit_sprint_continuation(),
    )


def main() -> int:
    report = run_runtime_enforcement_audit()
    print(json.dumps(report, default=lambda value: value.__dict__, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
