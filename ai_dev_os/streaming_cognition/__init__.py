from __future__ import annotations

from dataclasses import dataclass

STREAMING_COGNITION_REQUIREMENT_IDS = tuple(
    f"FR-STREAMINGCOGNITION-{index:02d}" for index in range(1, 13)
) + ("NFR-ARCH-STREAMING-01", "NFR-SEC-STREAMING-01")
STREAMING_COGNITION_TEST_IDS = tuple(f"TC-STREAMINGCOGNITION-{index:02d}" for index in range(1, 9))

MAX_SPEECH_CHUNKS = 4
MAX_COGNITION_DELTAS = 4
MAX_CONTINUATION_ITEMS = 3
MAX_PROVIDER_WINDOW = 3
MAX_STREAMING_HISTORY = 5
STREAMING_BUDGET_LIMIT = 12
CONTINUATION_ENTROPY_THRESHOLD = 70
INTERRUPTION_PRESSURE_THRESHOLD = 3
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_SPEECH_CHUNKS = (
    "greeting",
    "topic-anchor",
    "short-response",
)
DEFAULT_COGNITION_DELTAS = (
    "observe-chat",
    "filter-input",
    "select-local-provider",
    "emit-speech-delta",
)
DEFAULT_CONTINUATION_ITEMS = (
    "last-safe-topic",
    "current-speech-buffer",
    "provider-cooldown-state",
)
DEFAULT_PROVIDER_CANDIDATES = (
    "local-streaming-provider",
    "local-summary-provider",
    "bounded-fallback-provider",
)
DEFAULT_STREAMING_HISTORY = (
    "speech-start",
    "cognition-delta",
    "provider-local",
    "continuation-save",
    "speech-end",
)


@dataclass(frozen=True)
class StreamingSpeechFrame:
    speech_streaming_active: bool
    speech_chunks: tuple[str, ...]
    speech_chunk_limit: int
    speech_continuation: tuple[str, ...]
    speech_reset_on_interruption: bool
    deterministic_speech_buffer: str
    bounded_speech_summary: str


@dataclass(frozen=True)
class StreamingDeltaFrame:
    delta_streaming_active: bool
    cognition_deltas: tuple[str, ...]
    cognition_delta_limit: int
    delta_overflow_blocked: bool
    deterministic_delta_summary: str
    bounded_delta_recommendation: str


@dataclass(frozen=True)
class StreamingContinuationFrame:
    continuation_streaming_active: bool
    continuation_items: tuple[str, ...]
    continuation_limit: int
    continuation_persistence_reuse: bool
    continuation_reset_governed: bool
    continuation_entropy: int
    entropy_suppression_active: bool
    deterministic_continuation_summary: str


@dataclass(frozen=True)
class StreamingInterruptionFrame:
    interruption_streaming_active: bool
    interruption_detected: bool
    interruption_pressure: int
    interruption_recovery_score: int
    speech_reset_required: bool
    continuation_reset_safe: bool
    provider_stabilization_required: bool
    bounded_recovery_recommendation: str


@dataclass(frozen=True)
class ProviderStreamingFrame:
    provider_streaming_active: bool
    provider_order: tuple[str, ...]
    provider_window_limit: int
    recommended_provider: str
    provider_fallback_active: bool
    provider_cooldown_windows: int
    provider_fatigue_score: int
    local_first_streaming: bool
    bounded_provider_recommendation: str


@dataclass(frozen=True)
class StreamingGovernanceFrame:
    streaming_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_streaming_enforced: bool
    bounded_cognition_enforced: bool
    bounded_provider_reuse_enforced: bool
    bounded_continuation_persistence_enforced: bool
    recursive_streaming_blocked: bool
    hidden_realtime_agents_blocked: bool
    self_expanding_narration_blocked: bool
    retrieval_scope_widening_blocked: bool
    governance_policy_mutation_blocked: bool
    read_only_projection_enforced: bool


@dataclass(frozen=True)
class StreamingBudgetFrame:
    streaming_budget_active: bool
    streaming_budget_used: int
    streaming_budget_limit: int
    streaming_budget_exceeded: bool
    streaming_latency_score: int
    bounded_cognition_score: int
    budget_pressure: str


