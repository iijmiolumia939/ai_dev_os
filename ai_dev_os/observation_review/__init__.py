from __future__ import annotations

from dataclasses import dataclass

MAX_OBSERVATION_RETENTION = 6
MAX_ACTION_HISTORY_RETENTION = 4
PRESSURE_WARNING_THRESHOLD = 55
PRESSURE_BLOCKER_THRESHOLD = 80
READINESS_FLOOR = 70
MAX_SCORE = 100
MIN_SCORE = 0

DEFAULT_OBSERVATION_HISTORY = (
    "provider-pressure",
    "continuation-pressure",
    "context-pressure",
    "topic-pressure",
    "session-pressure",
    "queue-saturation",
)
SUPPORTED_OBSERVATION_RISK_LEVELS = ("LOW", "MODERATE", "HIGH", "CRITICAL")
SUPPORTED_OBSERVATION_ACTIONS = (
    "NONE",
    "MONITOR",
    "THROTTLE",
    "PAUSE_REVIEW",
    "OPERATOR_ATTENTION",
)


@dataclass(frozen=True)
class PressureAggregationFrame:
    pressure_aggregation_active: bool
    provider_pressure: int
    continuation_pressure: int
    context_pressure: int
    topic_pressure: int
    session_pressure: int
    aggregate_pressure: int
    pressure_level: str
    pressure_summary: str


@dataclass(frozen=True)
class SaturationAggregationFrame:
    saturation_aggregation_active: bool
    queue_saturation: int
    retention_saturation: int
    replay_saturation: int
    lifecycle_saturation: int
    aggregate_saturation: int
    saturation_level: str
    saturation_summary: str


@dataclass(frozen=True)
class ContinuationObservationFrame:
    continuation_observation_active: bool
    continuation_pressure: int
    transition_pressure: int
    lifecycle_transition_pressure: int
    replay_suppression_activity: int
    continuation_score: int
    continuation_stability: str
    continuation_summary: str


@dataclass(frozen=True)
class ObservationEscalationRecommendation:
    escalation_policy_active: bool
    risk_level: str
    action: str
    action_summary: str
    deterministic: bool
    no_autonomous_execution: bool


@dataclass(frozen=True)
class RuntimeReadinessFrame:
    observation_review_active: bool
    pressure: PressureAggregationFrame
    saturation: SaturationAggregationFrame
    continuation: ContinuationObservationFrame
    readiness_score: int
    risk_level: str
    action: str
    merge_readiness: str
    blocker_count: int
    merge_blockers: tuple[str, ...]
    operational_warnings: tuple[str, ...]
    pressure_summary: str
    saturation_summary: str
    continuation_summary: str
    action_summary: str
    operational_risk_summary: str
    retained_observations: tuple[str, ...]
    evicted_observations: tuple[str, ...]
    retained_action_history: tuple[str, ...]
    evicted_action_history: tuple[str, ...]
    retention_limit: int
    action_retention_limit: int
    no_autonomous_execution: bool
    deterministic: bool
    bounded: bool


class MergeReadinessEvaluator:
    def evaluate(
        self,
        *,
        readiness_score: int,
        blockers: tuple[str, ...],
        warnings: tuple[str, ...],
    ) -> str:
        if blockers:
            return "BLOCKED_FOR_MAIN_MERGE"
        if readiness_score >= 85 and not warnings:
            return "READY_FOR_MAIN_MERGE"
        if readiness_score >= READINESS_FLOOR:
            return "READY_WITH_WARNINGS"
        return "CONTINUE_OBSERVATION_BEFORE_MAIN_MERGE"


class ObservationEscalationPolicy:
    _ACTION_BY_RISK = {
        "LOW": "NONE",
        "MODERATE": "MONITOR",
        "HIGH": "THROTTLE",
        "CRITICAL": "OPERATOR_ATTENTION",
    }

    def recommend(self, *, risk_level: str) -> ObservationEscalationRecommendation:
        normalized_risk = risk_level.upper()
        if normalized_risk not in SUPPORTED_OBSERVATION_RISK_LEVELS:
            raise ValueError(f"unsupported risk level: {risk_level}")
        action = self._ACTION_BY_RISK[normalized_risk]
        return ObservationEscalationRecommendation(
            escalation_policy_active=True,
            risk_level=normalized_risk,
            action=action,
            action_summary=f"risk={normalized_risk};action={action};autonomous_execution=blocked",
            deterministic=True,
            no_autonomous_execution=True,
        )


