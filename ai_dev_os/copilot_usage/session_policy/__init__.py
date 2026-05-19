from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionState:
    context_tokens: int
    repeated_instruction_tokens: int
    task_continuity_score: float
    cache_reuse_likelihood: float
    completed_objectives: int = 0
    new_objectives: int = 0
    stale_turns: int = 0


@dataclass(frozen=True)
class SessionReuseReport:
    new_session_recommended: bool
    continue_session_recommended: bool
    compact_before_continue: bool
    fork_session_recommended: bool
    recommendation: str
    estimated_cache_benefit_tokens: int
    estimated_avoided_tokens: int
    warnings: tuple[str, ...]


class SessionCostPolicy:
    def __init__(self, *, compact_threshold_tokens: int = 12_000) -> None:
        self.compact_threshold_tokens = compact_threshold_tokens

    def evaluate(self, state: SessionState) -> SessionReuseReport:
        warnings: list[str] = []
        stable_cache = (
            state.repeated_instruction_tokens > 0 and state.cache_reuse_likelihood >= 0.65
        )
        high_context = state.context_tokens >= self.compact_threshold_tokens
        same_task = state.task_continuity_score >= 0.7 and state.new_objectives <= 1
        task_finished = state.completed_objectives > 0 and state.new_objectives > 0
        drifted_task = state.task_continuity_score < 0.35 or state.stale_turns >= 8

        if task_finished and not same_task:
            recommendation = "new_session"
            warnings.append("one_task_one_session_boundary")
        elif high_context and same_task and stable_cache:
            recommendation = "compact_before_continue"
            warnings.append("large_context_requires_compaction")
        elif high_context and not same_task:
            recommendation = "fork_session"
            warnings.append("avoid_dragging_stale_context")
        elif drifted_task:
            recommendation = "fork_session"
            warnings.append("task_continuity_low")
        else:
            recommendation = "continue_session"
            if stable_cache:
                warnings.append("cache_reuse_likely")

        estimated_cache_benefit = int(
            state.repeated_instruction_tokens * state.cache_reuse_likelihood
        )
        estimated_avoided = state.context_tokens if recommendation == "new_session" else 0
        if recommendation in {"compact_before_continue", "fork_session"}:
            estimated_avoided = max(0, state.context_tokens - self.compact_threshold_tokens // 2)

        return SessionReuseReport(
            new_session_recommended=recommendation == "new_session",
            continue_session_recommended=recommendation == "continue_session",
            compact_before_continue=recommendation == "compact_before_continue",
            fork_session_recommended=recommendation == "fork_session",
            recommendation=recommendation,
            estimated_cache_benefit_tokens=estimated_cache_benefit,
            estimated_avoided_tokens=estimated_avoided,
            warnings=tuple(warnings),
        )
