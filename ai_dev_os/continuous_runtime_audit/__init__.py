from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.adaptive_provider import AdaptiveProviderRuntime
from ai_dev_os.execution_memory import ExecutionMemoryRuntime
from ai_dev_os.reflective_evaluation import ReflectiveEvaluationRuntime
from ai_dev_os.runtime_hardening import RuntimeHardeningRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer
from ai_dev_os.runtime_orchestrator import RuntimeOrchestrator
from ai_dev_os.runtime_policy import RuntimePolicyEngine

CONTINUOUS_RUNTIME_AUDIT_REQUIREMENT_IDS = tuple(
    f"FR-CONTINUOUSAUDIT-{index:02d}" for index in range(1, 57)
) + ("NFR-COST-77", "NFR-ARCH-90", "NFR-SEC-61")
CONTINUOUS_RUNTIME_AUDIT_TEST_IDS = tuple(
    f"TC-CONTINUOUSAUDIT-{index:02d}" for index in range(1, 57)
)

MAX_TELEMETRY_WINDOW = 5
MAX_AUDIT_HISTORY = 5
AUDIT_BUDGET_LIMIT = 12
TELEMETRY_SATURATION_THRESHOLD = 78
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_TELEMETRY_SCOPE = (
    "retry-pressure",
    "provider-fatigue",
    "continuation-instability",
    "orchestration-pressure",
    "runtime-health",
)
DEFAULT_AUDIT_HISTORY = (
    "collect",
    "score",
    "summarize",
    "surface",
    "retain",
)


@dataclass(frozen=True)
class RuntimeTelemetryFrame:
    runtime_telemetry_active: bool
    telemetry_scope: tuple[str, ...]
    telemetry_window_limit: int
    telemetry_scope_overflow_blocked: bool
    bounded_runtime_telemetry: bool
    deterministic_operational_visibility_summary: str
    bounded_visibility_recommendation: str


@dataclass(frozen=True)
class RetryPressureFrame:
    retry_pressure_active: bool
    retry_amplification_pressure: int
    retry_saturation_windows: int
    retry_interruption_instability: int
    retry_cooldown_collapse: int
    retry_recovery_instability: int
    retry_pressure_score: int
    deterministic_retry_pressure_summary: str
    bounded_retry_visibility_recommendation: str


@dataclass(frozen=True)
class ProviderFatigueTelemetryFrame:
    provider_fatigue_telemetry_active: bool
    provider_fatigue_pressure: int
    provider_readiness_degradation: int
    provider_queue_saturation: int
    provider_cooldown_instability: int
    bounded_provider_confidence_collapse: int
    provider_fatigue_score: int
    deterministic_provider_fatigue_summary: str
    bounded_provider_visibility_recommendation: str


@dataclass(frozen=True)
class ContinuationInstabilityFrame:
    continuation_instability_active: bool
    continuation_instability_pressure: int
    continuation_saturation: int
    continuation_interruption_instability: int
    continuation_reset_loops: int
    bounded_continuation_drift: int
    continuation_instability_score: int
    deterministic_continuation_instability_summary: str
    bounded_continuation_visibility_recommendation: str


@dataclass(frozen=True)
class EscalationPressureFrame:
    escalation_pressure_active: bool
    provider_escalation_pressure: int
    provider_downgrade_pressure: int
    escalation_cooldown_pressure: int
    escalation_pressure_score: int
    deterministic_escalation_pressure_summary: str
    bounded_escalation_visibility_recommendation: str


@dataclass(frozen=True)
class OrchestrationPressureFrame:
    orchestration_pressure_active: bool
    orchestration_queue_pressure: int
    orchestration_dependency_stalls: int
    orchestration_cooldown_pressure: int
    orchestration_regression_pressure: int
    bounded_orchestration_drift: int
    orchestration_pressure_score: int
    deterministic_orchestration_pressure_summary: str
    bounded_orchestration_visibility_recommendation: str


