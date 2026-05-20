from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.stale_detection import GovernanceStaleDetectionPrimitive

STALE_REASONS = {
    "old_sprint": "unrelated_old_sprint_context",
    "obsolete_architecture": "obsolete_architecture_discussion",
    "inactive_roadmap": "inactive_roadmap_reference",
    "giant_summary": "repeated_giant_summary",
    "stale_review": "stale_review_context",
    "retrieval_drift": "implicit_retrieval_drift",
}


@dataclass(frozen=True)
class ContextSignal:
    identifier: str
    tokens: int
    reason: str
    relevance_score: float
    age_days: int = 0
    repeated: bool = False


@dataclass(frozen=True)
class StaleContextReport:
    stale_context_detected: bool
    stale_context_ratio: float
    recommended_evictions: tuple[str, ...]
    recommended_bundle_refresh: bool
    stale_reasons: tuple[str, ...]


class StaleContextDetectionPolicy:
    def __init__(self, *, stale_ratio_threshold: float = 0.3) -> None:
        self.stale_ratio_threshold = stale_ratio_threshold

    def evaluate(self, signals: tuple[ContextSignal, ...]) -> StaleContextReport:
        shared_stale = GovernanceStaleDetectionPrimitive().detect(
            tuple(signal.reason for signal in signals)
        )
        total_tokens = sum(max(0, signal.tokens) for signal in signals)
        stale_tokens = 0
        evictions: list[str] = []
        reasons: list[str] = []
        for signal in signals:
            reason = self._stale_reason(signal)
            if reason:
                stale_tokens += max(0, signal.tokens)
                evictions.append(signal.identifier)
                reasons.append(reason)
        ratio = stale_tokens / total_tokens if total_tokens else 0.0
        detected = (
            ratio >= self.stale_ratio_threshold or bool(evictions) or shared_stale.stale_detected
        )
        return StaleContextReport(
            stale_context_detected=detected,
            stale_context_ratio=round(ratio, 4),
            recommended_evictions=tuple(dict.fromkeys(evictions)),
            recommended_bundle_refresh=(
                detected
                and (ratio >= self.stale_ratio_threshold or shared_stale.stale_cleanup_recommended)
            ),
            stale_reasons=tuple(dict.fromkeys(reasons)),
        )

    def _stale_reason(self, signal: ContextSignal) -> str:
        normalized = signal.reason.lower()
        if signal.age_days >= 21 and signal.relevance_score < 0.4:
            return STALE_REASONS["old_sprint"]
        if "obsolete" in normalized and "architecture" in normalized:
            return STALE_REASONS["obsolete_architecture"]
        if "inactive" in normalized and "roadmap" in normalized:
            return STALE_REASONS["inactive_roadmap"]
        if signal.repeated and signal.tokens >= 4_000:
            return STALE_REASONS["giant_summary"]
        if "review" in normalized and signal.age_days >= 14:
            return STALE_REASONS["stale_review"]
        if "retrieval" in normalized and signal.relevance_score < 0.25:
            return STALE_REASONS["retrieval_drift"]
        return ""
