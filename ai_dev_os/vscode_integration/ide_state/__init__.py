from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class IDEStateFrame:
    active_workspace: str
    active_repo: str
    active_sprint: str
    active_prompt_mode: str
    current_session_focus: str
    pending_rollover: bool
    export_availability: bool
    telemetry_collected: bool
    network_used: bool


class IDEStatePolicy:
    def snapshot(
        self,
        workspace: str | Path = ".",
        *,
        active_sprint: str = "next",
        active_prompt_mode: str = "bounded_implementation",
        current_session_focus: str = "implementation",
        pending_rollover: bool = False,
        export_availability: bool = True,
    ) -> IDEStateFrame:
        root = Path(workspace).resolve()
        return IDEStateFrame(
            active_workspace=str(root),
            active_repo=root.name,
            active_sprint=active_sprint,
            active_prompt_mode=active_prompt_mode,
            current_session_focus=current_session_focus,
            pending_rollover=pending_rollover,
            export_availability=export_availability,
            telemetry_collected=False,
            network_used=False,
        )
