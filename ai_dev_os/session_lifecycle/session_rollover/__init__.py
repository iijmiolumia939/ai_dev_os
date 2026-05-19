from __future__ import annotations

from dataclasses import dataclass

HIGH_RETRIEVAL_PRESSURE = {"HIGH", "CRITICAL", "high", "critical"}


@dataclass(frozen=True)
class SessionRolloverFrame:
    session_age: int
    estimated_context_tokens: int
    stale_context_ratio: float
    retrieval_pressure: str
    cache_reuse_probability: float
    rollover_recommended: bool
    compact_bundle_required: bool
    architecture_isolation_required: bool
    recommended_session_action: str
    estimated_avoided_tokens: int
    triggers: tuple[str, ...]


class SessionRolloverPolicy:
    def __init__(
        self,
        *,
        max_session_age: int = 5,
        max_context_tokens: int = 16_000,
        stale_ratio_threshold: float = 0.35,
    ) -> None:
        self.max_session_age = max_session_age
        self.max_context_tokens = max_context_tokens
        self.stale_ratio_threshold = stale_ratio_threshold

    def evaluate(
        self,
        *,
        session_age: int,
        estimated_context_tokens: int,
        stale_context_ratio: float,
        retrieval_pressure: str,
        cache_reuse_probability: float,
        sprint_boundary: bool = False,
        architecture_escalation: bool = False,
    ) -> SessionRolloverFrame:
        triggers: list[str] = []
        if sprint_boundary:
            triggers.append("sprint_boundary")
        if session_age >= self.max_session_age:
            triggers.append("session_age_limit")
        if estimated_context_tokens >= self.max_context_tokens:
            triggers.append("context_growth")
        if stale_context_ratio >= self.stale_ratio_threshold:
            triggers.append("stale_history_pressure")
        if retrieval_pressure in HIGH_RETRIEVAL_PRESSURE:
            triggers.append("retrieval_pressure")
        if architecture_escalation:
            triggers.append("architecture_escalation")

        high_pressure = retrieval_pressure in HIGH_RETRIEVAL_PRESSURE
        rollover = bool(triggers) and (
            sprint_boundary
            or high_pressure
            or architecture_escalation
            or estimated_context_tokens >= self.max_context_tokens
            or stale_context_ratio >= self.stale_ratio_threshold
        )
        compact_required = rollover or estimated_context_tokens >= self.max_context_tokens // 2
        architecture_required = architecture_escalation or "architecture_escalation" in triggers

        if architecture_required:
            action = "isolate_architecture_session"
        elif rollover:
            action = "rollover_with_compact_bundle"
        elif compact_required and cache_reuse_probability >= 0.65:
            action = "compact_then_continue"
        else:
            action = "continue_bounded_session"

        avoided_tokens = 0
        if rollover:
            avoided_tokens = max(0, estimated_context_tokens - 2_400)
        elif compact_required:
            avoided_tokens = max(0, estimated_context_tokens - self.max_context_tokens // 2)

        return SessionRolloverFrame(
            session_age=session_age,
            estimated_context_tokens=estimated_context_tokens,
            stale_context_ratio=round(stale_context_ratio, 4),
            retrieval_pressure=retrieval_pressure,
            cache_reuse_probability=round(cache_reuse_probability, 4),
            rollover_recommended=rollover,
            compact_bundle_required=compact_required,
            architecture_isolation_required=architecture_required,
            recommended_session_action=action,
            estimated_avoided_tokens=avoided_tokens,
            triggers=tuple(dict.fromkeys(triggers)),
        )
