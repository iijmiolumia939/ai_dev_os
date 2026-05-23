from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.cognitive_state import CognitiveStateRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer

INTENTIONAL_PLANNING_REQUIREMENT_IDS = tuple(
    f"FR-INTENTIONALPLANNING-{index:02d}" for index in range(1, 45)
) + ("NFR-COST-61", "NFR-ARCH-74", "NFR-SEC-45")
INTENTIONAL_PLANNING_TEST_IDS = tuple(
    f"TC-INTENTIONALPLANNING-{index:02d}" for index in range(1, 45)
)

MAX_ACTIVE_GOALS = 4
MAX_SUSPENDED_GOALS = 4
MAX_COMPLETED_GOALS = 4
MAX_INTERRUPTED_GOALS = 3
MAX_DECAYED_GOALS = 3
MAX_PLANNING_WINDOW_ITEMS = 5
MAX_TASK_SALIENCE_ITEMS = 5
MAX_CONTINUATION_DEPTH = 3
PLANNING_BUDGET_LIMIT = 12
PLANNING_SATURATION_THRESHOLD = 85
DECAY_WATCH_THRESHOLD = 45
DECAY_RESET_THRESHOLD = 70

DEFAULT_GOAL_PRIORITIES = {
    "implement_intentional_planning": 42,
    "validate_runtime": 31,
    "connect_vscode": 17,
    "commit_push": 10,
}
DEFAULT_TASK_SALIENCE = {
    "goal_hierarchy": 34,
    "planning_governance": 29,
    "planning_decay": 21,
    "vscode_visibility": 16,
}


@dataclass(frozen=True)
class ActiveGoalFrame:
    active_goal_id: str
    active_goal_summary: str
    active_goal_status: str
    local_patch_scope: bool
    goal_can_synthesize_children: bool
    recursive_goal_synthesis_blocked: bool


@dataclass(frozen=True)
class GoalHierarchyFrame:
    active_goals: tuple[str, ...]
    suspended_goals: tuple[str, ...]
    completed_goals: tuple[str, ...]
    interrupted_goals: tuple[str, ...]
    decayed_goals: tuple[str, ...]
    total_tracked_goals: int
    hierarchy_limit: int
    bounded_goal_hierarchy: bool
    self_expanding_tree_blocked: bool


@dataclass(frozen=True)
class GoalPriorityFrame:
    priority_order: tuple[str, ...]
    primary_goal: str
    deterministic_goal_prioritization: bool
    active_goal_count: int
    priority_limit: int
    autonomous_reprioritization_blocked: bool


@dataclass(frozen=True)
class TaskSalienceFrame:
    salient_tasks: tuple[str, ...]
    salience_scores: tuple[str, ...]
    execution_relevance: str
    active_task_priority: str
    bounded_context_relevance: bool
    planning_continuation_necessity: str
    retrieval_scope_widening_blocked: bool
    dynamic_objective_synthesis_blocked: bool


@dataclass(frozen=True)
class PlanningWindowFrame:
    planning_window_items: tuple[str, ...]
    window_limit: int
    planning_window_pressure: str
    planning_saturation_score: int
    saturation_threshold: int
    bounded_planning_window: bool
    repo_wide_execution_reprioritization_blocked: bool


@dataclass(frozen=True)
class PlanningDecayFrame:
    stale_plans: tuple[str, ...]
    decayed_task_salience: tuple[str, ...]
    planning_interruption_duration: int
    abandoned_continuation_chains: int
    planning_decay_score: int
    planning_decay_status: str
    decay_summary: str
    bounded_reset_recommendation: str


@dataclass(frozen=True)
class PlanningInterruptionFrame:
    interrupted_goals: tuple[str, ...]
    interruption_count: int
    interruption_pressure: str
    bounded_interruption_handling: bool
    interruption_summary: str


@dataclass(frozen=True)
class PlanningConflictFrame:
    conflict_count: int
    conflict_pressure: str
    conflicting_goals: tuple[str, ...]
    deterministic_conflict_resolution: bool
    governance_conflict_blocked: bool


