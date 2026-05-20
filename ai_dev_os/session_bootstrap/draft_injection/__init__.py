from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.session_bootstrap.chat_launch import ChatLaunchPolicy
from ai_dev_os.session_bootstrap.chat_prefill import (
    ENTER_READY_STATE,
    WAITING_FOR_SEND_STATE,
    ChatPrefillPolicy,
)
from ai_dev_os.session_bootstrap.chat_target_detection import ChatTargetDetectionPolicy
from ai_dev_os.session_bootstrap.provider_prefill import (
    ENTER_ONLY_READY,
    PrefillObservabilityFrame,
    PrefillObservabilityPolicy,
    ProviderPrefillFrame,
)
from ai_dev_os.session_bootstrap.provider_prefill.clipboard_fallback import (
    ClipboardFallbackPrefillAdapter,
)
from ai_dev_os.session_bootstrap.provider_prefill.copilot_chat import CopilotChatPrefillAdapter
from ai_dev_os.session_bootstrap.provider_prefill.vscode_chat import VSCodeChatPrefillAdapter
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
    provider_name: str = "vscode_chat"
    enter_only_confidence: str = ENTER_ONLY_READY


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
    provider_name: str = "vscode_chat"
    prefill_supported: bool = True
    prefill_attempted: bool = True
    prefill_success: bool = True
    enter_only_confidence: str = ENTER_ONLY_READY
    provider_prefill: ProviderPrefillFrame | None = None
    observability: PrefillObservabilityFrame | None = None

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
            "FR-PREFILL-01",
            "FR-PREFILL-02",
            "FR-PREFILL-03",
            "FR-PREFILL-04",
            "FR-PREFILL-05",
            "NFR-UX-02",
            "NFR-UX-03",
            "NFR-ARCH-29",
            "NFR-ARCH-30",
            "NFR-OBS-03",
            "NFR-SEC-05",
        ),
        active_tests: tuple[str, ...] = (
            "TC-DRAFTINJECT-01",
            "TC-DRAFTINJECT-02",
            "TC-DRAFTINJECT-03",
            "TC-DRAFTINJECT-04",
            "TC-DRAFTINJECT-05",
            "TC-PREFILL-01",
            "TC-PREFILL-02",
            "TC-PREFILL-03",
            "TC-PREFILL-04",
            "TC-PREFILL-05",
        ),
        affected_runtimes: tuple[str, ...] = (
            "session_bootstrap.draft_injection",
            "session_bootstrap.chat_prefill",
            "session_bootstrap.chat_launch",
            "session_bootstrap.chat_target_detection",
            "session_bootstrap.provider_prefill",
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
        provider_prefill = self._provider_prefill(
            requested_target=target.detected_target,
            draft_text=prefill.draft_text,
            continuity_text=continuity.copy_ready_text,
            sprint_prompt_text=prompt.copy_ready_text,
            bootstrap_preview_text=objective,
        )
        observability = PrefillObservabilityPolicy().observe(provider_prefill)
        preview = BootstrapDraftPreviewFrame(
            estimated_token_size=prefill.estimated_token_size,
            included_continuity=prefill.included_continuity,
            excluded_stale_context=prefill.excluded_stale_context,
            sprint_focus=objective,
            architecture_isolation=architecture_isolation,
            enter_ready_state=ENTER_READY_STATE,
            waiting_for_send_state=WAITING_FOR_SEND_STATE,
            provider_name=provider_prefill.provider_name,
            enter_only_confidence=provider_prefill.enter_only_confidence,
        )
        warnings = tuple(
            dict.fromkeys(
                target.warnings
                + launch.warnings
                + prefill.warnings
                + provider_prefill.warnings
                + observability.warnings
            )
        )
        return CopilotDraftInjectionFrame(
            chat_opened=provider_prefill.chat_opened,
            draft_prefilled=provider_prefill.prefill_success,
            continuity_injected=provider_prefill.continuity_injected,
            awaiting_human_send=provider_prefill.awaiting_human_send,
            draft_text=prefill.draft_text,
            preview=preview,
            target=provider_prefill.provider_name,
            clipboard_fallback_active=provider_prefill.clipboard_fallback_active,
            auto_send=False,
            hidden_continuation=False,
            background_message_dispatch=False,
            silent_prompt_mutation=False,
            authority_escalation_used=False,
            status_bar_states=(
                "AI_DEV_OS ENTER_ONLY_READY",
                "AI_DEV_OS PREFILL_PARTIAL",
                "AI_DEV_OS CLIPBOARD_ONLY",
            ),
            warnings=warnings,
            provider_name=provider_prefill.provider_name,
            prefill_supported=provider_prefill.prefill_supported,
            prefill_attempted=provider_prefill.prefill_attempted,
            prefill_success=provider_prefill.prefill_success,
            enter_only_confidence=provider_prefill.enter_only_confidence,
            provider_prefill=provider_prefill,
            observability=observability,
        )

    def _provider_prefill(
        self,
        *,
        requested_target: str,
        draft_text: str,
        continuity_text: str,
        sprint_prompt_text: str,
        bootstrap_preview_text: str,
    ) -> ProviderPrefillFrame:
        common = {
            "draft_text": draft_text,
            "continuity_text": continuity_text,
            "sprint_prompt_text": sprint_prompt_text,
            "bootstrap_preview_text": bootstrap_preview_text,
        }
        if requested_target == "copilot_chat":
            return CopilotChatPrefillAdapter().prefill(**common)
        if requested_target == "vscode_chat":
            return VSCodeChatPrefillAdapter().prefill(**common)
        return ClipboardFallbackPrefillAdapter().prefill(**common)
