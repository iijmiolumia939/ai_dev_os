from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("extensions/ai-dev-os-vscode")


def test_extension_commands_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}

    assert {
        "aiDevOs.sessionAudit",
        "aiDevOs.generateHandoff",
        "aiDevOs.copyContinuityBundle",
        "aiDevOs.openNewSessionPrompt",
        "aiDevOs.confirmSessionRollover",
        "aiDevOs.showSessionBoundaryState",
        "aiDevOs.compactCurrentSession",
        "aiDevOs.showStaleSessionWarning",
        "aiDevOs.showReasoningTier",
        "aiDevOs.showCostBudget",
        "aiDevOs.showEscalationPolicy",
        "aiDevOs.showSprintReasoningMap",
        "aiDevOs.compactReasoningScope",
    }.issubset(commands)


def test_extension_has_local_state_without_telemetry() -> None:
    source = (ROOT / "src" / "state" / "boundaryState.ts").read_text(encoding="utf-8")

    assert "currentSessionGeneration" in source
    assert "lastRolloverTimestamp" in source
    assert "currentEnforcementState" in source
    assert "lastExportedContinuityBundle" in source
    assert "staleWarningCount" in source
    assert "pendingRolloverState" in source
    assert "telemetry" not in source.lower()


def test_extension_notification_rate_limiting() -> None:
    source = (ROOT / "src" / "notifications" / "rateLimitedNotifications.ts").read_text(
        encoding="utf-8"
    )

    assert "minIntervalMs" in source
    assert "return false" in source
    assert "showWarningMessage" in source


def test_extension_no_network_dependency_or_chat_ui_automation() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    forbidden = ("fetch(", "XMLHttpRequest", "https://", "http://", "playwright", "selenium")
    assert all(item not in source for item in forbidden)
    assert "workbench.action.chat.submit" not in source
    assert "workbench.action.chat.acceptInput" not in source
    assert "github.copilot" not in source.lower()


def test_extension_clipboard_and_handoff_support_are_local_only() -> None:
    clipboard = (ROOT / "src" / "clipboard" / "continuityClipboard.ts").read_text(encoding="utf-8")
    handoff = (ROOT / "src" / "handoff" / "handoffClient.ts").read_text(encoding="utf-8")

    assert "vscode.env.clipboard.writeText" in clipboard
    assert "ai_dev_os.cli" in handoff
    assert "execFile" in handoff
    assert "timeout" in handoff
