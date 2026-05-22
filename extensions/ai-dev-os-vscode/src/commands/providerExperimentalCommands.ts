import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  AdaptiveRoutingStatusBar,
  BenchmarkActiveStatusBar,
  CompactnessDecayStatusBar,
  DriftAwareRoutingStatusBar,
  DriftRiskStatusBar,
  ExperimentalProviderStatusBar,
  FatigueEscalationPressureStatusBar,
  FatigueLowStatusBar,
  GovernanceWeightedRoutingStatusBar,
  GovernanceStableStatusBar,
  ProviderExperimentalMonitor,
  RecoveryAvailableStatusBar,
  StableLocalStatusBar,
} from '../providerExperimental/providerExperimental';

export function registerProviderExperimentalCommands(
  monitor: ProviderExperimentalMonitor,
  experimentalStatus: ExperimentalProviderStatusBar,
  driftRiskStatus: DriftRiskStatusBar,
  governanceStableStatus: GovernanceStableStatusBar,
  benchmarkActiveStatus: BenchmarkActiveStatusBar,
  adaptiveRoutingStatus: AdaptiveRoutingStatusBar,
  stableLocalStatus: StableLocalStatusBar,
  driftAwareRoutingStatus: DriftAwareRoutingStatusBar,
  governanceWeightedRoutingStatus: GovernanceWeightedRoutingStatusBar,
  fatigueLowStatus: FatigueLowStatusBar,
  escalationPressureStatus: FatigueEscalationPressureStatusBar,
  compactnessDecayStatus: CompactnessDecayStatusBar,
  recoveryAvailableStatus: RecoveryAvailableStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    experimentalStatus.refresh();
    driftRiskStatus.refresh();
    governanceStableStatus.refresh();
    benchmarkActiveStatus.refresh();
    adaptiveRoutingStatus.refresh();
    stableLocalStatus.refresh();
    driftAwareRoutingStatus.refresh();
    governanceWeightedRoutingStatus.refresh();
    fatigueLowStatus.refresh();
    escalationPressureStatus.refresh();
    compactnessDecayStatus.refresh();
    recoveryAvailableStatus.refresh();
  };

  const runProviderBenchmarkAction = async () => {
    const state = monitor.runBenchmark();
    refreshAll();
    await notifications.info(
      'provider-benchmark-run',
      `AI_DEV_OS provider benchmark active; OpenMythos ${state.openMythosLoadResult}.`,
    );
  };

  const runProviderBenchmark = vscode.commands.registerCommand(
    'aiDevOs.runProviderBenchmark',
    runProviderBenchmarkAction,
  );

  const runStabilityBenchmark = vscode.commands.registerCommand(
    'aiDevOs.runStabilityBenchmark',
    async () => {
      const state = monitor.runStabilityBenchmark();
      refreshAll();
      await notifications.info(
        'provider-stability-benchmark-run',
        `AI_DEV_OS stability benchmark active; gain ${state.estimatedProviderStabilityGain}.`,
      );
    },
  );

  const testOpenMythosGguf = vscode.commands.registerCommand(
    'aiDevOs.testOpenMythosGguf',
    runProviderBenchmarkAction,
  );

  const compareProvidersAction = async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS OpenMythos comparison: fallback ${state.openMythosFallbackRoute}; depth gain ${state.estimatedReasoningDepthGain}.`,
    );
  };

  const compareProviders = vscode.commands.registerCommand('aiDevOs.compareProviders', compareProvidersAction);

  const compareOpenMythosProvider = vscode.commands.registerCommand(
    'aiDevOs.compareOpenMythosProvider',
    compareProvidersAction,
  );

  const showOpenMythosStability = vscode.commands.registerCommand(
    'aiDevOs.showOpenMythosStability',
    async () => {
      const state = governanceStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS OpenMythos stability: ${state.vramRuntimeStability}; GGUF ${state.ggufConversionResult}.`,
      );
    },
  );

  const showDriftRiskAction = async () => {
    const state = driftRiskStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS drift risk: ${state.driftRisk}; architecture ${state.estimatedArchitectureDriftRisk}.`,
    );
  };

  const showDriftRisk = vscode.commands.registerCommand('aiDevOs.showDriftRisk', showDriftRiskAction);

  const showProviderDrift = vscode.commands.registerCommand('aiDevOs.showProviderDrift', async () => {
    const state = driftRiskStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS provider drift: ${state.estimatedRecursiveDriftRisk}; ${state.driftResistanceRanking}.`,
    );
  });

  const showGovernanceDecay = vscode.commands.registerCommand('aiDevOs.showGovernanceDecay', async () => {
    const state = governanceStableStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS governance decay: stable; ${state.governanceAdherenceRanking}.`,
    );
  });

  const showCompactnessRetention = vscode.commands.registerCommand(
    'aiDevOs.showCompactnessRetention',
    async () => {
      const state = benchmarkActiveStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS compactness retention: ${state.compactnessRetentionRanking}.`,
      );
    },
  );

  const showOpenMythosDriftRisk = vscode.commands.registerCommand(
    'aiDevOs.showOpenMythosDriftRisk',
    showDriftRiskAction,
  );

  const compactBenchmarkSummary = vscode.commands.registerCommand(
    'aiDevOs.compactBenchmarkSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(`AI_DEV_OS compact benchmark summary: ${state.compactSummary}`);
    },
  );

  const compactOpenMythosSummary = vscode.commands.registerCommand(
    'aiDevOs.compactOpenMythosSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(`AI_DEV_OS compact OpenMythos summary: ${state.compactSummary}`);
    },
  );

  const compactStabilitySummary = vscode.commands.registerCommand(
    'aiDevOs.compactStabilitySummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(`AI_DEV_OS compact stability summary: ${state.stabilitySummary}`);
    },
  );

  const showAdaptiveRouting = vscode.commands.registerCommand('aiDevOs.showAdaptiveRouting', async () => {
    const state = monitor.runAdaptiveRouting();
    refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS adaptive routing: ${state.adaptiveRoutingSummary}`,
    );
  });

  const showRoutingConfidence = vscode.commands.registerCommand(
    'aiDevOs.showRoutingConfidence',
    async () => {
      const state = stableLocalStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS routing confidence: ${state.routingConfidenceSummary}`,
      );
    },
  );

  const showDriftAwareRouting = vscode.commands.registerCommand(
    'aiDevOs.showDriftAwareRouting',
    async () => {
      const state = driftAwareRoutingStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS drift-aware routing: ${state.driftAwareRoutingResult}; avoided drift ${state.estimatedAvoidedProviderDrift}.`,
      );
    },
  );

  const showStabilityRouting = vscode.commands.registerCommand(
    'aiDevOs.showStabilityRouting',
    async () => {
      const state = governanceWeightedRoutingStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS stability routing: ${state.providerStabilityComparison}; ${state.governanceWeightedRoutingResult}.`,
      );
    },
  );

  const compactRoutingRecommendation = vscode.commands.registerCommand(
    'aiDevOs.compactRoutingRecommendation',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS compact routing recommendation: ${state.adaptiveRoutingSummary}`,
      );
    },
  );

  const showProviderFatigue = vscode.commands.registerCommand('aiDevOs.showProviderFatigue', async () => {
    const state = monitor.runProviderFatigue();
    refreshAll();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS provider fatigue: ${state.providerFatigueSummary}`,
    );
  });

  const showEscalationFatigue = vscode.commands.registerCommand(
    'aiDevOs.showEscalationFatigue',
    async () => {
      const state = escalationPressureStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS escalation fatigue: ${state.escalationFatigueSummary}`,
      );
    },
  );

  const showFallbackOscillation = vscode.commands.registerCommand(
    'aiDevOs.showFallbackOscillation',
    async () => {
      const state = fatigueLowStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS fallback oscillation: ${state.fallbackOscillationSummary}`,
      );
    },
  );

  const showCompactnessDecay = vscode.commands.registerCommand(
    'aiDevOs.showCompactnessDecay',
    async () => {
      const state = compactnessDecayStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS compactness decay: ${state.compactnessDecaySummary}`,
      );
    },
  );

  const compactFatigueSummary = vscode.commands.registerCommand(
    'aiDevOs.compactFatigueSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS compact fatigue summary: ${state.providerRecoveryRecommendation}`,
      );
    },
  );

  return [
    runProviderBenchmark,
    runStabilityBenchmark,
    testOpenMythosGguf,
    compareProviders,
    compareOpenMythosProvider,
    showOpenMythosStability,
    showDriftRisk,
    showProviderDrift,
    showGovernanceDecay,
    showCompactnessRetention,
    showOpenMythosDriftRisk,
    compactBenchmarkSummary,
    compactOpenMythosSummary,
    compactStabilitySummary,
    showAdaptiveRouting,
    showRoutingConfidence,
    showDriftAwareRouting,
    showStabilityRouting,
    compactRoutingRecommendation,
    showProviderFatigue,
    showEscalationFatigue,
    showFallbackOscillation,
    showCompactnessDecay,
    compactFatigueSummary,
  ];
}
