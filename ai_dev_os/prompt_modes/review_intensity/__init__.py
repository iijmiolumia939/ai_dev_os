from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.prompt_modes.reasoning_profile import ReasoningProfileFrame


@dataclass(frozen=True)
class ReviewIntensityFrame:
    mode: str
    review_depth: str
    required_review_domains: tuple[str, ...]
    adversary_required: bool
    council_required: bool
    runtime_audit_required: bool
    release_gate_required: bool


class ReviewIntensityPolicy:
    def intensity(self, profile: ReasoningProfileFrame) -> ReviewIntensityFrame:
        if profile.review_intensity == "architecture_review":
            return ReviewIntensityFrame(
                mode="architecture_review",
                review_depth="deep_bounded",
                required_review_domains=("architecture", "runtime_boundaries", "tests"),
                adversary_required=True,
                council_required=True,
                runtime_audit_required=True,
                release_gate_required=False,
            )
        if profile.review_intensity == "governance_review":
            return ReviewIntensityFrame(
                mode="governance_review",
                review_depth="scoped",
                required_review_domains=("governance", "cost", "audit"),
                adversary_required=True,
                council_required=False,
                runtime_audit_required=True,
                release_gate_required=False,
            )
        if profile.review_intensity == "release_review":
            return ReviewIntensityFrame(
                mode="release_review",
                review_depth="release_bounded",
                required_review_domains=("ci", "packaging", "remote_verification"),
                adversary_required=False,
                council_required=False,
                runtime_audit_required=True,
                release_gate_required=True,
            )
        if profile.review_intensity == "scoped_runtime_review":
            return ReviewIntensityFrame(
                mode="scoped_runtime_review",
                review_depth="medium",
                required_review_domains=("runtime", "tests"),
                adversary_required=False,
                council_required=False,
                runtime_audit_required=True,
                release_gate_required=False,
            )
        return ReviewIntensityFrame(
            mode="lightweight_patch_review",
            review_depth="lightweight",
            required_review_domains=("patch", "tests"),
            adversary_required=False,
            council_required=False,
            runtime_audit_required=False,
            release_gate_required=False,
        )
