from __future__ import annotations

from ai_dev_os.provider_experimental import ProviderExperimentalRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_providerexperimental_01_openmythos_fallback_is_bounded() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.experimental_provider_active is True
    assert frame.openmythos_provider_active is False
    assert frame.openmythos.load_result == "unavailable:hf_repository_not_gguf"
    assert frame.openmythos.vram_runtime_stability == "not_loaded"
    assert frame.openmythos.no_architecture_authority is True
    assert frame.openmythos.no_governance_authority is True
    assert frame.openmythos.no_anti_explosion_authority is True
    assert frame.openmythos.no_autonomous_execution_authority is True


def test_tc_providerexperimental_04_openmythos_gguf_conversion_is_guarded() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.openmythos_loaded is False
    assert frame.openmythos_gguf_active is False
    assert frame.openmythos_conversion_active is True
    assert frame.gguf.direct_hf_repo == "maidacundo/open-mythos-hf"
    assert frame.gguf.weighted_hf_repo == "maidacundo/open-mythos-140m"
    assert frame.gguf.gguf_repository_found is False
    assert frame.gguf.llama_cpp_compatible is False
    assert frame.conversion.isolated_dependencies_only is True
    assert frame.conversion.stable_runtime_dependencies_unchanged is True
    assert frame.quantization.preferred_quantization == "Q4_K_M"
    assert frame.quantization.rtx3080_10gb_target is True
    assert frame.fallback.rollback_safe_fallback is True
    assert frame.fallback.no_production_routing_change is True


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
    assert report.openmythos_loaded is False
    assert report.openmythos_gguf_active is False
    assert report.openmythos_conversion_active is True
    assert report.openmythos_runtime_stability == "not_loaded"
    assert report.openmythos_drift_risk == "LOW_NOT_LOADED"
    assert report.openmythos_governance_adherence == "guards_preserved"
    assert report.openmythos_quantization == "Q4_K_M"
    assert report.openmythos_fallback_route == "qwen2.5-coder:7b"
    assert report.estimated_reasoning_depth_gain == 0
    assert report.estimated_governance_instability_risk == 2
    assert report.estimated_architecture_drift_risk == 2
