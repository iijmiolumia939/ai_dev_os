import * as vscode from 'vscode';

export type StrategyPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface DevelopmentStrategyState {
  devStrategyActive: true;
  strategyStable: boolean;
  costPressure: StrategyPressure;
  providerEfficiency: 'LOW' | 'MEDIUM' | 'HIGH';
  roadmapPressure: StrategyPressure;
  providerRoutingDistribution: {providerClass: 'HIGH' | 'MEDIUM' | 'LOW'; count: number}[];
  estimatedAvoidedStrategyOverhead: number;
  estimatedAvoidedRoadmapExplosion: number;
  compactSummary: string;
  costHints: string[];
  governanceHints: string[];
  providerHints: string[];
  sprintDensityHints: string[];
  localOnly: true;
  deterministic: true;
  summaryOnly: true;
  boundedStrategyOnly: true;
  humanConfirmedStrategyOnly: true;
  noAutonomousRoadmapGeneration: true;
  noHiddenProviderSwitching: true;
}

export class DevStrategyMonitor {
  private compacted = false;

  evaluate(): DevelopmentStrategyState {
    const costPressure: StrategyPressure = this.compacted ? 'LOW' : 'MEDIUM';
    const roadmapPressure: StrategyPressure = this.compacted ? 'LOW' : 'MEDIUM';
    return {
      devStrategyActive: true,
      strategyStable: this.compacted,
      costPressure,
      providerEfficiency: this.compacted ? 'HIGH' : 'MEDIUM',
      roadmapPressure,
      providerRoutingDistribution: [
        {providerClass: 'HIGH', count: 3},
        {providerClass: 'MEDIUM', count: 3},
        {providerClass: 'LOW', count: 3},
      ],
      estimatedAvoidedStrategyOverhead: this.compacted ? 3480 : 3240,
      estimatedAvoidedRoadmapExplosion: this.compacted ? 2600 : 2400,
      compactSummary: 'bounded next-focus guidance; no autonomous roadmap generation',
      costHints: ['LOW for summaries', 'MEDIUM for prioritization', 'HIGH for boundary risk only'],
      governanceHints: ['human-confirmed priorities', 'compact rollover', 'roadmap boundary protected'],
      providerHints: ['visible escalation reason', 'cleanup on LOW', 'density analysis on MEDIUM'],
      sprintDensityHints: ['one runtime neighborhood', 'radius 2 maximum', 'compact validation surface'],
      localOnly: true,
      deterministic: true,
      summaryOnly: true,
      boundedStrategyOnly: true,
      humanConfirmedStrategyOnly: true,
      noAutonomousRoadmapGeneration: true,
      noHiddenProviderSwitching: true,
    };
  }

  compactSummary(): DevelopmentStrategyState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class StrategyStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 67);

  constructor(private readonly monitor: DevStrategyMonitor) {
    this.item.command = 'aiDevOs.showDevelopmentStrategy';
  }

  refresh(): DevelopmentStrategyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS STRATEGY_STABLE ${state.strategyStable ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.compactSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CostPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 66);

  constructor(private readonly monitor: DevStrategyMonitor) {
    this.item.command = 'aiDevOs.showCostReductionStrategy';
  }

  refresh(): DevelopmentStrategyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS COST_PRESSURE ${state.costPressure}`;
    this.item.tooltip = `Avoided strategy overhead ${state.estimatedAvoidedStrategyOverhead}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ProviderEfficiencyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 65);

  constructor(private readonly monitor: DevStrategyMonitor) {
    this.item.command = 'aiDevOs.showProviderEfficiencyStrategy';
  }

  refresh(): DevelopmentStrategyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS PROVIDER_EFFICIENCY ${state.providerEfficiency}`;
    this.item.tooltip = state.providerHints.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RoadmapPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 64);

  constructor(private readonly monitor: DevStrategyMonitor) {
    this.item.command = 'aiDevOs.showGovernanceStabilityStrategy';
  }

  refresh(): DevelopmentStrategyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ROADMAP_PRESSURE ${state.roadmapPressure}`;
    this.item.tooltip = `Avoided roadmap explosion ${state.estimatedAvoidedRoadmapExplosion}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}