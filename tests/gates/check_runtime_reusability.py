from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_PATHS = (
    "core/contracts.py",
    "core/shared_runtime.py",
    "governance/model_tiers.py",
    "governance/budget_runtime.py",
    "governance/gpt55_guard.py",
    "governance/council_runtime.py",
    "retrieval/build_manifest.py",
    "retrieval/select_context.py",
    "retrieval/prune_context.py",
    "checkpoints/checkpoint.py",
    "telemetry/runtime.py",
    "integrations/litellm/bridge.py",
    "integrations/langfuse/tracing.py",
    "integrations/aider/patch_workflow.py",
    "integrations/continue_local/indexing.py",
    "integrations/dvc/artifacts.py",
    "bootstrap/init_project.py",
)
FORBIDDEN_IMPORT_ROOTS = {"orchestrator", "Assets", "Unity", "minecraft_bridge", "runtime"}


def iter_python_files() -> list[Path]:
    return [
        path
        for base in (
            "core",
            "governance",
            "retrieval",
            "checkpoints",
            "telemetry",
            "integrations",
            "bootstrap",
        )
        for path in (ROOT / base).rglob("*.py")
    ]


def main() -> int:
    failures: list[str] = []
    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).exists():
            failures.append(f"{relative_path}: missing required reusable runtime file")

    for path in iter_python_files():
        relative_path = path.relative_to(ROOT).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0]]
            else:
                continue
            for name in names:
                if name in FORBIDDEN_IMPORT_ROOTS:
                    failures.append(f"{relative_path}: forbidden project import {name}")

    if failures:
        print("Runtime reusability gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Runtime reusability gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
