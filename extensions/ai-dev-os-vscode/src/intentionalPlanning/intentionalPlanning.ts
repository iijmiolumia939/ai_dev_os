import * as vscode from 'vscode';

export interface IntentionalPlanningState {
  intentionalPlanningActive: boolean;
  activeGoalCount: number;
  primaryGoal: string;
  goalHierarchy: string[];
  planningWindowPressure: string;
  planningDecayStatus: string;
  planningInterruptionPressure: string;
  continuationPressure: string;
  compactSummary: string;
}

export class IntentionalPlanningMonitor {
  evaluate(): IntentionalPlanningState {
    return {
      intentionalPlanningActive: true,
      activeGoalCount: 4,
      primaryGoal: 'implement_intentional_planning',
      goalHierarchy: [
        'implement_intentional_planning',
        'validate_runtime',
        'connect_vscode',
        'commit_push',
      ],
      planningWindowPressure: 'MEDIUM',
      planningDecayStatus: 'STABLE',
      planningInterruptionPressure: 'LOW',
      continuationPressure: 'MEDIUM',
      compactSummary: 'bounded intentional planning active; recursive planning blocked',
    };
  }
}

export class GoalActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 16);

  constructor(private readonly monitor: IntentionalPlanningMonitor) {
    this.item.command = 'aiDevOs.showGoalHierarchy';
  }

  refresh(): IntentionalPlanningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS GOAL_ACTIVE';
    this.item.tooltip = `active goals ${state.activeGoalCount}; primary ${state.primaryGoal}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class PlanningBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 15);

  constructor(private readonly monitor: IntentionalPlanningMonitor) {
    this.item.command = 'aiDevOs.showPlanningWindow';
  }

  refresh(): IntentionalPlanningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PLANNING_BOUNDED';
    this.item.tooltip = `planning window pressure ${state.planningWindowPressure}; local patch scope`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class DecayTrackedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 14);

  constructor(private readonly monitor: IntentionalPlanningMonitor) {
    this.item.command = 'aiDevOs.showPlanningDecay';
  }

  refresh(): IntentionalPlanningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS DECAY_TRACKED';
    this.item.tooltip = `planning decay ${state.planningDecayStatus}; interruption ${state.planningInterruptionPressure}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ContinuationStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 13);

  constructor(private readonly monitor: IntentionalPlanningMonitor) {
    this.item.command = 'aiDevOs.showPlanningContinuation';
  }

  refresh(): IntentionalPlanningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS CONTINUATION_STABLE';
    this.item.tooltip = `continuation ${state.continuationPressure}; recursive planning blocked`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
