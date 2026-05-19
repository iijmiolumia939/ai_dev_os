from __future__ import annotations

from pathlib import Path


def test_vscode_extension_compile_step_is_in_ci() -> None:
    workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "VSCode extension compile check" in workflow
    assert "npm ci" in workflow
    assert "npm run compile" in workflow


def test_vscode_extension_docs_exist() -> None:
    for path in (
        Path("docs/session-boundary-enforcement.md"),
        Path("docs/vscode-rollover-extension.md"),
        Path("docs/stale-session-governance.md"),
    ):
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "FR-SESSIONBOUNDARY" in text
        assert "TC-SESSIONBOUNDARY" in text
        assert "UI automation" in text or "UI 自動操作" in text
