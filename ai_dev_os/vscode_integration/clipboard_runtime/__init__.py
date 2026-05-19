from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.vscode_integration.prompt_export import PromptExportFrame, PromptExportPolicy


@dataclass(frozen=True)
class ClipboardRuntimeFrame:
    clipboard_available: bool
    clipboard_copy_success: bool
    export_fallback: bool
    compact_export_mode: bool
    fallback_export: PromptExportFrame | None
    warnings: tuple[str, ...]


class ClipboardRuntimePolicy:
    def copy(
        self,
        *,
        copy_ready_prompt: str,
        compact_bundle: dict[str, object],
        output_dir: str | Path | None = None,
        clipboard_command: str | None = None,
    ) -> ClipboardRuntimeFrame:
        command = clipboard_command or self._default_command()
        available = bool(command and shutil.which(command))
        success = False
        warnings: list[str] = []
        if available:
            completed = subprocess.run(
                (command,),
                input=copy_ready_prompt,
                text=True,
                capture_output=True,
                check=False,
            )
            success = completed.returncode == 0
            if not success:
                warnings.append("clipboard_copy_failed")
        else:
            warnings.append("clipboard_unavailable")
        fallback = None
        if not success:
            fallback = PromptExportPolicy().export(
                copy_ready_prompt=copy_ready_prompt,
                compact_bundle=compact_bundle,
                output_dir=output_dir,
            )
        return ClipboardRuntimeFrame(
            clipboard_available=available,
            clipboard_copy_success=success,
            export_fallback=not success,
            compact_export_mode=True,
            fallback_export=fallback,
            warnings=tuple(warnings),
        )

    def _default_command(self) -> str:
        for command in ("clip", "pbcopy", "xclip"):
            if shutil.which(command):
                return command
        return ""
