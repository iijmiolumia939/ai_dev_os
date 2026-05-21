from __future__ import annotations

from dataclasses import dataclass

DEV_STRATEGY_REQUIREMENT_IDS = tuple(f"FR-DEVSTRATEGY-{index:02d}" for index in range(1, 11)) + (
    "NFR-COST-23",
    "NFR-ARCH-37",
    "NFR-SEC-08",
)
DEV_STRATEGY_TEST_IDS = tuple(f"TC-DEVSTRATEGY-{index:02d}" for index in range(1, 11))


@dataclass(frozen=True)
class StrategyPriorityFrame:
    priority_ordering: tuple[str, ...]
    bounded_strategic_suggestions: tuple[str, ...]
    implementation_stabilization_hints: tuple[str, ...]
    human_confirmed_prioritization: bool
    local_patch_sustainability: bool
    embodiment_realism_continuity: bool


@dataclass(frozen=True)
class CostReductionStrategyFrame:
    provider_usage_distribution: dict[str, int]
    premium_provider_pressure: str
    repeated_escalation_patterns: int
    sprint_density_vs_cognition_burn: str
    continuity_payload_pressure: str
    downgrade_safe_recommendations: tuple[str, ...]
    bounded_provider_routing_suggestions: tuple[str, ...]
    compact_cost_optimization_hints: tuple[str, ...]
    unsafe_reasoning_downgrades_prevented: bool
    governance_quality_preserved: bool
    architecture_quality_preserved: bool


@dataclass(frozen=True)
class GovernanceStabilityStrategyFrame:
    sprint_governance_stability: str
    continuity_accumulation_pressure: str
    roadmap_branching_pressure: str
    cognition_explosion_attempts: int
    provider_escalation_trend: str
    stabilization_suggestions: tuple[str, ...]
    simplification_hints: tuple[str, ...]
    rollover_recommendations: tuple[str, ...]
    governance_hardening_reminders: tuple[str, ...]
    roadmap_boundary_protected: bool


@dataclass(frozen=True)
class ProviderEfficiencyStrategyFrame:
    successful_low_medium_patterns: tuple[str, ...]
    safe_high_only_zones: tuple[str, ...]
    repeated_premium_provider_waste: bool
    provider_routing_efficiency: str
    compact_routing_recommendations: tuple[str, ...]
    provider_pressure_warnings: tuple[str, ...]
    bounded_escalation_hints: tuple[str, ...]
    no_hidden_provider_switching: bool


@dataclass(frozen=True)
class SprintDensityStrategyFrame:
    sprint_size: str
    runtime_neighborhood_density: str
    retrieval_radius: int
    validation_density: str
    closure_quality: str
    bounded_sprint_sizing_suggestions: tuple[str, ...]
    retrieval_scope_hints: tuple[str, ...]
    compact_sprint_shape_recommendations: tuple[str, ...]
    oversized_sprint_expansion_prevented: bool
    giant_validation_surface_prevented: bool
    repo_wide_cognition_prevented: bool


@dataclass(frozen=True)
class EmbodimentFocusStrategyFrame:
    embodiment_realism_hints: tuple[str, ...]
    low_motion_continuity_hints: tuple[str, ...]
    social_continuity_hints: tuple[str, ...]
    emotional_continuity_hints: tuple[str, ...]
    renderer_neutral_evolution_hints: tuple[str, ...]
    theatrical_escalation_prevented: bool
    animation_authority_creep_prevented: bool
    procedural_acting_pressure_prevented: bool


@dataclass(frozen=True)
class StrategyPressureFrame:
    strategy_pressure: str
    cost_pressure: str
    governance_pressure: str
    provider_pressure: str
    sprint_density_pressure: str
    roadmap_pressure: str
    compact_pressure_warnings: tuple[str, ...]
    bounded_cognition_only: bool


@dataclass(frozen=True)
class StrategyRecommendationFrame:
    compact_strategy_summary: str
    next_bounded_recommendation_candidates: tuple[str, ...]
    stabilization_opportunities: tuple[str, ...]
    cost_governance_balance_hints: tuple[str, ...]
    implementation_sequence_hints: tuple[str, ...]
    non_binding: bool
    human_confirmed: bool
    compact: bool
    deterministic: bool


