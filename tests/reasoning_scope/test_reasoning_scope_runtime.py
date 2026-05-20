from __future__ import annotations

from ai_dev_os.reasoning_scope import ReasoningScopeRuntime
from ai_dev_os.reasoning_scope.architecture_reasoning_guard import ArchitectureReasoningGuardPolicy
from ai_dev_os.reasoning_scope.local_patch_mode import LocalPatchModePolicy


def _frame():
    return ReasoningScopeRuntime().evaluate(
        task_name="local runtime patch",
        complexity="LOW",
        affected_runtimes=("reasoning_scope", "reasoning_routing"),
        touched_files=("ai_dev_os/reasoning_scope/__init__.py",),
        adjacent_contracts=("ReasoningScopeRuntimeFrame",),
        requested_depth=4,
        requested_runtime_count=6,
        repeated_architecture_sections=2,
        governance_sensitive=True,
        continuity_size=3_600,
        escalation_requested=True,
    )


def test_tc_reasoningscope_01_runtime_limits_reasoning_scope() -> None:
    frame = _frame()

    assert frame.reasoning_scope_active is True
    assert frame.reasoning_scope.bounded_reasoning_depth is True
    assert frame.reasoning_scope.task_local_cognition_scope == ("reasoning_routing",)
    assert frame.reasoning_scope.adjacent_runtime_only_reasoning_mode is True
    assert frame.reasoning_scope.governance_escalation_suppression is True


def test_tc_reasoningscope_02_constraints_are_local_deterministic_summary_only() -> None:
    frame = _frame()

    assert frame.local_only is True
    assert frame.deterministic is True
    assert frame.summary_only is True
    assert frame.bounded_cognition_only is True
    assert frame.no_hidden_chain_of_thought_persistence is True
    assert frame.no_ast_replay is True
    assert frame.no_hidden_provider_routing is True
    assert frame.no_automatic_architecture_escalation is True
    assert frame.no_automatic_roadmap_synthesis is True


def test_tc_reasoningscope_03_architecture_guard_blocks_low_task_expansion() -> None:
    frame = ArchitectureReasoningGuardPolicy().guard(
        complexity="LOW",
        requested_runtime_count=4,
        continuity_size=4_000,
        governance_sensitive=True,
    )

    assert frame.architecture_wide_reasoning_forbidden is True
    assert frame.broad_runtime_synthesis_prevented is True
    assert frame.unnecessary_governance_synthesis_prevented is True
    assert frame.giant_architecture_continuity_replay_prevented is True
    assert frame.no_automatic_architecture_escalation is True


def test_tc_reasoningscope_04_local_patch_mode_uses_file_and_contract_neighborhood() -> None:
    frame = LocalPatchModePolicy().scope(
        touched_files=("b.py", "a.py"),
        affected_runtimes=("runtime_graph", "reasoning_scope"),
        adjacent_contracts=("ContractB", "ContractA"),
    )

    assert frame.local_runtime_only_reasoning is True
    assert frame.file_neighborhood_reasoning == ("a.py", "b.py")
    assert frame.adjacent_contract_only_reasoning == ("ContractA", "ContractB")
    assert frame.no_roadmap_expansion is True
