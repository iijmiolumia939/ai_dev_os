from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.provider_fatigue import ProviderFatigueRuntime

MEMORY_PRESSURE_WORKLOADS = (
    "long-running bounded engineering session",
    "compact continuity rollover",
    "adjacent-runtime retrieval reuse",
    "sprint closure summarization",
)

BLOCKED_MEMORY_PRESSURE_BEHAVIORS = (
    "autonomous cognition erasure",
    "recursive continuity rewrite",
    "automatic retrieval scope expansion",
    "hidden context mutation",
    "governance runtime bypass",
)

MEMORY_PRESSURE_BASELINE = {
    "oversized_continuity_accumulation": 28,
    "stale_cognition_persistence": 18,
    "repeated_summary_duplication": 21,
    "fragmented_sprint_continuity": 17,
    "retrieval_radius_inflation": 16,
    "summary_entropy_growth": 24,
}


@dataclass(frozen=True)
class CognitiveMemoryPressureFrame:
    cognitive_memory_pressure_active: bool
    workloads: tuple[str, ...]
    blocked_behaviors: tuple[str, ...]
    memory_pressure_score: int
    memory_pressure_label: str
    memory_pressure_summary: str
    bounded_recovery_recommendation: str
    compact_continuity_reset_hints: tuple[str, ...]
    retrieval_narrowing_suggestions: tuple[str, ...]
    human_confirmed_only: bool
    deterministic: bool
    rollback_safe: bool


@dataclass(frozen=True)
class ContinuityInflationFrame:
    continuity_inflation_active: bool
    oversized_continuity_exports: int
    recursive_continuity_accumulation: int
    giant_sprint_closure_growth: int
    compact_summary_corruption: int
    inflation_score: int
    inflation_warning: str
    compactness_reset_recommendation: str
    bounded_continuity_truncation_hints: tuple[str, ...]


@dataclass(frozen=True)
class RetrievalOverloadFrame:
    retrieval_overload_active: bool
    retrieval_radius_expansion: int
    unrelated_retrieval_growth: int
    oversized_context_stitching: int
    adjacent_runtime_violation_pressure: int
    retrieval_overload_score: int
    retrieval_overload_summary: str
    repo_wide_retrieval_expansion_blocked: bool
    recursive_retrieval_loops_blocked: bool
    retrieval_narrowing_recommendation: str


@dataclass(frozen=True)
class SummaryEntropyFrame:
    summary_entropy_active: bool
    summary_noise_growth: int
    repeated_wording_inflation: int
    degraded_compactness_quality: int
    compact_completion_corruption: int
    entropy_score: int
    summary_entropy_summary: str
    bounded_rewrite_recommendation: str


@dataclass(frozen=True)
class ContextFragmentationFrame:
    context_fragmentation_active: bool
    inconsistent_continuity_chains: int
    stale_sprint_references: int
    disconnected_runtime_histories: int
    fragmented_routing_state: int
    fragmentation_score: int
    fragmentation_summary: str
    bounded_continuity_merge_hints: tuple[str, ...]


@dataclass(frozen=True)
class StaleCognitionFrame:
    stale_cognition_active: bool
    stale_cognition_persistence: int
    obsolete_decision_residue: int
    repeated_old_context_reuse: int
    stale_memory_eviction_required: bool
    autonomous_memory_deletion_allowed: bool


@dataclass(frozen=True)
class ContinuityPressureFrame:
    continuity_pressure_active: bool
    continuity_growth_pressure: int
    closure_growth_pressure: int
    continuity_duplication_pressure: int
    continuity_corruption_pressure: int
    continuity_pressure_summary: str


@dataclass(frozen=True)
class CompactnessPressureFrame:
    compactness_pressure_active: bool
    compactness_decay_score: int
    summary_duplication_score: int
    compact_completion_drift: int
    compactness_reset_recommended: bool
    compactness_pressure_summary: str


