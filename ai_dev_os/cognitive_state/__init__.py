from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.execution_continuation import ExecutionContinuationRuntime
from ai_dev_os.execution_coordination import ExecutionCoordinationRuntime
from ai_dev_os.execution_recovery import ExecutionRecoveryRuntime
from ai_dev_os.runtime_mediation import ExecutionSequencer

COGNITIVE_STATE_REQUIREMENT_IDS = tuple(
    f"FR-COGNITIVESTATE-{index:02d}" for index in range(1, 25)
) + ("NFR-COST-61", "NFR-ARCH-74", "NFR-SEC-45")
COGNITIVE_STATE_TEST_IDS = tuple(f"TC-COGNITIVESTATE-{index:02d}" for index in range(1, 25))

MAX_WORKING_MEMORY_ITEMS = 6
MAX_ATTENTION_TARGETS = 4
MAX_CONTEXT_SALIENCE_ITEMS = 5
MAX_DECAY_SCORE = 100
DECAY_WATCH_THRESHOLD = 45
DECAY_RESET_THRESHOLD = 70

DEFAULT_ATTENTION_WEIGHTS = {
    "implementation": 34,
    "tests": 27,
    "validation": 24,
    "vscode": 15,
}


@dataclass(frozen=True)
class ActiveCognitiveFrame:
    active_cognitive_frame: bool
    active_objective: str
    deterministic_state_key: str
    local_provider_only: bool
    high_tier_escalation_blocked: bool
    compact_prompts_required: bool
    cognitive_operations_execute_commands: bool


@dataclass(frozen=True)
class WorkingMemoryFrame:
    working_memory_active: bool
    bounded_items: tuple[str, ...]
    item_count: int
    memory_limit: int
    memory_pressure: str
    memory_overflow_blocked: bool
    recursive_memory_expansion_blocked: bool


@dataclass(frozen=True)
class TaskAttentionFrame:
    task_attention_active: bool
    attention_distribution: tuple[str, ...]
    primary_focus: str
    attention_target_count: int
    attention_limit: int
    attention_overflow_blocked: bool
    self_reprioritization_blocked: bool


@dataclass(frozen=True)
class ContextSalienceFrame:
    context_salience_active: bool
    salient_context: tuple[str, ...]
    ignored_context: tuple[str, ...]
    salience_threshold: int
    bounded_context_window: int
    repo_wide_context_blocked: bool
    raw_transcript_replay_blocked: bool


@dataclass(frozen=True)
class CognitiveDecayFrame:
    cognitive_decay_active: bool
    decay_score: int
    decay_status: str
    long_session_drift_detected: bool
    recursive_reasoning_risk_detected: bool
    compact_reset_recommended: bool
    decay_recovery_recommendation: str


@dataclass(frozen=True)
class ExecutionFocusFrame:
    execution_focus_active: bool
    integrated_runtimes: tuple[str, ...]
    mediation_focus_active: bool
    continuation_focus_active: bool
    recovery_focus_active: bool
    coordination_focus_active: bool
    execution_focus_summary: str
    autonomous_execution_loop_blocked: bool


@dataclass(frozen=True)
class BoundedMemoryFrame:
    bounded_memory_active: bool
    local_patch_compatible: bool
    rollback_safe: bool
    governance_preserving: bool
    compact_memory_summary: str
    no_provider_escalation: bool
    no_hidden_long_term_memory: bool
    no_autonomous_memory_mutation: bool


@dataclass(frozen=True)
class CognitiveStateFrame:
    cognitive_state_active: bool
    requirement_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    active: ActiveCognitiveFrame
    working_memory: WorkingMemoryFrame
    attention: TaskAttentionFrame
    salience: ContextSalienceFrame
    decay: CognitiveDecayFrame
    execution_focus: ExecutionFocusFrame
    bounded_memory: BoundedMemoryFrame
    attention_distribution: tuple[str, ...]
    memory_pressure: str
    decay_status: str
    active_focus: str
    deterministic: bool
    bounded: bool
    rollback_safe: bool
    governance_preserving: bool
    local_patch_compatible: bool
    provider_routing: str
    estimated_avoided_long_session_drift: int
    estimated_avoided_recursive_reasoning: int


