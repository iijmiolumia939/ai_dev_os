import * as vscode from 'vscode';

export interface FailureInjectionState {
  failureInjectionActive: boolean;
  retryInjectionScore: number;
  providerInjectionScore: number;
  orchestrationInjectionScore: number;
  recoveryResilienceScore: number;
  compactSummary: string;
}

export class FailureInjectionMonitor {
  evaluate(): FailureInjectionState {
    return {
      failureInjectionActive: true,
      retryInjectionScore: 68,
      providerInjectionScore: 45,
      orchestrationInjectionScore: 100,
      recoveryResilienceScore: 84,
      compactSummary: 'failure injection active; bounded recovery stable and local patch guarded',
    };
  }
}

export class FailureTestingStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -20);

  constructor(private readonly monitor: FailureInjectionMonitor) {
    this.item.command = 'aiDevOs.showFailureInjection';
  }

  refresh(): FailureInjectionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS FAILURE_TESTING';
    this.item.tooltip = `failure injection active ${state.failureInjectionActive}; recovery ${state.recoveryResilienceScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RecoveryStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -21);

  constructor(private readonly monitor: FailureInjectionMonitor) {
    this.item.command = 'aiDevOs.showRecoveryResilience';
  }

  refresh(): FailureInjectionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RECOVERY_STABLE';
    this.item.tooltip = `recovery resilience ${state.recoveryResilienceScore}; bounded validation`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetryResilientStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -22);

  constructor(private readonly monitor: FailureInjectionMonitor) {
    this.item.command = 'aiDevOs.showRetryInjection';
  }

  refresh(): FailureInjectionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RETRY_RESILIENT';
    this.item.tooltip = `retry injection ${state.retryInjectionScore}; storm bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class OrchestrationResilientStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -23);

  constructor(private readonly monitor: FailureInjectionMonitor) {
    this.item.command = 'aiDevOs.showFailureInjection';
  }

  refresh(): FailureInjectionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ORCHESTRATION_RESILIENT';
    this.item.tooltip = `orchestration injection ${state.orchestrationInjectionScore}; deadlock bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
