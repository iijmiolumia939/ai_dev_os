from __future__ import annotations

from ai_dev_os.session_orchestrator.continuity_export import ContinuityExportPolicy
from ai_dev_os.session_orchestrator.prompt_pack import PromptPackPolicy
from ai_dev_os.session_orchestrator.sprint_close import SprintCloseInput, SprintClosePolicy
from ai_dev_os.session_orchestrator.sprint_start import SprintStartInput, SprintStartPolicy


def test_sprint_start_generates_compact_copy_ready_prompt() -> None:
    frame = SprintStartPolicy().build(
        SprintStartInput(
            sprint_id="42",
            project_name="aituber",
            active_fr_tc=("FR-SESSION-CLI-01", "TC-SESSION-CLI-01"),
            affected_runtimes=("session_orchestrator", "session_lifecycle"),
            previous_sprint_summary="Session lifecycle governance completed.",
            active_risks=("hidden token burn",),
            current_roadmap=("CLI automation",),
            architecture_flags=("bounded continuity",),
        )
    )

    assert frame.context_budget_estimate > 0
    assert frame.copy_ready_prompt == frame.sprint_prompt
    assert "full_sprint_history" in frame.excluded_context
    assert "giant_markdown" in frame.excluded_context
    assert "Session lifecycle governance completed" in frame.copy_ready_prompt
    assert frame.recommended_reasoning_tier == "HIGH"
    assert frame.sprint_reasoning_map["architecture"] == "HIGH"
    assert frame.sprint_reasoning_map["runtime tests"] == "LOW"
    assert frame.sprint_reasoning_map["docs"] == "LOW"
    assert frame.sprint_reasoning_map["adapter wiring"] == "MEDIUM"
    assert frame.compaction_recommendations["architecture"] is True


def test_sprint_close_recommends_next_session_bundle_and_remote_verification() -> None:
    frame = SprintClosePolicy().close(
        SprintCloseInput(
            validation_summary="local validation pass",
            git_status_summary="clean; ahead 1",
            changed_paths=("ai_dev_os/session_orchestrator",),
            test_results=("pytest tests/session_orchestrator: pass",),
            remaining_risks=("remote CI pending",),
            next_roadmap=("release gate",),
            commit="abc123",
            ci_status="success",
            runtime_audit_status="active",
            rollout_summary="rollout unchanged",
        )
    )

    assert frame.session_should_close is True
    assert frame.next_session_bundle_required is True
    assert frame.commit_push_required is True
    assert frame.remote_verification_required is True
    assert "Next sprint context seed" in frame.next_sprint_context_seed
    assert frame.compact_reporting_active is True
    assert "Commit: abc123" in frame.compact_sprint_completion
    assert frame.compact_ci_summary == "CI: success"
    assert frame.compact_runtime_audit_summary == "Runtime audit: active"
    assert frame.compact_rollout_summary == "Rollout: compact-ref"
    assert frame.expandable_completion_details
    assert frame.estimated_avoided_completion_tokens >= 0


def test_prompt_pack_is_copy_ready_plain_text() -> None:
    frame = PromptPackPolicy().build(
        prompt_type="session_rollover",
        project_name="aituber",
        context_lines=("Use compact bundle only.",),
        excluded_context=("full_history",),
        plain_text=True,
    )

    assert frame.copy_ready_text == frame.plain_text
    assert "```" not in frame.copy_ready_text
    assert frame.estimated_tokens > 0
    assert "full_history_excluded" in frame.warnings


def test_continuity_export_excludes_full_history_and_generated_artifacts() -> None:
    frame = ContinuityExportPolicy().export(
        active_requirements=("FR-SESSION-CLI-05",),
        active_tests=("TC-SESSION-CLI-05",),
        current_sprint_boundary="Sprint 42",
        affected_runtimes=("session_orchestrator",),
        current_architecture_constraints=("no UI automation",),
        active_risks=("manual copy remains",),
        next_prompt_seed="Paste compact bundle only.",
        output_format="plain",
        extra_context={
            "full_history": "history " * 10_000,
            "generated_artifacts": "build output",
            "raw_memory": "raw memory",
        },
    )

    assert "full_history" in frame.excluded_context
    assert "generated_artifacts" in frame.excluded_context
    assert "raw_memory" in frame.excluded_context
    assert "history history" not in frame.copy_ready_text
    assert frame.estimated_tokens > 0
