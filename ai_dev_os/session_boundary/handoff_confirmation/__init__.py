from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HandoffConfirmationFrame:
    handoff_confirmed: bool
    export_consumed: bool
    prompt_copied: bool
    new_session_acknowledged: bool
    stale_session_closed: bool
    ui_automation_used: bool
    human_confirmed: bool


class HandoffConfirmationPolicy:
    def confirm(
        self,
        *,
        export_consumed: bool,
        prompt_copied: bool,
        new_session_acknowledged: bool,
        stale_session_closed: bool,
    ) -> HandoffConfirmationFrame:
        confirmed = all(
            (export_consumed, prompt_copied, new_session_acknowledged, stale_session_closed)
        )
        return HandoffConfirmationFrame(
            handoff_confirmed=confirmed,
            export_consumed=export_consumed,
            prompt_copied=prompt_copied,
            new_session_acknowledged=new_session_acknowledged,
            stale_session_closed=stale_session_closed,
            ui_automation_used=False,
            human_confirmed=confirmed,
        )
