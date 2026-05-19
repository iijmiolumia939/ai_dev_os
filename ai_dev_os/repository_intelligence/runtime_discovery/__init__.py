from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimeDiscoveryFrame:
    runtime_packages: tuple[str, ...]
    test_packages: tuple[str, ...]
    governance_runtimes: tuple[str, ...]
    adapter_runtimes: tuple[str, ...]
    renderer_runtimes: tuple[str, ...]
    experimental_runtimes: tuple[str, ...]
    stale_runtimes: tuple[str, ...]
    runtime_relationship_summary: tuple[str, ...]


class RuntimeDiscoveryPolicy:
    def discover(self, repo_path: str | Path = ".") -> RuntimeDiscoveryFrame:
        root = Path(repo_path).resolve()
        runtime_packages = self._packages(root / "ai_dev_os")
        test_packages = self._packages(root / "tests")
        governance = tuple(path for path in runtime_packages if "governance" in path)
        adapters = tuple(
            path for path in runtime_packages if "adapter" in path or "provider" in path
        )
        renderers = tuple(
            path for path in runtime_packages if "renderer" in path or "unity" in path
        )
        experimental = tuple(path for path in runtime_packages if "experimental" in path)
        stale = tuple(path for path in runtime_packages if "legacy" in path or "stale" in path)
        summary = (
            f"runtime_packages={len(runtime_packages)}",
            f"test_packages={len(test_packages)}",
            f"governance={len(governance)}",
            f"adapters={len(adapters)}",
            f"stale={len(stale)}",
        )
        return RuntimeDiscoveryFrame(
            runtime_packages=runtime_packages,
            test_packages=test_packages,
            governance_runtimes=governance,
            adapter_runtimes=adapters,
            renderer_runtimes=renderers,
            experimental_runtimes=experimental,
            stale_runtimes=stale,
            runtime_relationship_summary=summary,
        )

    def _packages(self, root: Path) -> tuple[str, ...]:
        if not root.exists():
            return ()
        packages = []
        for path in root.rglob("__init__.py"):
            relative = path.parent.relative_to(root.parent).as_posix()
            packages.append(relative)
        for path in root.rglob("test_*.py"):
            relative = path.parent.relative_to(root.parent).as_posix()
            packages.append(relative)
        return tuple(sorted(packages))
