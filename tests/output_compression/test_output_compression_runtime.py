from __future__ import annotations

from ai_dev_os.output_compression import (
    CompactCompletionInput,
    CompactCompletionPolicy,
    SummaryDeduplicationPolicy,
    SummarySection,
    ValidationCompactionPolicy,
    ValidationResult,
)


def test_tc_compact_01_compact_completion_validation() -> None:
    frame = CompactCompletionPolicy().compact(
        CompactCompletionInput(
            commit="abc123",
            ci_status="success",
            validation_results=(ValidationResult("pytest", "pass", 289),),
            runtime_audit_status="active",
            risks=("remaining cost risk", "verbosity drift"),
            next_step="summary deduplication",
            rollout_summary="unchanged rollout summary",
            unchanged_sections=("rollout",),
        )
    )

    assert frame.compact is True
    assert frame.bounded is True
    assert frame.expandable is True
    assert frame.human_readable is True
    assert frame.rollback_safe is True
    assert frame.deterministic_compact_mode is True
    assert "Commit: abc123" in frame.compact_summary
    assert "Validation: pass (289 passed total)" in frame.compact_summary
    assert "Risks: 2" in frame.compact_summary


def test_tc_compact_02_summary_deduplication_validation() -> None:
    frame = SummaryDeduplicationPolicy().deduplicate(
        (
            SummarySection("validation pass", "pytest passed"),
            SummarySection("validation pass", "pytest passed"),
            SummarySection("clean worktree", "clean", unchanged=True),
            SummarySection("CI success", "success", unchanged=True),
        )
    )

    assert frame.repeated_summary_detected is True
    assert frame.duplicate_section_collapse is True
    assert frame.unchanged_section_suppression is True
    assert frame.compact_references
    assert frame.estimated_avoided_repeated_tokens > 0
    assert frame.expandable is True


def test_tc_compact_03_validation_compaction_validation() -> None:
    frame = ValidationCompactionPolicy().compact(
        (
            ValidationResult("pytest tests/x", "pass", 11),
            ValidationResult("pytest tests/y", "pass", 8),
            ValidationResult("runtime audit", "pass", 1),
        )
    )

    assert frame.validation_aggregation is True
    assert frame.compact_validation_projection == "Validation: pass (20 passed total)"
    assert len(frame.expandable_details) == 3
    assert frame.runtime_audit_active is True
    assert frame.deterministic is True


def test_tc_compact_05_compact_mode_is_deterministic() -> None:
    data = CompactCompletionInput(
        commit="abc123",
        ci_status="success",
        validation_results=(ValidationResult("pytest", "pass", 289),),
        runtime_audit_status="active",
        risks=("verbosity drift",),
        next_step="bounded reporting",
    )

    first = CompactCompletionPolicy().compact(data)
    second = CompactCompletionPolicy().compact(data)

    assert first == second
    assert first.deterministic_compact_mode is True
