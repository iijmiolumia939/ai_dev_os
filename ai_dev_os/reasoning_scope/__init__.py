from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.reasoning_scope.architecture_reasoning_guard import (
    ArchitectureReasoningGuardFrame,
    ArchitectureReasoningGuardPolicy,
)
from ai_dev_os.reasoning_scope.local_patch_mode import LocalPatchModeFrame, LocalPatchModePolicy
from ai_dev_os.reasoning_scope.reasoning_compaction import (
    ReasoningCompactionFrame,
    ReasoningCompactionPolicy,
)
from ai_dev_os.reasoning_scope.reasoning_depth import ReasoningDepthFrame, ReasoningDepthPolicy
from ai_dev_os.reasoning_scope.reasoning_pressure import (
    ReasoningPressureFrame,
    ReasoningPressurePolicy,
)
from ai_dev_os.reasoning_scope.reasoning_recommendation import (
    ReasoningRecommendationFrame,
    ReasoningRecommendationPolicy,
)
from ai_dev_os.reasoning_scope.reasoning_scope import ReasoningScopeFrame, ReasoningScopePolicy


@dataclass(frozen=True)
class ReasoningScopeRuntimeFrame:
    reasoning_scope: ReasoningScopeFrame
    reasoning_depth: ReasoningDepthFrame
    architecture_guard: ArchitectureReasoningGuardFrame
    local_patch_mode: LocalPatchModeFrame
    reasoning_pressure: ReasoningPressureFrame
    reasoning_compaction: ReasoningCompactionFrame
    reasoning_recommendation: ReasoningRecommendationFrame
    reasoning_scope_active: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_cognition_only: bool
    no_hidden_chain_of_thought_persistence: bool
    no_ast_replay: bool
    no_hidden_provider_routing: bool
    no_automatic_architecture_escalation: bool
    no_automatic_roadmap_synthesis: bool
    estimated_avoided_premium_reasoning_burn: int
    estimated_avoided_unnecessary_architecture_reasoning: int


class ReasoningScopeRuntime:
    def evaluate(
        self,
        *,
        task_name: str,
        complexity: str,
        affected_runtimes: tuple[str, ...],
        touched_files: tuple[str, ...] = (),
        adjacent_contracts: tuple[str, ...] = (),
        requested_depth: int = 1,
        requested_runtime_count: int | None = None,
        repeated_architecture_sections: int = 0,
        governance_sensitive: bool = False,
        architecture_sensitive: bool = False,
        continuity_size: int = 0,
        escalation_requested: bool = False,
    ) -> ReasoningScopeRuntimeFrame:
        runtime_count = requested_runtime_count or len(affected_runtimes)
        depth = ReasoningDepthPolicy().cap(
            complexity=complexity,
            affected_runtimes=affected_runtimes,
            governance_sensitive=governance_sensitive,
        )
        guard = ArchitectureReasoningGuardPolicy().guard(
            complexity=depth.complexity,
            requested_runtime_count=runtime_count,
            continuity_size=continuity_size,
            governance_sensitive=governance_sensitive,
        )
        local_patch = LocalPatchModePolicy().scope(
            touched_files=touched_files,
            affected_runtimes=affected_runtimes,
            adjacent_contracts=adjacent_contracts,
        )
        scope = ReasoningScopePolicy().scope(
            depth=depth,
            guard=guard,
            local_patch=local_patch,
            affected_runtimes=affected_runtimes,
        )
        pressure = ReasoningPressurePolicy().evaluate(
            requested_depth=requested_depth,
            depth_cap=depth.reasoning_depth_cap,
            requested_runtime_count=runtime_count,
            neighborhood_cap=depth.maximum_reasoning_neighborhood,
            repeated_architecture_sections=repeated_architecture_sections,
            escalation_requested=escalation_requested,
        )
        compaction = ReasoningCompactionPolicy().compact(
            reasoning_summaries=(
                f"task:{task_name}",
                f"complexity:{depth.complexity}",
                f"scope:{','.join(scope.task_local_cognition_scope)}",
            ),
            escalation_explanations=depth.escalation_boundary_metadata,
            governance_reasoning=(
                ("governance_suppressed",) if guard.governance_escalation_suppression else ()
            ),
            deep_details=("deep reasoning details withheld until HIGH scope",),
            deep_details_required=depth.complexity == "HIGH",
        )
        recommendation = ReasoningRecommendationPolicy().recommend(
            complexity=depth.complexity,
            pressure=pressure,
            architecture_sensitive=architecture_sensitive,
        )
        active = all(
            (
                scope.bounded_reasoning_depth,
                local_patch.local_runtime_only_reasoning,
                guard.no_automatic_architecture_escalation,
                compaction.summary_only,
                recommendation.premium_reasoning_avoidance_recommendation
                or depth.compact_reasoning_recommendation,
            )
        )
        return ReasoningScopeRuntimeFrame(
            reasoning_scope=scope,
            reasoning_depth=depth,
            architecture_guard=guard,
            local_patch_mode=local_patch,
            reasoning_pressure=pressure,
            reasoning_compaction=compaction,
            reasoning_recommendation=recommendation,
            reasoning_scope_active=active,
            local_only=True,
            deterministic=True,
            summary_only=True,
            bounded_cognition_only=scope.bounded_cognition_only,
            no_hidden_chain_of_thought_persistence=True,
            no_ast_replay=True,
            no_hidden_provider_routing=True,
            no_automatic_architecture_escalation=guard.no_automatic_architecture_escalation,
            no_automatic_roadmap_synthesis=guard.no_automatic_roadmap_synthesis,
            estimated_avoided_premium_reasoning_burn=(pressure.estimated_premium_reasoning_burn),
            estimated_avoided_unnecessary_architecture_reasoning=(
                pressure.estimated_unnecessary_architecture_reasoning
            ),
        )


__all__ = [
    "ArchitectureReasoningGuardFrame",
    "ArchitectureReasoningGuardPolicy",
    "LocalPatchModeFrame",
    "LocalPatchModePolicy",
    "ReasoningCompactionFrame",
    "ReasoningCompactionPolicy",
    "ReasoningDepthFrame",
    "ReasoningDepthPolicy",
    "ReasoningPressureFrame",
    "ReasoningPressurePolicy",
    "ReasoningRecommendationFrame",
    "ReasoningRecommendationPolicy",
    "ReasoningScopeFrame",
    "ReasoningScopePolicy",
    "ReasoningScopeRuntime",
    "ReasoningScopeRuntimeFrame",
]
