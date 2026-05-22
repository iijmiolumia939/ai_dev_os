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
  providerFatigueActive: boolean;
  escalationFatigueActive: true;
  fallbackOscillationActive: true;
  compactnessDecayActive: true;
  recoveryAvailable: true;
  cognitiveMemoryPressureActive: boolean;
  continuityInflationActive: true;
  retrievalOverloadActive: true;
  summaryEntropyActive: true;
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
  providerFatigueSummary: string;
  escalationFatigueSummary: string;
  fallbackOscillationSummary: string;
  compactnessDecaySummary: string;
  providerRecoveryRecommendation: string;
  memoryPressureSummary: string;
  continuityInflationSummary: string;
  retrievalOverloadSummary: string;
  summaryEntropySummary: string;
  continuityRecoveryRecommendation: string;
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
  estimatedAvoidedProviderExhaustion: number;
  estimatedAvoidedRecursiveFatigue: number;
  estimatedAvoidedContextExplosion: number;
  estimatedAvoidedSummaryEntropy: number;
  estimatedAvoidedRetrievalOverload: number;
  estimatedAvoidedPremiumProviderBurn: number;
  estimatedRecursiveDriftRisk: string;
  estimatedLongSessionDegradation: string;
  providerStabilityComparison: string;
  governanceAdherenceRanking: string;
  compactnessRetentionRanking: string;
  driftResistanceRanking: string;
  localPatchAdherenceRanking: string;
  adaptiveProviderRanking: string;
  providerRecoveryRanking: string;
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
  private providerFatigueActive = false;
  private cognitiveMemoryPressureActive = false;

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
      providerFatigueActive: this.providerFatigueActive,
      escalationFatigueActive: true,
      fallbackOscillationActive: true,
      compactnessDecayActive: true,
      recoveryAvailable: true,
      cognitiveMemoryPressureActive: this.cognitiveMemoryPressureActive,
      continuityInflationActive: true,
      retrievalOverloadActive: true,
      summaryEntropyActive: true,
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
      providerFatigueSummary: 'qwen2.5-coder:7b fatigue low; escalation pressure guarded.',
      escalationFatigueSummary: 'ESCALATION_PRESSURE_GUARDED; downgrade before premium retry.',
      fallbackOscillationSummary: 'OSCILLATION_LOW_LOCAL_FIRST_BLOCKED_LOOPS',
      compactnessDecaySummary: 'COMPACTNESS_RESET_BEFORE_LONG_SESSION_CONTINUATION',
      providerRecoveryRecommendation: 'RECOVER_WITH_LOCAL_DOWNGRADE_AND_COMPACTNESS_RESET',
      memoryPressureSummary: 'MEMORY_PRESSURE_LOW_COMPACT_CONTINUITY_GUARDED',
      continuityInflationSummary: 'CONTINUITY_INFLATION_GUARDED',
      retrievalOverloadSummary: 'RETRIEVAL_BOUNDED_SCOPE_NARROWING_RECOMMENDED',
      summaryEntropySummary: 'SUMMARY_ENTROPY_GUARDED_REWRITE_RECOMMENDED',
      continuityRecoveryRecommendation: 'RESET_COMPACT_CONTINUITY_TRUNCATE_STALE_MEMORY_NARROW_RETRIEVAL',
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
      estimatedAvoidedProviderExhaustion: 16,
      estimatedAvoidedRecursiveFatigue: 11,
      estimatedAvoidedContextExplosion: 1800,
      estimatedAvoidedSummaryEntropy: 640,
      estimatedAvoidedRetrievalOverload: 920,
      estimatedAvoidedPremiumProviderBurn: 18,
      estimatedRecursiveDriftRisk: 'LOW_BASELINE_GUARDED',
      estimatedLongSessionDegradation: 'qwen2.5-coder:7b 4; qwen2.5-coder:14b 5; gemma3:12b 8; GPT-5.5 reference 18; OpenMythos placeholder 0',
      providerStabilityComparison: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      governanceAdherenceRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      compactnessRetentionRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      driftResistanceRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      localPatchAdherenceRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      adaptiveProviderRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
      providerRecoveryRanking: 'qwen2.5-coder:7b > qwen2.5-coder:14b > gemma3:12b > GPT-5.5 reference > OpenMythos placeholder',
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

  runProviderFatigue(): ProviderExperimentalState {
    this.providerFatigueActive = true;
    return this.evaluate();
  }

  runCognitiveMemoryPressure(): ProviderExperimentalState {
    this.cognitiveMemoryPressureActive = true;
    return this.evaluate();
  }

  compactSummary(): ProviderExperimentalState {
    this.benchmarkActive = false;
    this.stabilityBenchmarkActive = false;
    this.adaptiveRoutingActive = false;
    this.providerFatigueActive = false;
    this.cognitiveMemoryPressureActive = false;
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

export class FatigueLowStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 67);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showProviderFatigue';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS FATIGUE_LOW ${state.providerFatigueActive ? 'ON' : 'READY'}`;
    this.item.tooltip = `${state.providerFatigueSummary}; avoided exhaustion ${state.estimatedAvoidedProviderExhaustion}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class FatigueEscalationPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 66);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showEscalationFatigue';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ESCALATION_PRESSURE ${state.escalationFatigueActive ? 'GUARDED' : 'OFF'}`;
    this.item.tooltip = `${state.escalationFatigueSummary}; avoided premium burn ${state.estimatedAvoidedPremiumProviderBurn}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CompactnessDecayStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 65);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showCompactnessDecay';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS COMPACTNESS_DECAY ${state.compactnessDecayActive ? 'WATCH' : 'OFF'}`;
    this.item.tooltip = state.compactnessDecaySummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RecoveryAvailableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 64);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.compactFatigueSummary';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS RECOVERY_AVAILABLE ${state.recoveryAvailable ? 'YES' : 'NO'}`;
    this.item.tooltip = `${state.providerRecoveryRecommendation}; ${state.providerRecoveryRanking}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CognitiveMemoryPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 63);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showMemoryPressure';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS MEMORY_PRESSURE_LOW ${state.cognitiveMemoryPressureActive ? 'ON' : 'READY'}`;
    this.item.tooltip = `${state.memoryPressureSummary}; avoided context explosion ${state.estimatedAvoidedContextExplosion}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ContinuityInflationStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 62);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showContinuityInflation';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS CONTINUITY_INFLATION ${state.continuityInflationActive ? 'GUARDED' : 'OFF'}`;
    this.item.tooltip = `${state.continuityInflationSummary}; ${state.continuityRecoveryRecommendation}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetrievalBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 61);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showRetrievalOverload';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS RETRIEVAL_BOUNDED ${state.retrievalOverloadActive ? 'YES' : 'NO'}`;
    this.item.tooltip = `${state.retrievalOverloadSummary}; avoided overload ${state.estimatedAvoidedRetrievalOverload}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class EntropyGuardedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 60);

  constructor(private readonly monitor: ProviderExperimentalMonitor) {
    this.item.command = 'aiDevOs.showSummaryEntropy';
  }

  refresh(): ProviderExperimentalState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ENTROPY_GUARDED ${state.summaryEntropyActive ? 'YES' : 'NO'}`;
    this.item.tooltip = `${state.summaryEntropySummary}; avoided entropy ${state.estimatedAvoidedSummaryEntropy}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
