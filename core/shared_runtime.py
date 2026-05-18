from __future__ import annotations

from dataclasses import dataclass

from core.contracts import ProjectProfile, RuntimeHealth


@dataclass(frozen=True)
class SharedRuntimeDecision:
    project: str
    prompt_template: str
    governance_level: str
    local_first: bool
    warnings: tuple[str, ...]


def decide_runtime(profile: ProjectProfile) -> SharedRuntimeDecision:
    warnings: list[str] = []
    prompt_template = "prompts/sprint-lite.prompt.md"
    if profile.scientific_mode:
        prompt_template = "prompts/scientific-runtime.prompt.md"
    if profile.embodiment_mode:
        warnings.append("EMBODIMENT_EXTENSION_REQUIRED")
    return SharedRuntimeDecision(
        project=profile.project_name,
        prompt_template=prompt_template,
        governance_level=profile.governance_level,
        local_first=True,
        warnings=tuple(warnings),
    )


def degrade_component(component: str, reason: str) -> RuntimeHealth:
    return RuntimeHealth(component=component, healthy=False, fallback="local", warnings=(reason,))
