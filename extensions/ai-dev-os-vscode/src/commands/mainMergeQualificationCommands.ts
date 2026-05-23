import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  GovernanceCompleteStatusBar,
  MainMergeQualificationMonitor,
  MergeReadyStatusBar,
  QualificationValidationStableStatusBar,
  RiskBoundedStatusBar,
} from '../mainMergeQualification/mainMergeQualification';

export function registerMainMergeQualificationCommands(
  monitor: MainMergeQualificationMonitor,
  mergeReadyStatus: MergeReadyStatusBar,
  governanceCompleteStatus: GovernanceCompleteStatusBar,
  validationStableStatus: QualificationValidationStableStatusBar,
  riskBoundedStatus: RiskBoundedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    mergeReadyStatus.refresh();
    governanceCompleteStatus.refresh();
    validationStableStatus.refresh();
    riskBoundedStatus.refresh();
  };

  const showMergeQualification = vscode.commands.registerCommand(
    'aiDevOs.showMergeQualification',
    async () => {
      const state = mergeReadyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS merge qualification: ${state.mainMergeQualificationActive}.`,
      );
    },
  );

  const showGovernanceCompleteness = vscode.commands.registerCommand(
    'aiDevOs.showGovernanceCompleteness',
    async () => {
      const state = governanceCompleteStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS governance completeness: ${state.governanceCompletenessScore}.`,
      );
    },
  );

  const showValidationCompleteness = vscode.commands.registerCommand(
    'aiDevOs.showValidationCompleteness',
    async () => {
      const state = validationStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS validation completeness: ${state.validationCompletenessScore}.`,
      );
    },
  );

  const showOperationalRisk = vscode.commands.registerCommand(
    'aiDevOs.showOperationalRisk',
    async () => {
      const state = riskBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS operational risk: ${state.operationalRiskScore}.`,
      );
    },
  );

  const compactMergeQualificationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactMergeQualificationSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'main-merge-qualification-compact-summary',
        `AI_DEV_OS compact merge qualification: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showMergeQualification,
    showGovernanceCompleteness,
    showValidationCompleteness,
    showOperationalRisk,
    compactMergeQualificationSummary,
  ];
}
