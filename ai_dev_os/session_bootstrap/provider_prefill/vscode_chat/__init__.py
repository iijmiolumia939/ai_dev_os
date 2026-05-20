from __future__ import annotations

from ai_dev_os.session_bootstrap.provider_prefill import (
    ProviderPrefillFrame,
    ProviderPrefillPolicy,
)


class VSCodeChatPrefillAdapter:
    provider_name = "vscode_chat"

    def prefill(
        self,
        *,
        draft_text: str,
        continuity_text: str,
        sprint_prompt_text: str,
        bootstrap_preview_text: str,
        provider_detected: bool = True,
        input_injection_supported: bool = True,
        draft_visibility_confirmed: bool = True,
    ) -> ProviderPrefillFrame:
        supported = provider_detected and input_injection_supported
        attempted = supported and bool(draft_text)
        success = attempted and draft_visibility_confirmed
        fallback = not success
        warnings = tuple(
            warning
            for warning in (
                "vscode_chat_provider_not_detected" if not provider_detected else "",
                (
                    "vscode_chat_input_injection_unsupported"
                    if provider_detected and not supported
                    else ""
                ),
                "vscode_chat_draft_visibility_unconfirmed" if attempted and not success else "",
                "clipboard_fallback_escalated" if fallback else "",
            )
            if warning
        )
        return ProviderPrefillPolicy().evaluate(
            ProviderPrefillFrame(
                provider_name=self.provider_name,
                prefill_supported=supported,
                prefill_attempted=attempted,
                prefill_success=success,
                awaiting_human_send=success or fallback,
                chat_opened=supported,
                continuity_injected=success and bool(continuity_text),
                sprint_prompt_injected=success and bool(sprint_prompt_text),
                bootstrap_preview_available=bool(bootstrap_preview_text),
                injection_strategy="vscode_chat_partial_query_prefill",
                fallback_behavior="clipboard_fallback" if fallback else "none",
                clipboard_fallback_active=fallback,
                injection_failed=attempted and not success,
                provider_unsupported=not supported,
                enter_only_confidence="",
                observable_events=(
                    "vscode_chat_provider_detected" if provider_detected else "",
                    "vscode_chat_input_injection_attempted" if attempted else "",
                    "vscode_chat_draft_visible" if success else "",
                ),
                auto_send=False,
                hidden_continuation=False,
                silent_dispatch=False,
                background_prompt_execution=False,
                warnings=warnings,
            )
        )
