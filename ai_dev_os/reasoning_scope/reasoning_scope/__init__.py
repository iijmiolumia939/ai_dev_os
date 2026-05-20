from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.reasoning_scope.architecture_reasoning_guard import (
    ArchitectureReasoningGuardFrame,
)
from ai_dev_os.reasoning_scope.local_patch_mode import LocalPatchModeFrame
from ai_dev_os.reasoning_scope.reasoning_depth import ReasoningDepthFrame


@dataclass(frozen=True)
class ReasoningScopeFrame:
    bounded_reasoning_depth: bool
    task_local_cognition_scope: tuple[str, ...]
    architecture_expansion_suppression: bool
    governance_escalation_suppression: bool
    adjacent_runtime_only_reasoning_mode: bool
    bounded_cognition_only: bool
    local_only: bool
    deterministic: bool
    summary_only: bool


class ReasoningScopePolicy:
    def scope(
        self,
        *,
        depth: ReasoningDepthFrame,
        guard: ArchitectureReasoningGuardFrame,
        local_patch: LocalPatchModeFrame,
        affected_runtimes: tuple[str, ...],
    ) -> ReasoningScopeFrame:
        task_scope = tuple(dict.fromkeys(sorted(affected_runtimes)))[
            : depth.maximum_reasoning_neighborhood
        ]
        return ReasoningScopeFrame(
            bounded_reasoning_depth=depth.reasoning_depth_cap <= 4,
            task_local_cognition_scope=task_scope,
            architecture_expansion_suppression=guard.architecture_expansion_suppression,
            governance_escalation_suppression=guard.governance_escalation_suppression,
            adjacent_runtime_only_reasoning_mode=(
                local_patch.adjacent_runtime_only_reasoning_mode
            ),
            bounded_cognition_only=local_patch.bounded_cognition_only,
            local_only=True,
            deterministic=True,
            summary_only=True,
        )
