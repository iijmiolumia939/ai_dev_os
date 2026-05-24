from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.streaming_cognition import (
    CONTINUATION_ENTROPY_THRESHOLD,
    MAX_COGNITION_DELTAS,
    MAX_CONTINUATION_ITEMS,
    MAX_PROVIDER_WINDOW,
    MAX_SPEECH_CHUNKS,
    MAX_STREAMING_HISTORY,
    STREAMING_BUDGET_LIMIT,
    STREAMING_COGNITION_REQUIREMENT_IDS,
    STREAMING_COGNITION_TEST_IDS,
    StreamingCognitionRuntime,
)


def test_tc_streamingcognition_01_active_runtime_is_bounded_local_patch() -> None:
    frame = StreamingCognitionRuntime().evaluate()

    assert frame.streaming_cognition_active is True
    assert frame.requirement_ids == STREAMING_COGNITION_REQUIREMENT_IDS
    assert frame.test_ids == STREAMING_COGNITION_TEST_IDS
    assert frame.deterministic is True
    assert frame.bounded is True
    assert frame.rollback_safe is True
    assert frame.governance_preserving is True
    assert frame.local_patch_compatible is True
    assert frame.streaming_mode == "LOCAL_PATCH_BOUNDED_STREAMING_COGNITION"


def test_tc_streamingcognition_02_speech_and_cognition_continuation_are_bounded() -> None:
    speech = tuple(f"speech_{index}" for index in range(8))
    deltas = tuple(f"delta_{index}" for index in range(8))
    continuation = tuple(f"continuation_{index}" for index in range(6))

    frame = StreamingCognitionRuntime().evaluate(
        speech_chunks=speech,
        cognition_deltas=deltas,
        continuation_items=continuation,
    )

    assert len(frame.speech.speech_chunks) == MAX_SPEECH_CHUNKS
    assert len(frame.delta.cognition_deltas) == MAX_COGNITION_DELTAS
    assert len(frame.continuation.continuation_items) == MAX_CONTINUATION_ITEMS
    assert frame.speech.speech_continuation == speech[MAX_SPEECH_CHUNKS - 2 : MAX_SPEECH_CHUNKS]
    assert frame.delta.delta_overflow_blocked is True
    assert frame.eviction.evicted_speech_chunks == speech[MAX_SPEECH_CHUNKS:]
    assert frame.eviction.evicted_cognition_deltas == deltas[MAX_COGNITION_DELTAS:]


def test_tc_streamingcognition_03_interruption_recovery_resets_speech_safely() -> None:
    frame = StreamingCognitionRuntime().evaluate(interrupted=True, interruption_pressure=3)

    assert frame.interruption.interruption_detected is True
    assert frame.interruption.speech_reset_required is True
    assert frame.speech.speech_chunks == ()
    assert frame.speech.speech_reset_on_interruption is True
    assert frame.interruption.continuation_reset_safe is True
    assert frame.interruption.provider_stabilization_required is True
    assert "INTERRUPTION_PRESSURE_THRESHOLD_EXCEEDED" in frame.termination.termination_reasons


def test_tc_streamingcognition_04_provider_streaming_fallback_is_local_first() -> None:
    providers = tuple(f"provider_{index}" for index in range(6))
    frame = StreamingCognitionRuntime().evaluate(
        provider_candidates=providers,
        provider_failures=2,
        provider_cooldown_windows=2,
        provider_fatigue_score=66,
    )

    assert len(frame.provider.provider_order) == MAX_PROVIDER_WINDOW
    assert frame.provider.local_first_streaming is True
    assert frame.provider.provider_fallback_active is True
    assert frame.provider.recommended_provider == "local-summary-provider"
    assert frame.provider.bounded_provider_recommendation == "USE_LOCAL_SUMMARY_FALLBACK"
    assert frame.eviction.evicted_provider_items == providers[MAX_PROVIDER_WINDOW:]


def test_tc_streamingcognition_05_streaming_continuation_persistence_reuses_summary() -> None:
    frame = StreamingCognitionRuntime().evaluate(
        continuation_items=("topic", "buffer", "cooldown", "extra"),
        continuation_entropy=CONTINUATION_ENTROPY_THRESHOLD,
    )

    assert frame.continuation.continuation_persistence_reuse is True
    assert frame.continuation.continuation_reset_governed is True
    assert frame.continuation.entropy_suppression_active is True
    assert frame.continuation.deterministic_continuation_summary == "topic;buffer;cooldown"
    assert "CONTINUATION_ENTROPY_THRESHOLD_EXCEEDED" in frame.termination.termination_reasons


def test_tc_streamingcognition_06_recursive_streaming_and_governance_are_blocked() -> None:
    frame = StreamingCognitionRuntime().evaluate(
        recursive_streaming_attempts=1,
        hidden_realtime_agent_attempts=1,
        self_expanding_narration_attempts=1,
        retrieval_scope_widening_attempts=1,
        governance_policy_mutation_attempts=1,
    )

    assert frame.governance.recursive_streaming_blocked is True
    assert frame.governance.hidden_realtime_agents_blocked is True
    assert frame.governance.self_expanding_narration_blocked is True
    assert frame.governance.retrieval_scope_widening_blocked is True
    assert frame.governance.governance_policy_mutation_blocked is True
    assert frame.governance.read_only_projection_enforced is True
    assert frame.termination.recursive_streaming_detected is True
    assert frame.termination.governance_violation_detected is True


def test_tc_streamingcognition_07_streaming_termination_handles_budget() -> None:
    frame = StreamingCognitionRuntime().evaluate(streaming_budget_used=STREAMING_BUDGET_LIMIT + 1)

    assert frame.budget.streaming_budget_exceeded is True
    assert frame.budget.budget_pressure == "OVER_BUDGET"
    assert frame.termination.streaming_terminated is True
    assert "STREAMING_BUDGET_EXCEEDED" in frame.termination.termination_reasons


def test_tc_streamingcognition_08_bounded_streaming_retention_and_audit_projection() -> None:
    history = tuple(f"history_{index}" for index in range(9))
    frame = StreamingCognitionRuntime().evaluate(streaming_history_items=history)
    report = run_runtime_enforcement_audit().streaming_cognition

    assert len(frame.history.streaming_history) == MAX_STREAMING_HISTORY
    assert frame.history.history_overflow_blocked is True
    assert frame.eviction.evicted_history_items == history[MAX_STREAMING_HISTORY:]
    assert frame.confidence.deterministic_confidence is True
    assert report.streaming_cognition_active is True
    assert 0 <= report.streaming_latency_score <= 100
    assert 0 <= report.interruption_recovery_score <= 100
    assert 0 <= report.provider_streaming_score <= 100
    assert 0 <= report.continuation_streaming_score <= 100
    assert 0 <= report.bounded_cognition_score <= 100
    assert report.estimated_avoided_streaming_instability > 0
    assert report.estimated_avoided_provider_interruptions > 0
    assert report.estimated_avoided_frontier_streaming > 0


def test_tc_streamingcognition_09_runtime_is_deterministic() -> None:
    first = StreamingCognitionRuntime().evaluate()
    second = StreamingCognitionRuntime().evaluate()

    assert first == second
    assert (
        first.history.deterministic_streaming_summary
        == second.history.deterministic_streaming_summary
    )
    assert first.confidence.realtime_survivability_confidence is True
