from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("extensions/ai-dev-os-vscode")


def _source_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))


def test_tc_draftinject_01_commands_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"]: item["title"] for item in package["contributes"]["commands"]}

    assert commands["aiDevOs.startNewSprintSession"] == "AI_DEV_OS: Start New Sprint Session"
    assert commands["aiDevOs.openBootstrapChat"] == "AI_DEV_OS: Open Bootstrap Chat"
    assert commands["aiDevOs.previewBootstrapDraft"] == "AI_DEV_OS: Preview Bootstrap Draft"
    assert commands["aiDevOs.retryDraftInjection"] == "AI_DEV_OS: Retry Draft Injection"
    assert commands["aiDevOs.showEnterOnlyState"] == "AI_DEV_OS: Show Enter-Only State"


def test_tc_draftinject_02_activation_events_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    activation = set(package["activationEvents"])

    assert "onCommand:aiDevOs.startNewSprintSession" in activation
    assert "onCommand:aiDevOs.openBootstrapChat" in activation
    assert "onCommand:aiDevOs.previewBootstrapDraft" in activation
    assert "onCommand:aiDevOs.retryDraftInjection" in activation
    assert "onCommand:aiDevOs.showEnterOnlyState" in activation


def test_tc_draftinject_03_extension_uses_visible_prefill_and_status_states() -> None:
    source = _source_text()

    assert "workbench.action.chat.open" in source
    assert "isPartialQuery" in source
    assert "AI_DEV_OS ENTER_READY" in source
    assert "AI_DEV_OS WAITING_FOR_SEND" in source
    assert "bootstrap-draft" in source


def test_tc_draftinject_04_extension_does_not_dispatch_chat_send() -> None:
    source = _source_text().lower()
    forbidden = (
        "workbench.action.chat.submit",
        "workbench.action.chat.acceptinput",
        "acceptinput",
        "sendrequest",
        "background_message_dispatch: true",
        "auto_send: true",
        "hidden_continuation: true",
        "silent_prompt_mutation: true",
    )

    assert all(item not in source for item in forbidden)


def test_tc_draftinject_05_clipboard_fallback_is_explicit() -> None:
    source = _source_text()

    assert "clipboard.copy(result.draft_text)" in source
    assert "bootstrap-draft-clipboard-fallback" in source
    assert "Press Enter/Send" in source
