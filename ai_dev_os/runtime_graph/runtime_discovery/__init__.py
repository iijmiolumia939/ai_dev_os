from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

RuntimeCategory = str

_CATEGORY_MARKERS: tuple[tuple[RuntimeCategory, tuple[str, ...]], ...] = (
    ("governance", ("governance", "budget", "copilot_usage")),
    ("retrieval", ("retrieval", "context_subset")),
    ("persistence", ("persistence", "checkpoint", "schema")),
    ("provider", ("provider", "telemetry")),
    ("orchestration", ("session_orchestrator", "session_lifecycle", "session_boundary")),
    ("vscode", ("vscode", "extension")),
    ("cognition", ("repository_intelligence", "workspace_snapshot", "workspace_persistence")),
    ("adapters", ("adapter", "integration")),
)


@dataclass(frozen=True)
class RuntimeRecord:
    runtime_name: str
    runtime_category: str
    runtime_boundary: str
    runtime_contract_count: int
    runtime_dependency_count: int


@dataclass(frozen=True)
class RuntimeDiscoveryFrame:
    runtimes: tuple[RuntimeRecord, ...]
    runtime_names: tuple[str, ...]
    runtime_categories: tuple[str, ...]
    category_counts: dict[str, int]
    runtime_count: int
    deterministic_discovery: bool
    summary_only: bool
    full_source_indexing_used: bool
    ast_replay_used: bool
    dynamic_tracing_used: bool


class RuntimeDiscoveryPolicy:
    def discover(self, repo_path: str | Path = ".") -> RuntimeDiscoveryFrame:
        root = Path(repo_path).resolve()
        records = tuple(self._discover_records(root))
        category_counts = {category: 0 for category, _ in _CATEGORY_MARKERS}
        category_counts["other"] = 0
        for record in records:
            category_counts[record.runtime_category] = (
                category_counts.get(record.runtime_category, 0) + 1
            )
        return RuntimeDiscoveryFrame(
            runtimes=records,
            runtime_names=tuple(record.runtime_name for record in records),
            runtime_categories=tuple(sorted(set(record.runtime_category for record in records))),
            category_counts={key: value for key, value in category_counts.items() if value > 0},
            runtime_count=len(records),
            deterministic_discovery=True,
            summary_only=True,
            full_source_indexing_used=False,
            ast_replay_used=False,
            dynamic_tracing_used=False,
        )

    def _discover_records(self, root: Path) -> list[RuntimeRecord]:
        package_root = root / "ai_dev_os"
        if not package_root.exists():
            return []
        records: list[RuntimeRecord] = []
        for init_file in sorted(package_root.rglob("__init__.py")):
            package_dir = init_file.parent
            relative = package_dir.relative_to(package_root).as_posix()
            if not relative or "/" in relative:
                continue
            records.append(self._record_for(relative, package_dir))
        return records

    def _record_for(self, runtime_name: str, package_dir: Path) -> RuntimeRecord:
        category = _category_for(runtime_name)
        child_packages = tuple(path for path in package_dir.iterdir() if path.is_dir())
        py_modules = tuple(path for path in package_dir.glob("*.py") if path.name != "__init__.py")
        contract_count = min(12, len(child_packages) + len(py_modules))
        dependency_count = _dependency_hint(category)
        boundary = f"{category}:summary-only:{runtime_name}"
        return RuntimeRecord(
            runtime_name=runtime_name,
            runtime_category=category,
            runtime_boundary=boundary,
            runtime_contract_count=contract_count,
            runtime_dependency_count=dependency_count,
        )


def _category_for(runtime_name: str) -> str:
    lowered = runtime_name.lower()
    for category, markers in _CATEGORY_MARKERS:
        if any(marker in lowered for marker in markers):
            return category
    return "other"


def _dependency_hint(category: str) -> int:
    return {
        "governance": 4,
        "retrieval": 3,
        "persistence": 3,
        "provider": 2,
        "orchestration": 4,
        "vscode": 2,
        "cognition": 3,
        "adapters": 2,
    }.get(category, 1)
