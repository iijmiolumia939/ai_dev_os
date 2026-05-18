from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMON_DIRS = (
    "core",
    "governance",
    "retrieval",
    "checkpoints",
    "telemetry",
    "integrations",
    "prompts",
    "templates",
    "bootstrap",
)
LEAK_PATTERNS = (
    re.compile(r"\bAITuber\b", re.I),
    re.compile(r"\bcat[-_ ]?simulator\b", re.I),
    re.compile(r"\bLive2D\b", re.I),
    re.compile(r"\bMuJoCo\b", re.I),
    re.compile(r"\bProjectSettings\b", re.I),
)


def iter_common_files() -> list[Path]:
    files: list[Path] = []
    for relative_dir in COMMON_DIRS:
        base = ROOT / relative_dir
        if not base.exists():
            continue
        files.extend(
            path
            for path in base.rglob("*")
            if path.suffix.lower() in {".py", ".md", ".json", ".yml", ".yaml"}
        )
    return files


def main() -> int:
    failures: list[str] = []
    for path in iter_common_files():
        relative_path = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
        ):
            if any(pattern.search(line) for pattern in LEAK_PATTERNS):
                failures.append(f"{relative_path}:{line_number}: project boundary leak")

    if failures:
        print("Project boundary leak gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Project boundary leak gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
