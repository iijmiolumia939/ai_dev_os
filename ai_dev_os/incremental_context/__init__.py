from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.incremental_context.audit_delta import AuditDeltaFrame, AuditDeltaPolicy
from ai_dev_os.incremental_context.cognition_cache import CognitionCacheFrame, CognitionCachePolicy
from ai_dev_os.incremental_context.context_delta import ContextDeltaFrame, ContextDeltaPolicy
from ai_dev_os.incremental_context.continuity_delta import (
    ContinuityDeltaFrame,
    ContinuityDeltaPolicy,
)
from ai_dev_os.incremental_context.delta_retrieval import DeltaRetrievalFrame, DeltaRetrievalPolicy
from ai_dev_os.incremental_context.incremental_pressure import (
    IncrementalPressureFrame,
    IncrementalPressurePolicy,
)
from ai_dev_os.incremental_context.incremental_recommendation import (
    IncrementalRecommendationFrame,
    IncrementalRecommendationPolicy,
)
from ai_dev_os.retrieval_budget.retrieval_radius import RuntimeDependency


@dataclass(frozen=True)
class IncrementalContextFrame:
    context_delta: ContextDeltaFrame
    delta_retrieval: DeltaRetrievalFrame
    continuity_delta: ContinuityDeltaFrame
    audit_delta: AuditDeltaFrame
    cognition_cache: CognitionCacheFrame
    incremental_pressure: IncrementalPressureFrame
    incremental_recommendation: IncrementalRecommendationFrame
    incremental_context_active: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_retention: bool
    no_raw_transcript_persistence: bool
    no_hidden_provider_memory: bool
    no_ast_replay: bool
    no_repo_wide_replay: bool
    no_dynamic_tracing: bool
    no_automatic_context_expansion: bool
    estimated_avoided_repeated_input_tokens: int
    estimated_avoided_duplicate_runtime_cognition: int


class IncrementalContextRuntime:
    def evaluate(
        self,
        *,
        changed_runtimes: tuple[str, ...],
        all_runtimes: tuple[str, ...],
        dependencies: tuple[RuntimeDependency, ...] = (),
        changed_contracts: tuple[str, ...] = (),
        changed_governance: tuple[str, ...] = (),
        changed_session: tuple[str, ...] = (),
        previous_continuity: tuple[str, ...] = (),
        current_continuity: tuple[str, ...] = (),
        stale_continuity: tuple[str, ...] = (),
        changed_audit_sections: tuple[str, ...] = (),
        unchanged_audit_sections: tuple[str, ...] = (),
        repeated_validations: tuple[str, ...] = (),
        previous_fingerprints: tuple[str, ...] = (),
        continuity_size: int = 0,
        architecture_isolation: bool = True,
    ) -> IncrementalContextFrame:
        context_delta = ContextDeltaPolicy().summarize(
            changed_runtimes=changed_runtimes,
            all_runtimes=all_runtimes,
            changed_contracts=changed_contracts,
            changed_governance=changed_governance,
            changed_session=changed_session,
        )
        delta_retrieval = DeltaRetrievalPolicy().retrieve(
            delta=context_delta,
            all_runtimes=all_runtimes,
            dependencies=dependencies,
            continuity_size=continuity_size,
        )
        continuity_delta = ContinuityDeltaPolicy().diff(
            previous_summaries=previous_continuity,
            current_summaries=current_continuity,
            stale_summaries=stale_continuity,
        )
        audit_delta = AuditDeltaPolicy().summarize(
            changed_sections=changed_audit_sections,
            unchanged_sections=unchanged_audit_sections,
            repeated_validations=repeated_validations,
        )
        cache = CognitionCachePolicy().fingerprint(
            context_summaries=(
                context_delta.changed_runtime_summaries
                + context_delta.changed_contract_summaries
                + context_delta.changed_governance_summaries
                + context_delta.changed_session_summaries
                + continuity_delta.compact_continuity_diff
                + audit_delta.compact_audit_delta_summary
            ),
            previous_fingerprints=previous_fingerprints,
        )
        pressure = IncrementalPressurePolicy().evaluate(
            repeated_context_count=len(context_delta.excluded_unchanged_context),
            duplicate_architecture_sections=len(changed_governance),
            runtime_graph_replay_count=len(delta_retrieval.suppressed_unchanged_dependencies),
            continuity_replay_count=len(previous_continuity) + len(stale_continuity),
        )
        recommendation = IncrementalRecommendationPolicy().recommend(
            pressure=pressure,
            unchanged_runtimes=context_delta.excluded_unchanged_context,
            architecture_isolation=architecture_isolation,
        )
        avoided_tokens = (
            pressure.estimated_repeated_input_token_burn
            + continuity_delta.estimated_avoided_continuity_tokens
            + audit_delta.estimated_avoided_validation_tokens
        )
        active = all(
            (
                context_delta.unchanged_context_exclusion,
                delta_retrieval.delta_only_retrieval,
                continuity_delta.continuity_replay_reduction,
                audit_delta.runtime_audit_delta_mode,
                cache.no_raw_prompt_persistence,
                pressure.summary_only,
                recommendation.delta_only_session_recommendation,
            )
        )
        return IncrementalContextFrame(
            context_delta=context_delta,
            delta_retrieval=delta_retrieval,
            continuity_delta=continuity_delta,
            audit_delta=audit_delta,
            cognition_cache=cache,
            incremental_pressure=pressure,
            incremental_recommendation=recommendation,
            incremental_context_active=active,
            local_only=True,
            deterministic=True,
            summary_only=True,
            bounded_retention=cache.bounded_retention,
            no_raw_transcript_persistence=True,
            no_hidden_provider_memory=cache.no_provider_specific_hidden_memory,
            no_ast_replay=True,
            no_repo_wide_replay=delta_retrieval.repo_wide_replay_forbidden,
            no_dynamic_tracing=True,
            no_automatic_context_expansion=True,
            estimated_avoided_repeated_input_tokens=avoided_tokens,
            estimated_avoided_duplicate_runtime_cognition=(
                pressure.estimated_duplicate_runtime_cognition
            ),
        )


__all__ = [
    "AuditDeltaFrame",
    "AuditDeltaPolicy",
    "CognitionCacheFrame",
    "CognitionCachePolicy",
    "ContextDeltaFrame",
    "ContextDeltaPolicy",
    "ContinuityDeltaFrame",
    "ContinuityDeltaPolicy",
    "DeltaRetrievalFrame",
    "DeltaRetrievalPolicy",
    "IncrementalContextFrame",
    "IncrementalContextRuntime",
    "IncrementalPressureFrame",
    "IncrementalPressurePolicy",
    "IncrementalRecommendationFrame",
    "IncrementalRecommendationPolicy",
]
