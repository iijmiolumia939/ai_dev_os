from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RuntimeKind(StrEnum):
    AUTONOMOUS = "autonomous"
    SCIENTIFIC = "scientific"
    EMBODIMENT = "embodiment"
    SERVICE = "service"


@dataclass(frozen=True)
class ProjectProfile:
    project_name: str
    runtime_type: RuntimeKind
    architecture_type: str
    governance_level: str
    scientific_mode: bool = False
    embodiment_mode: bool = False


@dataclass(frozen=True)
class RuntimeHealth:
    component: str
    healthy: bool
    fallback: str = "local"
    warnings: tuple[str, ...] = ()
