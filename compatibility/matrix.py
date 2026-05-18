from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompatibilityEntry:
    os_version: str
    compatible_adapters: tuple[str, ...]
    compatible_extensions: tuple[str, ...]
    python_versions: tuple[str, ...]


@dataclass(frozen=True)
class CompatibilityMatrix:
    entries: tuple[CompatibilityEntry, ...]

    def entry_for(self, os_version: str) -> CompatibilityEntry | None:
        major_minor = ".".join(os_version.split(".")[:2])
        for entry in self.entries:
            if entry.os_version.startswith(f"{major_minor}."):
                return entry
        return None

    def is_adapter_compatible(self, os_version: str, adapter: str) -> bool:
        entry = self.entry_for(os_version)
        return bool(entry and adapter in entry.compatible_adapters)

    def is_extension_compatible(self, os_version: str, extension: str) -> bool:
        entry = self.entry_for(os_version)
        return bool(entry and extension in entry.compatible_extensions)


def default_matrix() -> CompatibilityMatrix:
    return CompatibilityMatrix(
        entries=(
            CompatibilityEntry(
                os_version="0.1.x",
                compatible_adapters=("aituber", "cat_simulator", "scientific", "unity"),
                compatible_extensions=("scientific", "embodiment", "unity", "mujoco"),
                python_versions=("3.11", "3.12"),
            ),
        )
    )
