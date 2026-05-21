from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("extensions/ai-dev-os-vscode")


def test_extension_commands_are_declared() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in package["contributes"]["commands"]}

    assert {
        "aiDevOs.sessionAudit",
        "aiDevOs.generateHandoff",
        "aiDevOs.copyContinuityBundle",
        "aiDevOs.openNewSessionPrompt",
        "aiDevOs.confirmSessionRollover",
        "aiDevOs.showSessionBoundaryState",
        "aiDevOs.compactCurrentSession",
        "aiDevOs.showStaleSessionWarning",
        "aiDevOs.showReasoningTier",
        "aiDevOs.showCostBudget",
        "aiDevOs.showEscalationPolicy",
        "aiDevOs.showSprintReasoningMap",
        "aiDevOs.compactReasoningScope",
        "aiDevOs.showReasoningScope",
        "aiDevOs.showReasoningDepth",
        "aiDevOs.showPremiumBurnPressure",
        "aiDevOs.showLocalPatchMode",
        "aiDevOs.showEscalationGuard",
        "aiDevOs.toggleCompactReporting",
        "aiDevOs.showVerbosityPressure",
        "aiDevOs.expandCompletionSummary",
        "aiDevOs.showReportDensity",
        "aiDevOs.showRetrievalBudget",
        "aiDevOs.showRetrievalRadius",
        "aiDevOs.showRetrievalPressure",
        "aiDevOs.compactRetrievalScope",
        "aiDevOs.showRetrievalNeighborhood",
        "aiDevOs.showContextDelta",
        "aiDevOs.showIncrementalRetrieval",
        "aiDevOs.showDeltaAudit",
        "aiDevOs.showReplayPressure",
        "aiDevOs.compactIncrementalContext",
        "aiDevOs.showIncrementalRecommendations",
        "aiDevOs.showProviderRouting",
        "aiDevOs.showProviderBudget",
        "aiDevOs.showDowngradeRecommendations",
        "aiDevOs.showProviderDistribution",
        "aiDevOs.compactProviderRouting",
        "aiDevOs.generateSprintPlan",
        "aiDevOs.showSprintLifecycle",
        "aiDevOs.generateNextSprint",
        "aiDevOs.generateSprintBootstrap",
        "aiDevOs.showSprintGovernance",
        "aiDevOs.compactSprintClosure",
        "aiDevOs.showSprintMemory",
        "aiDevOs.showSprintPatterns",
        "aiDevOs.showSprintFailures",
        "aiDevOs.showSprintEfficiency",
        "aiDevOs.compactSprintMemory",
        "aiDevOs.cleanupSprintMemory",
        "aiDevOs.showDevelopmentStrategy",
        "aiDevOs.showCostReductionStrategy",
        "aiDevOs.showGovernanceStabilityStrategy",
        "aiDevOs.showProviderEfficiencyStrategy",
        "aiDevOs.showSprintDensityStrategy",
        "aiDevOs.compactStrategySummary",
        "aiDevOs.showDevelopmentPolicies",
        "aiDevOs.showArchitectureProtection",
        "aiDevOs.showEmbodimentRealismPolicy",
        "aiDevOs.showProviderEscalationPolicy",
        "aiDevOs.showAntiExplosionPolicy",
        "aiDevOs.compactPolicySummary",
    }.issubset(commands)


def test_provider_routing_status_bars_are_declared() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert "AI_DEV_OS PREMIUM_PROVIDER" in source
    assert "AI_DEV_OS DOWNGRADE_READY" in source
    assert "AI_DEV_OS PROVIDER_PRESSURE" in source
    assert "registerProviderRoutingCommands" in source


def test_sprint_dev_loop_status_bars_are_declared() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert "AI_DEV_OS SPRINT_ACTIVE" in source
    assert "AI_DEV_OS ROLLOVER_READY" in source
    assert "AI_DEV_OS SPRINT_PRESSURE" in source
    assert "AI_DEV_OS LOCAL_PATCH_REQUIRED" in source
    assert "registerDevLoopCommands" in source


def test_sprint_memory_status_bars_are_declared() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert "AI_DEV_OS SPRINT_MEMORY" in source
    assert "AI_DEV_OS MEMORY_PRESSURE" in source
    assert "AI_DEV_OS PATTERN_STABLE" in source
    assert "AI_DEV_OS MEMORY_EVICTION" in source
    assert "registerSprintMemoryCommands" in source


def test_development_strategy_status_bars_are_declared() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert "AI_DEV_OS STRATEGY_STABLE" in source
    assert "AI_DEV_OS COST_PRESSURE" in source
    assert "AI_DEV_OS PROVIDER_EFFICIENCY" in source
    assert "AI_DEV_OS ROADMAP_PRESSURE" in source
    assert "registerDevStrategyCommands" in source


def test_development_policy_status_bars_are_declared() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    assert "AI_DEV_OS POLICY_STABLE" in source
    assert "AI_DEV_OS GOVERNANCE_PRESSURE" in source
    assert "AI_DEV_OS ESCALATION_PRESSURE" in source
    assert "AI_DEV_OS REALISM_PROTECTED" in source
    assert "registerDevPolicyCommands" in source


def test_extension_has_local_state_without_telemetry() -> None:
    source = (ROOT / "src" / "state" / "boundaryState.ts").read_text(encoding="utf-8")

    assert "currentSessionGeneration" in source
    assert "lastRolloverTimestamp" in source
    assert "currentEnforcementState" in source
    assert "lastExportedContinuityBundle" in source
    assert "staleWarningCount" in source
    assert "pendingRolloverState" in source
    assert "telemetry" not in source.lower()


def test_extension_notification_rate_limiting() -> None:
    source = (ROOT / "src" / "notifications" / "rateLimitedNotifications.ts").read_text(
        encoding="utf-8"
    )

    assert "minIntervalMs" in source
    assert "return false" in source
    assert "showWarningMessage" in source


def test_extension_no_network_dependency_or_chat_ui_automation() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.ts"))

    forbidden = ("fetch(", "XMLHttpRequest", "https://", "http://", "playwright", "selenium")
    assert all(item not in source for item in forbidden)
    assert "workbench.action.chat.submit" not in source
    assert "workbench.action.chat.acceptInput" not in source
    assert "github.copilot" not in source.lower()


def test_extension_clipboard_and_handoff_support_are_local_only() -> None:
    clipboard = (ROOT / "src" / "clipboard" / "continuityClipboard.ts").read_text(encoding="utf-8")
    handoff = (ROOT / "src" / "handoff" / "handoffClient.ts").read_text(encoding="utf-8")

    assert "vscode.env.clipboard.writeText" in clipboard
    assert "ai_dev_os.cli" in handoff
    assert "execFile" in handoff
    assert "timeout" in handoff
