from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_dev_os.consumer_rollout.compatibility_projection import CompatibilityProjectionPolicy
from ai_dev_os.consumer_rollout.governance_readiness import GovernanceReadinessPolicy
from ai_dev_os.consumer_rollout.migration_friction import MigrationFrictionPolicy
from ai_dev_os.consumer_rollout.rollback_rehearsal import RollbackRehearsalPolicy


@dataclass(frozen=True)
class ConsumerRolloutAuditFrame:
    rollout_ready: bool
    migration_friction: str
    governance_readiness: str
    rollback_ready: bool
    bounded_rollout_confirmed: bool
    install_state_active: bool
    vscode_extension_state_active: bool
    session_lifecycle_compatible: bool
    workspace_persistence_compatible: bool
    governance_runtime_compatible: bool
    runtime_graph_compatible: bool
    bounded_persistence_compatible: bool
    rollback_path_exists: bool
    consumer_name: str
    summary_only: bool = True
    hidden_mutation_used: bool = False
    automatic_migration_used: bool = False


class ConsumerRolloutAuditPolicy:
    def evaluate(
        self,
        consumer_repo: str | Path,
        *,
        platform_repo: str | Path = ".",
        installed_extensions_dir: str | Path | None = None,
    ) -> ConsumerRolloutAuditFrame:
        consumer = Path(consumer_repo)
        platform = Path(platform_repo)
        friction = MigrationFrictionPolicy().evaluate(
            consumer,
            platform_repo=platform,
            installed_extensions_dir=installed_extensions_dir,
        )
        compatibility = CompatibilityProjectionPolicy().evaluate(consumer, platform_repo=platform)
        governance = GovernanceReadinessPolicy().evaluate(consumer, platform_repo=platform)
        rollback = RollbackRehearsalPolicy().evaluate(consumer, platform_repo=platform)
        install_state = (platform / "pyproject.toml").exists() and (
            consumer / "pyproject.toml"
        ).exists()
        extension_state = (platform / "extensions" / "ai-dev-os-vscode" / "package.json").exists()
        session_lifecycle = "missing_session_lifecycle_setup" not in friction.friction_categories
        workspace_persistence = compatibility.persistence_compatibility
        governance_runtime = compatibility.governance_runtime_expectations
        runtime_graph = extension_state and (platform / "ai_dev_os" / "runtime_graph").exists()
        bounded_persistence = (
            compatibility.bounded_retention_support and compatibility.local_only_storage_support
        )
        rollout_ready = (
            install_state
            and extension_state
            and compatibility.bounded_compatibility_confirmed
            and governance.governance_ready
            and rollback.rollback_ready
            and not friction.rollout_blockers
        )
        bounded_confirmed = (
            compatibility.summary_only
            and governance.summary_only
            and rollback.summary_only
            and friction.summary_only
            and not friction.automatic_migration_used
            and not friction.workspace_mutation_used
        )
        return ConsumerRolloutAuditFrame(
            rollout_ready=rollout_ready,
            migration_friction=friction.friction_level,
            governance_readiness="READY" if governance.governance_ready else "TRAINING_REQUIRED",
            rollback_ready=rollback.rollback_ready,
            bounded_rollout_confirmed=bounded_confirmed,
            install_state_active=install_state,
            vscode_extension_state_active=extension_state,
            session_lifecycle_compatible=session_lifecycle,
            workspace_persistence_compatible=workspace_persistence,
            governance_runtime_compatible=governance_runtime,
            runtime_graph_compatible=runtime_graph,
            bounded_persistence_compatible=bounded_persistence,
            rollback_path_exists=rollback.rollback_ready,
            consumer_name=consumer.name,
        )
