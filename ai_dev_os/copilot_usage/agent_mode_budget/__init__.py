from __future__ import annotations

from dataclasses import dataclass

HIGH_PRESSURE_VALUES = {"HIGH", "CRITICAL", "high", "critical"}


@dataclass(frozen=True)
class AgentModeBudget:
    max_tool_calls: int = 24
    max_repair_loops: int = 3
    max_validation_retries: int = 2
    max_context_refresh: int = 2
    max_architecture_escalation: int = 1


@dataclass(frozen=True)
class AgentLoopState:
    tool_calls: int = 0
    repair_loops: int = 0
    validation_retries: int = 0
    context_refreshes: int = 0
    architecture_escalations: int = 0
    pressure: str = "NORMAL"


@dataclass(frozen=True)
class AgentLoopReport:
    stop_required: bool
    patch_only_mode: bool
    no_tier2: bool
    no_council_expansion: bool
    stop_reasons: tuple[str, ...]
    remaining_tool_calls: int
    warnings: tuple[str, ...]


class AgentModeBudgetGuard:
    def __init__(self, budget: AgentModeBudget | None = None) -> None:
        self.budget = budget or AgentModeBudget()

    def evaluate(self, state: AgentLoopState) -> AgentLoopReport:
        reasons: list[str] = []
        if state.tool_calls >= self.budget.max_tool_calls:
            reasons.append("max_tool_calls_reached")
        if state.repair_loops >= self.budget.max_repair_loops:
            reasons.append("max_repair_loops_reached")
        if state.validation_retries >= self.budget.max_validation_retries:
            reasons.append("max_validation_retries_reached")
        if state.context_refreshes >= self.budget.max_context_refresh:
            reasons.append("max_context_refresh_reached")
        if state.architecture_escalations >= self.budget.max_architecture_escalation:
            reasons.append("max_architecture_escalation_reached")

        high_pressure = state.pressure in HIGH_PRESSURE_VALUES
        if high_pressure:
            reasons.append("high_pressure_stop_and_report")

        remaining = max(0, self.budget.max_tool_calls - state.tool_calls)
        return AgentLoopReport(
            stop_required=bool(reasons),
            patch_only_mode=high_pressure,
            no_tier2=high_pressure,
            no_council_expansion=high_pressure or state.architecture_escalations > 0,
            stop_reasons=tuple(dict.fromkeys(reasons)),
            remaining_tool_calls=remaining,
            warnings=("agent_loop_expansion_suppressed",) if reasons else (),
        )
