from __future__ import annotations

from ai_dev_os.dev_policy import DevelopmentPolicyRuntime


def test_tc_devpolicy_04_architecture_policy_blocks_autonomous_rewrites() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    architecture = frame.architecture

    assert architecture.architecture_sprawl_pressure == "MEDIUM"
    assert architecture.cross_runtime_explosion_attempts == 1
    assert architecture.repo_wide_cognition_attempts == 1
    assert architecture.governance_bypass_attempts == 1
    assert "LOCAL_PATCH_REQUIRED" in architecture.local_patch_reminders
    assert architecture.automatic_architecture_rewrites_prevented is True
    assert architecture.autonomous_runtime_merging_prevented is True
    assert architecture.uncontrolled_dependency_growth_prevented is True


def test_tc_devpolicy_05_provider_escalation_policy_preserves_governance_quality() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    provider = frame.provider

    assert provider.provider_usage_distribution == {"HIGH": 4, "MEDIUM": 3, "LOW": 3}
    assert provider.repeated_high_usage is True
    assert provider.unsafe_escalation_attempts == 1
    assert "HIGH_only_for_boundary_analysis" in provider.downgrade_safe_recommendations
    assert "prefer_LOW_MEDIUM_for_repetitive_policy" in provider.low_medium_routing_encouragement
    assert provider.hidden_provider_switching_prevented is True
    assert provider.unsafe_downgrade_recommendations_prevented is True
    assert provider.governance_quality_collapse_prevented is True


def test_tc_devpolicy_06_policy_violation_frame_is_advisory_gate_only() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    violation = frame.violation

    assert violation.autonomous_enforcement_attempted is True
    assert violation.repository_mutation_attempted is True
    assert violation.hidden_policy_mutation_attempted is True
    assert violation.recursive_governance_expansion_attempted is True
    assert "autonomous_enforcement_blocked" in violation.blocked_violation_warnings
    assert violation.advisory_gate_only is True
