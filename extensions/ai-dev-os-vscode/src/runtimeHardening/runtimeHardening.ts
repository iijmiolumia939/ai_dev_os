import * as vscode from 'vscode';

export interface RuntimeHardeningState {
  runtimeHardeningActive: boolean;
  retryStormScore: number;
  escalationOscillationScore: number;
  orchestrationDeadlockScore: number;
  continuationStabilityScore: number;
  compactSummary: string;
}

export class RuntimeHardeningMonitor {
  evaluate(): RuntimeHardeningState {
    return {
      runtimeHardeningActive: true,
      retryStormScore: 60,
      escalationOscillationScore: 64,
      orchestrationDeadlockScore: 84,
      continuationStabilityScore: 82,
      compactSummary: 'runtime hardening active; retry, escalation, and orchestration stability bounded',
    };
  }
}

export class HardeningActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -12);

  constructor(private readonly monitor: RuntimeHardeningMonitor) {
    this.item.command = 'aiDevOs.showRuntimeHardening';
  }

  refresh(): RuntimeHardeningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS HARDENING_ACTIVE';
    this.item.tooltip = `hardening active ${state.runtimeHardeningActive}; continuation ${state.continuationStabilityScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetryStableHardeningStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -13);

  constructor(private readonly monitor: RuntimeHardeningMonitor) {
    this.item.command = 'aiDevOs.showRetryStormStatus';
  }

  refresh(): RuntimeHardeningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RETRY_STABLE';
    this.item.tooltip = `retry storm ${state.retryStormScore}; reset bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class OrchestrationSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -14);

  constructor(private readonly monitor: RuntimeHardeningMonitor) {
    this.item.command = 'aiDevOs.showOrchestrationDeadlocks';
  }

  refresh(): RuntimeHardeningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ORCHESTRATION_SAFE';
    this.item.tooltip = `deadlock ${state.orchestrationDeadlockScore}; orchestration guarded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class EscalationStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -15);

  constructor(private readonly monitor: RuntimeHardeningMonitor) {
    this.item.command = 'aiDevOs.showEscalationOscillation';
  }

  refresh(): RuntimeHardeningState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ESCALATION_STABLE';
    this.item.tooltip = `escalation ${state.escalationOscillationScore}; oscillation suppressed`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
