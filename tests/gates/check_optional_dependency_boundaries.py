from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPTIONAL_IMPORTS = {"litellm", "langfuse", "dvc", "aider", "aider_chat"}
ALLOWED_PREFIXES = ("integrations/", "tests/", "docs/")


def iter_python_files() -> list[Path]:
    return [path for path in ROOT.rglob("*.py") if ".git" not in path.parts]


def main() -> int:
    failures: list[str] = []
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
                if name in OPTIONAL_IMPORTS and not relative_path.startswith(ALLOWED_PREFIXES):
                    failures.append(f"{relative_path}: optional dependency hard coupling {name}")

    if failures:
        print("Optional dependency boundary gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Optional dependency boundary gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
