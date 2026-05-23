import * as vscode from 'vscode';
import {
  AdaptiveProviderMonitor,
  CostGuardedStatusBar,
  FatigueTrackedStatusBar,
  LocalFirstStatusBar,
  ProviderBoundedStatusBar,
} from '../adaptiveProvider/adaptiveProvider';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerAdaptiveProviderCommands(
  monitor: AdaptiveProviderMonitor,
  providerBoundedStatus: ProviderBoundedStatusBar,
  localFirstStatus: LocalFirstStatusBar,
  fatigueTrackedStatus: FatigueTrackedStatusBar,
  costGuardedStatus: CostGuardedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    providerBoundedStatus.refresh();
    localFirstStatus.refresh();
    fatigueTrackedStatus.refresh();
    costGuardedStatus.refresh();
  };

  const showProviderCapability = vscode.commands.registerCommand(
    'aiDevOs.showProviderCapability',
    async () => {
      const state = providerBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider capability: ${state.providerCapabilityScore}; ${state.recommendedProvider}.`,
      );
    },
  );

  const showProviderCost = vscode.commands.registerCommand(
    'aiDevOs.showProviderCost',
    async () => {
      const state = costGuardedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider cost pressure: ${state.providerCostPressure}.`,
      );
    },
  );

  const showProviderConfidence = vscode.commands.registerCommand(
    'aiDevOs.showProviderConfidence',
    async () => {
      const state = localFirstStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider confidence: ${state.providerConfidenceScore}.`,
      );
    },
  );

  const compactAdaptiveProviderSummary = vscode.commands.registerCommand(
    'aiDevOs.compactAdaptiveProviderSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'adaptive-provider-compact-summary',
        `AI_DEV_OS compact adaptive provider: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showProviderCapability,
    showProviderCost,
    showProviderConfidence,
    compactAdaptiveProviderSummary,
  ];
}
