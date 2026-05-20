from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RollbackRehearsalFrame:
    rollback_ready: bool
    rollback_risk: str
    orphaned_state_risk: str
    bounded_rollback_confirmed: bool
    dry_run_only: bool = True
    summary_only: bool = True
    mutation_performed: bool = False


class RollbackRehearsalPolicy:
    def evaluate(
        self, consumer_repo: str | Path, *, platform_repo: str | Path = "."
    ) -> RollbackRehearsalFrame:
        consumer = Path(consumer_repo)
        platform = Path(platform_repo)
        gitignore = _read_text(consumer / ".gitignore")
        docs = _read_docs(platform)
        extension_uninstall = "uninstall" in docs or "vsix" in docs
        cleanup_path = ".ai-dev-os/" in gitignore or ".ai-dev-os cleanup" in docs
        persistence_reset = "persistence reset" in docs or "reset local session state" in docs
        lifecycle_reset = "session lifecycle reset" in docs or "rollover" in docs
        governance_removal = "governance runtime removal" in docs or "rollback procedure" in docs
        readiness = all(
            (
                extension_uninstall,
                cleanup_path,
                persistence_reset,
                lifecycle_reset,
                governance_removal,
            )
        )
        orphaned = (
            "LOW" if cleanup_path and persistence_reset else "MEDIUM" if cleanup_path else "HIGH"
        )
        risk = "LOW" if readiness else "MEDIUM" if orphaned != "HIGH" else "HIGH"
        return RollbackRehearsalFrame(
            rollback_ready=readiness,
            rollback_risk=risk,
            orphaned_state_risk=orphaned,
            bounded_rollback_confirmed=readiness and orphaned == "LOW",
        )


def _read_docs(root: Path) -> str:
    docs = root / "docs"
    if not docs.exists():
        return ""
    return "\n".join(path.read_text(encoding="utf-8") for path in docs.rglob("*.md")).lower()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""
