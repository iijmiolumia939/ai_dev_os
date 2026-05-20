from __future__ import annotations

import inspect

from ai_dev_os.governance_health.health_score import GovernanceHealthPolicy
from ai_dev_os.governance_health.pressure_aggregation import GovernancePressurePolicy
from ai_dev_os.governance_health.risk_aggregation import GovernanceRiskPolicy
from ai_dev_os.governance_health.stability_assessment import GovernanceStabilityPolicy


def test_governance_score_validation() -> None:
    frame = GovernanceHealthPolicy().score(
        session_lifecycle="low",
        stale_context_pressure="medium",
        persistence_pressure="medium",
        retrieval_scaling_pressure="low",
        provider_simulation_pressure="low",
        architecture_isolation_pressure="low",
        schema_migration_pressure="medium",
        checkpoint_rotation_pressure="low",
        workspace_contamination_risk=False,
    )

    assert 0 <= frame.governance_health_score <= 100
    assert frame.governance_health_state in {
        "HEALTHY",
        "STABLE_WARNING",
        "HIGH_PRESSURE",
        "CRITICAL_GOVERNANCE",
    }
    assert frame.governance_attention_required is (frame.governance_health_state != "HEALTHY")


def test_pressure_aggregation_validation() -> None:
    frame = GovernancePressurePolicy().aggregate(
        retrieval_pressure="medium",
        persistence_pressure="high",
        session_pressure="medium",
        architecture_pressure="low",
        provider_pressure="low",
        continuity_pressure="high",
        checkpoint_pressure="high",
        stale_context_pressure="medium",
        previous_pressure="low",
    )

    assert frame.aggregate_pressure in {"medium", "high"}
    assert frame.dominant_pressure in {
        "persistence",
        "continuity",
        "checkpoint",
    }
    assert frame.pressure_direction == "rising"
    assert frame.pressure_trend


def test_risk_aggregation_validation() -> None:
    frame = GovernanceRiskPolicy().aggregate(
        stale_continuity_risk=True,
        hidden_context_drift=True,
        architecture_contamination=True,
        retrieval_explosion=False,
        persistence_explosion=True,
        checkpoint_explosion=True,
        provider_lock_in_risk=False,
        governance_runtime_drift=True,
        prompt_mode_drift=True,
    )

    assert frame.aggregate_risk in {"high", "critical"}
    assert frame.highest_risk == "architecture_contamination"
    assert frame.isolation_recommended is True
    assert frame.compact_recommended is True
    assert frame.rollover_recommended is True


def test_stability_assessment_validation() -> None:
    frame = GovernanceStabilityPolicy().assess(
        bounded_governance_maintained=True,
        uncontrolled_expansion_detected=False,
        stale_governance_accumulation=True,
        governance_oscillation=False,
        repeated_rollover_instability=True,
        persistence_instability=True,
        retrieval_instability=False,
    )

    assert frame.stability_score < 100
    assert frame.instability_detected is True
    assert frame.stabilization_recommended is True
    assert frame.compact_governance_recommended is True


def test_no_network_dependency_or_autonomous_enforcement() -> None:
    import ai_dev_os.governance_health.governance_dashboard as dashboard
    import ai_dev_os.governance_health.health_score as health
    import ai_dev_os.governance_health.pressure_aggregation as pressure
    import ai_dev_os.governance_health.risk_aggregation as risk
    import ai_dev_os.governance_health.stability_assessment as stability

    source = "\n".join(
        inspect.getsource(module) for module in (dashboard, health, pressure, risk, stability)
    ).lower()

    assert "requests" not in source
    assert "http" not in source
    assert "subprocess" not in source
    assert "shutdown" not in source
    assert "git commit" not in source
    assert "git push" not in source
    assert "upload(" not in source


def test_runtime_audit_reports_governance_health() -> None:
    from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

    report = run_runtime_enforcement_audit()

    assert report.governance_health.governance_health_active is True
    assert report.governance_health.governance_pressure_active is True
    assert report.governance_health.governance_risk_active is True
    assert report.governance_health.governance_dashboard_active is True
    assert report.governance_health.governance_stability_active is True
    assert report.governance_health.estimated_avoided_governance_drift > 0
