import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  BenchmarkActiveStatusBar,
  DriftRiskStatusBar,
  ExperimentalProviderStatusBar,
  GovernanceStableStatusBar,
  ProviderExperimentalMonitor,
} from '../providerExperimental/providerExperimental';

export function registerProviderExperimentalCommands(
  monitor: ProviderExperimentalMonitor,
  experimentalStatus: ExperimentalProviderStatusBar,
  driftRiskStatus: DriftRiskStatusBar,
  governanceStableStatus: GovernanceStableStatusBar,
  benchmarkActiveStatus: BenchmarkActiveStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    experimentalStatus.refresh();
    driftRiskStatus.refresh();
    governanceStableStatus.refresh();
    benchmarkActiveStatus.refresh();
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

  return [
    runProviderBenchmark,
    testOpenMythosGguf,
    compareProviders,
    compareOpenMythosProvider,
    showOpenMythosStability,
    showDriftRisk,
    showOpenMythosDriftRisk,
    compactBenchmarkSummary,
    compactOpenMythosSummary,
  ];
}
