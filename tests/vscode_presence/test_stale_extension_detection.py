from __future__ import annotations

import json
from pathlib import Path

from ai_dev_os.vscode_presence.stale_extension_detection import detect_stale_extension


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_tc_presence_02_stale_extension_reports_missing_commands_and_views(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    _write_json(
        root / "extensions" / "ai-dev-os-vscode" / "package.json",
        {"version": "0.1.0-alpha.3"},
    )
    _write_json(
        installed / "iijmiolumia939.ai-dev-os-vscode-0.1.0" / "package.json",
        {
            "version": "0.1.0",
            "activationEvents": ["onCommand:aiDevOs.sessionAudit"],
            "contributes": {
                "commands": [{"command": "aiDevOs.sessionAudit"}],
                "views": {"explorer": [{"id": "aiDevOsSessionBoundary"}]},
            },
        },
    )

    frame = detect_stale_extension(root, installed_extensions_dir=installed)

    assert frame.stale_extension_detected is True
    assert frame.reinstall_required is True
    assert frame.visibility_degraded is True
    assert frame.stale_activation is True
    assert "command:aiDevOs.showGovernancePresence" in frame.missing_capabilities
    assert "view:aiDevOsRuntimeGraph" in frame.missing_capabilities


def test_tc_presence_02_current_manifest_has_no_missing_capabilities(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    commands = [
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
    ]
    views = [
        "aiDevOsSessionBoundary",
        "aiDevOsGovernanceDashboard",
        "aiDevOsGovernanceTrends",
        "aiDevOsRuntimeGraph",
        "aiDevOsRuntimeOverlap",
        "aiDevOsSharedPrimitives",
        "aiDevOsBoundedRetention",
    ]
    manifest = {
        "version": "0.1.0-alpha.3",
        "activationEvents": [f"onCommand:{command}" for command in commands],
        "contributes": {
            "commands": [{"command": command} for command in commands],
            "views": {"explorer": [{"id": view} for view in views]},
        },
    }
    _write_json(root / "extensions" / "ai-dev-os-vscode" / "package.json", manifest)
    _write_json(
        installed / "iijmiolumia939.ai-dev-os-vscode-0.1.0-alpha.3" / "package.json", manifest
    )

    frame = detect_stale_extension(root, installed_extensions_dir=installed)

    assert frame.stale_extension_detected is False
    assert frame.missing_capabilities == ()
    assert frame.reinstall_required is False
