from __future__ import annotations

from dataclasses import dataclass

_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
_CLASS_BY_ORDER = {value: key for key, value in _ORDER.items()}


@dataclass(frozen=True)
class ProviderDowngradeFrame:
    downgrade_safe_recommendation: bool
    quality_floor_aware_downgrade: bool
    compact_summary_downgrade: bool
    repetitive_task_downgrade: bool
    local_patch_downgrade: bool
    recommended_provider_class: str
    downgrade_reason: str
    deterministic: bool
    summary_only: bool


class ProviderDowngradePolicy:
    def recommend(
        self,
        *,
        current_provider_class: str,
        quality_floor: str = "LOW",
        compact_summary: bool = False,
        repetitive_task: bool = False,
        local_patch: bool = False,
        pressure_level: str = "LOW",
    ) -> ProviderDowngradeFrame:
        target_order = _ORDER[current_provider_class]
        if local_patch or compact_summary or repetitive_task:
            target_order = min(target_order, _ORDER["LOW"])
        elif pressure_level in {"MEDIUM", "HIGH", "OVER_BUDGET"}:
            target_order = min(target_order, _ORDER["MEDIUM"])
        target_order = max(target_order, _ORDER[quality_floor])
        recommended = _CLASS_BY_ORDER[target_order]
        changed = recommended != current_provider_class
        reason = "quality_floor_preserved"
        if local_patch:
            reason = "local_patch_downgrade"
        elif compact_summary:
            reason = "compact_summary_downgrade"
        elif repetitive_task:
            reason = "repetitive_task_downgrade"
        elif changed:
            reason = "provider_pressure_downgrade"
        return ProviderDowngradeFrame(
            downgrade_safe_recommendation=changed,
            quality_floor_aware_downgrade=_ORDER[recommended] >= _ORDER[quality_floor],
            compact_summary_downgrade=compact_summary and changed,
            repetitive_task_downgrade=repetitive_task and changed,
            local_patch_downgrade=local_patch and changed,
            recommended_provider_class=recommended,
            downgrade_reason=reason,
            deterministic=True,
            summary_only=True,
        )
