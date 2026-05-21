from __future__ import annotations

from ai_dev_os.dev_execution import DevelopmentExecutionRuntime


def test_tc_devexecution_11_rollback_prevents_unsafe_continuation() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    rollback = frame.rollback

    assert rollback.rollback_safe_execution_state == "WATCH"
    assert rollback.staged_checkpoint_stability == "WATCH"
    assert rollback.migration_risk == "MEDIUM"
    assert rollback.provider_escalation_during_execution is True
    assert "human_confirmed_rollback_only" in rollback.rollback_safe_reminders
    assert rollback.unsafe_execution_continuation_prevented is True
    assert rollback.irreversible_sprint_mutations_prevented is True
    assert rollback.hidden_rollback_automation_prevented is True


def test_tc_devexecution_12_failure_and_pressure_stabilize_execution() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    failure = frame.failure
    pressure = frame.pressure

    assert failure.repeated_execution_failures == 1
    assert failure.repeated_rollback_events == 1
    assert failure.unstable_validation_loops == 1
    assert failure.provider_escalation_loops == 1
    assert failure.cognition_explosion_during_execution == 1
    assert "shrink_execution_stage" in failure.stabilization_recommendations
    assert pressure.execution_pressure == "MEDIUM"
    assert pressure.bounded_execution_only is True
    assert frame.provider_routing_distribution == {"HIGH": 4, "MEDIUM": 4, "LOW": 3}
