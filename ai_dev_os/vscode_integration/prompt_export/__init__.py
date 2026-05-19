from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PromptExportFrame:
    prompt_txt_path: str
    continuation_md_path: str
    compact_bundle_json_path: str
    copy_ready_plain_text: str
    compact_bundle: dict[str, Any]
    summary_only: bool
    bounded: bool
    files_written: bool
    warnings: tuple[str, ...]


class PromptExportPolicy:
    def export(
        self,
        *,
        copy_ready_prompt: str,
        compact_bundle: dict[str, Any],
        output_dir: str | Path | None = None,
        max_chars: int = 8_000,
    ) -> PromptExportFrame:
        bounded_prompt = self._bound(copy_ready_prompt, max_chars=max_chars)
        bundle = self._compact_bundle(compact_bundle)
        files_written = False
        prompt_path = "prompt.txt"
        continuation_path = "continuation.md"
        bundle_path = "compact_bundle.json"
        if output_dir is not None:
            root = Path(output_dir)
            root.mkdir(parents=True, exist_ok=True)
            prompt_path = str(root / "prompt.txt")
            continuation_path = str(root / "continuation.md")
            bundle_path = str(root / "compact_bundle.json")
            Path(prompt_path).write_text(bounded_prompt, encoding="utf-8")
            Path(continuation_path).write_text(
                self._continuation_markdown(bundle), encoding="utf-8"
            )
            Path(bundle_path).write_text(
                json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8"
            )
            files_written = True
        warnings = ("prompt_truncated",) if len(copy_ready_prompt) > max_chars else ()
        return PromptExportFrame(
            prompt_txt_path=prompt_path,
            continuation_md_path=continuation_path,
            compact_bundle_json_path=bundle_path,
            copy_ready_plain_text=bounded_prompt,
            compact_bundle=bundle,
            summary_only=True,
            bounded=True,
            files_written=files_written,
            warnings=warnings,
        )

    def _bound(self, text: str, *, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 32].rstrip() + "\n[truncated: summary-only export]"

    def _compact_bundle(self, bundle: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "handoff_summary",
            "repository_subset",
            "session_focus",
            "prompt_mode",
            "continuity_scope",
            "stale_topics",
            "rollover_required",
            "session_generation_metadata",
            "boundary_enforcement",
            "rollover_state",
            "stale_warning",
            "new_session_seed",
        }
        return {key: value for key, value in bundle.items() if key in allowed}

    def _continuation_markdown(self, bundle: dict[str, Any]) -> str:
        lines = ["# Compact Continuation", ""]
        for key, value in bundle.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines) + "\n"
