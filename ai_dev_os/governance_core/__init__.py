from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.governance_core.bounded_retention import (
    GovernanceBoundedRetentionFrame,
    GovernanceBoundedRetentionPrimitive,
)
from ai_dev_os.governance_core.compact_export import (
    GovernanceCompactExportFrame,
    GovernanceCompactExportPrimitive,
)
from ai_dev_os.governance_core.continuity_primitives import (
    GovernanceContinuityPrimitive,
    GovernanceContinuityPrimitiveFrame,
)
from ai_dev_os.governance_core.pressure_primitives import (
    GovernancePressurePrimitive,
    GovernancePressurePrimitiveFrame,
)
from ai_dev_os.governance_core.stale_detection import (
    GovernanceStaleDetectionFrame,
    GovernanceStaleDetectionPrimitive,
)


@dataclass(frozen=True)
class GovernanceCoreFrame:
    pressure: GovernancePressurePrimitiveFrame
    stale: GovernanceStaleDetectionFrame
    retention: GovernanceBoundedRetentionFrame
    continuity: GovernanceContinuityPrimitiveFrame
    compact_export: GovernanceCompactExportFrame
    governance_core_active: bool
    bounded_governance_reuse: bool
    local_only_architecture_cognition: bool
    automatic_rewrite_used: bool


class GovernanceCorePolicy:
    def evaluate(self) -> GovernanceCoreFrame:
        pressure = GovernancePressurePrimitive().aggregate(
            retrieval_pressure="medium",
            persistence_pressure="high",
            architecture_pressure="medium",
            session_pressure="high",
            checkpoint_pressure="high",
            provider_pressure="low",
            continuity_pressure="high",
        )
        stale = GovernanceStaleDetectionPrimitive().detect(
            (
                "stale_continuity",
                "stale_persistence",
                "expired_checkpoint",
                "old_sprint",
                "governance_drift",
                "retrieval_drift",
            )
        )
        retention = GovernanceBoundedRetentionPrimitive().apply(
            tuple(f"governance-item-{index}" for index in range(8)),
            retention_limit=5,
        )
        continuity = GovernanceContinuityPrimitive().scope(
            (
                "compact_continuity_bundle",
                "session_continuity",
                "sprint_continuity",
                "repository_subset_continuity",
                "architecture_continuity",
                "full_history_excluded",
            )
        )
        compact = GovernanceCompactExportPrimitive().export(
            (
                "continuity export",
                "governance dashboard export",
                "incident export",
                "runtime graph export",
                "simplification recommendation export",
            ),
            export_mode="copy_ready",
        )
        return GovernanceCoreFrame(
            pressure=pressure,
            stale=stale,
            retention=retention,
            continuity=continuity,
            compact_export=compact,
            governance_core_active=True,
            bounded_governance_reuse=True,
            local_only_architecture_cognition=True,
            automatic_rewrite_used=False,
        )
