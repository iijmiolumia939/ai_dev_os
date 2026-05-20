from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceContinuityPrimitiveFrame:
    continuity_scope: tuple[str, ...]
    continuity_budget: int
    continuity_compaction: bool
    bounded_continuity_maintained: bool
    excluded_scope: tuple[str, ...]


class GovernanceContinuityPrimitive:
    def scope(
        self,
        requested_scope: tuple[str, ...],
        *,
        continuity_budget: int = 2_400,
        max_scope_items: int = 5,
    ) -> GovernanceContinuityPrimitiveFrame:
        if continuity_budget <= 0:
            raise ValueError("continuity_budget must be positive")
        retained = tuple(item for item in requested_scope if item)[:max_scope_items]
        excluded = tuple(item for item in requested_scope if item)[max_scope_items:]
        return GovernanceContinuityPrimitiveFrame(
            continuity_scope=retained,
            continuity_budget=continuity_budget,
            continuity_compaction=bool(excluded),
            bounded_continuity_maintained=len(retained) <= max_scope_items,
            excluded_scope=excluded,
        )
