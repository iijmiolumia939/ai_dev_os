import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  PremiumProviderStatusBar,
  ProviderDowngradeStatusBar,
  ProviderPressureStatusBar,
  ProviderRoutingMonitor,
} from '../providerRouting/providerRouting';

export function registerProviderRoutingCommands(
  monitor: ProviderRoutingMonitor,
  premiumStatus: PremiumProviderStatusBar,
  downgradeStatus: ProviderDowngradeStatusBar,
  pressureStatus: ProviderPressureStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const showProviderRouting = vscode.commands.registerCommand('aiDevOs.showProviderRouting', async () => {
    const state = premiumStatus.refresh();
    downgradeStatus.refresh();
    pressureStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS provider routing: ${state.recommendedProviderClass}; local-only ${state.localOnly}.`,
    );
  });

  const showProviderBudget = vscode.commands.registerCommand('aiDevOs.showProviderBudget', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS provider budget: pressure ${state.providerBurnPressure}; avoided premium burn ${state.estimatedAvoidedPremiumProviderBurn}.`,
    );
  });

  const showDowngradeRecommendations = vscode.commands.registerCommand(
    'aiDevOs.showDowngradeRecommendations',
    async () => {
      const state = downgradeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS downgrade recommendations: ready ${state.downgradeReady}; compact ${state.compactRouting}.`,
      );
    },
  );

  const showProviderDistribution = vscode.commands.registerCommand(
    'aiDevOs.showProviderDistribution',
    async () => {
      const state = monitor.evaluate();
      const summary = state.distribution
        .map((entry) => `${entry.providerClass}:${entry.count}`)
        .join('; ');
      await vscode.window.showInformationMessage(`AI_DEV_OS provider distribution: ${summary}.`);
    },
  );

  const compactProviderRouting = vscode.commands.registerCommand('aiDevOs.compactProviderRouting', async () => {
    const state = monitor.compactRouting();
    premiumStatus.refresh();
    downgradeStatus.refresh();
    pressureStatus.refresh();
    await notifications.info(
      'provider-routing-compacted',
      `AI_DEV_OS compact provider routing retained ${state.distribution.length} provider classes.`,
    );
  });

  return [
    showProviderRouting,
    showProviderBudget,
    showDowngradeRecommendations,
    showProviderDistribution,
    compactProviderRouting,
  ];
}