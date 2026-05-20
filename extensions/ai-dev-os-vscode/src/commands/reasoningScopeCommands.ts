import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {ReasoningScopeMonitor, ReasoningScopeStatusBar} from '../reasoningScope/reasoningScope';

export function registerReasoningScopeCommands(
  monitor: ReasoningScopeMonitor,
  statusBar: ReasoningScopeStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const showReasoningScope = vscode.commands.registerCommand('aiDevOs.showReasoningScope', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS reasoning scope: ${state.taskLocalScope.join(', ')}; local patch ${state.localPatchModeActive}.`,
    );
  });

  const showReasoningDepth = vscode.commands.registerCommand('aiDevOs.showReasoningDepth', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS reasoning depth: cap ${state.depthCap}; bounded ${state.reasoningDepthActive}.`,
    );
  });

  const showPremiumBurnPressure = vscode.commands.registerCommand(
    'aiDevOs.showPremiumBurnPressure',
    async () => {
      const state = statusBar.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS premium pressure: ${state.reasoningPressure}; avoided burn ${state.estimatedAvoidedPremiumReasoningBurn}.`,
      );
    },
  );

  const showLocalPatchMode = vscode.commands.registerCommand('aiDevOs.showLocalPatchMode', async () => {
    const state = monitor.compactScope();
    statusBar.refresh();
    await notifications.info(
      'reasoning-scope-local-patch',
      `AI_DEV_OS local patch reasoning retained ${state.taskLocalScope.length} runtime scopes.`,
    );
  });

  const showEscalationGuard = vscode.commands.registerCommand('aiDevOs.showEscalationGuard', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS escalation guard: ${state.architectureGuardActive}; hidden provider routing ${state.noHiddenProviderRouting ? 'blocked' : 'open'}.`,
    );
  });

  return [
    showReasoningScope,
    showReasoningDepth,
    showPremiumBurnPressure,
    showLocalPatchMode,
    showEscalationGuard,
  ];
}
