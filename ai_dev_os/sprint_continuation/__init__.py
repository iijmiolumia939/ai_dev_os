from __future__ import annotations

from dataclasses import dataclass

SPRINT_CONTINUATION_REQUIREMENT_IDS = tuple(
    f"FR-SPRINTCONTINUATION-{index:02d}" for index in range(1, 13)
) + ("NFR-ARCH-SPRINTCONTINUATION-01", "NFR-SEC-SPRINTCONTINUATION-01")
SPRINT_CONTINUATION_TEST_IDS = tuple(f"TC-SPRINTCONTINUATION-{index:02d}" for index in range(1, 9))

MAX_NEXT_SPRINT_OPTIONS = 5
MAX_BACKLOG_ITEMS = 5
MAX_DEPENDENCY_ITEMS = 4
MAX_REGRESSION_ITEMS = 4
MAX_OPERATIONAL_CARRYOVER_ITEMS = 4
MAX_CONTINUATION_HISTORY = 5
MAX_CONTINUATION_DEPTH = 2
CONTINUATION_BUDGET_LIMIT = 12
REGRESSION_CONTINUATION_THRESHOLD = 70
DEPENDENCY_PRESSURE_THRESHOLD = 72
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_CANDIDATE_SPRINTS = (
    "stabilize-runtime-audit",
    "extend-vscode-visibility",
    "close-regression-carryover",
)
DEFAULT_BACKLOG_ITEMS = (
    "audit-projection-gap",
    "extension-command-visibility",
    "targeted-test-coverage",
)
DEFAULT_DEPENDENCY_ITEMS = (
    "runtime_audit",
    "sprint_loop",
    "runtime_orchestrator",
)
DEFAULT_REGRESSION_ITEMS = (
    "targeted-pytest",
    "runtime-audit",
)
DEFAULT_OPERATIONAL_CARRYOVER_ITEMS = (
    "validation-sequence",
    "commit-scope",
    "ci-observation",
)
DEFAULT_CONTINUATION_HISTORY = (
    "inspect",
    "select",
    "implement",
    "validate",
    "handoff",
)


@dataclass(frozen=True)
class ContinuationSelectionFrame:
    continuation_selection_active: bool
    candidate_sprints: tuple[str, ...]
    selected_sprint: str
    candidate_limit: int
    selection_overflow_blocked: bool
    continuation_selection_score: int
    deterministic_selection_summary: str
    bounded_selection_recommendation: str


@dataclass(frozen=True)
class BacklogPriorityFrame:
    backlog_priority_active: bool
    backlog_items: tuple[str, ...]
    backlog_item_limit: int
    backlog_overflow_blocked: bool
    backlog_continuation_score: int
    deterministic_backlog_summary: str
    bounded_backlog_recommendation: str


@dataclass(frozen=True)
class DependencyContinuationFrame:
    dependency_continuation_active: bool
    dependency_items: tuple[str, ...]
    dependency_item_limit: int
    dependency_pressure: int
    dependency_overflow_blocked: bool
    dependency_continuation_score: int
    deterministic_dependency_summary: str
    bounded_dependency_recommendation: str


@dataclass(frozen=True)
class RegressionContinuationFrame:
    regression_continuation_active: bool
    regression_items: tuple[str, ...]
    regression_item_limit: int
    regression_pressure: int
    regression_overflow_blocked: bool
    regression_continuation_score: int
    deterministic_regression_summary: str
    bounded_regression_recommendation: str


@dataclass(frozen=True)
class OperationalCarryoverFrame:
    operational_carryover_active: bool
    operational_items: tuple[str, ...]
    operational_item_limit: int
    operational_overflow_blocked: bool
    operational_carryover_score: int
    deterministic_operational_summary: str
    bounded_operational_recommendation: str


@dataclass(frozen=True)
class ContinuationGovernanceFrame:
    continuation_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_selection_enforced: bool
    bounded_backlog_enforced: bool
    bounded_dependency_enforced: bool
    bounded_regression_enforced: bool
    recursive_continuation_blocked: bool
    hidden_continuation_execution_blocked: bool
    autonomous_branch_mutation_blocked: bool
    autonomous_governance_mutation_blocked: bool
    self_expanding_sprint_chain_blocked: bool
    frontier_planning_blocked: bool


@dataclass(frozen=True)
class ContinuationBudgetFrame:
    continuation_budget_active: bool
    continuation_budget_used: int
    continuation_budget_limit: int
    continuation_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class ContinuationTerminationFrame:
    continuation_termination_active: bool
    continuation_terminated: bool
    termination_reasons: tuple[str, ...]
    continuation_budget_exceeded: bool
    recursive_continuation_detected: bool
    governance_violation_detected: bool
    dependency_pressure_threshold_exceeded: bool
    regression_continuation_threshold_exceeded: bool
    continuation_depth_exceeded: bool


