from __future__ import annotations

from pathlib import Path

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_runtime_audit_reports_session_lifecycle_governance() -> None:
    report = run_runtime_enforcement_audit()

    assert report.session_lifecycle.session_lifecycle_active is True
    assert report.session_lifecycle.rollover_recommendation is True
    assert report.session_lifecycle.stale_context_ratio > 0.5
    assert report.session_lifecycle.continuity_bundle_generated is True
    assert report.session_lifecycle.architecture_isolation_recommendation is True
    assert report.session_lifecycle.compact_bundle_required is True
    assert report.session_lifecycle.summary_only_continuity is True
    assert report.session_lifecycle.recommended_session_action == "isolate_architecture_session"
    assert report.session_lifecycle.estimated_avoided_tokens > 0


def test_session_lifecycle_runtime_has_no_network_dependency() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "session_lifecycle").rglob("*.py"))
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)


def test_no_full_repository_continuity_bundle_terms_in_runtime_output() -> None:
    report = run_runtime_enforcement_audit()
    serialized = str(report.session_lifecycle).lower()

    assert "full_repository_tree" not in serialized
    assert "full_sprint_history" not in serialized
    assert "giant_markdown" not in serialized
