from __future__ import annotations

from ai_dev_os.provider_routing import ProviderRoutingRuntime
from ai_dev_os.provider_routing.provider_capability_matrix import ProviderCapabilityMatrixPolicy
from ai_dev_os.provider_routing.provider_compaction import ProviderCompactionPolicy
from ai_dev_os.provider_routing.provider_recommendation import ProviderRecommendationPolicy
from ai_dev_os.provider_routing.provider_routing_policy import ProviderRoutingPolicy
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_providerrouting_01_capability_matrix_is_safe_and_deterministic() -> None:
    frame = ProviderCapabilityMatrixPolicy().classify(
        cognition_tier="HIGH",
        architecture_sensitive=True,
    )

    assert frame.recommended_provider_class == "HIGH"
    assert frame.architecture_safe_provider_classification is True
    assert frame.implementation_safe_provider_classification is True
    assert frame.compact_summary_safe_provider_classification is True
    assert frame.deterministic_provider_metadata_only is True
    assert frame.provider_neutral is True


def test_tc_providerrouting_02_policy_routes_low_medium_high_classes() -> None:
    policy = ProviderRoutingPolicy()

    assert policy.route(cognition_tier="LOW").recommended_provider_class == "LOW"
    assert policy.route(cognition_tier="MEDIUM").recommended_provider_class == "MEDIUM"
    assert policy.route(cognition_tier="HIGH").recommended_provider_class == "HIGH"
    assert policy.route(cognition_tier="HIGH", local_patch=True).local_patch_routing is True


def test_tc_providerrouting_03_recommendations_preserve_premium_usage() -> None:
    policy = ProviderRecommendationPolicy()
    low = policy.recommend(cognition_tier="LOW")
    medium = policy.recommend(cognition_tier="MEDIUM")
    high = policy.recommend(cognition_tier="HIGH", architecture_required=True)

    assert low.gemini_for_low_recommendation is True
    assert medium.claude_for_medium_recommendation is True
    assert high.recommended_provider == "GPT-5.5 premium provider"
    assert high.gpt55_only_when_required is True
    assert low.premium_provider_preservation_recommendation is True


def test_tc_providerrouting_04_compaction_is_deduplicated_and_expandable() -> None:
    frame = ProviderCompactionPolicy().compact(
        routing_summaries=("LOW", "LOW", "MEDIUM"),
        escalation_reasons=("architecture", "architecture"),
        provider_recommendations=("Gemini", "Gemini", "Claude"),
        provider_details=("detail",),
    )

    assert frame.compact_provider_routing_summaries == ("LOW", "MEDIUM")
    assert frame.compact_escalation_reasons == ("architecture",)
    assert frame.deduplicated_provider_recommendations == ("Gemini", "Claude")
    assert frame.expandable_provider_details == ("detail",)
    assert frame.summary_only is True


def test_tc_providerrouting_05_runtime_is_local_summary_only_and_no_execution() -> None:
    frame = ProviderRoutingRuntime().evaluate(
        cognition_tier="MEDIUM",
        implementation_patch=True,
        compact_summary=True,
        premium_units_used=9,
        premium_reasoning_requests=2,
        premium_escalations=1,
    )

    assert frame.provider_routing_active is True
    assert frame.local_only is True
    assert frame.deterministic is True
    assert frame.summary_only is True
    assert frame.no_real_billing_api is True
    assert frame.no_hidden_provider_switching is True
    assert frame.no_automatic_provider_execution is True
    assert frame.no_provider_upload is True
    assert frame.no_hidden_escalation is True


def test_tc_providerrouting_06_runtime_integrates_existing_governance_surfaces() -> None:
    frame = ProviderRoutingRuntime().evaluate(cognition_tier="LOW", compact_summary=True)

    assert frame.reasoning_routing_integration_active is True
    assert frame.reasoning_scope_integration_active is True
    assert frame.retrieval_budget_integration_active is True
    assert frame.incremental_context_integration_active is True
    assert frame.governance_health_integration_active is True
    assert frame.governance_trends_integration_active is True
    assert frame.compact_completion_integration_active is True
    assert frame.runtime_audit_integration_active is True
    assert frame.session_orchestrator_integration_active is True
    assert frame.local_provider.local_provider_active is True
    assert frame.local_provider.routing.low_execution_provider == "ollama:qwen2.5-coder:7b"


def test_tc_providerrouting_07_runtime_audit_reports_provider_routing_flags() -> None:
    report = run_runtime_enforcement_audit().provider_routing

    assert report.provider_routing_active is True
    assert report.provider_capability_matrix_active is True
    assert report.provider_budget_policy_active is True
    assert report.provider_pressure_active is True
    assert report.provider_downgrade_active is True
    assert report.provider_observability_active is True
    assert report.estimated_avoided_premium_provider_burn > 0


def test_tc_providerrouting_08_runtime_is_deterministic() -> None:
    first = ProviderRoutingRuntime().evaluate(cognition_tier="LOW", compact_summary=True)
    second = ProviderRoutingRuntime().evaluate(cognition_tier="LOW", compact_summary=True)

    assert first == second
