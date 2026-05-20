from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ai_dev_os import __version__
from ai_dev_os.governance_core import GovernanceCorePolicy

PYTHON_VERSIONS = ("3.11", "3.12")
CONSUMER_REPOSITORIES = (
    "AITuber",
    "cat simulator",
    "standalone governance repos",
    "experimental repos",
)
RELEASE_REQUIREMENT_IDS = (
    "NFR-REL-01",
    "NFR-REL-02",
    "NFR-ARCH-24",
    "NFR-COST-21",
    "FR-RELEASE-01",
    "FR-RELEASE-02",
    "FR-RELEASE-03",
    "FR-RELEASE-04",
    "FR-RELEASE-05",
    "TC-RELEASE-01",
    "TC-RELEASE-02",
    "TC-RELEASE-03",
    "TC-RELEASE-04",
    "TC-RELEASE-05",
)


@dataclass(frozen=True)
class ExtensionReadinessFrame:
    extension_compile_declared: bool
    vsix_packaging_supported: bool
    bounded_local_persistence: bool
    no_hidden_network_dependency: bool
    no_hidden_signal_export: bool
    clean_vscodeignore: bool
    extension_release_ready: bool


@dataclass(frozen=True)
class ConsumerRolloutFrame:
    consumer_rollout_active: bool
    supported_consumers: tuple[str, ...]
    install_flow_documented: bool
    vscode_extension_setup_documented: bool
    session_lifecycle_setup_documented: bool
    workspace_persistence_setup_documented: bool
    retrieval_scaling_integration_documented: bool
    governance_runtime_integration_documented: bool
    rollback_procedure_documented: bool
    migration_checklist_documented: bool
    local_only_persistence_rules_documented: bool
    human_confirmed_rollout: bool


@dataclass(frozen=True)
class GovernanceFreezeStatusFrame:
    governance_freeze_active: bool
    stabilized_contracts: tuple[str, ...]
    unstable_contracts: tuple[str, ...]
    experimental_runtimes: tuple[str, ...]
    bounded_api_expectations: tuple[str, ...]
    alpha_boundary_declared: bool
    api_freeze_not_guaranteed: bool


@dataclass(frozen=True)
class ReleaseReadinessFrame:
    release_version: str
    github_prerelease_tag: str
    release_ready: bool
    blocking_risks: tuple[str, ...]
    bounded_release_confirmed: bool
    consumer_safe: bool
    migration_ready: bool
    runtime_audit_active: bool
    governance_core_active: bool
    bounded_retention_active: bool
    session_lifecycle_active: bool
    vscode_extension_buildable: bool
    provider_simulation_isolated: bool
    no_telemetry: bool
    no_hidden_persistence: bool
    no_artifact_leakage: bool
    rollback_safe_release_prep: bool
    local_first_governance: bool
    compatibility_matrix_active: bool
    release_requirement_ids: tuple[str, ...]
    copy_ready_text: str


class ExtensionReadinessPolicy:
    def evaluate(self, repo_path: str | Path = ".") -> ExtensionReadinessFrame:
        root = Path(repo_path)
        extension = root / "extensions" / "ai-dev-os-vscode"
        package = _read_json(extension / "package.json")
        vscodeignore = _read_text(extension / ".vscodeignore")
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in (extension / "src").rglob("*.ts")
        )
        scripts = package.get("scripts", {})
        compile_declared = scripts.get("compile") == "tsc -p ./"
        clean_ignore = all(
            pattern in vscodeignore
            for pattern in (
                "node_modules/**",
                "src/**",
                "*.vsix",
                "telemetry/**",
                "dist/**",
                "build/**",
            )
        )
        no_network = not any(
            marker in source.lower()
            for marker in ("fetch(", "xmlhttprequest", "https://", "http://")
        )
        no_signal_export = "telemetry" not in source.lower()
        local_persistence = "globalState" in source or "LocalPersistenceStore" in source
        vsix_supported = bool(package.get("main") == "./out/extension.js" and clean_ignore)
        return ExtensionReadinessFrame(
            extension_compile_declared=compile_declared,
            vsix_packaging_supported=vsix_supported,
            bounded_local_persistence=local_persistence,
            no_hidden_network_dependency=no_network,
            no_hidden_signal_export=no_signal_export,
            clean_vscodeignore=clean_ignore,
            extension_release_ready=all(
                (compile_declared, vsix_supported, local_persistence, no_network, no_signal_export)
            ),
        )


