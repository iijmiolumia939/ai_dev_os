from __future__ import annotations

from pathlib import Path

from ai_dev_os.repository_intelligence.ci_context import CIContextPolicy
from ai_dev_os.repository_intelligence.git_collector import GitCollector
from ai_dev_os.repository_intelligence.runtime_discovery import RuntimeDiscoveryPolicy
from ai_dev_os.repository_intelligence.sprint_metadata import SprintMetadataPolicy
from ai_dev_os.repository_intelligence.validation_collector import ValidationCollectorPolicy


def test_git_collector_is_read_only_and_reports_repository_state() -> None:
    root = Path(__file__).resolve().parents[2]
    before = GitCollector().collect(root)
    after = GitCollector().collect(root)

    assert before == after
    assert before.read_only is True
    assert before.current_branch
    assert before.local_head
    assert before.modified_file_count >= 0
    assert isinstance(before.changed_runtime_paths, tuple)


def test_sprint_metadata_parses_simple_sprint_yml(tmp_path: Path) -> None:
    sprint_file = tmp_path / "sprint.yml"
    sprint_file.write_text(
        "\n".join(
            (
                "sprint_id: 42",
                "active_fr_tc:",
                "  - FR-REPOINTEL-01",
                "  - TC-REPOINTEL-01",
                "affected_runtimes: [repository_intelligence, session_orchestrator]",
                "roadmap_stage: workspace collector",
                "active_risks:",
                "  - manual summary drift",
                "architecture_flags:",
                "  - read-only collector",
                "continuity_state: compact",
                "validation_status: pending",
            )
        ),
        encoding="utf-8",
    )

    frame = SprintMetadataPolicy().from_file(sprint_file)

    assert frame.sprint_id == "42"
    assert frame.active_fr_tc == ("FR-REPOINTEL-01", "TC-REPOINTEL-01")
    assert frame.affected_runtimes == ("repository_intelligence", "session_orchestrator")
    assert frame.schema_supported is True


def test_runtime_discovery_finds_runtime_tests_and_relationships() -> None:
    root = Path(__file__).resolve().parents[2]
    frame = RuntimeDiscoveryPolicy().discover(root)

    assert "ai_dev_os/repository_intelligence" in frame.runtime_packages
    assert "tests/repository_intelligence" in frame.test_packages
    assert frame.runtime_relationship_summary


def test_validation_summary_aggregation_and_ci_context_parsing() -> None:
    validation = ValidationCollectorPolicy().collect(
        pytest_summary="63 passed",
        scoped_pytest=("tests/repository_intelligence: passed",),
        ruff_status="pass",
        black_status="pass",
        architecture_gates=("gates passed",),
        runtime_isolation_gates=("runtime isolation passed",),
        diff_check="clean",
        remote_ci_summary="success",
    )
    ci = CIContextPolicy().from_summary(
        latest_ci_status="failure",
        known_failures=("Unity license activation failed",),
    )

    assert validation.all_passed is True
    assert ci.unity_license_failure_detected is True
    assert ci.remote_required is True
