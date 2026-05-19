from __future__ import annotations

import inspect

from ai_dev_os.context_subset.continuity_scope import ContinuityScopeFrame
from ai_dev_os.context_subset.repository_subset import RepositorySubsetFrame
from ai_dev_os.context_subset.session_focus import SessionFocusFrame
from ai_dev_os.prompt_modes.session_mode_router import SessionModeRouterFrame
from ai_dev_os.vscode_integration.clipboard_runtime import ClipboardRuntimePolicy
from ai_dev_os.vscode_integration.handoff_notifications import HandoffNotificationPolicy
from ai_dev_os.vscode_integration.ide_state import IDEStatePolicy
from ai_dev_os.vscode_integration.prompt_export import PromptExportPolicy
from ai_dev_os.vscode_integration.session_handoff import SessionHandoffPolicy


def test_session_handoff_generation_is_bounded() -> None:
    frame = SessionHandoffPolicy().build(
        rollover_required=True,
        stale_context_detected=True,
        session_mode=SessionModeRouterFrame(
            recommended_mode="bounded_implementation",
            fallback_mode="bounded_implementation",
            escalation_required=False,
            compact_mode=True,
            isolation_required=False,
            recommended_prompt_type="patch_only",
        ),
        repository_subset=RepositorySubsetFrame(
            active_repositories=("ai_dev_os",),
            excluded_repositories=("legacy",),
            stale_repositories=(),
            architecture_sensitive_repositories=(),
            rollout_related_repositories=(),
            continuity_priority=("repo:ai_dev_os",),
            summary_only=True,
            full_workspace_continuation_blocked=True,
        ),
        session_focus=SessionFocusFrame(
            primary_focus="implementation",
            secondary_focus=("validation",),
            excluded_focus=("architecture",),
            escalation_required=False,
            focus_drift_risk="low",
            recommended_session_type="bounded-implementation",
        ),
        continuity_scope=ContinuityScopeFrame(
            included_context=("active_requirements", "repository_subset"),
            excluded_context=("full_history", "stale_topics"),
            continuity_depth="minimal",
            continuity_budget=900,
            summary_only_required=True,
        ),
        prompt_text="Patch only prompt",
    )

    assert frame.recommended_new_session is True
    assert frame.full_history_included is False
    assert frame.repository_subset == ("ai_dev_os",)
    assert "full history" in frame.copy_ready_prompt.lower()


def test_prompt_export_writes_compact_files_when_requested(tmp_path) -> None:
    frame = PromptExportPolicy().export(
        copy_ready_prompt="next-session prompt",
        compact_bundle={
            "handoff_summary": ("ready",),
            "repository_subset": ("ai_dev_os",),
            "full_history": "must not export",
        },
        output_dir=tmp_path,
    )

    assert frame.files_written is True
    assert frame.summary_only is True
    assert (tmp_path / "prompt.txt").read_text(encoding="utf-8") == "next-session prompt"
    assert "must not export" not in (tmp_path / "compact_bundle.json").read_text(encoding="utf-8")


def test_clipboard_fallback_uses_file_export_without_real_clipboard(tmp_path) -> None:
    frame = ClipboardRuntimePolicy().copy(
        copy_ready_prompt="copy ready prompt",
        compact_bundle={"handoff_summary": ("fallback",)},
        output_dir=tmp_path,
        clipboard_command="ai-dev-os-missing-clipboard",
    )

    assert frame.clipboard_available is False
    assert frame.clipboard_copy_success is False
    assert frame.export_fallback is True
    assert frame.fallback_export is not None
    assert frame.fallback_export.files_written is True


def test_notification_rate_limiting() -> None:
    frame = HandoffNotificationPolicy().notify(
        stale_context_detected=True,
        rollover_required=True,
        architecture_isolation_recommended=True,
        continuity_generated=True,
        prompt_export_ready=True,
        max_notifications=2,
    )

    assert frame.rate_limited is True
    assert frame.emitted_count == 2
    assert frame.suppressed_count == 3


def test_ide_state_is_deterministic_and_local() -> None:
    first = IDEStatePolicy().snapshot(
        ".", active_sprint="42", active_prompt_mode="bounded_implementation"
    )
    second = IDEStatePolicy().snapshot(
        ".", active_sprint="42", active_prompt_mode="bounded_implementation"
    )

    assert first == second
    assert first.network_used is False
    assert first.telemetry_collected is False


def test_vscode_runtime_has_no_network_or_ui_automation_imports() -> None:
    modules = (
        ClipboardRuntimePolicy,
        HandoffNotificationPolicy,
        IDEStatePolicy,
        PromptExportPolicy,
        SessionHandoffPolicy,
    )
    source = "\n".join(inspect.getsource(module) for module in modules)

    assert "requests" not in source
    assert "webbrowser" not in source
    assert "playwright" not in source
    assert "selenium" not in source
