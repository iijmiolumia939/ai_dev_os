from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.vscode_presence.presence_state import GovernancePresenceFrame


@dataclass(frozen=True)
class GovernanceStatusProjectionFrame:
    compact_status: str
    severity: str
    pressure_projection: str
    rollover_projection: str
    stale_projection: str
    notification_required: bool
    summary_only: bool = True
    automatic_action_allowed: bool = False


def project_governance_status(
    presence: GovernancePresenceFrame,
    *,
    pressure: str = "LOW",
    stale_extension_detected: bool = False,
) -> GovernanceStatusProjectionFrame:
    normalized_pressure = pressure.upper()
    rollover = "ROLLOVER_PENDING" if presence.rollover_pending else "ROLLOVER_OK"
    stale = "STALE" if presence.stale_session_detected or stale_extension_detected else "FRESH"
    if (
        stale_extension_detected
        or presence.stale_session_detected
        or normalized_pressure in {"HIGH", "CRITICAL"}
    ):
        severity = "WARNING"
    elif presence.rollover_pending:
        severity = "NOTICE"
    else:
        severity = "OK"
    active = "ACTIVE" if presence.extension_active and presence.runtime_audit_active else "PARTIAL"
    compact = " ".join(
        (
            f"AI_DEV_OS {active}",
            f"GEN:{presence.current_session_generation}",
            f"{normalized_pressure}_PRESSURE",
            rollover,
        )
    )
    return GovernanceStatusProjectionFrame(
        compact_status=compact,
        severity=severity,
        pressure_projection=f"{normalized_pressure}_PRESSURE",
        rollover_projection=rollover,
        stale_projection=stale,
        notification_required=severity == "WARNING",
    )
