from __future__ import annotations

from dataclasses import dataclass

DEV_POLICY_REQUIREMENT_IDS = tuple(f"FR-DEVPOLICY-{index:02d}" for index in range(1, 13)) + (
    "NFR-COST-24",
    "NFR-ARCH-38",
    "NFR-SEC-09",
)
DEV_POLICY_TEST_IDS = tuple(f"TC-DEVPOLICY-{index:02d}" for index in range(1, 13))


@dataclass(frozen=True)
class ArchitectureProtectionPolicyFrame:
    architecture_sprawl_pressure: str
    cross_runtime_explosion_attempts: int
    repo_wide_cognition_attempts: int
    oversized_sprint_patterns: int
    governance_bypass_attempts: int
    compact_architecture_warnings: tuple[str, ...]
    stabilization_recommendations: tuple[str, ...]
    simplification_hints: tuple[str, ...]
    local_patch_reminders: tuple[str, ...]
    automatic_architecture_rewrites_prevented: bool
    autonomous_runtime_merging_prevented: bool
    uncontrolled_dependency_growth_prevented: bool


@dataclass(frozen=True)
class EmbodimentRealismPolicyFrame:
    animation_authority_creep: bool
    exaggerated_reaction_escalation: bool
    procedural_acting_pressure: bool
    emotional_over_performance: bool
    high_amplitude_embodiment_drift: bool
    low_motion_realism_reminders: tuple[str, ...]
    subtle_continuity_recommendations: tuple[str, ...]
    renderer_neutral_reminders: tuple[str, ...]
    authority_boundary_warnings: tuple[str, ...]
    theatrical_embodiment_escalation_prevented: bool
    procedural_acting_systems_prevented: bool
    autonomous_social_scripting_prevented: bool


@dataclass(frozen=True)
class ProviderEscalationPolicyFrame:
    provider_usage_distribution: dict[str, int]
    repeated_high_usage: bool
    unsafe_escalation_attempts: int
    premium_provider_dependency: str
    unnecessary_reasoning_expansion: int
    sprint_burn_pressure: str
    downgrade_safe_recommendations: tuple[str, ...]
    bounded_provider_hints: tuple[str, ...]
    low_medium_routing_encouragement: tuple[str, ...]
    escalation_pressure_warnings: tuple[str, ...]
    hidden_provider_switching_prevented: bool
    unsafe_downgrade_recommendations_prevented: bool
    governance_quality_collapse_prevented: bool


@dataclass(frozen=True)
class BoundedCognitionPolicyFrame:
    repo_wide_reasoning_attempts: int
    giant_continuity_payloads: int
    oversized_sprint_synthesis_attempts: int
    retrieval_explosion_patterns: int
    recursive_planning_attempts: int
    bounded_retrieval_reminders: tuple[str, ...]
    compact_continuity_hints: tuple[str, ...]
    delta_only_reminders: tuple[str, ...]
    local_patch_governance_hints: tuple[str, ...]
    giant_cognition_replay_prevented: bool
    hidden_memory_accumulation_prevented: bool
    recursive_roadmap_synthesis_prevented: bool


@dataclass(frozen=True)
class AntiExplosionPolicyFrame:
    roadmap_branching_pressure: str
    sprint_explosion_pressure: str
    architecture_expansion_pressure: str
    governance_expansion_pressure: str
    continuity_accumulation_pressure: str
    compact_anti_explosion_recommendations: tuple[str, ...]
    stabilization_warnings: tuple[str, ...]
    simplification_guidance: tuple[str, ...]
    bounded_scope_reminders: tuple[str, ...]
    recursive_governance_expansion_prevented: bool


@dataclass(frozen=True)
class RolloutSafetyPolicyFrame:
    rollout_friction: str
    stale_extension_state: bool
    continuity_mismatch: bool
    unsafe_migration_attempts: int
    oversized_rollout_scope: bool
    rollback_safe_recommendations: tuple[str, ...]
    compact_rollout_guidance: tuple[str, ...]
    migration_stabilization_hints: tuple[str, ...]
    unsafe_rollout_escalation_prevented: bool
    hidden_migration_mutations_prevented: bool
    uncontrolled_rollout_automation_prevented: bool


