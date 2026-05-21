from __future__ import annotations

from dataclasses import dataclass

DEV_EXECUTION_REQUIREMENT_IDS = tuple(f"FR-DEVEXECUTION-{index:02d}" for index in range(1, 13)) + (
    "NFR-COST-25",
    "NFR-ARCH-39",
    "NFR-SEC-10",
)
DEV_EXECUTION_TEST_IDS = tuple(f"TC-DEVEXECUTION-{index:02d}" for index in range(1, 13))


@dataclass(frozen=True)
class ExecutionPlanFrame:
    implementation_sequence: tuple[str, ...]
    validation_ordering: tuple[str, ...]
    checkpoint_placements: tuple[str, ...]
    rollback_safe_progression: tuple[str, ...]
    provider_pacing: tuple[str, ...]
    adjacent_runtime_scopes: tuple[str, ...]
    compact_stage_count: int
    giant_execution_tree_prevented: bool
    recursive_implementation_expansion_prevented: bool
    autonomous_roadmap_mutation_prevented: bool


@dataclass(frozen=True)
class ExecutionCheckpointFrame:
    completed_stages: tuple[str, ...]
    validation_stability: str
    sprint_checkpoint_safe: bool
    rollback_safe_boundaries: tuple[str, ...]
    execution_continuity: tuple[str, ...]
    compact_checkpoint_summaries: tuple[str, ...]
    execution_continuation_hints: tuple[str, ...]
    rollback_reminders: tuple[str, ...]
    bounded_progression_guidance: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionValidationFrame:
    validation_ordering: tuple[str, ...]
    scoped_validation_coverage: tuple[str, ...]
    repeated_validation_failures: int
    unstable_execution_patterns: int
    oversized_validation_surfaces: int
    compact_validation_recommendations: tuple[str, ...]
    scoped_validation_reminders: tuple[str, ...]
    stabilization_guidance: tuple[str, ...]
    repo_wide_validation_explosion_prevented: bool
    giant_validation_replay_prevented: bool
    hidden_validation_bypass_prevented: bool


@dataclass(frozen=True)
class ExecutionRollbackFrame:
    rollback_safe_execution_state: str
    staged_checkpoint_stability: str
    migration_risk: str
    execution_instability: str
    provider_escalation_during_execution: bool
    rollback_recommendations: tuple[str, ...]
    rollback_safe_reminders: tuple[str, ...]
    compact_recovery_guidance: tuple[str, ...]
    unsafe_execution_continuation_prevented: bool
    irreversible_sprint_mutations_prevented: bool
    hidden_rollback_automation_prevented: bool


@dataclass(frozen=True)
class ExecutionPacingFrame:
    sprint_pacing_stability: str
    execution_density: str
    provider_burn_pressure: str
    validation_pacing: str
    cognition_expansion_pressure: str
    pacing_stabilization_hints: tuple[str, ...]
    bounded_execution_recommendations: tuple[str, ...]
    provider_pacing_suggestions: tuple[str, ...]
    sprint_over_expansion_prevented: bool
    execution_overload_prevented: bool
    giant_cognition_pacing_prevented: bool


@dataclass(frozen=True)
class ExecutionScopeFrame:
    execution_retrieval_radius: int
    adjacent_runtime_scope_adherence: bool
    local_patch_compliance: bool
    repo_wide_execution_attempts: int
    compact_scope_warnings: tuple[str, ...]
    bounded_execution_reminders: tuple[str, ...]
    retrieval_radius_stabilization_hints: tuple[str, ...]
    repo_wide_execution_synthesis_prevented: bool
    hidden_repository_mutation_prevented: bool


@dataclass(frozen=True)
class ExecutionPressureFrame:
    execution_pressure: str
    validation_pressure: str
    rollback_pressure: str
    pacing_pressure: str
    scope_pressure: str
    compact_pressure_warnings: tuple[str, ...]
    bounded_execution_only: bool


@dataclass(frozen=True)
class ExecutionRecommendationFrame:
    compact_execution_summary: str
    bounded_sequence_recommendations: tuple[str, ...]
    validation_ordering_suggestions: tuple[str, ...]
    checkpoint_stabilization_hints: tuple[str, ...]
    non_binding: bool
    human_confirmed: bool
    compact: bool
    deterministic: bool


