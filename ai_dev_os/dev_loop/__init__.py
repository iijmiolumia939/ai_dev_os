from __future__ import annotations

from dataclasses import dataclass

LIFECYCLE_STATES = ("PLANNING", "ACTIVE", "VALIDATING", "CLOSING", "ROLLOVER_READY")
DEV_LOOP_REQUIREMENT_IDS = tuple(f"FR-AIDEVLOOP-{index:02d}" for index in range(1, 11)) + (
    "NFR-COST-21",
    "NFR-ARCH-35",
    "NFR-SEC-06",
)
DEV_LOOP_TEST_IDS = tuple(f"TC-AIDEVLOOP-{index:02d}" for index in range(1, 11))


@dataclass(frozen=True)
class SprintScopeFrame:
    adjacent_runtime_scope: tuple[str, ...]
    runtime_neighborhood_recommendation: tuple[str, ...]
    local_patch_required: bool
    repo_wide_synthesis_forbidden: bool
    autonomous_scope_expansion_forbidden: bool
    roadmap_explosion_forbidden: bool


@dataclass(frozen=True)
class SprintComplexityFrame:
    reasoning_depth_recommendation: str
    retrieval_radius_recommendation: int
    provider_routing_recommendation: str
    bounded_cognition_only: bool
    cognition_expansion_pressure: str
    provider_escalation_pressure: str
    no_hidden_provider_switching: bool


@dataclass(frozen=True)
class SprintPlanningFrame:
    bounded_sprint_objective: str
    adjacent_runtime_only_scope: tuple[str, ...]
    local_patch_recommendation: bool
    provider_routing_recommendation: str
    reasoning_depth_recommendation: str
    retrieval_radius_recommendation: int
    no_roadmap_explosion: bool
    no_repo_wide_sprint_synthesis: bool
    no_giant_architecture_replay: bool
    no_autonomous_scope_expansion: bool


@dataclass(frozen=True)
class SprintLifecycleFrame:
    lifecycle_state: str
    next_allowed_states: tuple[str, ...]
    compact_lifecycle_summary: str
    validation_gate_required: bool
    validation_gate_passed: bool
    stale_sprint_detected: bool
    bounded_transition: bool


@dataclass(frozen=True)
class SprintClosureFrame:
    compact_closure_summary: str
    validation_summary: str
    delta_carryover: tuple[str, ...]
    compact_closure_ready: bool
    full_history_replay_forbidden: bool


@dataclass(frozen=True)
class SprintRolloverFrame:
    rollover_ready: bool
    compact_rollover_summary: str
    next_session_seed: str
    stale_sprint_evicted: bool
    infinite_sprint_chaining_prevented: bool


@dataclass(frozen=True)
class SprintProposalFrame:
    next_bounded_sprint_proposal: str
    adjacent_runtime_only_continuation: tuple[str, ...]
    runtime_neighborhood_recommendation: tuple[str, ...]
    provider_aware_implementation_recommendation: str
    infinite_sprint_chaining_prevented: bool
    giant_roadmap_branching_prevented: bool
    architecture_wide_planning_forbidden: bool


@dataclass(frozen=True)
class SprintContinuityFrame:
    compact_sprint_continuity: str
    delta_only_carryover: tuple[str, ...]
    stale_sprint_eviction: tuple[str, ...]
    compact_session_bootstrap: str
    bounded_continuity_summary: str
    giant_continuity_replay_forbidden: bool
    full_sprint_history_replay_forbidden: bool
    hidden_continuity_accumulation_forbidden: bool


@dataclass(frozen=True)
class SprintBootstrapFrame:
    next_session_bootstrap_draft: str
    compact_continuation_prompt: str
    provider_routing_summary: str
    local_patch_reminder: str
    validation_reminder: str
    enter_only_continuation_workflow: bool
    bounded_bootstrap_payload: bool
    provider_aware_bootstrap_summary: bool


@dataclass(frozen=True)
class SprintGovernanceFrame:
    sprint_explosion_pressure: str
    cognition_expansion_pressure: str
    provider_escalation_pressure: str
    roadmap_branching_pressure: str
    continuity_accumulation_pressure: str
    compact_governance_warnings: tuple[str, ...]
    downgrade_recommendations: tuple[str, ...]
    local_patch_enforcement_reminders: tuple[str, ...]
    human_confirmed_orchestration_only: bool


