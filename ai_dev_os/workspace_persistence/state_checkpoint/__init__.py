from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StateCheckpointFrame:
    session_generation: int
    enforcement_state: str
    prompt_mode: str
    continuity_scope: tuple[str, ...]
    repository_subset: tuple[str, ...]
    active_sprint_metadata: dict[str, Any]
    estimated_size: int
    size_budget: int
    budget_enforced: bool
    full_workspace_snapshot_included: bool


class StateCheckpointPolicy:
    def checkpoint(
        self,
        *,
        session_generation: int,
        enforcement_state: str,
        prompt_mode: str,
        continuity_scope: tuple[str, ...],
        repository_subset: tuple[str, ...],
        active_sprint_metadata: dict[str, Any],
        size_budget: int = 2_400,
    ) -> StateCheckpointFrame:
        bounded_metadata = {
            key: value
            for key, value in active_sprint_metadata.items()
            if key not in {"full_workspace_snapshot", "raw_transcript", "full_history"}
        }
        estimated = (
            len(prompt_mode) * 2
            + len(enforcement_state) * 2
            + sum(len(item) for item in continuity_scope) * 2
            + sum(len(item) for item in repository_subset) * 2
            + sum(len(str(value)) for value in bounded_metadata.values())
        )
        return StateCheckpointFrame(
            session_generation=max(1, session_generation),
            enforcement_state=enforcement_state,
            prompt_mode=prompt_mode,
            continuity_scope=continuity_scope[:8],
            repository_subset=repository_subset[:5],
            active_sprint_metadata=bounded_metadata,
            estimated_size=min(estimated, size_budget),
            size_budget=size_budget,
            budget_enforced=estimated <= size_budget,
            full_workspace_snapshot_included=False,
        )