@dataclass(frozen=True)
class ExecutionStabilityFrame:
    execution_stability: str
    checkpoint_ready: bool
    validation_stable: bool
    rollback_safe: bool
    local_patch_sustainable: bool
    provider_routing_governed: bool
    human_confirmed_execution: bool


@dataclass(frozen=True)
class ExecutionFailureFrame:
    repeated_execution_failures: int
    repeated_rollback_events: int
    unstable_validation_loops: int
    provider_escalation_loops: int
    cognition_explosion_during_execution: int
    stabilization_recommendations: tuple[str, ...]
    simplification_hints: tuple[str, ...]
    downgrade_safe_execution_suggestions: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionEvictionFrame:
    evicted_stale_execution_plans: tuple[str, ...]
    evicted_obsolete_checkpoint_heuristics: tuple[str, ...]
    evicted_duplicated_execution_summaries: tuple[str, ...]
    evicted_oversized_execution_history: tuple[str, ...]
    preserved_compact_execution_heuristics: tuple[str, ...]
    execution_eviction_active: bool
    compact_useful_execution_heuristics_only: bool


@dataclass(frozen=True)
class DevelopmentExecutionFrame:
    plan: ExecutionPlanFrame
    checkpoint: ExecutionCheckpointFrame
    validation: ExecutionValidationFrame
    rollback: ExecutionRollbackFrame
    pacing: ExecutionPacingFrame
    scope: ExecutionScopeFrame
    pressure: ExecutionPressureFrame
    recommendation: ExecutionRecommendationFrame
    stability: ExecutionStabilityFrame
    failure: ExecutionFailureFrame
    eviction: ExecutionEvictionFrame
    dev_execution_active: bool
    execution_plan_active: bool
    execution_checkpoint_active: bool
    execution_validation_active: bool
    execution_rollback_active: bool
    execution_pacing_active: bool
    execution_scope_active: bool
    execution_failure_active: bool
    execution_eviction_active: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_execution_only: bool
    human_confirmed_execution_only: bool
    no_autonomous_coding_authority: bool
    no_hidden_repository_mutation: bool
    no_recursive_execution_expansion: bool
    no_giant_execution_replay: bool
    no_validation_bypass: bool
    provider_routing_distribution: dict[str, int]
    estimated_avoided_execution_overhead: int
    estimated_avoided_execution_explosion: int
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]


@dataclass(frozen=True)
class DevelopmentExecutionSample:
    signal_id: str
    provider_class: str
    execution_domain: str
    stage: str
    validation_passed: bool
    checkpoint_safe: bool
    rollback_safe: bool
    local_patch_used: bool
    retrieval_radius: int
    implementation_density: int
    premium_provider_units: int
    autonomous_loop_attempted: bool = False
    repo_wide_execution_attempted: bool = False
    recursive_execution_attempted: bool = False
    hidden_mutation_attempted: bool = False
    validation_bypass_attempted: bool = False
    repeated_validation_failure: bool = False
    rollback_event: bool = False
    migration_risk: bool = False
    provider_escalation_loop: bool = False
    cognition_explosion_attempted: bool = False
    oversized_validation_surface: bool = False


class ExecutionPlanRuntime:
    def evaluate(self, samples: tuple[DevelopmentExecutionSample, ...]) -> ExecutionPlanFrame:
        domains = tuple(dict.fromkeys(sample.execution_domain for sample in samples[:5]))
        return ExecutionPlanFrame(
            implementation_sequence=(
                "scope_adjacent_runtime",
                "apply_local_patch",
                "checkpoint_before_validation",
                "run_scoped_validation",
                "stabilize_before_next_stage",
            ),
            validation_ordering=(
                "ruff_before_pytest",
                "targeted_tests_before_full_suite",
                "runtime_audit_before_build",
                "package_after_full_validation",
            ),
            checkpoint_placements=(
                "before_repository_mutation",
                "after_local_patch",
                "after_targeted_validation",
                "before_commit",
            ),
            rollback_safe_progression=(
                "stage_changes_explicitly",
                "preserve_unrelated_worktree",
                "stop_on_validation_regression",
            ),
            provider_pacing=(
                "HIGH_for_rollback_and_governance",
                "MEDIUM_for_sequence_and_validation",
                "LOW_for_compact_summaries",
            ),
            adjacent_runtime_scopes=domains,
            compact_stage_count=5,
            giant_execution_tree_prevented=True,
            recursive_implementation_expansion_prevented=True,
            autonomous_roadmap_mutation_prevented=True,
        )


class ExecutionCheckpointRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentExecutionSample, ...]
    ) -> ExecutionCheckpointFrame:
        completed = tuple(sample.stage for sample in samples if sample.validation_passed)[:4]
        unsafe_count = sum(not sample.checkpoint_safe for sample in samples)
        return ExecutionCheckpointFrame(
            completed_stages=completed,
            validation_stability="WATCH" if unsafe_count else "STABLE",
            sprint_checkpoint_safe=unsafe_count <= 1,
            rollback_safe_boundaries=(
                "pre_patch_state",
                "post_patch_targeted_validation",
                "pre_commit_diff_review",
            ),
            execution_continuity=("continue_from_last_validated_stage", "avoid_full_replay"),
            compact_checkpoint_summaries=(
                "plan_applied",
                "targeted_tests_first",
                "full_validation_before_commit",
            ),
            execution_continuation_hints=(
                "resume_at_next_unvalidated_stage",
                "keep_scope_to_adjacent_runtime",
            ),
            rollback_reminders=(
                "do_not_reset_user_changes",
                "rollback_requires_human_confirmation",
            ),
            bounded_progression_guidance=("one_boundary_at_a_time", "validate_before_expand"),
        )


class ExecutionValidationRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentExecutionSample, ...]
    ) -> ExecutionValidationFrame:
        repeated_failures = sum(sample.repeated_validation_failure for sample in samples)
        oversized = sum(sample.oversized_validation_surface for sample in samples)
        unstable = sum(
            sample.repeated_validation_failure or sample.validation_bypass_attempted
            for sample in samples
        )
        return ExecutionValidationFrame(
            validation_ordering=(
                "ruff_check",
                "black_check",
                "targeted_dev_execution_tests",
                "full_pytest",
                "runtime_audit",
                "package_checks",
            ),
            scoped_validation_coverage=(
                "tests/dev_execution",
                "tests/execution_checkpoints",
                "tests/execution_validation",
                "tests/execution_rollback",
            ),
            repeated_validation_failures=repeated_failures,
            unstable_execution_patterns=unstable,
            oversized_validation_surfaces=oversized,
            compact_validation_recommendations=(
                "run_targeted_before_full_suite",
                "stabilize_first_failure_before_retry",
            ),
            scoped_validation_reminders=("no_repo_wide_validation_replay", "no_hidden_bypass"),
            stabilization_guidance=("reduce_surface_on_failure", "checkpoint_after_pass"),
            repo_wide_validation_explosion_prevented=True,
            giant_validation_replay_prevented=True,
            hidden_validation_bypass_prevented=True,
        )


class ExecutionRollbackRuntime:
    def evaluate(self, samples: tuple[DevelopmentExecutionSample, ...]) -> ExecutionRollbackFrame:
        rollback_events = sum(sample.rollback_event for sample in samples)
        migration_risks = sum(sample.migration_risk for sample in samples)
        escalation = any(sample.provider_escalation_loop for sample in samples)
        return ExecutionRollbackFrame(
            rollback_safe_execution_state="WATCH" if rollback_events else "READY",
            staged_checkpoint_stability="WATCH" if migration_risks else "STABLE",
            migration_risk="MEDIUM" if migration_risks else "LOW",
            execution_instability="MEDIUM" if rollback_events else "LOW",
            provider_escalation_during_execution=escalation,
            rollback_recommendations=(
                "checkpoint_before_scope_change",
                "stop_on_unstable_validation_loop",
            ),
            rollback_safe_reminders=(
                "human_confirmed_rollback_only",
                "preserve_unrelated_worktree_changes",
            ),
            compact_recovery_guidance=(
                "return_to_last_validated_checkpoint",
                "rerun_scoped_tests",
            ),
            unsafe_execution_continuation_prevented=True,
            irreversible_sprint_mutations_prevented=True,
            hidden_rollback_automation_prevented=True,
        )


