from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.runtime_graph import RuntimeGraphPolicy
from ai_dev_os.runtime_simplification.contract_overlap import (
    RuntimeContractOverlapFrame,
    RuntimeContractOverlapPolicy,
)
from ai_dev_os.runtime_simplification.governance_duplication import (
    GovernanceDuplicationFrame,
    GovernanceDuplicationPolicy,
)
from ai_dev_os.runtime_simplification.overlap_detection import (
    RuntimeOverlapFrame,
    RuntimeOverlapPolicy,
)
from ai_dev_os.runtime_simplification.runtime_merge_candidates import (
    RuntimeMergeCandidateFrame,
    RuntimeMergeCandidatePolicy,
)
from ai_dev_os.runtime_simplification.simplification_recommendations import (
    RuntimeSimplificationRecommendationFrame,
    RuntimeSimplificationRecommendationPolicy,
)


@dataclass(frozen=True)
class RuntimeSimplificationFrame:
    runtime_overlap: RuntimeOverlapFrame
    contract_overlap: RuntimeContractOverlapFrame
    merge_candidates: RuntimeMergeCandidateFrame
    governance_duplication: GovernanceDuplicationFrame
    recommendations: RuntimeSimplificationRecommendationFrame
    runtime_simplification_active: bool
    bounded_simplification_analysis: bool
    local_only_architecture_cognition: bool
    autonomous_mutation_used: bool
    hidden_contract_injection_used: bool
    retrieval_budget_active: bool
    repo_wide_retrieval_forbidden: bool
    incremental_context_active: bool
    repo_wide_replay_forbidden: bool
    reasoning_scope_active: bool
    automatic_architecture_escalation_forbidden: bool


class RuntimeSimplificationPolicy:
    def evaluate(self, repo_path: str | Path = ".") -> RuntimeSimplificationFrame:
        runtime_graph = RuntimeGraphPolicy().evaluate(repo_path, max_edges=24)
        overlap = RuntimeOverlapPolicy().detect(runtime_graph.discovery)
        contract = RuntimeContractOverlapPolicy().detect(runtime_graph.contract_surface)
        merge = RuntimeMergeCandidatePolicy().propose(overlap, contract)
        governance = GovernanceDuplicationPolicy().detect(overlap)
        recommendations = RuntimeSimplificationRecommendationPolicy().summarize(
            merge,
            contract,
            governance,
        )
        return RuntimeSimplificationFrame(
            runtime_overlap=overlap,
            contract_overlap=contract,
            merge_candidates=merge,
            governance_duplication=governance,
            recommendations=recommendations,
            runtime_simplification_active=overlap.summary_only and recommendations.summary_only,
            bounded_simplification_analysis=True,
            local_only_architecture_cognition=True,
            autonomous_mutation_used=False,
            hidden_contract_injection_used=False,
            retrieval_budget_active=runtime_graph.retrieval_budget_active,
            repo_wide_retrieval_forbidden=runtime_graph.repo_wide_retrieval_forbidden,
            incremental_context_active=runtime_graph.incremental_context_active,
            repo_wide_replay_forbidden=runtime_graph.repo_wide_replay_forbidden,
            reasoning_scope_active=runtime_graph.reasoning_scope_active,
            automatic_architecture_escalation_forbidden=(
                runtime_graph.automatic_architecture_escalation_forbidden
            ),
        )
