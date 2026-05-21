import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  CheckpointReadyStatusBar,
  DevExecutionMonitor,
  ExecutionActiveStatusBar,
  RollbackSafeStatusBar,
  ValidationStableStatusBar,
} from '../devExecution/devExecution';

export function registerDevExecutionCommands(
  monitor: DevExecutionMonitor,
  executionStatus: ExecutionActiveStatusBar,
  checkpointStatus: CheckpointReadyStatusBar,
  validationStatus: ValidationStableStatusBar,
  rollbackStatus: RollbackSafeStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    executionStatus.refresh();
    checkpointStatus.refresh();
    validationStatus.refresh();
    rollbackStatus.refresh();
  };

  const generateExecutionPlan = vscode.commands.registerCommand(
    'aiDevOs.generateExecutionPlan',
    async () => {
      const state = executionStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution plan: ${state.executionPlan.join('; ')}.`,
      );
    },
  );

  const showExecutionCheckpoints = vscode.commands.registerCommand(
    'aiDevOs.showExecutionCheckpoints',
    async () => {
      const state = checkpointStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution checkpoints: ${state.checkpointHints.join('; ')}.`,
      );
    },
  );

  const showValidationSequence = vscode.commands.registerCommand(
    'aiDevOs.showValidationSequence',
    async () => {
      const state = validationStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS validation sequence: ${state.validationSequence.join('; ')}.`,
      );
    },
  );

  const showRollbackGuidance = vscode.commands.registerCommand(
    'aiDevOs.showRollbackGuidance',
    async () => {
      const state = rollbackStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS rollback guidance: ${state.rollbackGuidance.join('; ')}.`,
      );
    },
  );

  const showExecutionStability = vscode.commands.registerCommand(
    'aiDevOs.showExecutionStability',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution stability: validation ${state.validationStable}; rollback ${state.rollbackSafe}; pressure ${state.executionPressure}.`,
      );
    },
  );

  const compactExecutionSummary = vscode.commands.registerCommand(
    'aiDevOs.compactExecutionSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await notifications.info(
        'development-execution-compacted',
        `AI_DEV_OS execution summary compacted; execution pressure ${state.executionPressure}.`,
      );
    },
  );

  return [
    generateExecutionPlan,
    showExecutionCheckpoints,
    showValidationSequence,
    showRollbackGuidance,
    showExecutionStability,
    compactExecutionSummary,
  ];
}