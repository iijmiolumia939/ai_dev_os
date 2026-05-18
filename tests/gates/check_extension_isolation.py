from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTENSIONS = ROOT / "extensions"
FORBIDDEN_EXTENSION_COUPLING = (
    re.compile(r"from\s+adapters\b"),
    re.compile(r"import\s+adapters\b"),
    re.compile(r"from\s+core\b"),
    re.compile(r"import\s+core\b"),
)


def main() -> int:
    failures: list[str] = []
    for path in EXTENSIONS.rglob("*.py") if EXTENSIONS.exists() else []:
        relative_path = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(text) for pattern in FORBIDDEN_EXTENSION_COUPLING):
            failures.append(f"{relative_path}: extension coupling violation")

    if failures:
        print("Extension isolation gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Extension isolation gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
