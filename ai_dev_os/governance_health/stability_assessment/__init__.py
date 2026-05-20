from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceStabilityFrame:
    stability_score: int
    instability_detected: bool
    stabilization_recommended: bool
    compact_governance_recommended: bool
    bounded_governance_maintained: bool
    uncontrolled_expansion_detected: bool
    stale_governance_accumulation: bool
    governance_oscillation: bool
    repeated_rollover_instability: bool
    persistence_instability: bool
    retrieval_instability: bool


class GovernanceStabilityPolicy:
    def assess(
        self,
        *,
        bounded_governance_maintained: bool,
        uncontrolled_expansion_detected: bool,
        stale_governance_accumulation: bool,
        governance_oscillation: bool,
        repeated_rollover_instability: bool,
        persistence_instability: bool,
        retrieval_instability: bool,
    ) -> GovernanceStabilityFrame:
        instability_count = sum(
            (
                uncontrolled_expansion_detected,
                stale_governance_accumulation,
                governance_oscillation,
                repeated_rollover_instability,
                persistence_instability,
                retrieval_instability,
            )
        )
        score = 100 - instability_count * 13 - (0 if bounded_governance_maintained else 25)
        score = max(0, min(100, score))
        instability = instability_count > 0 or not bounded_governance_maintained
        return GovernanceStabilityFrame(
            stability_score=score,
            instability_detected=instability,
            stabilization_recommended=instability_count >= 2 or not bounded_governance_maintained,
            compact_governance_recommended=stale_governance_accumulation
            or persistence_instability
            or retrieval_instability,
            bounded_governance_maintained=bounded_governance_maintained,
            uncontrolled_expansion_detected=uncontrolled_expansion_detected,
            stale_governance_accumulation=stale_governance_accumulation,
            governance_oscillation=governance_oscillation,
            repeated_rollover_instability=repeated_rollover_instability,
            persistence_instability=persistence_instability,
            retrieval_instability=retrieval_instability,
        )
