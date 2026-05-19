from __future__ import annotations

from ai_dev_os.context_subset.continuity_scope import ContinuityScopeFrame
from ai_dev_os.context_subset.repository_subset import RepositorySubsetFrame
from ai_dev_os.context_subset.session_focus import SessionFocusFrame
from ai_dev_os.context_subset.topic_isolation import TopicIsolationFrame
from ai_dev_os.prompt_modes.context_depth import ContextDepthPolicy
from ai_dev_os.prompt_modes.prompt_shape import PromptShapePolicy
from ai_dev_os.prompt_modes.reasoning_profile import ReasoningProfilePolicy
from ai_dev_os.prompt_modes.review_intensity import ReviewIntensityPolicy
from ai_dev_os.prompt_modes.session_mode_router import SessionModeRouterPolicy
from ai_dev_os.repository_intelligence.validation_collector import ValidationCollectorPolicy
from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotFrame


def _focus(primary: str = "implementation", *, escalation: bool = False) -> SessionFocusFrame:
    return SessionFocusFrame(
        primary_focus=primary,
        secondary_focus=(),
        excluded_focus=("architecture", "rollout"),
        escalation_required=escalation,
        focus_drift_risk="high" if escalation else "low",
        recommended_session_type="isolated-architecture" if escalation else f"bounded-{primary}",
    )


def _isolation(architecture: bool = False) -> TopicIsolationFrame:
    return TopicIsolationFrame(
        isolated_topics=("architecture_redesign",) if architecture else (),
        active_topics=("implementation",),
        deferred_topics=("architecture_redesign",) if architecture else (),
        fork_session_required=architecture,
        architecture_session_required=architecture,
        summary_only=True,
    )


def _continuity() -> ContinuityScopeFrame:
    return ContinuityScopeFrame(
        included_context=("active_sprint_continuity", "repository_subset"),
        excluded_context=("full_workspace_continuation", "giant_continuity_summary"),
        continuity_depth="minimal",
        continuity_budget=1300,
        summary_only_required=True,
    )


def _repository_subset() -> RepositorySubsetFrame:
    return RepositorySubsetFrame(
        active_repositories=("ai_dev_os",),
        excluded_repositories=("stale_tool",),
        stale_repositories=("stale_tool",),
        architecture_sensitive_repositories=(),
        rollout_related_repositories=("ai_dev_os",),
        continuity_priority=("repo:ai_dev_os",),
        summary_only=True,
        full_workspace_continuation_blocked=True,
    )


def _hotspots(severity: str = "low") -> ArchitectureHotspotFrame:
    return ArchitectureHotspotFrame(
        broad_runtime_modifications=False,
        cross_boundary_modifications=False,
        giant_runtime_growth=False,
        governance_leakage_risk=False,
        renderer_authority_risk=False,
        provider_lock_in_risk=False,
        adapter_contamination_risk=False,
        experimental_runtime_spread=False,
        risk_severity=severity,
        review_recommendation="bounded_review",
        isolation_recommendation="same_session_ok",
        hotspot_summary=(f"severity={severity}",),
        read_only=True,
    )


def test_reasoning_profile_routing() -> None:
    default = ReasoningProfilePolicy().profile()
    architecture = ReasoningProfilePolicy().profile(_focus(escalation=True))
    rollout = ReasoningProfilePolicy().profile(_focus("rollout"))

    assert default.mode == "bounded_implementation"
    assert default.reasoning_depth == "low"
    assert architecture.mode == "isolated_architecture"
    assert architecture.architecture_allowance == "isolated"
    assert rollout.mode == "rollout_review"


def test_prompt_shape_deterministic() -> None:
    profile = ReasoningProfilePolicy().profile(mode="bounded_implementation")
    first = PromptShapePolicy().shape(profile)
    second = PromptShapePolicy().shape(profile)

    assert first == second
    assert first.recommended_prompt_shape == "compact_patch_prompt"
    assert first.compact_mode is True
    assert first.summary_only_mode is True


def test_review_intensity_bounded() -> None:
    patch = ReviewIntensityPolicy().intensity(
        ReasoningProfilePolicy().profile(mode="bounded_implementation")
    )
    architecture = ReviewIntensityPolicy().intensity(
        ReasoningProfilePolicy().profile(mode="isolated_architecture")
    )

    assert patch.council_required is False
    assert patch.adversary_required is False
    assert architecture.council_required is True
    assert architecture.runtime_audit_required is True


def test_context_depth_bounded() -> None:
    frame = ContextDepthPolicy().depth(
        ReasoningProfilePolicy().profile(mode="retrieval_maintenance"),
        _continuity(),
    )

    assert "full_historical_continuity" in frame.excluded_depth
    assert frame.compact_required is True
    assert frame.summary_only_required is True
    assert frame.retrieval_scaling_required is True
    assert frame.continuity_budget <= 1300


def test_session_mode_routing() -> None:
    frame = SessionModeRouterPolicy().route(
        session_focus=_focus(escalation=True),
        topic_isolation=_isolation(architecture=True),
        continuity_scope=_continuity(),
        repository_subset=_repository_subset(),
        architecture_hotspots=_hotspots("critical"),
        validation=ValidationCollectorPolicy().collect(remote_ci_summary="not_checked"),
    )

    assert frame.recommended_mode == "isolated_architecture"
    assert frame.fallback_mode == "bounded_implementation"
    assert frame.compact_mode is True
    assert frame.isolation_required is True
    assert frame.recommended_prompt_type == "architecture_isolation"
