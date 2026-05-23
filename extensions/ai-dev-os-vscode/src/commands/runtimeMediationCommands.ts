import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  CooldownStableStatusBar,
  ExecutionBoundedStatusBar,
  MediationActiveStatusBar,
  RetryGovernedStatusBar,
  RuntimeMediationMonitor,
} from '../runtimeMediation/runtimeMediation';

export function registerRuntimeMediationCommands(
  monitor: RuntimeMediationMonitor,
  mediationActiveStatus: MediationActiveStatusBar,
  executionBoundedStatus: ExecutionBoundedStatusBar,
  retryGovernedStatus: RetryGovernedStatusBar,
  cooldownStableStatus: CooldownStableStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    mediationActiveStatus.refresh();
    executionBoundedStatus.refresh();
    retryGovernedStatus.refresh();
    cooldownStableStatus.refresh();
  };

  const showRuntimeMediation = vscode.commands.registerCommand(
    'aiDevOs.showRuntimeMediation',
    async () => {
      const state = mediationActiveStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime mediation: ${state.mediationSummary}.`,
      );
    },
  );

  const showExecutionQueue = vscode.commands.registerCommand(
    'aiDevOs.showExecutionQueue',
    async () => {
      const state = executionBoundedStatus.refresh();
      await vscode.window.showInformationMessage(`AI_DEV_OS execution queue: ${state.queueSummary}.`);
    },
  );

  const showRetryGovernance = vscode.commands.registerCommand(
    'aiDevOs.showRetryGovernance',
    async () => {
      const state = retryGovernedStatus.refresh();
      await vscode.window.showInformationMessage(`AI_DEV_OS retry governance: ${state.retrySummary}.`);
    },
  );

  const showCooldownGovernance = vscode.commands.registerCommand(
    'aiDevOs.showCooldownGovernance',
    async () => {
      const state = cooldownStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS cooldown governance: ${state.cooldownSummary}.`,
      );
    },
  );

  const compactRuntimeMediationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactRuntimeMediationSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'runtime-mediation-compact-summary',
        `AI_DEV_OS compact runtime mediation summary: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showRuntimeMediation,
    showExecutionQueue,
    showRetryGovernance,
    showCooldownGovernance,
    compactRuntimeMediationSummary,
  ];
}