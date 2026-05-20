from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceBoundedRetentionFrame:
    bounded_retention_active: bool
    retention_limit: int
    retained_items: tuple[str, ...]
    evicted_items: tuple[str, ...]
    eviction_count: int
    oldest_first_eviction: bool
    bounded_growth_maintained: bool


class GovernanceBoundedRetentionPrimitive:
    def apply(
        self,
        items: tuple[str, ...],
        *,
        retention_limit: int = 5,
    ) -> GovernanceBoundedRetentionFrame:
        if retention_limit <= 0:
            raise ValueError("retention_limit must be positive")
        retained = items[-retention_limit:]
        evicted = items[: max(0, len(items) - retention_limit)]
        return GovernanceBoundedRetentionFrame(
            bounded_retention_active=True,
            retention_limit=retention_limit,
            retained_items=retained,
            evicted_items=evicted,
            eviction_count=len(evicted),
            oldest_first_eviction=True,
            bounded_growth_maintained=len(retained) <= retention_limit,
        )
