import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  CommandGroundedStatusBar,
  GitEvidenceSafeStatusBar,
  PytestVerifiedStatusBar,
  VerifiedExecutionMonitor,
  VerifiedExecutionStatusBar,
} from '../verifiedExecution/verifiedExecution';

export function registerVerifiedExecutionCommands(
  monitor: VerifiedExecutionMonitor,
  verifiedExecutionStatus: VerifiedExecutionStatusBar,
  commandGroundedStatus: CommandGroundedStatusBar,
  pytestVerifiedStatus: PytestVerifiedStatusBar,
  gitEvidenceSafeStatus: GitEvidenceSafeStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    verifiedExecutionStatus.refresh();
    commandGroundedStatus.refresh();
    pytestVerifiedStatus.refresh();
    gitEvidenceSafeStatus.refresh();
  };

  const runVerifiedCommand = vscode.commands.registerCommand(
    'aiDevOs.runVerifiedCommand',
    async () => {
      const state = commandGroundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS command evidence: ${state.commandSummary}.`,
      );
    },
  );

  const showExecutionEvidence = vscode.commands.registerCommand(
    'aiDevOs.showExecutionEvidence',
    async () => {
      const state = verifiedExecutionStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution evidence: ${state.executionSummary}.`,
      );
    },
  );

  const showPytestEvidence = vscode.commands.registerCommand(
    'aiDevOs.showPytestEvidence',
    async () => {
      const state = pytestVerifiedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS pytest evidence: ${state.pytestSummary}.`,
      );
    },
  );

  const showGitEvidence = vscode.commands.registerCommand('aiDevOs.showGitEvidence', async () => {
    const state = gitEvidenceSafeStatus.refresh();
    await vscode.window.showInformationMessage(`AI_DEV_OS git evidence: ${state.gitSummary}.`);
  });

  const compactVerifiedExecutionSummary = vscode.commands.registerCommand(
    'aiDevOs.compactVerifiedExecutionSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'verified-execution-compact-summary',
        `AI_DEV_OS compact verified execution summary: ${state.compactSummary}.`,
      );
    },
  );

  return [
    runVerifiedCommand,
    showExecutionEvidence,
    showPytestEvidence,
    showGitEvidence,
    compactVerifiedExecutionSummary,
  ];
}