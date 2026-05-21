from __future__ import annotations

from ai_dev_os.dev_policy import DevelopmentPolicyRuntime


def test_tc_devpolicy_10_anti_explosion_policy_tracks_pressure() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    anti_explosion = frame.anti_explosion

    assert anti_explosion.roadmap_branching_pressure == "MEDIUM"
    assert anti_explosion.sprint_explosion_pressure == "MEDIUM"
    assert anti_explosion.architecture_expansion_pressure == "MEDIUM"
    assert anti_explosion.governance_expansion_pressure == "MEDIUM"
    assert anti_explosion.continuity_accumulation_pressure == "MEDIUM"
    assert "cap_policy_to_current_sprint" in anti_explosion.compact_anti_explosion_recommendations
    assert anti_explosion.recursive_governance_expansion_prevented is True


def test_tc_devpolicy_11_policy_eviction_preserves_compact_heuristics_only() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    eviction = frame.eviction

    assert eviction.policy_eviction_active is True
    assert eviction.compact_useful_governance_heuristics_only is True
    assert eviction.evicted_obsolete_escalation_heuristics == ("old-high-default",)
    assert eviction.evicted_oversized_governance_history == ("giant-governance-history",)
    assert "human_confirmed_governance_only" in eviction.preserved_compact_governance_heuristics


def test_tc_devpolicy_12_policy_stability_keeps_human_confirmed_enforcement() -> None:
    frame = DevelopmentPolicyRuntime().evaluate()
    stability = frame.stability

    assert stability.policy_stability == "WATCH"
    assert stability.rollout_safety_stability == "WATCH"
    assert stability.local_patch_sustainability is True
    assert stability.human_confirmed_enforcement is True
    assert stability.compact_continuity_stabilized is True
    assert frame.pressure.bounded_policy_only is True
    assert frame.provider_routing_distribution == {"HIGH": 4, "MEDIUM": 3, "LOW": 3}
