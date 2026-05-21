from __future__ import annotations

from dataclasses import dataclass

SPRINT_MEMORY_REQUIREMENT_IDS = tuple(f"FR-SPRINTMEMORY-{index:02d}" for index in range(1, 11)) + (
    "NFR-COST-22",
    "NFR-ARCH-36",
    "NFR-SEC-07",
)
SPRINT_MEMORY_TEST_IDS = tuple(f"TC-SPRINTMEMORY-{index:02d}" for index in range(1, 11))


@dataclass(frozen=True)
class SprintPatternFrame:
    successful_sprint_shapes: tuple[str, ...]
    failed_sprint_shapes: tuple[str, ...]
    local_patch_success_patterns: tuple[str, ...]
    bounded_cognition_success_patterns: tuple[str, ...]
    compact_operational_patterns_only: bool
    autonomous_roadmap_learning_forbidden: bool


@dataclass(frozen=True)
class SprintOutcomeFrame:
    validation_stability: str
    ci_stability: str
    provider_efficiency: str
    reasoning_efficiency: str
    retrieval_efficiency: str
    governance_pressure: str
    sprint_closure_quality: str
    bounded_scoring_only: bool
    deterministic_metrics_only: bool
    compact_operational_summary: str


@dataclass(frozen=True)
class SprintEfficiencyFrame:
    provider_efficiency_score: int
    reasoning_efficiency_score: int
    retrieval_efficiency_score: int
    governance_efficiency_score: int
    closure_efficiency_score: int
    overall_efficiency_score: int
    low_medium_success_detected: bool
    local_patch_efficiency_detected: bool


@dataclass(frozen=True)
class SprintFailurePatternFrame:
    repeated_sprint_explosion: bool
    repeated_provider_escalation: bool
    repeated_giant_retrieval: bool
    repeated_repo_wide_reasoning: bool
    repeated_continuity_accumulation: bool
    unstable_sprint_rollover: bool
    downgrade_recommendations: tuple[str, ...]
    simplification_recommendations: tuple[str, ...]
    local_patch_reminders: tuple[str, ...]
    provider_downgrade_hints: tuple[str, ...]


@dataclass(frozen=True)
class SprintProviderPatternFrame:
    provider_usage_distribution: dict[str, int]
    repeated_premium_provider_usage: bool
    successful_low_medium_routing: bool
    provider_pressure_trend: str
    sprint_provider_efficiency: str
    compact_provider_recommendations: tuple[str, ...]
    premium_burn_warnings: tuple[str, ...]
    downgrade_safe_suggestions: tuple[str, ...]
    no_hidden_provider_switching: bool


@dataclass(frozen=True)
class SprintRetrievalPatternFrame:
    retrieval_radius: int
    repo_wide_cognition_frequency: int
    adjacent_runtime_success: bool
    retrieval_explosion_attempts: int
    continuity_size_trend: str
    compact_retrieval_recommendations: tuple[str, ...]
    bounded_retrieval_reminders: tuple[str, ...]
    delta_only_reminders: tuple[str, ...]
    no_giant_sprint_replay: bool


@dataclass(frozen=True)
class SprintGovernancePatternFrame:
    sprint_pressure_trend: str
    cognition_expansion_attempts: int
    roadmap_branching_attempts: int
    continuity_accumulation_trend: str
    sprint_stability: str
    compact_governance_warnings: tuple[str, ...]
    sprint_simplification_suggestions: tuple[str, ...]
    rollover_recommendations: tuple[str, ...]
    human_confirmed_orchestration_only: bool


@dataclass(frozen=True)
class SprintCompressionFrame:
    bounded_operational_heuristics: tuple[str, ...]
    compact_summary_patterns: tuple[str, ...]
    provider_routing_hints: tuple[str, ...]
    retrieval_heuristics: tuple[str, ...]
    governance_heuristics: tuple[str, ...]
    giant_memory_accumulation_prevented: bool
    full_historical_replay_forbidden: bool
    hidden_cognition_expansion_forbidden: bool
    summary_only: bool


@dataclass(frozen=True)
class SprintEvictionFrame:
    evicted_stale_sprint_memory: tuple[str, ...]
    evicted_oversized_sprint_memory: tuple[str, ...]
    evicted_redundant_sprint_patterns: tuple[str, ...]
    evicted_obsolete_provider_heuristics: tuple[str, ...]
    evicted_operational_duplicates: tuple[str, ...]
    preserved_compact_useful_heuristics: tuple[str, ...]
    stale_memory_eviction_active: bool
    bounded_memory_only: bool


