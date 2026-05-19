from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionGenerationFrame:
    session_id: str
    session_generation: int
    rollover_generation: int
    parent_session: str
    continuity_generation: int
    stale_generation: int
    active_generation: int
    full_history_replay_allowed: bool


class SessionGenerationPolicy:
    def generate(
        self,
        *,
        session_id: str,
        session_generation: int = 1,
        rollover_recommended: bool = False,
        parent_session: str = "",
        continuity_generation: int | None = None,
        stale_generation: int | None = None,
    ) -> SessionGenerationFrame:
        rollover_generation = (
            session_generation + 1 if rollover_recommended else session_generation
        )
        active_generation = rollover_generation if rollover_recommended else session_generation
        return SessionGenerationFrame(
            session_id=session_id,
            session_generation=max(1, session_generation),
            rollover_generation=max(1, rollover_generation),
            parent_session=parent_session,
            continuity_generation=continuity_generation or session_generation,
            stale_generation=stale_generation or session_generation,
            active_generation=max(1, active_generation),
            full_history_replay_allowed=False,
        )
