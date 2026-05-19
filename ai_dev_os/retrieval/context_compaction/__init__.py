from __future__ import annotations

from dataclasses import dataclass

from retrieval.prune_context import estimate_tokens

ACTIVE_KEYS = {"active_requirements", "changed_files", "active_artifacts", "entries", "policy"}
PRUNED_KEYS = {
    "stale_sprint_history",
    "inactive_adr",
    "obsolete_open_questions",
    "giant_markdown",
    "unrelated_summaries",
}


@dataclass(frozen=True)
class CompactionReport:
    before_tokens: int
    after_tokens: int
    removed_keys: tuple[str, ...]
    preserved_keys: tuple[str, ...]
    duplicate_context_suppressed: bool
    summary_only_mode: bool
    active_artifacts_preserved: bool
    warnings: tuple[str, ...]


def compact_context(
    bundle: dict[str, object], *, max_tokens: int = 8_000
) -> tuple[dict[str, object], CompactionReport]:
    if "full_repository_context" in bundle:
        raise ValueError("full repository injection is forbidden")
    if max_tokens <= 0:
        raise ValueError("max tokens must be positive")

    compacted = {key: value for key, value in bundle.items() if key in ACTIVE_KEYS}
    removed = set(bundle) - set(compacted)
    duplicate_suppressed = "duplicate_contexts" in removed

    entries = list(compacted.get("entries", []))
    seen_paths: set[str] = set()
    deduplicated_entries: list[object] = []
    for entry in entries:
        path = str(entry.get("path", entry)) if isinstance(entry, dict) else str(entry)
        if path in seen_paths:
            duplicate_suppressed = True
            continue
        seen_paths.add(path)
        deduplicated_entries.append(entry)
    if deduplicated_entries:
        compacted["entries"] = deduplicated_entries

    while estimate_tokens(compacted) > max_tokens and len(deduplicated_entries) > 1:
        deduplicated_entries = deduplicated_entries[: max(1, len(deduplicated_entries) // 2)]
        compacted["entries"] = deduplicated_entries

    summary_only_mode = estimate_tokens(compacted) > max_tokens
    if summary_only_mode:
        compacted = {key: value for key, value in compacted.items() if key != "entries"}

    compacted["context_tokens"] = estimate_tokens(compacted)
    warnings = []
    if removed & PRUNED_KEYS:
        warnings.append("STALE_CONTEXT_PRUNED")
    if duplicate_suppressed:
        warnings.append("DUPLICATE_CONTEXT_SUPPRESSED")
    if summary_only_mode:
        warnings.append("SUMMARY_ONLY_MODE")

    report = CompactionReport(
        before_tokens=estimate_tokens(bundle),
        after_tokens=estimate_tokens(compacted),
        removed_keys=tuple(sorted(removed)),
        preserved_keys=tuple(sorted(set(compacted) & ACTIVE_KEYS)),
        duplicate_context_suppressed=duplicate_suppressed,
        summary_only_mode=summary_only_mode,
        active_artifacts_preserved="active_artifacts" in compacted,
        warnings=tuple(warnings),
    )
    if not report.active_artifacts_preserved:
        raise ValueError("active artifact preservation is required")
    return compacted, report
