from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.output_compression import (
    CompactCompletionInput,
    CompactCompletionPolicy,
    ValidationResult,
)


@dataclass(frozen=True)
class SprintCloseInput:
    validation_summary: str
    git_status_summary: str
    changed_paths: tuple[str, ...]
    test_results: tuple[str, ...]
    remaining_risks: tuple[str, ...]
    next_roadmap: tuple[str, ...]
    commit: str = "pending"
    ci_status: str = "not_checked"
    runtime_audit_status: str = "not_checked"
    rollout_summary: str = ""


@dataclass(frozen=True)
class SprintCloseFrame:
    session_should_close: bool
    next_session_bundle_required: bool
    commit_push_required: bool
    remote_verification_required: bool
    remaining_local_changes: tuple[str, ...]
    next_sprint_context_seed: str
    warnings: tuple[str, ...]
    compact_sprint_completion: str
    compact_rollout_summary: str
    compact_runtime_audit_summary: str
    compact_ci_summary: str
    expandable_completion_details: tuple[str, ...]
    compact_reporting_active: bool
    estimated_avoided_completion_tokens: int


class SprintClosePolicy:
    def close(self, data: SprintCloseInput) -> SprintCloseFrame:
        dirty = "clean" not in data.git_status_summary.lower()
        committed = "ahead" not in data.git_status_summary.lower() and not dirty
        commit_push_required = dirty or "ahead" in data.git_status_summary.lower()
        remote_required = (
            commit_push_required or "remote ci" not in data.validation_summary.lower()
        )
        remaining = tuple(path for path in data.changed_paths if path)
        warnings = tuple(
            warning
            for warning in (
                "remaining_local_changes" if dirty else "",
                "remote_verification_required" if remote_required else "",
                "prepare_next_session_bundle",
            )
            if warning
        )
        seed = self._seed(data, committed=committed)
        completion = CompactCompletionPolicy().compact(
            CompactCompletionInput(
                commit=data.commit,
                ci_status=data.ci_status,
                validation_results=self._validation_results(data),
                runtime_audit_status=data.runtime_audit_status,
                risks=data.remaining_risks,
                next_step=", ".join(data.next_roadmap) if data.next_roadmap else "none",
                rollout_summary=data.rollout_summary,
                unchanged_sections=("rollout",) if data.rollout_summary else (),
            )
        )
        return SprintCloseFrame(
            session_should_close=True,
            next_session_bundle_required=True,
            commit_push_required=commit_push_required,
            remote_verification_required=remote_required,
            remaining_local_changes=remaining if dirty else (),
            next_sprint_context_seed=seed,
            warnings=warnings,
            compact_sprint_completion=completion.compact_summary,
            compact_rollout_summary=(
                "Rollout: compact-ref" if data.rollout_summary else "Rollout: not_changed"
            ),
            compact_runtime_audit_summary=f"Runtime audit: {data.runtime_audit_status}",
            compact_ci_summary=f"CI: {data.ci_status}",
            expandable_completion_details=completion.expandable_details,
            compact_reporting_active=completion.compact and completion.expandable,
            estimated_avoided_completion_tokens=completion.estimated_avoided_completion_tokens,
        )

    def _seed(self, data: SprintCloseInput, *, committed: bool) -> str:
        return "\n".join(
            (
                "Next sprint context seed:",
                f"Validation: {data.validation_summary}",
                f"Tests: {', '.join(data.test_results)}",
                f"Risks: {', '.join(data.remaining_risks)}",
                f"Roadmap: {', '.join(data.next_roadmap)}",
                f"Repository state: {'committed' if committed else data.git_status_summary}",
            )
        )

    def _validation_results(self, data: SprintCloseInput) -> tuple[ValidationResult, ...]:
        results = tuple(
            ValidationResult(
                name=result.split(":", maxsplit=1)[0],
                status=(
                    "pass" if "pass" in result.lower() or "passed" in result.lower() else "success"
                ),
                passed=_extract_passed_count(result),
                details=result,
            )
            for result in data.test_results
        )
        return results + (ValidationResult("runtime audit", data.runtime_audit_status),)


def _extract_passed_count(text: str) -> int:
    for part in text.replace(":", " ").split():
        if part.isdigit():
            return int(part)
    return 0
