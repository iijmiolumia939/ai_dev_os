import * as vscode from 'vscode';
import {GovernanceCoreMonitor, GovernanceCoreStatusBar} from '../governanceCore/governanceCore';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {BoundedRetentionViewProvider} from '../views/boundedRetentionView';
import {PrimitiveReuseViewProvider} from '../views/primitiveReuseView';
import {SharedPrimitiveViewProvider} from '../views/sharedPrimitiveView';

export function registerGovernanceCoreCommands(
  monitor: GovernanceCoreMonitor,
  statusBar: GovernanceCoreStatusBar,
  notifications: RateLimitedNotifications,
  sharedView: SharedPrimitiveViewProvider,
  reuseView: PrimitiveReuseViewProvider,
  retentionView: BoundedRetentionViewProvider,
): vscode.Disposable[] {
  const showGovernanceCore = vscode.commands.registerCommand('aiDevOs.showGovernanceCore', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS governance core active: ${state.coreActive}; bounded reuse ${state.boundedReuseStatus}.`,
    );
  });

  const showSharedPrimitives = vscode.commands.registerCommand('aiDevOs.showSharedPrimitives', async () => {
    const state = monitor.evaluate();
    sharedView.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS shared primitives: ${state.sharedPrimitives.length}.`,
    );
  });

  const showPrimitiveReuse = vscode.commands.registerCommand('aiDevOs.showPrimitiveReuse', async () => {
    const state = monitor.evaluate();
    reuseView.refresh();
    if (state.duplicatedGovernanceWarningsReduced) {
      await notifications.info(
        'governance-core-reuse-reduction',
        `AI_DEV_OS primitive reuse targets: ${state.reuseTargets.length}.`,
      );
    }
  });

  const showBoundedRetention = vscode.commands.registerCommand('aiDevOs.showBoundedRetention', async () => {
    const state = monitor.evaluate();
    retentionView.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS bounded retention limit ${state.retentionLimit}; evicted ${state.evictedItems}.`,
    );
  });

  const showCompactExportStatus = vscode.commands.registerCommand(
    'aiDevOs.showCompactExportStatus',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS compact export active: ${state.compactExportActive}; summary only ${state.summaryOnly}.`,
      );
    },
  );

  return [
    showGovernanceCore,
    showSharedPrimitives,
    showPrimitiveReuse,
    showBoundedRetention,
    showCompactExportStatus,
  ];
}