from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

FORBIDDEN_KEYS = {
    "raw_transcript",
    "full_prompt_history",
    "provider_responses",
    "full_architecture_history",
    "telemetry_uploads",
}


@dataclass(frozen=True)
class PersistenceStoreFrame:
    current_session_generation: int
    rollover_state: dict[str, Any]
    last_continuity_bundle: dict[str, Any]
    current_prompt_mode: str
    session_focus: str
    stale_warning_state: dict[str, Any]
    repository_subset_summary: tuple[str, ...]
    compact_continuity_metadata: dict[str, Any]
    store_path: str
    bounded: bool
    summary_only: bool
    forbidden_keys_removed: tuple[str, ...]


class PersistenceStorePolicy:
    def build(
        self,
        *,
        current_session_generation: int,
        rollover_state: dict[str, Any],
        last_continuity_bundle: dict[str, Any],
        current_prompt_mode: str,
        session_focus: str,
        stale_warning_state: dict[str, Any],
        repository_subset_summary: tuple[str, ...],
        compact_continuity_metadata: dict[str, Any],
        workspace: str | Path = ".",
    ) -> PersistenceStoreFrame:
        removed = tuple(
            key
            for payload in (
                rollover_state,
                last_continuity_bundle,
                stale_warning_state,
                compact_continuity_metadata,
            )
            for key in payload
            if key in FORBIDDEN_KEYS
        )
        return PersistenceStoreFrame(
            current_session_generation=max(1, current_session_generation),
            rollover_state=self._sanitize(rollover_state),
            last_continuity_bundle=self._sanitize(last_continuity_bundle),
            current_prompt_mode=current_prompt_mode or "bounded_implementation",
            session_focus=session_focus or "bounded-implementation",
            stale_warning_state=self._sanitize(stale_warning_state),
            repository_subset_summary=repository_subset_summary[:5],
            compact_continuity_metadata=self._sanitize(compact_continuity_metadata),
            store_path=str(Path(workspace) / ".ai-dev-os" / "session-boundary.json"),
            bounded=True,
            summary_only=True,
            forbidden_keys_removed=tuple(dict.fromkeys(removed)),
        )

    def write(self, frame: PersistenceStoreFrame) -> PersistenceStoreFrame:
        path = Path(frame.store_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(frame), indent=2, sort_keys=True), encoding="utf-8")
        return frame

    def read(self, workspace: str | Path = ".") -> PersistenceStoreFrame | None:
        path = Path(workspace) / ".ai-dev-os" / "session-boundary.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return PersistenceStoreFrame(
            current_session_generation=data["current_session_generation"],
            rollover_state=data["rollover_state"],
            last_continuity_bundle=data["last_continuity_bundle"],
            current_prompt_mode=data["current_prompt_mode"],
            session_focus=data["session_focus"],
            stale_warning_state=data["stale_warning_state"],
            repository_subset_summary=tuple(data["repository_subset_summary"]),
            compact_continuity_metadata=data["compact_continuity_metadata"],
            store_path=data["store_path"],
            bounded=data["bounded"],
            summary_only=data["summary_only"],
            forbidden_keys_removed=tuple(data["forbidden_keys_removed"]),
        )

    def _sanitize(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in payload.items() if key not in FORBIDDEN_KEYS}