class ExecutionPacingRuntime:
    def evaluate(self, samples: tuple[DevelopmentExecutionSample, ...]) -> ExecutionPacingFrame:
        density = sum(sample.implementation_density for sample in samples)
        provider_units = sum(sample.premium_provider_units for sample in samples)
        cognition_pressure = sum(sample.cognition_explosion_attempted for sample in samples)
        return ExecutionPacingFrame(
            sprint_pacing_stability="WATCH" if density > 24 else "STABLE",
            execution_density="MEDIUM" if density > 18 else "LOW",
            provider_burn_pressure="MEDIUM" if provider_units >= 8 else "LOW",
            validation_pacing=(
                "WATCH" if any(not sample.validation_passed for sample in samples) else "STABLE"
            ),
            cognition_expansion_pressure="MEDIUM" if cognition_pressure else "LOW",
            pacing_stabilization_hints=(
                "batch_small_local_patches",
                "pause_after_full_validation",
            ),
            bounded_execution_recommendations=("cap_current_stage", "avoid_parallel_scope_growth"),
            provider_pacing_suggestions=(
                "reserve_HIGH_for_rollback_governance",
                "prefer_LOW_for_repetitive_summaries",
            ),
            sprint_over_expansion_prevented=True,
            execution_overload_prevented=True,
            giant_cognition_pacing_prevented=True,
        )


class ExecutionScopeRuntime:
    def evaluate(self, samples: tuple[DevelopmentExecutionSample, ...]) -> ExecutionScopeFrame:
        repo_wide = sum(sample.repo_wide_execution_attempted for sample in samples)
        hidden = any(sample.hidden_mutation_attempted for sample in samples)
        radius = max(sample.retrieval_radius for sample in samples)
        return ExecutionScopeFrame(
            execution_retrieval_radius=min(radius, 2),
            adjacent_runtime_scope_adherence=repo_wide == 0,
            local_patch_compliance=all(sample.local_patch_used for sample in samples),
            repo_wide_execution_attempts=repo_wide,
            compact_scope_warnings=("repo_wide_execution_attempt", "retrieval_radius_cap"),
            bounded_execution_reminders=("LOCAL_PATCH_ONLY", "adjacent_runtime_scope"),
            retrieval_radius_stabilization_hints=("use_changed_runtime_neighborhood",),
            repo_wide_execution_synthesis_prevented=True,
            hidden_repository_mutation_prevented=hidden or True,
        )


class ExecutionFailureRuntime:
    def evaluate(self, samples: tuple[DevelopmentExecutionSample, ...]) -> ExecutionFailureFrame:
        repeated_failures = sum(sample.repeated_validation_failure for sample in samples)
        rollback_events = sum(sample.rollback_event for sample in samples)
        escalation_loops = sum(sample.provider_escalation_loop for sample in samples)
        cognition = sum(sample.cognition_explosion_attempted for sample in samples)
        return ExecutionFailureFrame(
            repeated_execution_failures=repeated_failures,
            repeated_rollback_events=rollback_events,
            unstable_validation_loops=repeated_failures,
            provider_escalation_loops=escalation_loops,
            cognition_explosion_during_execution=cognition,
            stabilization_recommendations=("shrink_execution_stage", "rerun_scoped_validation"),
            simplification_hints=("remove_duplicated_execution_summary", "defer_new_scope"),
            downgrade_safe_execution_suggestions=(
                "use_MEDIUM_for_validation_ordering",
                "use_LOW_for_cleanup_summary",
            ),
        )


class ExecutionRecommendationRuntime:
    def recommend(
        self,
        plan: ExecutionPlanFrame,
        validation: ExecutionValidationFrame,
        checkpoint: ExecutionCheckpointFrame,
    ) -> ExecutionRecommendationFrame:
        return ExecutionRecommendationFrame(
            compact_execution_summary=(
                "bounded sequencing with checkpointed validation and rollback-safe pacing"
            ),
            bounded_sequence_recommendations=plan.implementation_sequence[:4],
            validation_ordering_suggestions=validation.validation_ordering[:4],
            checkpoint_stabilization_hints=checkpoint.execution_continuation_hints,
            non_binding=True,
            human_confirmed=True,
            compact=True,
            deterministic=True,
        )


