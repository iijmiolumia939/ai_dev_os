from __future__ import annotations

from ai_dev_os.context_subset.continuity_scope import ContinuityScopePolicy
from ai_dev_os.context_subset.repository_subset import RepositorySubsetPolicy
from ai_dev_os.context_subset.session_focus import SessionFocusPolicy
from ai_dev_os.context_subset.stale_topic_eviction import StaleTopicEvictionPolicy
from ai_dev_os.context_subset.topic_isolation import TopicIsolationPolicy
from ai_dev_os.repository_intelligence.runtime_discovery import RuntimeDiscoveryFrame
from ai_dev_os.repository_intelligence.sprint_metadata import SprintMetadataFrame
from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotFrame
from ai_dev_os.workspace_snapshot.multi_repository import MultiRepositoryFrame
from ai_dev_os.workspace_snapshot.workspace_state import WorkspaceStateFrame


def _workspace_state() -> WorkspaceStateFrame:
    return WorkspaceStateFrame(
        active_repositories=("ai_dev_os", "consumer_app", "stale_tool", "isolated_tool"),
        current_sprint="TC-CONTEXTSUBSET-01",
        modified_repositories=("ai_dev_os", "consumer_app"),
        dirty_runtime_counts={"ai_dev_os": 3, "consumer_app": 1},
        dirty_governance_counts={"ai_dev_os": 1, "consumer_app": 0},
        dirty_adapter_counts={"ai_dev_os": 1, "consumer_app": 0},
        untracked_artifact_counts={"ai_dev_os": 0, "consumer_app": 0},
        architecture_review_pending=True,
        rollout_state="active",
        continuity_state="bounded",
        bounded_summary=("repositories=4", "modified=2"),
        read_only=True,
    )


def _multi_repository() -> MultiRepositoryFrame:
    return MultiRepositoryFrame(
        repository_relationships=("ai_dev_os: platform", "ai_dev_os -> consumer_app: consumer"),
        ai_dev_os_consumer_repos=("consumer_app",),
        isolated_repos=("isolated_tool",),
        stale_repos=("stale_tool",),
        migration_state={"ai_dev_os": "platform", "consumer_app": "consumer-linked"},
        adapter_compatibility_state={"ai_dev_os": "source", "consumer_app": "adapter-aware"},
        governance_compatibility={"ai_dev_os": "source", "consumer_app": "compatible"},
        repository_dependency_graph_summary=("nodes=4", "consumer_edges=1"),
        bounded=True,
        read_only=True,
    )


def _sprint_metadata() -> SprintMetadataFrame:
    return SprintMetadataFrame(
        sprint_id="42",
        active_fr_tc=("FR-CONTEXTSUBSET-01", "TC-CONTEXTSUBSET-01"),
        affected_runtimes=("context_subset", "workspace_snapshot"),
        roadmap_stage="context subset orchestration",
        active_risks=("context expansion",),
        architecture_flags=("summary-only",),
        continuity_state="bounded",
        validation_status="pending",
        schema_supported=True,
    )


def _hotspots(severity: str = "high") -> ArchitectureHotspotFrame:
    return ArchitectureHotspotFrame(
        broad_runtime_modifications=True,
        cross_boundary_modifications=True,
        giant_runtime_growth=False,
        governance_leakage_risk=True,
        renderer_authority_risk=False,
        provider_lock_in_risk=True,
        adapter_contamination_risk=True,
        experimental_runtime_spread=False,
        risk_severity=severity,
        review_recommendation="architecture_review_required",
        isolation_recommendation="same_session_ok",
        hotspot_summary=("severity=high",),
        read_only=True,
    )


def _runtime_discovery() -> RuntimeDiscoveryFrame:
    return RuntimeDiscoveryFrame(
        runtime_packages=("ai_dev_os/context_subset", "ai_dev_os/workspace_snapshot"),
        test_packages=("tests/context_subset",),
        governance_runtimes=("ai_dev_os/context_subset",),
        adapter_runtimes=(),
        renderer_runtimes=(),
        experimental_runtimes=(),
        stale_runtimes=(),
        runtime_relationship_summary=("runtime_packages=2",),
    )


def test_repository_subset_deterministic() -> None:
    policy = RepositorySubsetPolicy()
    kwargs = {
        "workspace_state": _workspace_state(),
        "multi_repository": _multi_repository(),
        "sprint_metadata": _sprint_metadata(),
        "architecture_hotspots": _hotspots(),
        "runtime_discovery": _runtime_discovery(),
    }

    first = policy.select(**kwargs)
    second = policy.select(**kwargs)

    assert first == second
    assert first.active_repositories == ("ai_dev_os", "consumer_app")
    assert "stale_tool" in first.excluded_repositories
    assert first.summary_only is True
    assert first.full_workspace_continuation_blocked is True


def test_topic_isolation_validation() -> None:
    frame = TopicIsolationPolicy().isolate(
        (
            "architecture redesign for runtime boundary",
            "provider migration discussion",
            "ci debt review",
        ),
        session_type="implementation",
        architecture_severity="high",
    )

    assert "architecture_redesign" in frame.isolated_topics
    assert "provider_migration" in frame.isolated_topics
    assert "ci_debt_review" in frame.active_topics
    assert frame.fork_session_required is True
    assert frame.architecture_session_required is True


def test_continuity_scope_bounded() -> None:
    subset = RepositorySubsetPolicy().select(
        workspace_state=_workspace_state(),
        multi_repository=_multi_repository(),
        sprint_metadata=_sprint_metadata(),
        architecture_hotspots=_hotspots(),
        runtime_discovery=_runtime_discovery(),
    )
    isolation = TopicIsolationPolicy().isolate(
        ("architecture redesign", "ci debt review"),
        architecture_severity="high",
    )
    frame = ContinuityScopePolicy().scope(
        repository_subset=subset,
        topic_isolation=isolation,
        active_tests=("TC-CONTEXTSUBSET-03",),
        rollout_required=True,
    )

    assert "repository_subset" in frame.included_context
    assert "full_workspace_continuation" in frame.excluded_context
    assert frame.continuity_budget <= 2400
    assert frame.summary_only_required is True


def test_stale_topic_eviction_validation() -> None:
    frame = StaleTopicEvictionPolicy().evict(
        (
            "old sprint review",
            "duplicate continuity",
            "active implementation context",
            "inactive governance debate",
        )
    )

    assert frame.evicted_topics == (
        "old sprint review",
        "duplicate continuity",
        "inactive governance debate",
    )
    assert frame.retained_topics == ("active implementation context",)
    assert frame.estimated_saved_tokens > 0
    assert frame.deterministic is True


def test_session_focus_validation() -> None:
    isolation = TopicIsolationPolicy().isolate(
        ("architecture redesign", "ci debt review"),
        architecture_severity="critical",
    )
    frame = SessionFocusPolicy().focus(
        requested_focus="implementation",
        topic_isolation=isolation,
        architecture_hotspots=_hotspots("critical"),
    )

    assert frame.primary_focus == "architecture"
    assert frame.escalation_required is True
    assert frame.focus_drift_risk == "critical"
    assert frame.recommended_session_type == "isolated-architecture"
