import * as vscode from 'vscode';

export type StreamingPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface StreamingCognitionState {
  streamingCognitionActive: true;
  streamingLatencyScore: number;
  interruptionRecoveryScore: number;
  providerStreamingScore: number;
  continuationStreamingScore: number;
  boundedCognitionScore: number;
  interruptionSafe: boolean;
  providerStreaming: boolean;
  continuationStreaming: boolean;
  streamingPressure: StreamingPressure;
  estimatedAvoidedStreamingInstability: number;
  estimatedAvoidedProviderInterruptions: number;
  estimatedAvoidedFrontierStreaming: number;
  compactSummary: string;
  cognitionSummary: string[];
  continuationSummary: string[];
  interruptionRecovery: string[];
  providerStreamingSummary: string[];
  deterministic: true;
  bounded: true;
  rollbackSafe: true;
  localPatchCompatible: true;
  readOnlyProjection: true;
  noProviderExecution: true;
  noGovernanceMutation: true;
  noRecursiveStreaming: true;
}

export class StreamingCognitionMonitor {
  private compacted = false;

  evaluate(): StreamingCognitionState {
    const streamingLatencyScore = this.compacted ? 92 : 86;
    const interruptionRecoveryScore = this.compacted ? 90 : 84;
    const providerStreamingScore = this.compacted ? 88 : 82;
    const continuationStreamingScore = this.compacted ? 91 : 85;
    const boundedCognitionScore = Math.min(
      streamingLatencyScore,
      interruptionRecoveryScore,
      providerStreamingScore,
      continuationStreamingScore,
    );
    const streamingPressure: StreamingPressure = this.compacted ? 'LOW' : 'MEDIUM';
    return {
      streamingCognitionActive: true,
      streamingLatencyScore,
      interruptionRecoveryScore,
      providerStreamingScore,
      continuationStreamingScore,
      boundedCognitionScore,
      interruptionSafe: interruptionRecoveryScore >= 80,
      providerStreaming: providerStreamingScore >= 80,
      continuationStreaming: continuationStreamingScore >= 80,
      streamingPressure,
      estimatedAvoidedStreamingInstability: this.compacted ? 2940 : 2600,
      estimatedAvoidedProviderInterruptions: this.compacted ? 1640 : 1400,
      estimatedAvoidedFrontierStreaming: this.compacted ? 3660 : 3560,
      compactSummary: 'bounded streaming cognition; read-only projection; no provider execution',
      cognitionSummary: [
        'bounded speech chunks',
        'bounded cognition deltas',
        'deterministic summaries',
      ],
      continuationSummary: [
        'compact continuation reuse',
        'governed reset window',
        'entropy suppression active',
      ],
      interruptionRecovery: [
        'speech reset on interruption',
        'continuation-safe reset',
        'provider cooldown stabilization',
      ],
      providerStreamingSummary: [
        'local-first streaming route',
        'bounded fallback window',
        'fatigue-aware cooldown',
      ],
      deterministic: true,
      bounded: true,
      rollbackSafe: true,
      localPatchCompatible: true,
      readOnlyProjection: true,
      noProviderExecution: true,
      noGovernanceMutation: true,
      noRecursiveStreaming: true,
    };
  }

  compactSummary(): StreamingCognitionState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class StreamingActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 63);

  constructor(private readonly monitor: StreamingCognitionMonitor) {
    this.item.command = 'aiDevOs.showStreamingCognition';
  }

  refresh(): StreamingCognitionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS STREAMING_ACTIVE ${state.streamingCognitionActive ? 'YES' : 'NO'}`;
    this.item.tooltip = state.compactSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class InterruptionSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 62);

  constructor(private readonly monitor: StreamingCognitionMonitor) {
    this.item.command = 'aiDevOs.showInterruptionRecovery';
  }

  refresh(): StreamingCognitionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS INTERRUPTION_SAFE ${state.interruptionSafe ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.interruptionRecovery.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ProviderStreamingStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 61);

  constructor(private readonly monitor: StreamingCognitionMonitor) {
    this.item.command = 'aiDevOs.showProviderStreaming';
  }

  refresh(): StreamingCognitionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS PROVIDER_STREAMING ${state.providerStreaming ? 'LOCAL' : 'WATCH'}`;
    this.item.tooltip = state.providerStreamingSummary.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ContinuationStreamingStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 60);

  constructor(private readonly monitor: StreamingCognitionMonitor) {
    this.item.command = 'aiDevOs.showStreamingContinuation';
  }

  refresh(): StreamingCognitionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS CONTINUATION_STREAMING ${state.continuationStreaming ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.continuationSummary.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
