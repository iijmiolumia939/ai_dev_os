from __future__ import annotations

import re
from dataclasses import dataclass

OBJECTIVE_MARKERS = (
    " implement ",
    " add ",
    " fix ",
    " review ",
    " refactor ",
    " document ",
    " test ",
    " deploy ",
    " architecture",
    "設計",
    "実装",
    "レビュー",
    "修正",
    "追加",
    "テスト",
)
BROAD_REVIEW_PATTERNS = (
    "overall review",
    "review everything",
    "review the whole",
    "改善できるところ",
    "全体的に",
    "いろいろ",
    "全部見て",
)
FULL_REPOSITORY_PATTERNS = (
    "full repository",
    "entire repository",
    "whole repo",
    "all files",
    "full repo",
    "リポジトリ全体",
    "全ファイル",
)
ARCHITECTURE_TERMS = ("architecture", "architectural", "adr", "設計", "アーキテクチャ")
IMPLEMENTATION_TERMS = ("implement", "implementation", "code", "実装", "修正", "追加")
REVIEW_TERMS = ("review", "audit", "レビュー", "監査")


@dataclass(frozen=True)
class AtomicPromptAuditReport:
    accepted: bool
    needs_split: bool
    blocked: bool
    suggested_split_tasks: tuple[str, ...]
    detected_patterns: tuple[str, ...]
    estimated_avoided_tokens: int


class AtomicPromptPolicy:
    def __init__(self, *, max_objectives: int = 1) -> None:
        self.max_objectives = max_objectives

    def evaluate(self, prompt: str) -> AtomicPromptAuditReport:
        normalized = f" {prompt.lower()} "
        detected: list[str] = []
        suggestions: list[str] = []
        objective_count = self._count_objectives(normalized)

        if objective_count > self.max_objectives:
            detected.append("multiple_unrelated_objectives")
            suggestions.extend(self._split_prompt(prompt))
        if any(pattern in normalized for pattern in BROAD_REVIEW_PATTERNS):
            detected.append("broad_vague_review_request")
            suggestions.append("Ask for one bounded review dimension on one changed area.")
        if any(pattern in normalized for pattern in FULL_REPOSITORY_PATTERNS):
            detected.append("full_repository_request")
            suggestions.append("Provide only changed files and active requirements.")
        if self._has_mixed_architecture_implementation_review(normalized):
            detected.append("mixed_architecture_implementation_review_prompt")
            suggestions.extend(
                (
                    "First decide the architecture boundary.",
                    "Then implement a scoped patch.",
                    "Then request a focused review of the diff.",
                )
            )

        blocked = "full_repository_request" in detected
        needs_split = bool(detected) and not blocked
        accepted = not detected
        unique_suggestions = tuple(dict.fromkeys(suggestions))
        return AtomicPromptAuditReport(
            accepted=accepted,
            needs_split=needs_split,
            blocked=blocked,
            suggested_split_tasks=unique_suggestions,
            detected_patterns=tuple(detected),
            estimated_avoided_tokens=900 * max(1, len(detected)) if detected else 0,
        )

    def _count_objectives(self, normalized_prompt: str) -> int:
        marker_hits = sum(1 for marker in OBJECTIVE_MARKERS if marker in normalized_prompt)
        separator_hits = len(re.findall(r"\b(and|then|also|plus)\b|[、,;]\s*", normalized_prompt))
        return max(marker_hits, separator_hits + 1 if separator_hits else marker_hits)

    def _split_prompt(self, prompt: str) -> tuple[str, ...]:
        parts = [part.strip(" -.,;\n") for part in re.split(r"\bthen\b|\balso\b|;|\n|- ", prompt)]
        bounded = tuple(part for part in parts if len(part.split()) >= 3)
        return bounded[:4] or ("Rewrite as one objective against one changed area.",)

    def _has_mixed_architecture_implementation_review(self, normalized_prompt: str) -> bool:
        has_architecture = any(term in normalized_prompt for term in ARCHITECTURE_TERMS)
        has_implementation = any(term in normalized_prompt for term in IMPLEMENTATION_TERMS)
        has_review = any(term in normalized_prompt for term in REVIEW_TERMS)
        return has_architecture and has_implementation and has_review