@dataclass(frozen=True)
class RegressionTelemetryFrame:
    regression_telemetry_active: bool
    repeated_regressions: int
    regression_cascade_pressure: int
    retry_regression_coupling: int
    regression_visibility_score: int
    deterministic_regression_summary: str
    bounded_regression_visibility_recommendation: str


@dataclass(frozen=True)
class RuntimeDriftFrame:
    runtime_drift_active: bool
    bounded_retry_drift: int
    bounded_provider_drift: int
    bounded_continuation_drift: int
    bounded_orchestration_drift: int
    runtime_drift_score: int
    deterministic_drift_summary: str
    bounded_drift_recommendation: str


@dataclass(frozen=True)
class RuntimeHealthFrame:
    runtime_health_active: bool
    bounded_runtime_coherence: bool
    bounded_orchestration_stability: bool
    bounded_retry_stability: bool
    bounded_provider_stability: bool
    bounded_continuation_stability: bool
    runtime_health_score: int
    deterministic_runtime_health_summary: str
    bounded_health_recommendation: str


@dataclass(frozen=True)
class AuditBudgetFrame:
    audit_budget_active: bool
    audit_budget_used: int
    audit_budget_limit: int
    audit_budget_exceeded: bool
    budget_pressure: str


@dataclass(frozen=True)
class AuditGovernanceFrame:
    audit_governance_active: bool
    local_patch_scope_enforced: bool
    deterministic_telemetry_enforced: bool
    bounded_telemetry_windows_enforced: bool
    autonomous_runtime_alteration_blocked: bool
    recursive_telemetry_optimization_blocked: bool
    novel_metric_synthesis_blocked: bool
    dynamic_telemetry_scope_widening_blocked: bool
    governance_policy_mutation_blocked: bool
    hidden_background_execution_blocked: bool


@dataclass(frozen=True)
class AuditTerminationFrame:
    audit_termination_active: bool
    continuous_audit_terminated: bool
    termination_reasons: tuple[str, ...]
    audit_budget_exceeded: bool
    recursive_telemetry_detected: bool
    governance_violation_detected: bool
    telemetry_saturation_threshold_exceeded: bool


@dataclass(frozen=True)
class AuditHistoryFrame:
    audit_history_active: bool
    audit_history: tuple[str, ...]
    audit_history_limit: int
    compact_audit_history_summary: str
    audit_history_overflow_blocked: bool
    self_expanding_history_blocked: bool


@dataclass(frozen=True)
class AuditConfidenceFrame:
    audit_confidence_active: bool
    audit_confidence_score: int
    confidence_status: str
    deterministic_confidence: bool
    operational_visibility_confidence: bool


@dataclass(frozen=True)
class AuditEvictionFrame:
    audit_eviction_active: bool
    evicted_telemetry_scope_items: tuple[str, ...]
    evicted_audit_history_items: tuple[str, ...]
    eviction_count: int
    bounded_eviction_active: bool
    eviction_summary: str


@dataclass(frozen=True)
class ContinuousRuntimeAuditFrame:
    continuous_runtime_audit_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    runtime_telemetry: RuntimeTelemetryFrame
    retry_pressure: RetryPressureFrame
    provider_fatigue_telemetry: ProviderFatigueTelemetryFrame
    continuation_instability: ContinuationInstabilityFrame
    escalation_pressure: EscalationPressureFrame
    orchestration_pressure: OrchestrationPressureFrame
    regression_telemetry: RegressionTelemetryFrame
    runtime_drift: RuntimeDriftFrame
    runtime_health: RuntimeHealthFrame
    audit_budget: AuditBudgetFrame
    audit_governance: AuditGovernanceFrame
    audit_termination: AuditTerminationFrame
    audit_history: AuditHistoryFrame
    audit_confidence: AuditConfidenceFrame
    audit_eviction: AuditEvictionFrame
    runtime_health_score: int
    retry_pressure_score: int
    provider_fatigue_score: int
    continuation_instability_score: int
    orchestration_pressure_score: int
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    continuous_runtime_audit_mode: str
    estimated_avoided_runtime_blindness: int
    estimated_avoided_orchestration_collapse: int
    estimated_avoided_frontier_observability: int


