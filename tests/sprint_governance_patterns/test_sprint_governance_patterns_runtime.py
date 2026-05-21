from __future__ import annotations

from ai_dev_os.sprint_memory import SprintMemoryRuntime


def test_tc_sprintmemory_07_governance_patterns_block_roadmap_learning() -> None:
    frame = SprintMemoryRuntime().evaluate()
    governance = frame.governance_patterns

    assert governance.sprint_pressure_trend in {"LOW", "MEDIUM", "HIGH"}
    assert governance.cognition_expansion_attempts == 1
    assert governance.roadmap_branching_attempts == 1
    assert governance.continuity_accumulation_trend == "MEDIUM"
    assert governance.sprint_stability == "UNSTABLE"
    assert "roadmap_branching_attempt" in governance.compact_governance_warnings
    assert governance.human_confirmed_orchestration_only is True


def test_tc_sprintmemory_08_compression_preserves_only_compact_heuristics() -> None:
    frame = SprintMemoryRuntime().evaluate()
    compression = frame.compression

    assert compression.summary_only is True
    assert compression.bounded_operational_heuristics
    assert "evict_stale_memory" in compression.bounded_operational_heuristics
    assert compression.giant_memory_accumulation_prevented is True
    assert compression.full_historical_replay_forbidden is True
    assert compression.hidden_cognition_expansion_forbidden is True
    assert len(compression.bounded_operational_heuristics) <= 5


def test_tc_sprintmemory_09_eviction_removes_stale_oversized_and_duplicate_memory() -> None:
    frame = SprintMemoryRuntime().evaluate()
    eviction = frame.eviction

    assert eviction.stale_memory_eviction_active is True
    assert eviction.bounded_memory_only is True
    assert eviction.evicted_oversized_sprint_memory == ("sprint-full-transcript",)
    assert eviction.evicted_redundant_sprint_patterns == (
        "duplicate-local-patch",
        "duplicate-local-patch",
    )
    assert "LOCAL_PATCH_REQUIRED" in eviction.preserved_compact_useful_heuristics
    assert "delta_only_memory" in eviction.preserved_compact_useful_heuristics


def test_tc_sprintmemory_10_runtime_is_local_deterministic_and_summary_only() -> None:
    first = SprintMemoryRuntime().evaluate()
    second = SprintMemoryRuntime().evaluate()

    assert first == second
    assert first.local_only is True
    assert first.deterministic is True
    assert first.summary_only is True
    assert first.bounded_memory_only is True
    assert first.no_hidden_provider_switching is True
    assert first.provider_routing_distribution == {"HIGH": 1, "MEDIUM": 1, "LOW": 2}
