from __future__ import annotations

from ai_dev_os.incremental_context.context_delta import ContextDeltaPolicy
from ai_dev_os.incremental_context.delta_retrieval import DeltaRetrievalPolicy
from ai_dev_os.retrieval_budget import RuntimeDependency


def test_tc_incrementalcontext_04_context_delta_excludes_unchanged_context() -> None:
    frame = ContextDeltaPolicy().summarize(
        changed_runtimes=("runtime_audit",),
        all_runtimes=("runtime_audit", "runtime_graph", "governance_health"),
        changed_contracts=("IncrementalContextAuditReport",),
        changed_governance=("NFR-COST-18",),
        changed_session=("TC-INCREMENTALCONTEXT-04",),
    )

    assert frame.changed_runtime_summaries == ("runtime:runtime_audit",)
    assert frame.changed_contract_summaries == ("contract:IncrementalContextAuditReport",)
    assert frame.unchanged_context_exclusion is True
    assert frame.excluded_unchanged_context == ("governance_health", "runtime_graph")
    assert frame.deterministic_delta_scope is True


def test_tc_incrementalcontext_05_delta_retrieval_suppresses_unchanged_dependencies() -> None:
    delta = ContextDeltaPolicy().summarize(
        changed_runtimes=("incremental_context",),
        all_runtimes=("incremental_context", "retrieval_budget", "provider_simulation"),
    )
    frame = DeltaRetrievalPolicy().retrieve(
        delta=delta,
        all_runtimes=("incremental_context", "retrieval_budget", "provider_simulation"),
        dependencies=(
            RuntimeDependency("incremental_context", "retrieval_budget", 1, "delta"),
            RuntimeDependency("provider_simulation", "release_readiness", 2, "unchanged"),
        ),
        continuity_size=800,
    )

    assert frame.delta_only_retrieval is True
    assert frame.bounded_incremental_retrieval_radius == 1
    assert frame.unchanged_dependency_suppression is True
    assert "provider_simulation->release_readiness" in frame.suppressed_unchanged_dependencies
    assert frame.repo_wide_replay_forbidden is True
