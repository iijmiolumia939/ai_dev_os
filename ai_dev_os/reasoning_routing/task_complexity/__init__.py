from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskComplexityInput:
    architecture_density: int = 0
    cross_runtime_scope: int = 0
    continuity_size: int = 0
    reasoning_depth: int = 0
    dependency_breadth: int = 0
    governance_sensitivity: int = 0
    runtime_authority_risk: int = 0


@dataclass(frozen=True)
class TaskComplexityFrame:
    complexity_level: str
    reasoning_recommendation: str
    escalation_required: bool
    estimated_reasoning_burn: int
    bounded_metadata: bool
    scoring_breakdown: dict[str, int]


class TaskComplexityPolicy:
    def evaluate(self, data: TaskComplexityInput) -> TaskComplexityFrame:
        breakdown = {
            "architecture_density": _bounded_score(data.architecture_density),
            "cross_runtime_scope": _bounded_score(data.cross_runtime_scope),
            "continuity_size": _bounded_score(data.continuity_size),
            "reasoning_depth": _bounded_score(data.reasoning_depth),
            "dependency_breadth": _bounded_score(data.dependency_breadth),
            "governance_sensitivity": _bounded_score(data.governance_sensitivity),
            "runtime_authority_risk": _bounded_score(data.runtime_authority_risk),
        }
        score = sum(breakdown.values())
        protected_pressure = (
            breakdown["governance_sensitivity"] >= 2
            or breakdown["runtime_authority_risk"] >= 2
            or breakdown["architecture_density"] >= 3
        )
        if score >= 14 or protected_pressure:
            level = "HIGH"
            recommendation = "HIGH"
            burn = 8 + score
        elif score >= 7:
            level = "MEDIUM"
            recommendation = "MEDIUM"
            burn = 3 + score
        else:
            level = "LOW"
            recommendation = "LOW"
            burn = 1 + score
        return TaskComplexityFrame(
            complexity_level=level,
            reasoning_recommendation=recommendation,
            escalation_required=level == "HIGH",
            estimated_reasoning_burn=burn,
            bounded_metadata=True,
            scoring_breakdown=breakdown,
        )


def _bounded_score(value: int) -> int:
    return max(0, min(3, int(value)))
