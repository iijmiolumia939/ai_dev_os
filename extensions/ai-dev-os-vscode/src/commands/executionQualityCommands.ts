import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ExecutionQualityMonitor,
  ExecutionSignalStableStatusBar,
  QualityBoundedStatusBar,
  QualityDriftSafeStatusBar,
  RedundancyLowStatusBar,
} from '../executionQuality/executionQuality';

export function registerExecutionQualityCommands(
  monitor: ExecutionQualityMonitor,
  qualityBoundedStatus: QualityBoundedStatusBar,
  redundancyLowStatus: RedundancyLowStatusBar,
  qualityDriftSafeStatus: QualityDriftSafeStatusBar,
  executionSignalStableStatus: ExecutionSignalStableStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    qualityBoundedStatus.refresh();
    redundancyLowStatus.refresh();
    qualityDriftSafeStatus.refresh();
    executionSignalStableStatus.refresh();
  };

  const showExecutionQuality = vscode.commands.registerCommand(
    'aiDevOs.showExecutionQuality',
    async () => {
      const state = qualityBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution quality: ${state.qualitySummary}.`,
      );
    },
  );

  const showQualityDrift = vscode.commands.registerCommand(
    'aiDevOs.showQualityDrift',
    async () => {
      const state = qualityDriftSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS quality drift: ${state.driftSummary}.`,
      );
    },
  );

  const showRedundancyPressure = vscode.commands.registerCommand(
    'aiDevOs.showRedundancyPressure',
    async () => {
      const state = redundancyLowStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS redundancy pressure: ${state.redundancySummary}.`,
      );
    },
  );

  const showPersistenceQuality = vscode.commands.registerCommand(
    'aiDevOs.showPersistenceQuality',
    async () => {
      const state = executionSignalStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS persistence quality: ${state.persistenceSummary}.`,
      );
    },
  );

  const compactQualitySummary = vscode.commands.registerCommand(
    'aiDevOs.compactQualitySummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'execution-quality-compact-summary',
        `AI_DEV_OS compact quality summary: ${state.compactQualitySummary}.`,
      );
    },
  );

  return [
    showExecutionQuality,
    showQualityDrift,
    showRedundancyPressure,
    showPersistenceQuality,
    compactQualitySummary,
  ];
}
