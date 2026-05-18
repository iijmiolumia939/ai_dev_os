from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdapterContract:
    name: str
    version: str
    supported_os: str
    required_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class ExtensionContract:
    name: str
    version: str
    supported_os: str
    optional_dependencies: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConsumerRuntimeContract:
    project_name: str
    adapter: AdapterContract
    extensions: tuple[ExtensionContract, ...]
    governance_level: str

    def required_optional_dependencies(self) -> tuple[str, ...]:
        dependencies: list[str] = []
        for extension in self.extensions:
            dependencies.extend(extension.optional_dependencies)
        return tuple(dict.fromkeys(dependencies))
