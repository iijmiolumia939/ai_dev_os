from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SprintCloseInput:
    validation_summary: str
    git_status_summary: str
    changed_paths: tuple[str, ...]
    test_results: tuple[str, ...]
    remaining_risks: tuple[str, ...]
    next_roadmap: tuple[str, ...]


@dataclass(frozen=True)
class SprintCloseFrame:
    session_should_close: bool
    next_session_bundle_required: bool
    commit_push_required: bool
    remote_verification_required: bool
    remaining_local_changes: tuple[str, ...]
    next_sprint_context_seed: str
    warnings: tuple[str, ...]


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
        return SprintCloseFrame(
            session_should_close=True,
            next_session_bundle_required=True,
            commit_push_required=commit_push_required,
            remote_verification_required=remote_required,
            remaining_local_changes=remaining if dirty else (),
            next_sprint_context_seed=seed,
            warnings=warnings,
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
