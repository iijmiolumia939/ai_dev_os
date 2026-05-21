from __future__ import annotations

from ai_dev_os.sprint_memory import SprintMemoryRuntime, SprintMemorySample


def test_tc_sprintmemory_04_failure_patterns_generate_bounded_recommendations() -> None:
    frame = SprintMemoryRuntime().evaluate()
    failure = frame.failure_patterns

    assert failure.repeated_sprint_explosion is True
    assert failure.repeated_provider_escalation is False
    assert failure.repeated_giant_retrieval is True
    assert failure.repeated_repo_wide_reasoning is True
    assert failure.repeated_continuity_accumulation is True
    assert failure.unstable_sprint_rollover is True
    assert "LOCAL_PATCH_REQUIRED" in failure.local_patch_reminders
    assert "avoid_HIGH_for_repetitive_memory" in failure.provider_downgrade_hints


def test_tc_sprintmemory_05_provider_patterns_track_distribution_and_downgrade_hints() -> None:
    frame = SprintMemoryRuntime().evaluate()
    provider = frame.provider_patterns

    assert provider.provider_usage_distribution == {"HIGH": 1, "MEDIUM": 1, "LOW": 2}
    assert provider.successful_low_medium_routing is True
    assert provider.sprint_provider_efficiency in {"HIGH", "MEDIUM"}
    assert "LOW_for_cleanup" in provider.compact_provider_recommendations
    assert "compact_summary_to_LOW" in provider.downgrade_safe_suggestions
    assert provider.no_hidden_provider_switching is True


def test_tc_sprintmemory_06_retrieval_patterns_are_adjacent_and_delta_only() -> None:
    samples = (
        SprintMemorySample("s1", "LOW", 1, True, True, True, True, continuity_tokens=800),
        SprintMemorySample("s2", "MEDIUM", 2, True, True, True, True, continuity_tokens=900),
    )
    frame = SprintMemoryRuntime().evaluate(samples)
    retrieval = frame.retrieval_patterns

    assert retrieval.retrieval_radius == 2
    assert retrieval.repo_wide_cognition_frequency == 0
    assert retrieval.adjacent_runtime_success is True
    assert retrieval.retrieval_explosion_attempts == 0
    assert retrieval.continuity_size_trend == "LOW"
    assert "adjacent_runtime_retrieval_only" in retrieval.bounded_retrieval_reminders
    assert "delta_only_memory_carryover" in retrieval.delta_only_reminders
