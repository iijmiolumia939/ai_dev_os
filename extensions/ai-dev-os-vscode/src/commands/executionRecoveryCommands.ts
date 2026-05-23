import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  CheckpointValidStatusBar,
  ExecutionRecoveryMonitor,
  RecoveryCooldownStatusBar,
  RecoverySafeStatusBar,
  RollbackBoundedStatusBar,
} from '../executionRecovery/executionRecovery';

export function registerExecutionRecoveryCommands(
  monitor: ExecutionRecoveryMonitor,
  recoverySafeStatus: RecoverySafeStatusBar,
  checkpointValidStatus: CheckpointValidStatusBar,
  recoveryCooldownStatus: RecoveryCooldownStatusBar,
  rollbackBoundedStatus: RollbackBoundedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    recoverySafeStatus.refresh();
    checkpointValidStatus.refresh();
    recoveryCooldownStatus.refresh();
    rollbackBoundedStatus.refresh();
  };

  const showRecoveryState = vscode.commands.registerCommand(
    'aiDevOs.showRecoveryState',
    async () => {
      const state = recoverySafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS recovery state: ${state.recoverySummary}.`,
      );
    },
  );

  const showRecoveryCooldown = vscode.commands.registerCommand(
    'aiDevOs.showRecoveryCooldown',
    async () => {
      const state = recoveryCooldownStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS recovery cooldown: ${state.cooldownSummary}.`,
      );
    },
  );

  const showCheckpointIntegrity = vscode.commands.registerCommand(
    'aiDevOs.showCheckpointIntegrity',
    async () => {
      const state = checkpointValidStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS checkpoint integrity: ${state.checkpointIntegritySummary}.`,
      );
    },
  );

  const resumeSafeRecovery = vscode.commands.registerCommand(
    'aiDevOs.resumeSafeRecovery',
    async () => {
      const state = monitor.resumeSafeRecovery();
      refreshAll();
      await notifications.info(
        'execution-recovery-safe-resume',
        `AI_DEV_OS safe recovery resume: ${state.recoveryRecommendation}.`,
      );
    },
  );

  const compactRecoverySummary = vscode.commands.registerCommand(
    'aiDevOs.compactRecoverySummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS compact recovery summary: ${state.compactRecoverySummary}.`,
      );
    },
  );

  return [
    showRecoveryState,
    showRecoveryCooldown,
    showCheckpointIntegrity,
    resumeSafeRecovery,
    compactRecoverySummary,
  ];
}
