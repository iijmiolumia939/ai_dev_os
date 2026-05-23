import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ConflictsBoundedStatusBar,
  CoordinationGuardedStatusBar,
  CoordinationStableStatusBar,
  ExecutionCoordinationMonitor,
  RuntimePrioritySafeStatusBar,
} from '../executionCoordination/executionCoordination';

export function registerExecutionCoordinationCommands(
  monitor: ExecutionCoordinationMonitor,
  coordinationStableStatus: CoordinationStableStatusBar,
  conflictsBoundedStatus: ConflictsBoundedStatusBar,
  runtimePrioritySafeStatus: RuntimePrioritySafeStatusBar,
  coordinationGuardedStatus: CoordinationGuardedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    coordinationStableStatus.refresh();
    conflictsBoundedStatus.refresh();
    runtimePrioritySafeStatus.refresh();
    coordinationGuardedStatus.refresh();
  };

  const showRuntimeCoordination = vscode.commands.registerCommand(
    'aiDevOs.showRuntimeCoordination',
    async () => {
      const state = coordinationStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime coordination: ${state.coordinationSummary}.`,
      );
    },
  );

  const showCoordinationConflicts = vscode.commands.registerCommand(
    'aiDevOs.showCoordinationConflicts',
    async () => {
      const state = conflictsBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS coordination conflicts: ${state.conflictSummary}.`,
      );
    },
  );

  const showRuntimePriorities = vscode.commands.registerCommand(
    'aiDevOs.showRuntimePriorities',
    async () => {
      const state = runtimePrioritySafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime priorities: ${state.prioritySummary}.`,
      );
    },
  );

  const showCoordinationCooldown = vscode.commands.registerCommand(
    'aiDevOs.showCoordinationCooldown',
    async () => {
      const state = coordinationGuardedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS coordination cooldown: ${state.cooldownSummary}.`,
      );
    },
  );

  const compactCoordinationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactCoordinationSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'execution-coordination-compact-summary',
        `AI_DEV_OS compact coordination summary: ${state.compactCoordinationSummary}.`,
      );
    },
  );

  return [
    showRuntimeCoordination,
    showCoordinationConflicts,
    showRuntimePriorities,
    showCoordinationCooldown,
    compactCoordinationSummary,
  ];
}