@dataclass(frozen=True)
class SprintMemoryFrame:
    patterns: SprintPatternFrame
    outcome: SprintOutcomeFrame
    efficiency: SprintEfficiencyFrame
    failure_patterns: SprintFailurePatternFrame
    provider_patterns: SprintProviderPatternFrame
    retrieval_patterns: SprintRetrievalPatternFrame
    governance_patterns: SprintGovernancePatternFrame
    compression: SprintCompressionFrame
    eviction: SprintEvictionFrame
    sprint_memory_active: bool
    sprint_pattern_active: bool
    sprint_outcome_active: bool
    sprint_provider_pattern_active: bool
    sprint_retrieval_pattern_active: bool
    sprint_governance_pattern_active: bool
    sprint_compression_active: bool
    sprint_eviction_active: bool
    local_only: bool
    deterministic: bool
    summary_only: bool
    bounded_memory_only: bool
    no_hidden_long_term_cognition: bool
    no_full_sprint_transcript_accumulation: bool
    no_autonomous_roadmap_learning: bool
    no_hidden_provider_switching: bool
    provider_routing_distribution: dict[str, int]
    estimated_avoided_manual_sprint_analysis: int
    estimated_avoided_repeated_sprint_failures: int
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]


@dataclass(frozen=True)
class SprintMemorySample:
    sprint_id: str
    provider_class: str
    retrieval_radius: int
    validation_passed: bool
    ci_passed: bool
    local_patch_used: bool
    bounded_cognition_used: bool
    repo_wide_reasoning_attempted: bool = False
    roadmap_branching_attempted: bool = False
    continuity_tokens: int = 0
    premium_provider_units: int = 0
    rollover_stable: bool = True


class SprintPatternRuntime:
    def evaluate(self, samples: tuple[SprintMemorySample, ...]) -> SprintPatternFrame:
        successful = tuple(
            sample.sprint_id
            for sample in samples
            if sample.validation_passed and sample.ci_passed and sample.local_patch_used
        )[:4]
        failed = tuple(
            sample.sprint_id
            for sample in samples
            if not sample.validation_passed or not sample.ci_passed
        )[:4]
        return SprintPatternFrame(
            successful_sprint_shapes=successful,
            failed_sprint_shapes=failed,
            local_patch_success_patterns=("adjacent_runtime_patch", "scoped_validation"),
            bounded_cognition_success_patterns=("summary_only_memory", "delta_only_carryover"),
            compact_operational_patterns_only=True,
            autonomous_roadmap_learning_forbidden=True,
        )


class SprintOutcomeRuntime:
    def evaluate(self, samples: tuple[SprintMemorySample, ...]) -> SprintOutcomeFrame:
        validation_ratio = _ratio(
            sum(sample.validation_passed for sample in samples), len(samples)
        )
        ci_ratio = _ratio(sum(sample.ci_passed for sample in samples), len(samples))
        provider_efficiency = "HIGH" if _premium_units(samples) <= 4 else "MEDIUM"
        retrieval_efficiency = (
            "HIGH" if max(sample.retrieval_radius for sample in samples) <= 2 else "LOW"
        )
        pressure = (
            "LOW" if all(sample.continuity_tokens <= 3_200 for sample in samples) else "MEDIUM"
        )
        closure = "STABLE" if validation_ratio >= 0.75 and ci_ratio >= 0.75 else "UNSTABLE"
        return SprintOutcomeFrame(
            validation_stability=_stability(validation_ratio),
            ci_stability=_stability(ci_ratio),
            provider_efficiency=provider_efficiency,
            reasoning_efficiency="HIGH" if _repo_wide_attempts(samples) == 0 else "MEDIUM",
            retrieval_efficiency=retrieval_efficiency,
            governance_pressure=pressure,
            sprint_closure_quality=closure,
            bounded_scoring_only=True,
            deterministic_metrics_only=True,
            compact_operational_summary=f"validation={validation_ratio:.2f}; ci={ci_ratio:.2f}",
        )


class SprintEfficiencyRuntime:
    def evaluate(self, samples: tuple[SprintMemorySample, ...]) -> SprintEfficiencyFrame:
        provider_score = max(20, 100 - _premium_units(samples) * 8)
        reasoning_score = max(20, 100 - _repo_wide_attempts(samples) * 20)
        retrieval_score = max(20, 100 - _retrieval_explosions(samples) * 25)
        governance_score = max(20, 100 - _roadmap_attempts(samples) * 25)
        closure_score = max(20, 100 - _unstable_rollovers(samples) * 25)
        scores = (
            provider_score,
            reasoning_score,
            retrieval_score,
            governance_score,
            closure_score,
        )
        return SprintEfficiencyFrame(
            provider_efficiency_score=provider_score,
            reasoning_efficiency_score=reasoning_score,
            retrieval_efficiency_score=retrieval_score,
            governance_efficiency_score=governance_score,
            closure_efficiency_score=closure_score,
            overall_efficiency_score=sum(scores) // len(scores),
            low_medium_success_detected=any(
                sample.provider_class in {"LOW", "MEDIUM"} and sample.validation_passed
                for sample in samples
            ),
            local_patch_efficiency_detected=any(sample.local_patch_used for sample in samples),
        )


