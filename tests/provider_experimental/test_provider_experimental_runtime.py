from __future__ import annotations

from ai_dev_os.provider_experimental import ProviderExperimentalRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_providerexperimental_01_openmythos_fallback_is_bounded() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.experimental_provider_active is True
    assert frame.openmythos_provider_active is False
    assert frame.openmythos.load_result == "unavailable:model_manifest_missing"
    assert frame.openmythos.vram_runtime_stability == "not_loaded"
    assert frame.openmythos.no_architecture_authority is True
    assert frame.openmythos.no_governance_authority is True
    assert frame.openmythos.no_anti_explosion_authority is True
    assert frame.openmythos.no_autonomous_execution_authority is True


def test_tc_providerexperimental_02_policy_prevents_unbounded_benchmarks() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.benchmark.provider_benchmark_active is True
    assert frame.benchmark.compact_prompts_only is True
    assert frame.benchmark.adjacent_runtime_only_retrieval is True
    assert frame.benchmark.deterministic_benchmark_tasks is True
    assert frame.benchmark.rollback_safe_evaluation_only is True
    assert frame.benchmark.recursive_benchmark_loops_forbidden is True
    assert frame.benchmark.unrestricted_prompts_forbidden is True
    assert frame.benchmark.repo_wide_evaluation_forbidden is True
    assert "repo-wide synthesis" in frame.benchmark.forbidden_tasks


def test_tc_providerexperimental_03_runtime_audit_reports_experimental_flags() -> None:
    report = run_runtime_enforcement_audit().provider_experimental

    assert report.experimental_provider_active is True
    assert report.openmythos_provider_active is False
    assert report.provider_benchmark_active is True
    assert report.provider_comparison_active is True
    assert report.provider_drift_active is True
    assert report.estimated_reasoning_depth_gain == 0
    assert report.estimated_governance_instability_risk == 2
    assert report.estimated_architecture_drift_risk == 2
