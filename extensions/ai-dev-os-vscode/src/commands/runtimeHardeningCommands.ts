import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  EscalationStableStatusBar,
  HardeningActiveStatusBar,
  OrchestrationSafeStatusBar,
  RetryStableHardeningStatusBar,
  RuntimeHardeningMonitor,
} from '../runtimeHardening/runtimeHardening';

export function registerRuntimeHardeningCommands(
  monitor: RuntimeHardeningMonitor,
  hardeningActiveStatus: HardeningActiveStatusBar,
  retryStableHardeningStatus: RetryStableHardeningStatusBar,
  orchestrationSafeStatus: OrchestrationSafeStatusBar,
  escalationStableStatus: EscalationStableStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    hardeningActiveStatus.refresh();
    retryStableHardeningStatus.refresh();
    orchestrationSafeStatus.refresh();
    escalationStableStatus.refresh();
  };

  const showRuntimeHardening = vscode.commands.registerCommand(
    'aiDevOs.showRuntimeHardening',
    async () => {
      const state = hardeningActiveStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime hardening: ${state.continuationStabilityScore}.`,
      );
    },
  );

  const showRetryStormStatus = vscode.commands.registerCommand(
    'aiDevOs.showRetryStormStatus',
    async () => {
      const state = retryStableHardeningStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry storm status: ${state.retryStormScore}.`,
      );
    },
  );

  const showEscalationOscillation = vscode.commands.registerCommand(
    'aiDevOs.showEscalationOscillation',
    async () => {
      const state = escalationStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS escalation oscillation: ${state.escalationOscillationScore}.`,
      );
    },
  );

  const showOrchestrationDeadlocks = vscode.commands.registerCommand(
    'aiDevOs.showOrchestrationDeadlocks',
    async () => {
      const state = orchestrationSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS orchestration deadlocks: ${state.orchestrationDeadlockScore}.`,
      );
    },
  );

  const compactRuntimeHardeningSummary = vscode.commands.registerCommand(
    'aiDevOs.compactRuntimeHardeningSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'runtime-hardening-compact-summary',
        `AI_DEV_OS compact runtime hardening: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showRuntimeHardening,
    showRetryStormStatus,
    showEscalationOscillation,
    showOrchestrationDeadlocks,
    compactRuntimeHardeningSummary,
  ];
}
