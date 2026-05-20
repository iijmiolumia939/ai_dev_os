from __future__ import annotations

import pytest

from ai_dev_os.session_bootstrap.chat_launch import ChatLaunchPolicy
from ai_dev_os.session_bootstrap.chat_target_detection import ChatTargetDetectionPolicy
from ai_dev_os.session_bootstrap.draft_injection import (
    CopilotDraftInjectionFrame,
    DraftInjectionPolicy,
)


def test_tc_draftinject_01_builds_visible_enter_only_draft() -> None:
    frame = DraftInjectionPolicy().build(project_name="ai_dev_os", sprint_id="next")

    assert frame.chat_opened is True
    assert frame.draft_prefilled is True
    assert frame.continuity_injected is True
    assert frame.awaiting_human_send is True
    assert "AI_DEV_OS Bootstrap Draft" in frame.draft_text
    assert "The final Enter/Send is a human action." in frame.draft_text
    assert "AI_DEV_OS ENTER_ONLY_READY" in frame.status_bar_states
    assert frame.enter_only_confidence == "ENTER_ONLY_READY"


def test_tc_draftinject_02_never_enables_hidden_or_background_send() -> None:
    frame = DraftInjectionPolicy().build(project_name="ai_dev_os")

    assert frame.auto_send is False
    assert frame.hidden_continuation is False
    assert frame.background_message_dispatch is False
    assert frame.silent_prompt_mutation is False
    assert frame.authority_escalation_used is False


def test_tc_draftinject_03_preview_reports_compact_context_and_stale_exclusions() -> None:
    frame = DraftInjectionPolicy().build(project_name="ai_dev_os")

    assert frame.preview.estimated_token_size > 0
    assert "FR-DRAFTINJECT-01" in frame.preview.included_continuity
    assert "TC-DRAFTINJECT-05" in frame.preview.included_continuity
    assert "full_history" in frame.preview.excluded_stale_context
    assert "old_sprint_logs" in frame.preview.excluded_stale_context


def test_tc_draftinject_04_clipboard_fallback_keeps_human_send_boundary() -> None:
    target = ChatTargetDetectionPolicy().detect(
        requested_target="unknown_chat",
        available_targets=("vscode_chat",),
        clipboard_fallback_allowed=True,
    )
    launch = ChatLaunchPolicy().launch(target)

    assert target.fallback_required is True
    assert launch.chat_opened is False
    assert launch.clipboard_fallback_active is True
    assert launch.awaiting_human_send is True
    assert launch.send_dispatched is False
    assert launch.background_dispatch_used is False


def test_tc_draftinject_05_rejects_authority_escalation_flags() -> None:
    preview = DraftInjectionPolicy().build(project_name="ai_dev_os").preview

    with pytest.raises(ValueError):
        CopilotDraftInjectionFrame(
            chat_opened=True,
            draft_prefilled=True,
            continuity_injected=True,
            awaiting_human_send=True,
            draft_text="draft",
            preview=preview,
            target="vscode_chat",
            clipboard_fallback_active=False,
            auto_send=True,
            hidden_continuation=False,
            background_message_dispatch=False,
            silent_prompt_mutation=False,
            authority_escalation_used=False,
            status_bar_states=("AI_DEV_OS ENTER_READY", "AI_DEV_OS WAITING_FOR_SEND"),
            warnings=(),
        )
