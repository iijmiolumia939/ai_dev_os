from __future__ import annotations

import json
import subprocess
import sys

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit
from ai_dev_os.session_lifecycle.architecture_isolation import ArchitectureIsolationPolicy
from ai_dev_os.session_lifecycle.cache_aware_session import CacheAwareSessionPolicy
from ai_dev_os.session_lifecycle.session_rollover import SessionRolloverPolicy
from ai_dev_os.session_lifecycle.stale_context_detection import (
    ContextSignal,
    StaleContextDetectionPolicy,
)
from ai_dev_os.session_orchestrator.session_decision import SessionDecisionPolicy
from ai_dev_os.session_orchestrator.sprint_start import SprintStartInput, SprintStartPolicy


def test_session_decision_forks_on_high_stale_context() -> None:
    rollover = SessionRolloverPolicy().evaluate(
        session_age=6,
        estimated_context_tokens=28_000,
        stale_context_ratio=0.7,
        retrieval_pressure="HIGH",
        cache_reuse_probability=0.8,
        sprint_boundary=True,
    )
    stale = StaleContextDetectionPolicy().evaluate(
        (ContextSignal("old", 10_000, "old sprint", 0.2, age_days=45),)
    )
    cache = CacheAwareSessionPolicy().evaluate(
        cache_reuse_probability=0.8,
        repeated_instruction_stability=0.8,
        context_freshness=0.3,
        retrieval_overlap=0.2,
        prompt_compactness=0.8,
        pressure="HIGH",
    )
    architecture = ArchitectureIsolationPolicy().evaluate("routine patch")

    frame = SessionDecisionPolicy().decide(
        rollover=rollover,
        stale=stale,
        cache=cache,
        architecture=architecture,
    )

    assert frame.fork_new_session is True
    assert frame.stop_and_close_session is True
    assert frame.continue_current_session is False
    assert "rollover_or_stale_context" in frame.reasons


def test_cli_json_mode_works() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "sprint-start",
            "--sprint",
            "42",
            "--project",
            "aituber",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)

    assert data["context_budget_estimate"] > 0
    assert data["continuity_bundle"]["active_fr_tc"] == [
        "FR-SESSION-CLI-01",
        "TC-SESSION-CLI-01",
    ]


def test_cli_copy_ready_mode_works() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_dev_os.cli",
            "prompt-pack",
            "--type",
            "sprint-start",
            "--project",
            "aituber",
            "--copy-ready",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Start sprint" in completed.stdout
    assert "```" not in completed.stdout
    assert "full sprint history" in completed.stdout.lower()


def test_runtime_audit_reports_session_orchestrator() -> None:
    report = run_runtime_enforcement_audit()

    assert report.session_orchestrator.sprint_start_automation_active is True
    assert report.session_orchestrator.sprint_close_automation_active is True
    assert report.session_orchestrator.prompt_pack_generation_active is True
    assert report.session_orchestrator.continuity_export_active is True
    assert report.session_orchestrator.session_decision_active is True
    assert report.session_orchestrator.copy_ready_output_generated is True
    assert report.session_orchestrator.estimated_avoided_manual_context_tokens > 0


def test_session_orchestrator_outputs_are_deterministic() -> None:
    data = SprintStartInput(
        sprint_id="42",
        project_name="aituber",
        active_fr_tc=("FR-SESSION-CLI-01",),
        affected_runtimes=("session_orchestrator",),
        previous_sprint_summary="Previous sprint complete.",
        active_risks=("manual rollover",),
        current_roadmap=("CLI",),
    )

    assert SprintStartPolicy().build(data) == SprintStartPolicy().build(data)