@dataclass(frozen=True)
class PolicyPressureFrame:
    policy_pressure: str
    governance_pressure: str
    escalation_pressure: str
    architecture_pressure: str
    realism_pressure: str
    rollout_pressure: str
    compact_pressure_warnings: tuple[str, ...]
    bounded_policy_only: bool


@dataclass(frozen=True)
class PolicyRecommendationFrame:
    compact_policy_summary: str
    bounded_governance_hints: tuple[str, ...]
    stabilization_opportunities: tuple[str, ...]
    escalation_pressure_guidance: tuple[str, ...]
    non_binding: bool
    human_confirmed: bool
    compact: bool
    deterministic: bool


@dataclass(frozen=True)
class PolicyEvictionFrame:
    evicted_stale_policy_hints: tuple[str, ...]
    evicted_obsolete_escalation_heuristics: tuple[str, ...]
    evicted_duplicated_policy_summaries: tuple[str, ...]
    evicted_oversized_governance_history: tuple[str, ...]
    preserved_compact_governance_heuristics: tuple[str, ...]
    policy_eviction_active: bool
    compact_useful_governance_heuristics_only: bool


@dataclass(frozen=True)
class PolicyViolationFrame:
    autonomous_enforcement_attempted: bool
    human_intent_override_attempted: bool
    repository_mutation_attempted: bool
    hidden_policy_mutation_attempted: bool
    recursive_governance_expansion_attempted: bool
    blocked_violation_warnings: tuple[str, ...]
    advisory_gate_only: bool


@dataclass(frozen=True)
class PolicyStabilityFrame:
    policy_stability: str
    rollout_safety_stability: str
    local_patch_sustainability: bool
    human_confirmed_enforcement: bool
    compact_continuity_stabilized: bool
    governance_scope_stable: bool


@dataclass(frozen=True)
class DevelopmentPolicyFrame:
    architecture: ArchitectureProtectionPolicyFrame
    embodiment: EmbodimentRealismPolicyFrame
    provider: ProviderEscalationPolicyFrame
    cognition: BoundedCognitionPolicyFrame
    anti_explosion: AntiExplosionPolicyFrame
    rollout: RolloutSafetyPolicyFrame
    pressure: PolicyPressureFrame
    recommendation: PolicyRecommendationFrame
    eviction: PolicyEvictionFrame
    violation: PolicyViolationFrame
    stability: PolicyStabilityFrame
    dev_policy_active: bool
    architecture_policy_active: bool
    embodiment_realism_policy_active: bool
    provider_escalation_policy_active: bool
    bounded_cognition_policy_active: bool
    anti_explosion_policy_active: bool
    rollout_safety_policy_active: bool
    policy_eviction_active: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_policy_only: bool
    human_confirmed_governance_only: bool
    no_autonomous_enforcement: bool
    no_repository_mutation_authority: bool
    no_hidden_provider_switching: bool
    no_recursive_governance_expansion: bool
    no_giant_policy_replay: bool
    provider_routing_distribution: dict[str, int]
    estimated_avoided_policy_overhead: int
    estimated_avoided_governance_explosion: int
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]


@dataclass(frozen=True)
class DevelopmentPolicySample:
    signal_id: str
    provider_class: str
    policy_domain: str
    governance_stable: bool
    local_patch_used: bool
    rollout_safe: bool
    continuity_tokens: int
    sprint_size: int
    retrieval_radius: int
    premium_provider_units: int
    architecture_sprawl_attempted: bool = False
    repo_wide_cognition_attempted: bool = False
    governance_bypass_attempted: bool = False
    animation_authority_creep_attempted: bool = False
    high_amplitude_reaction_attempted: bool = False
    procedural_acting_attempted: bool = False
    unsafe_escalation_attempted: bool = False
    recursive_planning_attempted: bool = False
    unsafe_migration_attempted: bool = False
    autonomous_enforcement_attempted: bool = False
    repository_mutation_attempted: bool = False
    hidden_policy_mutation_attempted: bool = False


class ArchitectureProtectionPolicyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentPolicySample, ...]
    ) -> ArchitectureProtectionPolicyFrame:
        sprawl = sum(sample.architecture_sprawl_attempted for sample in samples)
        repo_wide = sum(sample.repo_wide_cognition_attempted for sample in samples)
        bypass = sum(sample.governance_bypass_attempted for sample in samples)
        oversized = sum(sample.sprint_size > 4 for sample in samples)
        return ArchitectureProtectionPolicyFrame(
            architecture_sprawl_pressure="MEDIUM" if sprawl else "LOW",
            cross_runtime_explosion_attempts=sprawl,
            repo_wide_cognition_attempts=repo_wide,
            oversized_sprint_patterns=oversized,
            governance_bypass_attempts=bypass,
            compact_architecture_warnings=(
                "architecture_sprawl_attempt",
                "repo_wide_cognition_attempt",
                "governance_bypass_attempt",
            ),
            stabilization_recommendations=(
                "freeze_runtime_boundary",
                "require_human_architecture_gate",
            ),
            simplification_hints=("split_policy_from_implementation", "keep_adjacent_runtime"),
            local_patch_reminders=("LOCAL_PATCH_REQUIRED", "no_repo_wide_rewrite"),
            automatic_architecture_rewrites_prevented=True,
            autonomous_runtime_merging_prevented=True,
            uncontrolled_dependency_growth_prevented=True,
        )


class EmbodimentRealismPolicyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentPolicySample, ...]
    ) -> EmbodimentRealismPolicyFrame:
        animation = any(sample.animation_authority_creep_attempted for sample in samples)
        amplitude = any(sample.high_amplitude_reaction_attempted for sample in samples)
        acting = any(sample.procedural_acting_attempted for sample in samples)
        return EmbodimentRealismPolicyFrame(
            animation_authority_creep=animation,
            exaggerated_reaction_escalation=amplitude,
            procedural_acting_pressure=acting,
            emotional_over_performance=amplitude,
            high_amplitude_embodiment_drift=amplitude,
            low_motion_realism_reminders=("prefer_low_motion_presence",),
            subtle_continuity_recommendations=("preserve_subtle_reaction_band",),
            renderer_neutral_reminders=("policy_must_not_require_renderer_authority",),
            authority_boundary_warnings=(
                "animation_authority_creep_blocked",
                "autonomous_social_scripting_forbidden",
            ),
            theatrical_embodiment_escalation_prevented=True,
            procedural_acting_systems_prevented=True,
            autonomous_social_scripting_prevented=True,
        )


class ProviderEscalationPolicyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentPolicySample, ...]
    ) -> ProviderEscalationPolicyFrame:
        distribution = _provider_distribution(samples)
        unsafe = sum(sample.unsafe_escalation_attempted for sample in samples)
        premium_units = _premium_units(samples)
        reasoning_expansion = sum(sample.repo_wide_cognition_attempted for sample in samples)
        return ProviderEscalationPolicyFrame(
            provider_usage_distribution=distribution,
            repeated_high_usage=distribution["HIGH"] >= 3,
            unsafe_escalation_attempts=unsafe,
            premium_provider_dependency="MEDIUM" if premium_units > 3 else "LOW",
            unnecessary_reasoning_expansion=reasoning_expansion,
            sprint_burn_pressure="MEDIUM" if premium_units > 3 else "LOW",
            downgrade_safe_recommendations=(
                "LOW_for_policy_summary",
                "MEDIUM_for_policy_prioritization",
                "HIGH_only_for_boundary_analysis",
            ),
            bounded_provider_hints=("visible_escalation_reason_required",),
            low_medium_routing_encouragement=("prefer_LOW_MEDIUM_for_repetitive_policy",),
            escalation_pressure_warnings=("premium_policy_pressure",) if premium_units > 3 else (),
            hidden_provider_switching_prevented=True,
            unsafe_downgrade_recommendations_prevented=True,
            governance_quality_collapse_prevented=True,
        )


class BoundedCognitionPolicyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentPolicySample, ...]
    ) -> BoundedCognitionPolicyFrame:
        repo_wide = sum(sample.repo_wide_cognition_attempted for sample in samples)
        giant_payloads = sum(sample.continuity_tokens > 3200 for sample in samples)
        oversized = sum(sample.sprint_size > 4 for sample in samples)
        retrieval = sum(sample.retrieval_radius > 2 for sample in samples)
        recursive = sum(sample.recursive_planning_attempted for sample in samples)
        return BoundedCognitionPolicyFrame(
            repo_wide_reasoning_attempts=repo_wide,
            giant_continuity_payloads=giant_payloads,
            oversized_sprint_synthesis_attempts=oversized,
            retrieval_explosion_patterns=retrieval,
            recursive_planning_attempts=recursive,
            bounded_retrieval_reminders=("radius_1_summary", "radius_2_boundary_check"),
            compact_continuity_hints=("summary_only_policy_context",),
            delta_only_reminders=("delta_only_governance",),
            local_patch_governance_hints=("LOCAL_PATCH_REQUIRED",),
            giant_cognition_replay_prevented=True,
            hidden_memory_accumulation_prevented=True,
            recursive_roadmap_synthesis_prevented=True,
        )


class AntiExplosionPolicyRuntime:
    def evaluate(self, samples: tuple[DevelopmentPolicySample, ...]) -> AntiExplosionPolicyFrame:
        roadmap = any(sample.recursive_planning_attempted for sample in samples)
        sprint = any(sample.sprint_size > 4 for sample in samples)
        architecture = any(sample.architecture_sprawl_attempted for sample in samples)
        governance = any(sample.governance_bypass_attempted for sample in samples)
        continuity = any(sample.continuity_tokens > 3200 for sample in samples)
        return AntiExplosionPolicyFrame(
            roadmap_branching_pressure="MEDIUM" if roadmap else "LOW",
            sprint_explosion_pressure="MEDIUM" if sprint else "LOW",
            architecture_expansion_pressure="MEDIUM" if architecture else "LOW",
            governance_expansion_pressure="MEDIUM" if governance else "LOW",
            continuity_accumulation_pressure="MEDIUM" if continuity else "LOW",
            compact_anti_explosion_recommendations=(
                "cap_policy_to_current_sprint",
                "evict_oversized_governance_history",
            ),
            stabilization_warnings=("recursive_policy_expansion_blocked",),
            simplification_guidance=("collapse_duplicate_policy_hints",),
            bounded_scope_reminders=("one_policy_runtime_neighborhood",),
            recursive_governance_expansion_prevented=True,
        )


class RolloutSafetyPolicyRuntime:
    def evaluate(self, samples: tuple[DevelopmentPolicySample, ...]) -> RolloutSafetyPolicyFrame:
        unsafe_migrations = sum(sample.unsafe_migration_attempted for sample in samples)
        unsafe_rollout = unsafe_migrations > 0 or not all(
            sample.rollout_safe for sample in samples
        )
        return RolloutSafetyPolicyFrame(
            rollout_friction="MEDIUM" if unsafe_rollout else "LOW",
            stale_extension_state=unsafe_rollout,
            continuity_mismatch=any(sample.continuity_tokens > 3200 for sample in samples),
            unsafe_migration_attempts=unsafe_migrations,
            oversized_rollout_scope=any(sample.sprint_size > 4 for sample in samples),
            rollback_safe_recommendations=("keep_rollback_file_level",),
            compact_rollout_guidance=("human_review_before_migration",),
            migration_stabilization_hints=("no_hidden_migration_mutation",),
            unsafe_rollout_escalation_prevented=True,
            hidden_migration_mutations_prevented=True,
            uncontrolled_rollout_automation_prevented=True,
        )