@dataclass(frozen=True)
class SprintDevelopmentLoopFrame:
    planning: SprintPlanningFrame
    lifecycle: SprintLifecycleFrame
    scope: SprintScopeFrame
    complexity: SprintComplexityFrame
    closure: SprintClosureFrame
    rollover: SprintRolloverFrame
    proposal: SprintProposalFrame
    bootstrap: SprintBootstrapFrame
    continuity: SprintContinuityFrame
    governance: SprintGovernanceFrame
    dev_loop_active: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_cognition_only: bool
    human_confirmed_orchestration_only: bool
    no_autonomous_roadmap_expansion: bool
    no_hidden_provider_switching: bool
    no_giant_continuity_replay: bool
    provider_routing_distribution: dict[str, int]
    estimated_avoided_manual_orchestration_tokens: int
    estimated_avoided_sprint_explosion: int
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]


class SprintScopeRuntime:
    def frame(
        self,
        *,
        affected_runtime: str,
        adjacent_runtimes: tuple[str, ...],
        requested_scope: tuple[str, ...] = (),
    ) -> SprintScopeFrame:
        allowed = _dedupe((affected_runtime, *adjacent_runtimes))[:3]
        requested = requested_scope or allowed
        neighborhood = tuple(runtime for runtime in requested if runtime in allowed) or allowed[:1]
        return SprintScopeFrame(
            adjacent_runtime_scope=neighborhood,
            runtime_neighborhood_recommendation=neighborhood,
            local_patch_required=True,
            repo_wide_synthesis_forbidden=True,
            autonomous_scope_expansion_forbidden=True,
            roadmap_explosion_forbidden=True,
        )


class SprintComplexityRuntime:
    def frame(
        self,
        *,
        governance_sensitive: bool,
        architecture_sensitive: bool,
        repetitive_summary: bool = False,
    ) -> SprintComplexityFrame:
        provider = _provider_class(
            governance_sensitive=governance_sensitive,
            architecture_sensitive=architecture_sensitive,
            repetitive_summary=repetitive_summary,
            planning=True,
        )
        depth = "bounded-high" if provider == "HIGH" else "bounded-medium"
        radius = 2 if provider == "HIGH" else 1
        return SprintComplexityFrame(
            reasoning_depth_recommendation=depth,
            retrieval_radius_recommendation=radius,
            provider_routing_recommendation=provider,
            bounded_cognition_only=True,
            cognition_expansion_pressure="MEDIUM" if provider == "HIGH" else "LOW",
            provider_escalation_pressure="MEDIUM" if provider == "HIGH" else "LOW",
            no_hidden_provider_switching=True,
        )


class SprintPlanningRuntime:
    def generate(
        self,
        *,
        objective_seed: str,
        scope: SprintScopeFrame,
        complexity: SprintComplexityFrame,
    ) -> SprintPlanningFrame:
        objective = _compact_text(objective_seed, fallback="Implement bounded sprint dev loop")
        return SprintPlanningFrame(
            bounded_sprint_objective=f"Bounded sprint: {objective}",
            adjacent_runtime_only_scope=scope.adjacent_runtime_scope,
            local_patch_recommendation=scope.local_patch_required,
            provider_routing_recommendation=complexity.provider_routing_recommendation,
            reasoning_depth_recommendation=complexity.reasoning_depth_recommendation,
            retrieval_radius_recommendation=complexity.retrieval_radius_recommendation,
            no_roadmap_explosion=True,
            no_repo_wide_sprint_synthesis=True,
            no_giant_architecture_replay=True,
            no_autonomous_scope_expansion=True,
        )


