from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from ai_dev_os.context_subset.continuity_scope import ContinuityScopePolicy
from ai_dev_os.context_subset.repository_subset import RepositorySubsetPolicy
from ai_dev_os.context_subset.session_focus import SessionFocusPolicy
from ai_dev_os.context_subset.stale_topic_eviction import StaleTopicEvictionPolicy
from ai_dev_os.context_subset.topic_isolation import TopicIsolationPolicy
from ai_dev_os.prompt_modes.context_depth import ContextDepthPolicy
from ai_dev_os.prompt_modes.prompt_shape import PromptShapePolicy
from ai_dev_os.prompt_modes.reasoning_profile import ReasoningProfilePolicy
from ai_dev_os.prompt_modes.review_intensity import ReviewIntensityPolicy
from ai_dev_os.prompt_modes.session_mode_router import SessionModeRouterPolicy
from ai_dev_os.repository_intelligence.ci_context import CIContextPolicy
from ai_dev_os.repository_intelligence.git_collector import GitCollector
from ai_dev_os.repository_intelligence.runtime_discovery import RuntimeDiscoveryPolicy
from ai_dev_os.repository_intelligence.sprint_metadata import SprintMetadataPolicy
from ai_dev_os.repository_intelligence.validation_collector import ValidationCollectorPolicy
from ai_dev_os.session_boundary.boundary_enforcement import BoundaryEnforcementPolicy
from ai_dev_os.session_boundary.handoff_confirmation import HandoffConfirmationPolicy
from ai_dev_os.session_boundary.rollover_state import RolloverStatePolicy
from ai_dev_os.session_boundary.session_generation import SessionGenerationPolicy
from ai_dev_os.session_boundary.stale_session_detection import StaleSessionDetectionPolicy
from ai_dev_os.session_lifecycle.architecture_isolation import ArchitectureIsolationPolicy
from ai_dev_os.session_lifecycle.cache_aware_session import CacheAwareSessionPolicy
from ai_dev_os.session_lifecycle.session_rollover import SessionRolloverPolicy
from ai_dev_os.session_lifecycle.stale_context_detection import (
    ContextSignal,
    StaleContextDetectionPolicy,
)
from ai_dev_os.session_orchestrator.continuity_export import ContinuityExportPolicy
from ai_dev_os.session_orchestrator.prompt_pack import PromptPackPolicy
from ai_dev_os.session_orchestrator.session_decision import SessionDecisionPolicy
from ai_dev_os.session_orchestrator.sprint_close import SprintCloseInput, SprintClosePolicy
from ai_dev_os.session_orchestrator.sprint_start import SprintStartInput, SprintStartPolicy
from ai_dev_os.vscode_integration.clipboard_runtime import ClipboardRuntimePolicy
from ai_dev_os.vscode_integration.handoff_notifications import HandoffNotificationPolicy
from ai_dev_os.vscode_integration.ide_state import IDEStatePolicy
from ai_dev_os.vscode_integration.prompt_export import PromptExportPolicy
from ai_dev_os.vscode_integration.session_handoff import SessionHandoffPolicy
from ai_dev_os.workspace_persistence.continuity_index import ContinuityIndexPolicy
from ai_dev_os.workspace_persistence.persistence_cleanup import PersistenceCleanupPolicy
from ai_dev_os.workspace_persistence.persistence_store import PersistenceStorePolicy
from ai_dev_os.workspace_persistence.session_restore import SessionRestorePolicy
from ai_dev_os.workspace_persistence.state_checkpoint import StateCheckpointPolicy
from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotPolicy
from ai_dev_os.workspace_snapshot.known_failures import KnownFailurePolicy
from ai_dev_os.workspace_snapshot.multi_repository import MultiRepositoryPolicy
from ai_dev_os.workspace_snapshot.rollout_tracking import RolloutTrackingPolicy
from ai_dev_os.workspace_snapshot.workspace_state import WorkspaceStatePolicy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ai_dev_os.cli")
    parser.add_argument("command")
    parser.add_argument("--sprint", default="next")
    parser.add_argument("--project", default="project")
    parser.add_argument("--repo-path", default=".")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--from-file", default="")
    parser.add_argument("--type", default="sprint-start")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--copy-ready", action="store_true")
    args = parser.parse_args(argv)

    result = _dispatch(args)
    _print_result(result, json_mode=args.json, copy_ready=args.copy_ready)
    return 0


