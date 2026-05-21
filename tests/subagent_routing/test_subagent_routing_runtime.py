from __future__ import annotations

from ai_dev_os.provider_routing import ProviderRoutingRuntime
from ai_dev_os.subagent_execution import SubagentExecutionRuntime


def test_tc_subagentexec_05_routes_task_classes_to_provider_tiers() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.routing.task_routes["repetitive_tests"] == "LOW_LOCAL"
    assert frame.routing.task_routes["compact_summaries"] == "LOW_GOVERNANCE"
    assert frame.routing.task_routes["integration_sequencing"] == "MEDIUM"
    assert frame.routing.task_routes["architecture"] == "HIGH"
    assert frame.routing.low_local_provider == "ollama:qwen2.5-coder:7b"
    assert frame.routing.low_governance_provider == "ollama:gemma3:12b"
    assert frame.routing.high_provider == "GPT-5.5 premium governance provider"


def test_tc_subagentexec_06_routing_blocks_unsafe_local_governance_and_high_reasoning() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.routing.unsafe_local_governance_delegation_prevented is True
    assert frame.routing.high_reasoning_local_delegation_prevented is True
    assert frame.routing.hidden_provider_switching_prevented is True
    assert frame.no_hidden_provider_switching is True


def test_tc_subagentexec_07_provider_routing_integrates_subagent_distribution() -> None:
    frame = ProviderRoutingRuntime().evaluate(cognition_tier="LOW", compact_summary=True)

    assert frame.subagent_execution.subagent_routing_active is True
    assert frame.subagent_execution.routing.provider_routing_distribution == {
        "LOW_LOCAL": 5,
        "LOW_GOVERNANCE": 2,
        "MEDIUM": 2,
        "HIGH": 1,
    }
