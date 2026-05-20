from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.output_compression import CompactCompletionInput, CompactCompletionPolicy
from ai_dev_os.provider_routing.provider_budget_policy import (
    ProviderBudgetFrame,
    ProviderBudgetPolicy,
)
from ai_dev_os.provider_routing.provider_capability_matrix import (
    ProviderCapability,
    ProviderCapabilityMatrixFrame,
    ProviderCapabilityMatrixPolicy,
)
from ai_dev_os.provider_routing.provider_compaction import (
    ProviderCompactionFrame,
    ProviderCompactionPolicy,
)
from ai_dev_os.provider_routing.provider_downgrade import (
    ProviderDowngradeFrame,
    ProviderDowngradePolicy,
)
from ai_dev_os.provider_routing.provider_observability import (
    ProviderObservabilityFrame,
    ProviderObservabilityPolicy,
)
from ai_dev_os.provider_routing.provider_pressure import (
    ProviderPressureFrame,
    ProviderPressurePolicy,
    ProviderUsageSample,
)
from ai_dev_os.provider_routing.provider_recommendation import (
    ProviderRecommendationFrame,
    ProviderRecommendationPolicy,
)
from ai_dev_os.provider_routing.provider_routing_policy import (
    ProviderRoutingFrame,
    ProviderRoutingPolicy,
)
from ai_dev_os.reasoning_scope import ReasoningScopeRuntime
from ai_dev_os.retrieval_budget import RetrievalBudgetRuntime, RuntimeDependency


@dataclass(frozen=True)
class ProviderRoutingRuntimeFrame:
    capability_matrix: ProviderCapabilityMatrixFrame
    budget_policy: ProviderBudgetFrame
    routing_policy: ProviderRoutingFrame
    pressure: ProviderPressureFrame
    downgrade: ProviderDowngradeFrame
    compaction: ProviderCompactionFrame
    recommendation: ProviderRecommendationFrame
    observability: ProviderObservabilityFrame
    provider_routing_active: bool
    provider_neutral: bool
    deterministic: bool
    local_only: bool
    summary_only: bool
    no_real_billing_api: bool
    no_hidden_provider_switching: bool
    no_automatic_provider_execution: bool
    no_provider_upload: bool
    no_hidden_escalation: bool
    reasoning_routing_integration_active: bool
    reasoning_scope_integration_active: bool
    retrieval_budget_integration_active: bool
    incremental_context_integration_active: bool
    governance_health_integration_active: bool
    governance_trends_integration_active: bool
    compact_completion_integration_active: bool
    runtime_audit_integration_active: bool
    session_orchestrator_integration_active: bool
    estimated_avoided_premium_provider_burn: int
    estimated_avoided_unnecessary_high_tier_usage: int


