import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {ArchitecturePressureStatusBar, RuntimeGraphMonitor} from '../runtimeGraph/runtimeGraph';
import {RuntimeClusterViewProvider} from '../views/runtimeClusterView';
import {RuntimeGraphViewProvider} from '../views/runtimeGraphView';

export function registerRuntimeGraphCommands(
  monitor: RuntimeGraphMonitor,
  statusBar: ArchitecturePressureStatusBar,
  notifications: RateLimitedNotifications,
  graphView: RuntimeGraphViewProvider,
  clusterView: RuntimeClusterViewProvider,
): vscode.Disposable[] {
  const showRuntimeGraph = vscode.commands.registerCommand('aiDevOs.showRuntimeGraph', async () => {
    const state = statusBar.refresh();
    graphView.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS runtime graph: ${state.nodeCount} nodes, ${state.edgeCount} bounded edges.`,
    );
  });

  const showRuntimeClusters = vscode.commands.registerCommand('aiDevOs.showRuntimeClusters', async () => {
    const state = monitor.evaluate();
    clusterView.refresh();
    await vscode.window.showInformationMessage(JSON.stringify(state.clusterSizes, undefined, 2));
  });

  const showContractSurface = vscode.commands.registerCommand('aiDevOs.showContractSurface', async () => {
    const state = monitor.evaluate();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS contract surface: ${state.contractSurfaceSize}; pressure ${state.runtimeApiPressure}.`,
    );
  });

  const showArchitecturePressure = vscode.commands.registerCommand(
    'aiDevOs.showArchitecturePressure',
    async () => {
      const state = statusBar.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS architecture pressure: ${state.architecturePressure}; simplification ${state.simplificationRecommended}.`,
      );
    },
  );

  const showOversizedWarnings = vscode.commands.registerCommand(
    'aiDevOs.showOversizedRuntimeWarnings',
    async () => {
      const state = monitor.evaluate();
      if (state.oversizedRuntimes.length > 0) {
        await notifications.warn(
          'runtime-graph-oversized-warning',
          `AI_DEV_OS oversized runtime clusters: ${state.oversizedRuntimes.join(', ')}.`,
        );
      } else {
        await vscode.window.showInformationMessage('AI_DEV_OS oversized runtime clusters not detected.');
      }
    },
  );

  const compactRuntimeGraph = vscode.commands.registerCommand('aiDevOs.compactRuntimeGraph', async () => {
    const state = monitor.compact();
    graphView.refresh();
    clusterView.refresh();
    await notifications.info(
      'runtime-graph-compacted',
      `AI_DEV_OS compact runtime graph retained ${state.edgeCount} bounded edges.`,
    );
  });

  return [
    showRuntimeGraph,
    showRuntimeClusters,
    showContractSurface,
    showArchitecturePressure,
    showOversizedWarnings,
    compactRuntimeGraph,
  ];
}