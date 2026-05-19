from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.prompt_modes.reasoning_profile import ReasoningProfileFrame


@dataclass(frozen=True)
class PromptShapeFrame:
    recommended_prompt_shape: str
    prompt_compactness: str
    summary_density: str
    continuity_inclusion: str
    architecture_context_allowance: str
    review_checklist_density: str
    retrieval_injection_allowance: str
    compact_mode: bool
    architecture_mode: bool
    summary_only_mode: bool
    isolation_required: bool


class PromptShapePolicy:
    def shape(self, profile: ReasoningProfileFrame) -> PromptShapeFrame:
        architecture_mode = profile.mode == "isolated_architecture"
        release_like = profile.mode in {"rollout_review", "governance_review"}
        compactness = "strict" if profile.mode == "bounded_implementation" else "bounded"
        checklist = "dense" if architecture_mode or release_like else "focused"
        retrieval = "budgeted" if profile.retrieval_budget > 1000 else "minimal"
        prompt_shape = self._shape_name(profile.mode)
        return PromptShapeFrame(
            recommended_prompt_shape=prompt_shape,
            prompt_compactness=compactness,
            summary_density="high" if compactness == "strict" else "medium",
            continuity_inclusion=profile.continuity_preservation_level,
            architecture_context_allowance=profile.architecture_allowance,
            review_checklist_density=checklist,
            retrieval_injection_allowance=retrieval,
            compact_mode=True,
            architecture_mode=architecture_mode,
            summary_only_mode=True,
            isolation_required=profile.escalation_policy == "isolate_only",
        )

    def _shape_name(self, mode: str) -> str:
        if mode == "isolated_architecture":
            return "architecture_decision_prompt"
        if mode == "rollout_review":
            return "rollout_gate_prompt"
        if mode == "governance_review":
            return "governance_gate_prompt"
        if mode == "debugging":
            return "debugging_scope_prompt"
        return "compact_patch_prompt"
