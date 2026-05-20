from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CompatibilityProjectionFrame:
    compatibility_level: str
    incompatible_components: tuple[str, ...]
    python_version_supported: bool
    vscode_compatibility: bool
    extension_compatibility: bool
    persistence_compatibility: bool
    governance_runtime_expectations: bool
    bounded_retention_support: bool
    local_only_storage_support: bool
    bounded_compatibility_confirmed: bool
    summary_only: bool = True


class CompatibilityProjectionPolicy:
    def evaluate(
        self,
        consumer_repo: str | Path,
        *,
        platform_repo: str | Path = ".",
    ) -> CompatibilityProjectionFrame:
        consumer = Path(consumer_repo)
        platform = Path(platform_repo)
        package = _read_json(platform / "extensions" / "ai-dev-os-vscode" / "package.json")
        pyproject = _read_text(consumer / "pyproject.toml")
        gitignore = _read_text(consumer / ".gitignore")
        docs_text = _read_docs(consumer)
        python_supported = sys.version_info >= (3, 11) and _consumer_mentions_python(pyproject)
        vscode_ok = str(package.get("engines", {}).get("vscode", "")).startswith("^1.90")
        extension_ok = bool(package.get("main") == "./out/extension.js")
        persistence_ok = ".ai-dev-os/" in gitignore
        governance_ok = "governance" in docs_text or (consumer / "AGENTS.md").exists()
        retention_ok = "bounded" in docs_text or ".ai-dev-os/" in gitignore
        local_only = ".ai-dev-os/" in gitignore and ".env" in gitignore
        incompatible = tuple(
            name
            for name, passed in (
                ("python_version", python_supported),
                ("vscode", vscode_ok),
                ("extension", extension_ok),
                ("persistence", persistence_ok),
                ("governance_runtime", governance_ok),
                ("bounded_retention", retention_ok),
                ("local_only_storage", local_only),
            )
            if not passed
        )
        level = "FULL" if not incompatible else "PARTIAL" if len(incompatible) <= 2 else "LIMITED"
        return CompatibilityProjectionFrame(
            compatibility_level=level,
            incompatible_components=incompatible,
            python_version_supported=python_supported,
            vscode_compatibility=vscode_ok,
            extension_compatibility=extension_ok,
            persistence_compatibility=persistence_ok,
            governance_runtime_expectations=governance_ok,
            bounded_retention_support=retention_ok,
            local_only_storage_support=local_only,
            bounded_compatibility_confirmed=level in {"FULL", "PARTIAL"} and local_only,
        )


def _consumer_mentions_python(pyproject: str) -> bool:
    return "requires-python" in pyproject or sys.version_info >= (3, 11)


def _read_docs(root: Path) -> str:
    docs = root / "docs"
    if not docs.exists():
        return ""
    return "\n".join(path.read_text(encoding="utf-8") for path in docs.rglob("*.md")).lower()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}
