from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_TARGETS = ("vscode_chat", "copilot_chat")


@dataclass(frozen=True)
class ChatTargetDetectionFrame:
    requested_target: str
    detected_target: str
    target_available: bool
    prefill_supported: bool
    fallback_required: bool
    clipboard_fallback_allowed: bool
    authority_escalation_allowed: bool
    hidden_dispatch_allowed: bool
    auto_send_allowed: bool
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            self.authority_escalation_allowed
            or self.hidden_dispatch_allowed
            or self.auto_send_allowed
        ):
            raise ValueError("draft injection cannot escalate authority or dispatch hidden sends")


class ChatTargetDetectionPolicy:
    def detect(
        self,
        *,
        requested_target: str = "vscode_chat",
        available_targets: tuple[str, ...] = SUPPORTED_TARGETS,
        prefill_capable_targets: tuple[str, ...] = ("vscode_chat", "copilot_chat"),
        clipboard_fallback_allowed: bool = True,
    ) -> ChatTargetDetectionFrame:
        normalized = requested_target.strip().lower() or "vscode_chat"
        target_available = normalized in available_targets
        prefill_supported = normalized in prefill_capable_targets and target_available
        fallback_required = not prefill_supported
        warnings = tuple(
            warning
            for warning in (
                "target_unavailable" if not target_available else "",
                "prefill_fallback_required" if fallback_required else "",
                (
                    "clipboard_fallback_ready"
                    if fallback_required and clipboard_fallback_allowed
                    else ""
                ),
            )
            if warning
        )
        return ChatTargetDetectionFrame(
            requested_target=normalized,
            detected_target=normalized if target_available else "clipboard_fallback",
            target_available=target_available,
            prefill_supported=prefill_supported,
            fallback_required=fallback_required,
            clipboard_fallback_allowed=clipboard_fallback_allowed,
            authority_escalation_allowed=False,
            hidden_dispatch_allowed=False,
            auto_send_allowed=False,
            warnings=warnings,
        )
