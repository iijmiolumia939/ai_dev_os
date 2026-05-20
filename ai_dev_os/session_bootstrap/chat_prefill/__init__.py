from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.session_bootstrap.chat_launch import ChatLaunchFrame
from ai_dev_os.session_orchestrator.continuity_export import ContinuityExportFrame
from ai_dev_os.session_orchestrator.prompt_pack import PromptPackFrame

ENTER_READY_STATE = "AI_DEV_OS ENTER_READY"
WAITING_FOR_SEND_STATE = "AI_DEV_OS WAITING_FOR_SEND"


@dataclass(frozen=True)
class ChatPrefillFrame:
    draft_prefilled: bool
    draft_text: str
    continuity_injected: bool
    sprint_prompt_injected: bool
    awaiting_human_send: bool
    status_bar_state: str
    estimated_token_size: int
    included_continuity: tuple[str, ...]
    excluded_stale_context: tuple[str, ...]
    auto_send: bool
    hidden_continuation: bool
    background_message_dispatch: bool
    silent_prompt_mutation: bool
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            self.auto_send
            or self.hidden_continuation
            or self.background_message_dispatch
            or self.silent_prompt_mutation
        ):
            raise ValueError("chat prefill must remain human-confirmed and enter-only")


class ChatPrefillPolicy:
    def prefill(
        self,
        *,
        launch: ChatLaunchFrame,
        continuity: ContinuityExportFrame,
        prompt_pack: PromptPackFrame,
    ) -> ChatPrefillFrame:
        draft_text = self._draft_text(continuity, prompt_pack)
        estimated = continuity.estimated_tokens + prompt_pack.estimated_tokens
        included = (
            *continuity.active_requirements,
            *continuity.active_tests,
            *continuity.affected_runtimes,
        )
        warnings = tuple(
            dict.fromkeys(
                launch.warnings
                + prompt_pack.warnings
                + (("enter_only_human_send_required",) if launch.awaiting_human_send else ())
            )
        )
        return ChatPrefillFrame(
            draft_prefilled=launch.draft_payload_bound,
            draft_text=draft_text,
            continuity_injected=bool(continuity.copy_ready_text),
            sprint_prompt_injected=bool(prompt_pack.copy_ready_text),
            awaiting_human_send=launch.awaiting_human_send,
            status_bar_state=WAITING_FOR_SEND_STATE,
            estimated_token_size=estimated,
            included_continuity=tuple(dict.fromkeys(included)),
            excluded_stale_context=tuple(
                dict.fromkeys(continuity.excluded_context + prompt_pack.excluded_context)
            ),
            auto_send=False,
            hidden_continuation=False,
            background_message_dispatch=False,
            silent_prompt_mutation=False,
            warnings=warnings,
        )

    def _draft_text(
        self,
        continuity: ContinuityExportFrame,
        prompt_pack: PromptPackFrame,
    ) -> str:
        return "\n".join(
            (
                "AI_DEV_OS Bootstrap Draft",
                "Use only this compact continuity. Do not replay full history.",
                "The final Enter/Send is a human action.",
                "",
                "Continuity:",
                continuity.copy_ready_text,
                "",
                "Sprint prompt:",
                prompt_pack.copy_ready_text,
            )
        )
