from __future__ import annotations

from ai_dev_os.dev_execution import DevelopmentExecutionRuntime


def test_tc_devexecution_08_validation_prevents_bypass_and_replay() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    validation = frame.validation

    assert validation.repeated_validation_failures == 1
    assert validation.unstable_execution_patterns == 2
    assert validation.oversized_validation_surfaces == 1
    assert "tests/dev_execution" in validation.scoped_validation_coverage
    assert "full_pytest" in validation.validation_ordering
    assert validation.repo_wide_validation_explosion_prevented is True
    assert validation.giant_validation_replay_prevented is True
    assert validation.hidden_validation_bypass_prevented is True


def test_tc_devexecution_09_pacing_tracks_provider_and_cognition_pressure() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    pacing = frame.pacing

    assert pacing.sprint_pacing_stability == "STABLE"
    assert pacing.execution_density == "MEDIUM"
    assert pacing.provider_burn_pressure == "MEDIUM"
    assert pacing.cognition_expansion_pressure == "MEDIUM"
    assert "reserve_HIGH_for_rollback_governance" in pacing.provider_pacing_suggestions
    assert pacing.sprint_over_expansion_prevented is True
    assert pacing.execution_overload_prevented is True
    assert pacing.giant_cognition_pacing_prevented is True


def test_tc_devexecution_10_scope_caps_retrieval_and_blocks_repo_wide_execution() -> None:
    frame = DevelopmentExecutionRuntime().evaluate()
    scope = frame.scope

    assert scope.execution_retrieval_radius == 2
    assert scope.repo_wide_execution_attempts == 1
    assert scope.local_patch_compliance is True
    assert "LOCAL_PATCH_ONLY" in scope.bounded_execution_reminders
    assert scope.repo_wide_execution_synthesis_prevented is True
    assert scope.hidden_repository_mutation_prevented is True
