from __future__ import annotations

from pathlib import Path


def build_manifest(root: Path, include_dirs: tuple[str, ...]) -> dict[str, object]:
    entries = []
    for relative_dir in include_dirs:
        base = root / relative_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() in {".md", ".json", ".yml", ".yaml", ".py"}:
                entries.append(
                    {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size}
                )
    return {"version": 1, "entries": entries}