class SprintFailurePatternRuntime:
    def detect(self, samples: tuple[SprintMemorySample, ...]) -> SprintFailurePatternFrame:
        provider_escalation = _premium_units(samples) > 4
        giant_retrieval = _retrieval_explosions(samples) > 0
        repo_wide = _repo_wide_attempts(samples) > 0
        continuity = any(sample.continuity_tokens > 3_200 for sample in samples)
        unstable = _unstable_rollovers(samples) > 0
        sprint_explosion = repo_wide or continuity or _roadmap_attempts(samples) > 0
        return SprintFailurePatternFrame(
            repeated_sprint_explosion=sprint_explosion,
            repeated_provider_escalation=provider_escalation,
            repeated_giant_retrieval=giant_retrieval,
            repeated_repo_wide_reasoning=repo_wide,
            repeated_continuity_accumulation=continuity,
            unstable_sprint_rollover=unstable,
            downgrade_recommendations=("prefer_LOW_for_cleanup", "prefer_MEDIUM_for_patterns"),
            simplification_recommendations=("compress_to_heuristics", "evict_duplicate_patterns"),
            local_patch_reminders=("LOCAL_PATCH_REQUIRED", "adjacent_runtime_only"),
            provider_downgrade_hints=("avoid_HIGH_for_repetitive_memory",),
        )


class SprintProviderPatternRuntime:
    def evaluate(self, samples: tuple[SprintMemorySample, ...]) -> SprintProviderPatternFrame:
        distribution = _provider_distribution(samples)
        repeated_premium = distribution["HIGH"] > 1 or _premium_units(samples) > 4
        pressure = "MEDIUM" if repeated_premium else "LOW"
        return SprintProviderPatternFrame(
            provider_usage_distribution=distribution,
            repeated_premium_provider_usage=repeated_premium,
            successful_low_medium_routing=distribution["LOW"] + distribution["MEDIUM"] >= 2,
            provider_pressure_trend=pressure,
            sprint_provider_efficiency="HIGH" if not repeated_premium else "MEDIUM",
            compact_provider_recommendations=("LOW_for_cleanup", "MEDIUM_for_pattern_analysis"),
            premium_burn_warnings=(
                ("premium_memory_analysis_suppressed",) if repeated_premium else ()
            ),
            downgrade_safe_suggestions=(
                "compact_summary_to_LOW",
                "bounded_recommendation_to_MEDIUM",
            ),
            no_hidden_provider_switching=True,
        )


class SprintRetrievalPatternRuntime:
    def evaluate(self, samples: tuple[SprintMemorySample, ...]) -> SprintRetrievalPatternFrame:
        max_radius = max(sample.retrieval_radius for sample in samples)
        repo_wide = _repo_wide_attempts(samples)
        explosions = _retrieval_explosions(samples)
        trend = "MEDIUM" if any(sample.continuity_tokens > 3_200 for sample in samples) else "LOW"
        return SprintRetrievalPatternFrame(
            retrieval_radius=min(max_radius, 2),
            repo_wide_cognition_frequency=repo_wide,
            adjacent_runtime_success=repo_wide == 0,
            retrieval_explosion_attempts=explosions,
            continuity_size_trend=trend,
            compact_retrieval_recommendations=("radius_1_for_memory", "radius_2_for_governance"),
            bounded_retrieval_reminders=("adjacent_runtime_retrieval_only",),
            delta_only_reminders=("delta_only_memory_carryover",),
            no_giant_sprint_replay=True,
        )


