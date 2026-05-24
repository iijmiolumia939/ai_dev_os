import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  BacklogStableStatusBar,
  ContinuationReadyStatusBar,
  DependencyStableStatusBar,
  RegressionVisibleStatusBar,
  SprintContinuationMonitor,
} from '../sprintContinuation/sprintContinuation';

export function registerSprintContinuationCommands(
  monitor: SprintContinuationMonitor,
  continuationStatus: ContinuationReadyStatusBar,
  backlogStatus: BacklogStableStatusBar,
  dependencyStatus: DependencyStableStatusBar,
  regressionStatus: RegressionVisibleStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    continuationStatus.refresh();
    backlogStatus.refresh();
    dependencyStatus.refresh();
    regressionStatus.refresh();
  };

  const showSprintContinuation = vscode.commands.registerCommand(
    'aiDevOs.showSprintContinuation',
    async () => {
      const state = continuationStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS sprint continuation: ${state.continuationSummary.join('; ')}.`,
      );
    },
  );

  const showBacklogContinuation = vscode.commands.registerCommand(
    'aiDevOs.showBacklogContinuation',
    async () => {
      const state = backlogStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS backlog continuation: ${state.backlogSummary.join('; ')}.`,
      );
    },
  );

  const showDependencyContinuation = vscode.commands.registerCommand(
    'aiDevOs.showDependencyContinuation',
    async () => {
      const state = dependencyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS dependency continuation: ${state.dependencySummary.join('; ')}.`,
      );
    },
  );

  const showRegressionCarryover = vscode.commands.registerCommand(
    'aiDevOs.showRegressionCarryover',
    async () => {
      const state = regressionStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS regression carryover: ${state.regressionSummary.join('; ')}.`,
      );
    },
  );

  const compactSprintContinuationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactSprintContinuationSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await notifications.info(
        'sprint-continuation-compacted',
        `AI_DEV_OS sprint continuation compacted; pressure ${state.continuationPressure}.`,
      );
    },
  );

  return [
    showSprintContinuation,
    showBacklogContinuation,
    showDependencyContinuation,
    showRegressionCarryover,
    compactSprintContinuationSummary,
  ];
}