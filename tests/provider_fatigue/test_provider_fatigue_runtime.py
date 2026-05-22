from __future__ import annotations

from ai_dev_os.provider_fatigue import ProviderFatigueRuntime
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_providerfatigue_01_runtime_is_bounded_and_human_confirmed() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.provider_fatigue_active is True
    assert frame.bounded is True
    assert frame.human_confirmed_only is True
    assert frame.rollback_safe is True
    assert frame.provider_fatigue.human_confirmed_only is True
    assert "autonomous provider replacement" in frame.provider_fatigue.blocked_behaviors


def test_tc_providerfatigue_02_scores_detect_degradation_before_collapse() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.provider_fatigue.fatigue_score["qwen2.5-coder:7b"] == 19
    assert frame.provider_fatigue.fatigue_score["GPT-5.5 reference"] == 87
    assert frame.provider_fatigue.degradation_trend["qwen2.5-coder:7b"] == "FATIGUE_LOW"
    assert frame.provider_fatigue.degradation_trend["GPT-5.5 reference"] == ("RECOVERY_REQUIRED")


def test_tc_providerfatigue_03_escalation_fatigue_is_guarded() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.escalation_fatigue_active is True
    assert frame.escalation_fatigue.escalation_fatigue_warning == ("ESCALATION_PRESSURE_GUARDED")
    assert frame.escalation_fatigue.repeated_high_escalation_pressure["GPT-5.5 reference"] == 8
    assert frame.escalation_fatigue.unnecessary_premium_escalation["GPT-5.5 reference"] == 6
    assert "qwen2.5-coder:7b" in frame.escalation_fatigue.bounded_downgrade_recommendation


def test_tc_providerfatigue_04_fallback_oscillation_blocks_loops() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.fallback_oscillation_active is True
    assert frame.fallback_oscillation.recursive_reroute_loops_blocked is True
    assert frame.fallback_oscillation.unstable_escalation_oscillation_blocked is True
    assert frame.fallback_oscillation.fallback_oscillation_summary == (
        "OSCILLATION_LOW_LOCAL_FIRST_BLOCKED_LOOPS"
    )
    assert frame.fallback_oscillation.oscillation_risk_score["GPT-5.5 reference"] > (
        frame.fallback_oscillation.oscillation_risk_score["qwen2.5-coder:7b"]
    )


def test_tc_providerfatigue_05_compactness_decay_recommends_reset() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.compactness_decay_active is True
    assert frame.compactness_decay.compactness_retention_score["qwen2.5-coder:7b"] == 94
    assert frame.compactness_decay.summary_growth_inflation["GPT-5.5 reference"] == 16
    assert frame.compactness_decay.bounded_compression_recommendation == (
        "COMPACTNESS_RESET_BEFORE_LONG_SESSION_CONTINUATION"
    )


def test_tc_providerfatigue_06_recursive_pressure_blocks_expansion() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.recursive_pressure.recursive_pressure_active is True
    assert frame.recursive_pressure.recursive_loop_blocked is True
    assert frame.recursive_pressure.recursive_reasoning_pressure["GPT-5.5 reference"] == 19
    assert frame.recursive_pressure.retrieval_scope_expansion_pressure["GPT-5.5 reference"] > 0


def test_tc_providerfatigue_07_context_fatigue_recommends_compact_reset() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.context_fatigue.context_fatigue_active is True
    assert frame.context_fatigue.compact_context_reset_recommended is True
    assert frame.context_fatigue.continuity_corruption_tendency["GPT-5.5 reference"] == 14
    assert frame.context_fatigue.repeated_context_reuse_pressure["qwen2.5-coder:7b"] == 4


def test_tc_providerfatigue_08_summary_fatigue_evicts_oversized_payloads() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.summary_fatigue.summary_fatigue_active is True
    assert frame.summary_fatigue.oversized_summary_eviction_required is True
    assert frame.summary_fatigue.compact_summary_recovery == (
        "DEDUP_AND_TRUNCATE_TO_COMPACT_CONTINUITY"
    )
    assert frame.summary_fatigue.giant_summary_growth["qwen2.5-coder:14b"] == 5


