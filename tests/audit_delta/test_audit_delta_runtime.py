from __future__ import annotations

from ai_dev_os.incremental_context.audit_delta import AuditDeltaPolicy
from ai_dev_os.incremental_context.cognition_cache import CognitionCachePolicy
from ai_dev_os.incremental_context.continuity_delta import ContinuityDeltaPolicy


def test_tc_incrementalcontext_06_continuity_and_audit_delta_suppress_replay() -> None:
    continuity = ContinuityDeltaPolicy().diff(
        previous_summaries=("previous sprint",),
        current_summaries=("previous sprint", "new delta"),
        stale_summaries=("stale summary",),
    )
    audit = AuditDeltaPolicy().summarize(
        changed_sections=("incremental_context",),
        unchanged_sections=("activation", "routing"),
        repeated_validations=("pytest", "runtime_audit"),
    )

    assert continuity.changed_continuity_bundle_export == ("new delta",)
    assert continuity.unchanged_sprint_summary_suppression is True
    assert continuity.stale_continuity_deduplication is True
    assert continuity.continuity_replay_reduction is True
    assert audit.runtime_audit_delta_mode is True
    assert audit.unchanged_audit_section_suppression is True
    assert audit.repeated_validation_replay_suppression is True
    assert audit.estimated_avoided_validation_tokens > 0


def test_tc_incrementalcontext_07_cognition_cache_uses_fingerprints_only() -> None:
    first = CognitionCachePolicy().fingerprint(context_summaries=("summary", "delta"))
    second = CognitionCachePolicy().fingerprint(
        context_summaries=("summary", "delta"),
        previous_fingerprints=first.deterministic_context_fingerprints,
    )

    assert first.deterministic_context_fingerprints == second.deterministic_context_fingerprints
    assert second.unchanged_context_skip_recommendation is True
    assert second.no_raw_prompt_persistence is True
    assert second.no_provider_specific_hidden_memory is True
    assert all(
        "summary" not in item and "delta" not in item
        for item in second.deterministic_context_fingerprints
    )
