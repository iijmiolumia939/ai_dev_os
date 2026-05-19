from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.context_subset.session_focus import SessionFocusFrame

PROFILE_BY_MODE = {
    "bounded_implementation": (
        "low",
        "none",
        900,
        "lightweight_patch_review",
        "minimal",
        "no_escalation",
    ),
    "isolated_architecture": (
        "high",
        "isolated",
        1600,
        "architecture_review",
        "scoped",
        "isolate_only",
    ),
    "rollout_review": (
        "medium",
        "limited",
        1200,
        "release_review",
        "bounded",
        "approval_required",
    ),
    "governance_review": (
        "medium",
        "limited",
        1100,
        "governance_review",
        "bounded",
        "council_when_needed",
    ),
    "debugging": ("medium", "none", 1000, "scoped_runtime_review", "minimal", "no_architecture"),
    "retrieval_maintenance": (
        "medium",
        "limited",
        1300,
        "scoped_runtime_review",
        "bounded",
        "budget_guarded",
    ),
    "provider_analysis": (
        "medium",
        "limited",
        1200,
        "scoped_runtime_review",
        "bounded",
        "no_vendor_lock_in",
    ),
    "renderer_review": (
        "medium",
        "none",
        1000,
        "scoped_runtime_review",
        "minimal",
        "thin_renderer_only",
    ),
}


@dataclass(frozen=True)
class ReasoningProfileFrame:
    mode: str
    reasoning_depth: str
    architecture_allowance: str
    retrieval_budget: int
    review_intensity: str
    continuity_preservation_level: str
    escalation_policy: str
    bounded: bool


class ReasoningProfilePolicy:
    def profile(
        self, session_focus: SessionFocusFrame | None = None, *, mode: str = ""
    ) -> ReasoningProfileFrame:
        selected = self._mode_for(session_focus, mode)
        depth, allowance, budget, review, continuity, escalation = PROFILE_BY_MODE[selected]
        return ReasoningProfileFrame(
            mode=selected,
            reasoning_depth=depth,
            architecture_allowance=allowance,
            retrieval_budget=budget,
            review_intensity=review,
            continuity_preservation_level=continuity,
            escalation_policy=escalation,
            bounded=True,
        )

    def _mode_for(self, session_focus: SessionFocusFrame | None, mode: str) -> str:
        normalized = mode.replace("-", "_")
        if normalized in PROFILE_BY_MODE:
            return normalized
        if session_focus is None:
            return "bounded_implementation"
        recommended = session_focus.recommended_session_type.replace("-", "_")
        if recommended == "isolated_architecture":
            return recommended
        if session_focus.primary_focus == "rollout":
            return "rollout_review"
        if session_focus.primary_focus == "governance":
            return "governance_review"
        if session_focus.primary_focus == "debugging":
            return "debugging"
        if session_focus.primary_focus == "provider":
            return "provider_analysis"
        if session_focus.primary_focus == "renderer":
            return "renderer_review"
        return "bounded_implementation"
