from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepositoryRef:
    name: str
    path: Path


def discover_repositories(
    workspace: str | Path = ".", *, max_repositories: int = 8
) -> tuple[RepositoryRef, ...]:
    root = Path(workspace).resolve()
    candidates: list[Path] = []
    if (root / ".git").exists():
        candidates.append(root)
    for child in sorted(
        root.iterdir() if root.exists() else (), key=lambda item: item.name.lower()
    ):
        if child.is_dir() and (child / ".git").exists() and child not in candidates:
            candidates.append(child)
    return tuple(RepositoryRef(path.name, path) for path in candidates[:max_repositories])


def read_text_if_exists(path: Path, *, max_chars: int = 12_000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]


def has_any_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)