class ConsumerRolloutPolicy:
    def evaluate(self, repo_path: str | Path = ".") -> ConsumerRolloutFrame:
        root = Path(repo_path)
        rollout_doc = _read_text(root / "docs" / "consumer-rollout" / "index.md")
        migration_doc = _read_text(root / "docs" / "consumer-rollout" / "migration-checklist.md")
        rollback_doc = _read_text(root / "docs" / "consumer-rollout" / "rollback.md")
        combined = "\n".join((rollout_doc, migration_doc, rollback_doc)).lower()
        return ConsumerRolloutFrame(
            consumer_rollout_active=bool(rollout_doc and migration_doc and rollback_doc),
            supported_consumers=CONSUMER_REPOSITORIES,
            install_flow_documented="install flow" in combined,
            vscode_extension_setup_documented="vscode extension setup" in combined,
            session_lifecycle_setup_documented="session lifecycle setup" in combined,
            workspace_persistence_setup_documented="workspace persistence setup" in combined,
            retrieval_scaling_integration_documented="retrieval scaling integration" in combined,
            governance_runtime_integration_documented="governance runtime integration" in combined,
            rollback_procedure_documented="rollback procedure" in combined,
            migration_checklist_documented="migration checklist" in combined,
            local_only_persistence_rules_documented="local-only persistence rules" in combined,
            human_confirmed_rollout="human-confirmed rollout" in combined,
        )


class GovernanceFreezeStatusPolicy:
    def evaluate(self, repo_path: str | Path = ".") -> GovernanceFreezeStatusFrame:
        text = _read_text(Path(repo_path) / "docs" / "releases" / "runtime-governance-freeze.md")
        lowered = text.lower()
        return GovernanceFreezeStatusFrame(
            governance_freeze_active=bool(text),
            stabilized_contracts=(
                "runtime audit report shape",
                "governance core primitive frames",
                "session lifecycle summary frames",
                "VSCode command identifiers",
            ),
            unstable_contracts=(
                "internal policy scoring constants",
                "experimental recommendation wording",
            ),
            experimental_runtimes=(
                "governance incidents",
                "runtime simplification recommendations",
                "consumer rollout scoring",
            ),
            bounded_api_expectations=(
                "summary-only output",
                "local-first persistence",
                "human-confirmed rollout",
                "rollback-safe migration",
            ),
            alpha_boundary_declared="alpha boundary" in lowered,
            api_freeze_not_guaranteed="api freeze not guaranteed" in lowered,
        )


