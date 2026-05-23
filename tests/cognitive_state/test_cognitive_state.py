from __future__ import annotations

from ai_dev_os.cognitive_state import (
    COGNITIVE_STATE_REQUIREMENT_IDS,
    COGNITIVE_STATE_TEST_IDS,
    MAX_ATTENTION_TARGETS,
    MAX_CONTEXT_SALIENCE_ITEMS,
    MAX_WORKING_MEMORY_ITEMS,
    CognitiveStateRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_cognitivestate_01_active_frame_is_local_patch_bounded() -> None:
    frame = CognitiveStateRuntime().evaluate()

    assert frame.cognitive_state_active is True
    assert frame.requirement_ids == COGNITIVE_STATE_REQUIREMENT_IDS
    assert frame.test_ids == COGNITIVE_STATE_TEST_IDS
    assert frame.active.local_provider_only is True
    assert frame.active.high_tier_escalation_blocked is True
    assert frame.active.cognitive_operations_execute_commands is False
    assert frame.local_patch_compatible is True


def test_tc_cognitivestate_02_working_memory_is_bounded() -> None:
    frame = CognitiveStateRuntime().evaluate(
        working_memory_items=tuple(f"memory-{index}" for index in range(12))
    )

    assert frame.working_memory.item_count == MAX_WORKING_MEMORY_ITEMS
    assert frame.working_memory.memory_pressure == "HIGH"
    assert frame.working_memory.memory_overflow_blocked is True
    assert len(frame.working_memory.bounded_items) == MAX_WORKING_MEMORY_ITEMS


def test_tc_cognitivestate_03_attention_distribution_is_deterministic() -> None:
    weights = {"validation": 20, "tests": 30, "implementation": 50, "vscode": 10}
    first = CognitiveStateRuntime().evaluate(attention_weights=weights)
    second = CognitiveStateRuntime().evaluate(attention_weights=weights)

    assert first.attention.attention_distribution == second.attention.attention_distribution
    assert first.attention.primary_focus == "implementation"
    assert first.attention.attention_target_count == MAX_ATTENTION_TARGETS


def test_tc_cognitivestate_04_context_salience_is_compact() -> None:
    context_items = tuple(f"context-{index}" for index in range(9))
    frame = CognitiveStateRuntime().evaluate(context_items=context_items)

    assert len(frame.salience.salient_context) == MAX_CONTEXT_SALIENCE_ITEMS
    assert "context-5" in frame.salience.ignored_context
    assert frame.salience.bounded_context_window == MAX_CONTEXT_SALIENCE_ITEMS


def test_tc_cognitivestate_05_decay_status_escalates_without_provider_escalation() -> None:
    frame = CognitiveStateRuntime().evaluate(
        session_age_pressure=58,
        recursive_reasoning_attempts=1,
    )

    assert frame.decay.decay_status == "RESET_RECOMMENDED"
    assert frame.decay.recursive_reasoning_risk_detected is True
    assert frame.bounded_memory.no_provider_escalation is True
    assert frame.provider_routing == "LOCAL_FIRST_NO_HIGH_TIER_COGNITION"


def test_tc_cognitivestate_06_execution_focus_integrates_execution_runtimes() -> None:
    frame = CognitiveStateRuntime().evaluate()

    assert frame.execution_focus.mediation_focus_active is True
    assert frame.execution_focus.continuation_focus_active is True
    assert frame.execution_focus.recovery_focus_active is True
    assert frame.execution_focus.coordination_focus_active is True
    assert frame.execution_focus.autonomous_execution_loop_blocked is True


def test_tc_cognitivestate_07_bounded_memory_blocks_hidden_mutation() -> None:
    frame = CognitiveStateRuntime().evaluate(hidden_memory_mutation_attempts=1)

    assert frame.working_memory.recursive_memory_expansion_blocked is True
    assert frame.bounded_memory.no_autonomous_memory_mutation is False
    assert frame.bounded_memory.rollback_safe is True
    assert frame.bounded_memory.governance_preserving is True


def test_tc_cognitivestate_08_context_replay_and_repo_wide_scope_are_blocked() -> None:
    frame = CognitiveStateRuntime().evaluate(
        repo_wide_context_attempts=1,
        raw_transcript_replay_attempts=1,
    )

    assert frame.salience.repo_wide_context_blocked is True
    assert frame.salience.raw_transcript_replay_blocked is True
    assert frame.bounded is True


def test_tc_cognitivestate_09_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().cognitive_state

    assert report.cognitive_state_active is True
    assert report.attention_distribution[0].startswith("implementation:")
    assert report.memory_pressure == "MEDIUM"
    assert report.decay_status == "STABLE"


def test_tc_cognitivestate_10_runtime_is_deterministic() -> None:
    first = CognitiveStateRuntime().evaluate()
    second = CognitiveStateRuntime().evaluate()

    assert first == second
    assert first.deterministic is True
    assert first.rollback_safe is True
    assert first.governance_preserving is True
