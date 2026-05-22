import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  BoundedExecutionStatusBar,
  ContinuationSafeStatusBar,
  ExecutionContinuationMonitor,
  ExecutionContinuingStatusBar,
  LoopGuardedStatusBar,
} from '../executionContinuation/executionContinuation';

export function registerExecutionContinuationCommands(
  monitor: ExecutionContinuationMonitor,
  executionContinuingStatus: ExecutionContinuingStatusBar,
  continuationSafeStatus: ContinuationSafeStatusBar,
  loopGuardedStatus: LoopGuardedStatusBar,
  boundedExecutionStatus: BoundedExecutionStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    executionContinuingStatus.refresh();
    continuationSafeStatus.refresh();
    loopGuardedStatus.refresh();
    boundedExecutionStatus.refresh();
  };

  const continueExecution = vscode.commands.registerCommand('aiDevOs.continueExecution', async () => {
    const state = monitor.continueExecution();
    refreshAll();
    await notifications.info(
      'execution-continuation-continue',
      `AI_DEV_OS continue execution: ${state.continuationSummary}.`,
    );
  });

  const resumeBoundedSprint = vscode.commands.registerCommand(
    'aiDevOs.resumeBoundedSprint',
    async () => {
      const state = monitor.resumeBoundedSprint();
      refreshAll();
      await notifications.info(
        'execution-continuation-resume',
        `AI_DEV_OS bounded sprint resume: ${state.checkpointSummary}.`,
      );
    },
  );

  const showContinuationState = vscode.commands.registerCommand(
    'aiDevOs.showContinuationState',
    async () => {
      const state = continuationSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS continuation state: ${state.continuationSummary}; ${state.terminationSummary}.`,
      );
    },
  );

  const showExecutionBudget = vscode.commands.registerCommand(
    'aiDevOs.showExecutionBudget',
    async () => {
      const state = loopGuardedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution budget: ${state.executionBudgetSummary}; avoided loops ${state.estimatedAvoidedRecursiveLoops}.`,
      );
    },
  );

  const compactContinuationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactContinuationSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS compact continuation summary: ${state.compactContinuationSummary}.`,
      );
    },
  );

  return [
    continueExecution,
    resumeBoundedSprint,
    showContinuationState,
    showExecutionBudget,
    compactContinuationSummary,
  ];
}