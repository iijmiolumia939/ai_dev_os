from __future__ import annotations

from ai_dev_os.output_compression.report_density import ReportDensityPolicy


def test_tc_compact_04_verbosity_pressure_validation() -> None:
    frame = ReportDensityPolicy().audit(
        (
            "commit",
            "ci",
            "validation",
            "runtime audit",
            "risks",
            "next",
            "rollout",
            "artifact cleanup",
        ),
        unchanged_sections=5,
        repeated_token_estimate=240,
    )

    assert frame.section_count == 8
    assert frame.repeated_token_estimate == 240
    assert frame.unchanged_summary_ratio == 0.625
    assert frame.verbosity_pressure == "HIGH"
    assert frame.compaction_recommendation is True
    assert frame.estimated_avoided_completion_tokens > 0


def test_tc_compact_05_density_audit_is_deterministic() -> None:
    sections = ("commit", "ci", "validation")
    first = ReportDensityPolicy().audit(sections, unchanged_sections=1, repeated_token_estimate=20)
    second = ReportDensityPolicy().audit(
        sections, unchanged_sections=1, repeated_token_estimate=20
    )

    assert first == second
    assert first.deterministic is True
