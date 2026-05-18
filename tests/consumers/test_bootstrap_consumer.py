from __future__ import annotations

import json

from bootstrap import create_project


def test_scientific_bootstrap_generates_consumer_surface(tmp_path) -> None:
    project_dir = create_project(
        tmp_path,
        project_type="scientific",
        name="cat-simulator",
        runtime_type="scientific",
        scientific_mode=True,
        embodiment_mode=False,
    )
    profile = json.loads((project_dir / "ai-dev-os-profile.json").read_text(encoding="utf-8"))

    assert profile["project_type"] == "scientific"
    assert (project_dir / "governance" / "README.md").exists()
    assert (project_dir / "retrieval" / "README.md").exists()
    assert (project_dir / "telemetry" / "README.md").exists()
    assert (project_dir / "integrations" / "README.md").exists()
    assert (project_dir / "extensions" / "scientific.json").exists()
    assert (project_dir / ".github" / "workflows" / "cost-governance.yml").exists()
