from __future__ import annotations

from ai_dev_os.dev_loop import (
    SprintClosureRuntime,
    SprintContinuityRuntime,
    SprintLifecycleRuntime,
    SprintRolloverRuntime,
)


def test_tc_aidevloop_04_lifecycle_transitions_are_bounded_and_gated() -> None:
    validating = SprintLifecycleRuntime().transition(
        state="VALIDATING",
        validation_passed=False,
        sprint_age_days=1,
        continuity_tokens=900,
    )
    closing = SprintLifecycleRuntime().transition(
        state="CLOSING",
        validation_passed=True,
        sprint_age_days=1,
        continuity_tokens=900,
    )

    assert validating.next_allowed_states == ("ACTIVE",)
    assert validating.validation_gate_required is True
    assert validating.validation_gate_passed is False
    assert closing.next_allowed_states == ("ROLLOVER_READY",)
    assert closing.bounded_transition is True


def test_tc_aidevloop_05_stale_sprint_detection_and_rollover_are_compact() -> None:
    lifecycle = SprintLifecycleRuntime().transition(
        state="ROLLOVER_READY",
        validation_passed=True,
        sprint_age_days=21,
        continuity_tokens=4_500,
    )
    closure = SprintClosureRuntime().close(
        validation_summary="pytest pass; audit pass",
        changed_runtimes=("dev_loop", "runtime_audit", "provider_routing"),
        remaining_deltas=("vscode_extension",),
    )
    rollover = SprintRolloverRuntime().prepare(closure=closure, lifecycle=lifecycle)

    assert lifecycle.stale_sprint_detected is True
    assert closure.compact_closure_ready is True
    assert closure.full_history_replay_forbidden is True
    assert rollover.rollover_ready is True
    assert rollover.stale_sprint_evicted is True
    assert rollover.infinite_sprint_chaining_prevented is True


def test_tc_aidevloop_06_continuity_is_delta_only() -> None:
    closure = SprintClosureRuntime().close(
        validation_summary="validation pass",
        changed_runtimes=("dev_loop", "runtime_audit"),
        remaining_deltas=("extension", "docs"),
    )
    continuity = SprintContinuityRuntime().compact(
        closure=closure,
        stale_sprints=("sprint-1", "sprint-2", "sprint-3", "sprint-4", "sprint-5"),
    )

    assert continuity.delta_only_carryover == (
        "dev_loop",
        "runtime_audit",
        "extension",
        "docs",
    )
    assert continuity.stale_sprint_eviction == ("sprint-1", "sprint-2", "sprint-3", "sprint-4")
    assert continuity.giant_continuity_replay_forbidden is True
    assert continuity.full_sprint_history_replay_forbidden is True
    assert continuity.hidden_continuity_accumulation_forbidden is True
