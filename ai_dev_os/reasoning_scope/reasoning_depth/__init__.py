from __future__ import annotations

from dataclasses import dataclass

_DEPTH_CAPS = {"LOW": 1, "MEDIUM": 2, "HIGH": 4}
_NEIGHBORHOOD_CAPS = {"LOW": 1, "MEDIUM": 2, "HIGH": 4}


@dataclass(frozen=True)
class ReasoningDepthFrame:
    complexity: str
    reasoning_depth_cap: int
    bounded_chain_scope_metadata: tuple[str, ...]
    maximum_reasoning_neighborhood: int
    compact_reasoning_recommendation: bool
    escalation_boundary_metadata: tuple[str, ...]
    local_only: bool
    deterministic: bool
    summary_only: bool


class ReasoningDepthPolicy:
    def cap(
        self,
        *,
        complexity: str,
        affected_runtimes: tuple[str, ...] = (),
        governance_sensitive: bool = False,
    ) -> ReasoningDepthFrame:
        normalized = complexity.upper()
        if normalized not in _DEPTH_CAPS:
            normalized = "MEDIUM"
        depth_cap = _DEPTH_CAPS[normalized]
        neighborhood_cap = _NEIGHBORHOOD_CAPS[normalized]
        boundary = [f"complexity:{normalized}", f"depth_cap:{depth_cap}"]
        if governance_sensitive:
            boundary.append("governance_review:summary_only")
        return ReasoningDepthFrame(
            complexity=normalized,
            reasoning_depth_cap=depth_cap,
            bounded_chain_scope_metadata=(
                f"task_local:{bool(affected_runtimes)}",
                "chain_scope:metadata_only",
            ),
            maximum_reasoning_neighborhood=neighborhood_cap,
            compact_reasoning_recommendation=normalized in {"LOW", "MEDIUM"},
            escalation_boundary_metadata=tuple(boundary),
            local_only=True,
            deterministic=True,
            summary_only=True,
        )
