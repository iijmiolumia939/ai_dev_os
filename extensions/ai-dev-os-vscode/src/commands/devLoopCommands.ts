import * as vscode from 'vscode';
import {
  LocalPatchRequiredStatusBar,
  SprintActiveStatusBar,
  SprintDevLoopMonitor,
  SprintPressureStatusBar,
  SprintRolloverStatusBar,
} from '../devLoop/devLoop';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerDevLoopCommands(
  monitor: SprintDevLoopMonitor,
  sprintStatus: SprintActiveStatusBar,
  rolloverStatus: SprintRolloverStatusBar,
  pressureStatus: SprintPressureStatusBar,
  localPatchStatus: LocalPatchRequiredStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    sprintStatus.refresh();
    rolloverStatus.refresh();
    pressureStatus.refresh();
    localPatchStatus.refresh();
  };

  const generateSprintPlan = vscode.commands.registerCommand('aiDevOs.generateSprintPlan', async () => {
    const state = monitor.generatePlan();
    refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS sprint plan: LOCAL_PATCH_REQUIRED; provider distribution HIGH:${state.providerRoutingDistribution[0].count} MEDIUM:${state.providerRoutingDistribution[1].count} LOW:${state.providerRoutingDistribution[2].count}.`,
    );
  });

  const showSprintLifecycle = vscode.commands.registerCommand('aiDevOs.showSprintLifecycle', async () => {
    const state = monitor.evaluate();
    refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS sprint lifecycle: ${state.lifecycleState}; rollover ${state.rolloverReady ? 'ready' : 'pending'}.`,
    );
  });

  const generateNextSprint = vscode.commands.registerCommand('aiDevOs.generateNextSprint', async () => {
    const state = monitor.generateNextSprint();
    refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS next sprint: adjacent runtime continuation; pressure ${state.sprintPressure}.`,
    );
  });

  const generateSprintBootstrap = vscode.commands.registerCommand(
    'aiDevOs.generateSprintBootstrap',
    async () => {
      const state = monitor.generateBootstrap();
      refreshAll();
      await vscode.window.showInformationMessage(`AI_DEV_OS sprint bootstrap: ${state.compactBootstrap}`);
    },
  );

  const showSprintGovernance = vscode.commands.registerCommand('aiDevOs.showSprintGovernance', async () => {
    const state = pressureStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS sprint governance: pressure ${state.sprintPressure}; avoided explosion ${state.estimatedAvoidedSprintExplosion}.`,
    );
  });

  const compactSprintClosure = vscode.commands.registerCommand('aiDevOs.compactSprintClosure', async () => {
    const state = monitor.compactClosure();
    refreshAll();
    await notifications.info('sprint-closure-compacted', `AI_DEV_OS compact sprint closure: ${state.compactClosure}`);
  });

  return [
    generateSprintPlan,
    showSprintLifecycle,
    generateNextSprint,
    generateSprintBootstrap,
    showSprintGovernance,
    compactSprintClosure,
  ];
}
