from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.providers.provider_telemetry import ProviderTelemetryFrame
from ai_dev_os.retrieval.retrieval_scaling import RetrievalScalingFrame
from ai_dev_os.session_lifecycle.architecture_isolation import ArchitectureIsolationFrame
from ai_dev_os.session_lifecycle.cache_aware_session import CacheAwareSessionFrame
from ai_dev_os.session_lifecycle.session_rollover import SessionRolloverFrame
from ai_dev_os.session_lifecycle.stale_context_detection import StaleContextReport


@dataclass(frozen=True)
class SessionDecisionFrame:
    continue_current_session: bool
    compact_then_continue: bool
    fork_new_session: bool
    architecture_session_required: bool
    stop_and_close_session: bool
    recommended_next_action: str
    reasons: tuple[str, ...]
    estimated_avoided_tokens: int


class SessionDecisionPolicy:
    def decide(
        self,
        *,
        rollover: SessionRolloverFrame,
        stale: StaleContextReport,
        cache: CacheAwareSessionFrame,
        architecture: ArchitectureIsolationFrame,
        provider_telemetry: ProviderTelemetryFrame | None = None,
        retrieval_scaling: RetrievalScalingFrame | None = None,
    ) -> SessionDecisionFrame:
        reasons: list[str] = []
        if architecture.isolated_session_required or cache.architecture_session_required:
            action = "architecture_session_required"
            reasons.append("architecture_isolation")
        elif rollover.rollover_recommended or stale.recommended_bundle_refresh:
            action = "fork_new_session"
            reasons.append("rollover_or_stale_context")
        elif cache.compact_then_continue:
            action = "compact_then_continue"
            reasons.append("cache_reuse_requires_compaction")
        elif cache.fork_session:
            action = "fork_new_session"
            reasons.append("cache_policy_fork")
        else:
            action = "continue_current_session"
            reasons.append("bounded_continuation_allowed")

        if provider_telemetry and provider_telemetry.fallback_frequency > 0:
            reasons.append("provider_fallback_observed")
        if retrieval_scaling and retrieval_scaling.summary_only_mode:
            reasons.append("retrieval_summary_only_mode")
        stop = action in {"architecture_session_required", "fork_new_session"}
        return SessionDecisionFrame(
            continue_current_session=action == "continue_current_session",
            compact_then_continue=action == "compact_then_continue",
            fork_new_session=action == "fork_new_session",
            architecture_session_required=action == "architecture_session_required",
            stop_and_close_session=stop,
            recommended_next_action=action,
            reasons=tuple(dict.fromkeys(reasons)),
            estimated_avoided_tokens=rollover.estimated_avoided_tokens
            + int(stale.stale_context_ratio * 10_000),
        )
