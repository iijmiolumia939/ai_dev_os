from __future__ import annotations

import json
from pathlib import Path

from ai_dev_os.runtime_graph import RuntimeGraphPolicy
from ai_dev_os.runtime_simplification.contract_overlap import RuntimeContractOverlapPolicy

ROOT = Path("extensions/ai-dev-os-vscode")


def test_contract_overlap_validation() -> None:
    graph = RuntimeGraphPolicy().evaluate(".")
    frame = RuntimeContractOverlapPolicy().detect(graph.contract_surface)

    assert frame.contract_overlap_detected is True
    assert frame.duplicated_contract_groups
    assert frame.contract_fragmentation_pressure in {"low", "medium", "high"}
    assert frame.contract_simplification_recommended is True
    assert frame.summary_only is True
    assert frame.full_signature_export_used is False
    assert frame.raw_ast_export_used is False


def test_contract_overlap_is_bounded() -> None:
    graph = RuntimeGraphPolicy().evaluate(".")
    frame = RuntimeContractOverlapPolicy().detect(graph.contract_surface, max_groups=2)

    assert len(frame.duplicated_contract_groups) <= 2


def test_vscode_simplification_commands_are_declared_and_registered() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))
    required = {
        "aiDevOs.showRuntimeOverlap",
        "aiDevOs.showContractOverlap",
        "aiDevOs.showMergeCandidates",
        "aiDevOs.showGovernanceDuplication",
        "aiDevOs.showSimplificationRecommendations",
        "aiDevOs.compactSimplificationView",
    }

    assert required.issubset(commands)
    for command in required:
        assert command in source


def test_vscode_simplification_views_and_rate_limiting() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    view_ids = {item["id"] for item in package["contributes"]["views"]["explorer"]}
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert {
        "aiDevOsRuntimeOverlap",
        "aiDevOsContractOverlap",
        "aiDevOsMergeCandidates",
    }.issubset(view_ids)
    assert "registerTreeDataProvider('aiDevOsRuntimeOverlap'" in source
    assert "registerTreeDataProvider('aiDevOsContractOverlap'" in source
    assert "registerTreeDataProvider('aiDevOsMergeCandidates'" in source
    assert "RateLimitedNotifications" in source
    assert "runtime-simplification-governance-warning" in source


def test_vscode_simplification_has_no_network_or_chat_automation() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))
    lowered = source.lower()
    forbidden = (
        "fetch(",
        "xmlhttprequest",
        "https://",
        "http://",
        "workbench.action.chat",
        "github.copilot",
        "git commit",
        "git push",
    )

    assert all(item not in lowered for item in forbidden)
    assert "automaticmutationused: false" in lowered
