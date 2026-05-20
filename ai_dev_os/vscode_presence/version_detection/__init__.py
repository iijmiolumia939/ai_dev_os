from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXTENSION_ID = "iijmiolumia939.ai-dev-os-vscode"


@dataclass(frozen=True)
class ExtensionVersionFrame:
    repo_version: str
    installed_version: str
    version_match: bool
    stale_install: bool
    missing_reinstall: bool
    duplicate_install: bool
    stale_extension_detected: bool
    reinstall_recommended: bool
    duplicate_install_detected: bool
    installed_paths: tuple[str, ...]
    summary_only: bool = True


def detect_extension_version(
    workspace_root: Path | str = ".",
    *,
    installed_extensions_dir: Path | str | None = None,
    extension_id: str = EXTENSION_ID,
) -> ExtensionVersionFrame:
    root = Path(workspace_root)
    repo_manifest = _read_json(root / "extensions" / "ai-dev-os-vscode" / "package.json")
    repo_version = str(repo_manifest.get("version", ""))
    installed_dir = (
        Path(installed_extensions_dir) if installed_extensions_dir else _default_extensions_dir()
    )
    installed_manifests = _installed_manifests(installed_dir, extension_id)
    installed_versions = tuple(
        str(manifest.get("version", "")) for _, manifest in installed_manifests if manifest
    )
    installed_version = installed_versions[-1] if installed_versions else ""
    duplicate = len(installed_manifests) > 1
    version_match = bool(repo_version and installed_version and repo_version == installed_version)
    stale = bool(repo_version and installed_version and repo_version != installed_version)
    missing = bool(repo_version and not installed_version)
    installed_paths = tuple(str(path) for path, _ in installed_manifests)
    return ExtensionVersionFrame(
        repo_version=repo_version,
        installed_version=installed_version,
        version_match=version_match,
        stale_install=stale,
        missing_reinstall=missing,
        duplicate_install=duplicate,
        stale_extension_detected=stale or missing or duplicate,
        reinstall_recommended=stale or missing or duplicate,
        duplicate_install_detected=duplicate,
        installed_paths=installed_paths,
    )


def _default_extensions_dir() -> Path:
    home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or ".")
    return home / ".vscode" / "extensions"


def _installed_manifests(
    installed_extensions_dir: Path,
    extension_id: str,
) -> tuple[tuple[Path, dict[str, Any]], ...]:
    if not installed_extensions_dir.exists():
        return ()
    candidates = sorted(
        path for path in installed_extensions_dir.iterdir() if path.name.startswith(extension_id)
    )
    return tuple((path, _read_json(path / "package.json")) for path in candidates)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}