class SprintGovernancePatternRuntime:
    def evaluate(self, samples: tuple[SprintMemorySample, ...]) -> SprintGovernancePatternFrame:
        cognition = _repo_wide_attempts(samples)
        roadmap = _roadmap_attempts(samples)
        continuity = any(sample.continuity_tokens > 3_200 for sample in samples)
        pressure = "MEDIUM" if cognition or roadmap or continuity else "LOW"
        stable = "STABLE" if _unstable_rollovers(samples) == 0 else "UNSTABLE"
        warnings = tuple(
            warning
            for warning in (
                "cognition_expansion_attempt" if cognition else "",
                "roadmap_branching_attempt" if roadmap else "",
                "continuity_accumulation" if continuity else "",
            )
            if warning
        )
        return SprintGovernancePatternFrame(
            sprint_pressure_trend=pressure,
            cognition_expansion_attempts=cognition,
            roadmap_branching_attempts=roadmap,
            continuity_accumulation_trend="MEDIUM" if continuity else "LOW",
            sprint_stability=stable,
            compact_governance_warnings=warnings,
            sprint_simplification_suggestions=("shorten_memory_window", "keep_operational_only"),
            rollover_recommendations=("compact_before_rollover",),
            human_confirmed_orchestration_only=True,
        )


class SprintCompressionRuntime:
    def compress(
        self,
        *,
        patterns: SprintPatternFrame,
        provider: SprintProviderPatternFrame,
        retrieval: SprintRetrievalPatternFrame,
        governance: SprintGovernancePatternFrame,
    ) -> SprintCompressionFrame:
        heuristics = _dedupe(
            patterns.local_patch_success_patterns
            + patterns.bounded_cognition_success_patterns
            + ("evict_stale_memory",)
        )[:5]
        return SprintCompressionFrame(
            bounded_operational_heuristics=heuristics,
            compact_summary_patterns=patterns.successful_sprint_shapes[:3],
            provider_routing_hints=provider.downgrade_safe_suggestions[:3],
            retrieval_heuristics=retrieval.compact_retrieval_recommendations[:3],
            governance_heuristics=governance.sprint_simplification_suggestions[:3],
            giant_memory_accumulation_prevented=True,
            full_historical_replay_forbidden=True,
            hidden_cognition_expansion_forbidden=True,
            summary_only=True,
        )


class SprintEvictionRuntime:
    def evict(
        self,
        *,
        sprint_ids: tuple[str, ...],
        oversized_ids: tuple[str, ...] = (),
        duplicate_patterns: tuple[str, ...] = (),
        obsolete_provider_hints: tuple[str, ...] = (),
    ) -> SprintEvictionFrame:
        active_ids = sprint_ids[-4:]
        stale_ids = tuple(sprint_id for sprint_id in sprint_ids if sprint_id not in active_ids)
        preserved = _dedupe(active_ids + ("LOCAL_PATCH_REQUIRED", "delta_only_memory"))[:6]
        return SprintEvictionFrame(
            evicted_stale_sprint_memory=stale_ids[:4],
            evicted_oversized_sprint_memory=oversized_ids[:4],
            evicted_redundant_sprint_patterns=duplicate_patterns[:4],
            evicted_obsolete_provider_heuristics=obsolete_provider_hints[:4],
            evicted_operational_duplicates=duplicate_patterns[:4],
            preserved_compact_useful_heuristics=preserved,
            stale_memory_eviction_active=True,
            bounded_memory_only=True,
        )


