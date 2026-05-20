import * as vscode from 'vscode';

export type RetrievalPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface RetrievalBudgetState {
  retrievalBudgetActive: boolean;
  retrievalPressure: RetrievalPressure;
  maxRuntimeCount: number;
  maxContractCount: number;
  maxDependencyDistance: number;
  compactNeighborhood: string[];
  boundedContractAdjacency: string[];
  compactRetrievalRecommendation: boolean;
  estimatedAvoidedHiddenInputTokens: number;
  estimatedAvoidedRepoWideReasoning: number;
  repoWideRetrievalForbidden: true;
  localOnly: true;
  deterministic: true;
  summaryOnly: true;
}

const defaultNeighborhood = ['session_orchestrator', 'retrieval', 'context_subset'];

export class RetrievalBudgetMonitor {
  private compacted = false;

  evaluate(): RetrievalBudgetState {
    const compactNeighborhood = this.compacted ? defaultNeighborhood.slice(0, 2) : defaultNeighborhood;
    const pressure = compactNeighborhood.length > 4 ? 'HIGH' : compactNeighborhood.length > 2 ? 'MEDIUM' : 'LOW';
    return {
      retrievalBudgetActive: true,
      retrievalPressure: pressure,
      maxRuntimeCount: 5,
      maxContractCount: 8,
      maxDependencyDistance: 2,
      compactNeighborhood,
      boundedContractAdjacency: ['continuity', 'scope'],
      compactRetrievalRecommendation: pressure !== 'LOW',
      estimatedAvoidedHiddenInputTokens: 1600,
      estimatedAvoidedRepoWideReasoning: 1920,
      repoWideRetrievalForbidden: true,
      localOnly: true,
      deterministic: true,
      summaryOnly: true,
    };
  }

  compactScope(): RetrievalBudgetState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class RetrievalBudgetStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 80);

  constructor(private readonly monitor: RetrievalBudgetMonitor) {
    this.item.command = 'aiDevOs.showRetrievalBudget';
  }

  refresh(): RetrievalBudgetState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS RETRIEVAL_BUDGET${state.retrievalPressure === 'LOW' ? '' : ' RETRIEVAL_PRESSURE'}`;
    this.item.tooltip = `Retrieval ${state.compactNeighborhood.length}/${state.maxRuntimeCount} runtimes; pressure ${state.retrievalPressure}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}