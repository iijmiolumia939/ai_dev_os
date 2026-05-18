from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHARED_DIRS = (
    "core",
    "governance",
    "retrieval",
    "telemetry",
    "integrations",
    "checkpoints",
    "bootstrap",
)
CONSUMER_NAMES = ("AITuber", "CatSimulator", "cat-simulator")


def iter_shared_files() -> list[Path]:
    files: list[Path] = []
    for directory in SHARED_DIRS:
        base = ROOT / directory
        if base.exists():
            files.extend(
                path
                for path in base.rglob("*")
                if path.suffix.lower() in {".py", ".md", ".json", ".yml", ".yaml"}
            )
    return files


def main() -> int:
    failures: list[str] = []
    patterns = [re.compile(rf"\b{re.escape(name)}\b", re.I) for name in CONSUMER_NAMES]
    for path in iter_shared_files():
        relative_path = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
        ):
            if any(pattern.search(line) for pattern in patterns):
                failures.append(f"{relative_path}:{line_number}: consumer contamination")

    if failures:
        print("Consumer runtime isolation gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Consumer runtime isolation gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
