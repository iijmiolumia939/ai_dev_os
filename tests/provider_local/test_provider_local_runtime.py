from __future__ import annotations

from ai_dev_os.provider_local import LocalProviderRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_providerlocal_01_capability_metadata_matches_local_models() -> None:
    frame = LocalProviderRuntime().evaluate()

    assert frame.capability.primary_coding_model == "qwen2.5-coder:14b"
    assert frame.capability.qwen_coder_14b_coding is True
    assert frame.capability.qwen_coder_14b_summaries is True
    assert frame.capability.qwen_coder_14b_architecture is False
    assert frame.capability.qwen_coder_14b_governance is False
    assert frame.capability.gemma3_12b_compression is True
    assert frame.capability.gemma3_12b_governance_summaries is True
    assert frame.capability.gemma3_12b_coding == "limited"


def test_tc_providerlocal_02_ollama_health_and_budget_are_bounded() -> None:
    frame = LocalProviderRuntime().evaluate()

    assert frame.local_provider_active is True
    assert frame.ollama_provider_active is True
    assert frame.local_provider_health == "DEGRADED_FALLBACK_READY"
    assert frame.local_provider_budget == "LOCAL_BUDGET_OK"
    assert frame.health.primary_model_gpu_operational is False
    assert frame.health.fallback_model_operational is True
    assert frame.budget.compact_prompts_required is True
    assert frame.budget.local_patch_only is True
    assert frame.budget.bounded_context_windows is True
    assert frame.budget.human_confirmed_execution_authority is True


def test_tc_providerlocal_03_routing_distribution_preserves_premium_authority() -> None:
    frame = LocalProviderRuntime().evaluate()

    assert "repetitive_tests" in frame.routing.low_local_tasks
    assert "runtime_integration" in frame.routing.medium_routing_tasks
    assert "architecture" in frame.routing.high_cloud_tasks
    assert frame.routing.low_execution_provider == "ollama:qwen2.5-coder:7b"
    assert frame.routing.governance_compression_provider == "ollama:gemma3:12b"
    assert frame.routing.high_provider == "GPT-5.5 premium provider"
    assert frame.routing.local_has_no_architecture_authority is True
    assert frame.routing.local_has_no_governance_authority is True


def test_tc_providerlocal_04_constraints_block_local_execution_explosion() -> None:
    frame = LocalProviderRuntime().evaluate()

    assert frame.no_repo_wide_local_reasoning is True
    assert frame.no_giant_continuity_replay is True
    assert frame.no_recursive_local_execution is True
    assert frame.no_hidden_autonomous_loops is True
    assert frame.no_unrestricted_repository_mutation is True
    assert "adjacent_runtime_retrieval_only" in frame.constraints


def test_tc_providerlocal_05_runtime_audit_reports_local_provider() -> None:
    report = run_runtime_enforcement_audit().local_provider

    assert report.local_provider_active is True
    assert report.ollama_provider_active is True
    assert report.local_provider_health == "DEGRADED_FALLBACK_READY"
    assert report.local_provider_budget == "LOCAL_BUDGET_OK"
    assert report.local_provider_fallback.startswith("LIGHTWEIGHT")
    assert report.estimated_avoided_premium_tokens > 0
    assert report.estimated_local_execution_ratio > 0.5


def test_tc_providerlocal_06_runtime_is_deterministic() -> None:
    first = LocalProviderRuntime().evaluate()
    second = LocalProviderRuntime().evaluate()

    assert first == second
