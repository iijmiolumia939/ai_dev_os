from __future__ import annotations

from ai_dev_os.subagent_execution import SubagentExecutionRuntime


def test_tc_subagentexec_08_governance_blocks_swarm_and_recursive_delegation() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.subagent_governance_active is True
    assert frame.governance.autonomous_swarm_emergence_prevented is True
    assert frame.governance.recursive_delegation_trees_prevented is True
    assert frame.governance.uncontrolled_execution_fanout_prevented is True
    assert frame.governance.recursive_delegation_attempts == 2
    assert "swarm_blocked" in frame.governance.compact_governance_warnings


def test_tc_subagentexec_09_pressure_and_eviction_are_compact_and_bounded() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.pressure.bounded_delegation_only is True
    assert frame.pressure.swarm_pressure == "BLOCKED"
    assert frame.eviction.subagent_eviction_active is True
    assert frame.eviction.compact_useful_delegation_heuristics_only is True
    assert "repo_wide_delegate_request" in frame.eviction.evicted_oversized_execution_payloads
    assert "single_layer_local_patch" in frame.eviction.preserved_compact_delegation_heuristics


def test_tc_subagentexec_10_recommendations_are_non_binding_and_human_confirmed() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.recommendation.non_binding is True
    assert frame.recommendation.human_confirmed is True
    assert frame.recommendation.compact is True
    assert frame.recommendation.deterministic is True
    assert "HIGH_for_governance" in frame.recommendation.routing_recommendations