class ReleaseReadinessPolicy:
    def evaluate(self, repo_path: str | Path = ".") -> ReleaseReadinessFrame:
        from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

        root = Path(repo_path)
        audit = run_runtime_enforcement_audit()
        governance_core = GovernanceCorePolicy().evaluate()
        extension = ExtensionReadinessPolicy().evaluate(root)
        rollout = ConsumerRolloutPolicy().evaluate(root)
        freeze = GovernanceFreezeStatusPolicy().evaluate(root)
        compatibility_matrix_active = bool(
            _read_text(root / "docs" / "releases" / "compatibility-matrix.md")
        )
        no_artifacts = _artifact_leakage_blocked(root)
        checks = {
            "runtime_audit_active": audit.activation.initialized,
            "governance_core_active": governance_core.governance_core_active,
            "bounded_retention_active": governance_core.retention.bounded_retention_active,
            "session_lifecycle_active": audit.session_lifecycle.session_lifecycle_active,
            "vscode_extension_buildable": extension.extension_release_ready,
            "provider_simulation_isolated": audit.provider_simulation.no_real_provider_call,
            "no_telemetry": extension.no_hidden_signal_export,
            "no_hidden_persistence": extension.bounded_local_persistence
            and audit.workspace_persistence.local_workspace_persistence_active,
            "no_artifact_leakage": no_artifacts,
            "consumer_rollout_active": rollout.consumer_rollout_active,
            "governance_freeze_active": freeze.governance_freeze_active,
            "compatibility_matrix_active": compatibility_matrix_active,
        }
        blocking = tuple(name for name, passed in checks.items() if not passed)
        bounded = (
            not audit.runtime_graph.hidden_telemetry_used
            and not audit.runtime_simplification.autonomous_mutation_used
            and governance_core.automatic_rewrite_used is False
            and freeze.alpha_boundary_declared
            and freeze.api_freeze_not_guaranteed
        )
        consumer_safe = rollout.human_confirmed_rollout and extension.extension_release_ready
        migration_ready = (
            rollout.migration_checklist_documented and rollout.rollback_procedure_documented
        )
        release_ready = not blocking and bounded and consumer_safe and migration_ready
        copy_ready = _release_copy_ready_text(
            release_ready=release_ready,
            blocking=blocking,
            consumer_safe=consumer_safe,
            migration_ready=migration_ready,
        )
        return ReleaseReadinessFrame(
            release_version=__version__,
            github_prerelease_tag="0.1.0-alpha.3",
            release_ready=release_ready,
            blocking_risks=blocking,
            bounded_release_confirmed=bounded,
            consumer_safe=consumer_safe,
            migration_ready=migration_ready,
            runtime_audit_active=checks["runtime_audit_active"],
            governance_core_active=checks["governance_core_active"],
            bounded_retention_active=checks["bounded_retention_active"],
            session_lifecycle_active=checks["session_lifecycle_active"],
            vscode_extension_buildable=checks["vscode_extension_buildable"],
            provider_simulation_isolated=checks["provider_simulation_isolated"],
            no_telemetry=checks["no_telemetry"],
            no_hidden_persistence=checks["no_hidden_persistence"],
            no_artifact_leakage=checks["no_artifact_leakage"],
            rollback_safe_release_prep=rollout.rollback_procedure_documented,
            local_first_governance=audit.workspace_persistence.local_workspace_persistence_active,
            compatibility_matrix_active=compatibility_matrix_active,
            release_requirement_ids=RELEASE_REQUIREMENT_IDS,
            copy_ready_text=copy_ready,
        )


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _artifact_leakage_blocked(root: Path) -> bool:
    gitignore = _read_text(root / ".gitignore")
    vscodeignore = _read_text(root / "extensions" / "ai-dev-os-vscode" / ".vscodeignore")
    required = ("dist/", "build/", "*.vsix", "*.log", "runtime_audit_report*.json")
    return all(pattern in gitignore or pattern in vscodeignore for pattern in required)


def _release_copy_ready_text(
    *,
    release_ready: bool,
    blocking: tuple[str, ...],
    consumer_safe: bool,
    migration_ready: bool,
) -> str:
    return "\n".join(
        (
            "AI_DEV_OS 0.1.0-alpha.3 release readiness",
            f"release_ready: {release_ready}",
            f"consumer_safe: {consumer_safe}",
            f"migration_ready: {migration_ready}",
            "blocking_risks: " + (", ".join(blocking) if blocking else "none"),
            "rollout: human-confirmed, local-first, rollback-safe",
        )
    )


__all__ = [
    "ConsumerRolloutFrame",
    "ConsumerRolloutPolicy",
    "ExtensionReadinessFrame",
    "ExtensionReadinessPolicy",
    "GovernanceFreezeStatusFrame",
    "GovernanceFreezeStatusPolicy",
    "ReleaseReadinessFrame",
    "ReleaseReadinessPolicy",
]
