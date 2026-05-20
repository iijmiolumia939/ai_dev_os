import * as vscode from 'vscode';

export interface RuntimeGraphState {
  nodeCount: number;
  edgeCount: number;
  dependencyDensity: number;
  architecturePressure: 'low' | 'medium' | 'high';
  contractSurfaceSize: number;
  runtimeApiPressure: 'low' | 'medium' | 'high';
  clusterSizes: Record<string, number>;
  oversizedRuntimes: string[];
  crossBoundaryWarnings: string[];
  isolatedClusters: string[];
  simplificationRecommended: boolean;
  summaryOnly: true;
  hiddenSignalExportUsed: false;
}

const runtimeCategories: Record<string, string[]> = {
  governance: ['governance_health', 'governance_trends', 'persistence_governance'],
  retrieval: ['retrieval', 'context_subset'],
  persistence: ['workspace_persistence'],
  orchestration: ['session_orchestrator', 'session_lifecycle', 'session_boundary'],
  provider: ['providers'],
  vscode: ['vscode_integration', 'ai-dev-os-vscode'],
  cognition: ['repository_intelligence', 'workspace_snapshot'],
  adapters: ['integrations'],
};

export class RuntimeGraphMonitor {
  private compacted = false;

  evaluate(): RuntimeGraphState {
    const clusterSizes = Object.fromEntries(
      Object.entries(runtimeCategories).map(([category, runtimes]) => [category, runtimes.length]),
    );
    const nodeCount = Object.values(clusterSizes).reduce((total, count) => total + count, 0);
    const edgeCount = this.compacted ? 8 : 11;
    const density = Number((edgeCount / Math.max(1, nodeCount)).toFixed(4));
    const oversizedRuntimes = Object.entries(clusterSizes)
      .filter(([, count]) => count > 3)
      .map(([category]) => category);
    const crossBoundaryWarnings = density > 0.75 ? ['runtime cross-boundary review recommended'] : [];
    const architecturePressure = density > 0.85 ? 'high' : density > 0.55 ? 'medium' : 'low';
    const contractSurfaceSize = nodeCount * 3;
    const runtimeApiPressure = contractSurfaceSize > 48 ? 'high' : contractSurfaceSize > 24 ? 'medium' : 'low';
    return {
      nodeCount,
      edgeCount,
      dependencyDensity: density,
      architecturePressure,
      contractSurfaceSize,
      runtimeApiPressure,
      clusterSizes,
      oversizedRuntimes,
      crossBoundaryWarnings,
      isolatedClusters: [],
      simplificationRecommended: oversizedRuntimes.length > 0 || architecturePressure === 'high',
      summaryOnly: true,
      hiddenSignalExportUsed: false,
    };
  }

  compact(): RuntimeGraphState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class ArchitecturePressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 88);

  constructor(private readonly monitor: RuntimeGraphMonitor) {
    this.item.command = 'aiDevOs.showArchitecturePressure';
  }

  refresh(): RuntimeGraphState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS Arch ${state.architecturePressure.toUpperCase()}`;
    this.item.tooltip = `Runtime graph ${state.nodeCount} nodes / ${state.edgeCount} edges; contract ${state.runtimeApiPressure}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}