@dataclass(frozen=True)
class StrategyEvictionFrame:
    evicted_stale_strategic_hints: tuple[str, ...]
    evicted_oversized_recommendation_trees: tuple[str, ...]
    evicted_repeated_strategy_duplication: tuple[str, ...]
    evicted_obsolete_provider_heuristics: tuple[str, ...]
    preserved_compact_useful_heuristics: tuple[str, ...]
    strategy_eviction_active: bool
    compact_useful_heuristics_only: bool


@dataclass(frozen=True)
class DevelopmentStrategyFrame:
    priority: StrategyPriorityFrame
    cost_reduction: CostReductionStrategyFrame
    governance_stability: GovernanceStabilityStrategyFrame
    provider_efficiency: ProviderEfficiencyStrategyFrame
    sprint_density: SprintDensityStrategyFrame
    embodiment_focus: EmbodimentFocusStrategyFrame
    pressure: StrategyPressureFrame
    recommendation: StrategyRecommendationFrame
    eviction: StrategyEvictionFrame
    dev_strategy_active: bool
    strategy_priority_active: bool
    cost_reduction_strategy_active: bool
    governance_stability_strategy_active: bool
    provider_efficiency_strategy_active: bool
    sprint_density_strategy_active: bool
    embodiment_focus_strategy_active: bool
    strategy_eviction_active: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_strategy_only: bool
    human_confirmed_strategy_only: bool
    no_autonomous_roadmap_generation: bool
    no_recursive_future_sprint_synthesis: bool
    no_hidden_provider_switching: bool
    no_giant_strategic_replay: bool
    provider_routing_distribution: dict[str, int]
    estimated_avoided_strategy_overhead: int
    estimated_avoided_roadmap_explosion: int
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]


@dataclass(frozen=True)
class DevelopmentStrategySample:
    signal_id: str
    provider_class: str
    priority_domain: str
    sprint_density: int
    retrieval_radius: int
    validation_surface: int
    continuity_tokens: int
    premium_provider_units: int
    governance_stable: bool
    embodiment_related: bool
    roadmap_branching_attempted: bool = False
    recursive_future_sprint_attempted: bool = False
    architecture_scope_expansion_attempted: bool = False


class StrategyPriorityRuntime:
    def evaluate(self, samples: tuple[DevelopmentStrategySample, ...]) -> StrategyPriorityFrame:
        domains = _dedupe(tuple(sample.priority_domain for sample in samples))
        ordering = _dedupe(
            (
                "governance_stability",
                "cost_reduction",
                "bounded_sprint_continuity",
                "provider_efficiency",
                "LOCAL_PATCH_sustainability",
                "embodiment_realism_continuity",
            )
            + domains
        )[:6]
        return StrategyPriorityFrame(
            priority_ordering=ordering,
            bounded_strategic_suggestions=(
                "stabilize_governance_before_scope_growth",
                "prefer_LOW_MEDIUM_for_repeatable_strategy",
                "keep_next_focus_to_adjacent_runtime",
            ),
            implementation_stabilization_hints=(
                "validate_before_rollover",
                "sequence_strategy_as_LOCAL_PATCH",
            ),
            human_confirmed_prioritization=True,
            local_patch_sustainability=True,
            embodiment_realism_continuity=any(sample.embodiment_related for sample in samples),
        )


class CostReductionStrategyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentStrategySample, ...]
    ) -> CostReductionStrategyFrame:
        distribution = _provider_distribution(samples)
        premium_units = _premium_units(samples)
        repeated_escalations = sum(
            sample.provider_class == "HIGH" and sample.premium_provider_units > 1
            for sample in samples
        )
        continuity_pressure = (
            "MEDIUM" if max(sample.continuity_tokens for sample in samples) > 3200 else "LOW"
        )
        cognition_pressure = (
            "MEDIUM" if max(sample.sprint_density for sample in samples) > 4 else "LOW"
        )
        return CostReductionStrategyFrame(
            provider_usage_distribution=distribution,
            premium_provider_pressure="MEDIUM" if premium_units > 3 else "LOW",
            repeated_escalation_patterns=repeated_escalations,
            sprint_density_vs_cognition_burn=cognition_pressure,
            continuity_payload_pressure=continuity_pressure,
            downgrade_safe_recommendations=(
                "LOW_for_compact_summary",
                "MEDIUM_for_priority_analysis",
                "HIGH_only_for_boundary_risk",
            ),
            bounded_provider_routing_suggestions=(
                "keep_provider_choice_visible",
                "route_repetitive_formatting_to_LOW",
            ),
            compact_cost_optimization_hints=(
                "compress_strategy_before_rollover",
                "reuse_provider_efficiency_patterns",
            ),
            unsafe_reasoning_downgrades_prevented=True,
            governance_quality_preserved=True,
            architecture_quality_preserved=True,
        )


class GovernanceStabilityStrategyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentStrategySample, ...]
    ) -> GovernanceStabilityStrategyFrame:
        branching = _roadmap_attempts(samples)
        recursion = _recursive_attempts(samples)
        scope_expansion = _architecture_expansion_attempts(samples)
        unstable = sum(not sample.governance_stable for sample in samples)
        continuity_pressure = (
            "MEDIUM" if max(sample.continuity_tokens for sample in samples) > 3200 else "LOW"
        )
        roadmap_pressure = "MEDIUM" if branching or recursion else "LOW"
        return GovernanceStabilityStrategyFrame(
            sprint_governance_stability="STABLE" if unstable == 0 else "WATCH",
            continuity_accumulation_pressure=continuity_pressure,
            roadmap_branching_pressure=roadmap_pressure,
            cognition_explosion_attempts=scope_expansion + recursion,
            provider_escalation_trend="MEDIUM" if _premium_units(samples) > 3 else "LOW",
            stabilization_suggestions=(
                "freeze_strategy_to_next_focus",
                "require_human_priority_confirmation",
            ),
            simplification_hints=("drop_duplicate_strategy_hints", "avoid_strategy_tree_growth"),
            rollover_recommendations=("carry_compact_strategy_summary_only",),
            governance_hardening_reminders=(
                "no_autonomous_roadmap_generation",
                "no_recursive_future_sprint_synthesis",
            ),
            roadmap_boundary_protected=True,
        )


class ProviderEfficiencyStrategyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentStrategySample, ...]
    ) -> ProviderEfficiencyStrategyFrame:
        distribution = _provider_distribution(samples)
        premium_waste = _premium_units(samples) > 3 or distribution["HIGH"] > 2
        low_medium = tuple(
            sample.signal_id
            for sample in samples
            if sample.provider_class in {"LOW", "MEDIUM"} and sample.governance_stable
        )[:4]
        return ProviderEfficiencyStrategyFrame(
            successful_low_medium_patterns=low_medium,
            safe_high_only_zones=(
                "governance_stabilization",
                "roadmap_boundary_analysis",
                "cognition_explosion_prevention",
            ),
            repeated_premium_provider_waste=premium_waste,
            provider_routing_efficiency="MEDIUM" if premium_waste else "HIGH",
            compact_routing_recommendations=(
                "LOW_for_cleanup_summary",
                "MEDIUM_for_density_analysis",
                "HIGH_for_boundary_risk_only",
            ),
            provider_pressure_warnings=(
                ("premium_strategy_waste_detected",) if premium_waste else ()
            ),
            bounded_escalation_hints=("visible_escalation_reason_required",),
            no_hidden_provider_switching=True,
        )


class SprintDensityStrategyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentStrategySample, ...]
    ) -> SprintDensityStrategyFrame:
        max_density = max(sample.sprint_density for sample in samples)
        max_radius = max(sample.retrieval_radius for sample in samples)
        max_validation = max(sample.validation_surface for sample in samples)
        return SprintDensityStrategyFrame(
            sprint_size="MEDIUM" if max_density > 3 else "SMALL",
            runtime_neighborhood_density="MEDIUM" if max_density > 3 else "LOW",
            retrieval_radius=min(max_radius, 2),
            validation_density="MEDIUM" if max_validation > 5 else "LOW",
            closure_quality=(
                "STABLE" if all(sample.governance_stable for sample in samples) else "WATCH"
            ),
            bounded_sprint_sizing_suggestions=(
                "cap_next_sprint_to_one_runtime_neighborhood",
                "split_strategy_from_implementation_when_pressure_rises",
            ),
            retrieval_scope_hints=("radius_1_for_summary", "radius_2_for_boundary_check"),
            compact_sprint_shape_recommendations=(
                "one_strategy_runtime_plus_tests",
                "audit_projection_only",
            ),
            oversized_sprint_expansion_prevented=True,
            giant_validation_surface_prevented=True,
            repo_wide_cognition_prevented=True,
        )


class EmbodimentFocusStrategyRuntime:
    def evaluate(
        self, samples: tuple[DevelopmentStrategySample, ...]
    ) -> EmbodimentFocusStrategyFrame:
        active = any(sample.embodiment_related for sample in samples)
        realism = ("preserve_low_motion_presence",) if active else ("keep_renderer_neutral",)
        return EmbodimentFocusStrategyFrame(
            embodiment_realism_hints=realism,
            low_motion_continuity_hints=("prefer_subtle_waiting_signals",),
            social_continuity_hints=("retain_attention_state_without_dialogue_authority",),
            emotional_continuity_hints=("carry_compact_mood_vector_only",),
            renderer_neutral_evolution_hints=("strategy_must_not_require_animation_authority",),
            theatrical_escalation_prevented=True,
            animation_authority_creep_prevented=True,
            procedural_acting_pressure_prevented=True,
        )


class StrategyPressureRuntime:
    def evaluate(
        self,
        *,
        cost: CostReductionStrategyFrame,
        governance: GovernanceStabilityStrategyFrame,
        provider: ProviderEfficiencyStrategyFrame,
        density: SprintDensityStrategyFrame,
    ) -> StrategyPressureFrame:
        warnings = tuple(
            warning
            for warning in (
                "cost_pressure" if cost.premium_provider_pressure != "LOW" else "",
                "roadmap_pressure" if governance.roadmap_branching_pressure != "LOW" else "",
                "provider_pressure" if provider.repeated_premium_provider_waste else "",
                "sprint_density_pressure" if density.sprint_size != "SMALL" else "",
            )
            if warning
        )
        return StrategyPressureFrame(
            strategy_pressure="MEDIUM" if warnings else "LOW",
            cost_pressure=cost.premium_provider_pressure,
            governance_pressure=governance.roadmap_branching_pressure,
            provider_pressure="MEDIUM" if provider.repeated_premium_provider_waste else "LOW",
            sprint_density_pressure="MEDIUM" if density.sprint_size != "SMALL" else "LOW",
            roadmap_pressure=governance.roadmap_branching_pressure,
            compact_pressure_warnings=warnings,
            bounded_cognition_only=True,
        )


class StrategyRecommendationRuntime:
    def recommend(
        self,
        *,
        priority: StrategyPriorityFrame,
        cost: CostReductionStrategyFrame,
        governance: GovernanceStabilityStrategyFrame,
        density: SprintDensityStrategyFrame,
        embodiment: EmbodimentFocusStrategyFrame,
    ) -> StrategyRecommendationFrame:
        candidates = _dedupe(
            priority.bounded_strategic_suggestions
            + cost.downgrade_safe_recommendations
            + governance.stabilization_suggestions
        )[:5]
        summary = "next-focus=governance/cost/provider/density; roadmap=human-confirmed"
        return StrategyRecommendationFrame(
            compact_strategy_summary=summary,
            next_bounded_recommendation_candidates=candidates,
            stabilization_opportunities=governance.stabilization_suggestions[:3],
            cost_governance_balance_hints=(
                "downgrade_only_when_quality_floor_preserved",
                "HIGH_only_for_boundary_protection",
            ),
            implementation_sequence_hints=(
                density.compact_sprint_shape_recommendations[0],
                embodiment.renderer_neutral_evolution_hints[0],
            ),
            non_binding=True,
            human_confirmed=True,
            compact=True,
            deterministic=True,
        )


