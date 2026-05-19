from __future__ import annotations

from pathlib import Path

from ai_dev_os.copilot_usage.atomic_prompting import AtomicPromptPolicy
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_runtime_audit_reports_copilot_usage_optimization() -> None:
    report = run_runtime_enforcement_audit()

    assert report.copilot_usage.atomic_prompting_active is True
    assert report.copilot_usage.context_diet_active is True
    assert report.copilot_usage.skill_compaction_active is True
    assert report.copilot_usage.agent_mode_budget_active is True
    assert report.copilot_usage.cache_aware_session_policy_active is True
    assert report.copilot_usage.inline_first_recommendation_active is True
    assert report.copilot_usage.usage_dashboard_review_workflow_active is True
    assert report.copilot_usage.estimated_avoided_tokens > 0


def test_copilot_usage_outputs_are_deterministic() -> None:
    prompt = "Please review everything and implement architecture changes."
    first = AtomicPromptPolicy().evaluate(prompt)
    second = AtomicPromptPolicy().evaluate(prompt)

    assert first == second


def test_copilot_usage_has_no_network_dependency() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "copilot_usage").rglob("*.py"))
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)
