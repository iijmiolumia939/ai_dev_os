from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.session_lifecycle.architecture_isolation import ArchitectureIsolationPolicy
from ai_dev_os.session_lifecycle.continuity_bundle import (
    ContinuityBundleFrame,
    ContinuityBundlePolicy,
    ContinuityBundleSource,
)
from ai_dev_os.session_lifecycle.session_rollover import SessionRolloverPolicy
from ai_dev_os.session_orchestrator.prompt_pack import PromptPackPolicy


@dataclass(frozen=True)
class SprintStartInput:
    sprint_id: str
    project_name: str
    active_fr_tc: tuple[str, ...]
    affected_runtimes: tuple[str, ...]
    previous_sprint_summary: str
    active_risks: tuple[str, ...]
    current_roadmap: tuple[str, ...]
    architecture_flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class SprintStartFrame:
    recommended_session_action: str
    continuity_bundle: ContinuityBundleFrame
    sprint_prompt: str
    context_budget_estimate: int
    architecture_isolation_required: bool
    copy_ready_prompt: str
    excluded_context: tuple[str, ...]


class SprintStartPolicy:
    def build(self, data: SprintStartInput) -> SprintStartFrame:
        architecture_prompt = " ".join(data.architecture_flags)
        architecture = ArchitectureIsolationPolicy().evaluate(
            architecture_prompt,
            affected_runtimes=data.affected_runtimes,
        )
        rollover = SessionRolloverPolicy().evaluate(
            session_age=0,
            estimated_context_tokens=3_200,
            stale_context_ratio=0.0,
            retrieval_pressure="NORMAL",
            cache_reuse_probability=0.7,
            sprint_boundary=True,
            architecture_escalation=architecture.isolated_session_required,
        )
        bundle = ContinuityBundlePolicy(token_budget=2_400).build(
            ContinuityBundleSource(
                active_fr_tc=data.active_fr_tc,
                current_sprint_summary=data.previous_sprint_summary,
                affected_runtimes=data.affected_runtimes,
                active_risks=data.active_risks,
                current_roadmap=data.current_roadmap,
                current_architectural_constraints=data.architecture_flags,
                current_governance_state={
                    "session_action": rollover.recommended_session_action,
                    "context": "compact",
                },
                extra_context={
                    "full_sprint_history": "excluded",
                    "giant_markdown": "excluded",
                },
            ),
            summary_only=architecture.isolated_session_required,
        )
        prompt = PromptPackPolicy().build(
            prompt_type=(
                "architecture_isolation"
                if architecture.isolated_session_required
                else "sprint_start"
            ),
            project_name=data.project_name,
            sprint_id=data.sprint_id,
            objective="start bounded sprint session",
            context_lines=(
                f"Sprint summary: {bundle.current_sprint_summary}",
                f"Active FR/TC: {', '.join(bundle.active_fr_tc)}",
                f"Affected runtimes: {', '.join(bundle.affected_runtimes)}",
                f"Risks: {', '.join(bundle.active_risks)}",
                f"Roadmap: {', '.join(bundle.current_roadmap)}",
                f"Governance: {bundle.current_governance_state}",
            ),
            required_context=("continuity_bundle", "active_fr_tc", "affected_runtimes"),
            excluded_context=bundle.excluded_context,
            affected_runtimes=data.affected_runtimes,
            plain_text=True,
        )
        return SprintStartFrame(
            recommended_session_action=rollover.recommended_session_action,
            continuity_bundle=bundle,
            sprint_prompt=prompt.plain_text,
            context_budget_estimate=bundle.bundle_token_estimate + prompt.estimated_tokens,
            architecture_isolation_required=architecture.isolated_session_required,
            copy_ready_prompt=prompt.copy_ready_text,
            excluded_context=bundle.excluded_context,
        )