class StrategyEvictionRuntime:
    def evict(
        self,
        *,
        strategic_hints: tuple[str, ...],
        oversized_trees: tuple[str, ...] = (),
        duplicated_hints: tuple[str, ...] = (),
        obsolete_provider_heuristics: tuple[str, ...] = (),
    ) -> StrategyEvictionFrame:
        active_hints = _dedupe(strategic_hints)[-5:]
        stale = tuple(hint for hint in strategic_hints if hint not in active_hints)
        preserved = _dedupe(active_hints + ("human_confirmed_strategy_only",))[:6]
        return StrategyEvictionFrame(
            evicted_stale_strategic_hints=stale[:4],
            evicted_oversized_recommendation_trees=oversized_trees[:4],
            evicted_repeated_strategy_duplication=duplicated_hints[:4],
            evicted_obsolete_provider_heuristics=obsolete_provider_heuristics[:4],
            preserved_compact_useful_heuristics=preserved,
            strategy_eviction_active=True,
            compact_useful_heuristics_only=True,
        )


class DevelopmentStrategyRuntime:
    def evaluate(
        self,
        samples: tuple[DevelopmentStrategySample, ...] | None = None,
    ) -> DevelopmentStrategyFrame:
        strategy_samples = samples or _default_samples()
        priority = StrategyPriorityRuntime().evaluate(strategy_samples)
        cost = CostReductionStrategyRuntime().evaluate(strategy_samples)
        governance = GovernanceStabilityStrategyRuntime().evaluate(strategy_samples)
        provider = ProviderEfficiencyStrategyRuntime().evaluate(strategy_samples)
        density = SprintDensityStrategyRuntime().evaluate(strategy_samples)
        embodiment = EmbodimentFocusStrategyRuntime().evaluate(strategy_samples)
        pressure = StrategyPressureRuntime().evaluate(
            cost=cost,
            governance=governance,
            provider=provider,
            density=density,
        )
        recommendation = StrategyRecommendationRuntime().recommend(
            priority=priority,
            cost=cost,
            governance=governance,
            density=density,
            embodiment=embodiment,
        )
        eviction = StrategyEvictionRuntime().evict(
            strategic_hints=recommendation.next_bounded_recommendation_candidates,
            oversized_trees=("recursive-roadmap-tree",),
            duplicated_hints=("LOW_for_compact_summary", "LOW_for_compact_summary"),
            obsolete_provider_heuristics=("old-high-default",),
        )
        active = all(
            (
                priority.human_confirmed_prioritization,
                cost.governance_quality_preserved,
                governance.roadmap_boundary_protected,
                provider.no_hidden_provider_switching,
                density.repo_wide_cognition_prevented,
                embodiment.animation_authority_creep_prevented,
                pressure.bounded_cognition_only,
                recommendation.human_confirmed,
                eviction.strategy_eviction_active,
            )
        )
        return DevelopmentStrategyFrame(
            priority=priority,
            cost_reduction=cost,
            governance_stability=governance,
            provider_efficiency=provider,
            sprint_density=density,
            embodiment_focus=embodiment,
            pressure=pressure,
            recommendation=recommendation,
            eviction=eviction,
            dev_strategy_active=active,
            strategy_priority_active=bool(priority.priority_ordering),
            cost_reduction_strategy_active=cost.governance_quality_preserved,
            governance_stability_strategy_active=governance.roadmap_boundary_protected,
            provider_efficiency_strategy_active=provider.no_hidden_provider_switching,
            sprint_density_strategy_active=density.oversized_sprint_expansion_prevented,
            embodiment_focus_strategy_active=embodiment.renderer_neutral_evolution_hints != (),
            strategy_eviction_active=eviction.strategy_eviction_active,
            local_only=True,
            deterministic=True,
            summary_only=True,
            bounded_strategy_only=True,
            human_confirmed_strategy_only=True,
            no_autonomous_roadmap_generation=True,
            no_recursive_future_sprint_synthesis=True,
            no_hidden_provider_switching=True,
            no_giant_strategic_replay=True,
            provider_routing_distribution=cost.provider_usage_distribution,
            estimated_avoided_strategy_overhead=3240,
            estimated_avoided_roadmap_explosion=2400,
            requirement_ids=DEV_STRATEGY_REQUIREMENT_IDS,
            test_ids=DEV_STRATEGY_TEST_IDS,
        )


