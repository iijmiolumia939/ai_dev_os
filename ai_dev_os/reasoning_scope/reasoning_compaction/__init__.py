from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReasoningCompactionFrame:
    compact_reasoning_summaries: tuple[str, ...]
    compact_escalation_explanations: tuple[str, ...]
    deduplicated_governance_reasoning: tuple[str, ...]
    expandable_deep_details: tuple[str, ...]
    deep_details_required: bool
    summary_only: bool
    deterministic: bool


class ReasoningCompactionPolicy:
    def compact(
        self,
        *,
        reasoning_summaries: tuple[str, ...],
        escalation_explanations: tuple[str, ...] = (),
        governance_reasoning: tuple[str, ...] = (),
        deep_details: tuple[str, ...] = (),
        deep_details_required: bool = False,
    ) -> ReasoningCompactionFrame:
        summaries = tuple(dict.fromkeys(summary[:120] for summary in reasoning_summaries))
        explanations = tuple(
            dict.fromkeys(explanation[:120] for explanation in escalation_explanations)
        )
        governance = tuple(dict.fromkeys(sorted(governance_reasoning)))
        details = tuple(deep_details if deep_details_required else ())
        return ReasoningCompactionFrame(
            compact_reasoning_summaries=summaries,
            compact_escalation_explanations=explanations,
            deduplicated_governance_reasoning=governance,
            expandable_deep_details=details,
            deep_details_required=deep_details_required,
            summary_only=True,
            deterministic=True,
        )