@dataclass(frozen=True)
class ContinuationHistoryFrame:
    continuation_history_active: bool
    continuation_history: tuple[str, ...]
    continuation_history_limit: int
    compact_continuation_history_summary: str
    continuation_history_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class ContinuationConfidenceFrame:
    continuation_confidence_active: bool
    continuation_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    next_sprint_confidence: bool


@dataclass(frozen=True)
class ContinuationEvictionFrame:
    continuation_eviction_active: bool
    evicted_candidate_sprints: tuple[str, ...]
    evicted_backlog_items: tuple[str, ...]
    evicted_dependency_items: tuple[str, ...]
    evicted_regression_items: tuple[str, ...]
    evicted_operational_items: tuple[str, ...]
    evicted_history_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class SprintContinuationFrame:
    sprint_continuation_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    selection: ContinuationSelectionFrame
    backlog: BacklogPriorityFrame
    dependency: DependencyContinuationFrame
    regression: RegressionContinuationFrame
    operational: OperationalCarryoverFrame
    governance: ContinuationGovernanceFrame
    budget: ContinuationBudgetFrame
    termination: ContinuationTerminationFrame
    history: ContinuationHistoryFrame
    confidence: ContinuationConfidenceFrame
    eviction: ContinuationEvictionFrame
    continuation_selection_score: int
    backlog_continuation_score: int
    dependency_continuation_score: int
    regression_continuation_score: int
    operational_carryover_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    sprint_continuation_mode: str
    estimated_avoided_continuation_drift: int
    estimated_avoided_recursive_sprinting: int
    estimated_avoided_frontier_planning: int


