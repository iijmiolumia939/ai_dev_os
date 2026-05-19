from __future__ import annotations

from dataclasses import dataclass

TRIVIAL_TERMS = (
    "complete this line",
    "autocomplete",
    "simple completion",
    "boilerplate",
    "補完",
)
RENAME_TERMS = ("rename", "variable name", "関数名", "変数名", "リネーム")
COMMENT_TERMS = ("comment", "docstring", "コメント", "説明を追加")
GLUE_TERMS = ("glue", "wire", "adapter", "simple helper", "小さな helper")
LOCAL_REFACTOR_TERMS = ("local refactor", "extract helper", "small refactor", "局所")
ARCHITECTURE_TERMS = (
    "architecture",
    "adr",
    "cross-module",
    "security review",
    "設計",
    "アーキテクチャ",
)


@dataclass(frozen=True)
class InlineFirstReport:
    use_inline_completion: bool
    use_patch_prompt: bool
    use_agent: bool
    use_architecture_review: bool
    classification: str
    estimated_avoided_tokens: int
    warnings: tuple[str, ...]


class InlineFirstPolicy:
    def evaluate(
        self,
        task: str,
        *,
        touched_files: int = 1,
        estimated_diff_lines: int = 20,
    ) -> InlineFirstReport:
        normalized = task.lower()
        if any(term in normalized for term in ARCHITECTURE_TERMS) or touched_files > 5:
            return InlineFirstReport(
                use_inline_completion=False,
                use_patch_prompt=False,
                use_agent=False,
                use_architecture_review=True,
                classification="architecture_review",
                estimated_avoided_tokens=0,
                warnings=("architecture_scope_requires_review",),
            )

        if self._matches(normalized, TRIVIAL_TERMS):
            return self._inline("trivial_code_completion", 1_200)
        if self._matches(normalized, RENAME_TERMS):
            return self._inline("rename", 900)
        if self._matches(normalized, COMMENT_TERMS):
            return self._inline("comment", 800)
        if self._matches(normalized, GLUE_TERMS) and estimated_diff_lines <= 40:
            return self._inline("simple_glue_code", 1_000)
        if self._matches(normalized, LOCAL_REFACTOR_TERMS) and touched_files <= 2:
            return InlineFirstReport(
                use_inline_completion=False,
                use_patch_prompt=True,
                use_agent=False,
                use_architecture_review=False,
                classification="local_refactor_patch_prompt",
                estimated_avoided_tokens=700,
                warnings=("prefer_patch_prompt_over_agent",),
            )

        use_agent = touched_files > 2 or estimated_diff_lines > 80
        return InlineFirstReport(
            use_inline_completion=False,
            use_patch_prompt=not use_agent,
            use_agent=use_agent,
            use_architecture_review=False,
            classification="agent" if use_agent else "patch_prompt",
            estimated_avoided_tokens=300 if not use_agent else 0,
            warnings=(),
        )

    def _inline(self, classification: str, avoided_tokens: int) -> InlineFirstReport:
        return InlineFirstReport(
            use_inline_completion=True,
            use_patch_prompt=False,
            use_agent=False,
            use_architecture_review=False,
            classification=classification,
            estimated_avoided_tokens=avoided_tokens,
            warnings=("inline_completion_first",),
        )

    def _matches(self, normalized_task: str, terms: tuple[str, ...]) -> bool:
        return any(term in normalized_task for term in terms)
