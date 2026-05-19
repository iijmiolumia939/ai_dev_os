from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.context_subset.continuity_scope import ContinuityScopeFrame
from ai_dev_os.context_subset.repository_subset import RepositorySubsetFrame
from ai_dev_os.context_subset.session_focus import SessionFocusFrame
from ai_dev_os.prompt_modes.session_mode_router import SessionModeRouterFrame


@dataclass(frozen=True)
class SessionHandoffFrame:
    rollover_required: bool
    stale_context_detected: bool
    recommended_new_session: bool
    continuity_bundle: dict[str, object]
    prompt_mode: str
    repository_subset: tuple[str, ...]
    session_focus: str
    copy_ready_prompt: str
    handoff_summary: tuple[str, ...]
    full_history_included: bool


class SessionHandoffPolicy:
    def build(
        self,
        *,
        rollover_required: bool,
        stale_context_detected: bool,
        session_mode: SessionModeRouterFrame,
        repository_subset: RepositorySubsetFrame,
        session_focus: SessionFocusFrame,
        continuity_scope: ContinuityScopeFrame,
        prompt_text: str,
    ) -> SessionHandoffFrame:
        recommended = (
            rollover_required or stale_context_detected or session_mode.isolation_required
        )
        bundle = {
            "rollover_required": rollover_required,
            "prompt_mode": session_mode.recommended_mode,
            "repository_subset": repository_subset.active_repositories,
            "session_focus": session_focus.recommended_session_type,
            "continuity_scope": continuity_scope.included_context,
            "stale_topics": continuity_scope.excluded_context,
            "handoff_summary": (
                f"mode={session_mode.recommended_mode}",
                f"repos={len(repository_subset.active_repositories)}",
                f"budget={continuity_scope.continuity_budget}",
            ),
        }
        prompt = self._copy_ready_prompt(prompt_text, bundle)
        return SessionHandoffFrame(
            rollover_required=rollover_required,
            stale_context_detected=stale_context_detected,
            recommended_new_session=recommended,
            continuity_bundle=bundle,
            prompt_mode=session_mode.recommended_mode,
            repository_subset=repository_subset.active_repositories,
            session_focus=session_focus.recommended_session_type,
            copy_ready_prompt=prompt,
            handoff_summary=bundle["handoff_summary"],
            full_history_included=False,
        )

    def _copy_ready_prompt(self, prompt_text: str, bundle: dict[str, object]) -> str:
        lines = [
            "AI_DEV_OS Session Handoff",
            "Use only this compact continuity bundle. Do not replay full history.",
            "",
            "Continuity:",
        ]
        for key, value in bundle.items():
            lines.append(f"- {key}: {value}")
        lines.extend(("", "Prompt:", prompt_text))
        return "\n".join(lines)