class PolicyPressureRuntime:
    def evaluate(
        self,
        *,
        architecture: ArchitectureProtectionPolicyFrame,
        embodiment: EmbodimentRealismPolicyFrame,
        provider: ProviderEscalationPolicyFrame,
        anti_explosion: AntiExplosionPolicyFrame,
        rollout: RolloutSafetyPolicyFrame,
    ) -> PolicyPressureFrame:
        warnings = tuple(
            warning
            for warning in (
                "governance_pressure" if architecture.governance_bypass_attempts else "",
                "escalation_pressure" if provider.repeated_high_usage else "",
                "realism_pressure" if embodiment.high_amplitude_embodiment_drift else "",
                "rollout_pressure" if rollout.rollout_friction != "LOW" else "",
                (
                    "anti_explosion_pressure"
                    if anti_explosion.sprint_explosion_pressure != "LOW"
                    else ""
                ),
            )
            if warning
        )
        return PolicyPressureFrame(
            policy_pressure="MEDIUM" if warnings else "LOW",
            governance_pressure="MEDIUM" if architecture.governance_bypass_attempts else "LOW",
            escalation_pressure="MEDIUM" if provider.repeated_high_usage else "LOW",
            architecture_pressure=architecture.architecture_sprawl_pressure,
            realism_pressure="MEDIUM" if embodiment.high_amplitude_embodiment_drift else "LOW",
            rollout_pressure=rollout.rollout_friction,
            compact_pressure_warnings=warnings,
            bounded_policy_only=True,
        )


class PolicyRecommendationRuntime:
    def recommend(
        self,
        *,
        architecture: ArchitectureProtectionPolicyFrame,
        provider: ProviderEscalationPolicyFrame,
        anti_explosion: AntiExplosionPolicyFrame,
        rollout: RolloutSafetyPolicyFrame,
    ) -> PolicyRecommendationFrame:
        hints = _dedupe(
            architecture.stabilization_recommendations
            + provider.downgrade_safe_recommendations
            + anti_explosion.compact_anti_explosion_recommendations
            + rollout.rollback_safe_recommendations
        )[:6]
        return PolicyRecommendationFrame(
            compact_policy_summary="policy=advisory gate; enforcement=human-confirmed",
            bounded_governance_hints=hints,
            stabilization_opportunities=architecture.simplification_hints[:3],
            escalation_pressure_guidance=(
                "HIGH_only_for_governance_boundary",
                "LOW_for_repetitive_policy_formatting",
            ),
            non_binding=True,
            human_confirmed=True,
            compact=True,
            deterministic=True,
        )


class PolicyEvictionRuntime:
    def evict(
        self,
        *,
        policy_hints: tuple[str, ...],
        obsolete_escalation: tuple[str, ...] = (),
        duplicated_summaries: tuple[str, ...] = (),
        oversized_history: tuple[str, ...] = (),
    ) -> PolicyEvictionFrame:
        active_hints = _dedupe(policy_hints)[-5:]
        stale = tuple(hint for hint in policy_hints if hint not in active_hints)
        preserved = _dedupe(active_hints + ("human_confirmed_governance_only",))[:6]
        return PolicyEvictionFrame(
            evicted_stale_policy_hints=stale[:4],
            evicted_obsolete_escalation_heuristics=obsolete_escalation[:4],
            evicted_duplicated_policy_summaries=duplicated_summaries[:4],
            evicted_oversized_governance_history=oversized_history[:4],
            preserved_compact_governance_heuristics=preserved,
            policy_eviction_active=True,
            compact_useful_governance_heuristics_only=True,
        )


class PolicyViolationRuntime:
    def detect(self, samples: tuple[DevelopmentPolicySample, ...]) -> PolicyViolationFrame:
        enforcement = any(sample.autonomous_enforcement_attempted for sample in samples)
        repository = any(sample.repository_mutation_attempted for sample in samples)
        hidden = any(sample.hidden_policy_mutation_attempted for sample in samples)
        recursive = any(sample.recursive_planning_attempted for sample in samples)
        warnings = tuple(
            warning
            for warning in (
                "autonomous_enforcement_blocked" if enforcement else "",
                "repository_mutation_authority_blocked" if repository else "",
                "hidden_policy_mutation_blocked" if hidden else "",
                "recursive_governance_expansion_blocked" if recursive else "",
            )
            if warning
        )
        return PolicyViolationFrame(
            autonomous_enforcement_attempted=enforcement,
            human_intent_override_attempted=False,
            repository_mutation_attempted=repository,
            hidden_policy_mutation_attempted=hidden,
            recursive_governance_expansion_attempted=recursive,
            blocked_violation_warnings=warnings,
            advisory_gate_only=True,
        )


