from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ReasoningTier(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


TIER_ORDER = {
    ReasoningTier.LOW: 0,
    ReasoningTier.MEDIUM: 1,
    ReasoningTier.HIGH: 2,
}

HIGH_REASONING_TERMS = frozenset(
    {
        "architecture",
        "governance redesign",
        "embodiment",
        "rollout strategy",
        "runtime boundary",
        "boundary design",
        "authority risk",
    }
)
MEDIUM_REASONING_TERMS = frozenset(
    {
        "runtime integration",
        "adapter",
        "orchestration wiring",
        "migration",
        "rollout implementation",
        "integration",
    }
)
LOW_REASONING_TERMS = frozenset(
    {
        "formatting",
        "snapshot",
        "repetitive test",
        "markdown",
        "checklist",
        "repetitive glue",
        "docs",
    }
)


@dataclass(frozen=True)
class ReasoningTierFrame:
    task_name: str
    recommended_tier: str
    minimum_tier: str
    downgrade_possible: bool
    escalation_path: str
    compaction_recommendation: bool
    classification_reason: str
    human_visible: bool
    deterministic_policy: bool
    provider_neutral: bool
    rollback_safe: bool


@dataclass(frozen=True)
class ReasoningTask:
    name: str
    description: str = ""
    affected_runtimes: tuple[str, ...] = ()
    architecture_sensitive: bool = False
    governance_sensitive: bool = False
    embodiment_sensitive: bool = False
    runtime_authority_risk: bool = False


class ReasoningTierPolicy:
    def classify(self, task: ReasoningTask) -> ReasoningTierFrame:
        text = " ".join((task.name, task.description, " ".join(task.affected_runtimes))).lower()
        protected = (
            task.architecture_sensitive
            or task.governance_sensitive
            or task.embodiment_sensitive
            or task.runtime_authority_risk
        )
        if protected or any(term in text for term in HIGH_REASONING_TERMS):
            tier = ReasoningTier.HIGH
            reason = "protected_architecture_governance_or_embodiment_scope"
        elif (
            any(term in text for term in MEDIUM_REASONING_TERMS)
            or len(task.affected_runtimes) >= 2
        ):
            tier = ReasoningTier.MEDIUM
            reason = "runtime_integration_or_cross_runtime_scope"
        elif any(term in text for term in LOW_REASONING_TERMS):
            tier = ReasoningTier.LOW
            reason = "repetitive_or_low_authority_work"
        else:
            tier = ReasoningTier.MEDIUM
            reason = "default_bounded_implementation"

        minimum = ReasoningTier.HIGH if protected else ReasoningTier.LOW
        return ReasoningTierFrame(
            task_name=task.name,
            recommended_tier=tier.value,
            minimum_tier=minimum.value,
            downgrade_possible=TIER_ORDER[tier] > TIER_ORDER[minimum],
            escalation_path=(
                "human_visible_policy_escalation" if tier is ReasoningTier.HIGH else "none"
            ),
            compaction_recommendation=tier is ReasoningTier.HIGH,
            classification_reason=reason,
            human_visible=True,
            deterministic_policy=True,
            provider_neutral=True,
            rollback_safe=True,
        )


def coerce_tier(value: str | ReasoningTier) -> ReasoningTier:
    if isinstance(value, ReasoningTier):
        return value
    return ReasoningTier(value.upper())
