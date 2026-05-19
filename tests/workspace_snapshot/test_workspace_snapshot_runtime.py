from __future__ import annotations

import subprocess
from pathlib import Path

from ai_dev_os.workspace_snapshot.architecture_hotspots import ArchitectureHotspotPolicy
from ai_dev_os.workspace_snapshot.known_failures import KnownFailurePolicy
from ai_dev_os.workspace_snapshot.multi_repository import MultiRepositoryPolicy
from ai_dev_os.workspace_snapshot.rollout_tracking import RolloutTrackingPolicy
from ai_dev_os.workspace_snapshot.workspace_state import WorkspaceStateFrame, WorkspaceStatePolicy


def test_workspace_snapshot_deterministic() -> None:
    root = Path(__file__).resolve().parents[2]
    before = WorkspaceStatePolicy().snapshot(root, current_sprint="TC-WORKSPACE-01")
    after = WorkspaceStatePolicy().snapshot(root, current_sprint="TC-WORKSPACE-01")

    assert before == after
    assert before.read_only is True
    assert before.active_repositories
    assert before.continuity_state in {"bounded", "truncated"}
    assert all("/" not in repository for repository in before.active_repositories)


def test_multi_repository_isolation_and_dependency_summary(tmp_path: Path) -> None:
    platform = tmp_path / "ai_dev_os"
    consumer = tmp_path / "consumer_app"
    isolated = tmp_path / "isolated_tool"
    for repository in (platform, consumer, isolated):
        repository.mkdir()
        (repository / ".git").mkdir()
    (platform / "pyproject.toml").write_text(
        '[project]\nname = "ai-dev-os"\nversion = "0.1.0a2"\n', encoding="utf-8"
    )
    (consumer / "pyproject.toml").write_text(
        '[project]\ndependencies = ["ai-dev-os"]\n', encoding="utf-8"
    )

    frame = MultiRepositoryPolicy().map(tmp_path)

    assert frame.ai_dev_os_consumer_repos == ("consumer_app",)
    assert "isolated_tool" in frame.isolated_repos
    assert frame.migration_state["ai_dev_os"] == "platform"
    assert frame.repository_dependency_graph_summary
    assert frame.read_only is True


def test_rollout_tracking_validation(tmp_path: Path) -> None:
    platform = tmp_path / "ai_dev_os"
    consumer = tmp_path / "consumer_app"
    for repository in (platform, consumer):
        repository.mkdir()
        (repository / ".git").mkdir()
    (platform / "pyproject.toml").write_text(
        '[project]\nname = "ai-dev-os"\nversion = "0.1.0a2"\n', encoding="utf-8"
    )
    (consumer / "pyproject.toml").write_text(
        '[project]\ndependencies = ["ai-dev-os"]\n', encoding="utf-8"
    )

    frame = RolloutTrackingPolicy().track(tmp_path)

    assert frame.ai_dev_os_version == "0.1.0a2"
    assert frame.rollout_stage == "consumer-rollout"
    assert frame.consumer_adoption_status["consumer_app"] == "adopted"
    assert frame.migration_completeness == 1.0


def test_known_failure_classification() -> None:
    frame = KnownFailurePolicy().classify(
        current_failures=("Unity license activation failed", "new pytest regression"),
        known_unity_license_failures=("Unity license activation failed",),
        known_vendor_exclusions=("vendor generated warning",),
    )

    assert frame.baseline_failures == (
        "Unity license activation failed",
        "vendor generated warning",
    )
    assert frame.unresolved_failures == ("Unity license activation failed",)
    assert frame.new_failures == ("new pytest regression",)
    assert frame.ignored_failures == ()


def test_architecture_hotspot_detection() -> None:
    state = WorkspaceStateFrame(
        active_repositories=("ai_dev_os", "consumer_app", "AITuber"),
        current_sprint="TC-WORKSPACE-05",
        modified_repositories=("ai_dev_os", "AITuber"),
        dirty_runtime_counts={"ai_dev_os": 6, "AITuber": 2},
        dirty_governance_counts={"ai_dev_os": 2, "AITuber": 0},
        dirty_adapter_counts={"ai_dev_os": 2, "AITuber": 0},
        untracked_artifact_counts={"ai_dev_os": 0, "AITuber": 0},
        architecture_review_pending=True,
        rollout_state="active",
        continuity_state="bounded",
        bounded_summary=("repositories=3", "modified=2"),
        read_only=True,
    )

    frame = ArchitectureHotspotPolicy().detect(state=state)

    assert frame.broad_runtime_modifications is True
    assert frame.cross_boundary_modifications is True
    assert frame.governance_leakage_risk is True
    assert frame.provider_lock_in_risk is True
    assert frame.risk_severity in {"high", "critical"}
    assert frame.review_recommendation == "architecture_review_required"


def test_bounded_workspace_continuity(tmp_path: Path) -> None:
    for index in range(5):
        repository = tmp_path / f"repo_{index}"
        repository.mkdir()
        subprocess.run(("git", "init"), cwd=repository, check=True, capture_output=True)

    frame = WorkspaceStatePolicy().snapshot(tmp_path, max_repositories=3)

    assert len(frame.active_repositories) == 3
    assert frame.continuity_state == "bounded"
    assert frame.read_only is True
