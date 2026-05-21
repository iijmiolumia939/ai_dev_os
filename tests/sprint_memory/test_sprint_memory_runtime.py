from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.sprint_memory import (
    SPRINT_MEMORY_REQUIREMENT_IDS,
    SPRINT_MEMORY_TEST_IDS,
    SprintMemoryRuntime,
)


def test_tc_sprintmemory_01_memory_tracks_operational_patterns_only() -> None:
    frame = SprintMemoryRuntime().evaluate()

    assert "FR-SPRINTMEMORY-01" in SPRINT_MEMORY_REQUIREMENT_IDS
    assert "TC-SPRINTMEMORY-01" in SPRINT_MEMORY_TEST_IDS
    assert frame.sprint_memory_active is True
    assert frame.patterns.compact_operational_patterns_only is True
    assert frame.patterns.autonomous_roadmap_learning_forbidden is True
    assert frame.no_full_sprint_transcript_accumulation is True
    assert frame.no_hidden_long_term_cognition is True
    assert frame.no_autonomous_roadmap_learning is True


def test_tc_sprintmemory_02_outcome_and_efficiency_are_deterministic() -> None:
    frame = SprintMemoryRuntime().evaluate()

    assert frame.outcome.bounded_scoring_only is True
    assert frame.outcome.deterministic_metrics_only is True
    assert frame.outcome.validation_stability in {"LOW", "MEDIUM", "HIGH"}
    assert frame.outcome.ci_stability in {"LOW", "MEDIUM", "HIGH"}
    assert frame.efficiency.overall_efficiency_score > 0
    assert frame.efficiency.low_medium_success_detected is True
    assert frame.efficiency.local_patch_efficiency_detected is True


def test_tc_sprintmemory_03_runtime_audit_reports_sprint_memory_flags() -> None:
    report = run_runtime_enforcement_audit().sprint_memory

    assert report.sprint_memory_active is True
    assert report.sprint_pattern_active is True
    assert report.sprint_outcome_active is True
    assert report.sprint_provider_pattern_active is True
    assert report.sprint_retrieval_pattern_active is True
    assert report.sprint_governance_pattern_active is True
    assert report.sprint_compression_active is True
    assert report.sprint_eviction_active is True
    assert report.estimated_avoided_manual_sprint_analysis > 0
    assert report.estimated_avoided_repeated_sprint_failures > 0
