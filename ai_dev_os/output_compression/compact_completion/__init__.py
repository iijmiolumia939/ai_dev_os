from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.output_compression.report_density import ReportDensityFrame, ReportDensityPolicy
from ai_dev_os.output_compression.summary_deduplication import (
    SummaryDeduplicationFrame,
    SummaryDeduplicationPolicy,
    SummarySection,
)
from ai_dev_os.output_compression.validation_compaction import (
    ValidationCompactionFrame,
    ValidationCompactionPolicy,
    ValidationResult,
)


@dataclass(frozen=True)
class CompactCompletionInput:
    commit: str
    ci_status: str
    validation_results: tuple[ValidationResult, ...]
    runtime_audit_status: str
    risks: tuple[str, ...]
    next_step: str
    rollout_summary: str = ""
    unchanged_sections: tuple[str, ...] = ()


@dataclass(frozen=True)
class CompactCompletionFrame:
    compact: bool
    bounded: bool
    deduplicated: bool
    expandable: bool
    compact_summary: str
    expandable_details: tuple[str, ...]
    validation: ValidationCompactionFrame
    deduplication: SummaryDeduplicationFrame
    density: ReportDensityFrame
    estimated_avoided_completion_tokens: int
    estimated_avoided_repeated_summaries: int
    rollback_safe: bool
    human_readable: bool
    deterministic_compact_mode: bool


class CompactCompletionPolicy:
    def compact(self, data: CompactCompletionInput) -> CompactCompletionFrame:
        validation = ValidationCompactionPolicy().compact(data.validation_results)
        sections = (
            SummarySection("Commit", data.commit),
            SummarySection("CI", data.ci_status),
            SummarySection("Validation", validation.compact_validation_projection),
            SummarySection("Runtime audit", data.runtime_audit_status),
            SummarySection("Risks", str(len(data.risks))),
            SummarySection("Next", data.next_step),
            SummarySection(
                "Rollout summary", data.rollout_summary, "rollout" in data.unchanged_sections
            ),
        )
        deduplication = SummaryDeduplicationPolicy().deduplicate(sections)
        density = ReportDensityPolicy().audit(
            tuple(section.title for section in sections),
            unchanged_sections=len(data.unchanged_sections),
            repeated_token_estimate=deduplication.estimated_avoided_repeated_tokens,
        )
        compact_summary = "\n".join(
            (
                f"Commit: {data.commit}",
                f"CI: {data.ci_status}",
                validation.compact_validation_projection,
                f"Runtime audit: {data.runtime_audit_status}",
                f"Risks: {len(data.risks)}",
                f"Next: {data.next_step}",
            )
        )
        details = (
            validation.expandable_details
            + tuple(f"Risk: {risk}" for risk in data.risks)
            + tuple(deduplication.compact_references)
        )
        return CompactCompletionFrame(
            compact=True,
            bounded=True,
            deduplicated=deduplication.repeated_summary_detected
            or deduplication.unchanged_section_suppression,
            expandable=True,
            compact_summary=compact_summary,
            expandable_details=details,
            validation=validation,
            deduplication=deduplication,
            density=density,
            estimated_avoided_completion_tokens=density.estimated_avoided_completion_tokens,
            estimated_avoided_repeated_summaries=deduplication.estimated_avoided_repeated_tokens,
            rollback_safe=True,
            human_readable=True,
            deterministic_compact_mode=True,
        )
