from __future__ import annotations

from ai_dev_os.session_bootstrap.provider_prefill import (
    ProviderPrefillFrame,
    ProviderPrefillPolicy,
)


class ClipboardFallbackPrefillAdapter:
    provider_name = "clipboard_fallback"

    def prefill(
        self,
        *,
        draft_text: str,
        continuity_text: str,
        sprint_prompt_text: str,
        bootstrap_preview_text: str,
        clipboard_available: bool = True,
    ) -> ProviderPrefillFrame:
        fallback = bool(draft_text) and clipboard_available
        warnings = ("clipboard_only_rollover",) if fallback else ("clipboard_unavailable",)
        return ProviderPrefillPolicy().evaluate(
            ProviderPrefillFrame(
                provider_name=self.provider_name,
                prefill_supported=False,
                prefill_attempted=False,
                prefill_success=False,
                awaiting_human_send=fallback,
                chat_opened=False,
                continuity_injected=False,
                sprint_prompt_injected=False,
                bootstrap_preview_available=bool(bootstrap_preview_text),
                injection_strategy="clipboard_write_only",
                fallback_behavior="clipboard_fallback",
                clipboard_fallback_active=fallback,
                injection_failed=False,
                provider_unsupported=True,
                enter_only_confidence="",
                observable_events=(
                    "clipboard_fallback_ready" if fallback else "",
                    "continuity_available" if continuity_text else "",
                    "sprint_prompt_available" if sprint_prompt_text else "",
                ),
                auto_send=False,
                hidden_continuation=False,
                silent_dispatch=False,
                background_prompt_execution=False,
                warnings=warnings,
            )
        )
