from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.session_bootstrap.chat_launch import ChatLaunchPolicy
from ai_dev_os.session_bootstrap.chat_prefill import (
    ENTER_READY_STATE,
    WAITING_FOR_SEND_STATE,
    ChatPrefillPolicy,
)
from ai_dev_os.session_bootstrap.chat_target_detection import ChatTargetDetectionPolicy
from ai_dev_os.session_orchestrator.continuity_export import ContinuityExportPolicy
from ai_dev_os.session_orchestrator.prompt_pack import PromptPackPolicy


@dataclass(frozen=True)
class BootstrapDraftPreviewFrame:
    estimated_token_size: int
    included_continuity: tuple[str, ...]
    excluded_stale_context: tuple[str, ...]
    sprint_focus: str
    architecture_isolation: str
    enter_ready_state: str
    waiting_for_send_state: str


@dataclass(frozen=True)
class CopilotDraftInjectionFrame:
    chat_opened: bool
    draft_prefilled: bool
    continuity_injected: bool
    awaiting_human_send: bool
    draft_text: str
    preview: BootstrapDraftPreviewFrame
    target: str
    clipboard_fallback_active: bool
    auto_send: bool
    hidden_continuation: bool
    background_message_dispatch: bool
    silent_prompt_mutation: bool
    authority_escalation_used: bool
    status_bar_states: tuple[str, ...]
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            self.auto_send
            or self.hidden_continuation
            or self.background_message_dispatch
            or self.silent_prompt_mutation
            or self.authority_escalation_used
        ):
            raise ValueError("draft injection must stop at human-confirmed Enter/Send")


class DraftInjectionPolicy:
    def build(
        self,
        *,
        project_name: str,
        sprint_id: str = "next",
        requested_target: str = "vscode_chat",
        objective: str = "enter-only session rollover",
        active_requirements: tuple[str, ...] = (
            "FR-DRAFTINJECT-01",
            "FR-DRAFTINJECT-02",
            "FR-DRAFTINJECT-03",
            "FR-DRAFTINJECT-04",
            "FR-DRAFTINJECT-05",
            "NFR-UX-02",
            "NFR-ARCH-29",
            "NFR-SEC-05",
        ),
        active_tests: tuple[str, ...] = (
            "TC-DRAFTINJECT-01",
            "TC-DRAFTINJECT-02",
            "TC-DRAFTINJECT-03",
            "TC-DRAFTINJECT-04",
            "TC-DRAFTINJECT-05",
        ),
        affected_runtimes: tuple[str, ...] = (
            "session_bootstrap.draft_injection",
            "session_bootstrap.chat_prefill",
            "session_bootstrap.chat_launch",
            "session_bootstrap.chat_target_detection",
            "vscode_extension",
        ),
        architecture_isolation: str = "no authority escalation; extension opens draft only",
        active_risks: tuple[str, ...] = (
            "accidental send dispatch",
            "hidden continuation",
            "stale continuity replay",
        ),
    ) -> CopilotDraftInjectionFrame:
        continuity = ContinuityExportPolicy().export(
            active_requirements=active_requirements,
            active_tests=active_tests,
            current_sprint_boundary=f"{project_name}: {sprint_id} enter-only rollover",
            affected_runtimes=affected_runtimes,
            current_architecture_constraints=(
                "human confirmed final send",
                "no hidden continuation",
                "no background message dispatch",
                "no silent prompt mutation",
            ),
            active_risks=active_risks,
            next_prompt_seed=(
                "Open a new chat draft prefilled with compact continuity; " "stop at Enter."
            ),
            output_format="plain",
            extra_context={
                "full_history": "excluded",
                "old_sprint_logs": "excluded",
                "stale_roadmap": "excluded",
                "generated_artifacts": "excluded",
            },
        )
        prompt = PromptPackPolicy().build(
            prompt_type="session_rollover",
            project_name=project_name,
            sprint_id=sprint_id,
            objective=objective,
            context_lines=(
                "Use compact continuity only.",
                "Open a draft in the visible chat surface.",
                "Do not send, continue, or mutate the prompt without the human Enter/Send.",
            ),
            required_context=("continuity_export", "draft_preview", "enter_only_state"),
            excluded_context=("full_history", "old_sprint_logs", "background_dispatch"),
            affected_runtimes=affected_runtimes,
            prompt_shape="enter_only_bootstrap_draft",
            continuity_depth="minimal",
            review_checklist=(
                "visible draft prefill",
                "human final send",
                "clipboard fallback",
                "stale context excluded",
            ),
            architecture_allowance="none",
            retrieval_budget=900,
            plain_text=True,
        )
        target = ChatTargetDetectionPolicy().detect(requested_target=requested_target)
        launch = ChatLaunchPolicy().launch(target)
        prefill = ChatPrefillPolicy().prefill(
            launch=launch,
            continuity=continuity,
            prompt_pack=prompt,
        )
        preview = BootstrapDraftPreviewFrame(
            estimated_token_size=prefill.estimated_token_size,
            included_continuity=prefill.included_continuity,
            excluded_stale_context=prefill.excluded_stale_context,
            sprint_focus=objective,
            architecture_isolation=architecture_isolation,
            enter_ready_state=ENTER_READY_STATE,
            waiting_for_send_state=WAITING_FOR_SEND_STATE,
        )
        warnings = tuple(dict.fromkeys(target.warnings + launch.warnings + prefill.warnings))
        return CopilotDraftInjectionFrame(
            chat_opened=launch.chat_opened,
            draft_prefilled=prefill.draft_prefilled,
            continuity_injected=prefill.continuity_injected,
            awaiting_human_send=prefill.awaiting_human_send,
            draft_text=prefill.draft_text,
            preview=preview,
            target=target.detected_target,
            clipboard_fallback_active=launch.clipboard_fallback_active,
            auto_send=False,
            hidden_continuation=False,
            background_message_dispatch=False,
            silent_prompt_mutation=False,
            authority_escalation_used=False,
            status_bar_states=(ENTER_READY_STATE, WAITING_FOR_SEND_STATE),
            warnings=warnings,
        )
