from __future__ import annotations

from ai_dev_os.cognitive_memory_pressure import CognitiveMemoryPressureRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_memorypressure_01_runtime_is_bounded_and_human_confirmed() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.cognitive_memory_pressure_active is True
    assert frame.bounded is True
    assert frame.human_confirmed_only is True
    assert frame.rollback_safe is True
    assert frame.cognitive_memory_pressure.human_confirmed_only is True
    assert "autonomous cognition erasure" in frame.cognitive_memory_pressure.blocked_behaviors


def test_tc_memorypressure_02_memory_pressure_detects_pre_collapse_degradation() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.cognitive_memory_pressure.memory_pressure_score == 21
    assert frame.cognitive_memory_pressure.memory_pressure_label == "MEMORY_PRESSURE_LOW"
    assert frame.cognitive_memory_pressure.memory_pressure_summary == (
        "MEMORY_PRESSURE_LOW_COMPACT_CONTINUITY_GUARDED"
    )
    assert frame.cognitive_memory_pressure.bounded_recovery_recommendation == (
        "RESET_COMPACT_CONTINUITY_AND_NARROW_RETRIEVAL"
    )


def test_tc_memorypressure_03_continuity_inflation_warns_without_rewriting() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.continuity_inflation_active is True
    assert frame.continuity_inflation.oversized_continuity_exports == 28
    assert frame.continuity_inflation.recursive_continuity_accumulation == 12
    assert frame.continuity_inflation.giant_sprint_closure_growth == 21
    assert frame.continuity_inflation.inflation_warning == "CONTINUITY_INFLATION_GUARDED"
    assert frame.continuity_inflation.compactness_reset_recommendation == (
        "COMPACTNESS_RESET_BEFORE_CONTINUITY_REUSE"
    )


def test_tc_memorypressure_04_retrieval_overload_blocks_broad_expansion() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.retrieval_overload_active is True
    assert frame.retrieval_overload.retrieval_radius_expansion == 16
    assert frame.retrieval_overload.repo_wide_retrieval_expansion_blocked is True
    assert frame.retrieval_overload.recursive_retrieval_loops_blocked is True
    assert frame.retrieval_overload.retrieval_overload_summary == (
        "RETRIEVAL_BOUNDED_SCOPE_NARROWING_RECOMMENDED"
    )


def test_tc_memorypressure_05_summary_entropy_recommends_bounded_rewrite() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.summary_entropy_active is True
    assert frame.summary_entropy.summary_noise_growth == 24
    assert frame.summary_entropy.repeated_wording_inflation == 21
    assert frame.summary_entropy.entropy_score == 45
    assert frame.summary_entropy.summary_entropy_summary == (
        "SUMMARY_ENTROPY_GUARDED_REWRITE_RECOMMENDED"
    )
    assert frame.summary_entropy.bounded_rewrite_recommendation == (
        "DEDUP_SUMMARY_WITHOUT_REWRITING_HISTORY"
    )


def test_tc_memorypressure_06_context_fragmentation_emits_merge_hints_only() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.context_fragmentation_active is True
    assert frame.context_fragmentation.fragmentation_score == 26
    assert frame.context_fragmentation.fragmentation_summary == (
        "FRAGMENTATION_LOW_MERGE_HINTS_ONLY"
    )
    assert "Do not rewrite archived sprint history." in (
        frame.context_fragmentation.bounded_continuity_merge_hints
    )


def test_tc_memorypressure_07_stale_cognition_requires_confirmation() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.stale_cognition.stale_cognition_active is True
    assert frame.stale_cognition.stale_cognition_persistence == 18
    assert frame.stale_cognition.stale_memory_eviction_required is True
    assert frame.stale_cognition.autonomous_memory_deletion_allowed is False


def test_tc_memorypressure_08_continuity_pressure_tracks_duplication() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.continuity_pressure.continuity_pressure_active is True
    assert frame.continuity_pressure.continuity_growth_pressure == 28
    assert frame.continuity_pressure.continuity_duplication_pressure == 21
    assert frame.continuity_pressure.continuity_corruption_pressure == 24
    assert frame.continuity_pressure.continuity_pressure_summary == (
        "CONTINUITY_PRESSURE_GUARDED_COMPACT_RESET_HINTED"
    )


def test_tc_memorypressure_09_compactness_pressure_uses_fatigue_signal() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.compactness_pressure.compactness_pressure_active is True
    assert frame.compactness_pressure.compactness_decay_score == 16
    assert frame.compactness_pressure.summary_duplication_score == 21
    assert frame.compactness_pressure.compactness_reset_recommended is True
    assert frame.compactness_pressure.compactness_pressure_summary == (
        "COMPACTNESS_PRESSURE_LOW_RESET_BEFORE_ROLLOVER"
    )


