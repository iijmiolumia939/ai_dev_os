from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
HARDCODED_PATTERNS = (re.compile(r"[A-Za-z]:\\(?:Projects|work|repo|src)\\", re.I),)


def iter_files() -> list[Path]:
    return [
        path
        for path in ROOT_DIR.rglob("*")
        if ".git" not in path.parts
        and path.suffix.lower() in {".py", ".md", ".json", ".yml", ".yaml", ".toml"}
    ]


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        relative_path = path.relative_to(ROOT_DIR).as_posix()
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
        ):
            if any(pattern.search(line) for pattern in HARDCODED_PATTERNS):
                failures.append(f"{relative_path}:{line_number}: hardcoded project dependency")

    if failures:
        print("Hardcoded project dependency gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Hardcoded project dependency gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
