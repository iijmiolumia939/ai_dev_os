from __future__ import annotations

from ai_dev_os.session_lifecycle.architecture_isolation import ArchitectureIsolationPolicy
from ai_dev_os.session_lifecycle.continuity_bundle import (
    ContinuityBundlePolicy,
    ContinuityBundleSource,
)


def source() -> ContinuityBundleSource:
    return ContinuityBundleSource(
        active_fr_tc=("FR-SESSION-01", "FR-SESSION-02", "TC-SESSION-01", "TC-SESSION-02"),
        current_sprint_summary="Session lifecycle governance prevents stale context replay. " * 80,
        affected_runtimes=("session_lifecycle", "retrieval", "runtime_audit"),
        active_risks=("hidden token burn", "stale retrieval", "architecture mixing"),
        current_roadmap=("rollover", "bundle", "audit"),
        current_architectural_constraints=(
            "retrieval-first continuity",
            "bounded context lifecycle",
            "no full session replay",
        ),
        current_governance_state={"pressure": "HIGH", "tier2": "disabled"},
        extra_context={
            "full_sprint_history": "history " * 10_000,
            "giant_markdown": "markdown " * 8_000,
            "stale_oq": "question " * 5_000,
            "obsolete_adr": "adr " * 4_000,
            "full_repository_tree": "tree " * 8_000,
            "small_active_note": "active bounded note",
        },
    )


def test_compact_continuity_bundle_excludes_giant_replay_and_full_repository() -> None:
    frame = ContinuityBundlePolicy(token_budget=2_400).build(source(), summary_only=True)

    assert frame.bundle_token_estimate <= 2_400
    assert frame.summary_only is True
    assert "full_sprint_history" in frame.excluded_context
    assert "full_repository_tree" in frame.excluded_context
    assert "giant_markdown" in frame.excluded_context
    assert frame.token_reduction_estimate > frame.bundle_token_estimate
    assert frame.active_fr_tc == (
        "FR-SESSION-01",
        "FR-SESSION-02",
        "TC-SESSION-01",
        "TC-SESSION-02",
    )


def test_architecture_isolation_detects_redesign_and_broad_review() -> None:
    frame = ArchitectureIsolationPolicy().evaluate(
        "Please do an architecture redesign and runtime contract redesign, "
        "then review everything.",
        affected_runtimes=("session_lifecycle", "runtime_contracts"),
        routine_patch=True,
    )

    assert frame.isolated_session_required is True
    assert frame.fresh_session_required is True
    assert frame.scoped_architecture_bundle == ("session_lifecycle", "runtime_contracts")
    assert "architecture_redesign" in frame.detected_patterns
    assert "runtime_contract_redesign" in frame.detected_patterns
    assert "broad_review_request" in frame.detected_patterns
    assert "routine_patch_architecture_mixing" in frame.detected_patterns
    assert frame.warnings == ("routine_patch_must_not_mix_architecture_context",)


def test_continuity_bundle_output_is_deterministic() -> None:
    policy = ContinuityBundlePolicy(token_budget=2_400)

    assert policy.build(source(), summary_only=True) == policy.build(source(), summary_only=True)
