from __future__ import annotations

from ai_dev_os.provider_stability import ProviderStabilityRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_providerstability_01_baseline_is_bounded_and_placeholder_only() -> None:
    frame = ProviderStabilityRuntime().evaluate()

    assert frame.provider_stability_active is True
    assert frame.stability.openmythos_placeholder_only is True
    assert frame.stability.deterministic_workloads is True
    assert frame.stability.compact_prompts_only is True
    assert frame.stability.local_patch_discipline is True
    assert frame.stability.rollback_safe_evaluation is True
    assert "repo-wide synthesis" in frame.stability.blocked_behaviors
    assert "OpenMythos placeholder:not_loaded" in frame.stability.providers
    assert frame.benchmark.no_real_openmythos_execution is True
    assert frame.benchmark.no_hidden_provider_switching is True


def test_tc_providerstability_02_scores_are_deterministic_and_ranked() -> None:
    frame = ProviderStabilityRuntime().evaluate()

    assert frame.governance_decay.governance_adherence_score["qwen2.5-coder:7b"] == 96
    assert frame.benchmark.local_patch_adherence_score["qwen2.5-coder:7b"] == 97
    assert frame.compactness_retention.compactness_score["qwen2.5-coder:7b"] == 94
    assert frame.hallucination_pressure.drift_resistance_score["qwen2.5-coder:7b"] == 92
    assert frame.benchmark.repetitive_reliability_score["qwen2.5-coder:7b"] == 95
    assert frame.retrieval_radius.retrieval_discipline_score["qwen2.5-coder:7b"] == 96
    assert frame.governance_decay.governance_adherence_ranking[0] == "qwen2.5-coder:7b"
    assert frame.benchmark.local_patch_adherence_ranking[0] == "qwen2.5-coder:7b"
    assert frame.hallucination_pressure.drift_resistance_ranking[-1] == (
        "OpenMythos placeholder:not_loaded"
    )


def test_tc_providerstability_03_long_session_simulation_tracks_decay() -> None:
    frame = ProviderStabilityRuntime().evaluate()

    assert frame.long_session_drift_active is True
    assert frame.long_session_drift.simulated_rollovers == 6
    assert frame.long_session_drift.estimated_long_session_degradation["qwen2.5-coder:7b"] == 4
    assert frame.long_session_drift.estimated_long_session_degradation["GPT-5.5 reference"] == 18
    assert frame.long_session_drift.recursive_reasoning_tendency["qwen2.5-coder:7b"] == 5
    assert frame.estimated_recursive_drift_risk == "LOW_BASELINE_GUARDED"


def test_tc_providerstability_04_runtime_audit_exposes_stability_flags() -> None:
    report = run_runtime_enforcement_audit().provider_stability

    assert report.provider_stability_active is True
    assert report.long_session_drift_active is True
    assert report.governance_decay_active is True
    assert report.compactness_retention_active is True
    assert report.retrieval_radius_active is True
    assert report.hallucination_pressure_active is True
    assert report.stability_benchmark_active is True
    assert report.estimated_provider_stability_gain == 12
    assert report.estimated_recursive_drift_risk == "LOW_BASELINE_GUARDED"
    assert report.openmythos_placeholder_only is True
    assert report.no_real_openmythos_execution is True
    assert report.no_hidden_provider_switching is True