@dataclass(frozen=True)
class RetrievalRadiusPressureFrame:
    retrieval_radius_pressure_active: bool
    retrieval_radius_score: int
    adjacent_runtime_scope_score: int
    unrelated_context_score: int
    bounded_retrieval_radius: tuple[str, ...]
    automatic_scope_widening_allowed: bool


@dataclass(frozen=True)
class ContinuityRecoveryFrame:
    continuity_recovery_active: bool
    compactness_reset: bool
    continuity_truncation: bool
    stale_memory_eviction: bool
    bounded_retrieval_narrowing: bool
    governance_safe_continuity_refresh: bool
    continuity_recovery_recommendation: str
    autonomous_delete_allowed: bool
    sprint_history_rewrite_allowed: bool
    governance_policy_mutation_allowed: bool


@dataclass(frozen=True)
class MemoryPressureConfidenceFrame:
    memory_pressure_confidence_active: bool
    confidence_score: int
    pressure_label: str
    confidence_summary: tuple[str, ...]


@dataclass(frozen=True)
class MemoryPressureHistoryFrame:
    memory_pressure_history_active: bool
    history_entries: tuple[str, ...]
    bounded_history_size: int
    continuity_pressure_trend: tuple[int, ...]


@dataclass(frozen=True)
class MemoryPressureDecayFrame:
    memory_pressure_decay_active: bool
    continuity_decay: int
    retrieval_decay: int
    summary_entropy_decay: int
    fragmentation_decay: int
    memory_pressure_decay_guard_active: bool


@dataclass(frozen=True)
class MemoryPressureGovernanceFrame:
    memory_pressure_governance_active: bool
    compact_continuity: bool
    bounded_retrieval: bool
    local_patch_discipline: bool
    anti_explosion_governance: bool
    rollback_safe_cognition_management: bool
    human_confirmed_recovery: bool
    autonomous_cognition_erasure: bool
    recursive_continuity_mutation: bool
    governance_runtime_bypassed: bool
    hidden_context_mutation: bool
    retrieval_scope_expansion_allowed: bool
    automatic_context_expansion: bool


@dataclass(frozen=True)
class MemoryPressureEvictionFrame:
    memory_pressure_eviction_active: bool
    stale_cognition_eviction_recommended: bool
    oversized_continuity_payload_evicted: bool
    duplicate_summary_payload_evicted: bool
    eviction_requires_human_confirmation: bool
    max_history_entries: int


@dataclass(frozen=True)
class CognitiveMemoryPressureRuntimeFrame:
    cognitive_memory_pressure: CognitiveMemoryPressureFrame
    continuity_inflation: ContinuityInflationFrame
    retrieval_overload: RetrievalOverloadFrame
    summary_entropy: SummaryEntropyFrame
    context_fragmentation: ContextFragmentationFrame
    stale_cognition: StaleCognitionFrame
    continuity_pressure: ContinuityPressureFrame
    compactness_pressure: CompactnessPressureFrame
    retrieval_radius_pressure: RetrievalRadiusPressureFrame
    continuity_recovery: ContinuityRecoveryFrame
    confidence: MemoryPressureConfidenceFrame
    history: MemoryPressureHistoryFrame
    decay: MemoryPressureDecayFrame
    governance: MemoryPressureGovernanceFrame
    eviction: MemoryPressureEvictionFrame
    cognitive_memory_pressure_active: bool
    continuity_inflation_active: bool
    retrieval_overload_active: bool
    summary_entropy_active: bool
    context_fragmentation_active: bool
    estimated_avoided_context_explosion: int
    estimated_avoided_summary_entropy: int
    estimated_avoided_retrieval_overload: int
    deterministic: bool
    bounded: bool
    human_confirmed_only: bool
    rollback_safe: bool
    local_only: bool
    summary_only: bool


def _pressure_label(score: int) -> str:
    if score <= 25:
        return "MEMORY_PRESSURE_LOW"
    if score <= 45:
        return "MEMORY_PRESSURE_GUARDED"
    return "MEMORY_RECOVERY_REQUIRED"