class SprintLifecycleRuntime:
    def transition(
        self,
        *,
        state: str,
        validation_passed: bool = False,
        sprint_age_days: int = 0,
        continuity_tokens: int = 0,
    ) -> SprintLifecycleFrame:
        normalized = state if state in LIFECYCLE_STATES else "PLANNING"
        next_states = {
            "PLANNING": ("ACTIVE",),
            "ACTIVE": ("VALIDATING", "CLOSING"),
            "VALIDATING": ("CLOSING",) if validation_passed else ("ACTIVE",),
            "CLOSING": ("ROLLOVER_READY",) if validation_passed else ("VALIDATING",),
            "ROLLOVER_READY": (),
        }[normalized]
        stale = sprint_age_days > 14 or continuity_tokens > 4_000
        return SprintLifecycleFrame(
            lifecycle_state=normalized,
            next_allowed_states=next_states,
            compact_lifecycle_summary=(
                f"{normalized}: next={','.join(next_states) or 'none'}; "
                f"validation={'pass' if validation_passed else 'required'}"
            ),
            validation_gate_required=normalized in {"VALIDATING", "CLOSING"},
            validation_gate_passed=validation_passed,
            stale_sprint_detected=stale,
            bounded_transition=True,
        )


class SprintClosureRuntime:
    def close(
        self,
        *,
        validation_summary: str,
        changed_runtimes: tuple[str, ...],
        remaining_deltas: tuple[str, ...] = (),
    ) -> SprintClosureFrame:
        deltas = _dedupe((*changed_runtimes[:3], *remaining_deltas[:3]))
        summary = _compact_text(validation_summary, fallback="validation pending")
        return SprintClosureFrame(
            compact_closure_summary=f"closure: {summary}; deltas={','.join(deltas) or 'none'}",
            validation_summary=summary,
            delta_carryover=deltas,
            compact_closure_ready=True,
            full_history_replay_forbidden=True,
        )


class SprintRolloverRuntime:
    def prepare(
        self,
        *,
        closure: SprintClosureFrame,
        lifecycle: SprintLifecycleFrame,
    ) -> SprintRolloverFrame:
        ready = lifecycle.lifecycle_state == "ROLLOVER_READY" or closure.compact_closure_ready
        seed = "Continue only the closure deltas: " + (
            ", ".join(closure.delta_carryover) or "none"
        )
        return SprintRolloverFrame(
            rollover_ready=ready,
            compact_rollover_summary=closure.compact_closure_summary,
            next_session_seed=seed,
            stale_sprint_evicted=lifecycle.stale_sprint_detected,
            infinite_sprint_chaining_prevented=True,
        )


class SprintProposalRuntime:
    def generate(
        self,
        *,
        planning: SprintPlanningFrame,
        scope: SprintScopeFrame,
        completed_sprint_count: int = 0,
    ) -> SprintProposalFrame:
        continuation = scope.runtime_neighborhood_recommendation[:2]
        chained = completed_sprint_count >= 3
        provider = "LOW" if chained else planning.provider_routing_recommendation
        return SprintProposalFrame(
            next_bounded_sprint_proposal=(
                f"Next bounded sprint for {planning.bounded_sprint_objective[:72]}"
            ),
            adjacent_runtime_only_continuation=continuation,
            runtime_neighborhood_recommendation=continuation,
            provider_aware_implementation_recommendation=provider,
            infinite_sprint_chaining_prevented=True,
            giant_roadmap_branching_prevented=True,
            architecture_wide_planning_forbidden=True,
        )


class SprintContinuityRuntime:
    def compact(
        self,
        *,
        closure: SprintClosureFrame,
        stale_sprints: tuple[str, ...] = (),
    ) -> SprintContinuityFrame:
        deltas = closure.delta_carryover[:4]
        summary = f"continuity: {closure.validation_summary}; carry={','.join(deltas) or 'none'}"
        bootstrap = "Bootstrap with delta-only carryover and validation reminders."
        return SprintContinuityFrame(
            compact_sprint_continuity=summary,
            delta_only_carryover=deltas,
            stale_sprint_eviction=stale_sprints[:4],
            compact_session_bootstrap=bootstrap,
            bounded_continuity_summary=summary,
            giant_continuity_replay_forbidden=True,
            full_sprint_history_replay_forbidden=True,
            hidden_continuity_accumulation_forbidden=True,
        )


