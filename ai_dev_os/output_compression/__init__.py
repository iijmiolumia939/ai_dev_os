from __future__ import annotations

from ai_dev_os.output_compression.compact_completion import (
    CompactCompletionFrame,
    CompactCompletionInput,
    CompactCompletionPolicy,
)
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

__all__ = [
    "CompactCompletionFrame",
    "CompactCompletionInput",
    "CompactCompletionPolicy",
    "ReportDensityFrame",
    "ReportDensityPolicy",
    "SummaryDeduplicationFrame",
    "SummaryDeduplicationPolicy",
    "SummarySection",
    "ValidationCompactionFrame",
    "ValidationCompactionPolicy",
    "ValidationResult",
]
