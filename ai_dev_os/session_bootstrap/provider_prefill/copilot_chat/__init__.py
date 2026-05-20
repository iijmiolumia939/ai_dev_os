from __future__ import annotations

from ai_dev_os.session_bootstrap.provider_prefill import (
    ProviderPrefillFrame,
    ProviderPrefillPolicy,
)


class CopilotChatPrefillAdapter:
    provider_name = "github_copilot_chat"

    def prefill(
        self,
        *,
        draft_text: str,
        continuity_text: str,
        sprint_prompt_text: str,
        bootstrap_preview_text: str,
        provider_available: bool = True,
        prefill_api_available: bool = True,
        visible_draft_confirmed: bool = True,
    ) -> ProviderPrefillFrame:
        supported = provider_available and prefill_api_available
        attempted = supported and bool(draft_text)
        success = attempted and visible_draft_confirmed
        fallback = not success
        warnings = tuple(
            warning
            for warning in (
                "copilot_provider_unavailable" if not provider_available else "",
                "copilot_prefill_api_unavailable" if provider_available and not supported else "",
                "copilot_visible_draft_not_confirmed" if attempted and not success else "",
                "clipboard_fallback_ready" if fallback else "",
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
                injection_strategy="copilot_chat_query_prefill",
                fallback_behavior="clipboard_fallback" if fallback else "none",
                clipboard_fallback_active=fallback,
                injection_failed=attempted and not success,
                provider_unsupported=not supported,
                enter_only_confidence="",
                observable_events=(
                    "copilot_chat_open",
                    "copilot_draft_prefill_attempted" if attempted else "",
                    "copilot_draft_visible" if success else "",
                ),
                auto_send=False,
                hidden_continuation=False,
                silent_dispatch=False,
                background_prompt_execution=False,
                warnings=warnings,
            )
        )
