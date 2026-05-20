from __future__ import annotations

from ai_dev_os.incremental_context import IncrementalContextRuntime
from ai_dev_os.retrieval_budget import RuntimeDependency


def _frame():
    return IncrementalContextRuntime().evaluate(
        changed_runtimes=("incremental_context", "runtime_audit"),
        all_runtimes=(
            "incremental_context",
            "runtime_audit",
            "retrieval_budget",
            "runtime_graph",
            "governance_health",
        ),
        dependencies=(
            RuntimeDependency("incremental_context", "retrieval_budget", 1, "delta"),
            RuntimeDependency("runtime_graph", "governance_health", 3, "unchanged"),
        ),
        changed_contracts=("IncrementalContextFrame",),
        changed_governance=("NFR-COST-18",),
        changed_session=("FR-INCREMENTALCONTEXT-01",),
        previous_continuity=("old sprint summary",),
        current_continuity=("changed delta summary",),
        stale_continuity=("stale continuity",),
        changed_audit_sections=("incremental_context",),
        unchanged_audit_sections=("activation", "routing"),
        repeated_validations=("pytest",),
        continuity_size=1_800,
    )


def test_tc_incrementalcontext_01_runtime_is_active_and_bounded() -> None:
    frame = _frame()

    assert frame.incremental_context_active is True
    assert frame.local_only is True
    assert frame.deterministic is True
    assert frame.summary_only is True
    assert frame.bounded_retention is True


def test_tc_incrementalcontext_02_required_safety_constraints_are_enforced() -> None:
    frame = _frame()

    assert frame.no_raw_transcript_persistence is True
    assert frame.no_hidden_provider_memory is True
    assert frame.no_ast_replay is True
    assert frame.no_repo_wide_replay is True
    assert frame.no_dynamic_tracing is True
    assert frame.no_automatic_context_expansion is True


def test_tc_incrementalcontext_03_pressure_and_recommendation_reduce_replay() -> None:
    frame = _frame()

    assert frame.incremental_pressure.repeated_replay_detection is True
    assert frame.incremental_pressure.estimated_repeated_input_token_burn > 0
    assert frame.incremental_recommendation.delta_only_session_recommendation is True
    assert frame.incremental_recommendation.unchanged_runtime_suppression_recommendation is True
    assert frame.estimated_avoided_repeated_input_tokens > 0
    assert frame.estimated_avoided_duplicate_runtime_cognition > 0
