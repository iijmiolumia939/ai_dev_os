from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("extensions/ai-dev-os-vscode")


def _package() -> dict[str, object]:
    return json.loads((ROOT / "package.json").read_text(encoding="utf-8"))


def _extension_source() -> str:
    return (ROOT / "src" / "extension.ts").read_text(encoding="utf-8")


def _registry_source() -> str:
    return (ROOT / "src" / "registration" / "registrationRegistry.ts").read_text(
        encoding="utf-8"
    )


def test_duplicate_command_registration_is_visible_and_blocked() -> None:
    source = _registry_source()

    assert "class RegistrationConflictGuard" in source
    assert "kind: 'command' | 'status'" in source
    assert "this.conflicts.push" in source
    assert "return false" in source
    assert "Duplicate registrations were skipped" in _extension_source()


def test_package_commands_and_activation_events_are_unique() -> None:
    package = _package()
    commands = [item["command"] for item in package["contributes"]["commands"]]
    activation = [
        item.removeprefix("onCommand:")
        for item in package["activationEvents"]
        if item.startswith("onCommand:")
    ]

    assert len(commands) == len(set(commands))
    assert len(activation) == len(set(activation))
    assert set(commands) == set(activation)


def test_registration_namespace_stability() -> None:
    package = _package()
    commands = [item["command"] for item in package["contributes"]["commands"]]
    source = _registry_source()

    assert all(command.startswith("aiDevOs.") for command in commands)
    assert "acceptCommand" in source
    assert "commandId.startsWith('aiDevOs.')" in source
    assert "acceptStatus" in source
    assert "statusId.startsWith('AI_DEV_OS ')" in source


def test_deterministic_activation_ordering_is_explicit() -> None:
    source = _extension_source()
    command_orders = [
        int(value)
        for value in re.findall(
            r"\{order: (\d+), namespace: '[^']+', commandIds:",
            source,
        )
    ]
    status_orders = [
        int(value)
        for value in re.findall(
            r"\{order: (\d+), namespace: '[^']+', statusId:",
            source,
        )
    ]

    assert command_orders == sorted(command_orders)
    assert status_orders == sorted(status_orders)
    assert len(command_orders) == len(set(command_orders))
    assert len(status_orders) == len(set(status_orders))
    assert "deterministicOrder" in _registry_source()


def test_bounded_registration_retention() -> None:
    package = _package()
    commands = [item["command"] for item in package["contributes"]["commands"]]
    status_ids = re.findall(r"statusId: '([^']+)'", _extension_source())
    source = _registry_source()

    assert len(commands) <= 360
    assert len(status_ids) <= 240
    assert len(status_ids) == len(set(status_ids))
    assert "maxCommands = 360" in source
    assert "maxStatusBars = 240" in source
    assert "maxGroups = 96" in source


def test_extension_uses_bounded_registry_composition() -> None:
    source = _extension_source()

    assert "new CommandRegistrationRegistry" in source
    assert "new StatusBarRegistrationRegistry" in source
    assert source.count("context.subscriptions.push(") == 1
    assert "treeDataProviders" in source
    assert "commandRegistry.register" in source
    assert "statusRegistry.register" in source


def test_registration_stabilization_avoids_dynamic_loading() -> None:
    combined = _extension_source() + "\n" + _registry_source()

    forbidden = (
        "import(",
        "require(",
        "readdir",
        "glob",
        "rglob",
        "dynamic module",
        "self-register",
    )

    assert all(token not in combined for token in forbidden)