def test_tc_memorypressure_10_retrieval_radius_stays_bounded() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.retrieval_radius_pressure.retrieval_radius_pressure_active is True
    assert frame.retrieval_radius_pressure.retrieval_radius_score == 16
    assert frame.retrieval_radius_pressure.bounded_retrieval_radius == (
        "cognitive_memory_pressure",
        "provider_fatigue",
        "runtime_audit",
    )
    assert frame.retrieval_radius_pressure.automatic_scope_widening_allowed is False


def test_tc_memorypressure_11_recovery_is_recommendation_only() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.continuity_recovery.continuity_recovery_active is True
    assert frame.continuity_recovery.compactness_reset is True
    assert frame.continuity_recovery.continuity_truncation is True
    assert frame.continuity_recovery.stale_memory_eviction is True
    assert frame.continuity_recovery.bounded_retrieval_narrowing is True
    assert frame.continuity_recovery.continuity_recovery_recommendation == (
        "RESET_COMPACT_CONTINUITY_TRUNCATE_STALE_MEMORY_NARROW_RETRIEVAL"
    )
    assert frame.continuity_recovery.autonomous_delete_allowed is False
    assert frame.continuity_recovery.sprint_history_rewrite_allowed is False


def test_tc_memorypressure_12_confidence_tracks_guarded_pressure() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.confidence.memory_pressure_confidence_active is True
    assert frame.confidence.confidence_score == 79
    assert frame.confidence.pressure_label == "MEMORY_PRESSURE_LOW"
    assert frame.confidence.confidence_summary[0] == "memory:21:MEMORY_PRESSURE_LOW"
    assert frame.confidence.confidence_summary[3] == "entropy:45:ENTROPY_GUARDED"


def test_tc_memorypressure_13_history_is_bounded() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.history.memory_pressure_history_active is True
    assert frame.history.bounded_history_size == 8
    assert len(frame.history.history_entries) <= frame.history.bounded_history_size
    assert frame.history.continuity_pressure_trend == (18, 20, 21)


def test_tc_memorypressure_14_decay_guard_tracks_pressure_sources() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.decay.memory_pressure_decay_active is True
    assert frame.decay.memory_pressure_decay_guard_active is True
    assert frame.decay.continuity_decay == 28
    assert frame.decay.retrieval_decay == 16
    assert frame.decay.summary_entropy_decay == 24
    assert frame.decay.fragmentation_decay == 17


def test_tc_memorypressure_15_governance_blocks_hidden_mutation() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.governance.memory_pressure_governance_active is True
    assert frame.governance.compact_continuity is True
    assert frame.governance.bounded_retrieval is True
    assert frame.governance.local_patch_discipline is True
    assert frame.governance.anti_explosion_governance is True
    assert frame.governance.autonomous_cognition_erasure is False
    assert frame.governance.recursive_continuity_mutation is False
    assert frame.governance.governance_runtime_bypassed is False
    assert frame.governance.hidden_context_mutation is False
    assert frame.governance.retrieval_scope_expansion_allowed is False
    assert frame.governance.automatic_context_expansion is False


def test_tc_memorypressure_16_eviction_is_human_confirmed() -> None:
    frame = CognitiveMemoryPressureRuntime().evaluate()

    assert frame.eviction.memory_pressure_eviction_active is True
    assert frame.eviction.stale_cognition_eviction_recommended is True
    assert frame.eviction.oversized_continuity_payload_evicted is False
    assert frame.eviction.duplicate_summary_payload_evicted is False
    assert frame.eviction.eviction_requires_human_confirmation is True
    assert frame.eviction.max_history_entries == 8


def test_tc_memorypressure_17_runtime_audit_exposes_required_fields() -> None:
    report = run_runtime_enforcement_audit().cognitive_memory_pressure

    assert report.cognitive_memory_pressure_active is True
    assert report.continuity_inflation_active is True
    assert report.retrieval_overload_active is True
    assert report.summary_entropy_active is True
    assert report.context_fragmentation_active is True
    assert report.estimated_avoided_context_explosion == 1800
    assert report.estimated_avoided_summary_entropy == 640
    assert report.estimated_avoided_retrieval_overload == 920
    assert report.autonomous_cognition_erasure is False
    assert report.hidden_context_mutation is False


def test_tc_memorypressure_18_runtime_is_deterministic_and_summary_only() -> None:
    first = CognitiveMemoryPressureRuntime().evaluate()
    second = CognitiveMemoryPressureRuntime().evaluate()

    assert first == second
    assert first.deterministic is True
    assert first.local_only is True
    assert first.summary_only is True
    assert first.estimated_avoided_context_explosion == 1800
    assert first.estimated_avoided_summary_entropy == 640
