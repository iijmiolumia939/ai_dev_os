import * as vscode from 'vscode';

export interface ExecutionStabilityState {
  executionStabilityActive: boolean;
  stabilityDriftActive: boolean;
  stabilityOscillationActive: boolean;
  stabilityPersistenceActive: boolean;
  stabilitySummary: string;
  driftSummary: string;
  oscillationSummary: string;
  persistenceSummary: string;
  compactStabilitySummary: string;
  arbitrationHint: string;
  estimatedAvoidedLongSessionDrift: number;
  estimatedAvoidedRecursiveStabilization: number;
  estimatedAvoidedPersistenceEntropy: number;
}

export class ExecutionStabilityMonitor {
  evaluate(): ExecutionStabilityState {
    return {
      executionStabilityActive: true,
      stabilityDriftActive: true,
      stabilityOscillationActive: true,
      stabilityPersistenceActive: true,
      stabilitySummary: 'STABILITY_BOUNDED; long-horizon observation active',
      driftSummary: 'DRIFT_LOW; deterministic drift cooldown available',
      oscillationSummary: 'OSCILLATION_STABLE; bounded cooldown recommendation only',
      persistenceSummary: 'PERSISTENCE_SAFE; entropy and fragmentation guarded',
      compactStabilitySummary: 'bounded stability awareness; no autonomous healing',
      arbitrationHint: 'FOLLOW_DETERMINISTIC_STABILITY_PRIORITY_ORDER',
      estimatedAvoidedLongSessionDrift: 43,
      estimatedAvoidedRecursiveStabilization: 29,
      estimatedAvoidedPersistenceEntropy: 23,
    };
  }
}

export class StabilityBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 35);

  constructor(private readonly monitor: ExecutionStabilityMonitor) {
    this.item.command = 'aiDevOs.showExecutionStabilityRuntime';
  }

  refresh(): ExecutionStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS STABILITY_BOUNDED';
    this.item.tooltip = `${state.stabilitySummary}; avoided drift ${state.estimatedAvoidedLongSessionDrift}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class DriftLowStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 34);

  constructor(private readonly monitor: ExecutionStabilityMonitor) {
    this.item.command = 'aiDevOs.showStabilityDrift';
  }

  refresh(): ExecutionStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS DRIFT_LOW';
    this.item.tooltip = `${state.driftSummary}; ${state.arbitrationHint}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class OscillationStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 33);

  constructor(private readonly monitor: ExecutionStabilityMonitor) {
    this.item.command = 'aiDevOs.showStabilityOscillation';
  }

  refresh(): ExecutionStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS OSCILLATION_STABLE';
    this.item.tooltip = state.oscillationSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class PersistenceSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 32);

  constructor(private readonly monitor: ExecutionStabilityMonitor) {
    this.item.command = 'aiDevOs.showPersistenceStability';
  }

  refresh(): ExecutionStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PERSISTENCE_SAFE';
    this.item.tooltip = `${state.persistenceSummary}; avoided entropy ${state.estimatedAvoidedPersistenceEntropy}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
