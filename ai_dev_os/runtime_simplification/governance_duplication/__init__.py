from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_simplification.overlap_detection import RuntimeOverlapFrame


@dataclass(frozen=True)
class GovernanceDuplicationFrame:
    governance_duplication_detected: bool
    duplicated_governance_groups: tuple[str, ...]
    simplification_priority: str
    bounded_consolidation_possible: bool
    summary_only: bool


class GovernanceDuplicationPolicy:
    def detect(self, overlap: RuntimeOverlapFrame) -> GovernanceDuplicationFrame:
        groups = tuple(
            category
            for category in overlap.overlap_categories
            if category
            in {
                "duplicated_governance_signals",
                "duplicated_pressure_aggregation",
                "duplicated_persistence_logic",
                "duplicated_session_lifecycle_logic",
            }
        )
        priority = "high" if len(groups) >= 3 else "medium" if groups else "low"
        return GovernanceDuplicationFrame(
            governance_duplication_detected=bool(groups),
            duplicated_governance_groups=groups,
            simplification_priority=priority,
            bounded_consolidation_possible=0 < len(groups) <= 4,
            summary_only=True,
        )
