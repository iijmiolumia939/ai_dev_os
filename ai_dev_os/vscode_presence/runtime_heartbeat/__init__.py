from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import time


@dataclass(frozen=True)
class RuntimeHeartbeatFrame:
    last_runtime_audit: float
    last_continuity_export: float
    last_persistence_restore: float
    last_rollover_evaluation: float
    last_governance_trend_update: float
    heartbeat_active: bool
    heartbeat_age: float
    stale_heartbeat: bool
    heartbeat_summary: str
    summary_only: bool = True
    full_logs_included: bool = False


def build_heartbeat_frame(
    workspace_root: Path | str = ".",
    *,
    now: float | None = None,
    stale_after_seconds: int = 86_400,
) -> RuntimeHeartbeatFrame:
    root = Path(workspace_root)
    current_time = time() if now is None else now
    session_boundary = root / ".ai-dev-os" / "session-boundary.json"
    rollover_state = root / ".ai-dev-os" / "rollover-state.json"
    continuity_index = root / ".ai-dev-os" / "continuity-index.json"
    prompt_mode = root / ".ai-dev-os" / "prompt-mode-state.json"
    trend_source = root / "extensions" / "ai-dev-os-vscode" / "src" / "governance" / "trends.ts"
    stamps = (
        _mtime(session_boundary),
        _mtime(continuity_index),
        _mtime(session_boundary),
        _mtime(rollover_state),
        _mtime(trend_source) or _mtime(prompt_mode),
    )
    known = tuple(stamp for stamp in stamps if stamp > 0)
    latest = max(known, default=0.0)
    age = max(0.0, current_time - latest) if latest else float("inf")
    active = bool(known)
    stale = not active or age > stale_after_seconds
    summary = "ACTIVE" if active and not stale else "STALE" if active else "MISSING"
    return RuntimeHeartbeatFrame(
        last_runtime_audit=stamps[0],
        last_continuity_export=stamps[1],
        last_persistence_restore=stamps[2],
        last_rollover_evaluation=stamps[3],
        last_governance_trend_update=stamps[4],
        heartbeat_active=active and not stale,
        heartbeat_age=round(age, 3) if age != float("inf") else age,
        stale_heartbeat=stale,
        heartbeat_summary=summary,
    )


def _mtime(path: Path) -> float:
    return path.stat().st_mtime if path.exists() else 0.0
