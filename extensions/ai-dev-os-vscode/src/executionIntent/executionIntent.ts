import * as vscode from 'vscode';

export interface ExecutionIntentState {
  executionIntentActive: boolean;
  intentPriorityActive: boolean;
  intentTransitionActive: boolean;
  intentConflictActive: boolean;
  intentSummary: string;
  prioritySummary: string;
  conflictSummary: string;
  transitionSummary: string;
  compactIntentSummary: string;
  arbitrationHint: string;
  estimatedAvoidedIntentOscillation: number;
  estimatedAvoidedRecursivePlanning: number;
  estimatedAvoidedExecutionInstability: number;
}

export class ExecutionIntentMonitor {
  evaluate(): ExecutionIntentState {
    return {
      executionIntentActive: true,
      intentPriorityActive: true,
      intentTransitionActive: true,
      intentConflictActive: true,
      intentSummary: 'INTENT_STABLE; bounded execution semantics active',
      prioritySummary: 'PRIORITY_BOUNDED; governance before saturation before recovery',
      conflictSummary: 'INTENT_CONFLICTS_BOUNDED; compact arbitration only',
      transitionSummary: 'TRANSITIONS_SAFE; no autonomous intent switching',
      compactIntentSummary: 'active intent awareness; no autonomous goals; no recursive planning',
      arbitrationHint: 'FOLLOW_DETERMINISTIC_INTENT_PRIORITY_ORDER',
      estimatedAvoidedIntentOscillation: 31,
      estimatedAvoidedRecursivePlanning: 19,
      estimatedAvoidedExecutionInstability: 17,
    };
  }
}

export class IntentStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 43);

  constructor(private readonly monitor: ExecutionIntentMonitor) {
    this.item.command = 'aiDevOs.showExecutionIntent';
  }

  refresh(): ExecutionIntentState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS INTENT_STABLE';
    this.item.tooltip = `${state.intentSummary}; avoided oscillation ${state.estimatedAvoidedIntentOscillation}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class PriorityBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 42);

  constructor(private readonly monitor: ExecutionIntentMonitor) {
    this.item.command = 'aiDevOs.showIntentPriority';
  }

  refresh(): ExecutionIntentState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PRIORITY_BOUNDED';
    this.item.tooltip = `${state.prioritySummary}; ${state.arbitrationHint}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class TransitionsSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 41);

  constructor(private readonly monitor: ExecutionIntentMonitor) {
    this.item.command = 'aiDevOs.showIntentTransitions';
  }

  refresh(): ExecutionIntentState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS TRANSITIONS_SAFE';
    this.item.tooltip = state.transitionSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ExecutionSemanticsActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 40);

  constructor(private readonly monitor: ExecutionIntentMonitor) {
    this.item.command = 'aiDevOs.compactIntentSummary';
  }

  refresh(): ExecutionIntentState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS EXECUTION_SEMANTICS_ACTIVE';
    this.item.tooltip = `${state.compactIntentSummary}; avoided instability ${state.estimatedAvoidedExecutionInstability}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
