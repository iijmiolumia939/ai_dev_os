import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {RetrievalBudgetMonitor, RetrievalBudgetStatusBar} from '../retrievalBudget/retrievalBudget';

export function registerRetrievalBudgetCommands(
  monitor: RetrievalBudgetMonitor,
  statusBar: RetrievalBudgetStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const showRetrievalBudget = vscode.commands.registerCommand('aiDevOs.showRetrievalBudget', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS retrieval budget: ${state.compactNeighborhood.length}/${state.maxRuntimeCount} runtimes; repo-wide ${state.repoWideRetrievalForbidden ? 'blocked' : 'open'}.`,
    );
  });

  const showRetrievalRadius = vscode.commands.registerCommand('aiDevOs.showRetrievalRadius', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS retrieval radius: dependency distance ${state.maxDependencyDistance}; contracts ${state.boundedContractAdjacency.length}.`,
    );
  });

  const showRetrievalPressure = vscode.commands.registerCommand('aiDevOs.showRetrievalPressure', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS retrieval pressure: ${state.retrievalPressure}; avoided hidden input ${state.estimatedAvoidedHiddenInputTokens}.`,
    );
  });

  const compactRetrievalScope = vscode.commands.registerCommand('aiDevOs.compactRetrievalScope', async () => {
    const state = monitor.compactScope();
    statusBar.refresh();
    await notifications.info(
      'retrieval-scope-compacted',
      `AI_DEV_OS compact retrieval scope retained ${state.compactNeighborhood.length} runtimes.`,
    );
  });

  const showRetrievalNeighborhood = vscode.commands.registerCommand(
    'aiDevOs.showRetrievalNeighborhood',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retrieval neighborhood: ${state.compactNeighborhood.join(', ')}.`,
      );
    },
  );

  return [
    showRetrievalBudget,
    showRetrievalRadius,
    showRetrievalPressure,
    compactRetrievalScope,
    showRetrievalNeighborhood,
  ];
}