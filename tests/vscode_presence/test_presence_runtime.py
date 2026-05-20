from __future__ import annotations

import json
import time
from pathlib import Path

from ai_dev_os.vscode_presence import (
    build_heartbeat_frame,
    build_presence_frame,
    detect_extension_version,
    project_governance_status,
)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_tc_presence_01_presence_frame_is_summary_only(tmp_path: Path) -> None:
    root = tmp_path
    (root / "extensions" / "ai-dev-os-vscode" / "src").mkdir(parents=True)
    _write_json(
        root / "extensions" / "ai-dev-os-vscode" / "package.json", {"version": "0.1.0-alpha.3"}
    )
    (root / "extensions" / "ai-dev-os-vscode" / "src" / "extension.ts").write_text(
        "", encoding="utf-8"
    )
    _write_json(
        root / ".ai-dev-os" / "session-boundary.json",
        {
            "current_session_generation": 42,
            "rollover_state": {"rollover_pending": True},
            "stale_warning_state": {"stale_session_detected": False, "warning_count": 0},
            "summary_only": True,
            "bounded": True,
        },
    )
    _write_json(root / ".ai-dev-os" / "rollover-state.json", {"rollover_pending": True})
    _write_json(root / ".ai-dev-os" / "continuity-index.json", {"continuity_bundle_ids": []})

    frame = build_presence_frame(root)

    assert frame.extension_active is True
    assert frame.persistence_active is True
    assert frame.current_session_generation == 42
    assert frame.rollover_pending is True
    assert frame.bounded_presence_confirmed is True
    assert frame.raw_transcript_included is False


def test_tc_presence_02_version_mismatch_detects_stale_install(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "extensions"
    _write_json(
        root / "extensions" / "ai-dev-os-vscode" / "package.json",
        {"version": "0.1.0-alpha.3"},
    )
    _write_json(
        installed / "iijmiolumia939.ai-dev-os-vscode-0.1.0" / "package.json",
        {"version": "0.1.0"},
    )

    frame = detect_extension_version(root, installed_extensions_dir=installed)

    assert frame.repo_version == "0.1.0-alpha.3"
    assert frame.installed_version == "0.1.0"
    assert frame.version_match is False
    assert frame.stale_extension_detected is True
    assert frame.reinstall_recommended is True
    assert frame.duplicate_install_detected is False


def test_tc_presence_03_runtime_heartbeat_is_bounded(tmp_path: Path) -> None:
    now = time.time()
    _write_json(tmp_path / ".ai-dev-os" / "session-boundary.json", {"summary_only": True})
    _write_json(tmp_path / ".ai-dev-os" / "rollover-state.json", {"rollover_pending": False})
    _write_json(tmp_path / ".ai-dev-os" / "continuity-index.json", {"continuity_bundle_ids": []})

    frame = build_heartbeat_frame(tmp_path, now=now + 1)

    assert frame.heartbeat_active is True
    assert frame.stale_heartbeat is False
    assert frame.heartbeat_summary == "ACTIVE"
    assert frame.summary_only is True
    assert frame.full_logs_included is False


def test_tc_presence_04_compact_status_projection_is_low_noise(tmp_path: Path) -> None:
    _write_json(
        tmp_path / ".ai-dev-os" / "session-boundary.json",
        {
            "current_session_generation": 7,
            "rollover_state": {"rollover_pending": False},
            "stale_warning_state": {"stale_session_detected": False},
            "summary_only": True,
            "bounded": True,
        },
    )
    _write_json(tmp_path / ".ai-dev-os" / "rollover-state.json", {"rollover_pending": False})
    _write_json(tmp_path / ".ai-dev-os" / "continuity-index.json", {})

    presence = build_presence_frame(tmp_path)
    frame = project_governance_status(presence, pressure="LOW")

    assert frame.compact_status == "AI_DEV_OS PARTIAL GEN:7 LOW_PRESSURE ROLLOVER_OK"
    assert frame.severity == "OK"
    assert frame.notification_required is False
    assert frame.automatic_action_allowed is False


def test_tc_presence_05_presence_runtime_does_not_mutate_workspace(tmp_path: Path) -> None:
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    build_presence_frame(tmp_path)
    build_heartbeat_frame(tmp_path)
    detect_extension_version(tmp_path, installed_extensions_dir=tmp_path / "missing")

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert after == before
