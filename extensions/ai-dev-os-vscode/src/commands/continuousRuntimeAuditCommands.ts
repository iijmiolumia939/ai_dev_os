import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ContinuousRuntimeAuditMonitor,
  ContinuousRuntimeHealthStatusBar,
  OrchestrationVisibleStatusBar,
  ProviderVisibleStatusBar,
  RetryVisibleStatusBar,
} from '../continuousRuntimeAudit/continuousRuntimeAudit';

export function registerContinuousRuntimeAuditCommands(
  monitor: ContinuousRuntimeAuditMonitor,
  runtimeHealthStatus: ContinuousRuntimeHealthStatusBar,
  retryVisibleStatus: RetryVisibleStatusBar,
  orchestrationVisibleStatus: OrchestrationVisibleStatusBar,
  providerVisibleStatus: ProviderVisibleStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    runtimeHealthStatus.refresh();
    retryVisibleStatus.refresh();
    orchestrationVisibleStatus.refresh();
    providerVisibleStatus.refresh();
  };

  const showRuntimeHealth = vscode.commands.registerCommand(
    'aiDevOs.showRuntimeHealth',
    async () => {
      const state = runtimeHealthStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime health: ${state.runtimeHealthScore}.`,
      );
    },
  );

  const showRetryPressure = vscode.commands.registerCommand(
    'aiDevOs.showRetryPressure',
    async () => {
      const state = retryVisibleStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry pressure: ${state.retryPressureScore}.`,
      );
    },
  );

  const showProviderFatigue = vscode.commands.registerCommand(
    'aiDevOs.showContinuousProviderFatigue',
    async () => {
      const state = providerVisibleStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider fatigue: ${state.providerFatigueScore}.`,
      );
    },
  );

  const showOrchestrationPressure = vscode.commands.registerCommand(
    'aiDevOs.showOrchestrationPressure',
    async () => {
      const state = orchestrationVisibleStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS orchestration pressure: ${state.orchestrationPressureScore}.`,
      );
    },
  );

  const compactContinuousAuditSummary = vscode.commands.registerCommand(
    'aiDevOs.compactContinuousAuditSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'continuous-runtime-audit-compact-summary',
        `AI_DEV_OS compact continuous audit: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showRuntimeHealth,
    showRetryPressure,
    showProviderFatigue,
    showOrchestrationPressure,
    compactContinuousAuditSummary,
  ];
}
