from __future__ import annotations

from ai_dev_os.retrieval_budget import RetrievalBudgetRuntime, RuntimeDependency
from ai_dev_os.retrieval_budget.retrieval_budget_policy import RetrievalBudgetPolicy
from ai_dev_os.retrieval_budget.retrieval_compaction import RetrievalCompactionPolicy
from ai_dev_os.retrieval_budget.retrieval_radius import RetrievalRadiusPolicy


def _frame():
    return RetrievalBudgetRuntime().evaluate(
        affected_runtimes=("session_orchestrator", "retrieval"),
        all_runtimes=(
            "session_orchestrator",
            "retrieval",
            "context_subset",
            "runtime_graph",
            "providers",
        ),
        dependencies=(
            RuntimeDependency("session_orchestrator", "retrieval", 1, "continuity"),
            RuntimeDependency("retrieval", "context_subset", 1, "scope"),
            RuntimeDependency("runtime_graph", "providers", 4, "optional"),
        ),
        continuity_size=1_600,
        contract_surfaces=("RetrievalBudgetFrame", "RetrievalScopeFrame"),
        architecture_isolation=True,
    )


def test_tc_retrievalbudget_01_scope_is_affected_runtime_only() -> None:
    frame = _frame()

    assert frame.scope.affected_runtime_only_retrieval is True
    assert frame.scope.repo_wide_retrieval_forbidden is True
    assert frame.scope.dependency_depth_cap == 2
    assert frame.scope.architecture_isolation_aware_retrieval is True
    assert "providers" in frame.scope.excluded_runtimes


def test_tc_retrievalbudget_02_radius_caps_dependency_distance() -> None:
    frame = RetrievalRadiusPolicy().evaluate(
        ("a",),
        (
            RuntimeDependency("a", "b", 1, "near"),
            RuntimeDependency("a", "c", 3, "far"),
        ),
        max_dependency_distance=1,
    )

    assert frame.max_dependency_distance == 1
    assert frame.compact_runtime_neighborhood == ("a", "b")
    assert frame.bounded_contract_adjacency == ("near",)
    assert "a->c" in frame.isolated_runtime_boundaries


def test_tc_retrievalbudget_03_budget_policy_recommends_compaction() -> None:
    frame = RetrievalBudgetPolicy(max_runtime_count=2, max_contract_count=2).evaluate(
        runtime_count=3,
        contract_count=1,
        continuity_size=1_000,
    )

    assert frame.budget_exceeded is True
    assert frame.compact_retrieval_recommendation is True
    assert frame.automatic_retrieval_escalation is False


def test_tc_retrievalbudget_04_compaction_keeps_expandable_details() -> None:
    frame = RetrievalCompactionPolicy().compact(
        runtime_summaries=("runtime:a", "runtime:a", "runtime:b"),
        contract_surfaces=("Frame(detail)", "Frame(detail)"),
        runtime_metadata=("runtime a summary-only retrieval metadata",),
    )

    assert frame.deduplicated_retrieval_summaries == ("runtime:a", "runtime:b")
    assert frame.compact_contract_surfaces == ("Frame",)
    assert frame.expandable_retrieval_details
    assert frame.summary_only is True


def test_tc_retrievalbudget_06_runtime_is_local_deterministic_summary_only() -> None:
    first = _frame()
    second = _frame()

    assert first == second
    assert first.local_only is True
    assert first.deterministic is True
    assert first.summary_only is True
    assert first.scope.no_ast_replay is True
    assert first.scope.no_dynamic_tracing is True
    assert first.pressure.no_hidden_provider_routing is True
    assert first.pressure.no_automatic_retrieval_escalation is True
