from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from compatibility.matrix import CompatibilityMatrix
from consumer_contracts import ConsumerRuntimeContract


class ChangeKind(StrEnum):
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    PATCH = "PATCH"


@dataclass(frozen=True)
class CompatibilityReport:
    compatible: bool
    os_version: str
    adapter: str
    extensions: tuple[str, ...]
    warnings: tuple[str, ...]


def classify_change(*, breaking_runtime: bool, new_capability: bool) -> ChangeKind:
    if breaking_runtime:
        return ChangeKind.MAJOR
    if new_capability:
        return ChangeKind.MINOR
    return ChangeKind.PATCH


def validate_compatibility(
    contract: ConsumerRuntimeContract,
    *,
    os_version: str,
    matrix: CompatibilityMatrix,
) -> CompatibilityReport:
    warnings: list[str] = []
    adapter_ok = matrix.is_adapter_compatible(os_version, contract.adapter.name)
    if not adapter_ok:
        warnings.append("ADAPTER_INCOMPATIBLE")
    extension_names = tuple(extension.name for extension in contract.extensions)
    for extension_name in extension_names:
        if not matrix.is_extension_compatible(os_version, extension_name):
            warnings.append(f"EXTENSION_INCOMPATIBLE:{extension_name}")
    return CompatibilityReport(
        compatible=not warnings,
        os_version=os_version,
        adapter=contract.adapter.name,
        extensions=extension_names,
        warnings=tuple(warnings),
    )
