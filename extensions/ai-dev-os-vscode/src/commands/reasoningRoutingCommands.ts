import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {ReasoningRoutingMonitor, ReasoningTierStatusBar} from '../reasoningRouting/reasoningRouting';

export function registerReasoningRoutingCommands(
  monitor: ReasoningRoutingMonitor,
  statusBar: ReasoningTierStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const showReasoningTier = vscode.commands.registerCommand('aiDevOs.showReasoningTier', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS reasoning tier: ${state.activeTier}; human-visible ${state.humanVisibleRouting}.`,
    );
  });

  const showCostBudget = vscode.commands.registerCommand('aiDevOs.showCostBudget', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS cost budget: ${state.budgetPressure}; avoided premium burn ${state.estimatedAvoidedPremiumBurn}.`,
    );
  });

  const showEscalationPolicy = vscode.commands.registerCommand('aiDevOs.showEscalationPolicy', async () => {
    const state = monitor.evaluate();
    if (state.escalationWarning) {
      await notifications.warn(
        'reasoning-escalation-warning',
        'AI_DEV_OS high reasoning is reserved for visible architecture, governance, or embodiment scope.',
      );
    } else {
      await vscode.window.showInformationMessage('AI_DEV_OS escalation policy does not require high reasoning.');
    }
  });

  const showSprintReasoningMap = vscode.commands.registerCommand('aiDevOs.showSprintReasoningMap', async () => {
    const state = monitor.evaluate();
    const summary = state.sprintReasoningMap.map((entry) => `${entry.task}: ${entry.tier}`).join('; ');
    await vscode.window.showInformationMessage(`AI_DEV_OS sprint reasoning map: ${summary}.`);
  });

  const compactReasoningScope = vscode.commands.registerCommand('aiDevOs.compactReasoningScope', async () => {
    const state = monitor.compactScope();
    statusBar.refresh();
    await notifications.info(
      'reasoning-scope-compacted',
      `AI_DEV_OS compact reasoning scope retained ${state.sprintReasoningMap.length} active entries.`,
    );
  });

  return [
    showReasoningTier,
    showCostBudget,
    showEscalationPolicy,
    showSprintReasoningMap,
    compactReasoningScope,
  ];
}