def _dispatch(args: argparse.Namespace) -> Any:
    command = args.command
    if command == "session-audit":
        return _session_decision(args.project)
    if command == "sprint-start":
        return _sprint_start(args.sprint, args.project)
    if command == "sprint-close":
        return _sprint_close(args.sprint, args.project)
    if command == "continuity-export":
        return _continuity_export(
            args.project, output_format="plain" if args.copy_ready else "markdown"
        )
    if command == "prompt-pack":
        return _prompt_pack(args.type.replace("-", "_"), args.project, args.sprint)
    if command == "should-rollover":
        return _rollover(args.project)
    if command == "repo-intel":
        return _repo_intel(args.repo_path)
    if command == "sprint-import":
        return _sprint_import(args.from_file)
    if command == "validation-summary":
        return _validation_summary(args.repo_path)
    if command == "runtime-map":
        return RuntimeDiscoveryPolicy().discover(args.repo_path)
    if command == "ci-context":
        return CIContextPolicy().default_local()
    if command == "workspace-snapshot":
        return _workspace_snapshot(args.workspace, args.sprint)
    if command == "rollout-status":
        return RolloutTrackingPolicy().track(args.workspace)
    if command == "known-failures":
        return KnownFailurePolicy().from_workspace(args.workspace)
    if command == "architecture-hotspots":
        return ArchitectureHotspotPolicy().detect(args.workspace)
    if command == "multi-repo-map":
        return MultiRepositoryPolicy().map(args.workspace)
    if command == "context-subset":
        return _context_subset(args.workspace, args.sprint, requested_focus="implementation")
    if command == "topic-isolation":
        return _context_subset(args.workspace, args.sprint)["topic_isolation"]
    if command == "session-focus":
        return _context_subset(args.workspace, args.sprint)["session_focus"]
    if command == "stale-topics":
        return _context_subset(args.workspace, args.sprint)["stale_topic_eviction"]
    if command == "continuity-scope":
        return _context_subset(args.workspace, args.sprint)["continuity_scope"]
    if command == "reasoning-profile":
        return _prompt_modes(args.workspace, args.sprint)["reasoning_profile"]
    if command == "prompt-shape":
        return _prompt_modes(args.workspace, args.sprint)["prompt_shape"]
    if command == "review-intensity":
        return _prompt_modes(args.workspace, args.sprint)["review_intensity"]
    if command == "context-depth":
        return _prompt_modes(args.workspace, args.sprint)["context_depth"]
    if command == "session-mode":
        return _prompt_modes(args.workspace, args.sprint)["session_mode"]
    if command == "handoff-session":
        return _vscode_handoff(args.workspace, args.sprint)
    if command == "export-prompt":
        return _vscode_prompt_export(args.workspace, args.sprint)
    if command == "copy-prompt":
        return _vscode_copy_prompt(args.workspace, args.sprint)
    if command == "session-pressure":
        return _vscode_notifications(args.workspace, args.sprint)
    if command == "vscode-state":
        return _vscode_state(args.workspace, args.sprint)
    if command == "session-generation":
        return _session_boundary(args.workspace, args.sprint)["session_generation"]
    if command == "stale-session":
        return _session_boundary(args.workspace, args.sprint)["stale_session"]
    if command == "session-boundary":
        return _session_boundary(args.workspace, args.sprint)["boundary_enforcement"]
    if command == "rollover-state":
        return _session_boundary(args.workspace, args.sprint)["rollover_state"]
    if command == "handoff-confirmation":
        return _session_boundary(args.workspace, args.sprint)["handoff_confirmation"]
    if command == "session-boundary-handoff":
        return _session_boundary_handoff(args.workspace, args.sprint)
    if command == "persistence-store":
        return _workspace_persistence(args.workspace, args.sprint)["persistence_store"]
    if command == "restore-session-state":
        return _workspace_persistence(args.workspace, args.sprint)["session_restore"]
    if command == "state-checkpoint":
        return _workspace_persistence(args.workspace, args.sprint)["state_checkpoint"]
    if command == "continuity-index":
        return _workspace_persistence(args.workspace, args.sprint)["continuity_index"]
    if command == "cleanup-persistence":
        return _workspace_persistence(args.workspace, args.sprint)["persistence_cleanup"]
    raise SystemExit(f"unsupported command: {command}")


