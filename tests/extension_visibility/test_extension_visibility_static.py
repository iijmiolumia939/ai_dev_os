from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("extensions/ai-dev-os-vscode")


def test_tc_presence_01_presence_commands_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}

    assert {
        "aiDevOs.showGovernancePresence",
        "aiDevOs.showRuntimeHeartbeat",
        "aiDevOs.checkExtensionVersion",
        "aiDevOs.showPresenceStatus",
        "aiDevOs.showStaleExtensionWarning",
        "aiDevOs.refreshGovernancePresence",
    }.issubset(commands)


def test_tc_presence_01_presence_activation_events_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    activation = set(package["activationEvents"])

    assert "onCommand:aiDevOs.showGovernancePresence" in activation
    assert "onCommand:aiDevOs.showRuntimeHeartbeat" in activation
    assert "onCommand:aiDevOs.checkExtensionVersion" in activation
    assert "onCommand:aiDevOs.refreshGovernancePresence" in activation


def test_tc_presence_04_presence_status_bar_is_always_visible_and_low_noise() -> None:
    source = (ROOT / "src" / "presence" / "governancePresence.ts").read_text(encoding="utf-8")

    assert "createStatusBarItem" in source
    assert "AI_DEV_OS ACTIVE GEN:" in source
    assert "LOW_PRESSURE" in source or "_PRESSURE" in source
    assert "ROLLOVER_OK" in source
    assert "RateLimitedNotifications" in source
    assert "setInterval" not in source
    assert "setTimeout" not in source


def test_tc_presence_05_extension_visibility_has_no_hidden_chat_or_network_control() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))
    forbidden = (
        "fetch(",
        "XMLHttpRequest",
        "https://",
        "http://",
        "github.copilot",
        "workbench.action.chat.submit",
        "workbench.action.chat.acceptinput",
        "playwright",
        "selenium",
    )

    assert all(item not in source.lower() for item in forbidden)
    assert "workspace.applyedit" not in source.lower()


def test_tc_presence_03_runtime_heartbeat_is_summary_only() -> None:
    source = (ROOT / "src" / "presence" / "governancePresence.ts").read_text(encoding="utf-8")

    assert "heartbeatSummary" in source
    assert "lastRuntimeAudit" in source
    assert "summaryOnly: true" in source
    assert "readFile" in source
    assert "writeFile" not in source


def test_tc_presence_05_presence_docs_exist_and_define_boundaries() -> None:
    for path in (
        Path("docs/vscode-extension/presence-indicator.md"),
        Path("docs/vscode-extension/version-mismatch.md"),
        Path("docs/vscode-extension/runtime-heartbeat.md"),
    ):
        text = path.read_text(encoding="utf-8")
        assert "FR-PRESENCE" in text
        assert "TC-PRESENCE" in text
        assert "summary" in text.lower()
        assert "自動" in text or "automatic" in text.lower()
