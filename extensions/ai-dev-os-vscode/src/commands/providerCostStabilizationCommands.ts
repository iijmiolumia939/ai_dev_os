import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  CostStableStatusBar,
  FrontierBoundedStatusBar,
  LocalFirstEfficiencyStatusBar,
  OverheadFlatStatusBar,
  ProviderCostStabilizationMonitor,
} from '../providerCostStabilization/providerCostStabilization';

export function registerProviderCostStabilizationCommands(
  monitor: ProviderCostStabilizationMonitor,
  costStableStatus: CostStableStatusBar,
  frontierBoundedStatus: FrontierBoundedStatusBar,
  localFirstEfficiencyStatus: LocalFirstEfficiencyStatusBar,
  overheadFlatStatus: OverheadFlatStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    costStableStatus.refresh();
    frontierBoundedStatus.refresh();
    localFirstEfficiencyStatus.refresh();
    overheadFlatStatus.refresh();
  };

  const showCostStabilization = vscode.commands.registerCommand(
    'aiDevOs.showCostStabilization',
    async () => {
      const state = costStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS cost stabilization: ${state.providerCostStabilizationActive}.`,
      );
    },
  );

  const showFrontierDependency = vscode.commands.registerCommand(
    'aiDevOs.showFrontierDependency',
    async () => {
      const state = frontierBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS frontier dependency: ${state.frontierDependencyScore}.`,
      );
    },
  );

  const showRetryCost = vscode.commands.registerCommand(
    'aiDevOs.showRetryCost',
    async () => {
      const state = overheadFlatStatus.refresh();
      await vscode.window.showInformationMessage(`AI_DEV_OS retry cost: ${state.retryCostScore}.`);
    },
  );

  const showLocalFirstEfficiency = vscode.commands.registerCommand(
    'aiDevOs.showLocalFirstEfficiency',
    async () => {
      const state = localFirstEfficiencyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS local first efficiency: ${state.localFirstEfficiencyScore}.`,
      );
    },
  );

  const compactCostStabilizationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactCostStabilizationSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'provider-cost-stabilization-compact-summary',
        `AI_DEV_OS compact cost stabilization: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showCostStabilization,
    showFrontierDependency,
    showRetryCost,
    showLocalFirstEfficiency,
    compactCostStabilizationSummary,
  ];
}
