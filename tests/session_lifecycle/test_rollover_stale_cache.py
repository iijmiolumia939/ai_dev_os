from __future__ import annotations

from ai_dev_os.session_lifecycle.cache_aware_session import CacheAwareSessionPolicy
from ai_dev_os.session_lifecycle.session_rollover import SessionRolloverPolicy
from ai_dev_os.session_lifecycle.stale_context_detection import (
    ContextSignal,
    StaleContextDetectionPolicy,
)


def test_sprint_rollover_recommendation_detects_session_cut() -> None:
    frame = SessionRolloverPolicy().evaluate(
        session_age=7,
        estimated_context_tokens=32_000,
        stale_context_ratio=0.48,
        retrieval_pressure="HIGH",
        cache_reuse_probability=0.78,
        sprint_boundary=True,
        architecture_escalation=True,
    )

    assert frame.rollover_recommended is True
    assert frame.compact_bundle_required is True
    assert frame.architecture_isolation_required is True
    assert frame.recommended_session_action == "isolate_architecture_session"
    assert "sprint_boundary" in frame.triggers
    assert "stale_history_pressure" in frame.triggers
    assert frame.estimated_avoided_tokens == 29_600


def test_stale_context_detection_recommends_eviction_and_bundle_refresh() -> None:
    report = StaleContextDetectionPolicy().evaluate(
        (
            ContextSignal("active-runtime", 800, "active sprint", 0.95),
            ContextSignal("old-sprint", 10_000, "old sprint", 0.2, age_days=60),
            ContextSignal("obsolete-adr", 4_000, "obsolete architecture discussion", 0.2),
            ContextSignal("roadmap", 2_000, "inactive roadmap reference", 0.3),
            ContextSignal("giant", 5_000, "summary", 0.4, repeated=True),
            ContextSignal("drift", 3_000, "retrieval drift", 0.1),
        )
    )

    assert report.stale_context_detected is True
    assert report.stale_context_ratio > 0.9
    assert report.recommended_bundle_refresh is True
    assert report.recommended_evictions == (
        "old-sprint",
        "obsolete-adr",
        "roadmap",
        "giant",
        "drift",
    )
    assert "implicit_retrieval_drift" in report.stale_reasons


def test_cache_aware_session_routes_without_unbounded_continuation() -> None:
    compact = CacheAwareSessionPolicy().evaluate(
        cache_reuse_probability=0.8,
        repeated_instruction_stability=0.85,
        context_freshness=0.7,
        retrieval_overlap=0.65,
        prompt_compactness=0.8,
        pressure="HIGH",
    )
    fork = CacheAwareSessionPolicy().evaluate(
        cache_reuse_probability=0.9,
        repeated_instruction_stability=0.9,
        context_freshness=0.25,
        retrieval_overlap=0.2,
        prompt_compactness=0.8,
        pressure="NORMAL",
    )

    assert compact.continue_session is False
    assert compact.compact_then_continue is True
    assert "high_pressure_requires_compaction" in compact.warnings
    assert fork.fork_session is True
    assert "unbounded_session_continuation_blocked" in fork.warnings
