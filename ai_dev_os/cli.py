from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from ai_dev_os.repository_intelligence.ci_context import CIContextPolicy
from ai_dev_os.repository_intelligence.git_collector import GitCollector
from ai_dev_os.repository_intelligence.runtime_discovery import RuntimeDiscoveryPolicy
from ai_dev_os.repository_intelligence.sprint_metadata import SprintMetadataPolicy
from ai_dev_os.repository_intelligence.validation_collector import ValidationCollectorPolicy
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
    parser.add_argument("--repo-path", default=".")
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
    raise SystemExit(f"unsupported command: {command}")


def _sprint_start(sprint: str, project: str):
    metadata = SprintMetadataPolicy().default(sprint_id=sprint, project_name=project)
    discovery = RuntimeDiscoveryPolicy().discover(".")
    affected = metadata.affected_runtimes or discovery.runtime_packages[:3]
    return SprintStartPolicy().build(
        SprintStartInput(
            sprint_id=sprint,
            project_name=project,
            active_fr_tc=("FR-SESSION-CLI-01", "TC-SESSION-CLI-01"),
            affected_runtimes=affected,
            previous_sprint_summary="Workspace metadata collected for bounded sprint start.",
            active_risks=metadata.active_risks,
            current_roadmap=(metadata.roadmap_stage,),
            architecture_flags=metadata.architecture_flags,
        )
    )


def _sprint_close(sprint: str, project: str):
    git = GitCollector().collect(".")
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
            validation_summary=f"Sprint {sprint} for {project}: {validation.remote_ci_summary}",
            git_status_summary=status,
            changed_paths=git.changed_runtime_paths + git.changed_test_paths,
            test_results=validation.scoped_pytest,
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
    metadata = SprintMetadataPolicy().default(project_name=project)
    discovery = RuntimeDiscoveryPolicy().discover(".")
    return ContinuityExportPolicy().export(
        active_requirements=tuple(
            item for item in metadata.active_fr_tc if item.startswith("FR-")
        ),
        active_tests=tuple(item for item in metadata.active_fr_tc if item.startswith("TC-")),
        current_sprint_boundary=f"{project}: next bounded session",
        affected_runtimes=metadata.affected_runtimes or discovery.runtime_packages[:3],
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


def _repo_intel(repo_path: str):
    return {
        "git": GitCollector().collect(repo_path),
        "runtime_discovery": RuntimeDiscoveryPolicy().discover(repo_path),
        "validation": _validation_summary(repo_path),
        "ci_context": CIContextPolicy().default_local(),
    }


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
