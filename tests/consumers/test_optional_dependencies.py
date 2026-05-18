from __future__ import annotations

import tomllib
from pathlib import Path


def test_optional_extras_are_declared_for_consumer_modes() -> None:
    pyproject = tomllib.loads((Path(__file__).resolve().parents[2] / "pyproject.toml").read_text())
    extras = pyproject["project"]["optional-dependencies"]

    assert "scientific" in extras
    assert "telemetry" in extras
    assert "routing" in extras
    assert "coding" in extras
    assert "full" in extras
    assert any(dependency.startswith("dvc") for dependency in extras["scientific"])
    assert any(dependency.startswith("langfuse") for dependency in extras["telemetry"])
    assert any(dependency.startswith("litellm") for dependency in extras["routing"])
