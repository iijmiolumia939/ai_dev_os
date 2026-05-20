from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceCompactExportFrame:
    export_mode: str
    compact_export_size: int
    copy_ready: bool
    bounded_export_maintained: bool
    summary_only: bool
    full_export_used: bool


class GovernanceCompactExportPrimitive:
    def export(
        self,
        summary_items: tuple[str, ...],
        *,
        export_mode: str = "summary",
        max_items: int = 8,
    ) -> GovernanceCompactExportFrame:
        retained = tuple(item for item in summary_items if item)[:max_items]
        size = sum(max(1, len(item) // 4) for item in retained)
        mode = export_mode if export_mode in {"summary", "copy_ready", "dashboard"} else "summary"
        return GovernanceCompactExportFrame(
            export_mode=mode,
            compact_export_size=size,
            copy_ready=mode == "copy_ready" and bool(retained),
            bounded_export_maintained=len(retained) <= max_items,
            summary_only=True,
            full_export_used=False,
        )
