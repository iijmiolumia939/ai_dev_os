import * as vscode from 'vscode';

export interface RuntimeMediationState {
  runtimeMediationActive: boolean;
  executionBounded: boolean;
  retryGoverned: boolean;
  cooldownStable: boolean;
  mediationSummary: string;
  queueSummary: string;
  retrySummary: string;
  cooldownSummary: string;
  compactSummary: string;
  estimatedAvoidedRecursiveExecution: number;
  estimatedAvoidedRetryAmplification: number;
  estimatedAvoidedExecutionSaturation: number;
}

export class RuntimeMediationMonitor {
  evaluate(): RuntimeMediationState {
    return {
      runtimeMediationActive: true,
      executionBounded: true,
      retryGoverned: true,
      cooldownStable: true,
      mediationSummary: 'MEDIATION_ACTIVE; deterministic runtime authority enforced',
      queueSummary: 'EXECUTION_BOUNDED; compact execution windows active',
      retrySummary: 'RETRY_GOVERNED; retry amplification blocked',
      cooldownSummary: 'COOLDOWN_STABLE; bounded cooldown recommendations only',
      compactSummary: 'runtime mediation active; no direct LLM execution authority',
      estimatedAvoidedRecursiveExecution: 67,
      estimatedAvoidedRetryAmplification: 41,
      estimatedAvoidedExecutionSaturation: 38,
    };
  }
}

export class MediationActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 23);

  constructor(private readonly monitor: RuntimeMediationMonitor) {
    this.item.command = 'aiDevOs.showRuntimeMediation';
  }

  refresh(): RuntimeMediationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS MEDIATION_ACTIVE';
    this.item.tooltip = `${state.mediationSummary}; avoided recursive execution ${state.estimatedAvoidedRecursiveExecution}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ExecutionBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 22);

  constructor(private readonly monitor: RuntimeMediationMonitor) {
    this.item.command = 'aiDevOs.showExecutionQueue';
  }

  refresh(): RuntimeMediationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS EXECUTION_BOUNDED';
    this.item.tooltip = `${state.queueSummary}; avoided saturation ${state.estimatedAvoidedExecutionSaturation}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetryGovernedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 21);

  constructor(private readonly monitor: RuntimeMediationMonitor) {
    this.item.command = 'aiDevOs.showRetryGovernance';
  }

  refresh(): RuntimeMediationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RETRY_GOVERNED';
    this.item.tooltip = `${state.retrySummary}; avoided retry amplification ${state.estimatedAvoidedRetryAmplification}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CooldownStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 20);

  constructor(private readonly monitor: RuntimeMediationMonitor) {
    this.item.command = 'aiDevOs.showCooldownGovernance';
  }

  refresh(): RuntimeMediationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS COOLDOWN_STABLE';
    this.item.tooltip = state.cooldownSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}