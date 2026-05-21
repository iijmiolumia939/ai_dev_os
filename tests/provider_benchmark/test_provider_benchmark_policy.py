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
