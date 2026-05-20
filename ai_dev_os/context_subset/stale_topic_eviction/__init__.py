from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.stale_detection import GovernanceStaleDetectionPrimitive

STALE_MARKERS = {
    "obsolete_roadmap": ("obsolete roadmap", "old roadmap", "superseded roadmap"),
    "inactive_migration": ("inactive migration", "paused migration"),
    "stale_rollout_discussion": ("stale rollout", "old rollout"),
    "repeated_architecture_summary": ("repeated architecture", "architecture summary repeated"),
    "old_sprint_review": ("old sprint", "previous sprint review", "sprint review"),
    "inactive_governance_debate": ("inactive governance", "old governance debate"),
    "duplicate_continuity": ("duplicate continuity", "duplicated continuity"),
}


@dataclass(frozen=True)
class StaleTopicEvictionFrame:
    evicted_topics: tuple[str, ...]
    retained_topics: tuple[str, ...]
    eviction_reason: dict[str, str]
    estimated_saved_tokens: int
    deterministic: bool


class StaleTopicEvictionPolicy:
    def evict(self, topics: tuple[str, ...]) -> StaleTopicEvictionFrame:
        shared_stale = GovernanceStaleDetectionPrimitive().detect(topics)
        evicted: list[str] = []
        retained: list[str] = []
        reasons: dict[str, str] = {}
        for topic in topics:
            reason = self._reason(topic)
            if reason:
                evicted.append(topic)
                reasons[topic] = reason
            elif shared_stale.stale_detected and "stale" in topic.lower():
                evicted.append(topic)
                reasons[topic] = "shared_stale_signal"
            elif topic not in retained:
                retained.append(topic)
        saved = sum(max(80, len(topic.split()) * 35) for topic in evicted)
        return StaleTopicEvictionFrame(
            evicted_topics=tuple(evicted),
            retained_topics=tuple(retained),
            eviction_reason=reasons,
            estimated_saved_tokens=saved,
            deterministic=True,
        )

    def _reason(self, topic: str) -> str:
        normalized = topic.lower()
        for reason, markers in STALE_MARKERS.items():
            if any(marker in normalized for marker in markers):
                return reason
        return ""
