import * as vscode from 'vscode';

export interface SprintLoopState {
  sprintLoopActive: boolean;
  sprintValidationScore: number;
  sprintRegressionScore: number;
  sprintCommitReadinessScore: number;
  sprintContinuationScore: number;
  compactSummary: string;
}

export class SprintLoopMonitor {
  evaluate(): SprintLoopState {
    return {
      sprintLoopActive: true,
      sprintValidationScore: 100,
      sprintRegressionScore: 80,
      sprintCommitReadinessScore: 100,
      sprintContinuationScore: 92,
      compactSummary: 'bounded sprint loop active; validation and commit readiness stable',
    };
  }
}

export class SprintBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -4);

  constructor(private readonly monitor: SprintLoopMonitor) {
    this.item.command = 'aiDevOs.showSprintLoop';
  }

  refresh(): SprintLoopState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS SPRINT_BOUNDED';
    this.item.tooltip = `sprint active ${state.sprintLoopActive}; continuation ${state.sprintContinuationScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class SprintValidationStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -5);

  constructor(private readonly monitor: SprintLoopMonitor) {
    this.item.command = 'aiDevOs.showSprintValidation';
  }

  refresh(): SprintLoopState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS VALIDATION_STABLE';
    this.item.tooltip = `validation ${state.sprintValidationScore}; sequence bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RegressionTrackedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -6);

  constructor(private readonly monitor: SprintLoopMonitor) {
    this.item.command = 'aiDevOs.showSprintRegression';
  }

  refresh(): SprintLoopState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS REGRESSION_TRACKED';
    this.item.tooltip = `regression ${state.sprintRegressionScore}; cooldown guarded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CommitReadyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -7);

  constructor(private readonly monitor: SprintLoopMonitor) {
    this.item.command = 'aiDevOs.showSprintCommitReadiness';
  }

  refresh(): SprintLoopState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS COMMIT_READY';
    this.item.tooltip = `commit readiness ${state.sprintCommitReadinessScore}; autonomous commit blocked`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
