from __future__ import annotations

import re
from dataclasses import dataclass


def _marker(*parts: str) -> str:
    return " ".join(parts)


FORBIDDEN_FULL_FILE_REWRITE_MARKERS = (
    _marker("rewrite", "entire", "file"),
    _marker("full-" + "file", "regeneration"),
    _marker("replace", "whole", "file"),
)


@dataclass(frozen=True)
class AiderPatchRequest:
    git_diff: str
    changed_functions: tuple[str, ...]
    touched_tests: tuple[str, ...]


def extract_changed_functions(diff_text: str) -> tuple[str, ...]:
    names = []
    for line in diff_text.splitlines():
        if line.startswith("@@"):
            match = re.search(
                r"\b(?:def|class|function|void|public|private)\s+([A-Za-z_][A-Za-z0-9_]*)", line
            )
            if match:
                names.append(match.group(1))
    return tuple(dict.fromkeys(names))


def suppress_rewrite(prompt: str) -> str:
    lowered = prompt.lower()
    if any(marker in lowered for marker in FORBIDDEN_FULL_FILE_REWRITE_MARKERS):
        raise ValueError("full-file regeneration is forbidden")
    return prompt


def create_scoped_patch_prompt(request: AiderPatchRequest) -> str:
    prompt = "\n".join(
        [
            "# aider scoped patch request",
            "Policy: return minimal diff only; do not regenerate unrelated content.",
            "Changed functions:",
            *(f"- {name}" for name in request.changed_functions),
            "Touched tests:",
            *(f"- {test}" for test in request.touched_tests),
            "Git diff:",
            request.git_diff,
        ]
    )
    return suppress_rewrite(prompt)