class SprintMemoryRuntime:
    def evaluate(
        self,
        samples: tuple[SprintMemorySample, ...] | None = None,
    ) -> SprintMemoryFrame:
        memory_samples = samples or _default_samples()
        patterns = SprintPatternRuntime().evaluate(memory_samples)
        outcome = SprintOutcomeRuntime().evaluate(memory_samples)
        efficiency = SprintEfficiencyRuntime().evaluate(memory_samples)
        failure = SprintFailurePatternRuntime().detect(memory_samples)
        provider = SprintProviderPatternRuntime().evaluate(memory_samples)
        retrieval = SprintRetrievalPatternRuntime().evaluate(memory_samples)
        governance = SprintGovernancePatternRuntime().evaluate(memory_samples)
        compression = SprintCompressionRuntime().compress(
            patterns=patterns,
            provider=provider,
            retrieval=retrieval,
            governance=governance,
        )
        eviction = SprintEvictionRuntime().evict(
            sprint_ids=tuple(sample.sprint_id for sample in memory_samples),
            oversized_ids=("sprint-full-transcript",),
            duplicate_patterns=("duplicate-local-patch", "duplicate-local-patch"),
            obsolete_provider_hints=("old-premium-default",),
        )
        avoided_analysis = 1_600 + len(compression.bounded_operational_heuristics) * 220
        avoided_failures = 1_200 + len(failure.downgrade_recommendations) * 300
        active = all(
            (
                patterns.compact_operational_patterns_only,
                outcome.bounded_scoring_only,
                compression.summary_only,
                eviction.stale_memory_eviction_active,
                provider.no_hidden_provider_switching,
                governance.human_confirmed_orchestration_only,
            )
        )
        return SprintMemoryFrame(
            patterns=patterns,
            outcome=outcome,
            efficiency=efficiency,
            failure_patterns=failure,
            provider_patterns=provider,
            retrieval_patterns=retrieval,
            governance_patterns=governance,
            compression=compression,
            eviction=eviction,
            sprint_memory_active=active,
            sprint_pattern_active=bool(patterns.successful_sprint_shapes),
            sprint_outcome_active=outcome.deterministic_metrics_only,
            sprint_provider_pattern_active=provider.no_hidden_provider_switching,
            sprint_retrieval_pattern_active=retrieval.no_giant_sprint_replay,
            sprint_governance_pattern_active=governance.human_confirmed_orchestration_only,
            sprint_compression_active=compression.giant_memory_accumulation_prevented,
            sprint_eviction_active=eviction.stale_memory_eviction_active,
            local_only=True,
            deterministic=True,
            summary_only=True,
            bounded_memory_only=True,
            no_hidden_long_term_cognition=True,
            no_full_sprint_transcript_accumulation=True,
            no_autonomous_roadmap_learning=True,
            no_hidden_provider_switching=True,
            provider_routing_distribution=provider.provider_usage_distribution,
            estimated_avoided_manual_sprint_analysis=avoided_analysis,
            estimated_avoided_repeated_sprint_failures=avoided_failures,
            requirement_ids=SPRINT_MEMORY_REQUIREMENT_IDS,
            test_ids=SPRINT_MEMORY_TEST_IDS,
        )


def _default_samples() -> tuple[SprintMemorySample, ...]:
    return (
        SprintMemorySample("sprint-41", "LOW", 1, True, True, True, True, continuity_tokens=900),
        SprintMemorySample(
            "sprint-42", "MEDIUM", 2, True, True, True, True, continuity_tokens=1_400
        ),
        SprintMemorySample(
            "sprint-43",
            "HIGH",
            3,
            False,
            True,
            False,
            False,
            repo_wide_reasoning_attempted=True,
            roadmap_branching_attempted=True,
            continuity_tokens=4_800,
            premium_provider_units=2,
            rollover_stable=False,
        ),
        SprintMemorySample("sprint-44", "LOW", 1, True, True, True, True, continuity_tokens=800),
    )


def _provider_distribution(samples: tuple[SprintMemorySample, ...]) -> dict[str, int]:
    return {
        provider_class: sum(sample.provider_class == provider_class for sample in samples)
        for provider_class in ("HIGH", "MEDIUM", "LOW")
    }


def _premium_units(samples: tuple[SprintMemorySample, ...]) -> int:
    return sum(sample.premium_provider_units for sample in samples)


def _repo_wide_attempts(samples: tuple[SprintMemorySample, ...]) -> int:
    return sum(sample.repo_wide_reasoning_attempted for sample in samples)


def _roadmap_attempts(samples: tuple[SprintMemorySample, ...]) -> int:
    return sum(sample.roadmap_branching_attempted for sample in samples)


def _retrieval_explosions(samples: tuple[SprintMemorySample, ...]) -> int:
    return sum(sample.retrieval_radius > 2 for sample in samples)


def _unstable_rollovers(samples: tuple[SprintMemorySample, ...]) -> int:
    return sum(not sample.rollover_stable for sample in samples)


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / max(1, denominator), 4)


def _stability(ratio: float) -> str:
    if ratio >= 0.9:
        return "HIGH"
    if ratio >= 0.7:
        return "MEDIUM"
    return "LOW"


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


__all__ = [
    "SPRINT_MEMORY_REQUIREMENT_IDS",
    "SPRINT_MEMORY_TEST_IDS",
    "SprintCompressionFrame",
    "SprintCompressionRuntime",
    "SprintEfficiencyFrame",
    "SprintEfficiencyRuntime",
    "SprintEvictionFrame",
    "SprintEvictionRuntime",
    "SprintFailurePatternFrame",
    "SprintFailurePatternRuntime",
    "SprintGovernancePatternFrame",
    "SprintGovernancePatternRuntime",
    "SprintMemoryFrame",
    "SprintMemoryRuntime",
    "SprintMemorySample",
    "SprintOutcomeFrame",
    "SprintOutcomeRuntime",
    "SprintPatternFrame",
    "SprintPatternRuntime",
    "SprintProviderPatternFrame",
    "SprintProviderPatternRuntime",
    "SprintRetrievalPatternFrame",
    "SprintRetrievalPatternRuntime",
]