class SprintBootstrapRuntime:
    def generate(
        self,
        *,
        proposal: SprintProposalFrame,
        continuity: SprintContinuityFrame,
    ) -> SprintBootstrapFrame:
        provider = proposal.provider_aware_implementation_recommendation
        prompt = (
            f"Enter-only continuation: {proposal.next_bounded_sprint_proposal}; "
            f"carry={','.join(continuity.delta_only_carryover) or 'none'}"
        )
        return SprintBootstrapFrame(
            next_session_bootstrap_draft=prompt,
            compact_continuation_prompt=prompt[:480],
            provider_routing_summary=f"provider={provider}; hidden_switching=forbidden",
            local_patch_reminder="LOCAL_PATCH_REQUIRED: adjacent runtimes only.",
            validation_reminder=(
                "Run scoped tests, full tests, runtime_audit, build, extension compile."
            ),
            enter_only_continuation_workflow=True,
            bounded_bootstrap_payload=len(prompt) <= 480,
            provider_aware_bootstrap_summary=True,
        )


class SprintGovernanceRuntime:
    def evaluate(
        self,
        *,
        planning: SprintPlanningFrame,
        continuity: SprintContinuityFrame,
        lifecycle: SprintLifecycleFrame,
    ) -> SprintGovernanceFrame:
        sprint_pressure = _pressure(len(planning.adjacent_runtime_only_scope), high_at=4)
        cognition_pressure = (
            "MEDIUM" if planning.reasoning_depth_recommendation.endswith("high") else "LOW"
        )
        provider_pressure = (
            "MEDIUM" if planning.provider_routing_recommendation == "HIGH" else "LOW"
        )
        roadmap_pressure = "LOW" if planning.no_roadmap_explosion else "HIGH"
        continuity_pressure = _pressure(len(continuity.delta_only_carryover), high_at=5)
        warnings = tuple(
            warning
            for warning in (
                "compact_scope_only" if sprint_pressure != "LOW" else "",
                "validation_gate_required" if lifecycle.validation_gate_required else "",
                "delta_only_continuity" if continuity_pressure != "LOW" else "",
            )
            if warning
        )
        return SprintGovernanceFrame(
            sprint_explosion_pressure=sprint_pressure,
            cognition_expansion_pressure=cognition_pressure,
            provider_escalation_pressure=provider_pressure,
            roadmap_branching_pressure=roadmap_pressure,
            continuity_accumulation_pressure=continuity_pressure,
            compact_governance_warnings=warnings,
            downgrade_recommendations=("prefer_LOW_for_closure", "prefer_MEDIUM_for_planning"),
            local_patch_enforcement_reminders=(
                "LOCAL_PATCH_REQUIRED",
                "human_confirmed_orchestration_only",
            ),
            human_confirmed_orchestration_only=True,
        )


