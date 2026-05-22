from __future__ import annotations

from ai_dev_os.provider_experimental import ProviderExperimentalRuntime


def test_tc_providercomparison_01_comparison_is_deterministic_and_non_executing() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.comparison.provider_comparison_active is True
    assert frame.comparison.compact_benchmark_summaries_only is True
    assert frame.comparison.no_real_provider_execution is True
    assert frame.comparison.no_hidden_provider_switching is True
    assert frame.comparison.no_provider_upload is True
    assert frame.comparison.deterministic_scoring_only is True
    assert set(frame.comparison.metrics) == {
        "token efficiency",
        "output stability",
        "governance adherence",
        "LOCAL_PATCH compliance",
        "compactness",
        "runtime drift",
        "hallucination rate",
        "repetitive reliability",
        "recursive reasoning tendency",
    }


def test_tc_providercomparison_02_drift_risk_stays_guarded_without_model() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.drift.provider_drift_active is True
    assert frame.drift.recursive_reasoning_growth_blocked is True
    assert frame.drift.giant_synthesis_attempts_blocked is True
    assert frame.drift.hallucinated_architecture_expansion_blocked is True
    assert frame.drift.drift_risk == "LOW_NOT_LOADED"
    assert frame.summary.estimated_reasoning_depth_benefit == "unmeasured_model_unavailable"
    assert frame.summary.estimated_instability_risk == "low_until_model_loaded"


def test_tc_providercomparison_03_fallback_blocks_hidden_provider_switching() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.fallback.fallback_active is True
    assert frame.fallback.fallback_route == "qwen2.5-coder:7b"
    assert frame.fallback.no_hidden_provider_switching is True
    assert frame.comparison.no_hidden_provider_switching is True
    assert frame.comparison.no_real_provider_execution is True
