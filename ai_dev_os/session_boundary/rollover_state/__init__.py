from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RolloverStateFrame:
    rollover_pending: bool
    handoff_generated: bool
    clipboard_ready: bool
    export_ready: bool
    confirmation_pending: bool
    new_session_started: bool
    stale_session_active: bool


class RolloverStatePolicy:
    def evaluate(
        self,
        *,
        rollover_required: bool,
        handoff_generated: bool = False,
        clipboard_ready: bool = False,
        export_ready: bool = False,
        confirmed: bool = False,
        new_session_started: bool = False,
        stale_session_active: bool = False,
    ) -> RolloverStateFrame:
        pending = rollover_required and not new_session_started
        return RolloverStateFrame(
            rollover_pending=pending,
            handoff_generated=handoff_generated,
            clipboard_ready=clipboard_ready,
            export_ready=export_ready,
            confirmation_pending=pending and not confirmed,
            new_session_started=new_session_started,
            stale_session_active=stale_session_active,
        )
