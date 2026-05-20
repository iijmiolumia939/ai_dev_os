from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PersistenceBudgetFrame:
    checkpoint_storage: int
    continuity_index_storage: int
    prompt_export_storage: int
    stale_persistence_storage: int
    schema_metadata_storage: int
    current_budget_usage: int
    retention_pressure: str
    compact_required: bool
    cleanup_required: bool
    storage_budget_remaining: int
    storage_budget: int


class PersistenceBudgetPolicy:
    def evaluate(
        self,
        *,
        checkpoint_storage: int,
        continuity_index_storage: int,
        prompt_export_storage: int,
        stale_persistence_storage: int,
        schema_metadata_storage: int,
        storage_budget: int = 64_000,
    ) -> PersistenceBudgetFrame:
        usage = max(
            0,
            checkpoint_storage
            + continuity_index_storage
            + prompt_export_storage
            + stale_persistence_storage
            + schema_metadata_storage,
        )
        remaining = max(0, storage_budget - usage)
        ratio = usage / storage_budget if storage_budget else 1.0
        pressure = "high" if ratio >= 0.85 else "medium" if ratio >= 0.65 else "low"
        return PersistenceBudgetFrame(
            checkpoint_storage=checkpoint_storage,
            continuity_index_storage=continuity_index_storage,
            prompt_export_storage=prompt_export_storage,
            stale_persistence_storage=stale_persistence_storage,
            schema_metadata_storage=schema_metadata_storage,
            current_budget_usage=usage,
            retention_pressure=pressure,
            compact_required=ratio >= 0.65,
            cleanup_required=ratio >= 0.85 or stale_persistence_storage > storage_budget * 0.2,
            storage_budget_remaining=remaining,
            storage_budget=storage_budget,
        )
