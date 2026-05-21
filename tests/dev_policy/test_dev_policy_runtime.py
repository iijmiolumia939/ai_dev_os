from __future__ import annotations

from ai_dev_os.dev_policy import (
    DEV_POLICY_REQUIREMENT_IDS,
    DEV_POLICY_TEST_IDS,
    DevelopmentPolicyRuntime,
)
from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_tc_devpolicy_01_runtime_is_bounded_human_confirmed_and_advisory() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()

    assert "FR-DEVPOLICY-01" in DEV_POLICY_REQUIREMENT_IDS
    assert "FR-DEVPOLICY-12" in DEV_POLICY_REQUIREMENT_IDS
    assert "NFR-COST-24" in DEV_POLICY_REQUIREMENT_IDS
    assert "TC-DEVPOLICY-01" in DEV_POLICY_TEST_IDS
    assert frame.dev_policy_active is True
    assert frame.bounded_policy_only is True
    assert frame.human_confirmed_governance_only is True
    assert frame.no_autonomous_enforcement is True
    assert frame.no_repository_mutation_authority is True
    assert frame.no_recursive_governance_expansion is True


def test_tc_devpolicy_02_recommendations_are_compact_non_binding_and_deterministic() -> None:
    first = DevelopmentPolicyRuntime().evaluate()
    second = DevelopmentPolicyRuntime().evaluate()

    assert first == second
    assert first.recommendation.non_binding is True
    assert first.recommendation.human_confirmed is True
    assert first.recommendation.compact is True
    assert first.recommendation.deterministic is True
    assert len(first.recommendation.bounded_governance_hints) <= 6
    assert first.local_only is True
    assert first.summary_only is True


def test_tc_devpolicy_03_runtime_audit_reports_policy_flags() -> None:
    report = run_runtime_enforcement_audit().dev_policy

    assert report.dev_policy_active is True
    assert report.architecture_policy_active is True
    assert report.embodiment_realism_policy_active is True
    assert report.provider_escalation_policy_active is True
    assert report.bounded_cognition_policy_active is True
    assert report.anti_explosion_policy_active is True
    assert report.rollout_safety_policy_active is True
    assert report.policy_eviction_active is True
    assert report.estimated_avoided_policy_overhead == 3520
    assert report.estimated_avoided_governance_explosion == 2880
