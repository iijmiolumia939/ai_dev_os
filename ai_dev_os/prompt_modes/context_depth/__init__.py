from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.context_subset.continuity_scope import ContinuityScopeFrame
from ai_dev_os.prompt_modes.reasoning_profile import ReasoningProfileFrame


@dataclass(frozen=True)
class ContextDepthFrame:
    included_depth: tuple[str, ...]
    excluded_depth: tuple[str, ...]
    compact_required: bool
    summary_only_required: bool
    retrieval_scaling_required: bool
    continuity_budget: int


class ContextDepthPolicy:
    def depth(
        self,
        profile: ReasoningProfileFrame,
        continuity_scope: ContinuityScopeFrame,
    ) -> ContextDepthFrame:
        included = ["active_sprint_depth", "runtime_continuity_depth"]
        if profile.mode == "isolated_architecture":
            included.append("architecture_continuity_depth")
        if profile.mode == "rollout_review":
            included.append("rollout_continuity_depth")
        if profile.mode == "retrieval_maintenance":
            included.append("retrieval_continuity_depth")
        excluded = ["full_historical_continuity", *continuity_scope.excluded_context]
        retrieval_scaling = profile.retrieval_budget >= 1300 or len(included) >= 3
        return ContextDepthFrame(
            included_depth=tuple(dict.fromkeys(included)),
            excluded_depth=tuple(dict.fromkeys(excluded)),
            compact_required=True,
            summary_only_required=True,
            retrieval_scaling_required=retrieval_scaling,
            continuity_budget=min(continuity_scope.continuity_budget, profile.retrieval_budget),
        )