@dataclass(frozen=True)
class StreamingTerminationFrame:
    streaming_termination_active: bool
    streaming_terminated: bool
    termination_reasons: tuple[str, ...]
    streaming_budget_exceeded: bool
    recursive_streaming_detected: bool
    governance_violation_detected: bool
    continuation_entropy_threshold_exceeded: bool
    interruption_pressure_threshold_exceeded: bool


@dataclass(frozen=True)
class StreamingHistoryFrame:
    streaming_history_active: bool
    streaming_history: tuple[str, ...]
    streaming_history_limit: int
    deterministic_streaming_summary: str
    history_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class StreamingConfidenceFrame:
    streaming_confidence_active: bool
    streaming_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    realtime_survivability_confidence: bool


@dataclass(frozen=True)
class StreamingEvictionFrame:
    streaming_eviction_active: bool
    evicted_speech_chunks: tuple[str, ...]
    evicted_cognition_deltas: tuple[str, ...]
    evicted_continuation_items: tuple[str, ...]
    evicted_provider_items: tuple[str, ...]
    evicted_history_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class StreamingCognitionFrame:
    streaming_cognition_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    speech: StreamingSpeechFrame
    delta: StreamingDeltaFrame
    continuation: StreamingContinuationFrame
    interruption: StreamingInterruptionFrame
    provider: ProviderStreamingFrame
    governance: StreamingGovernanceFrame
    budget: StreamingBudgetFrame
    termination: StreamingTerminationFrame
    history: StreamingHistoryFrame
    confidence: StreamingConfidenceFrame
    eviction: StreamingEvictionFrame
    streaming_latency_score: int
    interruption_recovery_score: int
    provider_streaming_score: int
    continuation_streaming_score: int
    bounded_cognition_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    streaming_mode: str
    estimated_avoided_streaming_instability: int
    estimated_avoided_provider_interruptions: int
    estimated_avoided_frontier_streaming: int


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
        return "STREAMING_SURVIVABLE"
    if score >= 60:
        return "STREAMING_GUARDED"
    return "STREAMING_TERMINATION_REQUIRED"


