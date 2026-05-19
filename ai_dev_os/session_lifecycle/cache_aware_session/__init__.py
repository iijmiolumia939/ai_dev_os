from __future__ import annotations

from dataclasses import dataclass

HIGH_PRESSURE_VALUES = {"HIGH", "CRITICAL", "high", "critical"}


@dataclass(frozen=True)
class CacheAwareSessionFrame:
    cache_reuse_probability: float
    repeated_instruction_stability: float
    context_freshness: float
    retrieval_overlap: float
    prompt_compactness: float
    continue_session: bool
    fork_session: bool
    compact_then_continue: bool
    architecture_session_required: bool
    recommended_session_action: str
    warnings: tuple[str, ...]


class CacheAwareSessionPolicy:
    def evaluate(
        self,
        *,
        cache_reuse_probability: float,
        repeated_instruction_stability: float,
        context_freshness: float,
        retrieval_overlap: float,
        prompt_compactness: float,
        pressure: str = "NORMAL",
        architecture_scope: bool = False,
    ) -> CacheAwareSessionFrame:
        warnings: list[str] = []
        high_pressure = pressure in HIGH_PRESSURE_VALUES
        bounded_cache_value = (
            cache_reuse_probability >= 0.65
            and repeated_instruction_stability >= 0.7
            and context_freshness >= 0.55
            and retrieval_overlap >= 0.45
            and prompt_compactness >= 0.55
        )
        stale_or_drifted = context_freshness < 0.4 or retrieval_overlap < 0.3

        if architecture_scope:
            action = "architecture_session_required"
            warnings.append("architecture_context_must_be_isolated")
        elif high_pressure and bounded_cache_value:
            action = "compact_then_continue"
            warnings.append("high_pressure_requires_compaction")
        elif high_pressure or stale_or_drifted:
            action = "fork_session"
            warnings.append("unbounded_session_continuation_blocked")
        elif bounded_cache_value:
            action = "continue_session"
            warnings.append("cache_reuse_with_bounded_context")
        else:
            action = "compact_then_continue"
            warnings.append("compact_before_cache_reuse")

        return CacheAwareSessionFrame(
            cache_reuse_probability=round(cache_reuse_probability, 4),
            repeated_instruction_stability=round(repeated_instruction_stability, 4),
            context_freshness=round(context_freshness, 4),
            retrieval_overlap=round(retrieval_overlap, 4),
            prompt_compactness=round(prompt_compactness, 4),
            continue_session=action == "continue_session",
            fork_session=action == "fork_session",
            compact_then_continue=action == "compact_then_continue",
            architecture_session_required=action == "architecture_session_required",
            recommended_session_action=action,
            warnings=tuple(warnings),
        )