class CognitiveMemoryPressureRuntime:
    def evaluate(self) -> CognitiveMemoryPressureRuntimeFrame:
        fatigue = ProviderFatigueRuntime().evaluate()
        baseline = MEMORY_PRESSURE_BASELINE
        memory_pressure_score = round(sum(baseline.values()) / len(baseline))
        inflation_score = (
            baseline["oversized_continuity_accumulation"]
            + baseline["repeated_summary_duplication"]
            + fatigue.compactness_decay.summary_growth_inflation["GPT-5.5 reference"]
        )
        retrieval_overload_score = (
            baseline["retrieval_radius_inflation"]
            + fatigue.recursive_pressure.retrieval_scope_expansion_pressure["GPT-5.5 reference"]
            + 8
        )
        entropy_score = (
            baseline["summary_entropy_growth"] + baseline["repeated_summary_duplication"]
        )
        fragmentation_score = baseline["fragmented_sprint_continuity"] + 9
        pressure_label = _pressure_label(memory_pressure_score)

        cognitive_memory_pressure = CognitiveMemoryPressureFrame(
            cognitive_memory_pressure_active=True,
            workloads=MEMORY_PRESSURE_WORKLOADS,
            blocked_behaviors=BLOCKED_MEMORY_PRESSURE_BEHAVIORS,
            memory_pressure_score=memory_pressure_score,
            memory_pressure_label=pressure_label,
            memory_pressure_summary="MEMORY_PRESSURE_LOW_COMPACT_CONTINUITY_GUARDED",
            bounded_recovery_recommendation="RESET_COMPACT_CONTINUITY_AND_NARROW_RETRIEVAL",
            compact_continuity_reset_hints=(
                "Truncate duplicated sprint closure sections before continuation.",
                "Keep only active requirements, changed files, validation, and open risks.",
            ),
            retrieval_narrowing_suggestions=(
                "Use adjacent-runtime retrieval only.",
                "Exclude stale sprint references from the next handoff.",
            ),
            human_confirmed_only=True,
            deterministic=True,
            rollback_safe=True,
        )
        continuity_inflation = ContinuityInflationFrame(
            continuity_inflation_active=True,
            oversized_continuity_exports=baseline["oversized_continuity_accumulation"],
            recursive_continuity_accumulation=12,
            giant_sprint_closure_growth=baseline["repeated_summary_duplication"],
            compact_summary_corruption=baseline["summary_entropy_growth"],
            inflation_score=inflation_score,
            inflation_warning="CONTINUITY_INFLATION_GUARDED",
            compactness_reset_recommendation="COMPACTNESS_RESET_BEFORE_CONTINUITY_REUSE",
            bounded_continuity_truncation_hints=(
                "Drop obsolete completion prose after validation is recorded.",
                "Preserve target IDs, branch, commit, and CI state only.",
            ),
        )
        retrieval_overload = RetrievalOverloadFrame(
            retrieval_overload_active=True,
            retrieval_radius_expansion=baseline["retrieval_radius_inflation"],
            unrelated_retrieval_growth=10,
            oversized_context_stitching=13,
            adjacent_runtime_violation_pressure=8,
            retrieval_overload_score=retrieval_overload_score,
            retrieval_overload_summary="RETRIEVAL_BOUNDED_SCOPE_NARROWING_RECOMMENDED",
            repo_wide_retrieval_expansion_blocked=True,
            recursive_retrieval_loops_blocked=True,
            retrieval_narrowing_recommendation="NARROW_TO_CHANGED_RUNTIME_AND_AUDIT_NEIGHBORHOOD",
        )
        summary_entropy = SummaryEntropyFrame(
            summary_entropy_active=True,
            summary_noise_growth=baseline["summary_entropy_growth"],
            repeated_wording_inflation=baseline["repeated_summary_duplication"],
            degraded_compactness_quality=11,
            compact_completion_corruption=9,
            entropy_score=entropy_score,
            summary_entropy_summary="SUMMARY_ENTROPY_GUARDED_REWRITE_RECOMMENDED",
            bounded_rewrite_recommendation="DEDUP_SUMMARY_WITHOUT_REWRITING_HISTORY",
        )
        context_fragmentation = ContextFragmentationFrame(
            context_fragmentation_active=True,
            inconsistent_continuity_chains=9,
            stale_sprint_references=baseline["stale_cognition_persistence"],
            disconnected_runtime_histories=7,
            fragmented_routing_state=baseline["fragmented_sprint_continuity"],
            fragmentation_score=fragmentation_score,
            fragmentation_summary="FRAGMENTATION_LOW_MERGE_HINTS_ONLY",
            bounded_continuity_merge_hints=(
                "Merge only active sprint state into compact continuity.",
                "Do not rewrite archived sprint history.",
            ),
        )
        stale_cognition = StaleCognitionFrame(
            stale_cognition_active=True,
            stale_cognition_persistence=baseline["stale_cognition_persistence"],
            obsolete_decision_residue=8,
            repeated_old_context_reuse=11,
            stale_memory_eviction_required=True,
            autonomous_memory_deletion_allowed=False,
        )
        continuity_pressure = ContinuityPressureFrame(
            continuity_pressure_active=True,
            continuity_growth_pressure=baseline["oversized_continuity_accumulation"],
            closure_growth_pressure=baseline["repeated_summary_duplication"],
            continuity_duplication_pressure=baseline["repeated_summary_duplication"],
            continuity_corruption_pressure=baseline["summary_entropy_growth"],
            continuity_pressure_summary="CONTINUITY_PRESSURE_GUARDED_COMPACT_RESET_HINTED",
        )
        compactness_pressure = CompactnessPressureFrame(
            compactness_pressure_active=True,
            compactness_decay_score=fatigue.compactness_decay.summary_growth_inflation[
                "GPT-5.5 reference"
            ],
            summary_duplication_score=baseline["repeated_summary_duplication"],
            compact_completion_drift=9,
            compactness_reset_recommended=True,
            compactness_pressure_summary="COMPACTNESS_PRESSURE_LOW_RESET_BEFORE_ROLLOVER",
        )
        retrieval_radius_pressure = RetrievalRadiusPressureFrame(
            retrieval_radius_pressure_active=True,
            retrieval_radius_score=baseline["retrieval_radius_inflation"],
            adjacent_runtime_scope_score=8,
            unrelated_context_score=10,
            bounded_retrieval_radius=(
                "cognitive_memory_pressure",
                "provider_fatigue",
                "runtime_audit",
            ),
            automatic_scope_widening_allowed=False,
        )
        continuity_recovery = ContinuityRecoveryFrame(
            continuity_recovery_active=True,
            compactness_reset=True,
            continuity_truncation=True,
            stale_memory_eviction=True,
            bounded_retrieval_narrowing=True,
            governance_safe_continuity_refresh=True,
            continuity_recovery_recommendation=(
                "RESET_COMPACT_CONTINUITY_TRUNCATE_STALE_MEMORY_NARROW_RETRIEVAL"
            ),
            autonomous_delete_allowed=False,
            sprint_history_rewrite_allowed=False,
            governance_policy_mutation_allowed=False,
        )
        confidence = MemoryPressureConfidenceFrame(
            memory_pressure_confidence_active=True,
            confidence_score=100 - memory_pressure_score,
            pressure_label=pressure_label,
            confidence_summary=(
                f"memory:{memory_pressure_score}:{pressure_label}",
                f"continuity:{inflation_score}:CONTINUITY_INFLATION_GUARDED",
                f"retrieval:{retrieval_overload_score}:RETRIEVAL_BOUNDED",
                f"entropy:{entropy_score}:ENTROPY_GUARDED",
            ),
        )
        history = MemoryPressureHistoryFrame(
            memory_pressure_history_active=True,
            history_entries=(
                "rollover:compact-continuity-pressure-low",
                "retrieval:adjacent-runtime-bounded",
                "summary:entropy-guarded",
                "stale-cognition:eviction-recommended-human-confirmed",
            ),
            bounded_history_size=8,
            continuity_pressure_trend=(18, 20, memory_pressure_score),
        )
        decay = MemoryPressureDecayFrame(
            memory_pressure_decay_active=True,
            continuity_decay=baseline["oversized_continuity_accumulation"],
            retrieval_decay=baseline["retrieval_radius_inflation"],
            summary_entropy_decay=baseline["summary_entropy_growth"],
            fragmentation_decay=baseline["fragmented_sprint_continuity"],
            memory_pressure_decay_guard_active=True,
        )
        governance = MemoryPressureGovernanceFrame(
            memory_pressure_governance_active=True,
            compact_continuity=True,
            bounded_retrieval=True,
            local_patch_discipline=True,
            anti_explosion_governance=True,
            rollback_safe_cognition_management=True,
            human_confirmed_recovery=True,
            autonomous_cognition_erasure=False,
            recursive_continuity_mutation=False,
            governance_runtime_bypassed=False,
            hidden_context_mutation=False,
            retrieval_scope_expansion_allowed=False,
            automatic_context_expansion=False,
        )
        eviction = MemoryPressureEvictionFrame(
            memory_pressure_eviction_active=True,
            stale_cognition_eviction_recommended=True,
            oversized_continuity_payload_evicted=False,
            duplicate_summary_payload_evicted=False,
            eviction_requires_human_confirmation=True,
            max_history_entries=8,
        )
        return CognitiveMemoryPressureRuntimeFrame(
            cognitive_memory_pressure=cognitive_memory_pressure,
            continuity_inflation=continuity_inflation,
            retrieval_overload=retrieval_overload,
            summary_entropy=summary_entropy,
            context_fragmentation=context_fragmentation,
            stale_cognition=stale_cognition,
            continuity_pressure=continuity_pressure,
            compactness_pressure=compactness_pressure,
            retrieval_radius_pressure=retrieval_radius_pressure,
            continuity_recovery=continuity_recovery,
            confidence=confidence,
            history=history,
            decay=decay,
            governance=governance,
            eviction=eviction,
            cognitive_memory_pressure_active=(
                cognitive_memory_pressure.cognitive_memory_pressure_active
            ),
            continuity_inflation_active=continuity_inflation.continuity_inflation_active,
            retrieval_overload_active=retrieval_overload.retrieval_overload_active,
            summary_entropy_active=summary_entropy.summary_entropy_active,
            context_fragmentation_active=context_fragmentation.context_fragmentation_active,
            estimated_avoided_context_explosion=1800,
            estimated_avoided_summary_entropy=640,
            estimated_avoided_retrieval_overload=920,
            deterministic=True,
            bounded=True,
            human_confirmed_only=True,
            rollback_safe=True,
            local_only=True,
            summary_only=True,
        )


__all__ = [
    "BLOCKED_MEMORY_PRESSURE_BEHAVIORS",
    "MEMORY_PRESSURE_BASELINE",
    "MEMORY_PRESSURE_WORKLOADS",
    "CognitiveMemoryPressureFrame",
    "CognitiveMemoryPressureRuntime",
    "CognitiveMemoryPressureRuntimeFrame",
    "CompactnessPressureFrame",
    "ContextFragmentationFrame",
    "ContinuityInflationFrame",
    "ContinuityPressureFrame",
    "ContinuityRecoveryFrame",
    "MemoryPressureConfidenceFrame",
    "MemoryPressureDecayFrame",
    "MemoryPressureEvictionFrame",
    "MemoryPressureGovernanceFrame",
    "MemoryPressureHistoryFrame",
    "RetrievalOverloadFrame",
    "RetrievalRadiusPressureFrame",
    "StaleCognitionFrame",
    "SummaryEntropyFrame",
]
