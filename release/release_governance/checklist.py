from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseChecklist:
    governance_validation: bool
    cost_governance_validation: bool
    extension_validation: bool
    compatibility_validation: bool
    package_build_validation: bool
    readme_rendering_validation: bool
    twine_validation: bool


def validate_release(checklist: ReleaseChecklist) -> tuple[bool, tuple[str, ...]]:
    failures = tuple(field for field, value in checklist.__dict__.items() if not value)
    return (not failures, failures)
