import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  FailureInjectionMonitor,
  FailureTestingStatusBar,
  OrchestrationResilientStatusBar,
  RecoveryStableStatusBar,
  RetryResilientStatusBar,
} from '../failureInjection/failureInjection';

export function registerFailureInjectionCommands(
  monitor: FailureInjectionMonitor,
  failureTestingStatus: FailureTestingStatusBar,
  recoveryStableStatus: RecoveryStableStatusBar,
  retryResilientStatus: RetryResilientStatusBar,
  orchestrationResilientStatus: OrchestrationResilientStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    failureTestingStatus.refresh();
    recoveryStableStatus.refresh();
    retryResilientStatus.refresh();
    orchestrationResilientStatus.refresh();
  };

  const showFailureInjection = vscode.commands.registerCommand(
    'aiDevOs.showFailureInjection',
    async () => {
      const state = failureTestingStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS failure injection: ${state.failureInjectionActive}.`,
      );
    },
  );

  const showRetryInjection = vscode.commands.registerCommand(
    'aiDevOs.showRetryInjection',
    async () => {
      const state = retryResilientStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry injection: ${state.retryInjectionScore}.`,
      );
    },
  );

  const showProviderInjection = vscode.commands.registerCommand(
    'aiDevOs.showProviderInjection',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider injection: ${state.providerInjectionScore}.`,
      );
    },
  );

  const showRecoveryResilience = vscode.commands.registerCommand(
    'aiDevOs.showRecoveryResilience',
    async () => {
      const state = recoveryStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS recovery resilience: ${state.recoveryResilienceScore}.`,
      );
    },
  );

  const compactFailureInjectionSummary = vscode.commands.registerCommand(
    'aiDevOs.compactFailureInjectionSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'failure-injection-compact-summary',
        `AI_DEV_OS compact failure injection: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showFailureInjection,
    showRetryInjection,
    showProviderInjection,
    showRecoveryResilience,
    compactFailureInjectionSummary,
  ];
}
