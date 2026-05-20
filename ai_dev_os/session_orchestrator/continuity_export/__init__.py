from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from ai_dev_os.governance_core.compact_export import GovernanceCompactExportPrimitive

EXCLUDED_EXPORT_KEYS = (
    "full_history",
    "old_sprint_logs",
    "stale_roadmap",
    "vendor_assets",
    "raw_memory",
    "generated_artifacts",
)


@dataclass(frozen=True)
class ContinuityExportFrame:
    active_requirements: tuple[str, ...]
    active_tests: tuple[str, ...]
    current_sprint_boundary: str
    affected_runtimes: tuple[str, ...]
    current_architecture_constraints: tuple[str, ...]
    active_risks: tuple[str, ...]
    next_prompt_seed: str
    format: str
    copy_ready_text: str
    estimated_tokens: int
    excluded_context: tuple[str, ...]
    retrieval_budget_summary: str = ""
    incremental_context_summary: str = ""
    reasoning_scope_summary: str = ""
    unchanged_sprint_summary_suppressed: bool = True
    repo_wide_retrieval_forbidden: bool = True
    repo_wide_replay_forbidden: bool = True


class ContinuityExportPolicy:
    def export(
        self,
        *,
        active_requirements: tuple[str, ...],
        active_tests: tuple[str, ...],
        current_sprint_boundary: str,
        affected_runtimes: tuple[str, ...],
        current_architecture_constraints: tuple[str, ...],
        active_risks: tuple[str, ...],
        next_prompt_seed: str,
        output_format: str = "markdown",
        extra_context: dict[str, str] | None = None,
    ) -> ContinuityExportFrame:
        extra_context = extra_context or {}
        excluded = tuple(key for key in extra_context if key in EXCLUDED_EXPORT_KEYS)
        frame = ContinuityExportFrame(
            active_requirements=active_requirements,
            active_tests=active_tests,
            current_sprint_boundary=current_sprint_boundary,
            affected_runtimes=affected_runtimes,
            current_architecture_constraints=current_architecture_constraints,
            active_risks=active_risks,
            next_prompt_seed=next_prompt_seed,
            format=output_format,
            copy_ready_text="",
            estimated_tokens=0,
            excluded_context=excluded,
            retrieval_budget_summary="affected-runtime-only retrieval",
            incremental_context_summary="changed-continuity-only export",
            reasoning_scope_summary="local-patch reasoning only",
            unchanged_sprint_summary_suppressed=True,
            repo_wide_retrieval_forbidden=True,
            repo_wide_replay_forbidden=True,
        )
        text = self._render(frame, output_format)
        compact = GovernanceCompactExportPrimitive().export(
            self._plain_lines(frame),
            export_mode="copy_ready" if output_format in {"markdown", "plain"} else "summary",
        )
        return ContinuityExportFrame(
            active_requirements=frame.active_requirements,
            active_tests=frame.active_tests,
            current_sprint_boundary=frame.current_sprint_boundary,
            affected_runtimes=frame.affected_runtimes,
            current_architecture_constraints=frame.current_architecture_constraints,
            active_risks=frame.active_risks,
            next_prompt_seed=frame.next_prompt_seed,
            format=frame.format,
            copy_ready_text=text,
            estimated_tokens=min(self._estimate_tokens(text), max(1, compact.compact_export_size)),
            excluded_context=frame.excluded_context,
            retrieval_budget_summary=frame.retrieval_budget_summary,
            incremental_context_summary=frame.incremental_context_summary,
            reasoning_scope_summary=frame.reasoning_scope_summary,
            unchanged_sprint_summary_suppressed=frame.unchanged_sprint_summary_suppressed,
            repo_wide_retrieval_forbidden=frame.repo_wide_retrieval_forbidden,
            repo_wide_replay_forbidden=frame.repo_wide_replay_forbidden,
        )

    def _render(self, frame: ContinuityExportFrame, output_format: str) -> str:
        if output_format == "json":
            data = asdict(frame)
            data.pop("copy_ready_text", None)
            data.pop("estimated_tokens", None)
            return json.dumps(data, indent=2, sort_keys=True)
        if output_format == "plain":
            return "\n".join(self._plain_lines(frame))
        return "\n".join(("# Continuity Bundle", *self._plain_lines(frame)))

    def _plain_lines(self, frame: ContinuityExportFrame) -> tuple[str, ...]:
        return (
            f"Sprint boundary: {frame.current_sprint_boundary}",
            f"Active requirements: {', '.join(frame.active_requirements)}",
            f"Active tests: {', '.join(frame.active_tests)}",
            f"Affected runtimes: {', '.join(frame.affected_runtimes)}",
            f"Architecture constraints: {', '.join(frame.current_architecture_constraints)}",
            f"Active risks: {', '.join(frame.active_risks)}",
            f"Next prompt seed: {frame.next_prompt_seed}",
            f"Excluded context: {', '.join(frame.excluded_context)}",
            f"Retrieval budget: {frame.retrieval_budget_summary}",
            f"Incremental context: {frame.incremental_context_summary}",
            f"Reasoning scope: {frame.reasoning_scope_summary}",
            f"Unchanged sprint summary suppressed: {frame.unchanged_sprint_summary_suppressed}",
            f"Repo-wide retrieval forbidden: {frame.repo_wide_retrieval_forbidden}",
            f"Repo-wide replay forbidden: {frame.repo_wide_replay_forbidden}",
        )

    def _estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4) if text else 0
