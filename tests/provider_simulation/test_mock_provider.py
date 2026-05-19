from __future__ import annotations

from ai_dev_os.providers.mock_provider import simulate_provider_request
from ai_dev_os.providers.provider_contracts import ProviderRequest


def request_for(scenario: str) -> ProviderRequest:
    return ProviderRequest(
        provider_name="mock-router",
        model_tier="tier1",
        prompt_tokens=500,
        completion_tokens=100,
        retrieval_context_tokens=8_000,
        compressed_context_tokens=800,
        scenario=scenario,
    )


def test_mock_provider_success_is_deterministic_and_local() -> None:
    first = simulate_provider_request(request_for("success"))
    second = simulate_provider_request(request_for("success"))

    assert first == second
    assert first.response.status == "success"
    assert first.response.fallback_used is False
    assert first.no_real_provider_call is True
    assert first.simulated_latency_ms == 120


def test_mock_provider_timeout_and_rate_limit_trigger_fallback() -> None:
    timeout = simulate_provider_request(request_for("timeout"))
    rate_limit = simulate_provider_request(request_for("rate_limit"))

    assert timeout.response.status == "timeout"
    assert timeout.simulated_failure is not None
    assert timeout.response.failure_reason == "PROVIDER_TIMEOUT"
    assert timeout.route_taken.route_taken == ("mock-router", "local_fallback")
    assert rate_limit.response.status == "rate_limit"
    assert rate_limit.response.failure_reason == "PROVIDER_RATE_LIMIT"
    assert rate_limit.usage.fallback_used is True


def test_mock_provider_cost_spike_and_degraded_response_are_observable() -> None:
    cost_spike = simulate_provider_request(request_for("cost_spike"))
    degraded = simulate_provider_request(request_for("degraded_response"))

    assert cost_spike.response.status == "cost_spike"
    assert (
        cost_spike.simulated_cost
        > simulate_provider_request(request_for("success")).simulated_cost
    )
    assert degraded.response.status == "degraded_response"
    assert degraded.response.content == "degraded mock response"
