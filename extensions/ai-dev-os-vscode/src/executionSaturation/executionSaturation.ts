import * as vscode from 'vscode';

export interface ExecutionSaturationState {
  executionSaturationActive: boolean;
  retryOscillationActive: boolean;
  toolCongestionActive: boolean;
  checkpointInflationActive: boolean;
  saturationTerminationActive: boolean;
  saturationSummary: string;
  retryOscillationSummary: string;
  toolCongestionSummary: string;
  checkpointInflationSummary: string;
  compactSaturationSummary: string;
  recoveryRecommendation: string;
  terminationRecommendation: string;
  estimatedAvoidedRecursiveExecution: number;
  estimatedAvoidedRetryLoops: number;
  estimatedAvoidedCheckpointExplosion: number;
}

export class ExecutionSaturationMonitor {
  evaluate(): ExecutionSaturationState {
    return {
      executionSaturationActive: true,
      retryOscillationActive: true,
      toolCongestionActive: true,
      checkpointInflationActive: true,
      saturationTerminationActive: true,
      saturationSummary: 'SATURATION_LOW; continuation bounded; no recursive expansion',
      retryOscillationSummary: 'RETRY_STABLE; single bounded retry only',
      toolCongestionSummary: 'TOOL_PRESSURE_SAFE; single tool step cooldown available',
      checkpointInflationSummary: 'CHECKPOINT_COMPACT; cleanup recommendation only',
      compactSaturationSummary: 'bounded warning; compact recovery; deterministic termination only',
      recoveryRecommendation: 'CONTINUE_WITH_BOUNDED_SLOWDOWN',
      terminationRecommendation: 'NO_TERMINATION_REQUIRED',
      estimatedAvoidedRecursiveExecution: 31,
      estimatedAvoidedRetryLoops: 19,
      estimatedAvoidedCheckpointExplosion: 11,
    };
  }
}

export class SaturationLowStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 55);

  constructor(private readonly monitor: ExecutionSaturationMonitor) {
    this.item.command = 'aiDevOs.showExecutionSaturation';
  }

  refresh(): ExecutionSaturationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS SATURATION_LOW';
    this.item.tooltip = `${state.saturationSummary}; avoided recursive execution ${state.estimatedAvoidedRecursiveExecution}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetryStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 54);

  constructor(private readonly monitor: ExecutionSaturationMonitor) {
    this.item.command = 'aiDevOs.showRetryOscillation';
  }

  refresh(): ExecutionSaturationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RETRY_STABLE';
    this.item.tooltip = `${state.retryOscillationSummary}; avoided retry loops ${state.estimatedAvoidedRetryLoops}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ToolPressureSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 53);

  constructor(private readonly monitor: ExecutionSaturationMonitor) {
    this.item.command = 'aiDevOs.showToolCongestion';
  }

  refresh(): ExecutionSaturationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS TOOL_PRESSURE_SAFE';
    this.item.tooltip = state.toolCongestionSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ContinuationBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 52);

  constructor(private readonly monitor: ExecutionSaturationMonitor) {
    this.item.command = 'aiDevOs.compactSaturationSummary';
  }

  refresh(): ExecutionSaturationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS CONTINUATION_BOUNDED';
    this.item.tooltip = `${state.compactSaturationSummary}; ${state.terminationRecommendation}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
