from __future__ import annotations

from dataclasses import dataclass

TIER0_ROLES = ("generator", "evaluator", "gate_runner")
TIER1_ROLES = ("architect", "adversary")
TIER2_ROLES = ("research_librarian", "formal_verification")


@dataclass(frozen=True)
class CouncilScope:
    roles: tuple[str, ...]
    max_parallel_roles: int
    reason: str


def select_scope(flags: set[str]) -> CouncilScope:
    if flags & {"scientific_review", "major_redesign", "production_incident"}:
        return CouncilScope(TIER0_ROLES + TIER1_ROLES + TIER2_ROLES, 2, "tier2 scoped")
    if flags & {"schema_change", "architecture_change", "safety_change"}:
        return CouncilScope(TIER0_ROLES + TIER1_ROLES, 2, "tier1 scoped")
    return CouncilScope(TIER0_ROLES, 1, "tier0 routine")
