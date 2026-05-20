from __future__ import annotations

from dataclasses import dataclass

ENTER_ONLY_READY = "ENTER_ONLY_READY"
PREFILL_PARTIAL = "PREFILL_PARTIAL"
CLIPBOARD_ONLY = "CLIPBOARD_ONLY"


@dataclass(frozen=True)
class ProviderPrefillFrame:
    provider_name: str
    prefill_supported: bool
    prefill_attempted: bool
    prefill_success: bool
    awaiting_human_send: bool
    chat_opened: bool
    continuity_injected: bool
    sprint_prompt_injected: bool
    bootstrap_preview_available: bool
    injection_strategy: str
    fallback_behavior: str
    clipboard_fallback_active: bool
    injection_failed: bool
    provider_unsupported: bool
    enter_only_confidence: str
    observable_events: tuple[str, ...]
    auto_send: bool
    hidden_continuation: bool
    silent_dispatch: bool
    background_prompt_execution: bool
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            self.auto_send
            or self.hidden_continuation
            or self.silent_dispatch
            or self.background_prompt_execution
        ):
            raise ValueError("provider prefill must stop before automated send or dispatch")


@dataclass(frozen=True)
class PrefillObservabilityFrame:
    provider_name: str
    prefill_success: bool
    clipboard_fallback: bool
    injection_failed: bool
    provider_unsupported: bool
    enter_only_confidence: str
    current_status: str
    observable_events: tuple[str, ...]
    estimated_avoided_handoff_friction: int
    summary_only: bool
    warnings: tuple[str, ...]


class EnterOnlyConfidencePolicy:
    def classify(self, frame: ProviderPrefillFrame) -> str:
        if frame.prefill_success and frame.awaiting_human_send:
            return ENTER_ONLY_READY
        if frame.prefill_attempted and frame.clipboard_fallback_active:
            return PREFILL_PARTIAL
        return CLIPBOARD_ONLY


class PrefillObservabilityPolicy:
    def observe(self, frame: ProviderPrefillFrame) -> PrefillObservabilityFrame:
        events = tuple(
            dict.fromkeys(
                frame.observable_events
                + (
                    "prefill_success" if frame.prefill_success else "",
                    "clipboard_fallback" if frame.clipboard_fallback_active else "",
                    "injection_failed" if frame.injection_failed else "",
                    "provider_unsupported" if frame.provider_unsupported else "",
                    frame.enter_only_confidence,
                )
            )
        )
        events = tuple(event for event in events if event)
        avoided = 1_200 if frame.enter_only_confidence == ENTER_ONLY_READY else 600
        if frame.enter_only_confidence == CLIPBOARD_ONLY:
            avoided = 300
        return PrefillObservabilityFrame(
            provider_name=frame.provider_name,
            prefill_success=frame.prefill_success,
            clipboard_fallback=frame.clipboard_fallback_active,
            injection_failed=frame.injection_failed,
            provider_unsupported=frame.provider_unsupported,
            enter_only_confidence=frame.enter_only_confidence,
            current_status=frame.enter_only_confidence,
            observable_events=events,
            estimated_avoided_handoff_friction=avoided,
            summary_only=True,
            warnings=frame.warnings,
        )


class ProviderPrefillPolicy:
    def evaluate(self, frame: ProviderPrefillFrame) -> ProviderPrefillFrame:
        confidence = EnterOnlyConfidencePolicy().classify(frame)
        return ProviderPrefillFrame(
            provider_name=frame.provider_name,
            prefill_supported=frame.prefill_supported,
            prefill_attempted=frame.prefill_attempted,
            prefill_success=frame.prefill_success,
            awaiting_human_send=frame.awaiting_human_send,
            chat_opened=frame.chat_opened,
            continuity_injected=frame.continuity_injected,
            sprint_prompt_injected=frame.sprint_prompt_injected,
            bootstrap_preview_available=frame.bootstrap_preview_available,
            injection_strategy=frame.injection_strategy,
            fallback_behavior=frame.fallback_behavior,
            clipboard_fallback_active=frame.clipboard_fallback_active,
            injection_failed=frame.injection_failed,
            provider_unsupported=frame.provider_unsupported,
            enter_only_confidence=confidence,
            observable_events=frame.observable_events,
            auto_send=False,
            hidden_continuation=False,
            silent_dispatch=False,
            background_prompt_execution=False,
            warnings=frame.warnings,
        )


__all__ = [
    "CLIPBOARD_ONLY",
    "ENTER_ONLY_READY",
    "PREFILL_PARTIAL",
    "EnterOnlyConfidencePolicy",
    "PrefillObservabilityFrame",
    "PrefillObservabilityPolicy",
    "ProviderPrefillFrame",
    "ProviderPrefillPolicy",
]
