from __future__ import annotations

import inspect
import json
from pathlib import Path

from ai_dev_os.governance_core import GovernanceCorePolicy
from ai_dev_os.governance_core.bounded_retention import GovernanceBoundedRetentionPrimitive
from ai_dev_os.governance_core.compact_export import GovernanceCompactExportPrimitive
from ai_dev_os.governance_core.continuity_primitives import GovernanceContinuityPrimitive
from ai_dev_os.governance_core.pressure_primitives import GovernancePressurePrimitive
from ai_dev_os.governance_core.stale_detection import GovernanceStaleDetectionPrimitive

ROOT = Path("extensions/ai-dev-os-vscode")


def test_governance_core_primitive_activation() -> None:
    frame = GovernanceCorePolicy().evaluate()

    assert frame.governance_core_active is True
    assert frame.bounded_governance_reuse is True
    assert frame.pressure.bounded_pressure_state is True
    assert frame.stale.summary_only is True
    assert frame.retention.bounded_retention_active is True
    assert frame.continuity.bounded_continuity_maintained is True
    assert frame.compact_export.summary_only is True
    assert frame.automatic_rewrite_used is False


def test_pressure_stale_retention_continuity_and_export_are_bounded() -> None:
    pressure = GovernancePressurePrimitive().aggregate(
        retrieval_pressure="medium",
        persistence_pressure="high",
        architecture_pressure="low",
        session_pressure="high",
        checkpoint_pressure="high",
        provider_pressure="low",
        continuity_pressure="medium",
        previous_pressure="low",
    )
    stale = GovernanceStaleDetectionPrimitive().detect(
        ("stale_continuity", "expired_checkpoint", "governance_drift")
    )
    retention = GovernanceBoundedRetentionPrimitive().apply(
        tuple(f"item-{i}" for i in range(7)),
        retention_limit=3,
    )
    continuity = GovernanceContinuityPrimitive().scope(("a", "b", "c", "d"), max_scope_items=2)
    export = GovernanceCompactExportPrimitive().export(("a", "b", "c"), max_items=2)

    assert pressure.aggregated_pressure in {"medium", "high"}
    assert pressure.pressure_direction == "rising"
    assert stale.stale_detected is True
    assert stale.stale_cleanup_recommended is True
    assert retention.retained_items == ("item-4", "item-5", "item-6")
    assert retention.evicted_items == ("item-0", "item-1", "item-2", "item-3")
    assert retention.oldest_first_eviction is True
    assert continuity.continuity_scope == ("a", "b")
    assert continuity.excluded_scope == ("c", "d")
    assert export.bounded_export_maintained is True
    assert export.full_export_used is False


def test_runtime_audit_reports_governance_core_section() -> None:
    from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

    report = run_runtime_enforcement_audit()

    assert report.governance_core.governance_core_active is True
    assert report.governance_core.pressure_primitives_active is True
    assert report.governance_core.stale_detection_primitives_active is True
    assert report.governance_core.bounded_retention_active is True
    assert report.governance_core.continuity_primitives_active is True
    assert report.governance_core.compact_export_primitives_active is True
    assert report.governance_core.estimated_avoided_governance_duplication > 0
    assert report.governance_core.estimated_avoided_runtime_fragmentation > 0
    assert report.governance_core.estimated_avoided_bounded_retention_drift > 0
    assert report.governance_core.human_confirmed_migration is True
    assert report.governance_core.automatic_rewrite_used is False


def test_governance_core_has_no_network_or_autonomous_rewrite() -> None:
    import ai_dev_os.governance_core as root
    import ai_dev_os.governance_core.bounded_retention as retention
    import ai_dev_os.governance_core.compact_export as export
    import ai_dev_os.governance_core.continuity_primitives as continuity
    import ai_dev_os.governance_core.pressure_primitives as pressure
    import ai_dev_os.governance_core.stale_detection as stale

    source = "\n".join(
        inspect.getsource(module)
        for module in (root, pressure, stale, retention, continuity, export)
    ).lower()
    forbidden = (
        "requests",
        "http",
        "subprocess",
        "write_text",
        "unlink(",
        "rename(",
        "git commit",
        "git push",
        "automatic_rewrite_used=True",
    )

    assert all(item not in source for item in forbidden)


def test_vscode_governance_core_commands_views_and_rate_limiting() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}
    view_ids = {item["id"] for item in package["contributes"]["views"]["explorer"]}
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert {
        "aiDevOs.showGovernanceCore",
        "aiDevOs.showSharedPrimitives",
        "aiDevOs.showPrimitiveReuse",
        "aiDevOs.showBoundedRetention",
        "aiDevOs.showCompactExportStatus",
    }.issubset(commands)
    assert {
        "aiDevOsSharedPrimitives",
        "aiDevOsPrimitiveReuse",
        "aiDevOsBoundedRetention",
    }.issubset(view_ids)
    assert "registerTreeDataProvider('aiDevOsSharedPrimitives'" in source
    assert "registerTreeDataProvider('aiDevOsPrimitiveReuse'" in source
    assert "registerTreeDataProvider('aiDevOsBoundedRetention'" in source
    assert "RateLimitedNotifications" in source
    assert "governance-core-reuse-reduction" in source
    assert "automaticRewriteUsed: false" in source
