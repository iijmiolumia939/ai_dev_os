import * as vscode from 'vscode';
import {GovernanceHealthMonitor, GovernanceStatusBar} from '../governance/health';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {GovernanceDashboardViewProvider} from '../views/governanceDashboardView';

export function registerGovernanceHealthCommands(
  monitor: GovernanceHealthMonitor,
  statusBar: GovernanceStatusBar,
  notifications: RateLimitedNotifications,
  view: GovernanceDashboardViewProvider,
): vscode.Disposable[] {
  const showDashboard = vscode.commands.registerCommand('aiDevOs.showGovernanceDashboard', async () => {
    const state = await statusBar.refresh();
    view.refresh();
    await vscode.window.showInformationMessage(JSON.stringify(state, undefined, 2));
  });

  const showHealth = vscode.commands.registerCommand('aiDevOs.showGovernanceHealth', async () => {
    const state = await statusBar.refresh();
    await vscode.window.showInformationMessage(`AI_DEV_OS governance health: ${state.level} (${state.healthScore})`);
  });

  const showRisks = vscode.commands.registerCommand('aiDevOs.showGovernanceRisks', async () => {
    const state = await monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS highest governance risk: ${state.highestRisk}; warnings: ${state.activeWarnings.join(', ') || 'none'}`,
    );
  });

  const showPressure = vscode.commands.registerCommand('aiDevOs.showGovernancePressure', async () => {
    const state = await monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS governance pressure: ${state.pressure}; dominant: ${state.dominantPressure}`,
    );
  });

  const runStabilityAudit = vscode.commands.registerCommand('aiDevOs.runGovernanceStabilityAudit', async () => {
    const state = await statusBar.refresh();
    const stable = state.level === 'HEALTHY' || state.level === 'WARNING';
    await vscode.window.showInformationMessage(
      `AI_DEV_OS governance stability: ${stable ? 'stable' : 'review recommended'}; no automatic action taken.`,
    );
  });

  const compactContext = vscode.commands.registerCommand('aiDevOs.compactGovernanceContext', async () => {
    const state = await monitor.compactRecommendation();
    await notifications.info(
      'governance-compact-recommendation',
      `AI_DEV_OS compact governance context recommended: ${state.activeWarnings.length > 0}.`,
    );
  });

  const showArchitectureIsolation = vscode.commands.registerCommand(
    'aiDevOs.showArchitectureIsolationState',
    async () => {
      const state = await monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS architecture isolation state: ${state.architectureIsolationState}`,
      );
    },
  );

  return [
    showDashboard,
    showHealth,
    showRisks,
    showPressure,
    runStabilityAudit,
    compactContext,
    showArchitectureIsolation,
  ];
}
