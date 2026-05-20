from __future__ import annotations

from ai_dev_os.workspace_persistence.continuity_index import ContinuityIndexPolicy
from ai_dev_os.workspace_persistence.persistence_cleanup import PersistenceCleanupPolicy
from ai_dev_os.workspace_persistence.persistence_store import PersistenceStorePolicy
from ai_dev_os.workspace_persistence.session_restore import SessionRestorePolicy
from ai_dev_os.workspace_persistence.state_checkpoint import StateCheckpointPolicy


def test_persistence_store_validation_removes_forbidden_keys(tmp_path) -> None:
    frame = PersistenceStorePolicy().build(
        current_session_generation=2,
        rollover_state={"rollover_pending": True, "raw_transcript": "secret"},
        last_continuity_bundle={"bundle_id": "b-2", "provider_responses": "raw"},
        current_prompt_mode="bounded_implementation",
        session_focus="bounded-implementation",
        stale_warning_state={"stale_session_detected": True},
        repository_subset_summary=("ai_dev_os", "consumer", "third", "fourth", "fifth", "sixth"),
        compact_continuity_metadata={"summary_only": True, "full_prompt_history": "raw"},
        workspace=tmp_path,
    )

    assert frame.bounded is True
    assert frame.summary_only is True
    assert "raw_transcript" in frame.forbidden_keys_removed
    assert "provider_responses" in frame.forbidden_keys_removed
    assert "full_prompt_history" in frame.forbidden_keys_removed
    assert len(frame.repository_subset_summary) == 5
    assert "raw_transcript" not in frame.rollover_state


def test_persistence_store_roundtrip_is_workspace_local(tmp_path) -> None:
    policy = PersistenceStorePolicy()
    frame = policy.build(
        current_session_generation=3,
        rollover_state={"rollover_pending": False},
        last_continuity_bundle={"bundle_id": "b-3"},
        current_prompt_mode="bounded_implementation",
        session_focus="bounded-implementation",
        stale_warning_state={"stale_session_detected": False},
        repository_subset_summary=("ai_dev_os",),
        compact_continuity_metadata={"summary_only": True},
        workspace=tmp_path,
    )
    policy.write(frame)
    restored = policy.read(tmp_path)

    assert restored is not None
    assert restored.store_path.startswith(str(tmp_path))
    assert restored.current_session_generation == 3


def test_session_restore_does_not_auto_apply_stale_persistence(tmp_path) -> None:
    store = PersistenceStorePolicy().build(
        current_session_generation=4,
        rollover_state={"rollover_pending": True},
        last_continuity_bundle={"bundle_id": "b-4"},
        current_prompt_mode="bounded_implementation",
        session_focus="bounded-implementation",
        stale_warning_state={"stale_session_detected": True},
        repository_subset_summary=("ai_dev_os",),
        compact_continuity_metadata={"summary_only": True},
        workspace=tmp_path,
    )
    frame = SessionRestorePolicy().restore(store)

    assert frame.restore_available is True
    assert frame.restored_generation == 4
    assert frame.pending_rollover_restored is True
    assert frame.compact_bundle_restored is True
    assert frame.stale_state_detected is True
    assert frame.stale_persistence_auto_applied is False


def test_checkpoint_budget_enforcement() -> None:
    frame = StateCheckpointPolicy().checkpoint(
        session_generation=1,
        enforcement_state="ROLLOVER_REQUIRED",
        prompt_mode="bounded_implementation",
        continuity_scope=("active_sprint_continuity", "repository_subset"),
        repository_subset=("ai_dev_os",),
        active_sprint_metadata={"sprint": "42", "full_workspace_snapshot": "raw"},
        size_budget=128,
    )

    assert frame.estimated_size <= frame.size_budget
    assert frame.full_workspace_snapshot_included is False
    assert "full_workspace_snapshot" not in frame.active_sprint_metadata


def test_continuity_index_is_summary_only() -> None:
    frame = ContinuityIndexPolicy().index(
        continuity_bundle_ids=("b-1", "b-1", "b-2"),
        generation_mapping={"b-1": 1, "b-2": 2},
        sprint_mapping={"b-1": "s1", "b-2": "s2"},
        prompt_export_references=("prompt.txt",),
        rollover_lineage=("b-1", "b-2"),
        stale_continuity_flags=("b-1",),
    )

    assert frame.continuity_bundle_ids == ("b-1", "b-2")
    assert frame.summary_only is True
    assert frame.raw_export_replay_allowed is False


def test_cleanup_validation_detects_stale_entries() -> None:
    frame = PersistenceCleanupPolicy().cleanup(
        entries=("obsolete-bundle", "active-bundle", "duplicate-export"),
        active_entries=("active-bundle",),
        expired_entries=("obsolete-bundle",),
        duplicate_entries=("duplicate-export",),
    )

    assert frame.stale_persistence_detected is True
    assert frame.cleaned_entries == ("obsolete-bundle", "duplicate-export")
    assert frame.retained_entries == ("active-bundle",)
    assert frame.estimated_saved_storage > 0
