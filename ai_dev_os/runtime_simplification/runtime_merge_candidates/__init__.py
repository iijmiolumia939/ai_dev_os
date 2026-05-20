from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_simplification.contract_overlap import RuntimeContractOverlapFrame
from ai_dev_os.runtime_simplification.overlap_detection import RuntimeOverlapFrame


@dataclass(frozen=True)
class RuntimeMergeCandidateFrame:
    merge_candidates: tuple[str, ...]
    merge_risk: str
    rollback_safe_merge_possible: bool
    isolation_required: bool
    human_review_required: bool
    recommendation_only: bool
    automatic_merge_used: bool


class RuntimeMergeCandidatePolicy:
    def propose(
        self,
        overlap: RuntimeOverlapFrame,
        contract_overlap: RuntimeContractOverlapFrame,
        *,
        max_candidates: int = 5,
    ) -> RuntimeMergeCandidateFrame:
        candidates = []
        if "duplicated_governance_signals" in overlap.overlap_categories:
            candidates.append("governance_health + governance_trends dashboard summary")
        if "duplicated_persistence_logic" in overlap.overlap_categories:
            candidates.append("workspace_persistence + persistence_governance metadata boundary")
        if "duplicated_session_lifecycle_logic" in overlap.overlap_categories:
            candidates.append("session_lifecycle + session_boundary warning surface")
        if "duplicated_compact_export_logic" in overlap.overlap_categories:
            candidates.append("session_orchestrator + vscode_integration export adapter")
        if contract_overlap.oversized_contract_surface:
            candidates.append("runtime_graph + runtime_simplification contract summary")
        bounded = tuple(candidates[:max_candidates])
        risk = (
            "high"
            if contract_overlap.oversized_contract_surface
            else "medium" if bounded else "low"
        )
        return RuntimeMergeCandidateFrame(
            merge_candidates=bounded,
            merge_risk=risk,
            rollback_safe_merge_possible=bool(bounded) and risk != "high",
            isolation_required=risk == "high",
            human_review_required=bool(bounded),
            recommendation_only=True,
            automatic_merge_used=False,
        )