def _sprint_start(sprint: str, project: str):
    metadata = SprintMetadataPolicy().default(sprint_id=sprint, project_name=project)
    discovery = RuntimeDiscoveryPolicy().discover(".")
    workspace = _workspace_snapshot(".", sprint)
    subset = _context_subset(".", sprint)
    rollout = workspace["rollout_tracking"]
    hotspots = workspace["architecture_hotspots"]
    affected = metadata.affected_runtimes or discovery.runtime_packages[:3]
    handoff = _vscode_handoff(".", sprint)
    return SprintStartPolicy().build(
        SprintStartInput(
            sprint_id=sprint,
            project_name=project,
            active_fr_tc=("FR-SESSION-CLI-01", "TC-SESSION-CLI-01"),
            affected_runtimes=affected,
            previous_sprint_summary=(
                "Workspace snapshot collected: "
                + "; ".join(workspace["workspace_state"].bounded_summary)
                + f"; handoff={handoff.handoff_summary}"
            ),
            active_risks=metadata.active_risks
            + hotspots.hotspot_summary
            + (subset["session_focus"].focus_drift_risk,),
            current_roadmap=(metadata.roadmap_stage, rollout.rollout_stage),
            architecture_flags=metadata.architecture_flags
            + (
                hotspots.review_recommendation,
                hotspots.isolation_recommendation,
                subset["session_focus"].recommended_session_type,
            ),
        )
    )


def _sprint_close(sprint: str, project: str):
    git = GitCollector().collect(".")
    workspace = _workspace_snapshot(".", sprint)
    subset = _context_subset(".", sprint)
    handoff = _vscode_handoff(".", sprint)
    validation = ValidationCollectorPolicy().collect(
        pytest_summary="local pytest status unknown",
        scoped_pytest=("repository intelligence scoped tests pending",),
        ruff_status="unknown",
        black_status="unknown",
        diff_check="unknown",
        remote_ci_summary="unknown",
    )
    status = (
        "clean"
        if git.modified_file_count == 0 and git.untracked_file_count == 0 and git.ahead == 0
        else (
            f"modified {git.modified_file_count}; "
            f"untracked {git.untracked_file_count}; ahead {git.ahead}"
        )
    )
    return SprintClosePolicy().close(
        SprintCloseInput(
            validation_summary=(
                f"Sprint {sprint} for {project}: {validation.remote_ci_summary}; "
                f"workspace={workspace['workspace_state'].continuity_state}; "
                f"handoff={handoff.recommended_new_session}"
            ),
            git_status_summary=status,
            changed_paths=git.changed_runtime_paths + git.changed_test_paths,
            test_results=validation.scoped_pytest,
            remaining_risks=(
                "remote verification required",
                *workspace["known_failures"].baseline_failures,
                workspace["architecture_hotspots"].risk_severity,
                subset["session_focus"].focus_drift_risk,
            ),
            next_roadmap=(
                "release governance",
                workspace["rollout_tracking"].rollout_stage,
                subset["session_focus"].recommended_session_type,
            ),
        )
    )


