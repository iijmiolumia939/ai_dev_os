import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ContinuationValidStatusBar,
  ExecutionCoherentStatusBar,
  PlanningStableStatusBar,
  ReflectionBoundedStatusBar,
  ReflectiveEvaluationMonitor,
} from '../reflectiveEvaluation/reflectiveEvaluation';

export function registerReflectiveEvaluationCommands(
  monitor: ReflectiveEvaluationMonitor,
  reflectionBoundedStatus: ReflectionBoundedStatusBar,
  executionCoherentStatus: ExecutionCoherentStatusBar,
  continuationValidStatus: ContinuationValidStatusBar,
  planningStableStatus: PlanningStableStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    reflectionBoundedStatus.refresh();
    executionCoherentStatus.refresh();
    continuationValidStatus.refresh();
    planningStableStatus.refresh();
  };

  const showReflectiveEvaluation = vscode.commands.registerCommand(
    'aiDevOs.showReflectiveEvaluation',
    async () => {
      const state = reflectionBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS reflective evaluation: execution ${state.executionQualityScore}; coherence ${state.cognitiveCoherenceScore}.`,
      );
    },
  );

  const showCognitiveCoherence = vscode.commands.registerCommand(
    'aiDevOs.showCognitiveCoherence',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS cognitive coherence: ${state.cognitiveCoherenceScore}.`,
      );
    },
  );

  const showContinuationValidity = vscode.commands.registerCommand(
    'aiDevOs.showContinuationValidity',
    async () => {
      const state = continuationValidStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS continuation validity: ${state.continuationValidityScore}.`,
      );
    },
  );

  const showPlanningIntegrity = vscode.commands.registerCommand(
    'aiDevOs.showPlanningIntegrity',
    async () => {
      const state = planningStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS planning integrity: ${state.planningIntegrityScore}.`,
      );
    },
  );

  const compactReflectiveEvaluationSummary = vscode.commands.registerCommand(
    'aiDevOs.compactReflectiveEvaluationSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'reflective-evaluation-compact-summary',
        `AI_DEV_OS compact reflective evaluation: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showReflectiveEvaluation,
    showCognitiveCoherence,
    showContinuationValidity,
    showPlanningIntegrity,
    compactReflectiveEvaluationSummary,
  ];
}
