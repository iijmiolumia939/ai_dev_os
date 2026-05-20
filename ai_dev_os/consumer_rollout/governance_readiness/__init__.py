from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GovernanceReadinessFrame:
    governance_ready: bool
    missing_governance_components: tuple[str, ...]
    rollout_pressure: str
    governance_training_required: bool
    summary_only: bool = True
    automatic_governance_enforcement: bool = False


class GovernanceReadinessPolicy:
    def evaluate(
        self,
        consumer_repo: str | Path,
        *,
        platform_repo: str | Path = ".",
    ) -> GovernanceReadinessFrame:
        consumer = Path(consumer_repo)
        platform = Path(platform_repo)
        package = _read_json(platform / "extensions" / "ai-dev-os-vscode" / "package.json")
        commands = {
            item.get("command", "") for item in package.get("contributes", {}).get("commands", [])
        }
        docs = _read_docs(consumer)
        session_state = consumer / ".ai-dev-os" / "session-boundary.json"
        continuity = consumer / ".ai-dev-os" / "continuity-index.json"
        components = {
            "session_rollover_workflow": session_state.exists()
            or "rollover" in docs
            or "session boundary" in docs,
            "continuity_export_workflow": continuity.exists()
            or "continuity" in docs
            or "aiDevOs.copyContinuityBundle" in commands,
            "runtime_audit_workflow": "runtime_audit" in docs
            or "runtime audit" in docs
            or "ai_dev_os" in _read_text(consumer / "pyproject.toml"),
            "governance_dashboard_workflow": "aiDevOs.showGovernanceDashboard" in commands,
            "compact_context_workflow": "compact" in docs
            or "aiDevOs.compactCurrentSession" in commands,
            "stale_session_workflow": "stale" in docs
            or "aiDevOs.showStaleSessionWarning" in commands,
        }
        missing = tuple(name for name, present in components.items() if not present)
        pressure = "LOW" if not missing else "MEDIUM" if len(missing) <= 2 else "HIGH"
        return GovernanceReadinessFrame(
            governance_ready=len(missing) == 0,
            missing_governance_components=missing,
            rollout_pressure=pressure,
            governance_training_required=bool(missing),
        )


def _read_docs(root: Path) -> str:
    docs = root / "docs"
    if not docs.exists():
        return ""
    return "\n".join(path.read_text(encoding="utf-8") for path in docs.rglob("*.md")).lower()


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