def _prompt_pack(prompt_type: str, project: str, sprint: str):
    workspace = _workspace_snapshot(".", sprint)
    subset = _context_subset(".", sprint)
    modes = _prompt_modes(".", sprint)
    prompt_shape = modes["prompt_shape"]
    context_depth = modes["context_depth"]
    review = modes["review_intensity"]
    session_mode = modes["session_mode"]
    return PromptPackPolicy().build(
        prompt_type=prompt_type or session_mode.recommended_prompt_type,
        project_name=project,
        sprint_id=sprint,
        objective="automate bounded session orchestration",
        context_lines=(
            "Use compact continuity bundle only.",
            "Do not replay full sprint history.",
            "Return validation and remote verification summary.",
            "Workspace: " + "; ".join(workspace["workspace_state"].bounded_summary),
            "Rollout: " + workspace["rollout_tracking"].rollout_stage,
            "Architecture: " + workspace["architecture_hotspots"].risk_severity,
            "Repository subset: " + ", ".join(subset["repository_subset"].active_repositories),
            "Session focus: " + subset["session_focus"].recommended_session_type,
            "Reasoning mode: " + modes["reasoning_profile"].mode,
            "VSCode handoff: human confirmed; no autonomous UI control.",
        ),
        required_context=(
            "continuity_bundle",
            "active_fr_tc",
            "workspace_snapshot",
            "context_subset",
        ),
        excluded_context=(
            "full_history",
            "generated_artifacts",
            *subset["continuity_scope"].excluded_context,
            *context_depth.excluded_depth,
        ),
        affected_runtimes=("session_orchestrator",),
        prompt_shape=prompt_shape.recommended_prompt_shape,
        continuity_depth=context_depth.included_depth[-1],
        review_checklist=review.required_review_domains,
        architecture_allowance=modes["reasoning_profile"].architecture_allowance,
        retrieval_budget=modes["reasoning_profile"].retrieval_budget,
        plain_text=True,
    )


def _continuity_export(project: str, *, output_format: str):
    metadata = SprintMetadataPolicy().default(project_name=project)
    discovery = RuntimeDiscoveryPolicy().discover(".")
    workspace = _workspace_snapshot(".", "next")
    subset = _context_subset(".", "next")
    handoff = _vscode_handoff(".", "next")
    return ContinuityExportPolicy().export(
        active_requirements=tuple(
            item for item in metadata.active_fr_tc if item.startswith("FR-")
        ),
        active_tests=tuple(item for item in metadata.active_fr_tc if item.startswith("TC-")),
        current_sprint_boundary=f"{project}: next bounded session",
        affected_runtimes=metadata.affected_runtimes or discovery.runtime_packages[:3],
        current_architecture_constraints=("no UI automation", "no full history replay"),
        active_risks=(
            "manual copy step remains",
            workspace["architecture_hotspots"].risk_severity,
            subset["session_focus"].focus_drift_risk,
        ),
        next_prompt_seed=(
            "Start the next sprint from this compact bundle only. "
            "Workspace repositories: "
            f"{', '.join(workspace['workspace_state'].active_repositories)}. "
            "Active subset: "
            f"{', '.join(subset['repository_subset'].active_repositories)}. "
            f"Rollout: {workspace['rollout_tracking'].rollout_stage}."
        ),
        output_format=output_format,
        extra_context={
            "full_history": "excluded",
            "generated_artifacts": "excluded",
            "workspace_snapshot": workspace["workspace_state"].bounded_summary,
            "known_failures": workspace["known_failures"].baseline_failures,
            "repository_subset": subset["repository_subset"].active_repositories,
            "continuity_scope": subset["continuity_scope"].included_context,
            "stale_topic_eviction": subset["stale_topic_eviction"].evicted_topics,
            "vscode_handoff": handoff.handoff_summary,
        },
    )


def _rollover(project: str):
    return SessionRolloverPolicy().evaluate(
        session_age=6,
        estimated_context_tokens=28_000,
        stale_context_ratio=0.62,
        retrieval_pressure="HIGH",
        cache_reuse_probability=0.7,
        sprint_boundary=True,
        architecture_escalation=False,
    )


