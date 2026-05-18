from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiffOnlyRequest:
    request_type: str
    touched_files: tuple[str, ...]
    requested_files: tuple[str, ...]
    estimated_changed_lines: int


@dataclass(frozen=True)
class DiffOnlyDecision:
    allowed: bool
    rewrite_suppressed: bool
    touched_file_limited: bool
    scoped_patch_generated: bool
    warnings: tuple[str, ...]


def enforce_diff_only(
    request: DiffOnlyRequest, *, max_changed_lines: int = 300
) -> DiffOnlyDecision:
    normalized_type = request.request_type.strip().lower().replace("-", "_").replace(" ", "_")
    requested = set(request.requested_files)
    touched = set(request.touched_files)
    untouched_requested = bool(requested - touched)
    full_rewrite = normalized_type in {
        "full_file_regeneration",
        "full_repo_rewrite",
        "giant_rewrite",
    }
    too_large = request.estimated_changed_lines > max_changed_lines
    suppressed = full_rewrite or too_large or untouched_requested

    warnings: list[str] = []
    if full_rewrite:
        warnings.append("FULL_REWRITE_SUPPRESSED")
    if too_large:
        warnings.append("PATCH_SIZE_LIMIT_ENFORCED")
    if untouched_requested:
        warnings.append("UNTOUCHED_FILE_REWRITE_BLOCKED")

    return DiffOnlyDecision(
        allowed=not suppressed,
        rewrite_suppressed=suppressed,
        touched_file_limited=untouched_requested,
        scoped_patch_generated=suppressed,
        warnings=tuple(warnings),
    )
