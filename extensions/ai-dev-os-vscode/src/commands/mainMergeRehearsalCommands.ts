import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  CIReadyStatusBar,
  MainMergeRehearsalMonitor,
  MergeRehearsedStatusBar,
  PostMergeSafeStatusBar,
  RollbackReadyStatusBar,
} from '../mainMergeRehearsal/mainMergeRehearsal';

export function registerMainMergeRehearsalCommands(
  monitor: MainMergeRehearsalMonitor,
  mergeRehearsedStatus: MergeRehearsedStatusBar,
  rollbackReadyStatus: RollbackReadyStatusBar,
  postMergeSafeStatus: PostMergeSafeStatusBar,
  ciReadyStatus: CIReadyStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    mergeRehearsedStatus.refresh();
    rollbackReadyStatus.refresh();
    postMergeSafeStatus.refresh();
    ciReadyStatus.refresh();
  };

  const showMergeRehearsal = vscode.commands.registerCommand(
    'aiDevOs.showMergeRehearsal',
    async () => {
      const state = mergeRehearsedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS merge rehearsal: ${state.mainMergeRehearsalActive}.`,
      );
    },
  );

  const showProtectedBranchReadiness = vscode.commands.registerCommand(
    'aiDevOs.showProtectedBranchReadiness',
    async () => {
      const state = mergeRehearsedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS protected branch readiness: ${state.protectedBranchReadinessScore}.`,
      );
    },
  );

  const showRollbackSurvivability = vscode.commands.registerCommand(
    'aiDevOs.showRollbackSurvivability',
    async () => {
      const state = rollbackReadyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS rollback survivability: ${state.rollbackSurvivabilityScore}.`,
      );
    },
  );

  const showPostMergeRuntime = vscode.commands.registerCommand(
    'aiDevOs.showPostMergeRuntime',
    async () => {
      const state = postMergeSafeStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS post merge runtime: ${state.postMergeRuntimeScore}.`,
      );
    },
  );

  const compactMergeRehearsalSummary = vscode.commands.registerCommand(
    'aiDevOs.compactMergeRehearsalSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'main-merge-rehearsal-compact-summary',
        `AI_DEV_OS compact merge rehearsal: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showMergeRehearsal,
    showProtectedBranchReadiness,
    showRollbackSurvivability,
    showPostMergeRuntime,
    compactMergeRehearsalSummary,
  ];
}
