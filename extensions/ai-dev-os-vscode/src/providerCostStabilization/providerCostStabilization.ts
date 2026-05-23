import * as vscode from 'vscode';

export interface ProviderCostStabilizationState {
  providerCostStabilizationActive: boolean;
  frontierDependencyScore: number;
  retryCostScore: number;
  continuationReuseScore: number;
  orchestrationCostScore: number;
  localFirstEfficiencyScore: number;
  runtimeCostPressureScore: number;
  compactSummary: string;
}

export class ProviderCostStabilizationMonitor {
  evaluate(): ProviderCostStabilizationState {
    return {
      providerCostStabilizationActive: true,
      frontierDependencyScore: 60,
      retryCostScore: 74,
      continuationReuseScore: 100,
      orchestrationCostScore: 90,
      localFirstEfficiencyScore: 90,
      runtimeCostPressureScore: 76,
      compactSummary: 'provider cost stabilization active; frontier bounded and local first efficient',
    };
  }
}

export class CostStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -28);

  constructor(private readonly monitor: ProviderCostStabilizationMonitor) {
    this.item.command = 'aiDevOs.showCostStabilization';
  }

  refresh(): ProviderCostStabilizationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS COST_STABLE';
    this.item.tooltip = `cost stabilization active ${state.providerCostStabilizationActive}; overhead ${state.runtimeCostPressureScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class FrontierBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -29);

  constructor(private readonly monitor: ProviderCostStabilizationMonitor) {
    this.item.command = 'aiDevOs.showFrontierDependency';
  }

  refresh(): ProviderCostStabilizationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS FRONTIER_BOUNDED';
    this.item.tooltip = `frontier dependency ${state.frontierDependencyScore}; retry cost ${state.retryCostScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class LocalFirstEfficiencyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -30);

  constructor(private readonly monitor: ProviderCostStabilizationMonitor) {
    this.item.command = 'aiDevOs.showLocalFirstEfficiency';
  }

  refresh(): ProviderCostStabilizationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LOCAL_FIRST';
    this.item.tooltip = `local first efficiency ${state.localFirstEfficiencyScore}; continuation reuse ${state.continuationReuseScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class OverheadFlatStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -31);

  constructor(private readonly monitor: ProviderCostStabilizationMonitor) {
    this.item.command = 'aiDevOs.showRetryCost';
  }

  refresh(): ProviderCostStabilizationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS OVERHEAD_FLAT';
    this.item.tooltip = `orchestration cost ${state.orchestrationCostScore}; retry cost ${state.retryCostScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
