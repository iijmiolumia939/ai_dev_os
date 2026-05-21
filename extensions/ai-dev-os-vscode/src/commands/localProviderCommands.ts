import * as vscode from 'vscode';
import {
  LocalBudgetOkStatusBar,
  LocalProviderMonitor,
  LocalProviderReadyStatusBar,
  OllamaActiveStatusBar,
  PremiumEscalationStatusBar,
} from '../localProvider/localProvider';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerLocalProviderCommands(
  monitor: LocalProviderMonitor,
  localReadyStatus: LocalProviderReadyStatusBar,
  ollamaStatus: OllamaActiveStatusBar,
  budgetStatus: LocalBudgetOkStatusBar,
  escalationStatus: PremiumEscalationStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    const state = localReadyStatus.refresh();
    ollamaStatus.refresh();
    budgetStatus.refresh();
    escalationStatus.refresh();
    return state;
  };

  const showLocalProviders = vscode.commands.registerCommand('aiDevOs.showLocalProviders', async () => {
    const state = refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS local providers: ${state.primaryCodingModel}; compression ${state.governanceCompressionModel}.`,
    );
  });

  const testOllamaProvider = vscode.commands.registerCommand('aiDevOs.testOllamaProvider', async () => {
    const state = refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS Ollama provider: active ${state.ollamaActive}; bounded dry-run only.`,
    );
  });

  const showLocalProviderBudget = vscode.commands.registerCommand('aiDevOs.showLocalProviderBudget', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS local budget: ${state.localBudgetOk}; avoided premium tokens ${state.estimatedAvoidedPremiumTokens}.`,
    );
  });

  const compactLocalExecution = vscode.commands.registerCommand('aiDevOs.compactLocalExecution', async () => {
    const state = monitor.compactLocalExecution();
    refreshAll();
    await notifications.info(
      'local-provider-compacted',
      `AI_DEV_OS compact local execution ratio ${state.estimatedLocalExecutionRatio}.`,
    );
  });

  return [showLocalProviders, testOllamaProvider, showLocalProviderBudget, compactLocalExecution];
}
