from __future__ import annotations

import json
from pathlib import Path

from ai_dev_os.runtime_graph.contract_surface import RuntimeContractSurfacePolicy
from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryPolicy

ROOT = Path("extensions/ai-dev-os-vscode")


def test_contract_surface_validation() -> None:
    discovery = RuntimeDiscoveryPolicy().discover(".")
    frame = RuntimeContractSurfacePolicy().summarize(discovery, max_contract_surface=32)

    assert frame.contract_surface_size > 0
    assert frame.runtime_api_pressure in {"low", "medium", "high"}
    assert frame.exported_frames
    assert frame.exported_policies
    assert frame.exported_contracts
    assert frame.public_runtime_apis
    assert frame.full_signature_replay_used is False
    assert frame.raw_ast_export_used is False


def test_contract_surface_is_bounded() -> None:
    discovery = RuntimeDiscoveryPolicy().discover(".")
    frame = RuntimeContractSurfacePolicy().summarize(discovery, max_contract_surface=8)

    assert len(frame.exported_frames) <= 8
    assert len(frame.exported_policies) <= 8
    assert len(frame.exported_contracts) <= 8
    assert len(frame.public_runtime_apis) <= 8


def test_vscode_runtime_graph_commands_are_declared_and_registered() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))
    required = {
        "aiDevOs.showRuntimeGraph",
        "aiDevOs.showRuntimeClusters",
        "aiDevOs.showContractSurface",
        "aiDevOs.showArchitecturePressure",
        "aiDevOs.showOversizedRuntimeWarnings",
        "aiDevOs.compactRuntimeGraph",
    }

    assert required.issubset(commands)
    for command in required:
        assert command in source


def test_vscode_runtime_graph_views_and_rate_limiting() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    view_ids = {item["id"] for item in package["contributes"]["views"]["explorer"]}
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert {"aiDevOsRuntimeGraph", "aiDevOsRuntimeClusters"}.issubset(view_ids)
    assert "registerTreeDataProvider('aiDevOsRuntimeGraph'" in source
    assert "registerTreeDataProvider('aiDevOsRuntimeClusters'" in source
    assert "RateLimitedNotifications" in source
    assert "runtime-graph-oversized-warning" in source


def test_vscode_runtime_graph_has_no_network_or_chat_automation() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))
    forbidden = ("fetch(", "XMLHttpRequest", "https://", "http://", "playwright", "selenium")

    assert all(item not in source for item in forbidden)
    assert "workbench.action.chat" not in source
    assert "github.copilot" not in source.lower()