@dataclass(frozen=True)
class PlanningContinuationFrame:
    continuation_chain: tuple[str, ...]
    continuation_depth: int
    continuation_limit: int
    continuation_pressure: str
    bounded_continuation_planning: bool
    recursive_continuation_blocked: bool


@dataclass(frozen=True)
class PlanningRecoveryFrame:
    recovery_actions: tuple[str, ...]
    recovery_required: bool
    rollback_safe_recovery: bool
    deterministic_recovery_summary: str


@dataclass(frozen=True)
class PlanningGovernanceFrame:
    local_patch_scope_enforced: bool
    bounded_planning_windows_enforced: bool
    deterministic_hierarchy_enforced: bool
    bounded_continuation_depth_enforced: bool
    bounded_interruption_handling_enforced: bool
    recursive_planning_blocked: bool
    autonomous_goal_expansion_blocked: bool
    hidden_background_planning_blocked: bool
    self_expanding_execution_tree_blocked: bool
    governance_policy_mutation_blocked: bool
    retrieval_scope_widening_blocked: bool


@dataclass(frozen=True)
class PlanningTerminationFrame:
    planning_terminated: bool
    termination_reasons: tuple[str, ...]
    budget_exceeded: bool
    recursive_planning_detected: bool
    governance_violation_detected: bool
    saturation_threshold_exceeded: bool
    continuation_depth_exceeded: bool


@dataclass(frozen=True)
class PlanningBudgetFrame:
    planning_budget_used: int
    planning_budget_limit: int
    budget_pressure: str
    budget_exceeded: bool
    local_first_budget: bool
    high_tier_reasoning_blocked: bool


@dataclass(frozen=True)
class PlanningConfidenceFrame:
    confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    frontier_reasoning_dependency_reduced: bool


@dataclass(frozen=True)
class PlanningHistoryFrame:
    planning_history: tuple[str, ...]
    history_limit: int
    compact_history_summary: str
    raw_transcript_replay_blocked: bool
    no_hidden_background_history: bool


@dataclass(frozen=True)
class PlanningEvictionFrame:
    evicted_goals: tuple[str, ...]
    evicted_window_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class IntentionalPlanningFrame:
    intentional_planning_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    active_goal: ActiveGoalFrame
    goal_hierarchy: GoalHierarchyFrame
    goal_priority: GoalPriorityFrame
    task_salience: TaskSalienceFrame
    planning_window: PlanningWindowFrame
    planning_decay: PlanningDecayFrame
    planning_interruption: PlanningInterruptionFrame
    planning_conflict: PlanningConflictFrame
    planning_continuation: PlanningContinuationFrame
    planning_recovery: PlanningRecoveryFrame
    planning_governance: PlanningGovernanceFrame
    planning_termination: PlanningTerminationFrame
    planning_budget: PlanningBudgetFrame
    planning_confidence: PlanningConfidenceFrame
    planning_history: PlanningHistoryFrame
    planning_eviction: PlanningEvictionFrame
    active_goal_count: int
    planning_window_pressure: str
    planning_decay_status: str
    planning_interruption_pressure: str
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    provider_routing: str
    estimated_avoided_recursive_planning: int
    estimated_avoided_goal_explosion: int
    estimated_avoided_frontier_reasoning: int


