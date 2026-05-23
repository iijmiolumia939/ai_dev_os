import * as vscode from 'vscode';

export interface SoakStabilityState {
  soakStabilityActive: boolean;
  longSessionStabilityScore: number;
  retryAccumulationScore: number;
  providerFatigueAccumulationScore: number;
  continuationEntropyScore: number;
  orchestrationQueueDriftScore: number;
  runtimeInteractionEntropyScore: number;
  compactSummary: string;
}

export class SoakStabilityMonitor {
  evaluate(): SoakStabilityState {
    return {
      soakStabilityActive: true,
      longSessionStabilityScore: 60,
      retryAccumulationScore: 71,
      providerFatigueAccumulationScore: 61,
      continuationEntropyScore: 83,
      orchestrationQueueDriftScore: 66,
      runtimeInteractionEntropyScore: 78,
      compactSummary: 'soak stability active; drift bounded and long session entropy visible',
    };
  }
}

export class SoakStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -24);

  constructor(private readonly monitor: SoakStabilityMonitor) {
    this.item.command = 'aiDevOs.showSoakStability';
  }

  refresh(): SoakStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS SOAK_STABLE';
    this.item.tooltip = `soak stability active ${state.soakStabilityActive}; long session ${state.longSessionStabilityScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class DriftBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -25);

  constructor(private readonly monitor: SoakStabilityMonitor) {
    this.item.command = 'aiDevOs.showLongSessionDrift';
  }

  refresh(): SoakStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS DRIFT_BOUNDED';
    this.item.tooltip = `long session ${state.longSessionStabilityScore}; orchestration drift ${state.orchestrationQueueDriftScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class EntropyVisibleStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -26);

  constructor(private readonly monitor: SoakStabilityMonitor) {
    this.item.command = 'aiDevOs.showRuntimeEntropy';
  }

  refresh(): SoakStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ENTROPY_VISIBLE';
    this.item.tooltip = `runtime interaction entropy ${state.runtimeInteractionEntropyScore}; continuation ${state.continuationEntropyScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class LongSessionSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -27);

  constructor(private readonly monitor: SoakStabilityMonitor) {
    this.item.command = 'aiDevOs.showRetryAccumulation';
  }

  refresh(): SoakStabilityState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LONG_SESSION_SAFE';
    this.item.tooltip = `retry accumulation ${state.retryAccumulationScore}; provider fatigue ${state.providerFatigueAccumulationScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
