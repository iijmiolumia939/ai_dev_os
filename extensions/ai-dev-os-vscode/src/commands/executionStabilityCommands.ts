import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  DriftLowStatusBar,
  ExecutionStabilityMonitor,
  OscillationStableStatusBar,
  PersistenceSafeStatusBar,
  StabilityBoundedStatusBar,
} from '../executionStability/executionStability';

export function registerExecutionStabilityCommands(
  monitor: ExecutionStabilityMonitor,
  stabilityBoundedStatus: StabilityBoundedStatusBar,
  driftLowStatus: DriftLowStatusBar,
  oscillationStableStatus: OscillationStableStatusBar,
  persistenceSafeStatus: PersistenceSafeStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    stabilityBoundedStatus.refresh();
    driftLowStatus.refresh();
    oscillationStableStatus.refresh();
    persistenceSafeStatus.refresh();
  };

  const showExecutionStability = vscode.commands.registerCommand(
    'aiDevOs.showExecutionStabilityRuntime',
    async () => {
      const state = stabilityBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution stability: ${state.stabilitySummary}.`,
      );
    },
  );

  const showStabilityDrift = vscode.commands.registerCommand(
    'aiDevOs.showStabilityDrift',
    async () => {
      const state = driftLowStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS stability drift: ${state.driftSummary}.`,
      );
    },
  );

  const showStabilityOscillation = vscode.commands.registerCommand(
    'aiDevOs.showStabilityOscillation',
    async () => {
      const state = oscillationStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS stability oscillation: ${state.oscillationSummary}.`,
      );
    },
  );

  const showPersistenceStability = vscode.commands.registerCommand(
    'aiDevOs.showPersistenceStability',
    async () => {
      const state = persistenceSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS persistence stability: ${state.persistenceSummary}.`,
      );
    },
  );

  const compactStabilitySummary = vscode.commands.registerCommand(
    'aiDevOs.compactStabilitySummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'execution-stability-compact-summary',
        `AI_DEV_OS compact stability summary: ${state.compactStabilitySummary}.`,
      );
    },
  );

  return [
    showExecutionStability,
    showStabilityDrift,
    showStabilityOscillation,
    showPersistenceStability,
    compactStabilitySummary,
  ];
}
