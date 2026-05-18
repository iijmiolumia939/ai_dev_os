from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Checkpoint:
    active_requirements: tuple[str, ...] = ()
    active_open_questions: tuple[str, ...] = ()
    changed_modules: tuple[str, ...] = ()
    active_risks: tuple[str, ...] = ()
    latest_gates: tuple[str, ...] = ()
    next_sprint_focus: tuple[str, ...] = ()


def write_checkpoint(checkpoint: Checkpoint, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(checkpoint), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path