class ObservationReviewRuntime:
    def evaluate(
        self,
        *,
        provider_pressure: int = 28,
        social_interaction_pressure: int = 24,
        continuation_pressure: int = 26,
        context_pressure: int = 22,
        topic_pressure: int = 18,
        session_pressure: int = 20,
        viewer_event_saturation: int = 24,
        retention_saturation: int = 20,
        replay_suppression_activity: int = 18,
        lifecycle_transition_pressure: int = 16,
        transition_pressure: int = 14,
        observation_history: tuple[str, ...] = DEFAULT_OBSERVATION_HISTORY,
        action_history: tuple[str, ...] = (),
    ) -> RuntimeReadinessFrame:
        pressure = PressureAggregationFrame(
            pressure_aggregation_active=True,
            provider_pressure=_clamp(provider_pressure),
            continuation_pressure=_clamp(continuation_pressure),
            context_pressure=_clamp(context_pressure),
            topic_pressure=_clamp(topic_pressure),
            session_pressure=_clamp(session_pressure),
            aggregate_pressure=_clamp(
                round(
                    (
                        _clamp(provider_pressure) * 3
                        + _clamp(continuation_pressure) * 3
                        + _clamp(context_pressure) * 2
                        + _clamp(topic_pressure) * 2
                        + _clamp(session_pressure) * 2
                    )
                    / 12
                )
            ),
            pressure_level="",
            pressure_summary="",
        )
        pressure = PressureAggregationFrame(
            pressure_aggregation_active=pressure.pressure_aggregation_active,
            provider_pressure=pressure.provider_pressure,
            continuation_pressure=pressure.continuation_pressure,
            context_pressure=pressure.context_pressure,
            topic_pressure=pressure.topic_pressure,
            session_pressure=pressure.session_pressure,
            aggregate_pressure=pressure.aggregate_pressure,
            pressure_level=_level_for_value(pressure.aggregate_pressure),
            pressure_summary=(
                f"provider={pressure.provider_pressure};"
                f"continuation={pressure.continuation_pressure};"
                f"context={pressure.context_pressure};"
                f"topic={pressure.topic_pressure};"
                f"session={pressure.session_pressure};"
                f"aggregate={pressure.aggregate_pressure};"
                f"level={_level_for_value(pressure.aggregate_pressure)}"
            ),
        )

        saturation = SaturationAggregationFrame(
            saturation_aggregation_active=True,
            queue_saturation=_clamp(viewer_event_saturation),
            retention_saturation=_clamp(retention_saturation),
            replay_saturation=_clamp(replay_suppression_activity),
            lifecycle_saturation=_clamp(lifecycle_transition_pressure),
            aggregate_saturation=_clamp(
                round(
                    (
                        _clamp(viewer_event_saturation) * 3
                        + _clamp(retention_saturation) * 3
                        + _clamp(replay_suppression_activity) * 2
                        + _clamp(lifecycle_transition_pressure) * 2
                    )
                    / 10
                )
            ),
            saturation_level="",
            saturation_summary="",
        )
        saturation = SaturationAggregationFrame(
            saturation_aggregation_active=saturation.saturation_aggregation_active,
            queue_saturation=saturation.queue_saturation,
            retention_saturation=saturation.retention_saturation,
            replay_saturation=saturation.replay_saturation,
            lifecycle_saturation=saturation.lifecycle_saturation,
            aggregate_saturation=saturation.aggregate_saturation,
            saturation_level=_level_for_value(saturation.aggregate_saturation),
            saturation_summary=(
                f"queue={saturation.queue_saturation};"
                f"retention={saturation.retention_saturation};"
                f"replay={saturation.replay_saturation};"
                f"lifecycle={saturation.lifecycle_saturation};"
                f"aggregate={saturation.aggregate_saturation};"
                f"level={_level_for_value(saturation.aggregate_saturation)}"
            ),
        )

        continuation_score = _clamp(
            100
            - round(
                (
                    _clamp(continuation_pressure) * 4
                    + _clamp(transition_pressure) * 3
                    + _clamp(lifecycle_transition_pressure) * 3
                    + _clamp(replay_suppression_activity) * 2
                )
                / 12
            )
        )
        continuation = ContinuationObservationFrame(
            continuation_observation_active=True,
            continuation_pressure=_clamp(continuation_pressure),
            transition_pressure=_clamp(transition_pressure),
            lifecycle_transition_pressure=_clamp(lifecycle_transition_pressure),
            replay_suppression_activity=_clamp(replay_suppression_activity),
            continuation_score=continuation_score,
            continuation_stability=_continuation_stability_label(continuation_score),
            continuation_summary=(
                f"continuation={_clamp(continuation_pressure)};"
                f"transition={_clamp(transition_pressure)};"
                f"lifecycle={_clamp(lifecycle_transition_pressure)};"
                f"replay={_clamp(replay_suppression_activity)};"
                f"score={continuation_score};"
                f"stability={_continuation_stability_label(continuation_score)}"
            ),
        )

        retained_observations = observation_history[-MAX_OBSERVATION_RETENTION:]
        evicted_observations = observation_history[:-MAX_OBSERVATION_RETENTION]

        metric_blockers = _collect_blockers(
            pressure=pressure,
            saturation=saturation,
            continuation=continuation,
        )
        warnings = _collect_warnings(
            pressure=pressure,
            saturation=saturation,
            continuation=continuation,
            social_interaction_pressure=_clamp(social_interaction_pressure),
            transition_pressure=_clamp(transition_pressure),
        )
        base_score = _clamp(
            round(
                (MAX_SCORE - pressure.aggregate_pressure) * 0.4
                + (MAX_SCORE - saturation.aggregate_saturation) * 0.35
                + continuation.continuation_score * 0.25
            )
        )
        readiness_score = _clamp(base_score - len(metric_blockers) * 6 - len(warnings) * 2)
        blockers = metric_blockers + (
            ("READINESS_SCORE_BELOW_THRESHOLD",) if readiness_score < READINESS_FLOOR else ()
        )
        risk_level = _operational_risk_level(
            readiness_score=readiness_score,
            blocker_count=len(blockers),
            warning_count=len(warnings),
        )
        escalation = ObservationEscalationPolicy().recommend(risk_level=risk_level)
        combined_action_history = action_history + (escalation.action,)
        retained_action_history = combined_action_history[-MAX_ACTION_HISTORY_RETENTION:]
        evicted_action_history = combined_action_history[:-MAX_ACTION_HISTORY_RETENTION]
        merge_readiness = MergeReadinessEvaluator().evaluate(
            readiness_score=readiness_score,
            blockers=blockers,
            warnings=warnings,
        )
        operational_risk_summary = _operational_risk_summary(
            risk_level=risk_level,
            readiness_score=readiness_score,
            blocker_count=len(blockers),
            warning_count=len(warnings),
            social_interaction_pressure=_clamp(social_interaction_pressure),
            action=escalation.action,
        )
        return RuntimeReadinessFrame(
            observation_review_active=True,
            pressure=pressure,
            saturation=saturation,
            continuation=continuation,
            readiness_score=readiness_score,
            risk_level=risk_level,
            action=escalation.action,
            merge_readiness=merge_readiness,
            blocker_count=len(blockers),
            merge_blockers=blockers,
            operational_warnings=warnings,
            pressure_summary=pressure.pressure_summary,
            saturation_summary=saturation.saturation_summary,
            continuation_summary=continuation.continuation_summary,
            action_summary=escalation.action_summary,
            operational_risk_summary=operational_risk_summary,
            retained_observations=retained_observations,
            evicted_observations=evicted_observations,
            retained_action_history=retained_action_history,
            evicted_action_history=evicted_action_history,
            retention_limit=MAX_OBSERVATION_RETENTION,
            action_retention_limit=MAX_ACTION_HISTORY_RETENTION,
            no_autonomous_execution=escalation.no_autonomous_execution,
            deterministic=True,
            bounded=(
                len(retained_observations) <= MAX_OBSERVATION_RETENTION
                and len(retained_action_history) <= MAX_ACTION_HISTORY_RETENTION
            ),
        )


