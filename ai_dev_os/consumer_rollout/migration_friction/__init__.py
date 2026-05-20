from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ai_dev_os.vscode_presence.stale_extension_detection import detect_stale_extension


@dataclass(frozen=True)
class MigrationFrictionFrame:
    friction_level: str
    friction_categories: tuple[str, ...]
    rollout_blockers: tuple[str, ...]
    recommended_human_actions: tuple[str, ...]
    summary_only: bool = True
    automatic_migration_used: bool = False
    workspace_mutation_used: bool = False


class MigrationFrictionPolicy:
    def evaluate(
        self,
        consumer_repo: str | Path,
        *,
        platform_repo: str | Path = ".",
        installed_extensions_dir: str | Path | None = None,
        max_continuity_bytes: int = 12_000,
        python_version: tuple[int, int] | None = None,
    ) -> MigrationFrictionFrame:
        consumer = Path(consumer_repo)
        platform = Path(platform_repo)
        categories: list[str] = []
        blockers: list[str] = []
        actions: list[str] = []
        stale = detect_stale_extension(platform, installed_extensions_dir=installed_extensions_dir)
        if stale.stale_extension_detected:
            categories.append("stale_extension_mismatch")
            actions.append("reinstall current AI_DEV_OS VSIX after human review")
        gitignore = _read_text(consumer / ".gitignore")
        if ".ai-dev-os/" not in gitignore:
            categories.append("missing_gitignore_persistence_rule")
            actions.append("add .ai-dev-os/ to consumer .gitignore before rollout")
        if not (consumer / ".ai-dev-os").exists():
            categories.append("missing_session_lifecycle_setup")
            actions.append("initialize bounded local session state after approval")
        if not _has_runtime_audit_integration(consumer):
            categories.append("missing_runtime_audit_integration")
            actions.append("document how consumer invokes python -m ai_dev_os.runtime_audit")
        if not _has_vscode_tasks(consumer):
            categories.append("missing_vscode_tasks")
            actions.append("add optional VSCode task definitions in a human-confirmed change")
        if not _has_governance_commands(platform):
            categories.append("missing_governance_commands")
            blockers.append("platform VSCode manifest missing governance commands")
        runtime_version = python_version or (sys.version_info.major, sys.version_info.minor)
        if runtime_version < (3, 11):
            categories.append("incompatible_python_version")
            blockers.append("Python 3.11+ required")
        if _continuity_size(consumer) > max_continuity_bytes:
            categories.append("oversized_continuity_bundle")
            actions.append("compact consumer continuity bundle before rollout")
        if not _docs_fresh(consumer):
            categories.append("stale_rollout_docs")
            actions.append("refresh consumer rollout notes with current alpha boundary")
        level = _level(categories, blockers)
        return MigrationFrictionFrame(
            friction_level=level,
            friction_categories=tuple(dict.fromkeys(categories)),
            rollout_blockers=tuple(dict.fromkeys(blockers)),
            recommended_human_actions=tuple(dict.fromkeys(actions)),
        )


def _has_runtime_audit_integration(root: Path) -> bool:
    candidates = (root / "pyproject.toml", root / "run_tests.ps1", root / "README.md")
    text = "\n".join(_read_text(path) for path in candidates).lower()
    return "runtime_audit" in text or "runtime audit" in text or "ai_dev_os" in text


def _has_vscode_tasks(root: Path) -> bool:
    return (root / ".vscode" / "tasks.json").exists()


def _has_governance_commands(platform: Path) -> bool:
    package = _read_json(platform / "extensions" / "ai-dev-os-vscode" / "package.json")
    commands = {item.get("command") for item in package.get("contributes", {}).get("commands", [])}
    required = {
        "aiDevOs.showGovernancePresence",
        "aiDevOs.showRuntimeGraph",
        "aiDevOs.showSimplificationRecommendations",
    }
    return required.issubset(commands)


def _continuity_size(root: Path) -> int:
    storage = root / ".ai-dev-os"
    if not storage.exists():
        return 0
    return sum(path.stat().st_size for path in storage.rglob("*.json") if path.is_file())


def _docs_fresh(root: Path) -> bool:
    docs = root / "docs"
    if not docs.exists():
        return False
    text = "\n".join(_read_text(path) for path in docs.rglob("*.md")).lower()
    return "ai_dev_os" in text or "rollout" in text or "governance" in text


def _level(categories: list[str], blockers: list[str]) -> str:
    if blockers:
        return "BLOCKED"
    if len(categories) >= 5:
        return "HIGH"
    if len(categories) >= 2:
        return "MEDIUM"
    if categories:
        return "LOW"
    return "LOW"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}
