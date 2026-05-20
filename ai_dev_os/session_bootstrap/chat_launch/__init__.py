from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.session_bootstrap.chat_target_detection import ChatTargetDetectionFrame

CHAT_OPEN_COMMAND = "workbench.action.chat.open"


@dataclass(frozen=True)
class ChatLaunchFrame:
    chat_opened: bool
    opened_target: str
    command_name: str
    draft_payload_bound: bool
    awaiting_human_send: bool
    send_dispatched: bool
    background_dispatch_used: bool
    authority_escalation_used: bool
    clipboard_fallback_active: bool
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.send_dispatched or self.background_dispatch_used or self.authority_escalation_used:
            raise ValueError("chat launch must stop before send or hidden dispatch")


class ChatLaunchPolicy:
    def launch(self, target: ChatTargetDetectionFrame) -> ChatLaunchFrame:
        chat_opened = target.prefill_supported
        fallback = target.fallback_required and target.clipboard_fallback_allowed
        warnings = target.warnings + (("clipboard_fallback_active",) if fallback else ())
        return ChatLaunchFrame(
            chat_opened=chat_opened,
            opened_target=target.detected_target,
            command_name=CHAT_OPEN_COMMAND if chat_opened else "clipboard_fallback",
            draft_payload_bound=chat_opened,
            awaiting_human_send=chat_opened or fallback,
            send_dispatched=False,
            background_dispatch_used=False,
            authority_escalation_used=False,
            clipboard_fallback_active=fallback,
            warnings=tuple(dict.fromkeys(warnings)),
        )
