from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectureReasoningGuardFrame:
    architecture_wide_reasoning_forbidden: bool
    broad_runtime_synthesis_prevented: bool
    unnecessary_governance_synthesis_prevented: bool
    giant_architecture_continuity_replay_prevented: bool
    architecture_expansion_suppression: bool
    governance_escalation_suppression: bool
    no_automatic_architecture_escalation: bool
    no_automatic_roadmap_synthesis: bool
    summary_only: bool
    deterministic: bool


class ArchitectureReasoningGuardPolicy:
    def guard(
        self,
        *,
        complexity: str,
        requested_runtime_count: int,
        continuity_size: int,
        governance_sensitive: bool = False,
    ) -> ArchitectureReasoningGuardFrame:
        low_or_medium = complexity.upper() in {"LOW", "MEDIUM"}
        broad = requested_runtime_count > (1 if complexity.upper() == "LOW" else 2)
        giant = continuity_size > 2_400
        return ArchitectureReasoningGuardFrame(
            architecture_wide_reasoning_forbidden=complexity.upper() == "LOW",
            broad_runtime_synthesis_prevented=low_or_medium and broad,
            unnecessary_governance_synthesis_prevented=low_or_medium and governance_sensitive,
            giant_architecture_continuity_replay_prevented=giant,
            architecture_expansion_suppression=low_or_medium and (broad or giant),
            governance_escalation_suppression=low_or_medium,
            no_automatic_architecture_escalation=True,
            no_automatic_roadmap_synthesis=True,
            summary_only=True,
            deterministic=True,
        )
