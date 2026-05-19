from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from typing import Any

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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ai_dev_os.cli")
    parser.add_argument("command")
    parser.add_argument("--sprint", default="next")
    parser.add_argument("--project", default="project")
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
    raise SystemExit(f"unsupported command: {command}")


def _sprint_start(sprint: str, project: str):
    return SprintStartPolicy().build(
        SprintStartInput(
            sprint_id=sprint,
            project_name=project,
            active_fr_tc=("FR-SESSION-CLI-01", "TC-SESSION-CLI-01"),
            affected_runtimes=("session_orchestrator", "session_lifecycle"),
            previous_sprint_summary="Previous sprint completed session lifecycle governance.",
            active_risks=("hidden token burn", "manual rollover drift"),
            current_roadmap=("sprint start automation", "prompt pack", "CLI validation"),
            architecture_flags=("bounded continuity",),
        )
    )


def _sprint_close(sprint: str, project: str):
    return SprintClosePolicy().close(
        SprintCloseInput(
            validation_summary=(
                f"Sprint {sprint} for {project}: local checks pass; remote CI pending."
            ),
            git_status_summary="clean; ahead 1",
            changed_paths=("ai_dev_os/session_orchestrator", "tests/session_orchestrator"),
            test_results=("pytest tests/session_orchestrator: pass",),
            remaining_risks=("remote verification required",),
            next_roadmap=("release governance", "consumer workflow"),
        )
    )


def _prompt_pack(prompt_type: str, project: str, sprint: str):
    return PromptPackPolicy().build(
        prompt_type=prompt_type,
        project_name=project,
        sprint_id=sprint,
        objective="automate bounded session orchestration",
        context_lines=(
            "Use compact continuity bundle only.",
            "Do not replay full sprint history.",
            "Return validation and remote verification summary.",
        ),
        required_context=("continuity_bundle", "active_fr_tc"),
        excluded_context=("full_history", "generated_artifacts"),
        affected_runtimes=("session_orchestrator",),
        plain_text=True,
    )


def _continuity_export(project: str, *, output_format: str):
    return ContinuityExportPolicy().export(
        active_requirements=("FR-SESSION-CLI-01", "FR-SESSION-CLI-02"),
        active_tests=("TC-SESSION-CLI-01", "TC-SESSION-CLI-02"),
        current_sprint_boundary=f"{project}: next bounded session",
        affected_runtimes=("session_orchestrator", "session_lifecycle"),
        current_architecture_constraints=("no UI automation", "no full history replay"),
        active_risks=("manual copy step remains",),
        next_prompt_seed="Start the next sprint from this compact bundle only.",
        output_format=output_format,
        extra_context={"full_history": "excluded", "generated_artifacts": "excluded"},
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
    architecture = ArchitectureIsolationPolicy().evaluate(
        "routine sprint session",
        affected_runtimes=("session_orchestrator",),
    )
    return SessionDecisionPolicy().decide(
        rollover=rollover,
        stale=stale,
        cache=cache,
        architecture=architecture,
    )


def _print_result(result: Any, *, json_mode: bool, copy_ready: bool) -> None:
    data = _to_data(result)
    if copy_ready and isinstance(data, dict) and "copy_ready_text" in data:
        print(data["copy_ready_text"])
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