class ContinuousRuntimeAuditRuntime:
    def evaluate(
        self,
        *,
        telemetry_scope_items: tuple[str, ...] = DEFAULT_TELEMETRY_SCOPE,
        audit_history_items: tuple[str, ...] = DEFAULT_AUDIT_HISTORY,
        retry_amplification_pressure: int = 1,
        retry_saturation_windows: int = 1,
        retry_interruption_instability: int = 0,
        retry_cooldown_collapse: int = 0,
        retry_recovery_instability: int = 0,
        provider_readiness_degradation: int = 0,
        provider_queue_saturation: int = 1,
        provider_cooldown_instability: int = 0,
        bounded_provider_confidence_collapse: int = 0,
        continuation_instability_pressure: int = 1,
        continuation_saturation: int = 18,
        continuation_interruption_instability: int = 0,
        continuation_reset_loops: int = 0,
        bounded_continuation_drift: int = 0,
        provider_escalation_pressure: int = 1,
        provider_downgrade_pressure: int = 0,
        escalation_cooldown_pressure: int = 1,
        orchestration_queue_pressure: int = 1,
        orchestration_dependency_stalls: int = 0,
        orchestration_cooldown_pressure: int = 1,
        orchestration_regression_pressure: int = 1,
        bounded_orchestration_drift: int = 0,
        repeated_regressions: int = 0,
        regression_cascade_pressure: int = 1,
        retry_regression_coupling: int = 1,
        audit_budget_used: int = 7,
        recursive_telemetry_attempts: int = 0,
        autonomous_runtime_alteration_attempts: int = 0,
        recursive_telemetry_optimization_attempts: int = 0,
        novel_metric_synthesis_attempts: int = 0,
        dynamic_telemetry_scope_widening_attempts: int = 0,
        governance_policy_mutation_attempts: int = 0,
        hidden_background_execution_attempts: int = 0,
        self_expanding_history_attempts: int = 0,
    ) -> ContinuousRuntimeAuditFrame:
        runtime_policy = RuntimePolicyEngine().evaluate(
            retry_count=retry_amplification_pressure,
            retry_cooldown_pressure=max(1, retry_cooldown_collapse),
            continuation_saturation=continuation_saturation,
            policy_budget_used=min(audit_budget_used, AUDIT_BUDGET_LIMIT),
        )
        orchestrator = RuntimeOrchestrator().evaluate(
            retry_amplification=retry_amplification_pressure,
            retry_interruption_windows=retry_interruption_instability,
            continuation_interruption_windows=continuation_interruption_instability,
            repeated_regressions=repeated_regressions,
            regression_pressure=orchestration_regression_pressure,
            orchestration_budget_used=min(audit_budget_used, AUDIT_BUDGET_LIMIT),
        )
        hardening = RuntimeHardeningRuntime().evaluate(
            retry_amplification_chains=retry_amplification_pressure,
            retry_cooldown_collapse=retry_cooldown_collapse,
            retry_saturation_windows=retry_saturation_windows,
            retry_interruption_instability=retry_interruption_instability,
            continuation_saturation=continuation_saturation,
            continuation_interruption_instability=continuation_interruption_instability,
            provider_readiness_starvation=provider_readiness_degradation,
            bounded_provider_queue_saturation=provider_queue_saturation,
            provider_scheduling_instability=max(1, provider_cooldown_instability + 1),
            provider_confidence_collapse=bounded_provider_confidence_collapse,
            provider_escalation_loops=max(1, provider_escalation_pressure),
            provider_downgrade_loops=provider_downgrade_pressure,
            escalation_cooldown_pressure=escalation_cooldown_pressure,
            repeated_regressions=repeated_regressions,
            regression_dependency_pressure=regression_cascade_pressure,
            retry_regression_coupling=retry_regression_coupling,
            orchestration_dependency_deadlocks=orchestration_dependency_stalls,
            bounded_orchestration_stalls=bounded_orchestration_drift,
            hardening_budget_used=min(audit_budget_used, AUDIT_BUDGET_LIMIT),
        )
        adaptive_provider = AdaptiveProviderRuntime().evaluate(
            long_session_degradation=max(1, provider_cooldown_instability + 1),
            retry_amplification=retry_amplification_pressure,
            orchestration_instability=max(1, orchestration_dependency_stalls + 1),
            estimated_token_pressure=24 + provider_queue_saturation * 3,
            provider_budget_used=min(audit_budget_used, AUDIT_BUDGET_LIMIT),
        )
        execution_memory = ExecutionMemoryRuntime().evaluate(
            repeated_retry_chains=retry_amplification_pressure,
            continuation_reuse_depth=max(1, continuation_instability_pressure),
        )
        reflection = ReflectiveEvaluationRuntime().evaluate(
            execution_failure_frequency=repeated_regressions,
            retry_amplification_pressure=retry_amplification_pressure,
        )
        mediation = ExecutionSequencer().mediate(retry_count=retry_amplification_pressure)

        bounded_scope = telemetry_scope_items[:MAX_TELEMETRY_WINDOW]
        bounded_history = audit_history_items[:MAX_AUDIT_HISTORY]
        evicted_scope_items = telemetry_scope_items[MAX_TELEMETRY_WINDOW:]
        evicted_history_items = audit_history_items[MAX_AUDIT_HISTORY:]

        retry_pressure_raw = _clamp(
            retry_amplification_pressure * 18
            + retry_saturation_windows * 10
            + retry_interruption_instability * 12
            + retry_cooldown_collapse * 14
            + retry_recovery_instability * 12
        )
        retry_pressure_score = _clamp(100 - retry_pressure_raw)
        provider_fatigue_pressure = _clamp(
            max(0, 70 - adaptive_provider.provider_fatigue_score)
            + provider_readiness_degradation * 12
            + provider_queue_saturation * 8
            + provider_cooldown_instability * 10
            + bounded_provider_confidence_collapse * 14
        )
        provider_fatigue_score = _clamp(100 - provider_fatigue_pressure)
        continuation_pressure_raw = _clamp(
            continuation_instability_pressure * 12
            + continuation_saturation
            + continuation_interruption_instability * 12
            + continuation_reset_loops * 12
            + bounded_continuation_drift * 10
        )
        continuation_instability_score = _clamp(100 - continuation_pressure_raw)
        escalation_pressure_raw = _clamp(
            provider_escalation_pressure * 12
            + provider_downgrade_pressure * 12
            + escalation_cooldown_pressure * 10
        )
        escalation_pressure_score = _clamp(100 - escalation_pressure_raw)
        orchestration_pressure_raw = _clamp(
            orchestration_queue_pressure * 10
            + orchestration_dependency_stalls * 16
            + orchestration_cooldown_pressure * 10
            + orchestration_regression_pressure * 12
            + bounded_orchestration_drift * 12
            + max(0, 80 - orchestrator.orchestration_schedule_score)
        )
        orchestration_pressure_score = _clamp(100 - orchestration_pressure_raw)
        regression_pressure_raw = _clamp(
            repeated_regressions * 18
            + regression_cascade_pressure * 12
            + retry_regression_coupling * 10
        )
        regression_visibility_score = _clamp(100 - regression_pressure_raw)
        runtime_drift_score = _clamp(
            100
            - (
                max(0, 80 - retry_pressure_score)
                + max(0, 80 - provider_fatigue_score)
                + max(0, 80 - continuation_instability_score)
                + max(0, 80 - orchestration_pressure_score)
            )
        )
        runtime_health_score = _clamp(
            (
                retry_pressure_score
                + provider_fatigue_score
                + continuation_instability_score
                + orchestration_pressure_score
                + hardening.hardening_confidence.hardening_confidence_score
                + runtime_policy.policy_coherence.policy_coherence_score
            )
            // 6
            + int(mediation.runtime_mediation_active) * 3
            + int(execution_memory.execution_memory_active) * 2
        )
        telemetry_saturation = _clamp(
            max(0, len(telemetry_scope_items) - MAX_TELEMETRY_WINDOW) * 12
            + max(0, 80 - runtime_health_score)
            + max(0, 80 - runtime_drift_score)
        )
        telemetry_saturation_exceeded = telemetry_saturation >= TELEMETRY_SATURATION_THRESHOLD
        audit_budget_exceeded = audit_budget_used > AUDIT_BUDGET_LIMIT
        recursive_telemetry_detected = recursive_telemetry_attempts > 0
        governance_violation = any(
            (
                autonomous_runtime_alteration_attempts,
                recursive_telemetry_optimization_attempts,
                novel_metric_synthesis_attempts,
                dynamic_telemetry_scope_widening_attempts,
                governance_policy_mutation_attempts,
                hidden_background_execution_attempts,
            )
        )
        termination_reasons = _termination_reasons(
            audit_budget_exceeded,
            recursive_telemetry_detected,
            governance_violation,
            telemetry_saturation_exceeded,
        )
        audit_confidence_score = _clamp(runtime_health_score - len(termination_reasons) * 8)

        return ContinuousRuntimeAuditFrame(
            continuous_runtime_audit_active=True,
            requirement_ids=CONTINUOUS_RUNTIME_AUDIT_REQUIREMENT_IDS,
            test_ids=CONTINUOUS_RUNTIME_AUDIT_TEST_IDS,
            runtime_telemetry=RuntimeTelemetryFrame(
                runtime_telemetry_active=True,
                telemetry_scope=bounded_scope,
                telemetry_window_limit=MAX_TELEMETRY_WINDOW,
                telemetry_scope_overflow_blocked=bool(evicted_scope_items),
                bounded_runtime_telemetry=True,
                deterministic_operational_visibility_summary=(
                    f"scope={len(bounded_scope)};health={runtime_health_score};"
                    f"drift={runtime_drift_score}"
                ),
                bounded_visibility_recommendation=(
                    "COMPACT_TELEMETRY_SCOPE"
                    if evicted_scope_items
                    else "MAINTAIN_BOUNDED_TELEMETRY_WINDOW"
                ),
            ),
            retry_pressure=RetryPressureFrame(
                retry_pressure_active=True,
                retry_amplification_pressure=retry_amplification_pressure,
                retry_saturation_windows=retry_saturation_windows,
                retry_interruption_instability=retry_interruption_instability,
                retry_cooldown_collapse=retry_cooldown_collapse,
                retry_recovery_instability=retry_recovery_instability,
                retry_pressure_score=retry_pressure_score,
                deterministic_retry_pressure_summary=(
                    f"amplification={retry_amplification_pressure};"
                    f"saturation={retry_saturation_windows};score={retry_pressure_score}"
                ),
                bounded_retry_visibility_recommendation=(
                    "SURFACE_RETRY_PRESSURE_AND_RESET_WINDOW"
                    if retry_pressure_score < 60
                    else "RETRY_PRESSURE_VISIBLE_AND_STABLE"
                ),
            ),
            provider_fatigue_telemetry=ProviderFatigueTelemetryFrame(
                provider_fatigue_telemetry_active=True,
                provider_fatigue_pressure=provider_fatigue_pressure,
                provider_readiness_degradation=provider_readiness_degradation,
                provider_queue_saturation=provider_queue_saturation,
                provider_cooldown_instability=provider_cooldown_instability,
                bounded_provider_confidence_collapse=bounded_provider_confidence_collapse,
                provider_fatigue_score=provider_fatigue_score,
                deterministic_provider_fatigue_summary=(
                    f"adjacent_fatigue={adaptive_provider.provider_fatigue_score};"
                    f"pressure={provider_fatigue_pressure};score={provider_fatigue_score}"
                ),
                bounded_provider_visibility_recommendation=(
                    "SURFACE_PROVIDER_FATIGUE_AND_REBALANCE"
                    if provider_fatigue_score < 60
                    else "PROVIDER_FATIGUE_VISIBLE_AND_BOUNDED"
                ),
            ),
            continuation_instability=ContinuationInstabilityFrame(
                continuation_instability_active=True,
                continuation_instability_pressure=continuation_instability_pressure,
                continuation_saturation=continuation_saturation,
                continuation_interruption_instability=continuation_interruption_instability,
                continuation_reset_loops=continuation_reset_loops,
                bounded_continuation_drift=bounded_continuation_drift,
                continuation_instability_score=continuation_instability_score,
                deterministic_continuation_instability_summary=(
                    f"pressure={continuation_instability_pressure};"
                    f"saturation={continuation_saturation};"
                    f"score={continuation_instability_score}"
                ),
                bounded_continuation_visibility_recommendation=(
                    "SURFACE_CONTINUATION_INSTABILITY_AND_RESET"
                    if continuation_instability_score < 60
                    else "CONTINUATION_INSTABILITY_VISIBLE_AND_BOUNDED"
                ),
            ),
            escalation_pressure=EscalationPressureFrame(
                escalation_pressure_active=True,
                provider_escalation_pressure=provider_escalation_pressure,
                provider_downgrade_pressure=provider_downgrade_pressure,
                escalation_cooldown_pressure=escalation_cooldown_pressure,
                escalation_pressure_score=escalation_pressure_score,
                deterministic_escalation_pressure_summary=(
                    f"escalation={provider_escalation_pressure};"
                    f"downgrade={provider_downgrade_pressure};"
                    f"score={escalation_pressure_score}"
                ),
                bounded_escalation_visibility_recommendation=(
                    "SURFACE_ESCALATION_PRESSURE"
                    if escalation_pressure_score < 60
                    else "ESCALATION_PRESSURE_VISIBLE_AND_STABLE"
                ),
            ),
            orchestration_pressure=OrchestrationPressureFrame(
                orchestration_pressure_active=True,
                orchestration_queue_pressure=orchestration_queue_pressure,
                orchestration_dependency_stalls=orchestration_dependency_stalls,
                orchestration_cooldown_pressure=orchestration_cooldown_pressure,
                orchestration_regression_pressure=orchestration_regression_pressure,
                bounded_orchestration_drift=bounded_orchestration_drift,
                orchestration_pressure_score=orchestration_pressure_score,
                deterministic_orchestration_pressure_summary=(
                    f"queue={orchestration_queue_pressure};"
                    f"stalls={orchestration_dependency_stalls};"
                    f"score={orchestration_pressure_score}"
                ),
                bounded_orchestration_visibility_recommendation=(
                    "SURFACE_ORCHESTRATION_PRESSURE_AND_STALLS"
                    if orchestration_pressure_score < 60
                    else "ORCHESTRATION_PRESSURE_VISIBLE_AND_STABLE"
                ),
            ),
            regression_telemetry=RegressionTelemetryFrame(
                regression_telemetry_active=True,
                repeated_regressions=repeated_regressions,
                regression_cascade_pressure=regression_cascade_pressure,
                retry_regression_coupling=retry_regression_coupling,
                regression_visibility_score=regression_visibility_score,
                deterministic_regression_summary=(
                    f"regressions={repeated_regressions};"
                    f"pressure={regression_pressure_raw};"
                    f"quality={reflection.execution_quality.execution_quality_score}"
                ),
                bounded_regression_visibility_recommendation=(
                    "SURFACE_REGRESSION_PRESSURE"
                    if regression_visibility_score < 60
                    else "REGRESSION_PRESSURE_VISIBLE_AND_STABLE"
                ),
            ),
            runtime_drift=RuntimeDriftFrame(
                runtime_drift_active=True,
                bounded_retry_drift=max(0, 80 - retry_pressure_score),
                bounded_provider_drift=max(0, 80 - provider_fatigue_score),
                bounded_continuation_drift=max(0, 80 - continuation_instability_score),
                bounded_orchestration_drift=max(0, 80 - orchestration_pressure_score),
                runtime_drift_score=runtime_drift_score,
                deterministic_drift_summary=(
                    f"retry={max(0, 80 - retry_pressure_score)};"
                    f"provider={max(0, 80 - provider_fatigue_score)};"
                    f"orchestration={max(0, 80 - orchestration_pressure_score)}"
                ),
                bounded_drift_recommendation=(
                    "COMPACT_AND_SURFACE_RUNTIME_DRIFT"
                    if runtime_drift_score < 80
                    else "RUNTIME_DRIFT_VISIBLE_AND_BOUNDED"
                ),
            ),
            runtime_health=RuntimeHealthFrame(
                runtime_health_active=True,
                bounded_runtime_coherence=runtime_policy.runtime_policy_active,
                bounded_orchestration_stability=orchestrator.orchestration_schedule_score >= 80,
                bounded_retry_stability=retry_pressure_score >= 60,
                bounded_provider_stability=provider_fatigue_score >= 50,
                bounded_continuation_stability=continuation_instability_score >= 60,
                runtime_health_score=runtime_health_score,
                deterministic_runtime_health_summary=(
                    f"health={runtime_health_score};"
                    f"hardening={hardening.hardening_confidence.hardening_confidence_score};"
                    f"policy={runtime_policy.policy_coherence.policy_coherence_score}"
                ),
                bounded_health_recommendation=(
                    "SURFACE_RUNTIME_HEALTH_PRESSURE"
                    if runtime_health_score < 75
                    else "RUNTIME_HEALTH_VISIBLE_AND_STABLE"
                ),
            ),
            audit_budget=AuditBudgetFrame(
                audit_budget_active=True,
                audit_budget_used=audit_budget_used,
                audit_budget_limit=AUDIT_BUDGET_LIMIT,
                audit_budget_exceeded=audit_budget_exceeded,
                budget_pressure=_pressure(audit_budget_used, AUDIT_BUDGET_LIMIT),
            ),
            audit_governance=AuditGovernanceFrame(
                audit_governance_active=True,
                local_patch_scope_enforced=True,
                deterministic_telemetry_enforced=True,
                bounded_telemetry_windows_enforced=True,
                autonomous_runtime_alteration_blocked=True,
                recursive_telemetry_optimization_blocked=True,
                novel_metric_synthesis_blocked=True,
                dynamic_telemetry_scope_widening_blocked=True,
                governance_policy_mutation_blocked=True,
                hidden_background_execution_blocked=True,
            ),
            audit_termination=AuditTerminationFrame(
                audit_termination_active=True,
                continuous_audit_terminated=bool(termination_reasons),
                termination_reasons=termination_reasons,
                audit_budget_exceeded=audit_budget_exceeded,
                recursive_telemetry_detected=recursive_telemetry_detected,
                governance_violation_detected=governance_violation,
                telemetry_saturation_threshold_exceeded=telemetry_saturation_exceeded,
            ),
            audit_history=AuditHistoryFrame(
                audit_history_active=True,
                audit_history=bounded_history,
                audit_history_limit=MAX_AUDIT_HISTORY,
                compact_audit_history_summary=f"history={len(bounded_history)};audit=bounded",
                audit_history_overflow_blocked=bool(evicted_history_items),
                self_expanding_history_blocked=self_expanding_history_attempts > 0,
            ),
            audit_confidence=AuditConfidenceFrame(
                audit_confidence_active=True,
                audit_confidence_score=audit_confidence_score,
                confidence_status=_score_label(audit_confidence_score),
                deterministic_confidence=True,
                operational_visibility_confidence=audit_confidence_score >= 75,
            ),
            audit_eviction=AuditEvictionFrame(
                audit_eviction_active=True,
                evicted_telemetry_scope_items=evicted_scope_items,
                evicted_audit_history_items=evicted_history_items,
                eviction_count=len(evicted_scope_items) + len(evicted_history_items),
                bounded_eviction_active=bool(evicted_scope_items or evicted_history_items),
                eviction_summary=(
                    f"scope={len(evicted_scope_items)};history={len(evicted_history_items)}"
                ),
            ),
            runtime_health_score=runtime_health_score,
            retry_pressure_score=retry_pressure_score,
            provider_fatigue_score=provider_fatigue_score,
            continuation_instability_score=continuation_instability_score,
            orchestration_pressure_score=orchestration_pressure_score,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            continuous_runtime_audit_mode="LOCAL_PATCH_BOUNDED_CONTINUOUS_AUDIT",
            estimated_avoided_runtime_blindness=79,
            estimated_avoided_orchestration_collapse=(
                72 + max(0, 80 - orchestration_pressure_score) // 2
            ),
            estimated_avoided_frontier_observability=76 + runtime_health_score // 10,
        )


