from __future__ import annotations

from pathlib import Path


def test_extension_layers_are_present() -> None:
    root = Path(__file__).resolve().parents[2]

    assert (root / "extensions" / "scientific" / "README.md").exists()
    assert (root / "extensions" / "embodiment" / "README.md").exists()
    assert (root / "extensions" / "unity" / "README.md").exists()
    assert (root / "extensions" / "mujoco" / "README.md").exists()
