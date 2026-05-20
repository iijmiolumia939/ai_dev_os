import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {RuntimeSimplificationMonitor, SimplificationStatusBar} from '../runtimeSimplification/runtimeSimplification';
import {ContractOverlapViewProvider} from '../views/contractOverlapView';
import {MergeCandidateViewProvider} from '../views/mergeCandidateView';
import {RuntimeOverlapViewProvider} from '../views/runtimeOverlapView';

export function registerRuntimeSimplificationCommands(
  monitor: RuntimeSimplificationMonitor,
  statusBar: SimplificationStatusBar,
  notifications: RateLimitedNotifications,
  overlapView: RuntimeOverlapViewProvider,
  contractView: ContractOverlapViewProvider,
  mergeView: MergeCandidateViewProvider,
): vscode.Disposable[] {
  const showRuntimeOverlap = vscode.commands.registerCommand('aiDevOs.showRuntimeOverlap', async () => {
    const state = statusBar.refresh();
    overlapView.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS runtime overlap: ${state.overlapCategories.length}; density ${state.overlapDensity}.`,
    );
  });

  const showContractOverlap = vscode.commands.registerCommand('aiDevOs.showContractOverlap', async () => {
    const state = monitor.evaluate();
    contractView.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS contract overlap groups: ${state.contractGroups.length}.`,
    );
  });

  const showMergeCandidates = vscode.commands.registerCommand('aiDevOs.showMergeCandidates', async () => {
    const state = monitor.evaluate();
    mergeView.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS merge candidates require human review: ${state.mergeCandidates.length}.`,
    );
  });

  const showGovernanceDuplication = vscode.commands.registerCommand(
    'aiDevOs.showGovernanceDuplication',
    async () => {
      const state = monitor.evaluate();
      if (state.governanceGroups.length > 0) {
        await notifications.warn(
          'runtime-simplification-governance-warning',
          `AI_DEV_OS governance duplication groups: ${state.governanceGroups.length}.`,
        );
      } else {
        await vscode.window.showInformationMessage('AI_DEV_OS governance duplication not detected.');
      }
    },
  );

  const showRecommendations = vscode.commands.registerCommand(
    'aiDevOs.showSimplificationRecommendations',
    async () => {
      const state = statusBar.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS simplification recommendations: ${state.recommendationCount}; automatic mutation ${state.automaticMutationUsed}.`,
      );
    },
  );

  const compactSimplificationView = vscode.commands.registerCommand('aiDevOs.compactSimplificationView', async () => {
    const state = monitor.compact();
    overlapView.refresh();
    contractView.refresh();
    mergeView.refresh();
    await notifications.info(
      'runtime-simplification-compacted',
      `AI_DEV_OS compact simplification view retained ${state.recommendationCount} recommendations.`,
    );
  });

  return [
    showRuntimeOverlap,
    showContractOverlap,
    showMergeCandidates,
    showGovernanceDuplication,
    showRecommendations,
    compactSimplificationView,
  ];
}