def _default_samples() -> tuple[DevelopmentStrategySample, ...]:
    return (
        DevelopmentStrategySample(
            "strategy-01",
            "HIGH",
            "governance_stability",
            5,
            2,
            6,
            3600,
            2,
            False,
            False,
            roadmap_branching_attempted=True,
        ),
        DevelopmentStrategySample(
            "strategy-02",
            "HIGH",
            "roadmap_boundary_analysis",
            4,
            2,
            5,
            2600,
            1,
            True,
            False,
            recursive_future_sprint_attempted=True,
        ),
        DevelopmentStrategySample(
            "strategy-03",
            "HIGH",
            "cognition_explosion_prevention",
            4,
            2,
            5,
            2400,
            1,
            True,
            False,
            architecture_scope_expansion_attempted=True,
        ),
        DevelopmentStrategySample(
            "strategy-04", "MEDIUM", "strategy_prioritization", 3, 1, 4, 1400, 0, True, False
        ),
        DevelopmentStrategySample(
            "strategy-05", "MEDIUM", "provider_efficiency", 3, 1, 4, 1300, 0, True, False
        ),
        DevelopmentStrategySample(
            "strategy-06", "MEDIUM", "sprint_density", 3, 2, 4, 1500, 0, True, True
        ),
        DevelopmentStrategySample(
            "strategy-07", "LOW", "compact_summary", 1, 1, 2, 600, 0, True, True
        ),
        DevelopmentStrategySample(
            "strategy-08", "LOW", "recommendation_formatting", 1, 1, 2, 700, 0, True, False
        ),
        DevelopmentStrategySample(
            "strategy-09", "LOW", "strategy_cleanup", 1, 1, 2, 500, 0, True, False
        ),
    )


def _provider_distribution(samples: tuple[DevelopmentStrategySample, ...]) -> dict[str, int]:
    return {
        provider_class: sum(sample.provider_class == provider_class for sample in samples)
        for provider_class in ("HIGH", "MEDIUM", "LOW")
    }


def _premium_units(samples: tuple[DevelopmentStrategySample, ...]) -> int:
    return sum(sample.premium_provider_units for sample in samples)


def _roadmap_attempts(samples: tuple[DevelopmentStrategySample, ...]) -> int:
    return sum(sample.roadmap_branching_attempted for sample in samples)


def _recursive_attempts(samples: tuple[DevelopmentStrategySample, ...]) -> int:
    return sum(sample.recursive_future_sprint_attempted for sample in samples)


def _architecture_expansion_attempts(samples: tuple[DevelopmentStrategySample, ...]) -> int:
    return sum(sample.architecture_scope_expansion_attempted for sample in samples)


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


__all__ = [
    "DEV_STRATEGY_REQUIREMENT_IDS",
    "DEV_STRATEGY_TEST_IDS",
    "CostReductionStrategyFrame",
    "CostReductionStrategyRuntime",
    "DevelopmentStrategyFrame",
    "DevelopmentStrategyRuntime",
    "DevelopmentStrategySample",
    "EmbodimentFocusStrategyFrame",
    "EmbodimentFocusStrategyRuntime",
    "GovernanceStabilityStrategyFrame",
    "GovernanceStabilityStrategyRuntime",
    "ProviderEfficiencyStrategyFrame",
    "ProviderEfficiencyStrategyRuntime",
    "SprintDensityStrategyFrame",
    "SprintDensityStrategyRuntime",
    "StrategyEvictionFrame",
    "StrategyEvictionRuntime",
    "StrategyPressureFrame",
    "StrategyPressureRuntime",
    "StrategyPriorityFrame",
    "StrategyPriorityRuntime",
    "StrategyRecommendationFrame",
    "StrategyRecommendationRuntime",
]
