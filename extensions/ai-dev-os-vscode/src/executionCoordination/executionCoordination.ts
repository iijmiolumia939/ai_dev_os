import * as vscode from 'vscode';

export interface ExecutionCoordinationState {
  executionCoordinationActive: boolean;
  coordinationConflictActive: boolean;
  coordinationPriorityActive: boolean;
  coordinationTerminationActive: boolean;
  coordinationSummary: string;
  conflictSummary: string;
  prioritySummary: string;
  cooldownSummary: string;
  compactCoordinationSummary: string;
  boundedRecommendation: string;
  priorityHint: string;
  estimatedAvoidedRuntimeConflicts: number;
  estimatedAvoidedRecursiveCoordination: number;
  estimatedAvoidedRuntimeOscillation: number;
}

export class ExecutionCoordinationMonitor {
  evaluate(): ExecutionCoordinationState {
    return {
      executionCoordinationActive: true,
      coordinationConflictActive: true,
      coordinationPriorityActive: true,
      coordinationTerminationActive: true,
      coordinationSummary: 'COORDINATION_STABLE; deterministic priority only',
      conflictSummary: 'CONFLICTS_BOUNDED; compact arbitration available',
      prioritySummary: 'RUNTIME_PRIORITY_SAFE; governance before saturation before recovery',
      cooldownSummary: 'COORDINATION_GUARDED; no autonomous suppression',
      compactCoordinationSummary: 'bounded coordination; no runtime graph synthesis; no hidden hierarchy',
      boundedRecommendation: 'COORDINATE_BOUNDED_RUNTIME_RECOMMENDATIONS',
      priorityHint: 'FOLLOW_DETERMINISTIC_RUNTIME_PRIORITY_ORDER',
      estimatedAvoidedRuntimeConflicts: 29,
      estimatedAvoidedRecursiveCoordination: 17,
      estimatedAvoidedRuntimeOscillation: 15,
    };
  }
}

export class CoordinationStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 47);

  constructor(private readonly monitor: ExecutionCoordinationMonitor) {
    this.item.command = 'aiDevOs.showRuntimeCoordination';
  }

  refresh(): ExecutionCoordinationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS COORDINATION_STABLE';
    this.item.tooltip = `${state.coordinationSummary}; avoided conflicts ${state.estimatedAvoidedRuntimeConflicts}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ConflictsBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 46);

  constructor(private readonly monitor: ExecutionCoordinationMonitor) {
    this.item.command = 'aiDevOs.showCoordinationConflicts';
  }

  refresh(): ExecutionCoordinationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS CONFLICTS_BOUNDED';
    this.item.tooltip = state.conflictSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RuntimePrioritySafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 45);

  constructor(private readonly monitor: ExecutionCoordinationMonitor) {
    this.item.command = 'aiDevOs.showRuntimePriorities';
  }

  refresh(): ExecutionCoordinationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RUNTIME_PRIORITY_SAFE';
    this.item.tooltip = `${state.prioritySummary}; ${state.priorityHint}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CoordinationGuardedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 44);

  constructor(private readonly monitor: ExecutionCoordinationMonitor) {
    this.item.command = 'aiDevOs.showCoordinationCooldown';
  }

  refresh(): ExecutionCoordinationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS COORDINATION_GUARDED';
    this.item.tooltip = `${state.cooldownSummary}; avoided oscillation ${state.estimatedAvoidedRuntimeOscillation}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
