from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalBudgetPolicyFrame:
    max_runtime_count: int
    max_contract_count: int
    max_continuity_size: int
    retrieval_escalation_thresholds: dict[str, int]
    compact_retrieval_recommendation: bool
    budget_exceeded: bool
    retrieval_escalation_required: bool
    automatic_retrieval_escalation: bool
    deterministic: bool


class RetrievalBudgetPolicy:
    def __init__(
        self,
        *,
        max_runtime_count: int = 5,
        max_contract_count: int = 8,
        max_continuity_size: int = 2_400,
    ) -> None:
        self.max_runtime_count = max_runtime_count
        self.max_contract_count = max_contract_count
        self.max_continuity_size = max_continuity_size

    def evaluate(
        self,
        *,
        runtime_count: int,
        contract_count: int,
        continuity_size: int,
    ) -> RetrievalBudgetPolicyFrame:
        thresholds = {
            "runtime_count": self.max_runtime_count,
            "contract_count": self.max_contract_count,
            "continuity_size": self.max_continuity_size,
        }
        budget_exceeded = (
            runtime_count > self.max_runtime_count
            or contract_count > self.max_contract_count
            or continuity_size > self.max_continuity_size
        )
        escalation_required = (
            runtime_count > self.max_runtime_count * 2
            or contract_count > self.max_contract_count * 2
            or continuity_size > self.max_continuity_size * 2
        )
        return RetrievalBudgetPolicyFrame(
            max_runtime_count=self.max_runtime_count,
            max_contract_count=self.max_contract_count,
            max_continuity_size=self.max_continuity_size,
            retrieval_escalation_thresholds=thresholds,
            compact_retrieval_recommendation=budget_exceeded,
            budget_exceeded=budget_exceeded,
            retrieval_escalation_required=escalation_required,
            automatic_retrieval_escalation=False,
            deterministic=True,
        )