class PolicyStabilityRuntime:
    def evaluate(
        self,
        *,
        samples: tuple[DevelopmentPolicySample, ...],
        pressure: PolicyPressureFrame,
    ) -> PolicyStabilityFrame:
        return PolicyStabilityFrame(
            policy_stability="WATCH" if pressure.policy_pressure != "LOW" else "STABLE",
            rollout_safety_stability=(
                "STABLE" if all(sample.rollout_safe for sample in samples) else "WATCH"
            ),
            local_patch_sustainability=all(sample.local_patch_used for sample in samples),
            human_confirmed_enforcement=True,
            compact_continuity_stabilized=True,
            governance_scope_stable=True,
        )


class DevelopmentPolicyRuntime:
    def evaluate(
        self,
        samples: tuple[DevelopmentPolicySample, ...] | None = None,
    ) -> DevelopmentPolicyFrame:
        policy_samples = samples or _default_samples()
        architecture = ArchitectureProtectionPolicyRuntime().evaluate(policy_samples)
        embodiment = EmbodimentRealismPolicyRuntime().evaluate(policy_samples)
        provider = ProviderEscalationPolicyRuntime().evaluate(policy_samples)
        cognition = BoundedCognitionPolicyRuntime().evaluate(policy_samples)
        anti_explosion = AntiExplosionPolicyRuntime().evaluate(policy_samples)
        rollout = RolloutSafetyPolicyRuntime().evaluate(policy_samples)
        pressure = PolicyPressureRuntime().evaluate(
            architecture=architecture,
            embodiment=embodiment,
            provider=provider,
            anti_explosion=anti_explosion,
            rollout=rollout,
        )
        recommendation = PolicyRecommendationRuntime().recommend(
            architecture=architecture,
            provider=provider,
            anti_explosion=anti_explosion,
            rollout=rollout,
        )
        eviction = PolicyEvictionRuntime().evict(
            policy_hints=recommendation.bounded_governance_hints,
            obsolete_escalation=("old-high-default",),
            duplicated_summaries=("LOW_for_policy_summary", "LOW_for_policy_summary"),
            oversized_history=("giant-governance-history",),
        )
        violation = PolicyViolationRuntime().detect(policy_samples)
        stability = PolicyStabilityRuntime().evaluate(samples=policy_samples, pressure=pressure)
        active = all(
            (
                architecture.automatic_architecture_rewrites_prevented,
                embodiment.theatrical_embodiment_escalation_prevented,
                provider.hidden_provider_switching_prevented,
                cognition.giant_cognition_replay_prevented,
                anti_explosion.recursive_governance_expansion_prevented,
                rollout.hidden_migration_mutations_prevented,
                recommendation.human_confirmed,
                eviction.policy_eviction_active,
                violation.advisory_gate_only,
                stability.human_confirmed_enforcement,
            )
        )
        return DevelopmentPolicyFrame(
            architecture=architecture,
            embodiment=embodiment,
            provider=provider,
            cognition=cognition,
            anti_explosion=anti_explosion,
            rollout=rollout,
            pressure=pressure,
            recommendation=recommendation,
            eviction=eviction,
            violation=violation,
            stability=stability,
            dev_policy_active=active,
            architecture_policy_active=architecture.uncontrolled_dependency_growth_prevented,
            embodiment_realism_policy_active=embodiment.autonomous_social_scripting_prevented,
            provider_escalation_policy_active=provider.governance_quality_collapse_prevented,
            bounded_cognition_policy_active=cognition.hidden_memory_accumulation_prevented,
            anti_explosion_policy_active=anti_explosion.recursive_governance_expansion_prevented,
            rollout_safety_policy_active=rollout.uncontrolled_rollout_automation_prevented,
            policy_eviction_active=eviction.policy_eviction_active,
            local_only=True,
            deterministic=True,
            summary_only=True,
            bounded_policy_only=True,
            human_confirmed_governance_only=True,
            no_autonomous_enforcement=True,
            no_repository_mutation_authority=True,
            no_hidden_provider_switching=True,
            no_recursive_governance_expansion=True,
            no_giant_policy_replay=True,
            provider_routing_distribution=provider.provider_usage_distribution,
            estimated_avoided_policy_overhead=3520,
            estimated_avoided_governance_explosion=2880,
            requirement_ids=DEV_POLICY_REQUIREMENT_IDS,
            test_ids=DEV_POLICY_TEST_IDS,
        )


