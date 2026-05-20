from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("extensions/ai-dev-os-vscode")


def test_persistence_commands_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}

    assert {
        "aiDevOs.restoreSessionState",
        "aiDevOs.showPersistenceState",
        "aiDevOs.cleanupStalePersistence",
        "aiDevOs.exportLocalContinuityIndex",
        "aiDevOs.resetLocalSessionState",
    }.issubset(commands)


def test_extension_startup_restore_is_local_only() -> None:
    source = (ROOT / "src" / "extension.ts").read_text(encoding="utf-8")

    assert "persistence.ensure" in source
    assert "persistence.read" in source
    assert "startup-persistence-warning" in source
    assert "telemetry" not in source.lower()


def test_local_persistence_store_uses_workspace_files() -> None:
    source = (ROOT / "src" / "persistence" / "localPersistence.ts").read_text(encoding="utf-8")

    assert ".ai-dev-os" in source
    assert "session-boundary.json" in source
    assert "checkpoints" in source
    assert "summary_only: true" in source
    assert "bounded: true" in source


def test_vscode_persistence_has_no_network_telemetry_or_ui_automation() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    forbidden = (
        "fetch(",
        "XMLHttpRequest",
        "https://",
        "http://",
        "telemetry",
        "github.copilot",
        "workbench.action.chat.submit",
        "workbench.action.chat.acceptinput",
    )
    assert all(item not in source.lower() for item in forbidden)


def test_gitignore_excludes_workspace_local_persistence() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    assert ".ai-dev-os/" in gitignore
    assert "telemetry-artifacts/" in gitignore


def test_persistence_docs_exist_and_are_bounded() -> None:
    for path in (
        Path("docs/workspace-persistence.md"),
        Path("docs/extension-continuity-recovery.md"),
        Path("docs/local-bounded-persistence.md"),
    ):
        text = path.read_text(encoding="utf-8")
        assert "FR-PERSISTENCE" in text
        assert "TC-PERSISTENCE" in text
        assert "cloud sync" in text or "workspace-local" in text