def _clamp(value: int) -> int:
    return max(MIN_SCORE, min(MAX_SCORE, value))


def _level_for_value(value: int) -> str:
    if value >= PRESSURE_BLOCKER_THRESHOLD:
        return "HIGH"
    if value >= PRESSURE_WARNING_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def _continuation_stability_label(score: int) -> str:
    if score >= 80:
        return "STABLE"
    if score >= READINESS_FLOOR:
        return "GUARDED"
    return "UNSTABLE"


def _collect_blockers(
    *,
    pressure: PressureAggregationFrame,
    saturation: SaturationAggregationFrame,
    continuation: ContinuationObservationFrame,
) -> tuple[str, ...]:
    blockers: list[str] = []
    for label, value in (
        ("PROVIDER_PRESSURE_BLOCKER", pressure.provider_pressure),
        ("CONTINUATION_PRESSURE_BLOCKER", pressure.continuation_pressure),
        ("CONTEXT_PRESSURE_BLOCKER", pressure.context_pressure),
        ("TOPIC_PRESSURE_BLOCKER", pressure.topic_pressure),
        ("SESSION_PRESSURE_BLOCKER", pressure.session_pressure),
        ("QUEUE_SATURATION_BLOCKER", saturation.queue_saturation),
        ("RETENTION_SATURATION_BLOCKER", saturation.retention_saturation),
        ("REPLAY_SATURATION_BLOCKER", saturation.replay_saturation),
        ("LIFECYCLE_SATURATION_BLOCKER", saturation.lifecycle_saturation),
        ("TRANSITION_STABILITY_BLOCKER", continuation.transition_pressure),
    ):
        if value >= PRESSURE_BLOCKER_THRESHOLD:
            blockers.append(label)
    return tuple(blockers)


