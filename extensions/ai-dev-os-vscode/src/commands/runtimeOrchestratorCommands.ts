import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ContinuationOrderedStatusBar,
  OrchestrationBoundedStatusBar,
  RetryOrderedStatusBar,
  RuntimeOrchestratorMonitor,
  SchedulingStableStatusBar,
} from '../runtimeOrchestrator/runtimeOrchestrator';

export function registerRuntimeOrchestratorCommands(
  monitor: RuntimeOrchestratorMonitor,
  orchestrationBoundedStatus: OrchestrationBoundedStatusBar,
  schedulingStableStatus: SchedulingStableStatusBar,
  retryOrderedStatus: RetryOrderedStatusBar,
  continuationOrderedStatus: ContinuationOrderedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    orchestrationBoundedStatus.refresh();
    schedulingStableStatus.refresh();
    retryOrderedStatus.refresh();
    continuationOrderedStatus.refresh();
  };

  const showRuntimeOrchestrator = vscode.commands.registerCommand(
    'aiDevOs.showRuntimeOrchestrator',
    async () => {
      const state = orchestrationBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime orchestrator: ${state.orchestrationScheduleScore}.`,
      );
    },
  );

  const showValidationSchedule = vscode.commands.registerCommand(
    'aiDevOs.showValidationSchedule',
    async () => {
      const state = schedulingStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS validation schedule: ${state.validationScheduleScore}.`,
      );
    },
  );

  const showRetrySchedule = vscode.commands.registerCommand(
    'aiDevOs.showRetrySchedule',
    async () => {
      const state = retryOrderedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry schedule: ${state.retryScheduleScore}.`,
      );
    },
  );

  const showContinuationSchedule = vscode.commands.registerCommand(
    'aiDevOs.showContinuationSchedule',
    async () => {
      const state = continuationOrderedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS continuation schedule: ${state.continuationScheduleScore}.`,
      );
    },
  );

  const compactRuntimeOrchestratorSummary = vscode.commands.registerCommand(
    'aiDevOs.compactRuntimeOrchestratorSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'runtime-orchestrator-compact-summary',
        `AI_DEV_OS compact runtime orchestrator: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showRuntimeOrchestrator,
    showValidationSchedule,
    showRetrySchedule,
    showContinuationSchedule,
    compactRuntimeOrchestratorSummary,
  ];
}
