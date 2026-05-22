from __future__ import annotations

from ai_dev_os.provider_experimental import ProviderExperimentalRuntime


def test_tc_providerbenchmark_01_uses_identical_bounded_tasks_for_all_providers() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.benchmark.max_tasks_per_provider == len(frame.benchmark.tasks)
    assert frame.benchmark.tasks == (
        "compact dataclass generation",
        "runtime frame generation",
        "repetitive tests",
        "compact sprint summaries",
        "LOCAL_PATCH runtime integration",
        "bounded validation summaries",
    )
    assert frame.comparison.providers == (
        "openmythos:experimental",
        "qwen2.5-coder:7b",
        "qwen2.5-coder:14b",
        "gemma3:12b",
        "GPT-5.5 baseline",
    )


def test_tc_providerbenchmark_02_retains_compact_summaries_only() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.summary.provider_benchmark_summary_active is True
    assert frame.summary.summary_only is True
    assert frame.eviction.provider_benchmark_eviction_active is True
    assert frame.eviction.bounded_retention_limit == 5
    assert frame.eviction.evicts_raw_outputs is True
    assert frame.eviction.evicts_unbounded_context is True
    assert frame.eviction.compact_summary_retained is True


def test_tc_providerbenchmark_03_conversion_pipeline_uses_isolated_dependencies() -> None:
    frame = ProviderExperimentalRuntime().evaluate()

    assert frame.conversion.local_patch_only is True
    assert frame.conversion.isolated_dependencies_only is True
    assert frame.conversion.stable_runtime_dependencies_unchanged is True
    assert "transformers>=4.40,<5" in frame.conversion.dependencies
    assert "safetensors>=0.4,<1" in frame.conversion.dependencies
    assert "huggingface_hub>=0.23,<1" in frame.conversion.dependencies
    assert "llama.cpp convert_hf_to_gguf.py" in frame.conversion.conversion_tooling
    assert frame.model_validation.adjacent_runtime_retrieval_only is True
    assert frame.model_validation.compact_prompts_only is True
