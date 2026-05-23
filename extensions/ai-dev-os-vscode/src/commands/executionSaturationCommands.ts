import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ContinuationBoundedStatusBar,
  ExecutionSaturationMonitor,
  RetryStableStatusBar,
  SaturationLowStatusBar,
  ToolPressureSafeStatusBar,
} from '../executionSaturation/executionSaturation';

export function registerExecutionSaturationCommands(
  monitor: ExecutionSaturationMonitor,
  saturationLowStatus: SaturationLowStatusBar,
  retryStableStatus: RetryStableStatusBar,
  toolPressureSafeStatus: ToolPressureSafeStatusBar,
  continuationBoundedStatus: ContinuationBoundedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    saturationLowStatus.refresh();
    retryStableStatus.refresh();
    toolPressureSafeStatus.refresh();
    continuationBoundedStatus.refresh();
  };

  const showExecutionSaturation = vscode.commands.registerCommand(
    'aiDevOs.showExecutionSaturation',
    async () => {
      const state = saturationLowStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution saturation: ${state.saturationSummary}.`,
      );
    },
  );

  const showRetryOscillation = vscode.commands.registerCommand(
    'aiDevOs.showRetryOscillation',
    async () => {
      const state = retryStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry oscillation: ${state.retryOscillationSummary}.`,
      );
    },
  );

  const showToolCongestion = vscode.commands.registerCommand(
    'aiDevOs.showToolCongestion',
    async () => {
      const state = toolPressureSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS tool congestion: ${state.toolCongestionSummary}.`,
      );
    },
  );

  const showCheckpointInflation = vscode.commands.registerCommand(
    'aiDevOs.showCheckpointInflation',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS checkpoint inflation: ${state.checkpointInflationSummary}.`,
      );
    },
  );

  const compactSaturationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactSaturationSummary',
    async () => {
      const state = continuationBoundedStatus.refresh();
      await notifications.info(
        'execution-saturation-compact-summary',
        `AI_DEV_OS compact saturation summary: ${state.compactSaturationSummary}.`,
      );
    },
  );

  return [
    showExecutionSaturation,
    showRetryOscillation,
    showToolCongestion,
    showCheckpointInflation,
    compactSaturationSummary,
  ];
}
