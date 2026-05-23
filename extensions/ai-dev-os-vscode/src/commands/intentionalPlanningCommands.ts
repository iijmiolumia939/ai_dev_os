import * as vscode from 'vscode';
import {
  ContinuationStableStatusBar,
  DecayTrackedStatusBar,
  GoalActiveStatusBar,
  IntentionalPlanningMonitor,
  PlanningBoundedStatusBar,
} from '../intentionalPlanning/intentionalPlanning';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerIntentionalPlanningCommands(
  monitor: IntentionalPlanningMonitor,
  goalActiveStatus: GoalActiveStatusBar,
  planningBoundedStatus: PlanningBoundedStatusBar,
  decayTrackedStatus: DecayTrackedStatusBar,
  continuationStableStatus: ContinuationStableStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    goalActiveStatus.refresh();
    planningBoundedStatus.refresh();
    decayTrackedStatus.refresh();
    continuationStableStatus.refresh();
  };

  const showGoalHierarchy = vscode.commands.registerCommand(
    'aiDevOs.showGoalHierarchy',
    async () => {
      const state = goalActiveStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS goal hierarchy: ${state.goalHierarchy.join(' > ')}.`,
      );
    },
  );

  const showPlanningWindow = vscode.commands.registerCommand(
    'aiDevOs.showPlanningWindow',
    async () => {
      const state = planningBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS planning window pressure: ${state.planningWindowPressure}.`,
      );
    },
  );

  const showPlanningDecay = vscode.commands.registerCommand(
    'aiDevOs.showPlanningDecay',
    async () => {
      const state = decayTrackedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS planning decay: ${state.planningDecayStatus}; interruption ${state.planningInterruptionPressure}.`,
      );
    },
  );

  const showPlanningContinuation = vscode.commands.registerCommand(
    'aiDevOs.showPlanningContinuation',
    async () => {
      const state = continuationStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS planning continuation: ${state.continuationPressure}.`,
      );
    },
  );

  const compactIntentionalPlanningSummary = vscode.commands.registerCommand(
    'aiDevOs.compactIntentionalPlanningSummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'intentional-planning-compact-summary',
        `AI_DEV_OS compact intentional planning: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showGoalHierarchy,
    showPlanningWindow,
    showPlanningDecay,
    showPlanningContinuation,
    compactIntentionalPlanningSummary,
  ];
}
