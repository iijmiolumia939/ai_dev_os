from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ModelTier(StrEnum):
    TIER0 = "tier0"
    TIER1 = "tier1"
    TIER2 = "tier2"


@dataclass(frozen=True)
class ModelRoute:
    tier: ModelTier
    model: str
    provider: str
    expensive: bool = False


def route_tier(
    task_type: str, *, architecture_impact: bool = False, safety_impact: bool = False
) -> ModelTier:
    normalized = task_type.strip().lower().replace("-", "_").replace(" ", "_")
    if architecture_impact or safety_impact:
        return ModelTier.TIER2
    if normalized in {"formatting", "lint", "tiny_patch", "unit_tests", "markdown_cleanup"}:
        return ModelTier.TIER0
    return ModelTier.TIER1
