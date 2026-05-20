from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ai_dev_os.release_readiness import ConsumerRolloutPolicy

ROOT = Path(".")


def test_consumer_rollout_validation() -> None:
    frame = ConsumerRolloutPolicy().evaluate(ROOT)

    assert frame.consumer_rollout_active is True
    assert frame.supported_consumers == (
        "AITuber",
        "cat simulator",
        "standalone governance repos",
        "experimental repos",
    )
    assert frame.install_flow_documented is True
    assert frame.vscode_extension_setup_documented is True
    assert frame.session_lifecycle_setup_documented is True
    assert frame.workspace_persistence_setup_documented is True
    assert frame.retrieval_scaling_integration_documented is True
    assert frame.governance_runtime_integration_documented is True
    assert frame.rollback_procedure_documented is True
    assert frame.migration_checklist_documented is True
    assert frame.local_only_persistence_rules_documented is True
    assert frame.human_confirmed_rollout is True


def test_compatibility_matrix_validation() -> None:
    text = (ROOT / "docs" / "releases" / "compatibility-matrix.md").read_text(encoding="utf-8")

    assert "Python 3.11" in text
    assert "Python 3.12" in text
    assert "VSCode `^1.90.0`" in text
    assert "Windows" in text
    assert "macOS" in text
    assert "Linux" in text
    assert "Optional Dependency Boundaries" in text
    assert "Consumer Repository Expectations" in text
    assert "Bounded Persistence Requirements" in text


def test_session_lifecycle_release_guide_validation() -> None:
    text = (ROOT / "docs" / "session-lifecycle" / "index.md").read_text(encoding="utf-8")

    assert "Rollover Workflow" in text
    assert "Continuity Bundle Workflow" in text
    assert "Stale Session Workflow" in text
    assert "Compact Context Workflow" in text
    assert "Governance Incident Workflow" in text
    assert "Bounded Persistence Workflow" in text
    assert "human confirms" in text


def test_vscode_extension_release_docs_validation() -> None:
    install = (ROOT / "docs" / "vscode-extension" / "install.md").read_text(encoding="utf-8")
    handoff = (ROOT / "docs" / "vscode-extension" / "session-handoff.md").read_text(
        encoding="utf-8"
    )
    dashboard = (ROOT / "docs" / "vscode-extension" / "governance-dashboard.md").read_text(
        encoding="utf-8"
    )

    assert "VSIX build verification" in install
    assert "Extension compile verification" in install
    assert "hidden network dependency" in install
    assert "hidden telemetry" in install
    assert "human-confirmed" in handoff
    assert "does not automate chat UI" in handoff
    assert "summary-only" in dashboard
    assert "not a remote reporting channel" in dashboard


def test_consumer_rollout_cli_json_and_copy_ready() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "consumer-rollout-check", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["consumer_rollout_active"] is True
    assert data["human_confirmed_rollout"] is True
    assert "AITuber" in data["supported_consumers"]

    copy_ready = subprocess.run(
        [sys.executable, "-m", "ai_dev_os.cli", "governance-freeze-status", "--copy-ready"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "governance_freeze_active: True" in copy_ready.stdout


def test_local_only_persistence_and_no_hidden_automation_docs() -> None:
    docs = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").rglob("*.md"))
    lowered = docs.lower()

    assert "local-only persistence rules" in lowered
    assert "automatic consumer mutation" in lowered
    assert "hidden migration" in lowered
    assert "rollback-safe" in lowered
    assert "human-confirmed rollout" in lowered
