from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EscalationPolicyInput:
    recommended_tier: str
    complexity_level: str
    escalation_required: bool
    quality_floor_tier: str
    previous_escalations: int = 0
    cooldown_remaining: int = 0


@dataclass(frozen=True)
class EscalationFrame:
    high_reasoning_allowed: bool
    escalation_required: bool
    escalation_reason: str
    cooldown_active: bool
    bounded_escalation: bool
    rollback_safe_escalation: bool
    human_visible_escalation: bool
    hidden_provider_switching: bool
    warnings: tuple[str, ...]


class EscalationPolicy:
    def __init__(self, max_escalations_per_sprint: int = 2) -> None:
        self.max_escalations_per_sprint = max_escalations_per_sprint

    def evaluate(self, data: EscalationPolicyInput) -> EscalationFrame:
        tier = data.recommended_tier.upper()
        floor = data.quality_floor_tier.upper()
        critical_floor = floor == "HIGH"
        requested_high = tier == "HIGH" or data.complexity_level.upper() == "HIGH"
        cooldown_active = data.cooldown_remaining > 0
        quota_exhausted = data.previous_escalations >= self.max_escalations_per_sprint
        escalation_required = data.escalation_required or critical_floor or requested_high
        allowed = escalation_required and (
            critical_floor or not (cooldown_active or quota_exhausted)
        )
        warnings: list[str] = []
        if cooldown_active and not critical_floor:
            warnings.append("escalation_cooldown_active")
        if quota_exhausted and not critical_floor:
            warnings.append("escalation_quota_exhausted")
        if critical_floor and (cooldown_active or quota_exhausted):
            warnings.append("quality_floor_override_visible")
        reason = (
            "quality_floor_protection"
            if critical_floor
            else "complexity_threshold" if requested_high else "no_escalation_needed"
        )
        return EscalationFrame(
            high_reasoning_allowed=allowed,
            escalation_required=escalation_required,
            escalation_reason=reason,
            cooldown_active=cooldown_active,
            bounded_escalation=True,
            rollback_safe_escalation=True,
            human_visible_escalation=True,
            hidden_provider_switching=False,
            warnings=tuple(warnings),
        )
