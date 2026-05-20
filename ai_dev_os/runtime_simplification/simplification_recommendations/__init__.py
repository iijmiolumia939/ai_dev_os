from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.compact_export import GovernanceCompactExportPrimitive
from ai_dev_os.runtime_simplification.contract_overlap import RuntimeContractOverlapFrame
from ai_dev_os.runtime_simplification.governance_duplication import GovernanceDuplicationFrame
from ai_dev_os.runtime_simplification.runtime_merge_candidates import RuntimeMergeCandidateFrame


@dataclass(frozen=True)
class RuntimeSimplificationRecommendationFrame:
    recommended_runtime_merges: tuple[str, ...]
    recommended_contract_reductions: tuple[str, ...]
    recommended_boundary_tightening: tuple[str, ...]
    recommended_isolation: tuple[str, ...]
    recommended_governance_consolidation: tuple[str, ...]
    summary_only: bool
    human_confirmed_only: bool
    automatic_rewrite_used: bool


class RuntimeSimplificationRecommendationPolicy:
    def summarize(
        self,
        merge: RuntimeMergeCandidateFrame,
        contract_overlap: RuntimeContractOverlapFrame,
        governance: GovernanceDuplicationFrame,
    ) -> RuntimeSimplificationRecommendationFrame:
        reductions = tuple(
            f"reduce {group}" for group in contract_overlap.duplicated_contract_groups[:4]
        )
        tightening = (
            "keep VSCode as view-only integration",
            "keep runtime graph as summary metadata",
        )
        isolation = ("isolate high-risk merge candidates",) if merge.isolation_required else ()
        consolidation = tuple(
            f"consolidate {group}" for group in governance.duplicated_governance_groups[:4]
        )
        GovernanceCompactExportPrimitive().export(
            merge.merge_candidates + reductions + tightening + isolation + consolidation,
            export_mode="summary",
        )
        return RuntimeSimplificationRecommendationFrame(
            recommended_runtime_merges=merge.merge_candidates,
            recommended_contract_reductions=reductions,
            recommended_boundary_tightening=tightening,
            recommended_isolation=isolation,
            recommended_governance_consolidation=consolidation,
            summary_only=True,
            human_confirmed_only=True,
            automatic_rewrite_used=False,
        )
