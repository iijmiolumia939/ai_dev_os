from __future__ import annotations

from ai_dev_os.retrieval_budget.retrieval_pressure import RetrievalPressurePolicy


def test_tc_retrievalbudget_05_pressure_detects_explosion_and_burn() -> None:
    frame = RetrievalPressurePolicy().evaluate(
        selected_runtime_count=9,
        all_runtime_count=14,
        continuity_size=8_000,
        max_runtime_count=5,
        max_continuity_size=2_400,
        architecture_isolation=True,
    )

    assert frame.retrieval_explosion_detected is True
    assert frame.broad_architecture_leakage_detected is True
    assert frame.giant_continuity_retrieval_detected is True
    assert frame.estimated_hidden_input_token_burn > 0
    assert frame.retrieval_downgrade_recommendation is True
    assert frame.pressure_level == "HIGH"


def test_tc_retrievalbudget_06_pressure_is_deterministic_without_escalation() -> None:
    kwargs = dict(
        selected_runtime_count=2,
        all_runtime_count=8,
        continuity_size=1_200,
        max_runtime_count=5,
        max_continuity_size=2_400,
    )
    first = RetrievalPressurePolicy().evaluate(**kwargs)
    second = RetrievalPressurePolicy().evaluate(**kwargs)

    assert first == second
    assert first.pressure_level == "LOW"
    assert first.no_hidden_provider_routing is True
    assert first.no_automatic_retrieval_escalation is True
