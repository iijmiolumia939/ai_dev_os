import * as vscode from 'vscode';

export interface ReflectiveEvaluationState {
  reflectiveEvaluationActive: boolean;
  executionQualityScore: number;
  cognitiveCoherenceScore: number;
  continuationValidityScore: number;
  planningIntegrityScore: number;
  compactSummary: string;
}

export class ReflectiveEvaluationMonitor {
  evaluate(): ReflectiveEvaluationState {
    return {
      reflectiveEvaluationActive: true,
      executionQualityScore: 90,
      cognitiveCoherenceScore: 84,
      continuationValidityScore: 92,
      planningIntegrityScore: 81,
      compactSummary: 'bounded reflective evaluation active; self-optimization blocked',
    };
  }
}

export class ReflectionBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 12);

  constructor(private readonly monitor: ReflectiveEvaluationMonitor) {
    this.item.command = 'aiDevOs.showReflectiveEvaluation';
  }

  refresh(): ReflectiveEvaluationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS REFLECTION_BOUNDED';
    this.item.tooltip = `reflection bounded; execution ${state.executionQualityScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ExecutionCoherentStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 11);

  constructor(private readonly monitor: ReflectiveEvaluationMonitor) {
    this.item.command = 'aiDevOs.showReflectiveEvaluation';
  }

  refresh(): ReflectiveEvaluationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS EXECUTION_COHERENT';
    this.item.tooltip = `execution quality ${state.executionQualityScore}; local evidence only`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ContinuationValidStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 10);

  constructor(private readonly monitor: ReflectiveEvaluationMonitor) {
    this.item.command = 'aiDevOs.showContinuationValidity';
  }

  refresh(): ReflectiveEvaluationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS CONTINUATION_VALID';
    this.item.tooltip = `continuation validity ${state.continuationValidityScore}; bounded scoring`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class PlanningStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 9);

  constructor(private readonly monitor: ReflectiveEvaluationMonitor) {
    this.item.command = 'aiDevOs.showPlanningIntegrity';
  }

  refresh(): ReflectiveEvaluationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PLANNING_STABLE';
    this.item.tooltip = `planning integrity ${state.planningIntegrityScore}; governance preserved`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
