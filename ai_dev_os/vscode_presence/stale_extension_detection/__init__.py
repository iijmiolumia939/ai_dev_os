from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ai_dev_os.vscode_presence.version_detection import (
    ExtensionVersionFrame,
    detect_extension_version,
)

REQUIRED_COMMANDS = (
    "aiDevOs.showGovernancePresence",
    "aiDevOs.showRuntimeHeartbeat",
    "aiDevOs.checkExtensionVersion",
    "aiDevOs.showPresenceStatus",
    "aiDevOs.showStaleExtensionWarning",
    "aiDevOs.refreshGovernancePresence",
    "aiDevOs.showGovernanceCore",
    "aiDevOs.showRuntimeGraph",
    "aiDevOs.showRuntimeOverlap",
    "aiDevOs.showSimplificationRecommendations",
)

REQUIRED_TREE_VIEWS = (
    "aiDevOsSessionBoundary",
    "aiDevOsGovernanceDashboard",
    "aiDevOsGovernanceTrends",
    "aiDevOsRuntimeGraph",
    "aiDevOsRuntimeOverlap",
    "aiDevOsSharedPrimitives",
    "aiDevOsBoundedRetention",
)


@dataclass(frozen=True)
class StaleExtensionFrame:
    stale_extension_detected: bool
    missing_capabilities: tuple[str, ...]
    reinstall_required: bool
    visibility_degraded: bool
    stale_activation: bool
    stale_manifest: bool
    version: ExtensionVersionFrame
    summary_only: bool = True


def detect_stale_extension(
    workspace_root: Path | str = ".",
    *,
    installed_extensions_dir: Path | str | None = None,
) -> StaleExtensionFrame:
    root = Path(workspace_root)
    version = detect_extension_version(root, installed_extensions_dir=installed_extensions_dir)
    package = _select_manifest(root, version)
    commands = {
        item.get("command", "") for item in package.get("contributes", {}).get("commands", [])
    }
    views = {
        item.get("id", "")
        for item in package.get("contributes", {}).get("views", {}).get("explorer", [])
    }
    activation = set(package.get("activationEvents", []))
    missing_commands = tuple(
        f"command:{command}" for command in REQUIRED_COMMANDS if command not in commands
    )
    missing_views = tuple(f"view:{view}" for view in REQUIRED_TREE_VIEWS if view not in views)
    missing_activation = tuple(
        f"activation:onCommand:{command}"
        for command in REQUIRED_COMMANDS
        if f"onCommand:{command}" not in activation
    )
    missing = missing_commands + missing_views + missing_activation
    stale_manifest = bool(missing)
    stale = version.stale_extension_detected or stale_manifest
    return StaleExtensionFrame(
        stale_extension_detected=stale,
        missing_capabilities=missing,
        reinstall_required=stale,
        visibility_degraded=stale,
        stale_activation=bool(missing_activation),
        stale_manifest=stale_manifest,
        version=version,
    )


def _select_manifest(root: Path, version: ExtensionVersionFrame) -> dict[str, Any]:
    installed = (
        Path(version.installed_paths[-1]) / "package.json" if version.installed_paths else None
    )
    if installed and installed.exists():
        return _read_json(installed)
    return _read_json(root / "extensions" / "ai-dev-os-vscode" / "package.json")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}
