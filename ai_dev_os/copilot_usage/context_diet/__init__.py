from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

GENERATED_MARKERS = (
    "dist/",
    "build/",
    "__pycache__/",
    ".pytest_cache/",
    ".ruff_cache/",
    "coverage/",
    "node_modules/",
    "library/",
    "temp/",
    "logs/",
)
VENDOR_MARKERS = ("vendor/", "third_party/", "assets/vendor/", "packages/")
STALE_MARKERS = ("sprint", "history", "archive", "obsolete", "stale")


@dataclass(frozen=True)
class ContextItem:
    path: str
    tokens: int
    reason: str = "active"
    related: bool = True
    full_file: bool = False
    age_days: int = 0


@dataclass(frozen=True)
class ContextDietReport:
    allowed_context: tuple[ContextItem, ...]
    removed_context: tuple[ContextItem, ...]
    token_reduction_estimate: int
    warnings: tuple[str, ...]


class ContextDietPolicy:
    def __init__(self, *, large_file_tokens: int = 4_000, stale_days: int = 21) -> None:
        self.large_file_tokens = large_file_tokens
        self.stale_days = stale_days

    def evaluate(self, context_items: tuple[ContextItem, ...]) -> ContextDietReport:
        allowed: list[ContextItem] = []
        removed: list[ContextItem] = []
        warnings: list[str] = []

        for item in context_items:
            normalized_path = self._normalize(item.path)
            removal_reason = self._removal_reason(item, normalized_path)
            if removal_reason:
                removed.append(item)
                warnings.append(removal_reason)
            else:
                allowed.append(item)

        return ContextDietReport(
            allowed_context=tuple(allowed),
            removed_context=tuple(removed),
            token_reduction_estimate=sum(item.tokens for item in removed),
            warnings=tuple(dict.fromkeys(warnings)),
        )

    def _removal_reason(self, item: ContextItem, normalized_path: str) -> str:
        if normalized_path in {".", "./", "repo", "repository"} or item.reason == "full_repo":
            return "full_repo_context_removed"
        if any(marker in normalized_path for marker in GENERATED_MARKERS):
            return "generated_artifact_removed"
        if any(marker in normalized_path for marker in VENDOR_MARKERS):
            return "unnecessary_vendor_asset_removed"
        if item.full_file and item.tokens >= self.large_file_tokens:
            return "full_file_attachment_removed"
        if not item.related and item.tokens >= self.large_file_tokens // 2:
            return "unrelated_large_file_removed"
        if item.age_days >= self.stale_days or any(
            marker in normalized_path for marker in STALE_MARKERS
        ):
            return "stale_sprint_history_removed"
        return ""

    def _normalize(self, path: str) -> str:
        normalized = str(PurePosixPath(path.replace("\\", "/"))).lower()
        return normalized if normalized != "" else "."
