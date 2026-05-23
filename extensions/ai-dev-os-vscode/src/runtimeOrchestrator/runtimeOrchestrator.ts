import * as vscode from 'vscode';

export interface RuntimeOrchestratorState {
  runtimeOrchestratorActive: boolean;
  orchestrationScheduleScore: number;
  validationScheduleScore: number;
  retryScheduleScore: number;
  continuationScheduleScore: number;
  compactSummary: string;
}

export class RuntimeOrchestratorMonitor {
  evaluate(): RuntimeOrchestratorState {
    return {
      runtimeOrchestratorActive: true,
      orchestrationScheduleScore: 88,
      validationScheduleScore: 95,
      retryScheduleScore: 88,
      continuationScheduleScore: 92,
      compactSummary: 'bounded runtime orchestration active; schedules are deterministic',
    };
  }
}

export class OrchestrationBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -8);

  constructor(private readonly monitor: RuntimeOrchestratorMonitor) {
    this.item.command = 'aiDevOs.showRuntimeOrchestrator';
  }

  refresh(): RuntimeOrchestratorState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ORCHESTRATION_BOUNDED';
    this.item.tooltip = `orchestration ${state.orchestrationScheduleScore}; bounded active ${state.runtimeOrchestratorActive}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class SchedulingStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -9);

  constructor(private readonly monitor: RuntimeOrchestratorMonitor) {
    this.item.command = 'aiDevOs.showValidationSchedule';
  }

  refresh(): RuntimeOrchestratorState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS SCHEDULING_STABLE';
    this.item.tooltip = `validation ${state.validationScheduleScore}; deterministic ordering`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetryOrderedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -10);

  constructor(private readonly monitor: RuntimeOrchestratorMonitor) {
    this.item.command = 'aiDevOs.showRetrySchedule';
  }

  refresh(): RuntimeOrchestratorState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RETRY_ORDERED';
    this.item.tooltip = `retry ${state.retryScheduleScore}; hidden retries blocked`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ContinuationOrderedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -11);

  constructor(private readonly monitor: RuntimeOrchestratorMonitor) {
    this.item.command = 'aiDevOs.showContinuationSchedule';
  }

  refresh(): RuntimeOrchestratorState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS CONTINUATION_ORDERED';
    this.item.tooltip = `continuation ${state.continuationScheduleScore}; depth bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
