import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ExecutionSessionMonitor,
  LifecycleBoundedStatusBar,
  PersistenceGuardedStatusBar,
  SessionIntegritySafeStatusBar,
  SessionStableStatusBar,
} from '../executionSession/executionSession';

export function registerExecutionSessionCommands(
  monitor: ExecutionSessionMonitor,
  sessionStableStatus: SessionStableStatusBar,
  lifecycleBoundedStatus: LifecycleBoundedStatusBar,
  sessionIntegritySafeStatus: SessionIntegritySafeStatusBar,
  persistenceGuardedStatus: PersistenceGuardedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    sessionStableStatus.refresh();
    lifecycleBoundedStatus.refresh();
    sessionIntegritySafeStatus.refresh();
    persistenceGuardedStatus.refresh();
  };

  const showExecutionSessions = vscode.commands.registerCommand(
    'aiDevOs.showExecutionSessions',
    async () => {
      const state = sessionStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution sessions: ${state.sessionSummary}.`,
      );
    },
  );

  const showSessionLifecycle = vscode.commands.registerCommand(
    'aiDevOs.showSessionLifecycle',
    async () => {
      const state = lifecycleBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS session lifecycle: ${state.lifecycleSummary}.`,
      );
    },
  );

  const showSessionIntegrity = vscode.commands.registerCommand(
    'aiDevOs.showSessionIntegrity',
    async () => {
      const state = sessionIntegritySafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS session integrity: ${state.integritySummary}.`,
      );
    },
  );

  const showSessionConflicts = vscode.commands.registerCommand(
    'aiDevOs.showSessionConflicts',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS session conflicts: ${state.conflictSummary}.`,
      );
    },
  );

  const compactSessionSummary = vscode.commands.registerCommand(
    'aiDevOs.compactSessionSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'execution-session-compact-summary',
        `AI_DEV_OS compact session summary: ${state.compactSessionSummary}.`,
      );
    },
  );

  return [
    showExecutionSessions,
    showSessionLifecycle,
    showSessionIntegrity,
    showSessionConflicts,
    compactSessionSummary,
  ];
}
