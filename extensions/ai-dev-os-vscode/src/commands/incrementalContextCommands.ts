import * as vscode from 'vscode';
import {IncrementalContextMonitor, IncrementalContextStatusBar} from '../incrementalContext/incrementalContext';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerIncrementalContextCommands(
  monitor: IncrementalContextMonitor,
  statusBar: IncrementalContextStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const showContextDelta = vscode.commands.registerCommand('aiDevOs.showContextDelta', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS context delta: ${state.compactChangedNeighborhood.length} changed; ${state.unchangedContextExcluded.length} unchanged suppressed.`,
    );
  });

  const showIncrementalRetrieval = vscode.commands.registerCommand(
    'aiDevOs.showIncrementalRetrieval',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS incremental retrieval: delta-only ${state.deltaRetrievalActive}; repo-wide replay blocked ${state.repoWideReplayForbidden}.`,
      );
    },
  );

  const showDeltaAudit = vscode.commands.registerCommand('aiDevOs.showDeltaAudit', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS delta audit: active ${state.auditDeltaActive}; summary-only ${state.summaryOnly}.`,
    );
  });

  const showReplayPressure = vscode.commands.registerCommand('aiDevOs.showReplayPressure', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS replay pressure: ${state.replayPressure}; avoided repeated input ${state.estimatedAvoidedRepeatedInputTokens}.`,
    );
  });

  const compactIncrementalContext = vscode.commands.registerCommand(
    'aiDevOs.compactIncrementalContext',
    async () => {
      const state = monitor.compactContext();
      statusBar.refresh();
      await notifications.info(
        'incremental-context-compacted',
        `AI_DEV_OS compact incremental context retained ${state.compactChangedNeighborhood.length} changed runtimes.`,
      );
    },
  );

  const showIncrementalRecommendations = vscode.commands.registerCommand(
    'aiDevOs.showIncrementalRecommendations',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS incremental recommendation: continue delta-only; duplicate cognition avoided ${state.estimatedAvoidedDuplicateRuntimeCognition}.`,
      );
    },
  );

  return [
    showContextDelta,
    showIncrementalRetrieval,
    showDeltaAudit,
    showReplayPressure,
    compactIncrementalContext,
    showIncrementalRecommendations,
  ];
}
