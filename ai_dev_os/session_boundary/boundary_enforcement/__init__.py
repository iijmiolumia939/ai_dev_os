from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.session_boundary.stale_session_detection import StaleSessionFrame

ACTIVE = "ACTIVE"
WARNING = "WARNING"
ROLLOVER_REQUIRED = "ROLLOVER_REQUIRED"
STALE_BLOCKED = "STALE_BLOCKED"


@dataclass(frozen=True)
class BoundaryEnforcementFrame:
    enforcement_state: str
    session_continue_allowed: bool
    compact_only_allowed: bool
    architecture_isolation_required: bool
    bounded_patch_only_required: bool
    human_confirmation_required: bool
    ai_response_blocking_enforced: bool


class BoundaryEnforcementPolicy:
    def enforce(
        self,
        *,
        stale_session: StaleSessionFrame,
        architecture_isolation_signal: bool = False,
    ) -> BoundaryEnforcementFrame:
        state = self._state(stale_session)
        return BoundaryEnforcementFrame(
            enforcement_state=state,
            session_continue_allowed=state in {ACTIVE, WARNING},
            compact_only_allowed=state in {WARNING, ROLLOVER_REQUIRED, STALE_BLOCKED},
            architecture_isolation_required=architecture_isolation_signal
            or stale_session.architecture_topic_accumulation,
            bounded_patch_only_required=state != ACTIVE,
            human_confirmation_required=state in {ROLLOVER_REQUIRED, STALE_BLOCKED},
            ai_response_blocking_enforced=False,
        )

    def _state(self, stale_session: StaleSessionFrame) -> str:
        if stale_session.new_session_required:
            return STALE_BLOCKED
        if stale_session.rollover_required:
            return ROLLOVER_REQUIRED
        if stale_session.stale_session_detected:
            return WARNING
        return ACTIVE