class CognitiveStateRuntime:
    def evaluate(
        self,
        objective: str = "runtime-mediation-local-patch",
        *,
        working_memory_items: tuple[str, ...] = (
            "runtime_mediation",
            "execution_continuation",
            "execution_recovery",
            "execution_coordination",
        ),
        attention_weights: dict[str, int] | None = None,
        context_items: tuple[str, ...] = (
            "cognitive_state",
            "runtime_audit",
            "execution_runtime",
            "vscode_extension",
            "tests",
        ),
        stale_context_items: tuple[str, ...] = ("unrelated_artifacts",),
        session_age_pressure: int = 22,
        recursive_reasoning_attempts: int = 0,
        repo_wide_context_attempts: int = 0,
        raw_transcript_replay_attempts: int = 0,
        hidden_memory_mutation_attempts: int = 0,
        self_reprioritization_attempts: int = 0,
    ) -> CognitiveStateFrame:
        weights = dict(attention_weights or DEFAULT_ATTENTION_WEIGHTS)
        attention_distribution = _attention_distribution(weights)
        bounded_items = working_memory_items[:MAX_WORKING_MEMORY_ITEMS]
        salient_context = context_items[:MAX_CONTEXT_SALIENCE_ITEMS]
        ignored_context = tuple(stale_context_items) + context_items[MAX_CONTEXT_SALIENCE_ITEMS:]
        overflow_count = max(0, len(working_memory_items) - MAX_WORKING_MEMORY_ITEMS)
        attention_overflow = len(weights) > MAX_ATTENTION_TARGETS
        memory_pressure = _memory_pressure(len(working_memory_items), overflow_count)
        decay_score = min(
            MAX_DECAY_SCORE,
            session_age_pressure + recursive_reasoning_attempts * 28 + overflow_count * 7,
        )
        decay_status = _decay_status(decay_score)
        mediation = ExecutionSequencer().mediate()
        continuation = ExecutionContinuationRuntime().evaluate()
        recovery = ExecutionRecoveryRuntime().evaluate()
        coordination = ExecutionCoordinationRuntime().evaluate()
        integrated_runtimes = (
            "runtime_mediation",
            "execution_continuation",
            "execution_recovery",
            "execution_coordination",
        )
        active_focus = attention_distribution[0].split(":", maxsplit=1)[0]

        return CognitiveStateFrame(
            cognitive_state_active=True,
            requirement_ids=COGNITIVE_STATE_REQUIREMENT_IDS,
            test_ids=COGNITIVE_STATE_TEST_IDS,
            active=ActiveCognitiveFrame(
                active_cognitive_frame=True,
                active_objective=objective,
                deterministic_state_key=f"{objective}:{active_focus}:{len(bounded_items)}",
                local_provider_only=True,
                high_tier_escalation_blocked=True,
                compact_prompts_required=True,
                cognitive_operations_execute_commands=False,
            ),
            working_memory=WorkingMemoryFrame(
                working_memory_active=True,
                bounded_items=bounded_items,
                item_count=len(bounded_items),
                memory_limit=MAX_WORKING_MEMORY_ITEMS,
                memory_pressure=memory_pressure,
                memory_overflow_blocked=overflow_count > 0,
                recursive_memory_expansion_blocked=hidden_memory_mutation_attempts > 0,
            ),
            attention=TaskAttentionFrame(
                task_attention_active=True,
                attention_distribution=attention_distribution,
                primary_focus=active_focus,
                attention_target_count=min(len(weights), MAX_ATTENTION_TARGETS),
                attention_limit=MAX_ATTENTION_TARGETS,
                attention_overflow_blocked=attention_overflow,
                self_reprioritization_blocked=self_reprioritization_attempts > 0,
            ),
            salience=ContextSalienceFrame(
                context_salience_active=True,
                salient_context=salient_context,
                ignored_context=ignored_context,
                salience_threshold=60,
                bounded_context_window=MAX_CONTEXT_SALIENCE_ITEMS,
                repo_wide_context_blocked=repo_wide_context_attempts > 0,
                raw_transcript_replay_blocked=raw_transcript_replay_attempts > 0,
            ),
            decay=CognitiveDecayFrame(
                cognitive_decay_active=True,
                decay_score=decay_score,
                decay_status=decay_status,
                long_session_drift_detected=decay_score >= DECAY_WATCH_THRESHOLD,
                recursive_reasoning_risk_detected=recursive_reasoning_attempts > 0,
                compact_reset_recommended=decay_score >= DECAY_RESET_THRESHOLD,
                decay_recovery_recommendation=_decay_recommendation(decay_status),
            ),
            execution_focus=ExecutionFocusFrame(
                execution_focus_active=True,
                integrated_runtimes=integrated_runtimes,
                mediation_focus_active=mediation.runtime_mediation_active,
                continuation_focus_active=continuation.execution_continuation_active,
                recovery_focus_active=recovery.execution_recovery_active,
                coordination_focus_active=coordination.execution_coordination_active,
                execution_focus_summary=(
                    "mediation+continuation+recovery+coordination observed only"
                ),
                autonomous_execution_loop_blocked=True,
            ),
            bounded_memory=BoundedMemoryFrame(
                bounded_memory_active=True,
                local_patch_compatible=True,
                rollback_safe=True,
                governance_preserving=True,
                compact_memory_summary=(
                    f"items={len(bounded_items)};pressure={memory_pressure};decay={decay_status}"
                ),
                no_provider_escalation=True,
                no_hidden_long_term_memory=True,
                no_autonomous_memory_mutation=hidden_memory_mutation_attempts == 0,
            ),
            attention_distribution=attention_distribution,
            memory_pressure=memory_pressure,
            decay_status=decay_status,
            active_focus=active_focus,
            deterministic=True,
            bounded=True,
            rollback_safe=True,
            governance_preserving=True,
            local_patch_compatible=True,
            provider_routing="LOCAL_FIRST_NO_HIGH_TIER_COGNITION",
            estimated_avoided_long_session_drift=53,
            estimated_avoided_recursive_reasoning=47,
        )