class SprintContinuationRuntime:
    def evaluate(
        self,
        *,
        candidate_sprints: tuple[str, ...] = DEFAULT_CANDIDATE_SPRINTS,
        backlog_items: tuple[str, ...] = DEFAULT_BACKLOG_ITEMS,
        dependency_items: tuple[str, ...] = DEFAULT_DEPENDENCY_ITEMS,
        regression_items: tuple[str, ...] = DEFAULT_REGRESSION_ITEMS,
        operational_carryover_items: tuple[str, ...] = DEFAULT_OPERATIONAL_CARRYOVER_ITEMS,
        continuation_history_items: tuple[str, ...] = DEFAULT_CONTINUATION_HISTORY,
        continuation_depth: int = 1,
        dependency_pressure: int = 18,
        regression_pressure: int = 16,
        continuation_budget_used: int = 7,
        recursive_continuation_attempts: int = 0,
        hidden_continuation_execution_attempts: int = 0,
        autonomous_branch_mutation_attempts: int = 0,
        autonomous_governance_mutation_attempts: int = 0,
        self_expanding_sprint_chain_attempts: int = 0,
        frontier_planning_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> SprintContinuationFrame:
        bounded_candidates = candidate_sprints[:MAX_NEXT_SPRINT_OPTIONS]
        bounded_backlog = backlog_items[:MAX_BACKLOG_ITEMS]
        bounded_dependencies = dependency_items[:MAX_DEPENDENCY_ITEMS]
        bounded_regressions = regression_items[:MAX_REGRESSION_ITEMS]
        bounded_operational = operational_carryover_items[:MAX_OPERATIONAL_CARRYOVER_ITEMS]
        bounded_history = continuation_history_items[:MAX_CONTINUATION_HISTORY]

        evicted_candidates = candidate_sprints[MAX_NEXT_SPRINT_OPTIONS:]
        evicted_backlog = backlog_items[MAX_BACKLOG_ITEMS:]
        evicted_dependencies = dependency_items[MAX_DEPENDENCY_ITEMS:]
        evicted_regressions = regression_items[MAX_REGRESSION_ITEMS:]
        evicted_operational = operational_carryover_items[MAX_OPERATIONAL_CARRYOVER_ITEMS:]
        evicted_history = continuation_history_items[MAX_CONTINUATION_HISTORY:]
        eviction_count = sum(
            len(items)
            for items in (
                evicted_candidates,
                evicted_backlog,
                evicted_dependencies,
                evicted_regressions,
                evicted_operational,
                evicted_history,
            )
        )

        selected_sprint = (
            bounded_candidates[0] if bounded_candidates else "NO_CONTINUATION_SELECTED"
        )
        dependency_exceeded = dependency_pressure >= DEPENDENCY_PRESSURE_THRESHOLD
        regression_exceeded = regression_pressure >= REGRESSION_CONTINUATION_THRESHOLD
        depth_exceeded = continuation_depth > MAX_CONTINUATION_DEPTH
        budget_exceeded = continuation_budget_used > CONTINUATION_BUDGET_LIMIT
        recursive_detected = recursive_continuation_attempts > 0
        governance_violation = any(
            (
                hidden_continuation_execution_attempts,
                autonomous_branch_mutation_attempts,
                autonomous_governance_mutation_attempts,
                self_expanding_sprint_chain_attempts,
                frontier_planning_attempts,
            )
        )

        termination_reasons: list[str] = []
        if budget_exceeded:
            termination_reasons.append("CONTINUATION_BUDGET_EXCEEDED")
        if recursive_detected:
            termination_reasons.append("RECURSIVE_CONTINUATION_DETECTED")
        if governance_violation:
            termination_reasons.append("CONTINUATION_GOVERNANCE_VIOLATION_DETECTED")
        if dependency_exceeded:
            termination_reasons.append("DEPENDENCY_PRESSURE_THRESHOLD_EXCEEDED")
        if regression_exceeded:
            termination_reasons.append("REGRESSION_CONTINUATION_THRESHOLD_EXCEEDED")
        if depth_exceeded:
            termination_reasons.append("CONTINUATION_DEPTH_EXCEEDED")

        backlog_continuation_score = _clamp_score(94 - len(evicted_backlog) * 6)
        dependency_continuation_score = _clamp_score(
            92 - dependency_pressure // 2 - len(evicted_dependencies) * 5
        )
        regression_continuation_score = _clamp_score(
            91 - regression_pressure // 2 - len(evicted_regressions) * 5
        )
        operational_carryover_score = _clamp_score(90 - len(evicted_operational) * 6)
        continuation_selection_score = _clamp_score(
            min(
                backlog_continuation_score,
                dependency_continuation_score,
                regression_continuation_score,
                operational_carryover_score,
            )
            - int(recursive_detected) * 18
            - int(governance_violation) * 18
            - int(depth_exceeded) * 12
            - int(budget_exceeded) * 12
        )
        confidence_score = _clamp_score(
            continuation_selection_score - len(termination_reasons) * 7
        )

        return SprintContinuationFrame(
            sprint_continuation_active=True,
            requirement_ids=SPRINT_CONTINUATION_REQUIREMENT_IDS,
            test_ids=SPRINT_CONTINUATION_TEST_IDS,
            selection=ContinuationSelectionFrame(
                continuation_selection_active=True,
                candidate_sprints=bounded_candidates,
                selected_sprint=selected_sprint,
                candidate_limit=MAX_NEXT_SPRINT_OPTIONS,
                selection_overflow_blocked=bool(evicted_candidates),
                continuation_selection_score=continuation_selection_score,
                deterministic_selection_summary=(
                    f"selected={selected_sprint};candidates={len(bounded_candidates)}"
                ),
                bounded_selection_recommendation=(
                    "SELECT_BOUNDED_NEXT_SPRINT"
                    if not termination_reasons
                    else "TERMINATE_AND_COMPACT_CONTINUATION"
                ),
            ),
            backlog=BacklogPriorityFrame(
                backlog_priority_active=True,
                backlog_items=bounded_backlog,
                backlog_item_limit=MAX_BACKLOG_ITEMS,
                backlog_overflow_blocked=bool(evicted_backlog),
                backlog_continuation_score=backlog_continuation_score,
                deterministic_backlog_summary=";".join(bounded_backlog),
                bounded_backlog_recommendation="CARRY_BOUNDED_BACKLOG_ONLY",
            ),
            dependency=DependencyContinuationFrame(
                dependency_continuation_active=True,
                dependency_items=bounded_dependencies,
                dependency_item_limit=MAX_DEPENDENCY_ITEMS,
                dependency_pressure=dependency_pressure,
                dependency_overflow_blocked=bool(evicted_dependencies),
                dependency_continuation_score=dependency_continuation_score,
                deterministic_dependency_summary=";".join(bounded_dependencies),
                bounded_dependency_recommendation=(
                    "STABILIZE_DEPENDENCIES_BEFORE_CONTINUATION"
                    if dependency_exceeded
                    else "CONTINUE_WITH_STABLE_DEPENDENCIES"
                ),
            ),
            regression=RegressionContinuationFrame(
                regression_continuation_active=True,
                regression_items=bounded_regressions,
                regression_item_limit=MAX_REGRESSION_ITEMS,
                regression_pressure=regression_pressure,
                regression_overflow_blocked=bool(evicted_regressions),
                regression_continuation_score=regression_continuation_score,
                deterministic_regression_summary=";".join(bounded_regressions),
                bounded_regression_recommendation=(
                    "STABILIZE_REGRESSION_BEFORE_NEXT_SPRINT"
                    if regression_exceeded
                    else "REGRESSION_CARRYOVER_VISIBLE"
                ),
            ),
            operational=OperationalCarryoverFrame(
                operational_carryover_active=True,
                operational_items=bounded_operational,
                operational_item_limit=MAX_OPERATIONAL_CARRYOVER_ITEMS,
                operational_overflow_blocked=bool(evicted_operational),
                operational_carryover_score=operational_carryover_score,
                deterministic_operational_summary=";".join(bounded_operational),
                bounded_operational_recommendation="PRESERVE_OPERATIONAL_HANDOFF_ONLY",
            ),
            governance=ContinuationGovernanceFrame(
                continuation_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_selection_enforced=True,
                bounded_backlog_enforced=True,
                bounded_dependency_enforced=True,
                bounded_regression_enforced=True,
                recursive_continuation_blocked=True,
                hidden_continuation_execution_blocked=True,
                autonomous_branch_mutation_blocked=True,
                autonomous_governance_mutation_blocked=True,
                self_expanding_sprint_chain_blocked=True,
                frontier_planning_blocked=True,
            ),
            budget=ContinuationBudgetFrame(
                continuation_budget_active=True,
                continuation_budget_used=continuation_budget_used,
                continuation_budget_limit=CONTINUATION_BUDGET_LIMIT,
                continuation_budget_exceeded=budget_exceeded,
                budget_pressure=_pressure_label(
                    continuation_budget_used, CONTINUATION_BUDGET_LIMIT
                ),
            ),
            termination=ContinuationTerminationFrame(
                continuation_termination_active=True,
                continuation_terminated=bool(termination_reasons),
                termination_reasons=tuple(termination_reasons),
                continuation_budget_exceeded=budget_exceeded,
                recursive_continuation_detected=recursive_detected,
                governance_violation_detected=governance_violation,
                dependency_pressure_threshold_exceeded=dependency_exceeded,
                regression_continuation_threshold_exceeded=regression_exceeded,
                continuation_depth_exceeded=depth_exceeded,
            ),
            history=ContinuationHistoryFrame(
                continuation_history_active=True,
                continuation_history=bounded_history,
                continuation_history_limit=MAX_CONTINUATION_HISTORY,
                compact_continuation_history_summary=(
                    f"history={len(bounded_history)};continuation=bounded"
                ),
                continuation_history_overflow_blocked=bool(evicted_history),
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            confidence=ContinuationConfidenceFrame(
                continuation_confidence_active=True,
                continuation_confidence_score=confidence_score,
                confidence_status=_confidence_status(confidence_score),
                deterministic_confidence=True,
                next_sprint_confidence=confidence_score >= 70,
            ),
            eviction=ContinuationEvictionFrame(
                continuation_eviction_active=True,
                evicted_candidate_sprints=evicted_candidates,
                evicted_backlog_items=evicted_backlog,
                evicted_dependency_items=evicted_dependencies,
                evicted_regression_items=evicted_regressions,
                evicted_operational_items=evicted_operational,
                evicted_history_items=evicted_history,
                eviction_count=eviction_count,
                bounded_eviction_active=eviction_count > 0,
                eviction_summary=f"evicted={eviction_count}",
            ),
            continuation_selection_score=continuation_selection_score,
            backlog_continuation_score=backlog_continuation_score,
            dependency_continuation_score=dependency_continuation_score,
            regression_continuation_score=regression_continuation_score,
            operational_carryover_score=operational_carryover_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            sprint_continuation_mode="LOCAL_PATCH_BOUNDED_SPRINT_CONTINUATION",
            estimated_avoided_continuation_drift=2100 + eviction_count * 80,
            estimated_avoided_recursive_sprinting=1800 + recursive_continuation_attempts * 220,
            estimated_avoided_frontier_planning=2400 + len(bounded_candidates) * 90,
        )


def _clamp_score(value: int) -> int:
    return max(MIN_SCORE, min(MAX_SCORE, value))


def _pressure_label(used: int, limit: int) -> str:
    if used > limit:
        return "OVER_BUDGET"
    if used >= limit - 2:
        return "HIGH"
    if used >= limit // 2:
        return "MEDIUM"
    return "LOW"


def _confidence_status(score: int) -> str:
    if score >= 80:
        return "CONTINUATION_READY"
    if score >= 60:
        return "CONTINUATION_GUARDED"
    return "CONTINUATION_TERMINATION_REQUIRED"
