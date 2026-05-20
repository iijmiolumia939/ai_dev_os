from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryFrame

_OVERLAP_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("duplicated_governance_signals", ("governance", "cognition")),
    ("duplicated_persistence_logic", ("persistence", "governance")),
    ("duplicated_retrieval_scaling_logic", ("retrieval", "cognition")),
    ("duplicated_session_lifecycle_logic", ("orchestration", "vscode")),
    ("duplicated_pressure_aggregation", ("governance", "orchestration")),
    ("duplicated_compact_export_logic", ("orchestration", "vscode")),
)


@dataclass(frozen=True)
class RuntimeOverlapFrame:
    overlap_detected: bool
    overlap_categories: tuple[str, ...]
    overlap_density: float
    bounded_merge_possible: bool
    simplification_pressure: str
    summary_only: bool
    ast_replay_used: bool
    dynamic_tracing_used: bool
    full_source_analysis_used: bool


class RuntimeOverlapPolicy:
    def detect(
        self,
        discovery: RuntimeDiscoveryFrame,
        *,
        max_overlap_categories: int = 6,
    ) -> RuntimeOverlapFrame:
        categories = set(discovery.category_counts)
        overlaps = tuple(
            name
            for name, required in _OVERLAP_RULES
            if all(category in categories for category in required)
        )[:max_overlap_categories]
        density = round(
            len(overlaps) / max(1, min(max_overlap_categories, len(_OVERLAP_RULES))), 4
        )
        pressure = "high" if density >= 0.67 else "medium" if density >= 0.34 else "low"
        return RuntimeOverlapFrame(
            overlap_detected=bool(overlaps),
            overlap_categories=overlaps,
            overlap_density=density,
            bounded_merge_possible=0 < len(overlaps) <= max_overlap_categories,
            simplification_pressure=pressure,
            summary_only=True,
            ast_replay_used=False,
            dynamic_tracing_used=False,
            full_source_analysis_used=False,
        )
