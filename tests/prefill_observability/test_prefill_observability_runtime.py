from __future__ import annotations

from ai_dev_os.session_bootstrap.draft_injection import DraftInjectionPolicy
from ai_dev_os.session_bootstrap.provider_prefill import (
    CLIPBOARD_ONLY,
    ENTER_ONLY_READY,
    PREFILL_PARTIAL,
    PrefillObservabilityPolicy,
)
from ai_dev_os.session_bootstrap.provider_prefill.copilot_chat import CopilotChatPrefillAdapter
from ai_dev_os.session_bootstrap.provider_prefill.vscode_chat import VSCodeChatPrefillAdapter


def test_tc_prefill_01_observability_reports_prefill_success() -> None:
    provider = CopilotChatPrefillAdapter().prefill(
        draft_text="draft",
        continuity_text="continuity",
        sprint_prompt_text="prompt",
        bootstrap_preview_text="preview",
    )
    frame = PrefillObservabilityPolicy().observe(provider)

    assert frame.prefill_success is True
    assert frame.clipboard_fallback is False
    assert frame.provider_unsupported is False
    assert frame.enter_only_confidence == ENTER_ONLY_READY
    assert "prefill_success" in frame.observable_events


def test_tc_prefill_02_observability_reports_injection_failure() -> None:
    provider = VSCodeChatPrefillAdapter().prefill(
        draft_text="draft",
        continuity_text="continuity",
        sprint_prompt_text="prompt",
        bootstrap_preview_text="preview",
        draft_visibility_confirmed=False,
    )
    frame = PrefillObservabilityPolicy().observe(provider)

    assert frame.prefill_success is False
    assert frame.clipboard_fallback is True
    assert frame.injection_failed is True
    assert frame.enter_only_confidence == PREFILL_PARTIAL
    assert "injection_failed" in frame.observable_events


def test_tc_prefill_03_observability_reports_provider_unsupported() -> None:
    draft = DraftInjectionPolicy().build(
        project_name="ai_dev_os",
        requested_target="unsupported_provider",
    )

    assert draft.observability is not None
    assert draft.observability.provider_unsupported is True
    assert draft.observability.clipboard_fallback is True
    assert draft.enter_only_confidence == CLIPBOARD_ONLY


def test_tc_prefill_04_observability_is_summary_only_and_bounded() -> None:
    draft = DraftInjectionPolicy().build(project_name="ai_dev_os", requested_target="vscode_chat")

    assert draft.observability is not None
    assert draft.observability.summary_only is True
    assert draft.observability.estimated_avoided_handoff_friction > 0
    assert "full_history" in draft.preview.excluded_stale_context


def test_tc_prefill_05_runtime_audit_exposes_enter_only_confidence() -> None:
    from ai_dev_os.runtime_audit import audit_draft_injection

    audit = audit_draft_injection()

    assert audit.provider_prefill_active is True
    assert audit.copilot_prefill_active is True
    assert audit.vscode_chat_prefill_active is True
    assert audit.prefill_observability_active is True
    assert audit.enter_only_confidence == ENTER_ONLY_READY
