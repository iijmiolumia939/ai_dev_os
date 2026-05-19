from __future__ import annotations

from pathlib import Path

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_runtime_audit_reports_provider_simulation() -> None:
    report = run_runtime_enforcement_audit()

    assert report.provider_simulation.provider_simulation_active is True
    assert report.provider_simulation.mock_provider_fallback_verified is True
    assert report.provider_simulation.fallback_frequency == 1
    assert report.provider_simulation.no_real_provider_call is True
    assert report.provider_simulation.token_burn_avoided > 0
    assert report.retrieval_scaling.provider_token_estimate > 0
    assert report.retrieval_scaling.provider_cost_estimate > 0
    assert report.retrieval_scaling.token_burn_avoided > 0


def test_no_real_provider_sdk_calls_or_generated_telemetry_artifacts() -> None:
    root = Path(__file__).resolve().parents[2]
    provider_files = list((root / "ai_dev_os" / "providers").rglob("*.py"))
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in provider_files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)

    artifact_patterns = ("*provider_telemetry*.json", "*cost_telemetry*.json", "*.jsonl")
    artifacts = [path for pattern in artifact_patterns for path in root.rglob(pattern)]
    assert artifacts == []