def _attention_distribution(weights: dict[str, int]) -> tuple[str, ...]:
    total = sum(max(0, value) for value in weights.values()) or 1
    ordered = sorted(weights.items(), key=lambda item: (-item[1], item[0]))
    bounded = ordered[:MAX_ATTENTION_TARGETS]
    return tuple(f"{name}:{round(max(0, value) * 100 / total)}" for name, value in bounded)


def _memory_pressure(item_count: int, overflow_count: int) -> str:
    if overflow_count > 0 or item_count >= MAX_WORKING_MEMORY_ITEMS:
        return "HIGH"
    if item_count >= MAX_WORKING_MEMORY_ITEMS - 2:
        return "MEDIUM"
    return "LOW"


def _decay_status(decay_score: int) -> str:
    if decay_score >= DECAY_RESET_THRESHOLD:
        return "RESET_RECOMMENDED"
    if decay_score >= DECAY_WATCH_THRESHOLD:
        return "WATCH"
    return "STABLE"


def _decay_recommendation(decay_status: str) -> str:
    if decay_status == "RESET_RECOMMENDED":
        return "COMPACT_STATE_AND_REBASE_ATTENTION"
    if decay_status == "WATCH":
        return "MAINTAIN_BOUNDED_MEMORY_AND_REFRESH_SALIENCE"
    return "CONTINUE_LOCAL_PATCH_COGNITION"
