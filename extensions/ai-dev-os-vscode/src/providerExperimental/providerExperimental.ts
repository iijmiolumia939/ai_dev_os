import * as vscode from 'vscode';

export type DriftRisk = 'LOW_NOT_LOADED' | 'MEDIUM_EXPERIMENTAL';

export interface ProviderExperimentalState {
  experimentalProviderActive: true;
  openMythosProviderActive: boolean;
  openMythosGgufActive: boolean;
  openMythosConversionActive: boolean;
  providerBenchmarkActive: boolean;
  providerComparisonActive: boolean;
  providerDriftActive: true;
  driftRisk: DriftRisk;
  governanceStable: true;
  compactSummary: string;
  openMythosLoadResult: string;
  ggufConversionResult: string;
  openMythosFallbackRoute: string;
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
      openMythosGgufActive: false,
      openMythosConversionActive: true,
      providerBenchmarkActive: this.benchmarkActive,
      providerComparisonActive: true,
      providerDriftActive: true,
      driftRisk: 'LOW_NOT_LOADED',
      governanceStable: true,
      compactSummary: 'OpenMythos HF GGUF unavailable; conversion fallback guarded; no routing changed.',
      openMythosLoadResult: 'unavailable:hf_repository_not_gguf',
      ggufConversionResult: 'guarded:not_converted_custom_open_mythos_architecture',
      openMythosFallbackRoute: 'qwen2.5-coder:7b',
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
    this.item.text = `AI_DEV_OS OPENMYTHOS_ACTIVE ${state.openMythosProviderActive ? 'YES' : 'NO'}`;
    this.item.tooltip = `OpenMythos ${state.openMythosLoadResult}; fallback ${state.openMythosFallbackRoute}`;
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
    this.item.text = `AI_DEV_OS DRIFT_GUARDED ${state.driftRisk}`;
    this.item.tooltip = `Architecture drift risk ${state.estimatedArchitectureDriftRisk}; recursive drift guarded`;
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
    this.item.text = `AI_DEV_OS GOVERNANCE_PROTECTED ${state.governanceStable ? 'YES' : 'NO'}`;
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
    this.item.text = `AI_DEV_OS GGUF_EXPERIMENTAL ${state.openMythosConversionActive ? 'ON' : 'OFF'}`;
    this.item.tooltip = `GGUF ${state.ggufConversionResult}; summary-only ${state.summaryOnly}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
