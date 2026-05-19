from __future__ import annotations

from ai_dev_os.session_boundary.boundary_enforcement import (
    ACTIVE,
    ROLLOVER_REQUIRED,
    STALE_BLOCKED,
    BoundaryEnforcementPolicy,
)
from ai_dev_os.session_boundary.handoff_confirmation import HandoffConfirmationPolicy
from ai_dev_os.session_boundary.rollover_state import RolloverStatePolicy
from ai_dev_os.session_boundary.session_generation import SessionGenerationPolicy
from ai_dev_os.session_boundary.stale_session_detection import StaleSessionDetectionPolicy


def test_generation_increment_validation() -> None:
    frame = SessionGenerationPolicy().generate(
        session_id="s-1",
        session_generation=4,
        rollover_recommended=True,
        parent_session="s-0",
    )

    assert frame.session_generation == 4
    assert frame.rollover_generation == 5
    assert frame.active_generation == 5
    assert frame.full_history_replay_allowed is False


def test_stale_session_detection_after_ignored_rollover() -> None:
    generation = SessionGenerationPolicy().generate(
        session_id="s-1", session_generation=2, rollover_recommended=True
    )
    frame = StaleSessionDetectionPolicy().detect(
        generation=generation,
        rollover_recommended=True,
        handoff_generated=True,
        new_session_started=False,
        continuity_generation=1,
        architecture_topic_count=4,
        continuity_token_estimate=16_000,
        session_age=8,
        stale_continuity_reuse=True,
    )

    assert frame.rollover_recommended_but_ignored is True
    assert frame.stale_generation_mismatch is True
    assert frame.stale_session_detected is True
    assert frame.boundary_violation_risk == "high"
    assert frame.forced_compaction_recommended is True
    assert frame.new_session_required is True


def test_boundary_enforcement_state_transitions() -> None:
    generation = SessionGenerationPolicy().generate(session_id="s-1")
    clean = StaleSessionDetectionPolicy().detect(
        generation=generation,
        rollover_recommended=False,
        handoff_generated=False,
        new_session_started=False,
        continuity_generation=1,
    )
    warning = StaleSessionDetectionPolicy().detect(
        generation=generation,
        rollover_recommended=False,
        handoff_generated=False,
        new_session_started=False,
        continuity_generation=1,
        architecture_topic_count=3,
    )
    blocked = StaleSessionDetectionPolicy().detect(
        generation=generation,
        rollover_recommended=True,
        handoff_generated=True,
        new_session_started=False,
        continuity_generation=0,
        continuity_token_estimate=20_000,
    )

    assert BoundaryEnforcementPolicy().enforce(stale_session=clean).enforcement_state == ACTIVE
    assert (
        BoundaryEnforcementPolicy().enforce(stale_session=warning).enforcement_state
        == ROLLOVER_REQUIRED
    )
    enforced = BoundaryEnforcementPolicy().enforce(stale_session=blocked)
    assert enforced.enforcement_state == STALE_BLOCKED
    assert enforced.session_continue_allowed is False
    assert enforced.compact_only_allowed is True
    assert enforced.ai_response_blocking_enforced is False


def test_rollover_state_validation() -> None:
    frame = RolloverStatePolicy().evaluate(
        rollover_required=True,
        handoff_generated=True,
        clipboard_ready=True,
        export_ready=True,
        confirmed=False,
        new_session_started=False,
        stale_session_active=True,
    )

    assert frame.rollover_pending is True
    assert frame.confirmation_pending is True
    assert frame.stale_session_active is True


def test_handoff_confirmation_is_human_confirmed_without_ui_automation() -> None:
    frame = HandoffConfirmationPolicy().confirm(
        export_consumed=True,
        prompt_copied=True,
        new_session_acknowledged=True,
        stale_session_closed=True,
    )

    assert frame.handoff_confirmed is True
    assert frame.human_confirmed is True
    assert frame.ui_automation_used is False