def _session_decision(project: str):
    workspace = _workspace_snapshot(".", "next")
    subset = _context_subset(".", "next")
    _vscode_handoff(".", "next")
    rollover = _rollover(project)
    stale = StaleContextDetectionPolicy().evaluate(
        (
            ContextSignal("old-sprint", 12_000, "old sprint", 0.2, age_days=40),
            ContextSignal("active-cli", 800, "active runtime", 0.95),
        )
    )
    cache = CacheAwareSessionPolicy().evaluate(
        cache_reuse_probability=0.7,
        repeated_instruction_stability=0.8,
        context_freshness=0.35,
        retrieval_overlap=0.25,
        prompt_compactness=0.8,
        pressure="HIGH",
    )
    hotspot_severity = workspace["architecture_hotspots"].risk_severity
    architecture_prompt = (
        "architecture redesign for workspace snapshot"
        if hotspot_severity in {"high", "critical"}
        or subset["topic_isolation"].architecture_session_required
        else "routine sprint session"
    )
    architecture = ArchitectureIsolationPolicy().evaluate(
        architecture_prompt,
        affected_runtimes=("session_orchestrator", "workspace_snapshot"),
    )
    return SessionDecisionPolicy().decide(
        rollover=rollover,
        stale=stale,
        cache=cache,
        architecture=architecture,
    )


def _repo_intel(repo_path: str):
    return {
        "git": GitCollector().collect(repo_path),
        "runtime_discovery": RuntimeDiscoveryPolicy().discover(repo_path),
        "validation": _validation_summary(repo_path),
        "ci_context": CIContextPolicy().default_local(),
    }


def _workspace_snapshot(workspace: str, sprint: str):
    state = WorkspaceStatePolicy().snapshot(workspace, current_sprint=sprint)
    return {
        "workspace_state": state,
        "multi_repository": MultiRepositoryPolicy().map(workspace),
        "rollout_tracking": RolloutTrackingPolicy().track(workspace),
        "known_failures": KnownFailurePolicy().from_workspace(workspace),
        "architecture_hotspots": ArchitectureHotspotPolicy().detect(workspace, state=state),
    }


def _context_subset(
    workspace: str,
    sprint: str,
    *,
    requested_focus: str = "implementation",
):
    workspace_frame = _workspace_snapshot(workspace, sprint)
    sprint_metadata = SprintMetadataPolicy().default(sprint_id=sprint, project_name="workspace")
    runtime_discovery = RuntimeDiscoveryPolicy().discover(workspace)
    repository_subset = RepositorySubsetPolicy().select(
        workspace_state=workspace_frame["workspace_state"],
        multi_repository=workspace_frame["multi_repository"],
        sprint_metadata=sprint_metadata,
        architecture_hotspots=workspace_frame["architecture_hotspots"],
        runtime_discovery=runtime_discovery,
    )
    topics = (
        sprint_metadata.roadmap_stage,
        workspace_frame["rollout_tracking"].rollout_stage,
        workspace_frame["architecture_hotspots"].review_recommendation,
        *workspace_frame["known_failures"].baseline_failures,
        "old sprint review",
        "duplicate continuity",
    )
    stale = StaleTopicEvictionPolicy().evict(topics)
    topic_isolation = TopicIsolationPolicy().isolate(
        stale.retained_topics,
        session_type=requested_focus,
        architecture_severity=workspace_frame["architecture_hotspots"].risk_severity,
    )
    continuity_scope = ContinuityScopePolicy().scope(
        repository_subset=repository_subset,
        topic_isolation=topic_isolation,
        active_tests=sprint_metadata.active_fr_tc,
        rollout_required=bool(repository_subset.rollout_related_repositories),
    )
    session_focus = SessionFocusPolicy().focus(
        requested_focus=requested_focus,
        topic_isolation=topic_isolation,
        architecture_hotspots=workspace_frame["architecture_hotspots"],
    )
    return {
        "repository_subset": repository_subset,
        "topic_isolation": topic_isolation,
        "continuity_scope": continuity_scope,
        "stale_topic_eviction": stale,
        "session_focus": session_focus,
    }


