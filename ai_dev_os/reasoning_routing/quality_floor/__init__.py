from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.reasoning_routing.reasoning_tiers import TIER_ORDER, ReasoningTier, coerce_tier


@dataclass(frozen=True)
class QualityFloorFrame:
    selected_tier: str
    minimum_reasoning_floor: str
    architecture_protection: bool
    governance_protection: bool
    embodiment_protection: bool
    unsafe_downgrade_blocked: bool
    floor_reason: str


class QualityFloorPolicy:
    def enforce(
        self,
        candidate_tier: str | ReasoningTier,
        *,
        architecture_protection: bool = False,
        governance_protection: bool = False,
        embodiment_protection: bool = False,
    ) -> QualityFloorFrame:
        candidate = coerce_tier(candidate_tier)
        if architecture_protection or governance_protection or embodiment_protection:
            floor = ReasoningTier.HIGH
            reason = "critical_architecture_governance_or_embodiment_floor"
        else:
            floor = ReasoningTier.LOW
            reason = "routine_work_floor"
        selected = floor if TIER_ORDER[candidate] < TIER_ORDER[floor] else candidate
        return QualityFloorFrame(
            selected_tier=selected.value,
            minimum_reasoning_floor=floor.value,
            architecture_protection=architecture_protection,
            governance_protection=governance_protection,
            embodiment_protection=embodiment_protection,
            unsafe_downgrade_blocked=selected is not candidate,
            floor_reason=reason,
        )
