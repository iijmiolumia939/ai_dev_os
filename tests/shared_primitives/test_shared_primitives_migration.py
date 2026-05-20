from __future__ import annotations

import inspect

from ai_dev_os.context_subset.stale_topic_eviction import StaleTopicEvictionPolicy
from ai_dev_os.governance_health.pressure_aggregation import GovernancePressurePolicy
from ai_dev_os.governance_trends.trend_window import (
    GovernanceTrendSnapshot,
    GovernanceTrendWindowPolicy,
)
from ai_dev_os.persistence_governance.retention_policy import RetentionPolicy
from ai_dev_os.runtime_graph import RuntimeGraphPolicy
from ai_dev_os.runtime_simplification import RuntimeSimplificationPolicy
from ai_dev_os.session_lifecycle.continuity_bundle import (
    ContinuityBundlePolicy,
    ContinuityBundleSource,
)
from ai_dev_os.session_lifecycle.stale_context_detection import (
    ContextSignal,
    StaleContextDetectionPolicy,
)
from ai_dev_os.session_orchestrator.continuity_export import ContinuityExportPolicy
from ai_dev_os.workspace_persistence.persistence_cleanup import PersistenceCleanupPolicy


def test_governance_health_pressure_reuses_shared_primitive_contract() -> None:
    frame = GovernancePressurePolicy().aggregate(
        retrieval_pressure="medium",
        persistence_pressure="high",
        session_pressure="medium",
        architecture_pressure="low",
        provider_pressure="low",
        continuity_pressure="high",
        checkpoint_pressure="high",
        stale_context_pressure="medium",
        previous_pressure="low",
    )

    assert frame.aggregate_pressure in {"medium", "high"}
    assert frame.pressure_direction == "rising"
    assert frame.bounded_operation_recommended is (
        frame.aggregate_pressure in {"high", "critical"}
    )
    assert "stale_context:medium" in frame.pressure_trend


def test_bounded_retention_reuse_keeps_oldest_first_eviction() -> None:
    trend = GovernanceTrendWindowPolicy().apply(
        tuple(
            GovernanceTrendSnapshot(f"s-{i}", "medium", "low", "HEALTHY", "stable", 90)
            for i in range(6)
        ),
        max_window_size=3,
    )
    retention = RetentionPolicy().apply(
        checkpoint_generations=tuple(f"checkpoint-{i}" for i in range(6)),
        continuity_lineage=(),
        max_checkpoint_generations=3,
    )

    assert trend.evicted_snapshots == ("s-0", "s-1", "s-2")
    assert tuple(item.snapshot_id for item in trend.snapshots) == ("s-3", "s-4", "s-5")
    assert retention.expired_entries == ("checkpoint-0", "checkpoint-1", "checkpoint-2")
    assert retention.retained_entries == ("checkpoint-3", "checkpoint-4", "checkpoint-5")


def test_stale_and_continuity_reuse_stays_summary_only() -> None:
    stale = StaleContextDetectionPolicy().evaluate(
        (
            ContextSignal("stale-1", 800, "stale_continuity", 0.2, age_days=30),
            ContextSignal("active-1", 200, "active sprint", 0.9),
        )
    )
    bundle = ContinuityBundlePolicy(token_budget=200).build(
        ContinuityBundleSource(
            active_fr_tc=("TC-GOV-CORE-01",),
            current_sprint_summary="summary " * 80,
            affected_runtimes=("governance_core",),
            active_risks=("runtime fragmentation",),
            current_roadmap=("a", "b", "c", "d"),
            current_architectural_constraints=("summary only",),
            current_governance_state={"core": "active"},
        ),
        summary_only=True,
    )
    export = ContinuityExportPolicy().export(
        active_requirements=("FR-GOV-CORE",),
        active_tests=("TC-GOV-CORE-01",),
        current_sprint_boundary="shared primitives only",
        affected_runtimes=("governance_core",),
        current_architecture_constraints=("no rewrite",),
        active_risks=("duplication drift",),
        next_prompt_seed="continue bounded migration",
    )

    assert stale.stale_context_detected is True
    assert stale.recommended_bundle_refresh is True
    assert bundle.summary_only is True
    assert bundle.excluded_context == ()
    assert export.estimated_tokens > 0
    assert "Continuity Bundle" in export.copy_ready_text


def test_runtime_graph_and_simplification_reuse_remain_recommendation_only() -> None:
    graph = RuntimeGraphPolicy().evaluate(".", max_edges=24)
    simplification = RuntimeSimplificationPolicy().evaluate(".")

    assert graph.architecture_pressure.bounded_architecture_maintained is True
    assert graph.architecture_pressure.dominant_architecture_pressure
    assert simplification.recommendations.summary_only is True
    assert simplification.recommendations.human_confirmed_only is True
    assert simplification.autonomous_mutation_used is False


def test_workspace_and_context_subset_reuse_shared_stale_detection() -> None:
    cleanup = PersistenceCleanupPolicy().cleanup(
        entries=("active-note", "stale_persistence-note", "duplicate-old"),
        active_entries=("active-note",),
    )
    eviction = StaleTopicEvictionPolicy().evict(
        ("active roadmap", "stale retrieval summary", "duplicate continuity note")
    )

    assert "stale_persistence-note" in cleanup.cleaned_entries
    assert cleanup.stale_persistence_detected is True
    assert "stale retrieval summary" in eviction.evicted_topics
    assert "duplicate continuity note" in eviction.evicted_topics
    assert eviction.deterministic is True


def test_diff_only_migration_imports_shared_primitives_without_mutation() -> None:
    import ai_dev_os.context_subset.stale_topic_eviction as stale_topics
    import ai_dev_os.governance_health.pressure_aggregation as pressure
    import ai_dev_os.governance_trends.trend_window as trends
    import ai_dev_os.persistence_governance.retention_policy as retention
    import ai_dev_os.runtime_graph.architecture_pressure as runtime_pressure
    import ai_dev_os.runtime_simplification.simplification_recommendations as recommendations
    import ai_dev_os.session_lifecycle.continuity_bundle as bundle
    import ai_dev_os.session_lifecycle.stale_context_detection as stale_context
    import ai_dev_os.session_orchestrator.continuity_export as export
    import ai_dev_os.workspace_persistence.persistence_cleanup as cleanup

    modules = (
        pressure,
        trends,
        retention,
        stale_context,
        bundle,
        export,
        cleanup,
        stale_topics,
        runtime_pressure,
        recommendations,
    )
    source = "\n".join(inspect.getsource(module) for module in modules)

    assert source.count("ai_dev_os.governance_core") >= 8
    lowered = source.lower()
    assert "write_text" not in lowered
    assert "unlink(" not in lowered
    assert "rename(" not in lowered
    assert "git commit" not in lowered
    assert "git push" not in lowered