def _prompt_modes(workspace: str, sprint: str):
    subset = _context_subset(workspace, sprint)
    validation = ValidationCollectorPolicy().collect(remote_ci_summary="not_checked")
    session_mode = SessionModeRouterPolicy().route(
        session_focus=subset["session_focus"],
        topic_isolation=subset["topic_isolation"],
        continuity_scope=subset["continuity_scope"],
        repository_subset=subset["repository_subset"],
        architecture_hotspots=_workspace_snapshot(workspace, sprint)["architecture_hotspots"],
        validation=validation,
    )
    profile = ReasoningProfilePolicy().profile(
        subset["session_focus"], mode=session_mode.recommended_mode
    )
    shape = PromptShapePolicy().shape(profile)
    review = ReviewIntensityPolicy().intensity(profile)
    depth = ContextDepthPolicy().depth(profile, subset["continuity_scope"])
    return {
        "session_mode": session_mode,
        "reasoning_profile": profile,
        "prompt_shape": shape,
        "review_intensity": review,
        "context_depth": depth,
    }


def _vscode_handoff(workspace: str, sprint: str):
    subset = _context_subset(workspace, sprint)
    modes = _prompt_modes(workspace, sprint)
    prompt_pack = _prompt_pack_for_handoff(workspace, sprint)
    rollover = _rollover("workspace")
    stale_detected = subset["stale_topic_eviction"].estimated_saved_tokens > 0
    return SessionHandoffPolicy().build(
        rollover_required=rollover.rollover_recommended,
        stale_context_detected=stale_detected,
        session_mode=modes["session_mode"],
        repository_subset=subset["repository_subset"],
        session_focus=subset["session_focus"],
        continuity_scope=subset["continuity_scope"],
        prompt_text=prompt_pack.copy_ready_text,
    )


