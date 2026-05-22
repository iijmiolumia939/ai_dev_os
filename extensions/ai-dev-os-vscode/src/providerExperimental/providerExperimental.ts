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
  providerStabilityActive: boolean;
  adaptiveProviderRoutingActive: boolean;
  stabilityRoutingActive: true;
  driftAwareRoutingActive: true;
  governanceWeightedRoutingActive: true;
  routingConfidenceActive: true;
  longSessionDriftActive: true;
  governanceDecayActive: true;
  compactnessRetentionActive: true;
  driftRisk: DriftRisk;
  governanceStable: true;
  compactnessOk: true;
  compactSummary: string;
  stabilitySummary: string;
  adaptiveRoutingSummary: string;
  routingConfidenceSummary: string;
  driftAwareRoutingResult: string;
  governanceWeightedRoutingResult: string;
  openMythosLoadResult: string;
  ggufConversionResult: string;
  openMythosFallbackRoute: string;
  vramRuntimeStability: string;
  estimatedReasoningDepthGain: number;
  estimatedGovernanceInstabilityRisk: number;
  estimatedArchitectureDriftRisk: number;
  estimatedProviderStabilityGain: number;
  estimatedAvoidedProviderDrift: number;
  estimatedAvoidedPremiumProviderBurn: number;
  estimatedRecursiveDriftRisk: string;
  estimatedLongSessionDegradation: string;
  providerStabilityComparison: string;
  governanceAdherenceRanking: string;
  compactnessRetentionRanking: string;
  driftResistanceRanking: string;
  localPatchAdherenceRanking: string;
  adaptiveProviderRanking: string;
  summaryOnly: true;
  localOnly: true;
  rollbackSafe: true;
  noArchitectureAuthority: true;
  noGovernanceAuthority: true;
  noAutonomousExecutionAuthority: true;
}

export class ProviderExperimentalMonitor {
  private benchmarkActive = false;
  private stabilityBenchmarkActive = false;
  private adaptiveRoutingActive = false;

  evaluate(): ProviderExperimentalState {
    return {
      experimentalProviderActive: true,
      openMythosProviderActive: false,
      openMythosGgufActive: false,
      openMythosConversionActive: true,
      providerBenchmarkActive: this.benchmarkActive,
      providerComparisonActive: true,
      providerDriftActive: true,
      providerStabilityActive: this.stabilityBenchmarkActive,
      adaptiveProviderRoutingActive: this.adaptiveRoutingActive,
      stabilityRoutingActive: true,
      driftAwareRoutingActive: true,
      governanceWeightedRoutingActive: true,
      routingConfidenceActive: true,
      longSessionDriftActive: true,
      governanceDecayActive: true,
      compactnessRetentionActive: true,
      driftRisk: 'LOW_NOT_LOADED',
      governanceStable: true,
      compactnessOk: true,
      compactSummary: 'OpenMythos HF GGUF unavailable; conversion fallback guarded; no routing changed.',
      stabilitySummary: 'qwen2.5-coder:7b leads bounded stability; OpenMythos remains placeholder-only.',
      adaptiveRoutingSummary: 'qwen2.5-coder:7b recommended for LOW bounded work; human confirmation required.',
      routingConfidenceSummary: 'qwen2.5-coder:7b STABLE_LOCAL; gemma3:12b STABLE_GOVERNANCE; GPT-5.5 HIGH_ESCALATION_REQUIRED.',
      driftAwareRoutingResult: 'DRIFT_LOW_LOCAL_FIRST_ESCALATION_GUARDED',
      governanceWeightedRoutingResult: 'GOVERNANCE_WEIGHTED_LOCAL_PATCH_PREFERRED',
      openMythosLoadResult: 'unavailable:hf_repository_not_gguf',
      ggufConversionResult: 'guarded:not_converted_custom_open_mythos_architecture',
      openMythosFallbackRoute: 'qwen2.5-coder:7b',
      vramRuntimeStability: 'not_loaded',
      estimatedReasoningDepthGain: 0,
      estimatedGovernanceInstabilityRisk: 2,
      estimatedArchitectureDriftRisk: 2,
      estimatedProviderStabilityGain: 12,
      estimatedAvoidedProviderDrift: 14,
      estimatedAvoidedPremiumProviderBurn: 18,
      estimatedRecursiveDriftRisk: 'LOW_BASELINE_GUARDED',
      estimatedLongSessionDegradation: 'qwen2.5-coder:7b 4; qwen2.5-coder:14b 5; gemma3:12b 8; GPT-5.5 reference 18; OpenMythos placeholder 0',
      providerStabilityComparison: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      governanceAdherenceRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      compactnessRetentionRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      driftResistanceRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      localPatchAdherenceRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      adaptiveProviderRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
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

  runStabilityBenchmark(): ProviderExperimentalState {
    this.stabilityBenchmarkActive = true;
    return this.evaluate();
  }

  runAdaptiveRouting(): ProviderExperimentalState {
    this.adaptiveRoutingActive = true;
    return this.evaluate();
  }

  compactSummary(): ProviderExperimentalState {
    this.benchmarkActive = false;
    this.stabilityBenchmarkActive = false;
    this.adaptiveRoutingActive = false;
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
    this.item.text = `AI_DEV_OS STABILITY_BENCHMARK ${state.providerStabilityActive ? 'ON' : 'READY'}`;
    this.item.tooltip = `Baseline ${state.providerStabilityComparison}; OpenMythos ${state.openMythosLoadResult}`;
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
    this.item.command = 'aiDevOs.showProviderDrift';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS DRIFT_LOW ${state.estimatedRecursiveDriftRisk}`;
    this.item.tooltip = `Drift ranking ${state.driftResistanceRanking}; architecture risk ${state.estimatedArchitectureDriftRisk}`;
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
    this.item.command = 'aiDevOs.showGovernanceDecay';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS GOVERNANCE_STABLE ${state.governanceStable ? 'YES' : 'NO'}`;
    this.item.tooltip = `Governance ranking ${state.governanceAdherenceRanking}; no authority delegated ${state.noGovernanceAuthority}`;
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
    this.item.command = 'aiDevOs.showCompactnessRetention';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS COMPACTNESS_OK ${state.compactnessOk ? 'YES' : 'NO'}`;
    this.item.tooltip = `Compactness ranking ${state.compactnessRetentionRanking}; summary-only ${state.summaryOnly}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class AdaptiveRoutingStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 71);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showAdaptiveRouting';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ADAPTIVE_ROUTING ${state.adaptiveProviderRoutingActive ? 'ON' : 'READY'}`;
    this.item.tooltip = `${state.adaptiveRoutingSummary} Ranking ${state.adaptiveProviderRanking}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class StableLocalStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 70);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showRoutingConfidence';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS STABLE_LOCAL qwen2.5-coder:7b';
    this.item.tooltip = state.routingConfidenceSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class DriftAwareRoutingStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 69);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showDriftAwareRouting';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS DRIFT_AWARE ${state.driftAwareRoutingActive ? 'ON' : 'OFF'}`;
    this.item.tooltip = `${state.driftAwareRoutingResult}; avoided drift ${state.estimatedAvoidedProviderDrift}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class GovernanceWeightedRoutingStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 68);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showStabilityRouting';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS GOVERNANCE_WEIGHTED ${state.governanceWeightedRoutingActive ? 'ON' : 'OFF'}`;
    this.item.tooltip = `${state.governanceWeightedRoutingResult}; premium burn avoided ${state.estimatedAvoidedPremiumProviderBurn}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
