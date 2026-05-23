import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ExecutionIntentMonitor,
  ExecutionSemanticsActiveStatusBar,
  IntentStableStatusBar,
  PriorityBoundedStatusBar,
  TransitionsSafeStatusBar,
} from '../executionIntent/executionIntent';

export function registerExecutionIntentCommands(
  monitor: ExecutionIntentMonitor,
  intentStableStatus: IntentStableStatusBar,
  priorityBoundedStatus: PriorityBoundedStatusBar,
  transitionsSafeStatus: TransitionsSafeStatusBar,
  executionSemanticsActiveStatus: ExecutionSemanticsActiveStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    intentStableStatus.refresh();
    priorityBoundedStatus.refresh();
    transitionsSafeStatus.refresh();
    executionSemanticsActiveStatus.refresh();
  };

  const showExecutionIntent = vscode.commands.registerCommand(
    'aiDevOs.showExecutionIntent',
    async () => {
      const state = intentStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution intent: ${state.intentSummary}.`,
      );
    },
  );

  const showIntentPriority = vscode.commands.registerCommand(
    'aiDevOs.showIntentPriority',
    async () => {
      const state = priorityBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS intent priority: ${state.prioritySummary}.`,
      );
    },
  );

  const showIntentConflicts = vscode.commands.registerCommand(
    'aiDevOs.showIntentConflicts',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS intent conflicts: ${state.conflictSummary}.`,
      );
    },
  );

  const showIntentTransitions = vscode.commands.registerCommand(
    'aiDevOs.showIntentTransitions',
    async () => {
      const state = transitionsSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS intent transitions: ${state.transitionSummary}.`,
      );
    },
  );

  const compactIntentSummary = vscode.commands.registerCommand(
    'aiDevOs.compactIntentSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'execution-intent-compact-summary',
        `AI_DEV_OS compact intent summary: ${state.compactIntentSummary}.`,
      );
    },
  );

  return [
    showExecutionIntent,
    showIntentPriority,
    showIntentConflicts,
    showIntentTransitions,
    compactIntentSummary,
  ];
}
