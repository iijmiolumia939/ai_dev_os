import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  FallbackReadyStatusBar,
  LocalDelegationStatusBar,
  SubagentActiveStatusBar,
  SubagentExecutionMonitor,
  SwarmBlockedStatusBar,
} from '../subagentExecution/subagentExecution';

export function registerSubagentExecutionCommands(
  monitor: SubagentExecutionMonitor,
  subagentStatus: SubagentActiveStatusBar,
  localDelegationStatus: LocalDelegationStatusBar,
  fallbackStatus: FallbackReadyStatusBar,
  swarmStatus: SwarmBlockedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    const state = subagentStatus.refresh();
    localDelegationStatus.refresh();
    fallbackStatus.refresh();
    swarmStatus.refresh();
    return state;
  };

  const showSubagentRouting = vscode.commands.registerCommand('aiDevOs.showSubagentRouting', async () => {
    const state = refreshAll();
    const summary = state.routingDistribution.map((entry) => `${entry.providerClass}:${entry.count}`).join('; ');
    await vscode.window.showInformationMessage(`AI_DEV_OS subagent routing: ${summary}.`);
  });

  const testLocalSubagent = vscode.commands.registerCommand('aiDevOs.testLocalSubagent', async () => {
    const state = refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS local subagent: ${state.localSubagentProvider}; human-confirmed bounded delegation only.`,
    );
  });

  const showDelegationScope = vscode.commands.registerCommand('aiDevOs.showDelegationScope', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(`AI_DEV_OS delegation scope: ${state.delegationScope.join('; ')}.`);
  });

  const showFallbackState = vscode.commands.registerCommand('aiDevOs.showFallbackState', async () => {
    const state = fallbackStatus.refresh();
    await vscode.window.showInformationMessage(`AI_DEV_OS subagent fallback: ${state.fallbackState}.`);
  });

  const showSubagentGovernance = vscode.commands.registerCommand('aiDevOs.showSubagentGovernance', async () => {
    const state = swarmStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS subagent governance: ${state.governanceWarnings.join('; ')}.`,
    );
  });

  const compactDelegationSummary = vscode.commands.registerCommand('aiDevOs.compactDelegationSummary', async () => {
    const state = monitor.compactDelegationSummary();
    refreshAll();
    await notifications.info(
      'subagent-delegation-compacted',
      `AI_DEV_OS delegation summary compacted; avoided premium subagent tokens ${state.estimatedAvoidedPremiumSubagentTokens}.`,
    );
  });

  return [
    showSubagentRouting,
    testLocalSubagent,
    showDelegationScope,
    showFallbackState,
    showSubagentGovernance,
    compactDelegationSummary,
  ];
}