def test_tc_providerfatigue_09_long_session_pressure_tracks_rollovers() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.long_session_pressure_active is True
    assert frame.long_session_pressure.simulated_rollovers == 8
    assert frame.long_session_pressure.long_session_pressure_summary == (
        "LONG_SESSION_PRESSURE_LOW_BUT_WATCH_ESCALATION"
    )
    assert frame.long_session_pressure.provider_exhaustion["GPT-5.5 reference"] == 87
    assert frame.long_session_pressure.fallback_pressure_increase["qwen2.5-coder:7b"] == 2


def test_tc_providerfatigue_10_recovery_is_bounded_not_automatic() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.recovery.provider_recovery_active is True
    assert frame.recovery.bounded_cooldown is True
    assert frame.recovery.downgrade_to_local is True
    assert frame.recovery.compactness_reset is True
    assert frame.recovery.recovery_recommendation == (
        "RECOVER_WITH_LOCAL_DOWNGRADE_AND_COMPACTNESS_RESET"
    )
    assert frame.recovery.autonomous_reroute_allowed is False
    assert frame.recovery.governance_policy_mutation_allowed is False


def test_tc_providerfatigue_11_confidence_labels_show_low_fatigue_local() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.confidence.fatigue_confidence_active is True
    assert frame.confidence.overall_fatigue_label == "FATIGUE_LOW"
    assert frame.confidence.fatigue_label_by_provider["qwen2.5-coder:7b"] == "FATIGUE_LOW"
    assert frame.confidence.fatigue_label_by_provider["GPT-5.5 reference"] == ("RECOVERY_REQUIRED")
    assert frame.confidence.fatigue_confidence_summary[0].startswith("qwen2.5-coder:7b")


def test_tc_providerfatigue_12_history_and_eviction_are_bounded() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.history.fatigue_history_active is True
    assert frame.history.bounded_history_size == 8
    assert len(frame.history.fatigue_history_entries) <= frame.history.bounded_history_size
    assert frame.eviction.fatigue_eviction_active is True
    assert frame.eviction.stale_fatigue_history_evicted is True
    assert frame.eviction.oversized_fatigue_payloads_evicted is True


def test_tc_providerfatigue_13_decay_guard_tracks_pressure() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.decay.fatigue_decay_active is True
    assert frame.decay.fatigue_decay_guard_active is True
    assert frame.decay.compactness_decay["GPT-5.5 reference"] == 16
    assert frame.decay.escalation_decay["GPT-5.5 reference"] == 8
    assert frame.decay.recursive_decay["qwen2.5-coder:7b"] == 5


def test_tc_providerfatigue_14_governance_blocks_hidden_authority() -> None:
    frame = ProviderFatigueRuntime().evaluate()

    assert frame.governance.fatigue_governance_active is True
    assert frame.governance.bounded_cognition is True
    assert frame.governance.human_confirmed_routing is True
    assert frame.governance.governance_runtime_bypassed is False
    assert frame.governance.autonomous_provider_replacement is False
    assert frame.governance.hidden_escalation_switching is False
    assert frame.governance.retrieval_scope_expansion_allowed is False


def test_tc_providerfatigue_15_runtime_audit_exposes_fatigue_flags() -> None:
    report = run_runtime_enforcement_audit().provider_fatigue

    assert report.provider_fatigue_active is True
    assert report.escalation_fatigue_active is True
    assert report.fallback_oscillation_active is True
    assert report.compactness_decay_active is True
    assert report.long_session_pressure_active is True
    assert report.estimated_avoided_provider_exhaustion == 16
    assert report.estimated_avoided_recursive_fatigue == 11
    assert report.estimated_avoided_premium_burn == 14
    assert report.autonomous_provider_replacement is False


def test_tc_providerfatigue_16_runtime_is_deterministic_and_placeholder_guarded() -> None:
    first = ProviderFatigueRuntime().evaluate()
    second = ProviderFatigueRuntime().evaluate()

    assert first == second
    assert first.deterministic is True
    assert first.provider_fatigue.fatigue_score["OpenMythos placeholder:not_loaded"] == 100
    assert first.recovery.provider_recovery_ranking[-1] == ("OpenMythos placeholder:not_loaded")
    assert first.local_only is True
    assert first.summary_only is True
