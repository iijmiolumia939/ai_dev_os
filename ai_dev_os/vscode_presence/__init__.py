from __future__ import annotations

from ai_dev_os.vscode_presence.presence_state import GovernancePresenceFrame, build_presence_frame
from ai_dev_os.vscode_presence.runtime_heartbeat import (
    RuntimeHeartbeatFrame,
    build_heartbeat_frame,
)
from ai_dev_os.vscode_presence.stale_extension_detection import (
    StaleExtensionFrame,
    detect_stale_extension,
)
from ai_dev_os.vscode_presence.status_projection import (
    GovernanceStatusProjectionFrame,
    project_governance_status,
)
from ai_dev_os.vscode_presence.version_detection import (
    ExtensionVersionFrame,
    detect_extension_version,
)

__all__ = [
    "ExtensionVersionFrame",
    "GovernancePresenceFrame",
    "GovernanceStatusProjectionFrame",
    "RuntimeHeartbeatFrame",
    "StaleExtensionFrame",
    "build_heartbeat_frame",
    "build_presence_frame",
    "detect_extension_version",
    "detect_stale_extension",
    "project_governance_status",
]
