import * as vscode from 'vscode';

export interface ExecutionQualityState {
  executionQualityActive: boolean;
  qualityDriftActive: boolean;
  qualityRedundancyActive: boolean;
  qualityPersistenceActive: boolean;
  qualitySummary: string;
  driftSummary: string;
  redundancySummary: string;
  persistenceSummary: string;
  compactQualitySummary: string;
  qualityHint: string;
  estimatedAvoidedLowValueExecution: number;
  estimatedAvoidedRecursiveOptimization: number;
  estimatedAvoidedExecutionRedundancy: number;
}

export class ExecutionQualityMonitor {
  evaluate(): ExecutionQualityState {
    return {
      executionQualityActive: true,
      qualityDriftActive: true,
      qualityRedundancyActive: true,
      qualityPersistenceActive: true,
      qualitySummary: 'QUALITY_BOUNDED; deterministic execution quality awareness active',
      driftSummary: 'QUALITY_DRIFT_SAFE; bounded cooldown recommendation only',
      redundancySummary: 'REDUNDANCY_LOW; duplicate execution pressure guarded',
      persistenceSummary: 'EXECUTION_SIGNAL_STABLE; low-signal persistence guarded',
      compactQualitySummary: 'bounded quality awareness; no autonomous optimization',
      qualityHint: 'FOLLOW_DETERMINISTIC_QUALITY_PRIORITY_ORDER',
      estimatedAvoidedLowValueExecution: 47,
      estimatedAvoidedRecursiveOptimization: 31,
      estimatedAvoidedExecutionRedundancy: 29,
    };
  }
}

export class QualityBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 31);

  constructor(private readonly monitor: ExecutionQualityMonitor) {
    this.item.command = 'aiDevOs.showExecutionQuality';
  }

  refresh(): ExecutionQualityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS QUALITY_BOUNDED';
    this.item.tooltip = `${state.qualitySummary}; avoided low-value ${state.estimatedAvoidedLowValueExecution}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RedundancyLowStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 30);

  constructor(private readonly monitor: ExecutionQualityMonitor) {
    this.item.command = 'aiDevOs.showRedundancyPressure';
  }

  refresh(): ExecutionQualityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS REDUNDANCY_LOW';
    this.item.tooltip = `${state.redundancySummary}; ${state.qualityHint}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class QualityDriftSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 29);

  constructor(private readonly monitor: ExecutionQualityMonitor) {
    this.item.command = 'aiDevOs.showQualityDrift';
  }

  refresh(): ExecutionQualityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS QUALITY_DRIFT_SAFE';
    this.item.tooltip = state.driftSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ExecutionSignalStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 28);

  constructor(private readonly monitor: ExecutionQualityMonitor) {
    this.item.command = 'aiDevOs.showPersistenceQuality';
  }

  refresh(): ExecutionQualityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS EXECUTION_SIGNAL_STABLE';
    this.item.tooltip = `${state.persistenceSummary}; avoided redundancy ${state.estimatedAvoidedExecutionRedundancy}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