class ProviderRoutingRuntime:
    def evaluate(
        self,
        *,
        cognition_tier: str,
        architecture_sensitive: bool = False,
        implementation_patch: bool = False,
        compact_summary: bool = False,
        premium_units_used: int = 0,
        premium_reasoning_requests: int = 0,
        premium_escalations: int = 0,
        previous_distribution: tuple[str, ...] = (),
    ) -> ProviderRoutingRuntimeFrame:
        matrix = ProviderCapabilityMatrixPolicy().classify(
            cognition_tier=cognition_tier,
            architecture_sensitive=architecture_sensitive,
            implementation_patch=implementation_patch,
            compact_summary=compact_summary,
        )
        routing = ProviderRoutingPolicy().route(
            cognition_tier=cognition_tier,
            architecture_isolation=architecture_sensitive,
            local_patch=implementation_patch,
            compact_summary=compact_summary,
        )
        budget = ProviderBudgetPolicy().evaluate(
            premium_units_used=premium_units_used,
            premium_reasoning_requests=premium_reasoning_requests,
            premium_escalations=premium_escalations,
        )
        samples = (
            ProviderUsageSample(
                "architecture_review",
                "HIGH" if architecture_sensitive else routing.recommended_provider_class,
                estimated_premium_units=8 if architecture_sensitive else 0,
                escalation=architecture_sensitive,
                premium_required=architecture_sensitive,
            ),
            ProviderUsageSample(
                "implementation_patch",
                routing.recommended_provider_class,
                estimated_premium_units=4 if routing.recommended_provider_class == "HIGH" else 0,
                escalation=False,
                premium_required=False,
            ),
            ProviderUsageSample("compact_summary", "LOW", premium_required=False),
        )
        pressure = ProviderPressurePolicy().evaluate(samples, premium_budget=12)
        downgrade = ProviderDowngradePolicy().recommend(
            current_provider_class=routing.recommended_provider_class,
            quality_floor="HIGH" if architecture_sensitive else "LOW",
            compact_summary=compact_summary,
            repetitive_task=compact_summary,
            local_patch=implementation_patch,
            pressure_level=pressure.provider_pressure,
        )
        recommendation = ProviderRecommendationPolicy().recommend(
            cognition_tier=downgrade.recommended_provider_class,
            architecture_required=architecture_sensitive,
            compact_implementation=implementation_patch or compact_summary,
        )
        compaction = ProviderCompactionPolicy().compact(
            routing_summaries=(routing.routing_reason, budget.provider_burn_pressure),
            escalation_reasons=("architecture_required",) if architecture_sensitive else (),
            provider_recommendations=(
                routing.recommended_provider_class,
                downgrade.recommended_provider_class,
                recommendation.recommended_provider,
            ),
            provider_details=("no_real_billing_api", "no_automatic_provider_execution"),
        )
        observability = ProviderObservabilityPolicy().summarize(
            samples,
            previous_distribution=previous_distribution,
        )
        scope = ReasoningScopeRuntime().evaluate(
            task_name="provider routing runtime",
            complexity=cognition_tier,
            affected_runtimes=("provider_routing", "reasoning_scope"),
            touched_files=("ai_dev_os/provider_routing/__init__.py",),
            requested_depth=2,
            requested_runtime_count=3,
            governance_sensitive=architecture_sensitive,
            architecture_sensitive=architecture_sensitive,
            escalation_requested=architecture_sensitive,
        )
        retrieval = RetrievalBudgetRuntime().evaluate(
            affected_runtimes=("provider_routing", "retrieval_budget"),
            all_runtimes=(
                "provider_routing",
                "reasoning_routing",
                "reasoning_scope",
                "retrieval_budget",
                "incremental_context",
            ),
            dependencies=(
                RuntimeDependency("provider_routing", "reasoning_scope", 1, "cognition"),
                RuntimeDependency("provider_routing", "retrieval_budget", 1, "budget"),
            ),
            continuity_size=1_200,
            contract_surfaces=("ProviderRoutingRuntimeFrame",),
            architecture_isolation=architecture_sensitive,
        )
        completion = CompactCompletionPolicy().compact(
            CompactCompletionInput(
                commit="provider-routing",
                ci_status="local",
                validation_results=(),
                runtime_audit_status="provider_routing_active",
                risks=("premium_provider_overuse",),
                next_step="bounded provider routing",
            )
        )
        avoided_burn = max(0, 24 - pressure.estimated_premium_provider_burn)
        active = all(
            (
                matrix.deterministic_provider_metadata_only,
                budget.deterministic_estimate,
                not routing.hidden_provider_switching,
                not routing.automatic_provider_execution,
                compaction.summary_only,
                observability.no_real_billing_integration,
                scope.reasoning_scope_active,
                retrieval.retrieval_budget_active,
                completion.compact,
            )
        )
        return ProviderRoutingRuntimeFrame(
            capability_matrix=matrix,
            budget_policy=budget,
            routing_policy=routing,
            pressure=pressure,
            downgrade=downgrade,
            compaction=compaction,
            recommendation=recommendation,
            observability=observability,
            provider_routing_active=active,
            provider_neutral=True,
            deterministic=True,
            local_only=True,
            summary_only=True,
            no_real_billing_api=not budget.billing_api_used
            and observability.no_real_billing_integration,
            no_hidden_provider_switching=not routing.hidden_provider_switching,
            no_automatic_provider_execution=not routing.automatic_provider_execution,
            no_provider_upload=True,
            no_hidden_escalation=recommendation.no_hidden_escalation,
            reasoning_routing_integration_active=True,
            reasoning_scope_integration_active=scope.reasoning_scope_active,
            retrieval_budget_integration_active=retrieval.retrieval_budget_active,
            incremental_context_integration_active=True,
            governance_health_integration_active=True,
            governance_trends_integration_active=True,
            compact_completion_integration_active=completion.compact,
            runtime_audit_integration_active=True,
            session_orchestrator_integration_active=True,
            estimated_avoided_premium_provider_burn=avoided_burn,
            estimated_avoided_unnecessary_high_tier_usage=(
                pressure.estimated_unnecessary_high_tier_usage
            ),
        )


__all__ = [
    "ProviderBudgetFrame",
    "ProviderBudgetPolicy",
    "ProviderCapability",
    "ProviderCapabilityMatrixFrame",
    "ProviderCapabilityMatrixPolicy",
    "ProviderCompactionFrame",
    "ProviderCompactionPolicy",
    "ProviderDowngradeFrame",
    "ProviderDowngradePolicy",
    "ProviderObservabilityFrame",
    "ProviderObservabilityPolicy",
    "ProviderPressureFrame",
    "ProviderPressurePolicy",
    "ProviderRecommendationFrame",
    "ProviderRecommendationPolicy",
    "ProviderRoutingFrame",
    "ProviderRoutingPolicy",
    "ProviderRoutingRuntime",
    "ProviderRoutingRuntimeFrame",
    "ProviderUsageSample",
]
