from __future__ import annotations

import pytest

from ai_dev_os.session_bootstrap.draft_injection import DraftInjectionPolicy
from ai_dev_os.session_bootstrap.provider_prefill import (
    CLIPBOARD_ONLY,
    ENTER_ONLY_READY,
    PREFILL_PARTIAL,
    ProviderPrefillFrame,
)
from ai_dev_os.session_bootstrap.provider_prefill.clipboard_fallback import (
    ClipboardFallbackPrefillAdapter,
)
from ai_dev_os.session_bootstrap.provider_prefill.copilot_chat import CopilotChatPrefillAdapter
from ai_dev_os.session_bootstrap.provider_prefill.vscode_chat import VSCodeChatPrefillAdapter


def test_tc_prefill_01_provider_detection_supports_copilot_and_vscode() -> None:
    copilot = DraftInjectionPolicy().build(
        project_name="ai_dev_os",
        requested_target="copilot_chat",
    )
    vscode = DraftInjectionPolicy().build(
        project_name="ai_dev_os",
        requested_target="vscode_chat",
    )

    assert copilot.provider_name == "github_copilot_chat"
    assert copilot.prefill_supported is True
    assert vscode.provider_name == "vscode_chat"
    assert vscode.prefill_supported is True


def test_tc_prefill_02_copilot_prefill_success_stops_at_human_send() -> None:
    frame = CopilotChatPrefillAdapter().prefill(
        draft_text="draft",
        continuity_text="continuity",
        sprint_prompt_text="prompt",
        bootstrap_preview_text="preview",
    )

    assert frame.prefill_attempted is True
    assert frame.prefill_success is True
    assert frame.awaiting_human_send is True
    assert frame.enter_only_confidence == ENTER_ONLY_READY
    assert frame.auto_send is False
    assert frame.silent_dispatch is False


def test_tc_prefill_03_vscode_visibility_failure_escalates_to_partial_fallback() -> None:
    frame = VSCodeChatPrefillAdapter().prefill(
        draft_text="draft",
        continuity_text="continuity",
        sprint_prompt_text="prompt",
        bootstrap_preview_text="preview",
        draft_visibility_confirmed=False,
    )

    assert frame.prefill_supported is True
    assert frame.prefill_attempted is True
    assert frame.prefill_success is False
    assert frame.clipboard_fallback_active is True
    assert frame.injection_failed is True
    assert frame.enter_only_confidence == PREFILL_PARTIAL


def test_tc_prefill_04_unsupported_provider_is_clipboard_only() -> None:
    frame = ClipboardFallbackPrefillAdapter().prefill(
        draft_text="draft",
        continuity_text="continuity",
        sprint_prompt_text="prompt",
        bootstrap_preview_text="preview",
    )

    assert frame.prefill_supported is False
    assert frame.provider_unsupported is True
    assert frame.clipboard_fallback_active is True
    assert frame.enter_only_confidence == CLIPBOARD_ONLY
    assert frame.awaiting_human_send is True


def test_tc_prefill_05_provider_frame_rejects_auto_send() -> None:
    with pytest.raises(ValueError):
        ProviderPrefillFrame(
            provider_name="vscode_chat",
            prefill_supported=True,
            prefill_attempted=True,
            prefill_success=True,
            awaiting_human_send=True,
            chat_opened=True,
            continuity_injected=True,
            sprint_prompt_injected=True,
            bootstrap_preview_available=True,
            injection_strategy="vscode_chat_partial_query_prefill",
            fallback_behavior="none",
            clipboard_fallback_active=False,
            injection_failed=False,
            provider_unsupported=False,
            enter_only_confidence=ENTER_ONLY_READY,
            observable_events=(),
            auto_send=True,
            hidden_continuation=False,
            silent_dispatch=False,
            background_prompt_execution=False,
            warnings=(),
        )
