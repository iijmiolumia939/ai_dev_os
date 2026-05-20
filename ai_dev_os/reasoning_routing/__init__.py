from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.reasoning_routing.cost_budget_policy import (
    CostBudgetFrame,
    CostBudgetPolicy,
    ReasoningUsageSample,
)
from ai_dev_os.reasoning_routing.escalation_policy import (
    EscalationFrame,
    EscalationPolicy,
    EscalationPolicyInput,
)
from ai_dev_os.reasoning_routing.quality_floor import QualityFloorFrame, QualityFloorPolicy
from ai_dev_os.reasoning_routing.reasoning_tiers import (
    ReasoningTask,
    ReasoningTier,
    ReasoningTierFrame,
    ReasoningTierPolicy,
)
from ai_dev_os.reasoning_routing.task_complexity import (
    TaskComplexityFrame,
    TaskComplexityInput,
    TaskComplexityPolicy,
)


@dataclass(frozen=True)
class SprintReasoningTask:
    task_name: str
    description: str
    affected_runtimes: tuple[str, ...] = ()
    architecture_sensitive: bool = False
    governance_sensitive: bool = False
    embodiment_sensitive: bool = False
    runtime_authority_risk: bool = False


@dataclass(frozen=True)
class SprintReasoningMapFrame:
    sprint_id: str
    task_tiers: dict[str, str]
    escalation_paths: dict[str, str]
    downgrade_possibility: dict[str, bool]
    compaction_recommendations: dict[str, bool]
    human_visible_routing: bool
    rollback_safe_routing: bool


class SprintReasoningRouter:
    def map(
        self, sprint_id: str, tasks: tuple[SprintReasoningTask, ...]
    ) -> SprintReasoningMapFrame:
        tier_policy = ReasoningTierPolicy()
        task_tiers: dict[str, str] = {}
        escalation_paths: dict[str, str] = {}
        downgrade_possibility: dict[str, bool] = {}
        compaction_recommendations: dict[str, bool] = {}
        for task in tasks:
            frame = tier_policy.classify(
                ReasoningTask(
                    name=task.task_name,
                    description=task.description,
                    affected_runtimes=task.affected_runtimes,
                    architecture_sensitive=task.architecture_sensitive,
                    governance_sensitive=task.governance_sensitive,
                    embodiment_sensitive=task.embodiment_sensitive,
                    runtime_authority_risk=task.runtime_authority_risk,
                )
            )
            task_tiers[task.task_name] = frame.recommended_tier
            escalation_paths[task.task_name] = frame.escalation_path
            downgrade_possibility[task.task_name] = frame.downgrade_possible
            compaction_recommendations[task.task_name] = frame.compaction_recommendation
        return SprintReasoningMapFrame(
            sprint_id=sprint_id,
            task_tiers=task_tiers,
            escalation_paths=escalation_paths,
            downgrade_possibility=downgrade_possibility,
            compaction_recommendations=compaction_recommendations,
            human_visible_routing=True,
            rollback_safe_routing=True,
        )


__all__ = [
    "CostBudgetFrame",
    "CostBudgetPolicy",
    "EscalationFrame",
    "EscalationPolicy",
    "EscalationPolicyInput",
    "QualityFloorFrame",
    "QualityFloorPolicy",
    "ReasoningTask",
    "ReasoningTier",
    "ReasoningTierFrame",
    "ReasoningTierPolicy",
    "ReasoningUsageSample",
    "SprintReasoningMapFrame",
    "SprintReasoningRouter",
    "SprintReasoningTask",
    "TaskComplexityFrame",
    "TaskComplexityInput",
    "TaskComplexityPolicy",
]
