import * as vscode from 'vscode';
import {
  CommitReadyStatusBar,
  RegressionTrackedStatusBar,
  SprintBoundedStatusBar,
  SprintLoopMonitor,
  SprintValidationStableStatusBar,
} from '../sprintLoop/sprintLoop';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerSprintLoopCommands(
  monitor: SprintLoopMonitor,
  sprintBoundedStatus: SprintBoundedStatusBar,
  validationStableStatus: SprintValidationStableStatusBar,
  regressionTrackedStatus: RegressionTrackedStatusBar,
  commitReadyStatus: CommitReadyStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    sprintBoundedStatus.refresh();
    validationStableStatus.refresh();
    regressionTrackedStatus.refresh();
    commitReadyStatus.refresh();
  };

  const showSprintLoop = vscode.commands.registerCommand(
    'aiDevOs.showSprintLoop',
    async () => {
      const state = sprintBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS sprint loop: continuation ${state.sprintContinuationScore}.`,
      );
    },
  );

  const showSprintValidation = vscode.commands.registerCommand(
    'aiDevOs.showSprintValidation',
    async () => {
      const state = validationStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS sprint validation: ${state.sprintValidationScore}.`,
      );
    },
  );

  const showSprintRegression = vscode.commands.registerCommand(
    'aiDevOs.showSprintRegression',
    async () => {
      const state = regressionTrackedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS sprint regression: ${state.sprintRegressionScore}.`,
      );
    },
  );

  const showSprintCommitReadiness = vscode.commands.registerCommand(
    'aiDevOs.showSprintCommitReadiness',
    async () => {
      const state = commitReadyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS sprint commit readiness: ${state.sprintCommitReadinessScore}.`,
      );
    },
  );

  const compactSprintLoopSummary = vscode.commands.registerCommand(
    'aiDevOs.compactSprintLoopSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'sprint-loop-compact-summary',
        `AI_DEV_OS compact sprint loop: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showSprintLoop,
    showSprintValidation,
    showSprintRegression,
    showSprintCommitReadiness,
    compactSprintLoopSummary,
  ];
}
