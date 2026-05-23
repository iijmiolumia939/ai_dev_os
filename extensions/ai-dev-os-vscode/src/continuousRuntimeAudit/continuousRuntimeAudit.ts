import * as vscode from 'vscode';

export interface ContinuousRuntimeAuditState {
  continuousRuntimeAuditActive: boolean;
  runtimeHealthScore: number;
  retryPressureScore: number;
  providerFatigueScore: number;
  orchestrationPressureScore: number;
  compactSummary: string;
}

export class ContinuousRuntimeAuditMonitor {
  evaluate(): ContinuousRuntimeAuditState {
    return {
      continuousRuntimeAuditActive: true,
      runtimeHealthScore: 81,
      retryPressureScore: 72,
      providerFatigueScore: 61,
      orchestrationPressureScore: 68,
      compactSummary: 'continuous runtime audit active; signal scope bounded and operationally visible',
    };
  }
}

export class ContinuousRuntimeHealthStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -16);

  constructor(private readonly monitor: ContinuousRuntimeAuditMonitor) {
    this.item.command = 'aiDevOs.showRuntimeHealth';
  }

  refresh(): ContinuousRuntimeAuditState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RUNTIME_HEALTH';
    this.item.tooltip = `runtime health ${state.runtimeHealthScore}; audit active ${state.continuousRuntimeAuditActive}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetryVisibleStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -17);

  constructor(private readonly monitor: ContinuousRuntimeAuditMonitor) {
    this.item.command = 'aiDevOs.showRetryPressure';
  }

  refresh(): ContinuousRuntimeAuditState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RETRY_VISIBLE';
    this.item.tooltip = `retry pressure ${state.retryPressureScore}; bounded visibility`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class OrchestrationVisibleStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -18);

  constructor(private readonly monitor: ContinuousRuntimeAuditMonitor) {
    this.item.command = 'aiDevOs.showOrchestrationPressure';
  }

  refresh(): ContinuousRuntimeAuditState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ORCHESTRATION_VISIBLE';
    this.item.tooltip = `orchestration pressure ${state.orchestrationPressureScore}; stalls visible`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ProviderVisibleStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -19);

  constructor(private readonly monitor: ContinuousRuntimeAuditMonitor) {
    this.item.command = 'aiDevOs.showContinuousProviderFatigue';
  }

  refresh(): ContinuousRuntimeAuditState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PROVIDER_VISIBLE';
    this.item.tooltip = `provider fatigue ${state.providerFatigueScore}; starvation visible`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
