import * as vscode from 'vscode';

export type DriftRisk = 'LOW_NOT_LOADED' | 'MEDIUM_EXPERIMENTAL';

export interface ProviderExperimentalState {
  experimentalProviderActive: true;
  openMythosProviderActive: boolean;
  providerBenchmarkActive: boolean;
  providerComparisonActive: boolean;
  providerDriftActive: true;
  driftRisk: DriftRisk;
  governanceStable: true;
  compactSummary: string;
  openMythosLoadResult: string;
  vramRuntimeStability: string;
  estimatedReasoningDepthGain: number;
  estimatedGovernanceInstabilityRisk: number;
  estimatedArchitectureDriftRisk: number;
  summaryOnly: true;
  localOnly: true;
  rollbackSafe: true;
  noArchitectureAuthority: true;
  noGovernanceAuthority: true;
  noAutonomousExecutionAuthority: true;
}

export class ProviderExperimentalMonitor {
  private benchmarkActive = false;

  evaluate(): ProviderExperimentalState {
    return {
      experimentalProviderActive: true,
      openMythosProviderActive: false,
      providerBenchmarkActive: this.benchmarkActive,
      providerComparisonActive: true,
      providerDriftActive: true,
      driftRisk: 'LOW_NOT_LOADED',
      governanceStable: true,
      compactSummary: 'OpenMythos unavailable; bounded benchmark harness active; no routing changed.',
      openMythosLoadResult: 'unavailable:model_manifest_missing',
      vramRuntimeStability: 'not_loaded',
      estimatedReasoningDepthGain: 0,
      estimatedGovernanceInstabilityRisk: 2,
      estimatedArchitectureDriftRisk: 2,
      summaryOnly: true,
      localOnly: true,
      rollbackSafe: true,
      noArchitectureAuthority: true,
      noGovernanceAuthority: true,
      noAutonomousExecutionAuthority: true,
    };
  }

  runBenchmark(): ProviderExperimentalState {
    this.benchmarkActive = true;
    return this.evaluate();
  }

  compactSummary(): ProviderExperimentalState {
    this.benchmarkActive = false;
    return this.evaluate();
  }
}

export class ExperimentalProviderStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 75);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.runProviderBenchmark';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS EXPERIMENTAL_PROVIDER ${state.experimentalProviderActive ? 'ON' : 'OFF'}`;
    this.item.tooltip = `OpenMythos ${state.openMythosLoadResult}; rollback-safe ${state.rollbackSafe}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class DriftRiskStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 74);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showDriftRisk';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS DRIFT_RISK ${state.driftRisk}`;
    this.item.tooltip = `Architecture drift risk ${state.estimatedArchitectureDriftRisk}; governance risk ${state.estimatedGovernanceInstabilityRisk}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class GovernanceStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 73);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showOpenMythosStability';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS GOVERNANCE_STABLE ${state.governanceStable ? 'YES' : 'NO'}`;
    this.item.tooltip = `No governance authority ${state.noGovernanceAuthority}; no architecture authority ${state.noArchitectureAuthority}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class BenchmarkActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 72);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.compactBenchmarkSummary';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS BENCHMARK_ACTIVE ${state.providerBenchmarkActive ? 'YES' : 'NO'}`;
    this.item.tooltip = `Summary-only ${state.summaryOnly}; local-only ${state.localOnly}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