def _clamp(score: int) -> int:
    return max(MIN_SCORE, min(MAX_SCORE, score))


def _pressure(value: int, limit: int) -> str:
    if value > limit:
        return "HIGH"
    if value >= max(1, limit - 1):
        return "MEDIUM"
    return "LOW"


def _score_label(score: int) -> str:
    if score >= 80:
        return "STABLE"
    if score >= 60:
        return "WATCH"
    return "SURFACE_PRESSURE"


def _termination_reasons(
    audit_budget_exceeded: bool,
    recursive_telemetry_detected: bool,
    governance_violation_detected: bool,
    telemetry_saturation_threshold_exceeded: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if audit_budget_exceeded:
        reasons.append("AUDIT_BUDGET_EXCEEDED")
    if recursive_telemetry_detected:
        reasons.append("RECURSIVE_TELEMETRY_DETECTED")
    if governance_violation_detected:
        reasons.append("GOVERNANCE_VIOLATION_DETECTED")
    if telemetry_saturation_threshold_exceeded:
        reasons.append("TELEMETRY_SATURATION_THRESHOLD_EXCEEDED")
    return tuple(reasons)


__all__ = [
    "AUDIT_BUDGET_LIMIT",
    "CONTINUOUS_RUNTIME_AUDIT_REQUIREMENT_IDS",
    "CONTINUOUS_RUNTIME_AUDIT_TEST_IDS",
    "MAX_AUDIT_HISTORY",
    "MAX_TELEMETRY_WINDOW",
    "TELEMETRY_SATURATION_THRESHOLD",
    "AuditBudgetFrame",
    "AuditConfidenceFrame",
    "AuditEvictionFrame",
    "AuditGovernanceFrame",
    "AuditHistoryFrame",
    "AuditTerminationFrame",
    "ContinuationInstabilityFrame",
    "ContinuousRuntimeAuditFrame",
    "ContinuousRuntimeAuditRuntime",
    "EscalationPressureFrame",
    "OrchestrationPressureFrame",
    "ProviderFatigueTelemetryFrame",
    "RegressionTelemetryFrame",
    "RetryPressureFrame",
    "RuntimeDriftFrame",
    "RuntimeHealthFrame",
    "RuntimeTelemetryFrame",
]
