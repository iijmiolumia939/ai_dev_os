from __future__ import annotations

from ai_dev_os.providers.cost_simulation import simulate_cost
from ai_dev_os.providers.fallback_simulation import simulate_fallback_chain
from ai_dev_os.providers.mock_provider import simulate_provider_request
from ai_dev_os.providers.provider_contracts import ProviderRequest
from ai_dev_os.providers.provider_telemetry import aggregate_provider_telemetry
from governance.budget_runtime import BudgetState


def provider_request(scenario: str = "success", tier: str = "tier2") -> ProviderRequest:
    return ProviderRequest(
        provider_name="mock-router",
        model_tier=tier,
        prompt_tokens=900,
        completion_tokens=220,
        retrieval_context_tokens=24_000,
        compressed_context_tokens=700,
        scenario=scenario,
    )


def test_fallback_chain_combines_budget_pressure_and_provider_failure() -> None:
    frame = simulate_fallback_chain(
        provider_request("timeout"),
        budget_state=BudgetState(100.0, 500.0, 1500.0, daily_spend=99.0),
    )

    assert frame.pressure == "HIGH"
    assert frame.tier2_disabled is True
    assert frame.local_fallback is True
    assert frame.retrieval_only_fallback is True
    assert frame.summary_only_fallback is True
    assert frame.patch_only_fallback is True
    assert frame.route_chain == (
        "mock-router",
        "tier2_disabled",
        "local_fallback",
        "retrieval_only",
        "summary_only",
        "patch_only",
    )


def test_provider_telemetry_aggregates_usage_cost_latency_and_failures() -> None:
    frames = (
        simulate_provider_request(provider_request("success", tier="tier0")),
        simulate_provider_request(provider_request("rate_limit", tier="tier1")),
        simulate_provider_request(provider_request("high_latency", tier="tier1")),
    )
    telemetry = aggregate_provider_telemetry(frames)

    assert telemetry.provider_usage_count == {"mock-router": 3}
    assert telemetry.tier_usage_distribution == {"tier0": 1, "tier1": 2}
    assert telemetry.token_burn_estimate == 3_360
    assert telemetry.cost_estimate > 0
    assert telemetry.latency_distribution["slow"] == 1
    assert telemetry.fallback_frequency == 1
    assert telemetry.failure_frequency == 1
    assert telemetry.retrieval_related_cost > 0
    assert telemetry.machine_readable_summary["fallback_frequency"] == 1


def test_cost_simulation_compares_before_after_retrieval_scaling() -> None:
    frame = simulate_cost(
        provider_request("success", tier="tier1"), fallback_used=True, retry_count=1
    )

    assert frame.before_retrieval_scaling == 25_120
    assert frame.after_retrieval_scaling == 1_820
    assert frame.token_burn_avoided == 23_300
    assert frame.estimated_savings_ratio > 0.9
    assert frame.fallback_penalty == 1.10
    assert frame.retry_penalty == 1.15


def test_summary_only_fallback_behavior_under_critical_pressure() -> None:
    frame = simulate_fallback_chain(
        provider_request("provider_error"),
        budget_state=BudgetState(100.0, 500.0, 1500.0, daily_spend=120.0),
    )

    assert frame.pressure == "CRITICAL"
    assert frame.route_chain[-1] == "patch_only"
    assert frame.summary_only_fallback is True
    assert frame.provider_frame.no_real_provider_call is True
