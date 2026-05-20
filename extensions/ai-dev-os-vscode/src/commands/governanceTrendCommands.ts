import * as vscode from 'vscode';
import {GovernanceTrendMonitor, GovernanceTrendStatusBar} from '../governance/trends';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {GovernanceTrendViewProvider} from '../views/governanceTrendView';

export function registerGovernanceTrendCommands(
  monitor: GovernanceTrendMonitor,
  statusBar: GovernanceTrendStatusBar,
  notifications: RateLimitedNotifications,
  view: GovernanceTrendViewProvider,
): vscode.Disposable[] {
  const showTrends = vscode.commands.registerCommand('aiDevOs.showGovernanceTrends', async () => {
    const state = await statusBar.refresh();
    view.refresh();
    await vscode.window.showInformationMessage(JSON.stringify(state, undefined, 2));
  });

  const showDrift = vscode.commands.registerCommand('aiDevOs.showGovernanceDrift', async () => {
    const state = await monitor.evaluate();
    if (state.driftDetected) {
      await notifications.warn('governance-drift-warning', `AI_DEV_OS governance trend is ${state.trendLevel}.`);
    } else {
      await vscode.window.showInformationMessage('AI_DEV_OS governance drift is stable.');
    }
  });

  const showRegression = vscode.commands.registerCommand('aiDevOs.showGovernanceRegression', async () => {
    const state = await monitor.evaluate();
    if (state.regressionDetected) {
      await notifications.warn('governance-regression-warning', 'AI_DEV_OS governance regression review recommended.');
    } else {
      await vscode.window.showInformationMessage('AI_DEV_OS governance regression not detected.');
    }
  });

  const showDelta = vscode.commands.registerCommand('aiDevOs.showDashboardDelta', async () => {
    const state = await monitor.evaluate();
    await vscode.window.showInformationMessage(`AI_DEV_OS dashboard delta: ${state.dashboardDelta.join('; ')}`);
  });

  const compactWindow = vscode.commands.registerCommand('aiDevOs.compactGovernanceWindow', async () => {
    monitor.compactWindow();
    view.refresh();
    await notifications.info('governance-window-compacted', 'AI_DEV_OS governance trend window compacted.');
  });

  const resetWindow = vscode.commands.registerCommand('aiDevOs.resetGovernanceTrendWindow', async () => {
    monitor.resetWindow();
    view.refresh();
    await notifications.info('governance-window-reset', 'AI_DEV_OS governance trend window reset.');
  });

  return [showTrends, showDrift, showRegression, showDelta, compactWindow, resetWindow];
}