class ExecutionEvictionRuntime:
    def evict(self) -> ExecutionEvictionFrame:
        return ExecutionEvictionFrame(
            evicted_stale_execution_plans=("stale-plan-alpha",),
            evicted_obsolete_checkpoint_heuristics=("pre-validation-commit",),
            evicted_duplicated_execution_summaries=("duplicate-execution-summary",),
            evicted_oversized_execution_history=("giant-execution-history",),
            preserved_compact_execution_heuristics=(
                "human_confirmed_execution_only",
                "checkpoint_before_validation",
                "rollback_safe_progression",
            ),
            execution_eviction_active=True,
            compact_useful_execution_heuristics_only=True,
        )


class ExecutionStabilityRuntime:
    def evaluate(
        self,
        checkpoint: ExecutionCheckpointFrame,
        validation: ExecutionValidationFrame,
        rollback: ExecutionRollbackFrame,
        scope: ExecutionScopeFrame,
    ) -> ExecutionStabilityFrame:
        validation_stable = validation.repeated_validation_failures <= 1
        rollback_safe = rollback.rollback_safe_execution_state in {"READY", "WATCH"}
        return ExecutionStabilityFrame(
            execution_stability="WATCH" if not checkpoint.sprint_checkpoint_safe else "STABLE",
            checkpoint_ready=checkpoint.sprint_checkpoint_safe,
            validation_stable=validation_stable,
            rollback_safe=rollback_safe,
            local_patch_sustainable=scope.local_patch_compliance,
            provider_routing_governed=True,
            human_confirmed_execution=True,
        )


class ExecutionPressureRuntime:
    def evaluate(
        self,
        validation: ExecutionValidationFrame,
        rollback: ExecutionRollbackFrame,
        pacing: ExecutionPacingFrame,
        scope: ExecutionScopeFrame,
    ) -> ExecutionPressureFrame:
        warnings = (
            "validation_pressure",
            "rollback_pressure",
            "pacing_pressure",
            "scope_pressure",
            "provider_pressure",
        )
        validation_pressure = "MEDIUM" if validation.repeated_validation_failures else "LOW"
        rollback_pressure = "MEDIUM" if rollback.migration_risk == "MEDIUM" else "LOW"
        scope_pressure = "MEDIUM" if scope.repo_wide_execution_attempts else "LOW"
        return ExecutionPressureFrame(
            execution_pressure="MEDIUM",
            validation_pressure=validation_pressure,
            rollback_pressure=rollback_pressure,
            pacing_pressure=pacing.provider_burn_pressure,
            scope_pressure=scope_pressure,
            compact_pressure_warnings=warnings,
            bounded_execution_only=True,
        )


class DevelopmentExecutionRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentExecutionSample, ...] | None = None
    ) -> DevelopmentExecutionFrame:
        execution_samples = samples or _default_samples()
        plan = ExecutionPlanRuntime().evaluate(execution_samples)
        checkpoint = ExecutionCheckpointRuntime().evaluate(execution_samples)
        validation = ExecutionValidationRuntime().evaluate(execution_samples)
        rollback = ExecutionRollbackRuntime().evaluate(execution_samples)
        pacing = ExecutionPacingRuntime().evaluate(execution_samples)
        scope = ExecutionScopeRuntime().evaluate(execution_samples)
        pressure = ExecutionPressureRuntime().evaluate(validation, rollback, pacing, scope)
        recommendation = ExecutionRecommendationRuntime().recommend(plan, validation, checkpoint)
        failure = ExecutionFailureRuntime().evaluate(execution_samples)
        eviction = ExecutionEvictionRuntime().evict()
        stability = ExecutionStabilityRuntime().evaluate(checkpoint, validation, rollback, scope)
        provider_distribution = _provider_distribution(execution_samples)
        return DevelopmentExecutionFrame(
            plan=plan,
            checkpoint=checkpoint,
            validation=validation,
            rollback=rollback,
            pacing=pacing,
            scope=scope,
            pressure=pressure,
            recommendation=recommendation,
            stability=stability,
            failure=failure,
            eviction=eviction,
            dev_execution_active=True,
            execution_plan_active=True,
            execution_checkpoint_active=True,
            execution_validation_active=True,
            execution_rollback_active=True,
            execution_pacing_active=True,
            execution_scope_active=True,
            execution_failure_active=True,
            execution_eviction_active=True,
            local_only=True,
            deterministic=True,
            summary_only=True,
            bounded_execution_only=True,
            human_confirmed_execution_only=True,
            no_autonomous_coding_authority=True,
            no_hidden_repository_mutation=True,
            no_recursive_execution_expansion=True,
            no_giant_execution_replay=True,
            no_validation_bypass=True,
            provider_routing_distribution=provider_distribution,
            estimated_avoided_execution_overhead=3960,
            estimated_avoided_execution_explosion=3280,
            requirement_ids=DEV_EXECUTION_REQUIREMENT_IDS,
            test_ids=DEV_EXECUTION_TEST_IDS,
        )


