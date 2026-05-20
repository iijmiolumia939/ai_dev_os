from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalCompactionFrame:
    deduplicated_retrieval_summaries: tuple[str, ...]
    compact_contract_surfaces: tuple[str, ...]
    compact_runtime_metadata: tuple[str, ...]
    expandable_retrieval_details: tuple[str, ...]
    estimated_compacted_tokens: int
    summary_only: bool
    deterministic: bool


class RetrievalCompactionPolicy:
    def compact(
        self,
        *,
        runtime_summaries: tuple[str, ...],
        contract_surfaces: tuple[str, ...],
        runtime_metadata: tuple[str, ...],
    ) -> RetrievalCompactionFrame:
        summaries = tuple(
            dict.fromkeys(item.strip() for item in runtime_summaries if item.strip())
        )
        contracts = tuple(
            dict.fromkeys(_compact_contract(item) for item in contract_surfaces if item)
        )
        metadata = tuple(
            dict.fromkeys(_compact_metadata(item) for item in runtime_metadata if item)
        )
        details = summaries + contracts + metadata
        return RetrievalCompactionFrame(
            deduplicated_retrieval_summaries=summaries,
            compact_contract_surfaces=contracts,
            compact_runtime_metadata=metadata,
            expandable_retrieval_details=details,
            estimated_compacted_tokens=sum(max(1, len(item.split())) for item in details),
            summary_only=True,
            deterministic=True,
        )


def _compact_contract(value: str) -> str:
    return value.split("(", maxsplit=1)[0].strip()


def _compact_metadata(value: str) -> str:
    parts = value.split()
    return " ".join(parts[:8])