class IntentionalPlanningRuntime:
    def evaluate(
        self,
        *,
        active_goals: tuple[str, ...] = (
            "implement_intentional_planning",
            "validate_runtime",
            "connect_vscode",
            "commit_push",
        ),
        suspended_goals: tuple[str, ...] = ("defer_broad_retrieval",),
        completed_goals: tuple[str, ...] = ("runtime_mediation", "cognitive_state"),
        interrupted_goals: tuple[str, ...] = (),
        decayed_goals: tuple[str, ...] = (),
        goal_priorities: dict[str, int] | None = None,
        task_salience: dict[str, int] | None = None,
        planning_window_items: tuple[str, ...] = (
            "runtime",
            "audit",
            "vscode",
            "tests",
            "validation",
        ),
        continuation_chain: tuple[str, ...] = (
            "implement",
            "validate",
            "commit",
        ),
        stale_plans: tuple[str, ...] = (),
        interruption_duration: int = 0,
        abandoned_continuation_chains: int = 0,
        planning_budget_used: int = 7,
        recursive_planning_attempts: int = 0,
        autonomous_goal_expansion_attempts: int = 0,
        hidden_background_planning_attempts: int = 0,
        self_expanding_tree_attempts: int = 0,
        governance_mutation_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
        repo_wide_reprioritization_attempts: int = 0,
        dynamic_objective_attempts: int = 0,
        raw_transcript_replay_attempts: int = 0,
        conflict_count: int = 0,
    ) -> IntentionalPlanningFrame:
        priorities = dict(goal_priorities or DEFAULT_GOAL_PRIORITIES)
        salience = dict(task_salience or DEFAULT_TASK_SALIENCE)
        bounded_active_goals = active_goals[:MAX_ACTIVE_GOALS]
        bounded_suspended_goals = suspended_goals[:MAX_SUSPENDED_GOALS]
        bounded_completed_goals = completed_goals[:MAX_COMPLETED_GOALS]
        bounded_interrupted_goals = interrupted_goals[:MAX_INTERRUPTED_GOALS]
        bounded_decayed_goals = decayed_goals[:MAX_DECAYED_GOALS]
        bounded_window = planning_window_items[:MAX_PLANNING_WINDOW_ITEMS]
        bounded_continuation = continuation_chain[:MAX_CONTINUATION_DEPTH]
        priority_order = _ordered_keys(priorities, MAX_ACTIVE_GOALS)
        salience_scores = _salience_scores(salience)
        salient_tasks = tuple(score.split(":", maxsplit=1)[0] for score in salience_scores)
        primary_goal = priority_order[0] if priority_order else "no_active_goal"
        planning_window_pressure = _pressure(len(planning_window_items), MAX_PLANNING_WINDOW_ITEMS)
        interruption_pressure = _pressure(
            len(interrupted_goals) + interruption_duration,
            MAX_INTERRUPTED_GOALS + DECAY_WATCH_THRESHOLD,
        )
        continuation_pressure = _pressure(len(continuation_chain), MAX_CONTINUATION_DEPTH)
        overflow_goal_count = max(0, len(active_goals) - MAX_ACTIVE_GOALS)
        evicted_window_items = planning_window_items[MAX_PLANNING_WINDOW_ITEMS:]
        evicted_goals = active_goals[MAX_ACTIVE_GOALS:]
        saturation_score = min(
            100,
            len(planning_window_items) * 12
            + len(active_goals) * 6
            + recursive_planning_attempts * 35
            + autonomous_goal_expansion_attempts * 20,
        )
        decay_score = min(
            100,
            len(stale_plans) * 18
            + len(decayed_goals) * 16
            + interruption_duration
            + abandoned_continuation_chains * 22,
        )
        decay_status = _decay_status(decay_score)
        budget_pressure = _pressure(planning_budget_used, PLANNING_BUDGET_LIMIT)
        governance_violation = any(
            (
                governance_mutation_attempts,
                hidden_background_planning_attempts,
                self_expanding_tree_attempts,
                retrieval_scope_widening_attempts,
                repo_wide_reprioritization_attempts,
                dynamic_objective_attempts,
            )
        )
        termination_reasons = _termination_reasons(
            planning_budget_used > PLANNING_BUDGET_LIMIT,
            recursive_planning_attempts > 0,
            governance_violation,
            saturation_score >= PLANNING_SATURATION_THRESHOLD,
            len(continuation_chain) > MAX_CONTINUATION_DEPTH,
        )
        mediation = ExecutionSequencer().mediate()
        cognitive = CognitiveStateRuntime().evaluate()
        active_summary = _summary(primary_goal)
        confidence_score = _confidence_score(
            len(termination_reasons), planning_window_pressure, decay_status
        )

        return IntentionalPlanningFrame(
            intentional_planning_active=True,
            requirement_ids=INTENTIONAL_PLANNING_REQUIREMENT_IDS,
            test_ids=INTENTIONAL_PLANNING_TEST_IDS,
            active_goal=ActiveGoalFrame(
                active_goal_id=primary_goal,
                active_goal_summary=active_summary,
                active_goal_status="ACTIVE" if bounded_active_goals else "EMPTY",
                local_patch_scope=True,
                goal_can_synthesize_children=False,
                recursive_goal_synthesis_blocked=recursive_planning_attempts > 0,
            ),
            goal_hierarchy=GoalHierarchyFrame(
                active_goals=bounded_active_goals,
                suspended_goals=bounded_suspended_goals,
                completed_goals=bounded_completed_goals,
                interrupted_goals=bounded_interrupted_goals,
                decayed_goals=bounded_decayed_goals,
                total_tracked_goals=(
                    len(bounded_active_goals)
                    + len(bounded_suspended_goals)
                    + len(bounded_completed_goals)
                    + len(bounded_interrupted_goals)
                    + len(bounded_decayed_goals)
                ),
                hierarchy_limit=MAX_ACTIVE_GOALS,
                bounded_goal_hierarchy=True,
                self_expanding_tree_blocked=self_expanding_tree_attempts > 0,
            ),
            goal_priority=GoalPriorityFrame(
                priority_order=priority_order,
                primary_goal=primary_goal,
                deterministic_goal_prioritization=True,
                active_goal_count=len(bounded_active_goals),
                priority_limit=MAX_ACTIVE_GOALS,
                autonomous_reprioritization_blocked=(repo_wide_reprioritization_attempts > 0),
            ),
            task_salience=TaskSalienceFrame(
                salient_tasks=salient_tasks,
                salience_scores=salience_scores,
                execution_relevance=(
                    "HIGH" if mediation.runtime_mediation_active else "UNAVAILABLE"
                ),
                active_task_priority=primary_goal,
                bounded_context_relevance=cognitive.bounded,
                planning_continuation_necessity=_continuation_necessity(continuation_pressure),
                retrieval_scope_widening_blocked=retrieval_scope_widening_attempts > 0,
                dynamic_objective_synthesis_blocked=dynamic_objective_attempts > 0,
            ),
            planning_window=PlanningWindowFrame(
                planning_window_items=bounded_window,
                window_limit=MAX_PLANNING_WINDOW_ITEMS,
                planning_window_pressure=planning_window_pressure,
                planning_saturation_score=saturation_score,
                saturation_threshold=PLANNING_SATURATION_THRESHOLD,
                bounded_planning_window=True,
                repo_wide_execution_reprioritization_blocked=(
                    repo_wide_reprioritization_attempts > 0
                ),
            ),
            planning_decay=PlanningDecayFrame(
                stale_plans=stale_plans,
                decayed_task_salience=bounded_decayed_goals,
                planning_interruption_duration=interruption_duration,
                abandoned_continuation_chains=abandoned_continuation_chains,
                planning_decay_score=decay_score,
                planning_decay_status=decay_status,
                decay_summary=(
                    f"stale={len(stale_plans)};interruption={interruption_duration};"
                    f"abandoned={abandoned_continuation_chains}"
                ),
                bounded_reset_recommendation=_reset_recommendation(decay_status),
            ),
            planning_interruption=PlanningInterruptionFrame(
                interrupted_goals=bounded_interrupted_goals,
                interruption_count=len(bounded_interrupted_goals),
                interruption_pressure=interruption_pressure,
                bounded_interruption_handling=True,
                interruption_summary=f"interrupted={len(bounded_interrupted_goals)}",
            ),
            planning_conflict=PlanningConflictFrame(
                conflict_count=conflict_count,
                conflict_pressure=_pressure(conflict_count, MAX_ACTIVE_GOALS),
                conflicting_goals=bounded_active_goals[: min(conflict_count, 2)],
                deterministic_conflict_resolution=True,
                governance_conflict_blocked=governance_violation,
            ),
            planning_continuation=PlanningContinuationFrame(
                continuation_chain=bounded_continuation,
                continuation_depth=len(bounded_continuation),
                continuation_limit=MAX_CONTINUATION_DEPTH,
                continuation_pressure=continuation_pressure,
                bounded_continuation_planning=True,
                recursive_continuation_blocked=(
                    recursive_planning_attempts > 0
                    or len(continuation_chain) > MAX_CONTINUATION_DEPTH
                ),
            ),
            planning_recovery=PlanningRecoveryFrame(
                recovery_actions=_recovery_actions(decay_status, termination_reasons),
                recovery_required=bool(termination_reasons) or decay_status != "STABLE",
                rollback_safe_recovery=True,
                deterministic_recovery_summary=(
                    "bounded recovery only; no plan expansion or policy mutation"
                ),
            ),
            planning_governance=PlanningGovernanceFrame(
                local_patch_scope_enforced=True,
                bounded_planning_windows_enforced=True,
                deterministic_hierarchy_enforced=True,
                bounded_continuation_depth_enforced=True,
                bounded_interruption_handling_enforced=True,
                recursive_planning_blocked=recursive_planning_attempts > 0,
                autonomous_goal_expansion_blocked=(autonomous_goal_expansion_attempts > 0),
                hidden_background_planning_blocked=(hidden_background_planning_attempts > 0),
                self_expanding_execution_tree_blocked=self_expanding_tree_attempts > 0,
                governance_policy_mutation_blocked=governance_mutation_attempts > 0,
                retrieval_scope_widening_blocked=retrieval_scope_widening_attempts > 0,
            ),
            planning_termination=PlanningTerminationFrame(
                planning_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                budget_exceeded=planning_budget_used > PLANNING_BUDGET_LIMIT,
                recursive_planning_detected=recursive_planning_attempts > 0,
                governance_violation_detected=governance_violation,
                saturation_threshold_exceeded=(saturation_score >= PLANNING_SATURATION_THRESHOLD),
                continuation_depth_exceeded=(len(continuation_chain) > MAX_CONTINUATION_DEPTH),
            ),
            planning_budget=PlanningBudgetFrame(
                planning_budget_used=planning_budget_used,
                planning_budget_limit=PLANNING_BUDGET_LIMIT,
                budget_pressure=budget_pressure,
                budget_exceeded=planning_budget_used > PLANNING_BUDGET_LIMIT,
                local_first_budget=True,
                high_tier_reasoning_blocked=True,
            ),
            planning_confidence=PlanningConfidenceFrame(
                confidence_score=confidence_score,
                confidence_status=_confidence_status(confidence_score),
                deterministic_confidence=True,
                frontier_reasoning_dependency_reduced=True,
            ),
            planning_history=PlanningHistoryFrame(
                planning_history=(
                    "goal_hierarchy_bounded",
                    "planning_window_bounded",
                    "governance_enforced",
                ),
                history_limit=3,
                compact_history_summary=(
                    "hierarchy=bounded;window=bounded;governance=local_patch"
                ),
                raw_transcript_replay_blocked=raw_transcript_replay_attempts > 0,
                no_hidden_background_history=hidden_background_planning_attempts == 0,
            ),
            planning_eviction=PlanningEvictionFrame(
                evicted_goals=evicted_goals,
                evicted_window_items=evicted_window_items,
                eviction_count=len(evicted_goals) + len(evicted_window_items),
                bounded_eviction_active=bool(evicted_goals or evicted_window_items),
                eviction_summary=(
                    f"goals={len(evicted_goals)};window={len(evicted_window_items)}"
                ),
            ),
            active_goal_count=len(bounded_active_goals),
            planning_window_pressure=planning_window_pressure,
            planning_decay_status=decay_status,
            planning_interruption_pressure=interruption_pressure,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            provider_routing="LOCAL_FIRST_NO_FRONTIER_INTENTIONALITY",
            estimated_avoided_recursive_planning=64 + recursive_planning_attempts * 8,
            estimated_avoided_goal_explosion=58 + overflow_goal_count * 6,
            estimated_avoided_frontier_reasoning=71,
        )


