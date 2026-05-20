from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceRiskFrame:
    aggregate_risk: str
    highest_risk: str
    isolation_recommended: bool
    compact_recommended: bool
    rollover_recommended: bool
    active_risks: tuple[str, ...]


class GovernanceRiskPolicy:
    def aggregate(
        self,
        *,
        stale_continuity_risk: bool,
        hidden_context_drift: bool,
        architecture_contamination: bool,
        retrieval_explosion: bool,
        persistence_explosion: bool,
        checkpoint_explosion: bool,
        provider_lock_in_risk: bool,
        governance_runtime_drift: bool,
        prompt_mode_drift: bool,
    ) -> GovernanceRiskFrame:
        signals = {
            "stale_continuity": stale_continuity_risk,
            "hidden_context_drift": hidden_context_drift,
            "architecture_contamination": architecture_contamination,
            "retrieval_explosion": retrieval_explosion,
            "persistence_explosion": persistence_explosion,
            "checkpoint_explosion": checkpoint_explosion,
            "provider_lock_in": provider_lock_in_risk,
            "governance_runtime_drift": governance_runtime_drift,
            "prompt_mode_drift": prompt_mode_drift,
        }
        active = tuple(name for name, enabled in signals.items() if enabled)
        highest = _highest(active)
        return GovernanceRiskFrame(
            aggregate_risk=_risk_label(len(active)),
            highest_risk=highest,
            isolation_recommended=architecture_contamination or prompt_mode_drift,
            compact_recommended=bool(
                stale_continuity_risk
                or retrieval_explosion
                or persistence_explosion
                or checkpoint_explosion
            ),
            rollover_recommended=stale_continuity_risk or hidden_context_drift,
            active_risks=active,
        )


def _risk_label(count: int) -> str:
    if count >= 6:
        return "critical"
    if count >= 4:
        return "high"
    if count >= 2:
        return "medium"
    return "low"


def _highest(active: tuple[str, ...]) -> str:
    priority = (
        "architecture_contamination",
        "hidden_context_drift",
        "retrieval_explosion",
        "persistence_explosion",
        "checkpoint_explosion",
        "stale_continuity",
        "governance_runtime_drift",
        "prompt_mode_drift",
        "provider_lock_in",
    )
    for item in priority:
        if item in active:
            return item
    return "none"
