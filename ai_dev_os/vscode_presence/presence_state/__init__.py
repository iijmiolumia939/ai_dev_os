from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GovernancePresenceFrame:
    extension_active: bool
    runtime_audit_active: bool
    governance_core_active: bool
    session_boundary_active: bool
    persistence_active: bool
    runtime_graph_active: bool
    current_session_generation: int
    rollover_pending: bool
    stale_session_detected: bool
    bounded_presence_confirmed: bool
    summary_only: bool = True
    raw_transcript_included: bool = False


def build_presence_frame(
    workspace_root: Path | str = ".",
    *,
    runtime_audit_active: bool = True,
    governance_core_active: bool = True,
    runtime_graph_active: bool = True,
) -> GovernancePresenceFrame:
    root = Path(workspace_root)
    extension_root = root / "extensions" / "ai-dev-os-vscode"
    state = _read_json(root / ".ai-dev-os" / "session-boundary.json")
    rollover = _read_json(root / ".ai-dev-os" / "rollover-state.json")
    stale_state = _as_mapping(state.get("stale_warning_state"))
    rollover_state = _as_mapping(state.get("rollover_state")) | rollover
    current_generation = int(state.get("current_session_generation", 1))
    rollover_pending = bool(rollover_state.get("rollover_pending", False))
    stale_detected = bool(
        stale_state.get("stale_session_detected", rollover.get("stale_session_active", False))
    )
    persistence_active = all(
        (root / ".ai-dev-os" / file_name).exists()
        for file_name in (
            "session-boundary.json",
            "rollover-state.json",
            "continuity-index.json",
        )
    )
    extension_active = (extension_root / "package.json").exists() and (
        extension_root / "src" / "extension.ts"
    ).exists()
    bounded = bool(state.get("bounded", True)) and bool(state.get("summary_only", True))
    return GovernancePresenceFrame(
        extension_active=extension_active,
        runtime_audit_active=runtime_audit_active,
        governance_core_active=governance_core_active,
        session_boundary_active=persistence_active,
        persistence_active=persistence_active,
        runtime_graph_active=runtime_graph_active,
        current_session_generation=current_generation,
        rollover_pending=rollover_pending,
        stale_session_detected=stale_detected,
        bounded_presence_confirmed=bounded
        and persistence_active
        and not _has_raw_transcript(state),
    )


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _as_mapping(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _has_raw_transcript(value: object) -> bool:
    if isinstance(value, dict):
        return any(
            key == "raw_transcript" or _has_raw_transcript(child) for key, child in value.items()
        )
    if isinstance(value, list | tuple):
        return any(_has_raw_transcript(child) for child in value)
    return False
