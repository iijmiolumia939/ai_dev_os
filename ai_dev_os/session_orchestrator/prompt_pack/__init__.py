from __future__ import annotations

from dataclasses import dataclass

PROMPT_TEMPLATES = {
    "sprint_start": "\n".join(
        (
            "Start sprint {sprint_id} for {project_name}.",
            "Objective: {objective}",
            "Context:",
            "{context}",
            "Expected output: scoped plan, patch, validation, and handoff summary.",
        )
    ),
    "sprint_close": "\n".join(
        (
            "Close sprint {sprint_id} for {project_name}.",
            "Validate results, summarize risks, prepare next-session continuity,",
            "and report commit/push/CI status.",
            "Context:",
            "{context}",
        )
    ),
    "architecture_isolation": "\n".join(
        (
            "Open an isolated architecture session for {project_name}.",
            "Scope only these runtimes: {runtimes}.",
            "Do not mix routine patch context.",
            "Context:",
            "{context}",
        )
    ),
    "patch_only": "\n".join(
        (
            "Run patch-only work for {project_name}.",
            "Touch only scoped files and return a diff-focused result.",
            "Context:",
            "{context}",
        )
    ),
    "session_rollover": "\n".join(
        (
            "Roll over the current session for {project_name}.",
            "Use compact continuity and avoid full transcript replay.",
            "Context:",
            "{context}",
        )
    ),
    "remote_verification": "\n".join(
        (
            "Verify remote CI for {project_name}.",
            "Report run URL, conclusion, job status, HEAD sync, and artifact hygiene.",
            "Context:",
            "{context}",
        )
    ),
}


@dataclass(frozen=True)
class PromptPackFrame:
    prompt_type: str
    copy_ready_text: str
    plain_text: str
    estimated_tokens: int
    required_context: tuple[str, ...]
    excluded_context: tuple[str, ...]
    warnings: tuple[str, ...]


class PromptPackPolicy:
    def build(
        self,
        *,
        prompt_type: str,
        project_name: str,
        sprint_id: str = "",
        objective: str = "bounded sprint task",
        context_lines: tuple[str, ...] = (),
        required_context: tuple[str, ...] = (),
        excluded_context: tuple[str, ...] = (),
        affected_runtimes: tuple[str, ...] = (),
        plain_text: bool = True,
    ) -> PromptPackFrame:
        if prompt_type not in PROMPT_TEMPLATES:
            raise ValueError(f"unsupported prompt type: {prompt_type}")
        context = "\n".join(f"- {line}" for line in context_lines if line) or "- none"
        text = PROMPT_TEMPLATES[prompt_type].format(
            sprint_id=sprint_id or "next",
            project_name=project_name,
            objective=objective,
            context=context,
            runtimes=", ".join(affected_runtimes) or "scoped runtime only",
        )
        copy_ready = text if plain_text else f"```text\n{text}\n```"
        warnings = tuple(
            warning
            for warning in (
                "plain_text_copy_ready" if plain_text else "fenced_copy_ready",
                "full_history_excluded" if excluded_context else "",
            )
            if warning
        )
        return PromptPackFrame(
            prompt_type=prompt_type,
            copy_ready_text=copy_ready,
            plain_text=text,
            estimated_tokens=self._estimate_tokens(text),
            required_context=required_context,
            excluded_context=excluded_context,
            warnings=warnings,
        )

    def _estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4) if text else 0
