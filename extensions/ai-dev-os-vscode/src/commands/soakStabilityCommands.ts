import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  DriftBoundedStatusBar,
  EntropyVisibleStatusBar,
  LongSessionSafeStatusBar,
  SoakStabilityMonitor,
  SoakStableStatusBar,
} from '../soakStability/soakStability';

export function registerSoakStabilityCommands(
  monitor: SoakStabilityMonitor,
  soakStableStatus: SoakStableStatusBar,
  driftBoundedStatus: DriftBoundedStatusBar,
  entropyVisibleStatus: EntropyVisibleStatusBar,
  longSessionSafeStatus: LongSessionSafeStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    soakStableStatus.refresh();
    driftBoundedStatus.refresh();
    entropyVisibleStatus.refresh();
    longSessionSafeStatus.refresh();
  };

  const showSoakStability = vscode.commands.registerCommand(
    'aiDevOs.showSoakStability',
    async () => {
      const state = soakStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS soak stability: ${state.soakStabilityActive}.`,
      );
    },
  );

  const showLongSessionDrift = vscode.commands.registerCommand(
    'aiDevOs.showLongSessionDrift',
    async () => {
      const state = driftBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS long session stability: ${state.longSessionStabilityScore}.`,
      );
    },
  );

  const showRetryAccumulation = vscode.commands.registerCommand(
    'aiDevOs.showRetryAccumulation',
    async () => {
      const state = longSessionSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry accumulation: ${state.retryAccumulationScore}.`,
      );
    },
  );

  const showRuntimeEntropy = vscode.commands.registerCommand(
    'aiDevOs.showRuntimeEntropy',
    async () => {
      const state = entropyVisibleStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime entropy: ${state.runtimeInteractionEntropyScore}.`,
      );
    },
  );

  const compactSoakStabilitySummary = vscode.commands.registerCommand(
    'aiDevOs.compactSoakStabilitySummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'soak-stability-compact-summary',
        `AI_DEV_OS compact soak stability: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showSoakStability,
    showLongSessionDrift,
    showRetryAccumulation,
    showRuntimeEntropy,
    compactSoakStabilitySummary,
  ];
}
