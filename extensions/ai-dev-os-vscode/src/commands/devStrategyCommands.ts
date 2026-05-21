import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  CostPressureStatusBar,
  DevStrategyMonitor,
  ProviderEfficiencyStatusBar,
  RoadmapPressureStatusBar,
  StrategyStableStatusBar,
} from '../devStrategy/devStrategy';

export function registerDevStrategyCommands(
  monitor: DevStrategyMonitor,
  strategyStatus: StrategyStableStatusBar,
  costStatus: CostPressureStatusBar,
  providerStatus: ProviderEfficiencyStatusBar,
  roadmapStatus: RoadmapPressureStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    strategyStatus.refresh();
    costStatus.refresh();
    providerStatus.refresh();
    roadmapStatus.refresh();
  };

  const showDevelopmentStrategy = vscode.commands.registerCommand(
    'aiDevOs.showDevelopmentStrategy',
    async () => {
      const state = strategyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS development strategy: ${state.compactSummary}; human-confirmed ${state.humanConfirmedStrategyOnly}.`,
      );
    },
  );

  const showCostReductionStrategy = vscode.commands.registerCommand(
    'aiDevOs.showCostReductionStrategy',
    async () => {
      const state = costStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS cost strategy: ${state.costHints.join('; ')}; pressure ${state.costPressure}.`,
      );
    },
  );

  const showGovernanceStabilityStrategy = vscode.commands.registerCommand(
    'aiDevOs.showGovernanceStabilityStrategy',
    async () => {
      const state = roadmapStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS governance strategy: ${state.governanceHints.join('; ')}; roadmap ${state.roadmapPressure}.`,
      );
    },
  );

  const showProviderEfficiencyStrategy = vscode.commands.registerCommand(
    'aiDevOs.showProviderEfficiencyStrategy',
    async () => {
      const state = providerStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider strategy: ${state.providerHints.join('; ')}.`,
      );
    },
  );

  const showSprintDensityStrategy = vscode.commands.registerCommand(
    'aiDevOs.showSprintDensityStrategy',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS sprint density strategy: ${state.sprintDensityHints.join('; ')}.`,
      );
    },
  );

  const compactStrategySummary = vscode.commands.registerCommand(
    'aiDevOs.compactStrategySummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await notifications.info(
        'development-strategy-compacted',
        `AI_DEV_OS strategy summary compacted; roadmap pressure ${state.roadmapPressure}.`,
      );
    },
  );

  return [
    showDevelopmentStrategy,
    showCostReductionStrategy,
    showGovernanceStabilityStrategy,
    showProviderEfficiencyStrategy,
    showSprintDensityStrategy,
    compactStrategySummary,
  ];
}