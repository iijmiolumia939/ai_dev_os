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

  const runProviderBenchmark = vscode.commands.registerCommand('aiDevOs.runProviderBenchmark', async () => {
    const state = monitor.runBenchmark();
    refreshAll();
    await notifications.info(
      'provider-benchmark-run',
      `AI_DEV_OS provider benchmark active; OpenMythos ${state.openMythosLoadResult}.`,
    );
  });

  const compareProviders = vscode.commands.registerCommand('aiDevOs.compareProviders', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS provider comparison: deterministic summary; depth gain ${state.estimatedReasoningDepthGain}.`,
    );
  });

  const showOpenMythosStability = vscode.commands.registerCommand(
    'aiDevOs.showOpenMythosStability',
    async () => {
      const state = governanceStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS OpenMythos stability: ${state.vramRuntimeStability}; load ${state.openMythosLoadResult}.`,
      );
    },
  );

  const showDriftRisk = vscode.commands.registerCommand('aiDevOs.showDriftRisk', async () => {
    const state = driftRiskStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS drift risk: ${state.driftRisk}; architecture ${state.estimatedArchitectureDriftRisk}.`,
    );
  });

  const compactBenchmarkSummary = vscode.commands.registerCommand(
    'aiDevOs.compactBenchmarkSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await vscode.window.showInformationMessage(`AI_DEV_OS compact benchmark summary: ${state.compactSummary}`);
    },
  );

  return [
    runProviderBenchmark,
    compareProviders,
    showOpenMythosStability,
    showDriftRisk,
    compactBenchmarkSummary,
  ];
}
