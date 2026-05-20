import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {CompactReportingStatusBar, OutputCompressionMonitor} from '../outputCompression/outputCompression';

export function registerOutputCompressionCommands(
  monitor: OutputCompressionMonitor,
  statusBar: CompactReportingStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const toggleCompactReporting = vscode.commands.registerCommand(
    'aiDevOs.toggleCompactReporting',
    async () => {
      const state = monitor.toggleCompactReporting();
      statusBar.refresh();
      await notifications.info(
        'compact-reporting-toggle',
        `AI_DEV_OS compact reporting ${state.compactReporting ? 'enabled' : 'disabled'}.`,
      );
    },
  );

  const showVerbosityPressure = vscode.commands.registerCommand(
    'aiDevOs.showVerbosityPressure',
    async () => {
      const state = statusBar.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS verbosity pressure: ${state.verbosityPressure}; compact reporting ${state.compactReporting}.`,
      );
    },
  );

  const expandCompletionSummary = vscode.commands.registerCommand(
    'aiDevOs.expandCompletionSummary',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(state.expandableCompletion.join('; '));
    },
  );

  const showReportDensity = vscode.commands.registerCommand('aiDevOs.showReportDensity', async () => {
    const state = statusBar.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS report density: ${state.summaryDensity}; avoided repeated summaries ${state.estimatedAvoidedRepeatedSummaries}.`,
    );
  });

  return [toggleCompactReporting, showVerbosityPressure, expandCompletionSummary, showReportDensity];
}