class SprintDevLoopRuntime:
    def evaluate(
        self,
        *,
        objective_seed: str = "AI Development Loop Runtime",
        affected_runtime: str = "dev_loop",
        adjacent_runtimes: tuple[str, ...] = (
            "session_orchestrator",
            "provider_routing",
            "runtime_audit",
        ),
        lifecycle_state: str = "PLANNING",
        validation_passed: bool = False,
        sprint_age_days: int = 0,
        continuity_tokens: int = 0,
        completed_sprint_count: int = 0,
        stale_sprints: tuple[str, ...] = (),
        governance_sensitive: bool = True,
        architecture_sensitive: bool = False,
    ) -> SprintDevelopmentLoopFrame:
        scope = SprintScopeRuntime().frame(
            affected_runtime=affected_runtime,
            adjacent_runtimes=adjacent_runtimes,
        )
        complexity = SprintComplexityRuntime().frame(
            governance_sensitive=governance_sensitive,
            architecture_sensitive=architecture_sensitive,
        )
        planning = SprintPlanningRuntime().generate(
            objective_seed=objective_seed,
            scope=scope,
            complexity=complexity,
        )
        lifecycle = SprintLifecycleRuntime().transition(
            state=lifecycle_state,
            validation_passed=validation_passed,
            sprint_age_days=sprint_age_days,
            continuity_tokens=continuity_tokens,
        )
        closure = SprintClosureRuntime().close(
            validation_summary="validation pass" if validation_passed else "validation required",
            changed_runtimes=scope.adjacent_runtime_scope,
            remaining_deltas=("runtime_audit", "vscode_extension"),
        )
        rollover = SprintRolloverRuntime().prepare(closure=closure, lifecycle=lifecycle)
        proposal = SprintProposalRuntime().generate(
            planning=planning,
            scope=scope,
            completed_sprint_count=completed_sprint_count,
        )
        continuity = SprintContinuityRuntime().compact(
            closure=closure,
            stale_sprints=stale_sprints,
        )
        bootstrap = SprintBootstrapRuntime().generate(proposal=proposal, continuity=continuity)
        governance = SprintGovernanceRuntime().evaluate(
            planning=planning,
            continuity=continuity,
            lifecycle=lifecycle,
        )
        provider_distribution = {"HIGH": 3, "MEDIUM": 3, "LOW": 3}
        avoided_orchestration = 1_800 + len(scope.adjacent_runtime_scope) * 240
        avoided_explosion = 1_200 + len(continuity.stale_sprint_eviction) * 400
        active = all(
            (
                planning.no_roadmap_explosion,
                lifecycle.bounded_transition,
                closure.compact_closure_ready,
                rollover.infinite_sprint_chaining_prevented,
                proposal.giant_roadmap_branching_prevented,
                bootstrap.bounded_bootstrap_payload,
                continuity.giant_continuity_replay_forbidden,
                governance.human_confirmed_orchestration_only,
            )
        )
        return SprintDevelopmentLoopFrame(
            planning=planning,
            lifecycle=lifecycle,
            scope=scope,
            complexity=complexity,
            closure=closure,
            rollover=rollover,
            proposal=proposal,
            bootstrap=bootstrap,
            continuity=continuity,
            governance=governance,
            dev_loop_active=active,
            local_only=True,
            deterministic=True,
            summary_only=True,
            bounded_cognition_only=True,
            human_confirmed_orchestration_only=True,
            no_autonomous_roadmap_expansion=True,
            no_hidden_provider_switching=True,
            no_giant_continuity_replay=True,
            provider_routing_distribution=provider_distribution,
            estimated_avoided_manual_orchestration_tokens=avoided_orchestration,
            estimated_avoided_sprint_explosion=avoided_explosion,
            requirement_ids=DEV_LOOP_REQUIREMENT_IDS,
            test_ids=DEV_LOOP_TEST_IDS,
        )


def _compact_text(value: str, *, fallback: str) -> str:
    collapsed = " ".join(value.split()) or fallback
    return collapsed[:120]


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


def _provider_class(
    *,
    governance_sensitive: bool,
    architecture_sensitive: bool,
    repetitive_summary: bool,
    planning: bool,
) -> str:
    if architecture_sensitive or (governance_sensitive and not planning):
        return "HIGH"
    if planning and not repetitive_summary:
        return "MEDIUM"
    return "LOW"


def _pressure(count: int, *, high_at: int) -> str:
    if count >= high_at:
        return "HIGH"
    if count > 1:
        return "MEDIUM"
    return "LOW"


__all__ = [
    "DEV_LOOP_REQUIREMENT_IDS",
    "DEV_LOOP_TEST_IDS",
    "LIFECYCLE_STATES",
    "SprintBootstrapFrame",
    "SprintBootstrapRuntime",
    "SprintClosureFrame",
    "SprintClosureRuntime",
    "SprintComplexityFrame",
    "SprintComplexityRuntime",
    "SprintContinuityFrame",
    "SprintContinuityRuntime",
    "SprintDevLoopRuntime",
    "SprintDevelopmentLoopFrame",
    "SprintGovernanceFrame",
    "SprintGovernanceRuntime",
    "SprintLifecycleFrame",
    "SprintLifecycleRuntime",
    "SprintPlanningFrame",
    "SprintPlanningRuntime",
    "SprintProposalFrame",
    "SprintProposalRuntime",
    "SprintRolloverFrame",
    "SprintRolloverRuntime",
    "SprintScopeFrame",
    "SprintScopeRuntime",
]