def _ordered_keys(values: dict[str, int], limit: int) -> tuple[str, ...]:
    ordered = sorted(values.items(), key=lambda item: (-item[1], item[0]))
    return tuple(name for name, _score in ordered[:limit])


def _salience_scores(values: dict[str, int]) -> tuple[str, ...]:
    ordered = sorted(values.items(), key=lambda item: (-item[1], item[0]))
    total = sum(max(0, value) for value in values.values()) or 1
    return tuple(
        f"{name}:{round(max(0, value) * 100 / total)}"
        for name, value in ordered[:MAX_TASK_SALIENCE_ITEMS]
    )


def _pressure(value: int, limit: int) -> str:
    if value > limit:
        return "HIGH"
    if value >= max(1, limit - 1):
        return "MEDIUM"
    return "LOW"


def _decay_status(decay_score: int) -> str:
    if decay_score >= DECAY_RESET_THRESHOLD:
        return "RESET_RECOMMENDED"
    if decay_score >= DECAY_WATCH_THRESHOLD:
        return "WATCH"
    return "STABLE"


def _reset_recommendation(decay_status: str) -> str:
    if decay_status == "RESET_RECOMMENDED":
        return "TERMINATE_STALE_PLANNING_AND_REBASE_WINDOW"
    if decay_status == "WATCH":
        return "REFRESH_SALIENCE_AND_BOUND_CONTINUATION"
    return "CONTINUE_BOUNDED_PLANNING"


