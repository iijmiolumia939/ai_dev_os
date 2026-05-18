from __future__ import annotations

import argparse
import json
from pathlib import Path

BOOTSTRAP_WORKFLOW = "\n".join(
    (
        "name: Cost Governance",
        "on: [pull_request]",
        "jobs:",
        "  placeholder:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - run: echo ai-dev-os governance",
        "",
    )
)


def create_project(
    output_dir: Path,
    *,
    project_type: str,
    name: str,
    runtime_type: str,
    scientific_mode: bool,
    embodiment_mode: bool,
) -> Path:
    project_dir = output_dir / name
    for relative in (
        "prompts",
        "governance",
        "retrieval",
        "telemetry",
        "integrations",
        "extensions",
        ".github/workflows",
    ):
        (project_dir / relative).mkdir(parents=True, exist_ok=True)
    profile = {
        "project_name": name,
        "project_type": project_type,
        "runtime_type": runtime_type,
        "scientific_mode": scientific_mode,
        "embodiment_mode": embodiment_mode,
        "governance_level": "cost-aware-runtime-enforced",
    }
    (project_dir / "ai-dev-os-profile.json").write_text(
        json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (project_dir / "prompts" / "README.md").write_text(
        "# Project Prompts\n\nGenerated from AI Development OS templates.\n", encoding="utf-8"
    )
    (project_dir / "governance" / "README.md").write_text(
        "# Governance\n\nRuntime-enforced budget, routing, and council policies.\n",
        encoding="utf-8",
    )
    (project_dir / "retrieval" / "README.md").write_text(
        "# Retrieval\n\nRetrieval-first context bundle configuration.\n", encoding="utf-8"
    )
    (project_dir / "telemetry" / "README.md").write_text(
        "# Telemetry\n\nProject-tagged usage and cost reporting.\n", encoding="utf-8"
    )
    (project_dir / "integrations" / "README.md").write_text(
        "# Integrations\n\nOptional provider integrations with graceful degradation.\n",
        encoding="utf-8",
    )
    if scientific_mode:
        (project_dir / "extensions" / "scientific.json").write_text(
            json.dumps(
                {"enabled": True, "requires": ["scientific", "retrieval", "governance"]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    (project_dir / ".github" / "workflows" / "cost-governance.yml").write_text(
        BOOTSTRAP_WORKFLOW,
        encoding="utf-8",
    )
    return project_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, dest="project_type")
    parser.add_argument("--name", required=True)
    parser.add_argument("--runtime-type", default="autonomous")
    parser.add_argument("--scientific-mode", action="store_true")
    parser.add_argument("--embodiment-mode", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path("generated-projects"))
    args = parser.parse_args()
    project_dir = create_project(
        args.output_dir,
        project_type=args.project_type,
        name=args.name,
        runtime_type=args.runtime_type,
        scientific_mode=args.scientific_mode,
        embodiment_mode=args.embodiment_mode,
    )
    print(project_dir.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
