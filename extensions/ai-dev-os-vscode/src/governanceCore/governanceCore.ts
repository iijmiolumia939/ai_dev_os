import * as vscode from 'vscode';

export interface GovernanceCoreState {
  coreActive: boolean;
  sharedPrimitives: string[];
  reuseTargets: string[];
  retentionLimit: number;
  evictedItems: number;
  compactExportActive: boolean;
  duplicatedGovernanceWarningsReduced: boolean;
  boundedReuseStatus: 'compact' | 'watch';
  summaryOnly: true;
  automaticRewriteUsed: false;
}

export class GovernanceCoreMonitor {
  evaluate(): GovernanceCoreState {
    const sharedPrimitives = [
      'pressure primitives',
      'stale detection primitives',
      'bounded retention primitives',
      'continuity primitives',
      'compact export primitives',
    ];
    const reuseTargets = [
      'governance health',
      'governance trends',
      'persistence governance',
      'session lifecycle',
      'session orchestrator',
      'workspace persistence',
      'context subset',
      'runtime graph',
      'runtime simplification',
    ];
    return {
      coreActive: true,
      sharedPrimitives,
      reuseTargets,
      retentionLimit: 5,
      evictedItems: 3,
      compactExportActive: true,
      duplicatedGovernanceWarningsReduced: true,
      boundedReuseStatus: reuseTargets.length <= 10 ? 'compact' : 'watch',
      summaryOnly: true,
      automaticRewriteUsed: false,
    };
  }
}

export class GovernanceCoreStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 86);

  constructor(private readonly monitor: GovernanceCoreMonitor) {
    this.item.command = 'aiDevOs.showGovernanceCore';
  }

  refresh(): GovernanceCoreState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS Core ${state.boundedReuseStatus.toUpperCase()}`;
    this.item.tooltip = `Shared governance primitives ${state.sharedPrimitives.length}; reuse targets ${state.reuseTargets.length}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}