def _default_samples() -> tuple[DevelopmentPolicySample, ...]:
    return (
        DevelopmentPolicySample(
            "policy-01",
            "HIGH",
            "governance_boundary_analysis",
            False,
            True,
            False,
            3800,
            5,
            3,
            2,
            architecture_sprawl_attempted=True,
            repo_wide_cognition_attempted=True,
            governance_bypass_attempted=True,
            recursive_planning_attempted=True,
            autonomous_enforcement_attempted=True,
        ),
        DevelopmentPolicySample(
            "policy-02",
            "HIGH",
            "explosion_prevention",
            True,
            True,
            True,
            2600,
            4,
            2,
            1,
            repository_mutation_attempted=True,
        ),
        DevelopmentPolicySample(
            "policy-03",
            "HIGH",
            "architecture_protection",
            True,
            True,
            True,
            2400,
            4,
            2,
            1,
            unsafe_escalation_attempted=True,
        ),
        DevelopmentPolicySample(
            "policy-04",
            "HIGH",
            "realism_protection",
            True,
            True,
            True,
            1800,
            3,
            1,
            1,
            animation_authority_creep_attempted=True,
            high_amplitude_reaction_attempted=True,
            procedural_acting_attempted=True,
        ),
        DevelopmentPolicySample(
            "policy-05",
            "MEDIUM",
            "policy_prioritization",
            True,
            True,
            True,
            1200,
            3,
            1,
            0,
        ),
        DevelopmentPolicySample(
            "policy-06",
            "MEDIUM",
            "rollout_stabilization",
            True,
            True,
            False,
            1500,
            3,
            1,
            0,
            unsafe_migration_attempted=True,
        ),
        DevelopmentPolicySample(
            "policy-07",
            "MEDIUM",
            "provider_escalation_analysis",
            True,
            True,
            True,
            1400,
            3,
            1,
            0,
        ),
        DevelopmentPolicySample(
            "policy-08", "LOW", "compact_summary", True, True, True, 600, 1, 1, 0
        ),
        DevelopmentPolicySample(
            "policy-09", "LOW", "governance_formatting", True, True, True, 700, 1, 1, 0
        ),
        DevelopmentPolicySample(
            "policy-10",
            "LOW",
            "policy_cleanup",
            True,
            True,
            True,
            500,
            1,
            1,
            0,
            hidden_policy_mutation_attempted=True,
        ),
    )


def _provider_distribution(samples: tuple[DevelopmentPolicySample, ...]) -> dict[str, int]:
    return {
        provider_class: sum(sample.provider_class == provider_class for sample in samples)
        for provider_class in ("HIGH", "MEDIUM", "LOW")
    }


def _premium_units(samples: tuple[DevelopmentPolicySample, ...]) -> int:
    return sum(sample.premium_provider_units for sample in samples)


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


__all__ = [
    "DEV_POLICY_REQUIREMENT_IDS",
    "DEV_POLICY_TEST_IDS",
    "AntiExplosionPolicyFrame",
    "AntiExplosionPolicyRuntime",
    "ArchitectureProtectionPolicyFrame",
    "ArchitectureProtectionPolicyRuntime",
    "BoundedCognitionPolicyFrame",
    "BoundedCognitionPolicyRuntime",
    "DevelopmentPolicyFrame",
    "DevelopmentPolicyRuntime",
    "DevelopmentPolicySample",
    "EmbodimentRealismPolicyFrame",
    "EmbodimentRealismPolicyRuntime",
    "PolicyEvictionFrame",
    "PolicyEvictionRuntime",
    "PolicyPressureFrame",
    "PolicyPressureRuntime",
    "PolicyRecommendationFrame",
    "PolicyRecommendationRuntime",
    "PolicyStabilityFrame",
    "PolicyStabilityRuntime",
    "PolicyViolationFrame",
    "PolicyViolationRuntime",
    "ProviderEscalationPolicyFrame",
    "ProviderEscalationPolicyRuntime",
    "RolloutSafetyPolicyFrame",
    "RolloutSafetyPolicyRuntime",
]
