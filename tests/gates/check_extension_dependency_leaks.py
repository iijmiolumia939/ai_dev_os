from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTENSIONS = ROOT / "extensions"
FORBIDDEN_IMPORTS = {"adapters", "orchestrator", "Assets", "runtime"}


def main() -> int:
    failures: list[str] = []
    for path in EXTENSIONS.rglob("*.py") if EXTENSIONS.exists() else []:
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
                if name in FORBIDDEN_IMPORTS:
                    failures.append(f"{relative_path}: extension dependency leak {name}")

    if failures:
        print("Extension dependency leak gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Extension dependency leak gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