def _collect_warnings(
    *,
    pressure: PressureAggregationFrame,
    saturation: SaturationAggregationFrame,
    continuation: ContinuationObservationFrame,
    social_interaction_pressure: int,
    transition_pressure: int,
) -> tuple[str, ...]:
    warnings: list[str] = []
    if pressure.aggregate_pressure >= PRESSURE_WARNING_THRESHOLD:
        warnings.append("PRESSURE_ELEVATED")
    if saturation.aggregate_saturation >= PRESSURE_WARNING_THRESHOLD:
        warnings.append("SATURATION_ELEVATED")
    if continuation.continuation_score < 80:
        warnings.append("CONTINUATION_GUARDED")
    if social_interaction_pressure >= PRESSURE_WARNING_THRESHOLD:
        warnings.append("SOCIAL_INTERACTION_PRESSURE_ELEVATED")
    if transition_pressure >= PRESSURE_WARNING_THRESHOLD:
        warnings.append("TRANSITION_PRESSURE_ELEVATED")
    return tuple(warnings)


def _operational_risk_summary(
    *,
    risk_level: str,
    readiness_score: int,
    blocker_count: int,
    warning_count: int,
    social_interaction_pressure: int,
    action: str,
) -> str:
    return (
        f"risk={risk_level};"
        f"score={readiness_score};"
        f"blockers={blocker_count};"
        f"warnings={warning_count};"
        f"social={social_interaction_pressure};"
        f"action={action}"
    )


def _operational_risk_level(
    *,
    readiness_score: int,
    blocker_count: int,
    warning_count: int,
) -> str:
    if blocker_count >= 4 or readiness_score < 55:
        return "CRITICAL"
    if blocker_count or readiness_score < READINESS_FLOOR:
        return "HIGH"
    if warning_count or readiness_score < 85:
        return "MODERATE"
    return "LOW"


__all__ = [
    "ContinuationObservationFrame",
    "DEFAULT_OBSERVATION_HISTORY",
    "MAX_ACTION_HISTORY_RETENTION",
    "MAX_OBSERVATION_RETENTION",
    "MergeReadinessEvaluator",
    "ObservationEscalationPolicy",
    "ObservationEscalationRecommendation",
    "ObservationReviewRuntime",
    "PressureAggregationFrame",
    "RuntimeReadinessFrame",
    "SaturationAggregationFrame",
    "SUPPORTED_OBSERVATION_ACTIONS",
    "SUPPORTED_OBSERVATION_RISK_LEVELS",
]
