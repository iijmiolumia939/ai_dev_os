import * as vscode from 'vscode';

export type ReplayPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface IncrementalContextState {
  incrementalContextActive: boolean;
  contextDeltaActive: boolean;
  deltaRetrievalActive: boolean;
  auditDeltaActive: boolean;
  replayPressure: ReplayPressure;
  compactChangedNeighborhood: string[];
  unchangedContextExcluded: string[];
  estimatedAvoidedRepeatedInputTokens: number;
  estimatedAvoidedDuplicateRuntimeCognition: number;
  localOnly: true;
  deterministic: true;
  summaryOnly: true;
  boundedRetention: true;
  repoWideReplayForbidden: true;
}

const changedNeighborhood = ['incremental_context', 'runtime_audit', 'retrieval_budget'];
const excludedContext = ['provider_simulation', 'release_readiness', 'consumer_rollout'];

export class IncrementalContextMonitor {
  private compacted = false;

  evaluate(): IncrementalContextState {
    const compactChangedNeighborhood = this.compacted ? changedNeighborhood.slice(0, 2) : changedNeighborhood;
    const pressure: ReplayPressure = excludedContext.length > 2 ? 'HIGH' : 'MEDIUM';
    return {
      incrementalContextActive: true,
      contextDeltaActive: true,
      deltaRetrievalActive: true,
      auditDeltaActive: true,
      replayPressure: pressure,
      compactChangedNeighborhood,
      unchangedContextExcluded: excludedContext,
      estimatedAvoidedRepeatedInputTokens: 3400,
      estimatedAvoidedDuplicateRuntimeCognition: 5,
      localOnly: true,
      deterministic: true,
      summaryOnly: true,
      boundedRetention: true,
      repoWideReplayForbidden: true,
    };
  }

  compactContext(): IncrementalContextState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class IncrementalContextStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 79);

  constructor(private readonly monitor: IncrementalContextMonitor) {
    this.item.command = 'aiDevOs.showContextDelta';
  }

  refresh(): IncrementalContextState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS DELTA_CONTEXT${state.replayPressure === 'LOW' ? '' : ' REPLAY_PRESSURE'}`;
    this.item.tooltip = `Delta context ${state.compactChangedNeighborhood.length} changed runtimes; replay ${state.replayPressure}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