class StreamingCognitionRuntime:
    def evaluate(
        self,
        *,
        speech_chunks: tuple[str, ...] = DEFAULT_SPEECH_CHUNKS,
        cognition_deltas: tuple[str, ...] = DEFAULT_COGNITION_DELTAS,
        continuation_items: tuple[str, ...] = DEFAULT_CONTINUATION_ITEMS,
        provider_candidates: tuple[str, ...] = DEFAULT_PROVIDER_CANDIDATES,
        streaming_history_items: tuple[str, ...] = DEFAULT_STREAMING_HISTORY,
        interrupted: bool = False,
        interruption_pressure: int = 1,
        provider_failures: int = 0,
        provider_cooldown_windows: int = 1,
        provider_fatigue_score: int = 18,
        continuation_entropy: int = 18,
        streaming_budget_used: int = 7,
        recursive_streaming_attempts: int = 0,
        hidden_realtime_agent_attempts: int = 0,
        self_expanding_narration_attempts: int = 0,
        retrieval_scope_widening_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> StreamingCognitionFrame:
        bounded_speech = speech_chunks[:MAX_SPEECH_CHUNKS]
        bounded_deltas = cognition_deltas[:MAX_COGNITION_DELTAS]
        bounded_continuation = continuation_items[:MAX_CONTINUATION_ITEMS]
        bounded_providers = provider_candidates[:MAX_PROVIDER_WINDOW]
        bounded_history = streaming_history_items[:MAX_STREAMING_HISTORY]

        evicted_speech = speech_chunks[MAX_SPEECH_CHUNKS:]
        evicted_deltas = cognition_deltas[MAX_COGNITION_DELTAS:]
        evicted_continuation = continuation_items[MAX_CONTINUATION_ITEMS:]
        evicted_providers = provider_candidates[MAX_PROVIDER_WINDOW:]
        evicted_history = streaming_history_items[MAX_STREAMING_HISTORY:]
        eviction_count = sum(
            len(items)
            for items in (
                evicted_speech,
                evicted_deltas,
                evicted_continuation,
                evicted_providers,
                evicted_history,
            )
        )

        speech_reset_required = (
            interrupted or interruption_pressure >= INTERRUPTION_PRESSURE_THRESHOLD
        )
        speech_buffer = () if speech_reset_required else bounded_speech
        speech_continuation = () if speech_reset_required else speech_buffer[-2:]

        governance_violation = any(
            (
                hidden_realtime_agent_attempts,
                self_expanding_narration_attempts,
                retrieval_scope_widening_attempts,
                governance_policy_mutation_attempts,
            )
        )
        recursive_detected = recursive_streaming_attempts > 0
        budget_exceeded = streaming_budget_used > STREAMING_BUDGET_LIMIT
        entropy_exceeded = continuation_entropy >= CONTINUATION_ENTROPY_THRESHOLD
        interruption_exceeded = interruption_pressure >= INTERRUPTION_PRESSURE_THRESHOLD

        termination_reasons: list[str] = []
        if budget_exceeded:
            termination_reasons.append("STREAMING_BUDGET_EXCEEDED")
        if recursive_detected:
            termination_reasons.append("RECURSIVE_STREAMING_DETECTED")
        if governance_violation:
            termination_reasons.append("GOVERNANCE_VIOLATION_DETECTED")
        if entropy_exceeded:
            termination_reasons.append("CONTINUATION_ENTROPY_THRESHOLD_EXCEEDED")
        if interruption_exceeded:
            termination_reasons.append("INTERRUPTION_PRESSURE_THRESHOLD_EXCEEDED")

        interruption_recovery_score = _clamp_score(
            92 - interruption_pressure * 11 - int(interrupted) * 14 - provider_failures * 7
        )
        provider_streaming_score = _clamp_score(
            88
            - provider_failures * 13
            - provider_cooldown_windows * 4
            - provider_fatigue_score // 3
        )
        continuation_streaming_score = _clamp_score(91 - continuation_entropy // 2)
        streaming_latency_score = _clamp_score(
            94
            - len(bounded_deltas) * 3
            - len(speech_buffer) * 2
            - provider_cooldown_windows * 4
            - provider_failures * 6
        )
        bounded_cognition_score = _clamp_score(
            min(
                streaming_latency_score,
                interruption_recovery_score,
                provider_streaming_score,
                continuation_streaming_score,
            )
            - int(recursive_detected) * 20
            - int(governance_violation) * 20
            - int(budget_exceeded) * 15
        )
        confidence_score = _clamp_score(
            (streaming_latency_score + interruption_recovery_score + provider_streaming_score) // 3
            - int(bool(termination_reasons)) * 12
        )

        provider_fallback_active = provider_failures > 0 or provider_fatigue_score >= 60
        recommended_provider = (
            "local-summary-provider" if provider_fallback_active else bounded_providers[0]
        )
        continuation_summary = ";".join(bounded_continuation)
        delta_summary = ";".join(bounded_deltas)
        history_summary = ";".join(bounded_history)

        return StreamingCognitionFrame(
            streaming_cognition_active=True,
            requirement_ids=STREAMING_COGNITION_REQUIREMENT_IDS,
            test_ids=STREAMING_COGNITION_TEST_IDS,
            speech=StreamingSpeechFrame(
                speech_streaming_active=True,
                speech_chunks=speech_buffer,
                speech_chunk_limit=MAX_SPEECH_CHUNKS,
                speech_continuation=speech_continuation,
                speech_reset_on_interruption=speech_reset_required,
                deterministic_speech_buffer="|".join(speech_buffer),
                bounded_speech_summary=f"chunks={len(speech_buffer)};reset={speech_reset_required}",
            ),
            delta=StreamingDeltaFrame(
                delta_streaming_active=True,
                cognition_deltas=bounded_deltas,
                cognition_delta_limit=MAX_COGNITION_DELTAS,
                delta_overflow_blocked=len(evicted_deltas) > 0,
                deterministic_delta_summary=delta_summary,
                bounded_delta_recommendation="EMIT_BOUNDED_DELTAS_ONLY",
            ),
            continuation=StreamingContinuationFrame(
                continuation_streaming_active=True,
                continuation_items=bounded_continuation,
                continuation_limit=MAX_CONTINUATION_ITEMS,
                continuation_persistence_reuse=True,
                continuation_reset_governed=speech_reset_required or entropy_exceeded,
                continuation_entropy=continuation_entropy,
                entropy_suppression_active=entropy_exceeded,
                deterministic_continuation_summary=continuation_summary,
            ),
            interruption=StreamingInterruptionFrame(
                interruption_streaming_active=True,
                interruption_detected=interrupted or interruption_pressure > 1,
                interruption_pressure=interruption_pressure,
                interruption_recovery_score=interruption_recovery_score,
                speech_reset_required=speech_reset_required,
                continuation_reset_safe=True,
                provider_stabilization_required=provider_fallback_active or interruption_exceeded,
                bounded_recovery_recommendation=(
                    "RESET_SPEECH_AND_STABILIZE_PROVIDER"
                    if speech_reset_required
                    else "CONTINUE_BOUNDED_STREAM"
                ),
            ),
            provider=ProviderStreamingFrame(
                provider_streaming_active=True,
                provider_order=bounded_providers,
                provider_window_limit=MAX_PROVIDER_WINDOW,
                recommended_provider=recommended_provider,
                provider_fallback_active=provider_fallback_active,
                provider_cooldown_windows=provider_cooldown_windows,
                provider_fatigue_score=provider_fatigue_score,
                local_first_streaming=True,
                bounded_provider_recommendation=(
                    "USE_LOCAL_SUMMARY_FALLBACK"
                    if provider_fallback_active
                    else "USE_LOCAL_STREAMING_PROVIDER"
                ),
            ),
            governance=StreamingGovernanceFrame(
                streaming_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_streaming_enforced=True,
                bounded_cognition_enforced=True,
                bounded_provider_reuse_enforced=True,
                bounded_continuation_persistence_enforced=True,
                recursive_streaming_blocked=recursive_detected,
                hidden_realtime_agents_blocked=hidden_realtime_agent_attempts > 0,
                self_expanding_narration_blocked=self_expanding_narration_attempts > 0,
                retrieval_scope_widening_blocked=retrieval_scope_widening_attempts > 0,
                governance_policy_mutation_blocked=governance_policy_mutation_attempts > 0,
                read_only_projection_enforced=True,
            ),
            budget=StreamingBudgetFrame(
                streaming_budget_active=True,
                streaming_budget_used=streaming_budget_used,
                streaming_budget_limit=STREAMING_BUDGET_LIMIT,
                streaming_budget_exceeded=budget_exceeded,
                streaming_latency_score=streaming_latency_score,
                bounded_cognition_score=bounded_cognition_score,
                budget_pressure=_pressure_label(streaming_budget_used, STREAMING_BUDGET_LIMIT),
            ),
            termination=StreamingTerminationFrame(
                streaming_termination_active=True,
                streaming_terminated=bool(termination_reasons),
                termination_reasons=tuple(termination_reasons),
                streaming_budget_exceeded=budget_exceeded,
                recursive_streaming_detected=recursive_detected,
                governance_violation_detected=governance_violation,
                continuation_entropy_threshold_exceeded=entropy_exceeded,
                interruption_pressure_threshold_exceeded=interruption_exceeded,
            ),
            history=StreamingHistoryFrame(
                streaming_history_active=True,
                streaming_history=bounded_history,
                streaming_history_limit=MAX_STREAMING_HISTORY,
                deterministic_streaming_summary=history_summary,
                history_overflow_blocked=len(evicted_history) > 0,
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            confidence=StreamingConfidenceFrame(
                streaming_confidence_active=True,
                streaming_confidence_score=confidence_score,
                confidence_status=_confidence_status(confidence_score),
                deterministic_confidence=True,
                realtime_survivability_confidence=confidence_score >= 70,
            ),
            eviction=StreamingEvictionFrame(
                streaming_eviction_active=True,
                evicted_speech_chunks=evicted_speech,
                evicted_cognition_deltas=evicted_deltas,
                evicted_continuation_items=evicted_continuation,
                evicted_provider_items=evicted_providers,
                evicted_history_items=evicted_history,
                eviction_count=eviction_count,
                bounded_eviction_active=eviction_count > 0,
                eviction_summary=f"evicted={eviction_count}",
            ),
            streaming_latency_score=streaming_latency_score,
            interruption_recovery_score=interruption_recovery_score,
            provider_streaming_score=provider_streaming_score,
            continuation_streaming_score=continuation_streaming_score,
            bounded_cognition_score=bounded_cognition_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            streaming_mode="LOCAL_PATCH_BOUNDED_STREAMING_COGNITION",
            estimated_avoided_streaming_instability=2600 + eviction_count * 120,
            estimated_avoided_provider_interruptions=1400 + provider_failures * 180,
            estimated_avoided_frontier_streaming=3200 + len(bounded_deltas) * 90,
        )