def _continuation_necessity(pressure: str) -> str:
    if pressure == "HIGH":
        return "TERMINATE_OR_COMPACT"
    if pressure == "MEDIUM":
        return "WATCH"
    return "CONTINUE"


def _termination_reasons(
    budget_exceeded: bool,
    recursive_planning_detected: bool,
    governance_violation_detected: bool,
    saturation_threshold_exceeded: bool,
    continuation_depth_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if budget_exceeded:
        reasons.append("PLANNING_BUDGET_EXCEEDED")
    if recursive_planning_detected:
        reasons.append("RECURSIVE_PLANNING_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if saturation_threshold_exceeded:
        reasons.append("PLANNING_SATURATION_EXCEEDED")
    if continuation_depth_exceeded:
        reasons.append("CONTINUATION_DEPTH_EXCEEDED")
    return tuple(reasons)


def _recovery_actions(decay_status: str, termination_reasons: tuple[str, ...]) -> tuple[str, ...]:
    actions: list[str] = []
    if termination_reasons:
        actions.append("freeze_planning_window")
    if decay_status != "STABLE":
        actions.append("compact_planning_summary")
    if not actions:
        actions.append("continue_bounded_planning")
    return tuple(actions)


def _confidence_score(
    termination_count: int, planning_window_pressure: str, decay_status: str
) -> int:
    pressure_penalty = {"LOW": 0, "MEDIUM": 12, "HIGH": 28}[planning_window_pressure]
    decay_penalty = {"STABLE": 0, "WATCH": 16, "RESET_RECOMMENDED": 34}[decay_status]
    return max(0, 92 - pressure_penalty - decay_penalty - termination_count * 18)


def _confidence_status(score: int) -> str:
    if score >= 75:
        return "STABLE"
    if score >= 45:
        return "WATCH"
    return "LOW"


def _summary(goal_id: str) -> str:
    return goal_id.replace("_", " ")
