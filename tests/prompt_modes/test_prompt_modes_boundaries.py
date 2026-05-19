from __future__ import annotations

from pathlib import Path


def test_no_unrestricted_escalation_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "prompt_modes").rglob("*.py"))
    forbidden = (
        "unrestricted_reasoning",
        "always_escalate",
        "full_historical_continuity_allowed",
        "force_council_for_patch",
    )

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(marker not in text for marker in forbidden)


def test_no_network_dependency() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "prompt_modes").rglob("*.py"))
    forbidden = ("openai", "litellm", "langfuse", "requests", "httpx", "urllib")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(f"import {name}" not in text for name in forbidden)
        assert all(f"from {name}" not in text for name in forbidden)


def test_bounded_reasoning_continuity() -> None:
    root = Path(__file__).resolve().parents[2]
    files = list((root / "ai_dev_os" / "prompt_modes").rglob("*.py"))

    for path in files:
        text = path.read_text(encoding="utf-8")
        assert "full_historical_continuity" not in text or "excluded" in text
        assert "bounded_implementation" in text or path.name == "__init__.py"