def _session_boundary(workspace: str, sprint: str):
    handoff = _vscode_handoff(workspace, sprint)
    modes = _prompt_modes(workspace, sprint)
    generation = SessionGenerationPolicy().generate(
        session_id=f"{Path(workspace).resolve().name}:{sprint}",
        session_generation=1,
        rollover_recommended=handoff.recommended_new_session,
        parent_session="current-human-confirmed-session",
    )
    continuity_tokens = max(12_000, len(handoff.copy_ready_prompt) // 2)
    stale = StaleSessionDetectionPolicy().detect(
        generation=generation,
        rollover_recommended=handoff.rollover_required,
        handoff_generated=True,
        new_session_started=False,
        continuity_generation=generation.continuity_generation,
        architecture_topic_count=3 if modes["session_mode"].isolation_required else 2,
        continuity_token_estimate=continuity_tokens,
        session_age=6,
        stale_continuity_reuse=handoff.stale_context_detected,
    )
    enforcement = BoundaryEnforcementPolicy().enforce(
        stale_session=stale,
        architecture_isolation_signal=modes["session_mode"].isolation_required,
    )
    export = _vscode_prompt_export(workspace, sprint)
    clipboard = ClipboardRuntimePolicy().copy(
        copy_ready_prompt=handoff.copy_ready_prompt,
        compact_bundle=handoff.continuity_bundle,
        clipboard_command="ai-dev-os-missing-clipboard",
    )
    rollover = RolloverStatePolicy().evaluate(
        rollover_required=stale.rollover_required,
        handoff_generated=bool(handoff.continuity_bundle),
        clipboard_ready=clipboard.clipboard_copy_success or clipboard.export_fallback,
        export_ready=export.bounded,
        confirmed=False,
        new_session_started=False,
        stale_session_active=stale.stale_session_detected,
    )
    confirmation = HandoffConfirmationPolicy().confirm(
        export_consumed=False,
        prompt_copied=clipboard.clipboard_copy_success,
        new_session_acknowledged=False,
        stale_session_closed=False,
    )
    return {
        "session_generation": generation,
        "stale_session": stale,
        "boundary_enforcement": enforcement,
        "rollover_state": rollover,
        "handoff_confirmation": confirmation,
    }


def _session_boundary_handoff(workspace: str, sprint: str):
    handoff = _vscode_handoff(workspace, sprint)
    boundary = _session_boundary(workspace, sprint)
    bundle = {
        **handoff.continuity_bundle,
        "session_generation_metadata": boundary["session_generation"],
        "boundary_enforcement": boundary["boundary_enforcement"],
        "rollover_state": boundary["rollover_state"],
        "stale_warning": boundary["stale_session"].boundary_violation_risk,
        "new_session_seed": handoff.copy_ready_prompt,
    }
    export = PromptExportPolicy().export(
        copy_ready_prompt=handoff.copy_ready_prompt,
        compact_bundle=_to_data(bundle),
    )
    return {
        "copy_ready_prompt": handoff.copy_ready_prompt,
        "compact_continuity_bundle": export,
        "session_generation": boundary["session_generation"],
        "stale_session": boundary["stale_session"],
        "boundary_enforcement": boundary["boundary_enforcement"],
        "rollover_state": boundary["rollover_state"],
        "handoff_confirmation": boundary["handoff_confirmation"],
    }


def _workspace_persistence(workspace: str, sprint: str):
    boundary = _session_boundary(workspace, sprint)
    modes = _prompt_modes(workspace, sprint)
    subset = _context_subset(workspace, sprint)
    handoff = _vscode_handoff(workspace, sprint)
    store = PersistenceStorePolicy().build(
        current_session_generation=boundary["session_generation"].active_generation,
        rollover_state=_to_data(boundary["rollover_state"]),
        last_continuity_bundle=handoff.continuity_bundle,
        current_prompt_mode=modes["reasoning_profile"].mode,
        session_focus=handoff.session_focus,
        stale_warning_state=_to_data(boundary["stale_session"]),
        repository_subset_summary=subset["repository_subset"].active_repositories,
        compact_continuity_metadata={
            "continuity_scope": subset["continuity_scope"].included_context,
            "prompt_mode": modes["reasoning_profile"].mode,
            "summary_only": True,
        },
        workspace=workspace,
    )
    restore = SessionRestorePolicy().restore(store)
    checkpoint = StateCheckpointPolicy().checkpoint(
        session_generation=store.current_session_generation,
        enforcement_state=boundary["boundary_enforcement"].enforcement_state,
        prompt_mode=store.current_prompt_mode,
        continuity_scope=subset["continuity_scope"].included_context,
        repository_subset=store.repository_subset_summary,
        active_sprint_metadata={
            "sprint": sprint,
            "session_focus": store.session_focus,
            "full_workspace_snapshot": "excluded",
        },
    )
    bundle_id = f"{Path(workspace).resolve().name}:{sprint}:{store.current_session_generation}"
    index = ContinuityIndexPolicy().index(
        continuity_bundle_ids=(bundle_id,),
        generation_mapping={bundle_id: store.current_session_generation},
        sprint_mapping={bundle_id: sprint},
        prompt_export_references=("prompt.txt", "continuation.md"),
        rollover_lineage=(boundary["session_generation"].parent_session, bundle_id),
        stale_continuity_flags=(
            ("stale-warning",) if boundary["stale_session"].stale_session_detected else ()
        ),
    )
    cleanup = PersistenceCleanupPolicy().cleanup(
        entries=("obsolete-continuity", bundle_id, "duplicate-compact-export"),
        active_entries=(bundle_id,),
        expired_entries=("obsolete-continuity",),
        duplicate_entries=("duplicate-compact-export",),
    )
    return {
        "persistence_store": store,
        "session_restore": restore,
        "state_checkpoint": checkpoint,
        "continuity_index": index,
        "persistence_cleanup": cleanup,
    }


def _prompt_pack_for_handoff(workspace: str, sprint: str):
    subset = _context_subset(workspace, sprint)
    modes = _prompt_modes(workspace, sprint)
    return PromptPackPolicy().build(
        prompt_type=modes["session_mode"].recommended_prompt_type,
        project_name="workspace",
        sprint_id=sprint,
        objective="human-confirmed bounded session handoff",
        context_lines=(
            "Use compact continuity only.",
            "Do not operate the Chat UI automatically.",
            "Repository subset: " + ", ".join(subset["repository_subset"].active_repositories),
            "Session focus: " + subset["session_focus"].recommended_session_type,
        ),
        required_context=("context_subset", "prompt_modes", "vscode_handoff"),
        excluded_context=("full_history", "chat_ui_automation"),
        affected_runtimes=("vscode_integration", "session_orchestrator"),
        prompt_shape=modes["prompt_shape"].recommended_prompt_shape,
        continuity_depth=modes["context_depth"].included_depth[-1],
        review_checklist=modes["review_intensity"].required_review_domains,
        architecture_allowance=modes["reasoning_profile"].architecture_allowance,
        retrieval_budget=modes["reasoning_profile"].retrieval_budget,
        plain_text=True,
    )


def _vscode_prompt_export(workspace: str, sprint: str):
    handoff = _vscode_handoff(workspace, sprint)
    return PromptExportPolicy().export(
        copy_ready_prompt=handoff.copy_ready_prompt,
        compact_bundle=handoff.continuity_bundle,
    )


def _vscode_copy_prompt(workspace: str, sprint: str):
    handoff = _vscode_handoff(workspace, sprint)
    return ClipboardRuntimePolicy().copy(
        copy_ready_prompt=handoff.copy_ready_prompt,
        compact_bundle=handoff.continuity_bundle,
    )


def _vscode_notifications(workspace: str, sprint: str):
    handoff = _vscode_handoff(workspace, sprint)
    modes = _prompt_modes(workspace, sprint)
    export = _vscode_prompt_export(workspace, sprint)
    return HandoffNotificationPolicy().notify(
        stale_context_detected=handoff.stale_context_detected,
        rollover_required=handoff.rollover_required,
        architecture_isolation_recommended=modes["session_mode"].isolation_required,
        continuity_generated=bool(handoff.continuity_bundle),
        prompt_export_ready=export.bounded,
    )


def _vscode_state(workspace: str, sprint: str):
    handoff = _vscode_handoff(workspace, sprint)
    modes = _prompt_modes(workspace, sprint)
    return IDEStatePolicy().snapshot(
        workspace,
        active_sprint=sprint,
        active_prompt_mode=modes["reasoning_profile"].mode,
        current_session_focus=handoff.session_focus,
        pending_rollover=handoff.recommended_new_session,
        export_availability=True,
    )


def _sprint_import(path: str):
    if not path:
        raise SystemExit("--from-file is required for sprint-import")
    return SprintMetadataPolicy().from_file(Path(path))


def _validation_summary(repo_path: str):
    git = GitCollector().collect(repo_path)
    return ValidationCollectorPolicy().collect(
        pytest_summary="existing results not executed by collector",
        scoped_pytest=tuple(f"changed test: {path}" for path in git.changed_test_paths),
        ruff_status="not_executed",
        black_status="not_executed",
        architecture_gates=tuple(
            f"governance path: {path}" for path in git.changed_governance_paths
        ),
        runtime_isolation_gates=("not_executed",),
        diff_check="not_executed",
        remote_ci_summary="not_checked",
    )


def _print_result(result: Any, *, json_mode: bool, copy_ready: bool) -> None:
    data = _to_data(result)
    if copy_ready and isinstance(data, dict) and "copy_ready_text" in data:
        print(data["copy_ready_text"])
        return
    if copy_ready and isinstance(data, dict) and "copy_ready_plain_text" in data:
        print(data["copy_ready_plain_text"])
        return
    if copy_ready and isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
        return
    if json_mode:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(data)


def _to_data(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, tuple):
        return tuple(_to_data(item) for item in value)
    if isinstance(value, dict):
        return {key: _to_data(item) for key, item in value.items()}
    return value


if __name__ == "__main__":
    raise SystemExit(main())