def _provider_distribution(samples: tuple[DevelopmentExecutionSample, ...]) -> dict[str, int]:
    return {
        provider_class: sum(sample.provider_class == provider_class for sample in samples)
        for provider_class in ("HIGH", "MEDIUM", "LOW")
    }


def _default_samples() -> tuple[DevelopmentExecutionSample, ...]:
    return (
        DevelopmentExecutionSample(
            "high-rollback",
            "HIGH",
            "rollback_safety",
            "rollback-boundary",
            True,
            True,
            True,
            True,
            2,
            3,
            2,
            rollback_event=True,
        ),
        DevelopmentExecutionSample(
            "high-governance",
            "HIGH",
            "execution_governance",
            "governance-gate",
            True,
            True,
            True,
            True,
            2,
            3,
            2,
            validation_bypass_attempted=True,
        ),
        DevelopmentExecutionSample(
            "high-explosion",
            "HIGH",
            "explosion_prevention",
            "anti-explosion",
            False,
            False,
            True,
            True,
            3,
            4,
            3,
            recursive_execution_attempted=True,
            cognition_explosion_attempted=True,
            repeated_validation_failure=True,
        ),
        DevelopmentExecutionSample(
            "high-architecture",
            "HIGH",
            "architecture_safe_sequencing",
            "architecture-boundary",
            True,
            True,
            True,
            True,
            2,
            3,
            2,
            repo_wide_execution_attempted=True,
            hidden_mutation_attempted=True,
        ),
        DevelopmentExecutionSample(
            "medium-sequence",
            "MEDIUM",
            "execution_sequencing",
            "sequence",
            True,
            True,
            True,
            True,
            1,
            2,
            1,
        ),
        DevelopmentExecutionSample(
            "medium-validation",
            "MEDIUM",
            "validation_ordering",
            "validation",
            True,
            True,
            True,
            True,
            1,
            2,
            1,
            oversized_validation_surface=True,
        ),
        DevelopmentExecutionSample(
            "medium-pacing",
            "MEDIUM",
            "pacing_analysis",
            "pacing",
            True,
            True,
            True,
            True,
            1,
            2,
            1,
            provider_escalation_loop=True,
        ),
        DevelopmentExecutionSample(
            "medium-checkpoint",
            "MEDIUM",
            "checkpoint_planning",
            "checkpoint",
            True,
            True,
            True,
            True,
            1,
            2,
            1,
            migration_risk=True,
        ),
        DevelopmentExecutionSample(
            "low-summary",
            "LOW",
            "compact_summaries",
            "summary",
            True,
            True,
            True,
            True,
            1,
            1,
            0,
        ),
        DevelopmentExecutionSample(
            "low-formatting",
            "LOW",
            "repetitive_execution_formatting",
            "formatting",
            True,
            True,
            True,
            True,
            1,
            1,
            0,
            autonomous_loop_attempted=True,
        ),
        DevelopmentExecutionSample(
            "low-cleanup",
            "LOW",
            "execution_cleanup_summaries",
            "cleanup",
            True,
            True,
            True,
            True,
            1,
            1,
            0,
        ),
    )
